from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import (
    ImportJob,
    OwnershipRecord,
    Parcel,
    ParcelGeometry,
    ParcelProjectLink,
    ParcelTagLink,
    PipelineStatus,
    Project,
    SourceObservation,
    SourceType,
    Tag,
)
from app.schemas.parcel import ParcelFilterParams, ParcelImportRequest
from app.services.audit import write_audit_log
from app.services.connectors.base import ParcelConnector
from app.services.parcel_validation import normalize_parcel_identifier, validate_parcel_identifier


def list_parcels(db: Session, filters: ParcelFilterParams) -> tuple[list[Parcel], int]:
    query = select(Parcel).options(
        selectinload(Parcel.observations),
        selectinload(Parcel.ownership_records),
        selectinload(Parcel.documents),
    )
    if filters.query:
        pattern = f"%{filters.query}%"
        query = query.where(
            or_(
                Parcel.original_identifier.ilike(pattern),
                Parcel.normalized_identifier.ilike(pattern),
                Parcel.gmina.ilike(pattern),
                Parcel.voivodeship.ilike(pattern),
            )
        )
    if filters.kw_number:
        query = query.where(Parcel.kw_number.ilike(f"%{filters.kw_number}%"))
    if filters.pipeline_status:
        query = query.where(Parcel.pipeline_status == filters.pipeline_status)
    if filters.project_name:
        query = query.join(ParcelProjectLink).join(Project).where(
            Project.name.ilike(f"%{filters.project_name}%")
        )
    if filters.owner_name:
        query = query.join(OwnershipRecord).where(
            OwnershipRecord.owner_name.ilike(f"%{filters.owner_name}%")
        )
    if filters.tag:
        query = query.join(ParcelTagLink).join(Tag).where(Tag.name.ilike(f"%{filters.tag}%"))
    items = db.scalars(query.order_by(Parcel.created_at.desc())).all()
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    return items, total


def get_parcel_or_404(db: Session, parcel_id: int) -> Parcel | None:
    return db.scalar(
        select(Parcel)
        .options(
            selectinload(Parcel.observations),
            selectinload(Parcel.ownership_records),
            selectinload(Parcel.documents),
        )
        .where(Parcel.id == parcel_id, Parcel.deleted_at.is_(None))
    )


def resolve_and_upsert_parcel(
    db: Session,
    raw_identifier: str,
    connector: ParcelConnector,
    *,
    user_email: str | None = None,
) -> Parcel:
    normalized = normalize_parcel_identifier(raw_identifier)
    errors = validate_parcel_identifier(normalized)
    if errors:
        raise ValueError("; ".join(errors))

    resolved = connector.resolve(normalized)
    parcel = db.scalar(select(Parcel).where(Parcel.normalized_identifier == normalized))
    if parcel is None:
        parcel = Parcel(
            original_identifier=raw_identifier,
            normalized_identifier=normalized,
        )
        db.add(parcel)
        db.flush()

    parcel.voivodeship = resolved.voivodeship
    parcel.powiat = resolved.powiat
    parcel.gmina = resolved.gmina
    parcel.obreb = resolved.obreb
    parcel.parcel_number = resolved.parcel_number
    parcel.area_m2 = resolved.area_m2
    parcel.land_use_classification = resolved.land_use_classification
    parcel.centroid_lat = resolved.centroid_lat
    parcel.centroid_lon = resolved.centroid_lon
    parcel.bounding_box = resolved.bounding_box
    parcel.pipeline_status = PipelineStatus.ENRICHED

    if parcel.geometry is None:
        db.add(
            ParcelGeometry(
                parcel=parcel,
                source_name=resolved.source_name,
                geom_wkt=resolved.geometry_wkt,
                centroid_wkt=None,
            )
        )
    for field_name, value in {
        "voivodeship": resolved.voivodeship,
        "powiat": resolved.powiat,
        "gmina": resolved.gmina,
        "obreb": resolved.obreb,
        "parcel_number": resolved.parcel_number,
        "area_m2": resolved.area_m2,
        "land_use_classification": resolved.land_use_classification,
    }.items():
        if value is None:
            continue
        db.add(
            SourceObservation(
                parcel=parcel,
                source_name=resolved.source_name,
                source_type=resolved.source_type,
                field_name=field_name,
                field_value=str(value),
                confidence=resolved.confidence,
                observed_at=datetime.now(UTC),
                source_reference=resolved.source_reference,
            )
        )

    db.commit()
    db.refresh(parcel)
    write_audit_log(
        db,
        action="parcel.resolved",
        entity_type="parcel",
        entity_id=str(parcel.id),
        user_email=user_email,
        details={"source": resolved.source_name, "identifier": normalized},
    )
    return parcel


def create_import_job(
    db: Session, payload: ParcelImportRequest, connector: ParcelConnector
) -> ImportJob:
    job = ImportJob(
        file_name="manual-import",
        status="processing",
        total_rows=len(payload.rows),
        processed_rows=0,
        error_rows=0,
        result_summary={"errors": []},
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    errors: list[dict[str, str]] = []
    for row in payload.rows:
        try:
            parcel = resolve_and_upsert_parcel(db, row.identifier, connector)
            if row.project_name:
                project = db.scalar(select(Project).where(Project.name == row.project_name))
                if project is None:
                    project = Project(name=row.project_name)
                    db.add(project)
                    db.flush()
                existing_link = db.scalar(
                    select(ParcelProjectLink).where(
                        ParcelProjectLink.parcel_id == parcel.id,
                        ParcelProjectLink.project_id == project.id,
                    )
                )
                if existing_link is None:
                    db.add(ParcelProjectLink(parcel_id=parcel.id, project_id=project.id))
                parcel.notes = f"Imported via project {row.project_name}"
            for tag_name in row.tags:
                tag = db.scalar(select(Tag).where(Tag.name == tag_name))
                if tag is None:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.flush()
                existing_tag_link = db.scalar(
                    select(ParcelTagLink).where(
                        ParcelTagLink.parcel_id == parcel.id,
                        ParcelTagLink.tag_id == tag.id,
                    )
                )
                if existing_tag_link is None:
                    db.add(ParcelTagLink(parcel_id=parcel.id, tag_id=tag.id))
        except ValueError as exc:
            job.error_rows += 1
            errors.append({"identifier": row.identifier, "error": str(exc)})
        finally:
            job.processed_rows += 1

    job.status = "completed"
    job.result_summary = {"errors": errors}
    db.commit()
    db.refresh(job)
    write_audit_log(
        db,
        action="import.completed",
        entity_type="import",
        entity_id=str(job.id),
        details={"rows": job.total_rows, "errors": job.error_rows},
    )
    return job

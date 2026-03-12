from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models import User
from app.schemas.parcel import (
    ImportJobRead,
    ParcelFilterParams,
    ParcelImportRequest,
    ParcelListResponse,
    ParcelRead,
    ParcelRefreshResponse,
    ParcelValidateItem,
    ParcelValidationResult,
)
from app.services.connectors.demo_poland import DemoPolandParcelConnector
from app.services.parcel_service import create_import_job, get_parcel_or_404, list_parcels, resolve_and_upsert_parcel
from app.services.parcel_validation import normalize_parcel_identifier, validate_parcel_identifier

router = APIRouter()
connector = DemoPolandParcelConnector()


@router.post("/validate", response_model=list[ParcelValidationResult])
def validate_parcels(payload: list[ParcelValidateItem]) -> list[ParcelValidationResult]:
    results: list[ParcelValidationResult] = []
    for item in payload:
        normalized = normalize_parcel_identifier(item.value)
        errors = validate_parcel_identifier(item.value)
        results.append(
            ParcelValidationResult(
                original=item.value,
                normalized=None if errors else normalized,
                valid=not errors,
                errors=errors,
            )
        )
    return results


@router.post("/import", response_model=ImportJobRead)
def import_parcels(
    payload: ParcelImportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ImportJobRead:
    job = create_import_job(db, payload, connector)
    return ImportJobRead.model_validate(job)


@router.get("", response_model=ParcelListResponse)
def get_parcels(
    query: str | None = Query(default=None),
    project_name: str | None = Query(default=None),
    kw_number: str | None = Query(default=None),
    owner_name: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    pipeline_status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParcelListResponse:
    filters = ParcelFilterParams(
        query=query,
        project_name=project_name,
        kw_number=kw_number,
        owner_name=owner_name,
        tag=tag,
        pipeline_status=pipeline_status,
    )
    items, total = list_parcels(db, filters)
    return ParcelListResponse(items=[ParcelRead.model_validate(item) for item in items], total=total)


@router.get("/{parcel_id}", response_model=ParcelRead)
def get_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParcelRead:
    parcel = get_parcel_or_404(db, parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return ParcelRead.model_validate(parcel)


@router.post("/{parcel_id}/refresh", response_model=ParcelRefreshResponse)
def refresh_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ParcelRefreshResponse:
    parcel = get_parcel_or_404(db, parcel_id)
    if parcel is None:
        raise HTTPException(status_code=404, detail="Parcel not found")
    resolve_and_upsert_parcel(db, parcel.normalized_identifier, connector, user_email=current_user.email)
    return ParcelRefreshResponse(
        parcel_id=parcel_id,
        refreshed_at=datetime.now(UTC),
        source=connector.connector_name,
        confidence=0.85 if settings.demo_mode else 0.5,
    )

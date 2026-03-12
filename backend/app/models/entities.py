from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy import JSON, Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class UserRole(StrEnum):
    ADMIN = "admin"
    ANALYST = "analyst"
    REVIEWER = "reviewer"


class PipelineStatus(StrEnum):
    NEW = "new"
    VALIDATED = "validated"
    ENRICHED = "enriched"
    OWNERSHIP_PENDING = "ownership_pending"
    OWNERSHIP_VERIFIED = "ownership_verified"
    OUTREACH_READY = "outreach_ready"
    ARCHIVED = "archived"


class OwnerType(StrEnum):
    INDIVIDUAL = "individual"
    COMPANY = "company"
    PUBLIC_BODY = "public_body"
    UNKNOWN = "unknown"


class SourceType(StrEnum):
    OFFICIAL_PUBLIC = "official_public"
    USER_SUPPLIED = "user_supplied"
    MANUAL_VERIFIED = "manual_verified"
    DEMO = "demo"


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[UserRole] = mapped_column(Enum(UserRole), unique=True)
    users: Mapped[list[User]] = relationship(back_populates="role")


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Role] = relationship(back_populates="users")


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    parcels: Mapped[list[ParcelProjectLink]] = relationship(back_populates="project")


class Parcel(Base, TimestampMixin):
    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_identifier: Mapped[str] = mapped_column(String(128))
    normalized_identifier: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    voivodeship: Mapped[str | None] = mapped_column(String(128))
    powiat: Mapped[str | None] = mapped_column(String(128))
    gmina: Mapped[str | None] = mapped_column(String(128))
    obreb: Mapped[str | None] = mapped_column(String(128))
    parcel_number: Mapped[str | None] = mapped_column(String(64))
    kw_number: Mapped[str | None] = mapped_column(String(64))
    area_m2: Mapped[float | None] = mapped_column(Float)
    land_use_classification: Mapped[str | None] = mapped_column(String(255))
    centroid_lat: Mapped[float | None] = mapped_column(Float)
    centroid_lon: Mapped[float | None] = mapped_column(Float)
    bounding_box: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    pipeline_status: Mapped[PipelineStatus] = mapped_column(
        Enum(PipelineStatus), default=PipelineStatus.NEW
    )
    notes: Mapped[str | None] = mapped_column(Text)

    geometry: Mapped[ParcelGeometry | None] = relationship(back_populates="parcel", uselist=False)
    observations: Mapped[list[SourceObservation]] = relationship(back_populates="parcel")
    ownership_records: Mapped[list[OwnershipRecord]] = relationship(back_populates="parcel")
    documents: Mapped[list[Document]] = relationship(back_populates="parcel")
    project_links: Mapped[list[ParcelProjectLink]] = relationship(back_populates="parcel")
    tag_links: Mapped[list[ParcelTagLink]] = relationship(back_populates="parcel")


class ParcelGeometry(Base, TimestampMixin):
    __tablename__ = "parcel_geometries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey("parcels.id"), unique=True)
    source_name: Mapped[str] = mapped_column(String(255))
    geom_wkt: Mapped[str | None] = mapped_column(Text)
    geom: Mapped[str | None] = mapped_column(Geometry("MULTIPOLYGON", srid=4326))
    centroid_wkt: Mapped[str | None] = mapped_column(Text)
    parcel: Mapped[Parcel] = relationship(back_populates="geometry")


class SourceObservation(Base, TimestampMixin):
    __tablename__ = "source_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey("parcels.id"))
    source_name: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    field_name: Mapped[str] = mapped_column(String(128))
    field_value: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    source_reference: Mapped[str | None] = mapped_column(Text)
    parcel: Mapped[Parcel] = relationship(back_populates="observations")


class OwnershipRecord(Base, TimestampMixin):
    __tablename__ = "ownership_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey("parcels.id"))
    owner_name: Mapped[str | None] = mapped_column(String(255))
    owner_type: Mapped[OwnerType] = mapped_column(Enum(OwnerType), default=OwnerType.UNKNOWN)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    source_reference: Mapped[str] = mapped_column(Text)
    verified_by: Mapped[str | None] = mapped_column(String(255))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    lawful_basis_note: Mapped[str] = mapped_column(Text)
    parcel: Mapped[Parcel] = relationship(back_populates="ownership_records")


class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int | None] = mapped_column(ForeignKey("parcels.id"))
    document_type: Mapped[str] = mapped_column(String(64))
    file_name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(Text)
    source_reference: Mapped[str | None] = mapped_column(Text)
    uploaded_by: Mapped[str | None] = mapped_column(String(255))
    parcel: Mapped[Parcel | None] = relationship(back_populates="documents")


class ParcelProjectLink(Base, TimestampMixin):
    __tablename__ = "parcel_project_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey("parcels.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    parcel: Mapped[Parcel] = relationship(back_populates="project_links")
    project: Mapped[Project] = relationship(back_populates="parcels")


class ImportJob(Base, TimestampMixin):
    __tablename__ = "imports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(64), default="queued")
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    processed_rows: Mapped[int] = mapped_column(Integer, default=0)
    error_rows: Mapped[int] = mapped_column(Integer, default=0)
    result_summary: Mapped[dict[str, Any] | None] = mapped_column(JSON)


class ExportJob(Base, TimestampMixin):
    __tablename__ = "export_jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    export_type: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(64), default="queued")
    filters: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    file_path: Mapped[str | None] = mapped_column(Text)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_email: Mapped[str | None] = mapped_column(String(255))
    action: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(128))
    entity_id: Mapped[str | None] = mapped_column(String(64))
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    parcel_links: Mapped[list[ParcelTagLink]] = relationship(back_populates="tag")


class ParcelTagLink(Base, TimestampMixin):
    __tablename__ = "parcel_tag_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parcel_id: Mapped[int] = mapped_column(ForeignKey("parcels.id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    parcel: Mapped[Parcel] = relationship(back_populates="tag_links")
    tag: Mapped[Tag] = relationship(back_populates="parcel_links")

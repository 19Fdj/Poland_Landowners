from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.entities import OwnerType, PipelineStatus, SourceType
from app.schemas.common import ORMModel


class ParcelValidateItem(BaseModel):
    value: str = Field(min_length=3, max_length=128)


class ParcelValidationResult(BaseModel):
    original: str
    normalized: str | None
    valid: bool
    errors: list[str] = Field(default_factory=list)


class ParcelImportRow(BaseModel):
    identifier: str
    project_name: str | None = None
    tags: list[str] = Field(default_factory=list)


class ParcelImportRequest(BaseModel):
    rows: list[ParcelImportRow]


class ParcelResolveItem(BaseModel):
    identifier: str


class ParcelResolveResponse(BaseModel):
    original: str
    valid: bool
    normalized: str | None = None
    error: str | None = None
    parcel: ParcelRead | None = None


class SourceObservationRead(ORMModel):
    id: int
    source_name: str
    source_type: SourceType
    field_name: str
    field_value: str
    confidence: float
    observed_at: datetime
    source_reference: str | None


class OwnershipRecordCreate(BaseModel):
    parcel_id: int
    owner_name: str | None = None
    owner_type: OwnerType = OwnerType.UNKNOWN
    source_type: SourceType
    source_reference: str
    verified_by: str | None = None
    verified_at: datetime | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    lawful_basis_note: str = Field(min_length=8)


class OwnershipRecordRead(ORMModel):
    id: int
    parcel_id: int
    owner_name: str | None
    owner_type: OwnerType
    source_type: SourceType
    source_reference: str
    verified_by: str | None
    verified_at: datetime | None
    confidence: float
    lawful_basis_note: str


class DocumentCreate(BaseModel):
    parcel_id: int | None = None
    document_type: str
    file_name: str
    file_path: str
    source_reference: str | None = None
    uploaded_by: str | None = None


class DocumentRead(ORMModel):
    id: int
    parcel_id: int | None
    document_type: str
    file_name: str
    file_path: str
    source_reference: str | None
    uploaded_by: str | None


class ParcelRead(ORMModel):
    id: int
    original_identifier: str
    normalized_identifier: str
    voivodeship: str | None
    powiat: str | None
    gmina: str | None
    obreb: str | None
    parcel_number: str | None
    kw_number: str | None
    area_m2: float | None
    land_use_classification: str | None
    centroid_lat: float | None
    centroid_lon: float | None
    bounding_box: dict[str, Any] | None
    pipeline_status: PipelineStatus
    notes: str | None
    observations: list[SourceObservationRead] = Field(default_factory=list)
    ownership_records: list[OwnershipRecordRead] = Field(default_factory=list)
    documents: list[DocumentRead] = Field(default_factory=list)


class ParcelRefreshResponse(BaseModel):
    parcel_id: int
    refreshed_at: datetime
    source: str
    confidence: float


class ParcelListResponse(BaseModel):
    items: list[ParcelRead]
    total: int


class ExportJobRead(ORMModel):
    id: int
    export_type: str
    status: str
    filters: dict[str, Any] | None
    file_path: str | None


class ImportJobRead(ORMModel):
    id: int
    file_name: str
    status: str
    total_rows: int
    processed_rows: int
    error_rows: int
    result_summary: dict[str, Any] | None


class ParcelFilterParams(BaseModel):
    query: str | None = None
    project_name: str | None = None
    kw_number: str | None = None
    owner_name: str | None = None
    tag: str | None = None
    pipeline_status: PipelineStatus | None = None

    @field_validator("query", "project_name", "kw_number", "owner_name", "tag")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

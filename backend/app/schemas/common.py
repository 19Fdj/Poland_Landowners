from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AuditLogRead(ORMModel):
    id: int
    user_email: str | None
    action: str
    entity_type: str
    entity_id: str | None
    details: dict[str, Any] | None
    created_at: datetime


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int


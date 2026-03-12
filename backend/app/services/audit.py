from typing import Any

from sqlalchemy.orm import Session

from app.models import AuditLog


def write_audit_log(
    db: Session,
    *,
    action: str,
    entity_type: str,
    entity_id: str | None = None,
    user_email: str | None = None,
    details: dict[str, Any] | None = None,
) -> AuditLog:
    audit = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_email=user_email,
        details=details,
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


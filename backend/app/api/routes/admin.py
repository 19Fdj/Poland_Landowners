from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models import AuditLog, Role, User
from app.schemas.admin import UserCreate, UserRead
from app.schemas.common import AuditLogRead
from app.services.audit import write_audit_log

router = APIRouter()


@router.get("/audit-logs", response_model=list[AuditLogRead])
def get_audit_logs(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[AuditLogRead]:
    rows = db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(100)).all()
    return [AuditLogRead.model_validate(row) for row in rows]


@router.get("/settings")
def get_admin_settings(
    current_user: User = Depends(get_current_user),
) -> dict[str, str | bool]:
    return {
        "demo_mode": settings.demo_mode,
        "legal_disclaimer_text": settings.legal_disclaimer_text,
    }


@router.get("/users", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[UserRead]:
    users = db.scalars(select(User).order_by(User.created_at.desc())).all()
    return [UserRead.model_validate(user) for user in users]


@router.post("/users", response_model=UserRead)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    role = db.scalar(select(Role).where(Role.name == payload.role))
    if role is None:
        role = Role(name=payload.role)
        db.add(role)
        db.flush()

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=get_password_hash(payload.password),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    write_audit_log(
        db,
        action="user.created",
        entity_type="user",
        entity_id=str(user.id),
        user_email=current_user.email,
        details={"email": user.email, "role": payload.role},
    )
    return UserRead.model_validate(user)

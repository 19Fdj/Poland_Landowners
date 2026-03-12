from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import OwnershipRecord, User
from app.schemas.parcel import OwnershipRecordCreate, OwnershipRecordRead
from app.services.audit import write_audit_log

router = APIRouter()


@router.post("/ownership-records", response_model=OwnershipRecordRead)
def create_ownership_record(
    payload: OwnershipRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OwnershipRecordRead:
    record = OwnershipRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    write_audit_log(
        db,
        action="ownership.created",
        entity_type="ownership_record",
        entity_id=str(record.id),
        user_email=current_user.email,
        details={"parcel_id": record.parcel_id, "source_type": record.source_type},
    )
    return OwnershipRecordRead.model_validate(record)


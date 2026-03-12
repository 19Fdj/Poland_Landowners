from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Document, User
from app.schemas.parcel import DocumentCreate, DocumentRead
from app.services.audit import write_audit_log

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentRead)
def upload_document(
    payload: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DocumentRead:
    document = Document(**payload.model_dump())
    db.add(document)
    db.commit()
    db.refresh(document)
    write_audit_log(
        db,
        action="document.created",
        entity_type="document",
        entity_id=str(document.id),
        user_email=current_user.email,
        details={"parcel_id": document.parcel_id, "file_name": document.file_name},
    )
    return DocumentRead.model_validate(document)


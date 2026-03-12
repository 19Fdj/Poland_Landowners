from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import ExportJob, User
from app.schemas.parcel import ExportJobRead
from app.services.audit import write_audit_log

router = APIRouter()


@router.get("/exports/{job_id}", response_model=ExportJobRead)
def get_export_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExportJobRead:
    job = db.scalar(select(ExportJob).where(ExportJob.id == job_id))
    if job is None:
        raise HTTPException(status_code=404, detail="Export job not found")
    write_audit_log(
        db,
        action="export.read",
        entity_type="export_job",
        entity_id=str(job.id),
        user_email=current_user.email,
    )
    return ExportJobRead.model_validate(job)


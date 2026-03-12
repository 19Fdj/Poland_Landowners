from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import Base, SessionLocal, engine
from app.models import ExportJob, Role, User, UserRole
from app.services.audit import write_audit_log


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for role_name in UserRole:
            if db.scalar(select(Role).where(Role.name == role_name)) is None:
                db.add(Role(name=role_name))
        db.commit()
        admin_role = db.scalar(select(Role).where(Role.name == UserRole.ADMIN))
        if db.scalar(select(User).where(User.email == "admin@example.com")) is None and admin_role is not None:
            db.add(
                User(
                    email="admin@example.com",
                    password_hash=get_password_hash("password123"),
                    full_name="Admin User",
                    role_id=admin_role.id,
                )
            )
            db.commit()
        if db.scalar(select(ExportJob).where(ExportJob.id == 1)) is None:
            db.add(
                ExportJob(
                    export_type="csv",
                    status="completed",
                    filters={"pipeline_status": "enriched"},
                    file_path="/exports/demo-parcels.csv",
                )
            )
            db.commit()
        write_audit_log(db, action="seed.completed", entity_type="system")
    finally:
        db.close()


if __name__ == "__main__":
    main()


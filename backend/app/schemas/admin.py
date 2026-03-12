from pydantic import BaseModel, EmailStr

from app.models import UserRole
from app.schemas.common import ORMModel


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: UserRole


class UserRead(ORMModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    role_id: int

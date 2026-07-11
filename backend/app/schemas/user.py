from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    nome: str
    email: EmailStr
    role: UserRole = UserRole.viewer
    ativo: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    ativo: Optional[bool] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True

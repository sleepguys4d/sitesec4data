from typing import Optional

from pydantic import BaseModel


class TeamMemberBase(BaseModel):
    nome: str
    cargo: Optional[str] = None
    foto: Optional[str] = None
    bio: Optional[str] = None
    linkedin: Optional[str] = None
    ordem: int = 0
    ativo: bool = True


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberUpdate(BaseModel):
    nome: Optional[str] = None
    cargo: Optional[str] = None
    foto: Optional[str] = None
    bio: Optional[str] = None
    linkedin: Optional[str] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None


class TeamMemberOut(TeamMemberBase):
    id: int

    class Config:
        from_attributes = True

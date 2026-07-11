from typing import Optional

from pydantic import BaseModel


class ServiceBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    icone: str = "shield"
    ordem: int = 0
    ativo: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    icone: Optional[str] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None


class ServiceOut(ServiceBase):
    id: int

    class Config:
        from_attributes = True

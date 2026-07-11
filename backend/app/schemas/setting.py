from typing import Optional

from pydantic import BaseModel


class SettingBase(BaseModel):
    chave: str
    valor: Optional[str] = None
    grupo: str = "geral"
    descricao: Optional[str] = None


class SettingUpdate(BaseModel):
    valor: Optional[str] = None
    descricao: Optional[str] = None


class SettingOut(SettingBase):
    id: int

    class Config:
        from_attributes = True

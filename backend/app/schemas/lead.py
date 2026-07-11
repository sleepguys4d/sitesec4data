from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.lead import EstadoLead


class LeadCreate(BaseModel):
    nome: str
    email: EmailStr
    empresa: Optional[str] = None
    telefone: Optional[str] = None
    tipo_pedido: Optional[str] = None
    mensagem: Optional[str] = None


class LeadUpdate(BaseModel):
    estado: Optional[EstadoLead] = None
    notas_internas: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    empresa: Optional[str] = None
    telefone: Optional[str] = None
    tipo_pedido: Optional[str] = None
    mensagem: Optional[str] = None
    estado: EstadoLead
    notas_internas: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum

from app.core.database import Base


class EstadoLead(str, enum.Enum):
    novo = "novo"
    em_contacto = "em_contacto"
    convertido = "convertido"
    arquivado = "arquivado"


class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(180), nullable=False)
    empresa = Column(String(150))
    telefone = Column(String(40))
    tipo_pedido = Column(String(80))
    mensagem = Column(Text)
    estado = Column(Enum(EstadoLead), default=EstadoLead.novo)
    notas_internas = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Text, Boolean

from app.core.database import Base


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text)
    icone = Column(String(60), default="shield")
    ordem = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

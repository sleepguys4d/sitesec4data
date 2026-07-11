from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(120), unique=True, index=True, nullable=False)
    valor = Column(Text)
    grupo = Column(String(60), default="geral")
    descricao = Column(String(255))

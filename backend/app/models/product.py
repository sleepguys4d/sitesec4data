from sqlalchemy import Column, Integer, String, Text, Boolean, JSON

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    tagline = Column(String(200))
    descricao = Column(Text)
    features = Column(JSON, default=list)
    link_externo = Column(String(255))
    icone = Column(String(60), default="cpu")
    ordem = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

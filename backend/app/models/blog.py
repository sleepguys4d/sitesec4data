import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum

from app.core.database import Base


class EstadoPost(str, enum.Enum):
    rascunho = "rascunho"
    publicado = "publicado"


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    slug = Column(String(220), unique=True, index=True, nullable=False)
    resumo = Column(String(400))
    conteudo = Column(Text, nullable=False)
    imagem_capa = Column(Text)
    categoria = Column(String(80))
    autor = Column(String(120))
    estado = Column(Enum(EstadoPost), default=EstadoPost.rascunho)
    publicado_em = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

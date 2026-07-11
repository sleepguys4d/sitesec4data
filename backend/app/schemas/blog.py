from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.blog import EstadoPost


class BlogPostBase(BaseModel):
    titulo: str
    slug: str
    resumo: Optional[str] = None
    conteudo: str
    imagem_capa: Optional[str] = None
    categoria: Optional[str] = None
    autor: Optional[str] = None
    estado: EstadoPost = EstadoPost.rascunho


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostUpdate(BaseModel):
    titulo: Optional[str] = None
    slug: Optional[str] = None
    resumo: Optional[str] = None
    conteudo: Optional[str] = None
    imagem_capa: Optional[str] = None
    categoria: Optional[str] = None
    autor: Optional[str] = None
    estado: Optional[EstadoPost] = None


class BlogPostOut(BlogPostBase):
    id: int
    publicado_em: Optional[datetime] = None
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True

from typing import Optional

from pydantic import BaseModel


class TestimonialBase(BaseModel):
    nome: str
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    texto: str
    foto: Optional[str] = None
    ordem: int = 0
    ativo: bool = True


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    nome: Optional[str] = None
    empresa: Optional[str] = None
    cargo: Optional[str] = None
    texto: Optional[str] = None
    foto: Optional[str] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None


class TestimonialOut(TestimonialBase):
    id: int

    class Config:
        from_attributes = True

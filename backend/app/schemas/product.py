from typing import Optional, List

from pydantic import BaseModel


class ProductBase(BaseModel):
    nome: str
    tagline: Optional[str] = None
    descricao: Optional[str] = None
    features: List[str] = []
    link_externo: Optional[str] = None
    icone: str = "cpu"
    ordem: int = 0
    ativo: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    nome: Optional[str] = None
    tagline: Optional[str] = None
    descricao: Optional[str] = None
    features: Optional[List[str]] = None
    link_externo: Optional[str] = None
    icone: Optional[str] = None
    ordem: Optional[int] = None
    ativo: Optional[bool] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True

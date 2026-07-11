from sqlalchemy import Column, Integer, String, Text, Boolean

from app.core.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    empresa = Column(String(150))
    cargo = Column(String(120))
    texto = Column(Text, nullable=False)
    foto = Column(Text)
    ordem = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

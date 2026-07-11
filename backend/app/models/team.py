from sqlalchemy import Column, Integer, String, Text, Boolean

from app.core.database import Base


class TeamMember(Base):
    __tablename__ = "team_members"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    cargo = Column(String(150))
    foto = Column(Text)
    bio = Column(Text)
    linkedin = Column(String(255))
    ordem = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

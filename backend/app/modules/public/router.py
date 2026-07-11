from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.blog import BlogPost, EstadoPost
from app.models.service import Service
from app.models.product import Product
from app.models.team import TeamMember
from app.models.testimonial import Testimonial
from app.models.setting import Setting
from app.schemas.blog import BlogPostOut
from app.schemas.service import ServiceOut
from app.schemas.product import ProductOut
from app.schemas.team import TeamMemberOut
from app.schemas.testimonial import TestimonialOut

router = APIRouter()


@router.get("/blog", response_model=list[BlogPostOut])
def blog_publico(db: Session = Depends(get_db)):
    return db.query(BlogPost).filter(BlogPost.estado == EstadoPost.publicado).order_by(BlogPost.publicado_em.desc()).all()


@router.get("/blog/{slug}", response_model=BlogPostOut)
def blog_post_publico(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug, BlogPost.estado == EstadoPost.publicado).first()
    if not post:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")
    return post


@router.get("/services", response_model=list[ServiceOut])
def services_publico(db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.ativo == True).order_by(Service.ordem).all()  # noqa: E712


@router.get("/products", response_model=list[ProductOut])
def products_publico(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.ativo == True).order_by(Product.ordem).all()  # noqa: E712


@router.get("/team", response_model=list[TeamMemberOut])
def team_publico(db: Session = Depends(get_db)):
    return db.query(TeamMember).filter(TeamMember.ativo == True).order_by(TeamMember.ordem).all()  # noqa: E712


@router.get("/testimonials", response_model=list[TestimonialOut])
def testimonials_publico(db: Session = Depends(get_db)):
    return db.query(Testimonial).filter(Testimonial.ativo == True).order_by(Testimonial.ordem).all()  # noqa: E712


@router.get("/settings")
def settings_publico(db: Session = Depends(get_db)):
    items = db.query(Setting).all()
    return {s.chave: s.valor for s in items}

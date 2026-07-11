from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.blog import BlogPost, EstadoPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogPostOut

router = APIRouter()


@router.get("/", response_model=list[BlogPostOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(BlogPost).order_by(BlogPost.criado_em.desc()).all()


@router.post("/", response_model=BlogPostOut)
def criar(payload: BlogPostCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    if db.query(BlogPost).filter(BlogPost.slug == payload.slug).first():
        raise HTTPException(status_code=400, detail="Já existe um artigo com este slug")
    post = BlogPost(**payload.model_dump())
    if post.estado == EstadoPost.publicado:
        post.publicado_em = datetime.utcnow()
    db.add(post); db.commit(); db.refresh(post)
    return post


@router.put("/{post_id}", response_model=BlogPostOut)
def atualizar(post_id: int, payload: BlogPostUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(post, field, value)
    if data.get("estado") == EstadoPost.publicado and not post.publicado_em:
        post.publicado_em = datetime.utcnow()
    db.commit(); db.refresh(post)
    return post


@router.delete("/{post_id}")
def apagar(post_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")
    db.delete(post); db.commit()
    return {"ok": True}

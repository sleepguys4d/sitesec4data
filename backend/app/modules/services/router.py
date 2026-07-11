from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceOut

router = APIRouter()


@router.get("/", response_model=list[ServiceOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Service).order_by(Service.ordem).all()


@router.post("/", response_model=ServiceOut)
def criar(payload: ServiceCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = Service(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ServiceOut)
def atualizar(item_id: int, payload: ServiceUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = db.query(Service).filter(Service.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Serviço não encontrado(a)")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item


@router.delete("/{item_id}")
def apagar(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    item = db.query(Service).filter(Service.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Serviço não encontrado(a)")
    db.delete(item); db.commit()
    return {"ok": True}

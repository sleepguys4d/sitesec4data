from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Product).order_by(Product.ordem).all()


@router.post("/", response_model=ProductOut)
def criar(payload: ProductCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = Product(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ProductOut)
def atualizar(item_id: int, payload: ProductUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = db.query(Product).filter(Product.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado(a)")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item


@router.delete("/{item_id}")
def apagar(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    item = db.query(Product).filter(Product.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Produto não encontrado(a)")
    db.delete(item); db.commit()
    return {"ok": True}

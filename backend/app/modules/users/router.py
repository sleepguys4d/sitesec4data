from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter()


@router.get("/", response_model=list[UserOut])
def listar(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    return db.query(User).order_by(User.id).all()


@router.post("/", response_model=UserOut)
def criar(payload: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Já existe um utilizador com este email")
    user = User(
        nome=payload.nome, email=payload.email, role=payload.role,
        ativo=payload.ativo, password_hash=hash_password(payload.password),
    )
    db.add(user); db.commit(); db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserOut)
def atualizar(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    data = payload.model_dump(exclude_unset=True)
    if data.get("password"):
        user.password_hash = hash_password(data.pop("password"))
    else:
        data.pop("password", None)
    for field, value in data.items():
        setattr(user, field, value)
    db.commit(); db.refresh(user)
    return user


@router.delete("/{user_id}")
def apagar(user_id: int, db: Session = Depends(get_db), current: User = Depends(require_roles(UserRole.admin))):
    if user_id == current.id:
        raise HTTPException(status_code=400, detail="Não é possível remover o próprio utilizador")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado")
    db.delete(user); db.commit()
    return {"ok": True}

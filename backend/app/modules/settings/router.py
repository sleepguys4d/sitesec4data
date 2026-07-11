from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.setting import Setting
from app.schemas.setting import SettingUpdate, SettingOut

router = APIRouter()


@router.get("/", response_model=list[SettingOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Setting).order_by(Setting.grupo, Setting.chave).all()


@router.put("/{chave}", response_model=SettingOut)
def atualizar(chave: str, payload: SettingUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = db.query(Setting).filter(Setting.chave == chave).first()
    if not item:
        raise HTTPException(status_code=404, detail="Definição não encontrada")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item

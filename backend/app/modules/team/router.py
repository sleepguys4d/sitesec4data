from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.team import TeamMember
from app.schemas.team import TeamMemberCreate, TeamMemberUpdate, TeamMemberOut

router = APIRouter()


@router.get("/", response_model=list[TeamMemberOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(TeamMember).order_by(TeamMember.ordem).all()


@router.post("/", response_model=TeamMemberOut)
def criar(payload: TeamMemberCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = TeamMember(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item


@router.put("/{item_id}", response_model=TeamMemberOut)
def atualizar(item_id: int, payload: TeamMemberUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin, UserRole.editor))):
    item = db.query(TeamMember).filter(TeamMember.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Membro da equipa não encontrado(a)")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item


@router.delete("/{item_id}")
def apagar(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    item = db.query(TeamMember).filter(TeamMember.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Membro da equipa não encontrado(a)")
    db.delete(item); db.commit()
    return {"ok": True}

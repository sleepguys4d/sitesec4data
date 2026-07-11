from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user
from app.models.user import User, UserRole
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate, LeadOut

router = APIRouter()


@router.post("/", response_model=LeadOut)
def criar_publico(payload: LeadCreate, db: Session = Depends(get_db)):
    """Endpoint público — recebe as submissões do formulário de contacto do site."""
    lead = Lead(**payload.model_dump())
    db.add(lead); db.commit(); db.refresh(lead)
    return lead


@router.get("/", response_model=list[LeadOut])
def listar(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Lead).order_by(Lead.criado_em.desc()).all()


@router.put("/{lead_id}", response_model=LeadOut)
def atualizar(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Contacto não encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    db.commit(); db.refresh(lead)
    return lead


@router.delete("/{lead_id}")
def apagar(lead_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.admin))):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Contacto não encontrado")
    db.delete(lead); db.commit()
    return {"ok": True}

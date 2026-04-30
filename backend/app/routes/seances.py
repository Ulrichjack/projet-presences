from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.seance import SeanceCreate, SeanceResponse
from app.services import seance_service

# --- IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_admin, obtenir_utilisateur_actuel

router = APIRouter(prefix="/seances", tags=["Séances"])

# 🔒 ADMIN SEULEMENT
@router.post("/", response_model=SeanceResponse, status_code=201)
def creer_seance(seance: SeanceCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return seance_service.creer_seance(db=db, seance=seance)

# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/", response_model=list[SeanceResponse])
def lire_seances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return seance_service.get_seances(db=db, skip=skip, limit=limit)

# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/{seance_id}", response_model=SeanceResponse)
def lire_seance_par_id(seance_id: int, db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return seance_service.get_seance_par_id(db=db, seance_id=seance_id)

# 🔒 ADMIN SEULEMENT
@router.put("/{seance_id}", response_model=SeanceResponse)
def modifier_seance(seance_id: int, seance: SeanceCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return seance_service.modifier_seance(db=db, seance_id=seance_id, seance_update=seance)

# 🔒 ADMIN SEULEMENT
@router.delete("/{seance_id}")
def supprimer_seance(seance_id: int, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return seance_service.supprimer_seance(db=db, seance_id=seance_id)
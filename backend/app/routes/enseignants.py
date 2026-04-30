from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enseignant import EnseignantResponse, EnseignantCreate
from app.services import enseignant_service

# --- IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_admin, obtenir_utilisateur_actuel

router = APIRouter(prefix="/enseignants", tags=["Enseignants"])

# 🔒 ADMIN SEULEMENT
@router.post("/", response_model=EnseignantResponse, status_code=201)
def creer_enseignant(enseignant: EnseignantCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return enseignant_service.creer_enseignant(db=db, enseignant=enseignant)

# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/", response_model=list[EnseignantResponse])
def lire_enseignants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return enseignant_service.get_enseignant(db=db, skip=skip, limit=limit)

# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/{enseignant_id}", response_model=EnseignantResponse)
def lire_enseignant_par_id(enseignant_id: int, db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return enseignant_service.get_enseignant_par_id(db=db, enseignant_id=enseignant_id)

# 🔒 ADMIN SEULEMENT
@router.put("/{enseignant_id}", response_model=EnseignantResponse)
def modifier_enseignant(enseignant_id: int, enseignant: EnseignantCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return enseignant_service.modifier_enseignant(db=db, enseignant_id=enseignant_id, enseignant_update=enseignant)

# 🔒 ADMIN SEULEMENT
@router.delete("/{enseignant_id}")
def supprimer_enseignant(enseignant_id: int, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return enseignant_service.supprimer_enseignant(db=db, enseignant_id=enseignant_id)
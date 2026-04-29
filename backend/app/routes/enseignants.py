# app/routes/enseignants.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enseignant import EnseignantResponse, EnseignantCreate
from app.services import enseignant_service

router = APIRouter(
    prefix="/enseignants",
    tags=["Enseignants"]
)

# 1. CRÉER
@router.post("/", response_model=EnseignantResponse, status_code=201)
def creer_enseignant(enseignant: EnseignantCreate, db: Session = Depends(get_db)):
    return enseignant_service.creer_enseignant(db=db, enseignant=enseignant)

# 2. LIRE TOUT
@router.get("/", response_model=list[EnseignantResponse])
def lire_enseignants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return enseignant_service.get_enseignant(db=db, skip=skip, limit=limit)

# 3. LIRE UN SEUL
@router.get("/{enseignant_id}", response_model=EnseignantResponse)
def lire_enseignant_par_id(enseignant_id: int, db: Session = Depends(get_db)):
    return enseignant_service.get_enseignant_par_id(db=db, enseignant_id=enseignant_id)

# 4. MODIFIER
@router.put("/{enseignant_id}", response_model=EnseignantResponse)
def modifier_enseignant(enseignant_id: int, enseignant: EnseignantCreate, db: Session = Depends(get_db)):
    return enseignant_service.modifier_enseignant(db=db, enseignant_id=enseignant_id, enseignant_update=enseignant)

# 5. SUPPRIMER
@router.delete("/{enseignant_id}")
def supprimer_enseignant(enseignant_id: int, db: Session = Depends(get_db)):
    return enseignant_service.supprimer_enseignant(db=db, enseignant_id=enseignant_id)
# app/routes/etudiants.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# On importe notre base de données, nos schémas et notre tout nouveau service !
from app.database import get_db
from app.schemas.etudiant import EtudiantCreate, EtudiantResponse
from app.services import etudiant_service

# On crée le routeur (le préfixe permet de ne pas répéter "/etudiants" partout)
router = APIRouter(
    prefix="/etudiants",
    tags=["Étudiants"]
)

# --- 1. CRÉER ---
@router.post("/", response_model=EtudiantResponse, status_code=201)
def creer_etudiant(etudiant: EtudiantCreate, db: Session = Depends(get_db)):
    return etudiant_service.creer_etudiant(db=db, etudiant=etudiant)

# --- 2. LIRE TOUT (Avec ta pagination !) ---
@router.get("/", response_model=list[EtudiantResponse])
def lire_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return etudiant_service.get_etudiant(db=db, skip=skip, limit=limit)

# --- 3. LIRE UN SEUL (Par ID) ---
@router.get("/{etudiant_id}", response_model=EtudiantResponse)
def lire_etudiant_par_id(etudiant_id: int, db: Session = Depends(get_db)):
    return etudiant_service.get_etudiant_par_id(db=db, etudiant_id=etudiant_id)

# --- 4. MODIFIER ---
@router.put("/{etudiant_id}", response_model=EtudiantResponse)
def modifier_etudiant(etudiant_id: int, etudiant: EtudiantCreate, db: Session = Depends(get_db)):
    return etudiant_service.modifier_etudiant(db=db, etudiant_id=etudiant_id, etudiant_update=etudiant)

# --- 5. SUPPRIMER ---
@router.delete("/{etudiant_id}")
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    return etudiant_service.supprimer_etudiant(db=db, etudiant_id=etudiant_id)
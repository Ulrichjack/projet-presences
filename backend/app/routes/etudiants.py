from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.etudiant import EtudiantCreate, EtudiantResponse
from app.services import etudiant_service
from fastapi import HTTPException

# --- IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_admin, obtenir_utilisateur_actuel, verifier_prof_ou_admin

router = APIRouter(prefix="/etudiants", tags=["Étudiants"])

# 🔒 ADMIN SEULEMENT
@router.post("/", response_model=EtudiantResponse, status_code=201)
def creer_etudiant(etudiant: EtudiantCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return etudiant_service.creer_etudiant(db=db, etudiant=etudiant)

# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/", response_model=list[EtudiantResponse])
def lire_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), prof = Depends(verifier_prof_ou_admin)):
    return etudiant_service.get_etudiant(db=db, skip=skip, limit=limit)

# 🔓 TOUT LE MONDE, MAIS L'ÉTUDIANT NE VOIT QUE LUI-MÊME
@router.get("/{etudiant_id}", response_model=EtudiantResponse)
def lire_etudiant_par_id(etudiant_id: int, db: Session = Depends(get_db), user=Depends(obtenir_utilisateur_actuel)):
    # Si c'est un étudiant et qu'il essaie de regarder le profil d'un autre (ID différent) -> DEHORS !
    if user.role == "ETUDIANT" and user.id != etudiant_id:
        raise HTTPException(status_code=403, detail="Petit curieux ! Tu ne peux voir que ton propre profil.")

    return etudiant_service.get_etudiant_par_id(db=db, etudiant_id=etudiant_id)
# 🔒 ADMIN SEULEMENT
@router.put("/{etudiant_id}", response_model=EtudiantResponse)
def modifier_etudiant(etudiant_id: int, etudiant: EtudiantCreate, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return etudiant_service.modifier_etudiant(db=db, etudiant_id=etudiant_id, etudiant_update=etudiant)

# 🔒 ADMIN SEULEMENT
@router.delete("/{etudiant_id}")
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return etudiant_service.supprimer_etudiant(db=db, etudiant_id=etudiant_id)
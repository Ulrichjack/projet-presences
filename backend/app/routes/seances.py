from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.seance import Seance
from app.models.inscription import Inscription # 👈 NOUVEL IMPORT ICI !
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


@router.get("/mes-seances", response_model=list[SeanceResponse])
def lire_mes_seances(db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return db.query(Seance).filter(Seance.enseignant_id == user.id).all()


@router.get("/mon-emploi-du-temps", response_model=list[SeanceResponse])
def lire_mon_emploi_du_temps(db: Session = Depends(get_db), user=Depends(obtenir_utilisateur_actuel)):
    # 1. Trouver les cours où l'étudiant est inscrit
    mes_inscriptions = db.query(Inscription).filter(Inscription.etudiant_id == user.id).all()
    mes_cours_ids = [i.cours_id for i in mes_inscriptions]

    # 2. Renvoyer les séances de ces cours
    return db.query(Seance).filter(Seance.cours_id.in_(mes_cours_ids)).all()

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
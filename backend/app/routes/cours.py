from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cours import Cours
from app.schemas.cours import CoursCreate, CoursResponse
from app.services import cours_service
from app.models.seance import Seance
# --- NOUVEAUX IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_admin, obtenir_utilisateur_actuel

router = APIRouter(prefix="/cours", tags=["Cours"])

# VERROUILLÉ : Seul un ADMIN peut créer un cours
@router.post("/", response_model=CoursResponse, status_code=status.HTTP_201_CREATED)
def creer_cours(
    cours: CoursCreate,
    db: Session = Depends(get_db),
    admin = Depends(verifier_admin) # <-- Le videur Admin est ici !
):
    return cours_service.creer_cours(db=db, cours=cours)

#  OUVERT AUX CONNECTÉS : Tout le monde (connecté) peut voir les cours
@router.get("/", response_model=list[CoursResponse])
def lire_les_cours(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    utilisateur = Depends(obtenir_utilisateur_actuel) # <-- Le videur "Connecté" est ici !
):
    return cours_service.get_cours(db=db, skip=skip, limit=limit)


@router.get("/mes-cours", response_model=list[CoursResponse])
def lire_mes_cours(db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    # On cherche toutes les séances données par le prof connecté
    seances_du_prof = db.query(Seance).filter(Seance.enseignant_id == user.id).all()
    # On extrait les IDs uniques des cours
    cours_ids = {s.cours_id for s in seances_du_prof}
    # On retourne les cours correspondants
    return db.query(Cours).filter(Cours.id.in_(cours_ids)).all()

@router.get("/{cours_id}", response_model=CoursResponse)
def lire_cours_par_id(
    cours_id: int,
    db: Session = Depends(get_db),
    utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return cours_service.get_cours_par_id(db=db, cours_id=cours_id)

# VERROUILLÉ : Seul un ADMIN peut modifier
@router.put("/{cours_id}", response_model=CoursResponse)
def modifier_cours(
    cours_id: int, cours: CoursCreate,
    db: Session = Depends(get_db),
    admin = Depends(verifier_admin)
):
    return cours_service.modifier_cours(db=db, cours_id=cours_id, cours_update=cours)

#  VERROUILLÉ : Seul un ADMIN peut supprimer
@router.delete("/{cours_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_cours(
    cours_id: int,
    db: Session = Depends(get_db),
    admin = Depends(verifier_admin)
):
    cours_service.supprimer_cours(db=db, cours_id=cours_id)
    return


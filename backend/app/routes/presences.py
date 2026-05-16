from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.presence import PresenceCreate, PresenceResponse
from app.services import presence_service

# --- IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_prof_ou_admin, obtenir_utilisateur_actuel

router = APIRouter(
    prefix="/presences",
    tags=["Présences"],
)

# 🔒 PROF / ADMIN SEULEMENT
@router.post("/", response_model=PresenceResponse, status_code=201)
def marquer_presence(
        presence: PresenceCreate,
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    return presence_service.marquer_presence(db=db, presence=presence)


# 🔒 PROF / ADMIN SEULEMENT
@router.get("/", response_model=list[PresenceResponse])
def lire_presences(
        skip: int = 0,
        limit: int = 1000,
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    # Le service s'occupe d'ajouter les absents automatiquement !
    return presence_service.get_presences(db=db, skip=skip, limit=limit)


# 🔓 ACCESSIBLE AUX ÉTUDIANTS
@router.get("/mes-presences", response_model=list[PresenceResponse])
def lire_mes_presences(
        db: Session = Depends(get_db),
        user=Depends(obtenir_utilisateur_actuel)
):
    if user.role != "ETUDIANT":
        raise HTTPException(status_code=403, detail="Cette route est réservée aux étudiants.")
    return presence_service.get_presences_par_etudiant(db, etudiant_id=user.id)


# ==========================================================
# 🚀 ROUTE : POUR L'HISTORIQUE DU PROFESSEUR
# ==========================================================
@router.get("/mes-cours", response_model=list[PresenceResponse])
def lire_presences_de_mes_cours(
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    # Le service s'occupe de filtrer et d'ajouter les absents !
    return presence_service.get_presences_de_mes_cours(db=db, prof_id=user.id)


# 🔒 PROF / ADMIN SEULEMENT (Doit rester EN DESSOUS des autres GET !)
@router.get("/{presence_id}", response_model=PresenceResponse)
def lire_presence_par_id(
        presence_id: int,
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    return presence_service.get_presence_par_id(db=db, presence_id=presence_id)


# 🔒 PROF / ADMIN SEULEMENT
@router.put("/{presence_id}", response_model=PresenceResponse)
def modifier_presence(
        presence_id: int,
        presence: PresenceCreate,
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    return presence_service.modifier_presence(
        db=db, presence_id=presence_id, presence_update=presence
    )


# 🔒 PROF / ADMIN SEULEMENT
@router.delete("/{presence_id}")
def supprimer_presence(
        presence_id: int,
        db: Session = Depends(get_db),
        user=Depends(verifier_prof_ou_admin)
):
    return presence_service.supprimer_presence(db=db, presence_id=presence_id)
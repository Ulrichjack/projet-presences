from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models.presence import Presence
from app.models.seance import Seance
from app.models.inscription import Inscription
from app.schemas.presence import PresenceCreate


def marquer_presence(db: Session, presence: PresenceCreate):
    # Sécurité : Un étudiant ne peut pas pointer deux fois pour la même séance !
    presence_existante = db.query(Presence).filter(
        Presence.etudiant_id == presence.etudiant_id,
        Presence.seance_id == presence.seance_id
    ).first()

    if presence_existante:
        raise HTTPException(status_code=400, detail="L'étudiant a déjà été pointé pour cette séance.")

    nouvelle_presence = Presence(**presence.model_dump())
    db.add(nouvelle_presence)
    db.commit()
    db.refresh(nouvelle_presence)
    return nouvelle_presence


# --- LA MAGIE EST ICI : On calcule les absents à la volée ---
def _ajouter_absents(db: Session, presences_reelles: list, seances_filtrees: list = None):
    maintenant = datetime.utcnow()

    # Si on ne filtre pas les séances, on prend toutes les séances terminées
    if seances_filtrees is None:
        seances_terminees = db.query(Seance).filter(Seance.date_heure_fin < maintenant).all()
    else:
        seances_terminees = [s for s in seances_filtrees if s.date_heure_fin < maintenant]

    toutes_les_presences = list(presences_reelles)

    for seance in seances_terminees:
        # On cherche qui est inscrit à ce cours
        inscriptions = db.query(Inscription).filter(Inscription.cours_id == seance.cours_id).all()

        for ins in inscriptions:
            # Est-ce que cet étudiant a pointé à cette séance ?
            a_pointe = any(p.etudiant_id == ins.etudiant_id and p.seance_id == seance.id for p in presences_reelles)

            # S'il n'a pas pointé, on crée une "fausse" présence avec le statut ABSENT
            if not a_pointe:
                fausse_presence = Presence(
                    id=0,  # ID 0 pour dire que ce n'est pas en base
                    etudiant_id=ins.etudiant_id,
                    seance_id=seance.id,
                    statut="Absent",
                    methode_pointage="Non pointé",
                    heure_pointage=seance.date_heure_fin  # On met l'heure de fin du cours
                )
                toutes_les_presences.append(fausse_presence)

    return toutes_les_presences


# ------------------------------------------------------------

def get_presences(db: Session, skip: int = 0, limit: int = 1000):
    presences_reelles = db.query(Presence).offset(skip).limit(limit).all()
    return _ajouter_absents(db, presences_reelles)


def get_presences_de_mes_cours(db: Session, prof_id: int):
    # 1. Trouver toutes les séances de ce prof
    mes_seances = db.query(Seance).filter(Seance.enseignant_id == prof_id).all()
    mes_seances_ids = [s.id for s in mes_seances]

    # 2. Récupérer les présences réelles
    presences_reelles = db.query(Presence).filter(Presence.seance_id.in_(mes_seances_ids)).all()

    # 3. Ajouter les absents (uniquement pour les séances du prof)
    return _ajouter_absents(db, presences_reelles, mes_seances)


def get_presences_par_etudiant(db: Session, etudiant_id: int):
    # Pour l'étudiant, on ne renvoie que ses vrais scans (le frontend calcule déjà ses absences)
    return db.query(Presence).filter(Presence.etudiant_id == etudiant_id).all()


def get_presence_par_id(db: Session, presence_id: int):
    presence = db.query(Presence).filter(Presence.id == presence_id).first()
    if not presence:
        raise HTTPException(status_code=404, detail="Pointage introuvable.")
    return presence


def modifier_presence(db: Session, presence_id: int, presence_update: PresenceCreate):
    db_presence = get_presence_par_id(db, presence_id)
    for cle, valeur in presence_update.model_dump().items():
        setattr(db_presence, cle, valeur)
    db.commit()
    db.refresh(db_presence)
    return db_presence


def supprimer_presence(db: Session, presence_id: int):
    db_presence = get_presence_par_id(db, presence_id)
    db.delete(db_presence)
    db.commit()
    return {"message": "Pointage supprimé avec succès."}
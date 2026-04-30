from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.presence import Presence
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

def get_presences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Presence).offset(skip).limit(limit).all()

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

def get_presences_par_etudiant(db: Session, etudiant_id: int):
    return db.query(Presence).filter(Presence.etudiant_id == etudiant_id).all()
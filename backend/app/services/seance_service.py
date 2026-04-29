from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.seance import Seance
from app.schemas.seance import SeanceCreate


def creer_seance(db: Session, seance: SeanceCreate):
    # Petite sécurité : on vérifie que la date de fin est après la date de début !
    if seance.date_heure_fin <= seance.date_heure_debut:
        raise HTTPException(status_code=400, detail="La date de fin doit être après la date de début.")

    nouvelle_seance = Seance(**seance.model_dump())
    db.add(nouvelle_seance)
    db.commit()
    db.refresh(nouvelle_seance)
    return nouvelle_seance


def get_seances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Seance).offset(skip).limit(limit).all()


def get_seance_par_id(db: Session, seance_id: int):
    seance = db.query(Seance).filter(Seance.id == seance_id).first()
    if not seance:
        raise HTTPException(status_code=404, detail="Séance introuvable.")
    return seance


def modifier_seance(db: Session, seance_id: int, seance_update: SeanceCreate):
    db_seance = get_seance_par_id(db, seance_id)
    for cle, valeur in seance_update.model_dump().items():
        setattr(db_seance, cle, valeur)
    db.commit()
    db.refresh(db_seance)
    return db_seance


def supprimer_seance(db: Session, seance_id: int):
    db_seance = get_seance_par_id(db, seance_id)
    db.delete(db_seance)
    db.commit()
    return {"message": "La séance a été supprimée."}
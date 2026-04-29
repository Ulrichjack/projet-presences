from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cours import Cours
from app.schemas.cours import CoursCreate


def creer_cours(db: Session, cours: CoursCreate):
    cours_existant = db.query(Cours).filter(Cours.nom == cours.nom).first()
    if cours_existant:
        raise HTTPException(status_code=400, detail="Ce cours existe déjà.")

    nouveau_cours = Cours(**cours.model_dump())
    db.add(nouveau_cours)
    db.commit()
    db.refresh(nouveau_cours)
    return nouveau_cours


def get_cours(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Cours).offset(skip).limit(limit).all()


def get_cours_par_id(db: Session, cours_id: int):
    cours = db.query(Cours).filter(Cours.id == cours_id).first()
    if not cours:
        raise HTTPException(status_code=404, detail="Cours introuvable.")
    return cours


def modifier_cours(db: Session, cours_id: int, cours_update: CoursCreate):
    db_cours = get_cours_par_id(db, cours_id)
    for cle, valeur in cours_update.model_dump().items():
        setattr(db_cours, cle, valeur)
    db.commit()
    db.refresh(db_cours)
    return db_cours


def supprimer_cours(db: Session, cours_id: int):
    db_cours = get_cours_par_id(db, cours_id)
    db.delete(db_cours)
    db.commit()
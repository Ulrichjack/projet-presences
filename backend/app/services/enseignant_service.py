from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.enseignant import Enseignant
from app.schemas.enseignant import EnseignantCreate

#CREATE
def creer_enseignant(db: Session, enseignant: EnseignantCreate):
    enseignant_existant = db.query(Enseignant).filter(
        (Enseignant.matricule == enseignant.matricule) | (Enseignant.email == enseignant.email)
    ).first()

    if enseignant_existant:
        raise HTTPException(status_code=400, detail="Ce matricule ou cet email existe deja")

    nouvel_enseignant = Enseignant(**enseignant.model_dump())

    db.add(nouvel_enseignant)
    db.commit()
    db.refresh(nouvel_enseignant)
    return nouvel_enseignant

#READ
def get_enseignant(db: Session, skip: int = 0, limit: int =100):
    return db.query(Enseignant).offset(skip).limit(limit).all()

#READ par ID
def get_enseignant_par_id(db: Session, enseignant_id: int):
    enseignant = db.query(Enseignant).filter(Enseignant.id == enseignant_id).first()

    if not enseignant:
        raise HTTPException(status_code=404, detail="Enseignant introuvable.")
    return enseignant

#UPDATE
def modifier_enseignant(db:Session, enseignant_id: int, enseignant_update: EnseignantCreate):
    db_enseignant = get_enseignant_par_id(db, enseignant_id)

    donnees_a_modifier = enseignant_update.model_dump()
    for cle, valeur in donnees_a_modifier.items():
        setattr(db_enseignant, cle, valeur)
    db.commit()
    db.refresh(db_enseignant)
    return db_enseignant

#DELETE
def supprimer_enseignant(db:Session, enseignant_id:int):
    db_enseignant = get_enseignant_par_id(db, enseignant_id)
    db.delete(db_enseignant)
    db.commit()
    return {"message": f"L'enseignant avec l'ID {enseignant_id} a été supprimé."}

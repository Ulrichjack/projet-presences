
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.etudiant import Etudiant
from app.schemas.etudiant import EtudiantCreate
from app.utils.security import hacher_mot_de_passe
#CREATE
def creer_etudiant (db: Session, etudiant: EtudiantCreate):
        etudiant_existant = db.query(Etudiant).filter(
            (Etudiant.matricule == etudiant.matricule) | (Etudiant.email == etudiant.email)
        ).first()

        if etudiant_existant:
            raise HTTPException(status_code=400, detail="Ce matricule ou cet email existe deja")

        etudiant.mot_de_passe = hacher_mot_de_passe(etudiant.mot_de_passe)

        nouvel_etudiant = Etudiant(**etudiant.model_dump())

        db.add(nouvel_etudiant)
        db.commit()
        db.refresh(nouvel_etudiant)
        return nouvel_etudiant

#READ
def get_etudiant(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Etudiant).offset(skip).limit(limit).all()

#READ par ID
def get_etudiant_par_id(db: Session, etudiant_id: int):
        etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()

        if not etudiant:
            raise HTTPException(status_code=404, detail="Étudiant introuvable.")
        return etudiant

#UPDATE
def modifier_etudiant(db:Session, etudiant_id: int, etudiant_update: EtudiantCreate):
    db_etudiant = get_etudiant_par_id(db, etudiant_id)

    donnees_a_modifier = etudiant_update.model_dump()
    for cle, valeur in donnees_a_modifier.items():
        setattr(db_etudiant, cle, valeur)
    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

#DELETE
def supprimer_etudiant(db:Session, etudiant_id:int):
    db_etudiant = get_etudiant_par_id(db, etudiant_id)
    db.delete(db_etudiant)
    db.commit()
    return {"message": f"L'étudiant avec l'ID {etudiant_id} a été supprimé."}

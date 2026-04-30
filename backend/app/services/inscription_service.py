from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.inscription import Inscription
from app.schemas.inscription import InscriptionCreate


def inscrire_etudiant(db: Session, inscription: InscriptionCreate):
    # Vérifier si l'étudiant n'est pas déjà inscrit à ce cours !
    existante = db.query(Inscription).filter(
        Inscription.etudiant_id == inscription.etudiant_id,
        Inscription.cours_id == inscription.cours_id
    ).first()

    if existante:
        raise HTTPException(status_code=400, detail="L'étudiant est déjà inscrit à ce cours.")

    nouvelle_inscription = Inscription(**inscription.model_dump())
    db.add(nouvelle_inscription)
    db.commit()
    db.refresh(nouvelle_inscription)
    return nouvelle_inscription


def lister_inscriptions(db: Session):
    return db.query(Inscription).all()
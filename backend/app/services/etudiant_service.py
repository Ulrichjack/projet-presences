
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.etudiant import Etudiant
from app.schemas.etudiant import EtudiantCreate, EtudiantUpdate
from app.utils.security import hacher_mot_de_passe
from app.models.inscription import Inscription
from app.models.presence import Presence
#CREATE
def creer_etudiant(db: Session, etudiant: EtudiantCreate):
    # Correction de la syntaxe du filter
    etudiant_existant = db.query(Etudiant).filter(
        (Etudiant.matricule == etudiant.matricule) | (Etudiant.email == etudiant.email)
    ).first()

    if etudiant_existant:
        raise HTTPException(status_code=400, detail="Ce matricule ou cet email existe déjà")

    # On hache le mot de passe avant d'insérer en base
    mot_hache = hacher_mot_de_passe(etudiant.mot_de_passe)

    # On crée l'objet SQLAlchemy en remplaçant le mot de passe clair par le haché
    db_etudiant = Etudiant(
        nom=etudiant.nom,
        prenom=etudiant.prenom,
        matricule=etudiant.matricule,
        email=etudiant.email,
        photo_reference=etudiant.photo_reference, # Chemin enregistré par la route
        qr_code=etudiant.qr_code,
        mot_de_passe=mot_hache,
        role="ETUDIANT"
    )

    db.add(db_etudiant)
    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

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
# UPDATE
def modifier_etudiant(db: Session, etudiant_id: int, etudiant_update: EtudiantUpdate):  # 👈 Utilise EtudiantUpdate
    db_etudiant = get_etudiant_par_id(db, etudiant_id)

    # exclude_unset=True permet d'ignorer les champs qu'on n'a pas envoyés
    donnees_a_modifier = etudiant_update.model_dump(exclude_unset=True)

    for cle, valeur in donnees_a_modifier.items():
        # Si on modifie le mot de passe, on doit le hacher !
        if cle == "mot_de_passe" and valeur:
            valeur = hacher_mot_de_passe(valeur)
        setattr(db_etudiant, cle, valeur)

    db.commit()
    db.refresh(db_etudiant)
    return db_etudiant

#DELETE
def supprimer_etudiant(db: Session, etudiant_id: int):
    db_etudiant = get_etudiant_par_id(db, etudiant_id)

    # 1. On supprime toutes ses présences
    db.query(Presence).filter(Presence.etudiant_id == etudiant_id).delete()

    # 2. On supprime toutes ses inscriptions aux cours
    db.query(Inscription).filter(Inscription.etudiant_id == etudiant_id).delete()

    # 3. Maintenant que le terrain est propre, on peut supprimer l'étudiant !
    db.delete(db_etudiant)
    db.commit()

    return {"message": f"L'étudiant avec l'ID {etudiant_id} a été supprimé proprement."}
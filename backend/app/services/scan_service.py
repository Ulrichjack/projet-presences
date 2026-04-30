import os
import shutil
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.etudiant import Etudiant
from app.models.seance import Seance
from app.models.presence import Presence
from app.models.inscription import Inscription
from app.services import ia_service

def verifier_et_enregistrer_presence(db: Session, etudiant: Etudiant, seance: Seance, methode: str):
    # Vérifier l'inscription
    inscription = db.query(Inscription).filter(
        Inscription.etudiant_id == etudiant.id, Inscription.cours_id == seance.cours_id
    ).first()
    if not inscription:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Accès refusé : non inscrit.")

    # Vérifier les doublons
    presence_existante = db.query(Presence).filter(
        Presence.etudiant_id == etudiant.id, Presence.seance_id == seance.id
    ).first()
    if presence_existante:
        raise HTTPException(status_code=400, detail="Déjà pointé !")

    # Enregistrer
    nouvelle_presence = Presence(
        etudiant_id=etudiant.id, seance_id=seance.id,
        statut="Présent", methode_pointage=methode
    )
    db.add(nouvelle_presence)
    db.commit()
    db.refresh(nouvelle_presence)
    return nouvelle_presence

def scan_prof(db: Session, qr_code_texte: str):
    etudiant = db.query(Etudiant).filter(Etudiant.qr_code == qr_code_texte).first()
    if not etudiant: raise HTTPException(status_code=404, detail="Étudiant non reconnu.")

    maintenant = datetime.utcnow()
    seance = db.query(Seance).filter(Seance.date_heure_debut <= maintenant, Seance.date_heure_fin >= maintenant).first()
    if not seance: raise HTTPException(status_code=404, detail="Aucun cours en ce moment.")

    return verifier_et_enregistrer_presence(db, etudiant, seance, "Scan par le Prof")

def scan_etudiant(db: Session, etudiant_id: int, code_tableau: str):
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    if not etudiant: raise HTTPException(status_code=404, detail="Étudiant introuvable.")

    seance = db.query(Seance).filter(Seance.code_validation == code_tableau).first()
    if not seance: raise HTTPException(status_code=404, detail="QR Code invalide.")

    maintenant = datetime.utcnow()
    if maintenant < seance.date_heure_debut or maintenant > seance.date_heure_fin:
        raise HTTPException(status_code=400, detail="Cours inactif.")

    return verifier_et_enregistrer_presence(db, etudiant, seance, "Scan par l'Étudiant")

def scan_visage(db: Session, etudiant_id: int, seance_id: int, photo_webcam: UploadFile):
    etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
    seance = db.query(Seance).filter(Seance.id == seance_id).first()
    if not etudiant or not seance: raise HTTPException(status_code=404, detail="Étudiant ou séance introuvable.")

    chemin_temp = f"temp_webcam_{etudiant_id}.jpg"
    with open(chemin_temp, "wb") as buffer:
        shutil.copyfileobj(photo_webcam.file, buffer)

    chemin_reference = etudiant.photo_reference
    if not chemin_reference or not os.path.exists(chemin_reference):
        os.remove(chemin_temp)
        raise HTTPException(status_code=400, detail="Pas de photo de référence.")

    correspondance = ia_service.comparer_visages(chemin_reference, chemin_temp)
    os.remove(chemin_temp)

    if not correspondance:
        raise HTTPException(status_code=403, detail="Alerte Imposteur ! Visage non reconnu.")

    return verifier_et_enregistrer_presence(db, etudiant, seance, "Reconnaissance Faciale")
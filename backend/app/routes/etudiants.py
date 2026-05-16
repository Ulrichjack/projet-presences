from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form # Ajoute UploadFile, File, Form
import os
import shutil
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.etudiant import EtudiantCreate, EtudiantResponse, EtudiantUpdate
from app.services import etudiant_service
from app.dependencies import verifier_admin, obtenir_utilisateur_actuel, verifier_prof_ou_admin

router = APIRouter(prefix="/etudiants", tags=["Étudiants"])

# 🔒 ADMIN SEULEMENT : Modification pour accepter la PHOTO
@router.post("/", response_model=EtudiantResponse, status_code=201)
async def creer_etudiant(
    nom: str = Form(...),
    prenom: str = Form(...),
    matricule: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...),
    qr_code: Optional[str] = Form(None),
    photo: UploadFile = File(...), # <-- Le fichier image
    db: Session = Depends(get_db),
    admin = Depends(verifier_admin)
):
    # 1. On s'assure que le dossier de stockage existe
    dossier = "photos_reference"
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    # 2. On définit le chemin du fichier (on utilise le matricule pour le nom du fichier)
    extension = photo.filename.split(".")[-1]
    nom_fichier = f"{matricule}.{extension}"
    chemin_photo = os.path.join(dossier, nom_fichier)

    # 3. On enregistre le fichier sur le disque dur
    with open(chemin_photo, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # 4. On crée l'objet EtudiantCreate pour le passer au service
    # (Note: photo_reference contiendra le chemin vers le fichier)
    nouvel_etudiant_data = EtudiantCreate(
        nom=nom,
        prenom=prenom,
        matricule=matricule,
        email=email,
        mot_de_passe=mot_de_passe,
        qr_code=qr_code or f"QR-{matricule}",
        photo_reference=chemin_photo
    )

    return etudiant_service.creer_etudiant(db=db, etudiant=nouvel_etudiant_data)
# 🔓 TOUT UTILISATEUR CONNECTÉ
@router.get("/", response_model=list[EtudiantResponse])
def lire_etudiants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), prof = Depends(verifier_prof_ou_admin)):
    return etudiant_service.get_etudiant(db=db, skip=skip, limit=limit)

# 🔓 TOUT LE MONDE, MAIS L'ÉTUDIANT NE VOIT QUE LUI-MÊME
@router.get("/{etudiant_id}", response_model=EtudiantResponse)
def lire_etudiant_par_id(etudiant_id: int, db: Session = Depends(get_db), user=Depends(obtenir_utilisateur_actuel)):
    # Si c'est un étudiant et qu'il essaie de regarder le profil d'un autre (ID différent) -> DEHORS !
    if user.role == "ETUDIANT" and user.id != etudiant_id:
        raise HTTPException(status_code=403, detail="Petit curieux ! Tu ne peux voir que ton propre profil.")

    return etudiant_service.get_etudiant_par_id(db=db, etudiant_id=etudiant_id)
# 🔒 ADMIN SEULEMENT
@router.put("/{etudiant_id}", response_model=EtudiantResponse)
def modifier_etudiant(etudiant_id: int, etudiant: EtudiantUpdate, db: Session = Depends(get_db), admin = Depends(verifier_admin)): # 👈 Utilise EtudiantUpdate
    return etudiant_service.modifier_etudiant(db=db, etudiant_id=etudiant_id, etudiant_update=etudiant)
# 🔒 ADMIN SEULEMENT
@router.delete("/{etudiant_id}")
def supprimer_etudiant(etudiant_id: int, db: Session = Depends(get_db), admin = Depends(verifier_admin)):
    return etudiant_service.supprimer_etudiant(db=db, etudiant_id=etudiant_id)
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.schemas.presence import PresenceResponse
from app.services import scan_service

# --- IMPORTS DE SÉCURITÉ ---
from app.dependencies import verifier_prof_ou_admin, obtenir_utilisateur_actuel

router = APIRouter(prefix="/scan", tags=["Scanner (Logique Métier)"])

class ScanProfRequest(BaseModel):
    qr_code_texte: str

class ScanEtudiantRequest(BaseModel):
    etudiant_id: int
    code_scanne_au_tableau: str

# 🔒 PROF OU ADMIN SEULEMENT (C'est le prof qui tient la tablette)
@router.post("/prof", response_model=PresenceResponse, status_code=status.HTTP_201_CREATED)
def le_prof_scanne_letudiant(requete: ScanProfRequest, db: Session = Depends(get_db), prof = Depends(verifier_prof_ou_admin)):
    return scan_service.scan_prof(db=db, qr_code_texte=requete.qr_code_texte)

# 🔓 TOUT UTILISATEUR CONNECTÉ (L'étudiant utilise son propre téléphone)
@router.post("/etudiant", response_model=PresenceResponse, status_code=status.HTTP_201_CREATED)
def letudiant_scanne_le_tableau(requete: ScanEtudiantRequest, db: Session = Depends(get_db), user = Depends(obtenir_utilisateur_actuel)):
    return scan_service.scan_etudiant(db=db, etudiant_id=requete.etudiant_id, code_tableau=requete.code_scanne_au_tableau)

# 🔒 PROF OU ADMIN SEULEMENT (C'est le prof qui tient la webcam)
@router.post("/visage", response_model=PresenceResponse, status_code=status.HTTP_201_CREATED)
def scan_par_reconnaissance_faciale(
    etudiant_id: int = Form(...),
    seance_id: int = Form(...),
    photo_webcam: UploadFile = File(...),
    db: Session = Depends(get_db),
    prof = Depends(verifier_prof_ou_admin)
):
    return scan_service.scan_visage(db=db, etudiant_id=etudiant_id, seance_id=seance_id, photo_webcam=photo_webcam)
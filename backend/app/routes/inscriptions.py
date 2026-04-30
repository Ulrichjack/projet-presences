from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.inscription import InscriptionCreate, InscriptionResponse
from app.services import inscription_service
from app.dependencies import verifier_admin
router = APIRouter(
    prefix="/inscriptions",
    tags=["Inscriptions aux Cours"],
    dependencies=[Depends(verifier_admin)]
)

@router.post("/", response_model=InscriptionResponse, status_code=status.HTTP_201_CREATED)
def inscrire_etudiant(inscription: InscriptionCreate, db: Session = Depends(get_db)):
    return inscription_service.inscrire_etudiant(db=db, inscription=inscription)

@router.get("/", response_model=list[InscriptionResponse])
def lire_les_inscriptions(db: Session = Depends(get_db)):
    return inscription_service.lister_inscriptions(db=db)
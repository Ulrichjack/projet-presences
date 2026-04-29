from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.presence import PresenceCreate, PresenceResponse
from app.services import presence_service

router = APIRouter(prefix="/presences", tags=["Présences"])

@router.post("/", response_model=PresenceResponse, status_code=201)
def marquer_presence(presence: PresenceCreate, db: Session = Depends(get_db)):
    return presence_service.marquer_presence(db=db, presence=presence)

@router.get("/", response_model=list[PresenceResponse])
def lire_presences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return presence_service.get_presences(db=db, skip=skip, limit=limit)

@router.get("/{presence_id}", response_model=PresenceResponse)
def lire_presence_par_id(presence_id: int, db: Session = Depends(get_db)):
    return presence_service.get_presence_par_id(db=db, presence_id=presence_id)

@router.put("/{presence_id}", response_model=PresenceResponse)
def modifier_presence(presence_id: int, presence: PresenceCreate, db: Session = Depends(get_db)):
    return presence_service.modifier_presence(db=db, presence_id=presence_id, presence_update=presence)

@router.delete("/{presence_id}")
def supprimer_presence(presence_id: int, db: Session = Depends(get_db)):
    return presence_service.supprimer_presence(db=db, presence_id=presence_id)
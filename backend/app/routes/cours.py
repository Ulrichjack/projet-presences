from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cours import CoursCreate, CoursResponse
from app.services import cours_service

router = APIRouter(prefix="/cours", tags=["Cours"])

@router.post("/", response_model=CoursResponse, status_code=status.HTTP_201_CREATED)
def creer_cours(cours: CoursCreate, db: Session = Depends(get_db)):
    return cours_service.creer_cours(db=db, cours=cours)

@router.get("/", response_model=list[CoursResponse])
def lire_les_cours(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cours_service.get_cours(db=db, skip=skip, limit=limit)

@router.get("/{cours_id}", response_model=CoursResponse)
def lire_cours_par_id(cours_id: int, db: Session = Depends(get_db)):
    return cours_service.get_cours_par_id(db=db, cours_id=cours_id)

@router.put("/{cours_id}", response_model=CoursResponse)
def modifier_cours(cours_id: int, cours: CoursCreate, db: Session = Depends(get_db)):
    return cours_service.modifier_cours(db=db, cours_id=cours_id, cours_update=cours)

@router.delete("/{cours_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_cours(cours_id: int, db: Session = Depends(get_db)):
    cours_service.supprimer_cours(db=db, cours_id=cours_id)
    return
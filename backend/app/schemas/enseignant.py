from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class EnseignantCreate(BaseModel):
    nom: str
    prenom: str
    matricule: str
    email: EmailStr
    specialite: Optional[str] = None


class EnseignantResponse(EnseignantCreate):
    id: int
    date_creation: datetime

    class Config:
        from_attributes = True
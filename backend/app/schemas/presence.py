from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PresenceCreate(BaseModel):
    etudiant_id: int
    seance_id: int
    statut: Optional[str] = "Présent"
    methode_pointage: str

class PresenceResponse(PresenceCreate):
    id: int
    heure_pointage: datetime

    class Config:
        from_attributes = True
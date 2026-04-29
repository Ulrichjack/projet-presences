from pydantic import BaseModel
from datetime import datetime

class SeanceCreate(BaseModel):
    date_heure_debut: datetime
    date_heure_fin: datetime
    cours_id: int
    enseignant_id: int

class SeanceResponse(SeanceCreate):
    id: int

    class Config:
        from_attributes = True
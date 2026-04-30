from pydantic import BaseModel
from datetime import datetime

class SeanceCreate(BaseModel):
    date_heure_debut: datetime
    date_heure_fin: datetime
    cours_id: int
    enseignant_id: int
    salle: str

class SeanceResponse(SeanceCreate):
    id: int
    code_validation: str

    class Config:
        from_attributes = True
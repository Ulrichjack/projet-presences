from pydantic import BaseModel
from datetime import datetime

class InscriptionCreate(BaseModel):
    etudiant_id: int
    cours_id: int

class InscriptionResponse(InscriptionCreate):
    id: int
    date_inscription: datetime

    class Config:
        from_attributes = True
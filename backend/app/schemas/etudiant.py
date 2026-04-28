# app/schemas/etudiant_service.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 1. Le schéma pour CRÉER un étudiant (ce que le frontend envoie)
class EtudiantCreate(BaseModel):
    nom: str
    prenom: str
    matricule: str
    email: EmailStr  # Pydantic vérifiera tout seul que c'est un vrai format d'email !
    photo_reference: Optional[str] = None
    qr_code: str

# 2. Le schéma pour LIRE un étudiant (ce que le backend renvoie au frontend)
# On ajoute l'ID et la date, car la base de données les a générés toute seule
class EtudiantResponse(EtudiantCreate):
    id: int
    date_inscription: datetime

    # Indique à Pydantic qu'il lit des données venant de SQLAlchemy
    class Config:
        from_attributes = True
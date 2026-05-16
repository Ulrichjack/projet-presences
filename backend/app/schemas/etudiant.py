from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 1. Schéma de base (SANS LE MOT DE PASSE)
class EtudiantBase(BaseModel):
    nom: str
    prenom: str
    matricule: str
    email: str
    photo_reference: Optional[str] = None
    qr_code: str

# 2. Schéma pour CRÉER (On ajoute le mot de passe obligatoire)
class EtudiantCreate(EtudiantBase):
    mot_de_passe: str

# 3. Schéma pour MODIFIER (Tout est optionnel)
class EtudiantUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    matricule: Optional[str] = None
    email: Optional[str] = None
    mot_de_passe: Optional[str] = None
    qr_code: Optional[str] = None

# 4. Schéma pour RÉPONDRE (Hérite de la base = PAS DE MOT DE PASSE)
class EtudiantResponse(EtudiantBase):
    id: int
    date_inscription: datetime

    class Config:
        from_attributes = True
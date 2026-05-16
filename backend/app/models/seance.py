from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from app.database import Base
import uuid

def generer_code():
    # Génère un code du genre "A1B2C3D4" (8 caractères)
    return str(uuid.uuid4())[:8].upper()

class Seance(Base):
    __tablename__ = "seances"

    id = Column(Integer, primary_key=True, index=True)
    date_heure_debut = Column(DateTime, nullable=False)
    date_heure_fin = Column(DateTime, nullable=False)
    salle = Column(String(50), nullable=False)

    cours_id = Column(Integer, ForeignKey("cours.id", ondelete="CASCADE"), nullable=False)
    enseignant_id = Column(Integer, ForeignKey("enseignants.id", ondelete="CASCADE"), nullable=False)
    code_validation = Column(String(50), unique=True, index=True, default=generer_code)
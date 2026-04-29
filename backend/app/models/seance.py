from sqlalchemy import Column, Integer, DateTime, ForeignKey
from app.database import Base


class Seance(Base):
    __tablename__ = "seances"

    id = Column(Integer, primary_key=True, index=True)
    date_heure_debut = Column(DateTime, nullable=False)
    date_heure_fin = Column(DateTime, nullable=False)

    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    enseignant_id = Column(Integer, ForeignKey("enseignants.id"), nullable=False)
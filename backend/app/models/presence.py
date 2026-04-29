from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Presence(Base):
    __tablename__ = "presences"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    seance_id = Column(Integer, ForeignKey("seances.id"), nullable=False)

    # L'heure exacte à laquelle la caméra ou le scanner a vu l'étudiant
    heure_pointage = Column(DateTime, default=datetime.utcnow)

    # Ex: "Présent", "Retard", "Absent"
    statut = Column(String(20), default="Présent")

    # Ex: "QR Code", "Reconnaissance Faciale", "Manuel"
    methode_pointage = Column(String(50), nullable=False)
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Inscription(Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=False)
    date_inscription = Column(DateTime, default=datetime.utcnow)
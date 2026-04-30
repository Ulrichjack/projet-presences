from sqlalchemy import Column, Integer, String, DateTime
from  datetime import datetime
from app.database import Base

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    matricule = Column(String(20), unique=True, index= True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    photo_reference = Column(String(255), nullable=True)
    qr_code = Column(String(255), unique=True, index=True, nullable=False )
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(String(50), default="ETUDIANT")
    date_inscription = Column(DateTime, default=datetime.utcnow)
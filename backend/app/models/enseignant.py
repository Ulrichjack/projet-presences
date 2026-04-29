from sqlalchemy import Column, Integer, String, DateTime
from  datetime import datetime
from app.database import Base

class Enseignant(Base):
    __tablename__ = "enseignants"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    matricule = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index= True, nullable=False)
    specialite = Column(String(100), nullable=True)
    date_creation = Column(DateTime, default=datetime.utcnow)
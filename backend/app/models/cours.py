from sqlalchemy import Column, Integer, String
from app.database import Base

class Cours(Base):
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    code = Column(String(20), unique=True, nullable=False)
    filiere = Column(String(100), nullable=False)
    niveau = Column(String(20), nullable=False)  # Ex: "L1", "L2", "M1"...
    credits = Column(Integer, nullable=False)
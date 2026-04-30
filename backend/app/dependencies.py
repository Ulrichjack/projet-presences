from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models.enseignant import Enseignant
from app.models.etudiant import Etudiant

# FastAPI saura que le token vient de la route "/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def obtenir_utilisateur_actuel(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")  # <-- On récupère le rôle du Token
        if email is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # --- LA CORRECTION EST ICI ---
    # Si le token dit que c'est un étudiant, on cherche dans la table des étudiants
    if role == "ETUDIANT":
        utilisateur = db.query(Etudiant).filter(Etudiant.email == email).first()
    # Sinon (si c'est PROF ou ADMIN), on cherche dans la table des enseignants
    else:
        utilisateur = db.query(Enseignant).filter(Enseignant.email == email).first()
    # ----------------------------

    if utilisateur is None:
        raise credentials_exception

    return utilisateur

def verifier_admin(utilisateur_actuel: Enseignant = Depends(obtenir_utilisateur_actuel)):
    """Vérifie si l'utilisateur connecté a bien le rôle ADMIN"""
    if utilisateur_actuel.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Vous devez être Administrateur."
        )
    return utilisateur_actuel

def verifier_prof_ou_admin(utilisateur_actuel = Depends(obtenir_utilisateur_actuel)):
    """Vérifie si l'utilisateur est au moins un Professeur"""
    if utilisateur_actuel.role not in ["ADMIN", "PROF"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès refusé : Réservé aux professeurs et administrateurs."
        )
    return utilisateur_actuel
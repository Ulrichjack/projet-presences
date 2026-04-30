from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

# On dit à Passlib d'utiliser l'algorithme bcrypt (le standard de l'industrie)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hacher_mot_de_passe(mot_de_passe: str) -> str:
    """Transforme 'azerty' en '$2b$12$Kix...'"""
    return pwd_context.hash(mot_de_passe)

def verifier_mot_de_passe(mot_de_passe_clair: str, mot_de_passe_hache: str) -> bool:
    """Vérifie si le mot de passe tapé correspond au hash de la base de données"""
    return pwd_context.verify(mot_de_passe_clair, mot_de_passe_hache)


def creer_token_acces(data: dict):
    """Fabrique le badge JWT avec les infos de l'utilisateur"""
    a_encoder = data.copy()

    # On calcule l'heure d'expiration
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    a_encoder.update({"exp": expiration})

    # On crypte le tout avec notre clé secrète
    token_jwt = jwt.encode(a_encoder, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt
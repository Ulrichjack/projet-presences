from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enseignant import Enseignant
from app.models.etudiant import Etudiant
from app.utils.security import verifier_mot_de_passe, creer_token_acces

router = APIRouter(tags=["Authentification"])


# On utilise OAuth2PasswordRequestForm : c'est le standard FastAPI qui va
# créer le bouton "Authorize" (Cadenas) tout en haut de Swagger !
@router.post("/login")
def connexion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. On cherche d'abord si c'est un Professeur (form_data.username contiendra l'email)
    utilisateur = db.query(Enseignant).filter(Enseignant.email == form_data.username).first()

    # 2. Si ce n'est pas un prof, on cherche dans les Étudiants
    if not utilisateur:
        utilisateur = db.query(Etudiant).filter(Etudiant.email == form_data.username).first()

    # 3. Si on ne trouve personne, ou si le mot de passe est faux -> Erreur 401
    if not utilisateur or not verifier_mot_de_passe(form_data.password, utilisateur.mot_de_passe):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 4. Si tout est bon, on fabrique le badge (Token JWT)
    donnees_token = {
        "sub": utilisateur.email,  # sub = subject (le standard pour l'identifiant)
        "id": utilisateur.id,
        "role": utilisateur.role
    }

    token = creer_token_acces(data=donnees_token)

    # On renvoie le token au format standard attendu par le frontend
    return {"access_token": token, "token_type": "bearer"}
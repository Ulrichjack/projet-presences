from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from datetime import datetime

from app.database import get_db
from app.dependencies import verifier_prof_ou_admin
from app.models.cours import Cours
from app.models.enseignant import Enseignant
from app.models.etudiant import Etudiant
from app.models.seance import Seance
from app.models.presence import Presence
from app.dependencies import obtenir_utilisateur_actuel # Ajoute cet import
from app.models.inscription import Inscription # 👈 Ajoute cet import en haut du fichier avec les autres
from app.services import presence_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats", dependencies=[Depends(verifier_prof_ou_admin)])
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_etudiants = db.query(func.count(Etudiant.id)).scalar()
    total_profs = db.query(func.count(Enseignant.id)).filter(Enseignant.role == "PROF").scalar()

    today = date.today()
    seances_du_jour = db.query(func.count(Seance.id)).filter(
        func.date(Seance.date_heure_debut) == today
    ).scalar()

    # --- CORRECTION DU CALCUL DES PRÉSENCES ---
    # On utilise le service qui inclut les "fantômes" (les absents) !
    toutes_les_presences = presence_service.get_presences(db=db)

    total_enregistrements = len(toutes_les_presences)
    presences_effectives = sum(1 for p in toutes_les_presences if p.statut == "Présent")

    taux_presence = 0
    if total_enregistrements > 0:
        taux_presence = round((presences_effectives / total_enregistrements) * 100)

    alertes_absences = total_enregistrements - presences_effectives
    # ------------------------------------------

    derniers_cours = db.query(Cours).order_by(Cours.id.desc()).limit(5).all()

    return {
        "totalEtudiants": total_etudiants,
        "totalProfesseurs": total_profs,
        "seancesDuJour": seances_du_jour,
        "tauxDePresence": taux_presence,
        "alertesAbsences": alertes_absences,
        "derniersCours": derniers_cours
    }
@router.get("/stats/etudiant", dependencies=[Depends(obtenir_utilisateur_actuel)])
def get_etudiant_stats(db: Session = Depends(get_db), user=Depends(obtenir_utilisateur_actuel)):
    if user.role != "ETUDIANT":
        raise HTTPException(status_code=403, detail="Réservé aux étudiants")

    # 1. On récupère les cours auxquels l'étudiant est inscrit
    inscriptions = db.query(Inscription).filter(Inscription.etudiant_id == user.id).all()
    cours_ids = [i.cours_id for i in inscriptions]

    if not cours_ids:
        return {"tauxDePresence": 0, "heuresAbsence": 0, "prochainCours": "Aucun cours"}

    # 2. On compte combien de séances ont DÉJÀ EU LIEU pour ces cours
    maintenant = datetime.utcnow()
    seances_passees = db.query(Seance).filter(
        Seance.cours_id.in_(cours_ids),
        Seance.date_heure_debut < maintenant
    ).all()
    total_seances_passees = len(seances_passees)

    # 3. On compte combien de fois l'étudiant a réellement pointé
    presences = db.query(Presence).filter(Presence.etudiant_id == user.id).all()
    nb_presences = len(presences)

    # 4. Calcul du Taux et des Absences (On compte 2h par absence)
    taux_presence = 0
    if total_seances_passees > 0:
        taux_presence = round((nb_presences / total_seances_passees) * 100)
    elif nb_presences > 0:
        taux_presence = 100  # S'il a pointé à une séance qui n'est pas encore finie

    absences = total_seances_passees - nb_presences
    heures_absence = absences * 2 if absences > 0 else 0

    # 5. Quel est son PROCHAIN cours ?
    prochain = db.query(Seance).filter(
        Seance.cours_id.in_(cours_ids),
        Seance.date_heure_debut > maintenant
    ).order_by(Seance.date_heure_debut.asc()).first()

    nom_prochain = "Rien de prévu"
    if prochain:
        cours = db.query(Cours).filter(Cours.id == prochain.cours_id).first()
        # Formate la date joliment ex: "ALGO (28/04 à 10:00)"
        date_formatee = prochain.date_heure_debut.strftime('%d/%m à %H:%M')
        nom_prochain = f"{cours.nom} ({date_formatee})"

    return {
        "tauxDePresence": taux_presence,
        "heuresAbsence": heures_absence,
        "prochainCours": nom_prochain
    }
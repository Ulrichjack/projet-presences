from app.database import engine, Base, SessionLocal
from app.models import etudiant, enseignant, cours, seance, presence, inscription
from app.models.enseignant import Enseignant
from app.utils.security import hacher_mot_de_passe

print("🧹 Suppression des anciennes tables...")
Base.metadata.drop_all(bind=engine)

print("✨ Création des nouvelles tables toutes neuves...")
Base.metadata.create_all(bind=engine)

print(" Création du Super Administrateur...")
db = SessionLocal()
try:
    admin = Enseignant(
        nom="Directeur",
        prenom="Admin",
        matricule="ADMIN-001",
        email="admin@ecole.com",
        mot_de_passe=hacher_mot_de_passe("admin123"), # Mot de passe par défaut
        specialite="Direction",
        role="ADMIN"
    )
    db.add(admin)
    db.commit()
    print("✅ Administrateur créé avec succès ! (Email: admin@ecole.com | Mdp: admin123)")
except Exception as e:
    print(f"❌ Erreur lors de la création de l'admin : {e}")
finally:
    db.close()

print("✅ Terminé !")
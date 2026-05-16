from sqlalchemy import text
from app.database import engine, Base, SessionLocal

# ⚠️ IMPORTANT : Il faut importer TOUS les fichiers de tes modèles ici
# pour que SQLAlchemy sache quelles tables il doit recréer !
from app.models import etudiant, enseignant, cours, seance, presence, inscription
from app.models.enseignant import Enseignant
from app.models.cours import Cours
from app.utils.security import hacher_mot_de_passe

print("🧹 Suppression des anciennes tables (Méthode forte PostgreSQL)...")

# Méthode "Nuke" pour PostgreSQL : On supprime tout en cascade
with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE;"))
    conn.execute(text("CREATE SCHEMA public;"))
    conn.commit()

print("✨ Création des nouvelles tables toutes neuves...")
Base.metadata.create_all(bind=engine)

print("👨‍🏫 Création des données de base...")
db = SessionLocal()
try:
    # 1. Création de l'Administrateur
    admin = Enseignant(
        nom="Directeur",
        prenom="Admin",
        matricule="ADMIN-001",
        email="admin@ecole.com",
        mot_de_passe=hacher_mot_de_passe("admin123"),
        specialite="Direction",
        role="ADMIN"
    )
    db.add(admin)

    # 2. Création de quelques profs depuis ton emploi du temps
    prof1 = Enseignant(
        nom="Le BRAVE",
        prenom="Armel",
        matricule="PROF-001",
        email="enseignant@ecole.com",
        mot_de_passe=hacher_mot_de_passe("123456"),
        specialite="Architectures micro-services",
        role="PROF"
    )
    prof2 = Enseignant(
        nom="HACK",
        prenom="Brice",
        matricule="PROF-002",
        email="enseignant1@ecole.com",
        mot_de_passe=hacher_mot_de_passe("prof123"),
        specialite="Économie d'entreprise",
        role="PROF"
    )
    db.add_all([prof1, prof2])
    db.commit()

    # 3. Création de quelques cours depuis ton emploi du temps
    cours1 = Cours(
        nom="Architectures micro-services",
        code="ARCH-MICRO",
        filiere="3IL3 AC/J",
        niveau="L3",
        credits=4
    )
    cours2 = Cours(
        nom="Économie d'entreprise",
        code="ECO-ENT",
        filiere="3IL3 AC/J",
        niveau="L3",
        credits=3
    )
    db.add_all([cours1, cours2])
    db.commit()

    print("✅ Base de données réinitialisée avec succès !")
    print("👉 Email Admin : admin@ecole.com | Mdp: admin123")
    print("👉 Email Prof  : enseignant@ecole.com | Mdp: 123456")

except Exception as e:
    print(f"❌ Erreur lors de la création des données : {e}")
    db.rollback()
finally:
    db.close()
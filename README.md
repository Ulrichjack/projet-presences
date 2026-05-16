# 🎓 PrésencePro - Système de Suivi des Présences (QR Code & IA)

![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![AI](https://img.shields.io/badge/DeepFace-AI-FF6F00?style=for-the-badge)

**PrésencePro** est une application web complète (SaaS / ERP) conçue pour moderniser et sécuriser la gestion des présences dans les établissements scolaires et universitaires. Elle remplace l'appel traditionnel par des technologies de pointe : **Scan de QR Codes dynamiques** et **Reconnaissance Faciale par Intelligence Artificielle**.

---

## 📸 Aperçu de l'application

*(Ajoutez les captures d'écran ici avant la présentation)*

| Dashboard Administrateur | Scanner Professeur (IA & QR) |
| :---: | :---: |
| <img src="docs/screenshots/admin_dashboard.png" width="400" alt="Dashboard Admin" /> | <img src="docs/screenshots/prof_scanner.png" width="400" alt="Scanner Professeur" /> |
| **Espace Étudiant (Emploi du temps)** | **Rapports & Exports (PDF/Excel)** |
| <img src="docs/screenshots/etudiant_dashboard.png" width="400" alt="Espace Étudiant" /> | <img src="docs/screenshots/admin_rapports.png" width="400" alt="Rapports et Exports" /> |

---

##  Fonctionnalités par Rôle

L'application s'adapte dynamiquement en fonction du rôle de l'utilisateur connecté (sécurisé par JWT).

### 👑 Administrateur (Directeur / Scolarité)
- **Tableau de bord global** : Statistiques en temps réel (taux de présence, alertes absences).
- **Gestion du personnel et des étudiants** : CRUD complet avec upload de photos de référence pour l'IA.
- **Gestion académique** : Création des cours, planification des séances et gestion des inscriptions.
- **Rapports & Exports** : Génération de rapports d'assiduité en un clic (PDF, Excel, CSV).

### 👨‍🏫 Professeur
- **Mes Cours & Séances** : Vue filtrée sur ses propres assignations.
- **Faire l'appel (Scanner)** : 
  - *Méthode 1* : L'étudiant scanne le QR Code projeté au tableau par le professeur.
  - *Méthode 2* : Le professeur utilise la webcam pour valider la présence par **Reconnaissance Faciale**.
- **Historique** : Suivi des présences et absences de ses classes.

### 👨‍🎓 Étudiant
- **Mon QR Code** : Génération d'un QR Code personnel infalsifiable.
- **Mon Emploi du temps** : Grille interactive générée dynamiquement.
- **Mes Présences** : Suivi de son taux d'assiduité par matière et alertes en cas de risque.

---

## 🛠️ Stack Technique & Architecture

### Backend (API REST)
- **Framework** : FastAPI (Python 3.12)
- **Base de données** : PostgreSQL
- **ORM** : SQLAlchemy
- **Sécurité** : JWT (JSON Web Tokens), Passlib (Bcrypt) pour le hachage des mots de passe.
- **Intelligence Artificielle** : DeepFace (modèle VGG-Face avec détecteur RetinaFace).

### Frontend (SPA)
- **Framework** : Vue.js 3 (Composition API `<script setup>`)
- **Stylisation** : Tailwind CSS v4
- **Gestion d'état** : Pinia
- **Routage** : Vue Router
- **Appels API** : Axios (avec intercepteurs pour le token)
- **Outils** : `html5-qrcode` (Scanner), `qrcode.vue` (Générateur), `jspdf` & `xlsx` (Exports).

---

## ⚙️ Prérequis et Installation

Assurez-vous d'avoir installé **Python 3.12+**, **Node.js 18+** et **PostgreSQL**.

### 1. Configuration du Backend
```bash
# Se déplacer dans le dossier backend
cd backend

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
# Créez un fichier .env à la racine du backend avec :
# DATABASE_URL=postgresql://utilisateur:motdepasse@localhost:5432/nom_de_la_base
# SECRET_KEY=votre_cle_secrete_jwt
# ALGORITHM=HS256

# Initialiser la base de données et créer l'Admin par défaut
python reset_db.py

# Lancer le serveur
uvicorn app.main:app --reload
```

### 2. Configuration du Frontend
```
# Se déplacer dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```
### L'application sera accessible sur http://localhost:5173.
### Identifiants par défaut : admin@ecole.com / admin123

### 3.Structure du Projet (Monorepo)
```
projet_presences/
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── models/           # Modèles SQLAlchemy (Tables)
│   │   ├── schemas/          # Schémas Pydantic (Validation)
│   │   ├── routes/           # Endpoints de l'API
│   │   ├── services/         # Logique métier & IA
│   │   └── dependencies.py   # Middlewares & Sécurité JWT
│   └── photos_reference/     # Stockage local des visages (Ignoré par Git)
│
└── frontend/                 # Application Vue.js
    ├── src/
    │   ├── components/       # Composants divisés par rôle (admin, prof, etudiant)
    │   ├── views/            # Pages principales (Login, Dashboard)
    │   ├── stores/           # Pinia (Gestion de l'authentification)
    │   └── services/         # Configuration Axios
    └── tailwind.config.js
```

### Auteur

Ulrich (Ulrichjack) - Développeur Fullstack
Projet réalisé dans le cadre d'une soutenance académique.
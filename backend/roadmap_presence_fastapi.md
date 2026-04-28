# ROADMAP COMPLET — Système de Suivi des Présences
## QR Code + Reconnaissance Faciale
### Stack : FastAPI (Backend) + Vue.js (Frontend)

---

## POURQUOI VUE.JS ET PAS ANGULAR ?

Angular est un framework très puissant mais très complexe pour un débutant. Il impose
TypeScript, une structure rigide, et beaucoup de concepts avancés à apprendre en même temps.
Vue.js fait exactement la même chose mais est conçu pour être appris progressivement.
Tu peux commencer simple et ajouter de la complexité au fur et à mesure. Pour un projet
école avec FastAPI à apprendre en parallèle, Vue.js est le bon choix.

---

## COMPRENDRE L'ARCHITECTURE GLOBALE AVANT TOUT

Avant d'écrire la moindre ligne de code, il faut comprendre comment les pièces
s'assemblent. Voici comment l'application fonctionne de bout en bout.

L'étudiant arrive en classe. Deux choses peuvent se passer : soit il scanne son QR Code
personnel avec une tablette ou un téléphone posé à l'entrée, soit une webcam capture
son visage et le système le reconnaît automatiquement. Dans les deux cas, le système
enregistre sa présence avec l'heure et le cours concerné. L'enseignant peut ensuite
consulter un tableau de bord en temps réel et exporter des rapports.

### Les trois couches de l'application

**Couche 1 — Le Frontend (Vue.js)**
C'est ce que l'utilisateur voit dans son navigateur. Il y a deux interfaces distinctes :
une interface étudiant (scan QR ou reconnaissance faciale) et une interface enseignant
ou administrateur (tableau de bord, gestion des cours, rapports).

**Couche 2 — Le Backend (FastAPI)**
C'est le cerveau. Il reçoit les requêtes du frontend, exécute la logique métier,
interroge la base de données, lance l'OCR ou la reconnaissance faciale, et renvoie
les résultats. Le frontend ne parle qu'au backend via des appels API.

**Couche 3 — La Base de données (PostgreSQL)**
C'est la mémoire. Elle stocke les étudiants, les cours, les présences, les photos
de référence des visages.

### Schéma de communication simplifié

```
[Navigateur Vue.js] ←→ [API FastAPI] ←→ [PostgreSQL]
                              ↓
                    [OpenCV / DeepFace]
                    [Bibliothèque QR Code]
```

**Cherche sur Google pour comprendre :**
- "Qu'est ce qu'une API REST explication simple"
- "Difference frontend backend explication débutant"
- "Comment fonctionne HTTP requête réponse"

---

## LES DIAGRAMMES À PRODUIRE

Avant de coder quoi que ce soit, ton dossier de projet doit contenir ces diagrammes.
Ils servent à réfléchir avant d'agir et à communiquer ton architecture clairement.

### 1. Diagramme des Cas d'Utilisation (Use Case)

Ce diagramme montre qui fait quoi dans le système. Les acteurs principaux sont :
l'Étudiant, l'Enseignant, et l'Administrateur.

**Cas d'utilisation de l'Étudiant :**
- Scanner son QR Code pour marquer sa présence
- Se faire identifier par reconnaissance faciale

**Cas d'utilisation de l'Enseignant :**
- Consulter la liste des présents pour un cours
- Générer et exporter un rapport de présences
- Voir les statistiques d'assiduité

**Cas d'utilisation de l'Administrateur :**
- Créer et gérer les comptes étudiants
- Enregistrer les photos de référence des étudiants
- Créer les cours et les emplois du temps
- Générer les QR Codes individuels

**Outil recommandé pour dessiner :** draw.io (gratuit, en ligne, aucune installation)
**Cherche sur Google :** "diagramme cas utilisation UML exemple école"

### 2. Diagramme de Classes

Ce diagramme montre les entités de ta base de données et leurs relations.

**Classe Etudiant :**
- id (identifiant unique)
- nom
- prénom
- numéro matricule
- email
- photo_reference (chemin vers la photo stockée)
- qr_code (valeur unique du QR Code)
- date_inscription

**Classe Cours :**
- id
- nom_matiere
- code_cours
- enseignant_id (lien vers Enseignant)
- jour
- heure_debut
- heure_fin
- salle

**Classe Presence :**
- id
- etudiant_id (lien vers Etudiant)
- cours_id (lien vers Cours)
- date_heure_arrivee
- methode (QR_CODE ou FACIALE)
- statut (PRESENT, RETARD, ABSENT)

**Classe Enseignant :**
- id
- nom
- prénom
- email
- mot_de_passe (hashé, jamais en clair)
- role (ENSEIGNANT ou ADMIN)

**Relations entre classes :**
- Un Enseignant enseigne plusieurs Cours (1 vers N)
- Un Cours a plusieurs Présences (1 vers N)
- Un Etudiant a plusieurs Présences (1 vers N)

**Cherche sur Google :** "diagramme de classes UML relation association agrégation"

### 3. Diagramme de Séquence

Ce diagramme montre le déroulement chronologique d'une action précise.
Fais-en un pour chaque scénario important.

**Scénario 1 — Marquage de présence par QR Code :**
1. L'étudiant présente son QR Code devant la caméra ou lecteur
2. Le Frontend envoie la valeur du QR Code au Backend
3. Le Backend vérifie que le QR Code correspond à un étudiant existant
4. Le Backend vérifie qu'un cours est en cours à cet horaire dans cette salle
5. Le Backend enregistre la présence en base de données
6. Le Backend renvoie une confirmation au Frontend
7. Le Frontend affiche "Présence enregistrée — Bienvenue Prénom NOM"

**Scénario 2 — Marquage par reconnaissance faciale :**
1. La webcam capture une image en temps réel
2. Le Frontend envoie l'image capturée au Backend
3. Le Backend passe l'image dans DeepFace/OpenCV
4. DeepFace compare le visage avec les photos de référence en base
5. Si correspondance trouvée, le Backend identifie l'étudiant
6. Le Backend enregistre la présence
7. Le Backend renvoie le nom de l'étudiant identifié au Frontend
8. Le Frontend affiche la confirmation

**Cherche sur Google :** "diagramme de séquence UML exemple connexion utilisateur"

---

## PHASE 1 — PRÉPARATION DE L'ENVIRONNEMENT

### Ce qu'il faut installer sur ton ordinateur

**Python 3.11 ou 3.12**
Python est le langage de tout ton backend. Télécharge-le depuis python.org. Lors
de l'installation sur Windows, coche absolument la case "Add Python to PATH".

**Cherche sur Google :** "installer Python 3.12 Windows tutoriel"

**Visual Studio Code**
C'est l'éditeur de code recommandé pour ce projet. Léger, gratuit, excellent support
Python et Vue.js via des extensions. Installe les extensions Python, Pylance,
et Volar (pour Vue.js).

**Node.js**
Nécessaire pour faire fonctionner Vue.js. Télécharge la version LTS depuis nodejs.org.

**PostgreSQL**
La base de données. Télécharge-le depuis postgresql.org. Retiens bien le mot de passe
que tu crées pendant l'installation, tu en auras besoin.

**DBeaver**
Un outil graphique gratuit pour visualiser et gérer ta base de données PostgreSQL
sans écrire de SQL à la main au début.

**Cherche sur Google :** "installer PostgreSQL Windows DBeaver tutoriel débutant"

### Organisation des dossiers du projet

Voici comment organiser ton projet dès le départ. Une bonne structure évite
la confusion quand le projet grossit.

```
projet_presences/
│
├── backend/                    ← Tout le code FastAPI est ici
│   ├── app/
│   │   ├── main.py             ← Point d'entrée de l'application
│   │   ├── database.py         ← Configuration connexion PostgreSQL
│   │   ├── models/             ← Les classes qui représentent tes tables
│   │   ├── schemas/            ← La forme des données échangées avec le frontend
│   │   ├── routes/             ← Les routes de ton API (URL)
│   │   ├── services/           ← La logique métier (OCR, QR, reconnaissance)
│   │   └── utils/              ← Fonctions utilitaires réutilisables
│   ├── requirements.txt        ← Liste de toutes les bibliothèques Python
│   └── .env                    ← Variables d'environnement (mot de passe DB, etc.)
│
├── frontend/                   ← Tout le code Vue.js est ici
│   ├── src/
│   │   ├── views/              ← Les pages de l'application
│   │   ├── components/         ← Les composants réutilisables
│   │   ├── services/           ← Les appels vers l'API FastAPI
│   │   └── router/             ← La navigation entre les pages
│   └── package.json
│
└── docs/                       ← Tes diagrammes UML et documentation
```

**Cherche sur Google :** "bonne structure projet FastAPI organisation dossiers"

---

## PHASE 2 — COMPRENDRE FASTAPI AVANT DE CODER

### Le concept fondamental d'une API REST

FastAPI crée des URLs que le frontend peut appeler pour obtenir ou envoyer des données.
Ces URLs s'appellent des endpoints ou routes. Chaque route fait une chose précise.

Par exemple :
- GET /etudiants → renvoie la liste de tous les étudiants
- GET /etudiants/42 → renvoie l'étudiant avec l'id 42
- POST /presences → crée une nouvelle présence
- DELETE /cours/5 → supprime le cours numéro 5

GET, POST, DELETE sont des méthodes HTTP. Elles indiquent l'intention de l'action.

**Cherche sur Google :**
- "méthodes HTTP GET POST PUT DELETE explication simple"
- "FastAPI tutorial officiel français"
- "FastAPI documentation officielle" (docs.fastapi.tiangolo.com — lire les 3 premières sections)

### Les concepts FastAPI à comprendre dans l'ordre

**1. Les routes et fonctions**
Chaque URL est liée à une fonction Python. Quand le frontend appelle cette URL,
la fonction s'exécute et renvoie un résultat.

**2. Pydantic — la validation des données**
FastAPI utilise Pydantic pour valider automatiquement les données reçues. Si le
frontend envoie des données incorrectes, FastAPI renvoie une erreur claire sans
que tu aies à écrire de vérification manuellement.

**3. SQLAlchemy — parler à la base de données**
SQLAlchemy est une bibliothèque Python qui te permet de manipuler PostgreSQL avec
du Python au lieu d'écrire du SQL brut. On appelle ça un ORM (Object Relational Mapper).

**4. La gestion des fichiers**
Pour recevoir des images (reconnaissance faciale), FastAPI gère nativement l'upload
de fichiers. Tu dois comprendre comment recevoir un fichier, le sauvegarder
temporairement, et le passer à ta bibliothèque de reconnaissance.

**5. L'authentification JWT**
Les enseignants et administrateurs doivent se connecter. FastAPI utilise des tokens
JWT (JSON Web Token) pour sécuriser les routes. Un token est une chaîne de caractères
chiffrée qui prouve que tu es bien connecté. Le frontend le stocke et l'envoie
à chaque requête.

**Cherche sur Google :**
- "SQLAlchemy ORM débutant explication"
- "Pydantic validation données Python explication"
- "JWT token authentification explication simple"
- "FastAPI authentification JWT tutoriel"

---

## PHASE 3 — LES MODULES À DÉVELOPPER DANS L'ORDRE

### Module 1 — Gestion des étudiants et enseignants (commencer ici)

C'est le module le plus simple et il te permet de comprendre FastAPI sans
la complexité de la reconnaissance faciale. Tu crées les routes pour :
créer un étudiant, lister les étudiants, modifier un étudiant, supprimer un étudiant.
C'est ce qu'on appelle un CRUD (Create, Read, Update, Delete). Tout développeur
backend doit maîtriser ça.

**Bonne pratique importante :** Ne jamais stocker un mot de passe en clair dans
la base de données. Toujours le "hasher" avec une bibliothèque comme bcrypt.
Si ta base de données est piratée, les mots de passe restent illisibles.

**Cherche sur Google :** "FastAPI CRUD PostgreSQL SQLAlchemy tutoriel complet"

### Module 2 — Gestion des cours et emplois du temps

Même logique que le Module 1 mais pour les cours. L'important ici est de bien
modéliser la relation entre un cours et un enseignant dans la base de données.
Un cours appartient à un enseignant. Un enseignant peut avoir plusieurs cours.

### Module 3 — Génération des QR Codes

Chaque étudiant reçoit un QR Code unique à sa création. Ce QR Code encode
une valeur unique (son matricule ou un identifiant UUID généré aléatoirement).
La bibliothèque Python qrcode génère une image PNG du QR Code que tu stockes
et que tu peux imprimer ou envoyer par email à l'étudiant.

**Cherche sur Google :** "Python qrcode bibliothèque générer QR Code image"

### Module 4 — Scan et validation du QR Code

Quand l'étudiant scanne son QR Code, le frontend lit la valeur encodée et l'envoie
au backend. Le backend vérifie si la valeur correspond à un étudiant, vérifie si
un cours est actif à cet instant, et enregistre la présence. Si l'étudiant arrive
après un certain délai (exemple : 15 minutes après le début du cours), le statut
est automatiquement mis à RETARD au lieu de PRESENT.

### Module 5 — Reconnaissance Faciale

C'est le module le plus technique. Voici comment il fonctionne conceptuellement.

**Phase d'enregistrement (à faire une seule fois par étudiant) :**
L'administrateur prend une photo de l'étudiant ou importe une photo. Cette photo
est stockée sur le serveur et son chemin est enregistré en base de données.
DeepFace analyse cette photo et crée une "empreinte" mathématique du visage
(un vecteur numérique). Cette empreinte peut être précalculée et stockée pour
accélérer les comparaisons.

**Phase de reconnaissance (à chaque cours) :**
La webcam capture une image. Le backend reçoit cette image, passe l'image dans
DeepFace, DeepFace compare le visage capturé avec toutes les empreintes stockées,
renvoie l'identifiant de l'étudiant si la similarité dépasse un seuil défini.

**Points importants à comprendre :**
La qualité de la photo de référence est cruciale. Une photo floue ou mal éclairée
donnera de mauvais résultats. Il faut prévoir un message d'erreur quand aucun
visage n'est reconnu. Il faut aussi un seuil de confiance configurable — si la
reconnaissance donne 60% de similarité, ce n'est pas assez certain pour valider
une présence automatiquement.

**Cherche sur Google :**
- "DeepFace Python tutoriel reconnaissance faciale"
- "OpenCV Python capture webcam tutoriel"
- "DeepFace vs face_recognition Python comparaison"

### Module 6 — Tableau de bord et statistiques

L'enseignant se connecte et voit pour chaque cours le nombre de présents, de retards
et d'absents. Des graphiques montrent l'évolution de l'assiduité dans le temps.
Vue.js avec la bibliothèque Chart.js permet de faire des graphiques sans difficulté.

**Cherche sur Google :** "Vue.js Chart.js graphique tutoriel"

### Module 7 — Export des rapports

L'enseignant peut exporter la liste de présences en PDF ou Excel.
En Python, openpyxl génère des fichiers Excel et ReportLab génère des PDFs.
Le fichier généré est renvoyé au frontend qui déclenche le téléchargement.

**Cherche sur Google :**
- "FastAPI télécharger fichier response FileResponse"
- "Python openpyxl créer fichier Excel tutoriel"
- "Python ReportLab générer PDF tutoriel"

---

## PHASE 4 — LE FRONTEND VUE.JS

### Les pages à créer

**Page de connexion**
Formulaire email + mot de passe. Au succès, le token JWT est stocké et
l'utilisateur est redirigé vers son tableau de bord.

**Page de scan (accessible sans connexion sur la tablette d'entrée)**
Interface plein écran simple avec la webcam active ou un champ pour scanner
le QR Code. Elle affiche un message de confirmation ou d'erreur après chaque scan.

**Page tableau de bord enseignant**
Vue d'ensemble des cours du jour, statistiques rapides, liste des absents.

**Page détail d'un cours**
Liste complète des étudiants avec leur statut pour ce cours. Bouton d'export.

**Page gestion étudiants (admin seulement)**
Tableau avec tous les étudiants, ajout, modification, suppression, upload photo.

### Comment Vue.js communique avec FastAPI

Le frontend utilise une bibliothèque appelée Axios pour envoyer des requêtes HTTP
vers ton API FastAPI. Ce n'est pas compliqué — c'est simplement du JavaScript qui
dit "envoie cette donnée à cette URL et donne-moi la réponse".

**Cherche sur Google :**
- "Vue.js 3 tutoriel débutant français"
- "Axios Vue.js appel API REST tutoriel"
- "Vue Router navigation entre pages tutoriel"

---

## PHASE 5 — BONNES PRATIQUES DE DÉVELOPPEMENT

### Utiliser un environnement virtuel Python

Un environnement virtuel isole les bibliothèques de ton projet. Si tu travailles
sur plusieurs projets Python, chacun a ses propres bibliothèques sans conflits.
Crée toujours un environnement virtuel avant d'installer quoi que ce soit.

**Cherche sur Google :** "Python environnement virtuel venv explication"

### Le fichier .env pour les secrets

Ne mets jamais ton mot de passe de base de données directement dans le code.
Utilise un fichier .env qui contient toutes les variables sensibles. Ce fichier
ne doit JAMAIS être mis sur GitHub ou partagé. Ajoute-le dans .gitignore.

**Cherche sur Google :** "Python dotenv variables environnement tutoriel"

### Utiliser Git dès le premier jour

Git est un outil de versionnage. Il sauvegarde l'historique de toutes tes modifications.
Si tu casses quelque chose, tu peux revenir en arrière. C'est indispensable.
Crée un dépôt sur GitHub pour ton projet dès le début.

**Cherche sur Google :** "Git tutoriel débutant commandes de base français"

### Tester son API avec Swagger UI

FastAPI génère automatiquement une interface de test à l'adresse /docs quand
ton serveur tourne. Tu peux tester chaque route directement depuis le navigateur
sans avoir besoin du frontend. Utilise-la constamment pendant le développement.

### Nommer les choses clairement

Les variables, fonctions, et fichiers doivent avoir des noms explicites.
"get_student_by_id" est mieux que "gsbi". "presence_router.py" est mieux que "pr.py".
Un bon code se lit comme de la prose.

---

## RÉSUMÉ DE L'ORDRE DE DÉVELOPPEMENT RECOMMANDÉ

**Semaine 1-2 :** Installer l'environnement. Comprendre FastAPI avec les tutoriels officiels.
Dessiner les diagrammes UML. Créer la structure des dossiers.

**Semaine 3-4 :** Créer la base de données PostgreSQL. Développer le module étudiants
(CRUD complet). Tester avec Swagger UI.

**Semaine 5 :** Développer le module cours. Ajouter l'authentification JWT.

**Semaine 6 :** Développer la génération et validation des QR Codes.

**Semaine 7-8 :** Développer la reconnaissance faciale avec DeepFace. C'est la partie
la plus longue à cause de la configuration d'OpenCV.

**Semaine 9 :** Développer le tableau de bord et les exports.

**Semaine 10-11 :** Développer le frontend Vue.js en connectant chaque page à l'API.

**Semaine 12 :** Tests complets, corrections de bugs, préparation de la présentation.

---

## BIBLIOTHÈQUES PYTHON À INSTALLER

- fastapi — le framework web
- uvicorn — le serveur qui fait tourner FastAPI
- sqlalchemy — pour parler à PostgreSQL
- psycopg2-binary — connecteur Python/PostgreSQL
- pydantic — validation des données (inclus avec FastAPI)
- python-jose — pour les tokens JWT
- passlib[bcrypt] — pour hasher les mots de passe
- python-multipart — pour recevoir des fichiers uploadés
- qrcode[pil] — pour générer les QR Codes
- deepface — pour la reconnaissance faciale
- opencv-python — pour la capture webcam et traitement d'images
- openpyxl — pour générer des fichiers Excel
- reportlab — pour générer des PDFs
- python-dotenv — pour lire le fichier .env

**Cherche sur Google :** "pip install Python packages tutoriel"

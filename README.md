# 📚 Memora

## À propos du projet

Memora est une plateforme web de révision développée dans le cadre de l'UE Projet de Licence 3 Informatique à Aix-Marseille Université.

L'objectif de l'application est d'aider les étudiants à organiser et optimiser leurs révisions à partir de leurs propres supports de cours. En important un document PDF, l'utilisateur peut générer différents outils de révision grâce à l'intelligence artificielle, tels que des résumés, des flashcards, des quiz ou encore des plannings personnalisés.

L'application propose également des fonctionnalités d'organisation (planning et gestion des tâches), ainsi qu'un espace communautaire permettant aux étudiants d'échanger entre eux.

---

## Fonctionnalités principales

### 📄 Gestion des cours

* Importation de documents PDF
* Consultation des cours enregistrés
* Modification et suppression de cours
* Recherche et organisation des documents

### 🤖 Assistant Memi

Memi est l'assistant intelligent intégré à la plateforme. Il permet à l'utilisateur d'obtenir des explications et de poser des questions à propos des cours importés.

### 📝 Résumés automatiques

À partir du contenu d'un PDF, l'application peut générer un résumé synthétique afin de faciliter la compréhension et la révision des notions importantes.

### 🗂️ Flashcards

* Génération automatique de flashcards
* Création manuelle de cartes
* Révision interactive
* Gestion de plusieurs decks

### ✅ Quiz

* Génération automatique de quiz
* Questions à choix multiples
* Correction automatique
* Suivi des résultats

### 📅 Planning de révision

* Création manuelle de séances de révision
* Gestion des disponibilités
* Génération automatique de plannings via l'IA

### ✔️ To-Do List

* Création et gestion de tâches
* Priorités et échéances
* Suivi de progression

### 💬 Forum

* Publication de messages
* Commentaires et échanges entre étudiants
* Catégorisation des discussions

### 👤 Gestion du profil

* Modification des informations personnelles
* Changement de mot de passe
* Personnalisation du compte

---

## Architecture du projet

L'application est composée de deux parties principales :

### Frontend

Le frontend a été développé avec React et Vite. Il est responsable de l'interface utilisateur, de la navigation et des interactions avec l'API.

### Backend

Le backend repose sur Django et Django REST Framework. Il gère l'authentification, les données utilisateur, les cours, les fonctionnalités IA ainsi que l'ensemble des services de l'application.

### Base de données

Les données sont stockées dans une base SQLite durant le développement.

### Intelligence artificielle

Les fonctionnalités de génération de contenu utilisent l'API OpenAI pour la création de résumés, flashcards, quiz et plannings.

---

## Technologies utilisées

### Frontend

* React
* Vite
* Tailwind CSS
* React Router
* Framer Motion

### Backend

* Python
* Django
* Django REST Framework
* Token Authentication
* django-cors-headers

### Base de données

* SQLite

### Services externes

* OpenAI API
* Bibliothèques de traitement PDF

---

## Structure du projet

```text
memora/
│
├── Backend/
│   ├── accounts/
│   ├── courses/
│   ├── planning/
│   ├── todos/
│   ├── forum/
│   └── ai_service/
│
├── frontend/
│   ├── components/
│   ├── layouts/
│   ├── pages/
│   ├── services/
│   └── utils/
│
├── database/
│
└── README.md
```

---

## Prérequis

Avant d'installer le projet, vérifier que les outils suivants sont disponibles :

* Python 3
* pip
* Node.js
* npm
* Une clé API OpenAI

---

## Installation

### Cloner le dépôt

```bash
git clone <url-du-projet>
cd memora
```

### Installation du backend

```bash
cd Backend

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Créer ensuite le fichier `.env` à partir du modèle fourni.

### Installation du frontend

```bash
cd frontend

npm install
```

Créer également le fichier `.env` à partir du modèle fourni.

---

## Configuration

### Backend (.env)

Exemple de configuration :

```env
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_TIME_ZONE=Europe/Paris

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FRONTEND_URL=http://localhost:5173

OPENAI_API_KEY=

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Frontend (.env)

```env
VITE_API_ORIGIN=http://127.0.0.1:8000
```

---

## Lancement du projet

### Démarrage du backend

```bash
cd Backend

python manage.py migrate
python manage.py runserver
```

Le serveur sera accessible à l'adresse :

```text
http://127.0.0.1:8000
```

### Démarrage du frontend

```bash
cd frontend

npm run dev
```

L'application sera accessible à l'adresse :

```text
http://localhost:5173
```

---

## Maintenance

Après toute modification des modèles Django :

```bash
python manage.py makemigrations
python manage.py migrate
```

Vérification du backend :

```bash
python manage.py check
```

Exécution des tests :

```bash
python manage.py test
```

Vérification du frontend :

```bash
npm run lint
npm run build
```

---

## Auteurs

Projet réalisé par :

* Alice Barka
* Manal Chabane
* Faiza Siroukane

Licence 3 Informatique - Aix-Marseille Université

Année universitaire 2025-2026

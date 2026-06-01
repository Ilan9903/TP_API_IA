# 🐧 Penguin Classifier API

API REST développée avec FastAPI permettant de prédire l'espèce d'un manchot (pingouin) de l'archipel Palmer à partir de ses mensurations.

La prédiction est effectuée par un modèle de Machine Learning (**Random Forest**) entraîné au préalable.

L'API intègre également l'API de **Mistral AI** pour générer des descriptions textuelles naturelles des espèces reconnues.

Le projet est conçu pour être conteneurisé avec **Docker** et déployé de manière automatisée sur **Render**.

---

# 🏗️ Architecture du projet

Le code respecte une architecture orientée objet (**OOP**) qui sépare clairement les responsabilités (modèles, services, routes) :

- **`app/main.py`** : Point d'entrée de l'application, déclare l'instance FastAPI et les routes HTTP.
- **`app/schemas.py`** : Définit le contrat de données (entrées et sorties) grâce aux modèles Pydantic, garantissant la validation automatique des types.
- **`app/service.py`** : Contient la logique métier, notamment le chargement des fichiers `.pkl` (au démarrage) et l'appel à l'API externe Mistral.
- **`models/`** : Dossier contenant le modèle Random Forest (`model.pkl`) et l'encodeur (`encoder.pkl`) générés lors de la phase d'entraînement.
- **`notebook/train.ipynb`** : Jupyter Notebook contenant le pipeline complet de data science (nettoyage, entraînement, évaluation et exportation du modèle).
- **`Dockerfile`** : Script de construction de l'image Docker basée sur `python:3.11-slim`.
- **`requirements.txt`** : Liste des dépendances Python nécessaires (FastAPI, Scikit-Learn, Uvicorn, etc.) figées dans des versions spécifiques pour garantir la stabilité.

---

# 🚀 Fonctionnalités (Endpoints)

## `GET /health`

Vérifie l'état du serveur et renvoie la version du modèle en service.

### Réponse exemple

```json
{
  "status": "ok",
  "model_version": "1.0.0"
}
```

---

## `POST /predict`

Reçoit 4 caractéristiques numériques :

- Longueur du bec (`bill_length_mm`)
- Hauteur du bec (`bill_depth_mm`)
- Longueur de la nageoire (`flipper_length_mm`)
- Masse corporelle (`body_mass_g`)

Retourne :

- L'espèce prédite
- L'indice de confiance associé

### Exemple de requête

```json
{
  "bill_length_mm": 39.1,
  "bill_depth_mm": 18.7,
  "flipper_length_mm": 181,
  "body_mass_g": 3750
}
```

### Exemple de réponse

```json
{
  "species": "Adelie",
  "confidence": 0.96
}
```

---

## `POST /analyze`

Effectue la même prédiction que l'endpoint `/predict` mais interroge également **Mistral AI** afin de générer une description pédagogique de l'animal détecté.

### Exemple de réponse

```json
{
  "species": "Adelie",
  "confidence": 0.96,
  "description": "Le manchot Adélie est une espèce emblématique de l'Antarctique, connue pour son comportement social et son adaptation aux climats extrêmes."
}
```

---

# ⚙️ Installation et exécution en local

## Prérequis

- Python 3.11+
- Une clé d'API Mistral valide

## Configuration

### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd penguin-classifier-api
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l'environnement

**Windows**

```powershell
.\.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet en s'appuyant sur le fichier `.env.example` :

```env
MISTRAL_API_KEY=votre_cle_ici
BASE_URL=votre_url_locale_ou_prod (generalement http://localhost:8000)
```

> ⚠️ Ce fichier doit rester strictement local et ne jamais être versionné. Il est ignoré par Git pour des raisons de sécurité.

---

## Lancement de l'application

Démarrer le serveur Uvicorn avec rechargement automatique :

```bash
uvicorn app.main:app --reload --port 8000
```

L'API sera accessible à l'adresse :

```text
http://localhost:8000
```

Documentation interactive Swagger :

```text
http://localhost:8000/docs
```

---

# 🐳 Exécution via Docker

## Construire l'image

```bash
docker build -t penguin-api:v1 .
```

## Lancer le conteneur

```bash
docker run -d \
  --name penguin-api \
  -p 8000:8000 \
  -e MISTRAL_API_KEY=votre_cle_ici \
  -e BASE_URL=votre_url_locale_ou_prod \
  penguin-api:v1
```

> 🔒 Bonne pratique : les secrets (clés API, mots de passe, tokens) ne doivent jamais être écrits en dur dans le `Dockerfile`. Ils doivent être injectés à l'exécution via des variables d'environnement.

---

# 📂 Structure du projet

```text
penguin-classifier-api/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── service.py
│
├── models/
│   ├── model.pkl
│   └── encoder.pkl
│
├── notebook/
│   └── train.ipynb
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# 👨‍💻 Auteur

**Ilan**

- Apprenti Concepteur Développeur d'Applications (CDA)
- EPSI Bachelor SIN
- Spécialisation DevOps & Full Stack

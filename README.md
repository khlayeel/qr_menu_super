# QR Menu — Menu Digital pour Cafés

Une plateforme SaaS moderne permettant aux cafés tunisiens de remplacer leur menu papier par un **menu digital accessible via QR Code**.

## 🎯 Vision

Moderniser l'expérience des clients et des propriétaires de cafés avec une solution simple, rapide et professionnelle.

```
Propriétaire du Café
   ↓
Dashboard Simple
   ↓
Gère son menu
   ↓
Génère QR Code
           ↓
          QR Code
           ↓
        Client
           ↓
        Scanne
           ↓
      Voir menu
```

---

## 🚀 Fonctionnalités (MVP Basic)

### Pour le Propriétaire

✅ Inscription et connexion sécurisée  
✅ Gestion du profil du café (nom, logo, description)  
✅ CRUD complet des catégories  
✅ CRUD complet des produits  
✅ Gestion des images (logo + photos produits)  
✅ Gestion des prix en temps réel  
✅ Disponibilité des produits  
✅ Organisation des catégories et produits  
✅ Génération QR Code  
✅ Téléchargement QR Code PNG  
✅ Impression QR Code  

### Pour le Client

✅ Accès instantané au menu via QR Code  
✅ Pas d'inscription requise  
✅ Affichage du café (logo, nom, description)  
✅ Navigation par catégories  
✅ Visualisation des produits avec photos  
✅ Voir les prix et descriptions  
✅ Voir la disponibilité des produits  
✅ Recherche de produits  
✅ Interface mobile-first ultra-rapide  

---

## 🛠 Stack Technique

### Backend
- **Python 3.10+**
- **FastAPI** — Framework web moderne
- **SQLAlchemy** — ORM pour la base de données
- **Alembic** — Migration de base de données
- **Pydantic** — Validation des données
- **JWT** — Authentification sécurisée
- **bcrypt** — Hash des mots de passe

### Database
- **MySQL** 8.0+ avec charset UTF-8MB4 (support arabe)

### Frontend
- **HTML5**
- **CSS3** (Responsive, Mobile-First)
- **JavaScript Vanilla** (ECMAScript 6+)

### Autres
- **QRCode** — Génération de codes QR
- **Pillow** — Traitement d'images
- **python-slugify** — Génération de slugs
- **python-dotenv** — Variables d'environnement

---

## 📁 Structure du Projet

```
qr-menu/
├── backend/
│   ├── app/
│   │   ├── main.py              # Point d'entrée FastAPI
│   │   ├── database.py          # Configuration SQLAlchemy
│   │   │
│   │   ├── core/
│   │   │   ├── config.py        # Configuration centralisée
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/              # Modèles SQLAlchemy (phase 6)
│   │   │   └── __init__.py
│   │   │
│   │   ├── schemas/             # Schémas Pydantic (phase 7)
│   │   │   └── __init__.py
│   │   │
│   │   ├── routers/             # Endpoints API (phases 7-12)
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/            # Logique métier (phase 8+)
│   │   │   └── __init__.py
│   │   │
│   │   ├── utils/               # Fonctions utilitaires
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── alembic/                 # Migrations (phase 5)
│   │   └── env.py
│   │
│   ├── tests/                   # Tests (phase 17)
│   │   └── __init__.py
│   │
│   ├── uploads/                 # Fichiers uploadés (phase 15)
│   │   └── .gitkeep
│   │
│   ├── requirements.txt         # Dépendances Python
│   ├── .env.example             # Exemple de configuration
│   └── README_BACKEND.md        # Documentation backend
│
├── frontend/
│   ├── index.html               # Page d'accueil
│   ├── login.html               # Connexion propriétaire
│   ├── dashboard.html           # Dashboard propriétaire
│   ├── menu.html                # Menu public clients
│   │
│   ├── css/
│   │   ├── style.css            # Styles généraux
│   │   └── menu.css             # Styles du menu public
│   │
│   ├── js/
│   │   ├── app.js               # Utilities globales
│   │   ├── auth.js              # Authentification
│   │   ├── dashboard.js         # Logique dashboard
│   │   └── menu.js              # Logique menu public
│   │
│   └── README_FRONTEND.md       # Documentation frontend
│
├── .gitignore                   # Fichiers à ignorer Git
├── .env.example                 # Configuration exemple
├── README.md                    # Ce fichier
└── LICENSE                      # Licence du projet
```

---

## 🚦 Phases de Développement

| Phase | Titre | Durée Est. | Statut |
|-------|-------|-----------|--------|
| 1 | Analyse | 1-2h | ✅ Complété |
| 2 | Architecture | 1-2h | **🔄 En cours** |
| 3 | Setup Python/Env | 1-2h | ⏳ Planifié |
| 4 | FastAPI + MySQL | 4-6h | ⏳ Planifié |
| 5 | SQLAlchemy/Alembic | 4-6h | ⏳ Planifié |
| 6 | Modèles de données | 3-4h | ⏳ Planifié |
| 7 | Authentication | 6-8h | ⏳ Planifié |
| 8 | Gestion Café | 4-5h | ⏳ Planifié |
| 9 | CRUD Catégories | 3-4h | ⏳ Planifié |
| 10 | CRUD Produits | 6-8h | ⏳ Planifié |
| 11 | API Menu Public | 3-4h | ⏳ Planifié |
| 12 | Frontend Menu | 8-10h | ⏳ Planifié |
| 13 | Dashboard | 10-12h | ⏳ Planifié |
| 14 | Upload Images | 5-7h | ⏳ Planifié |
| 15 | QR Code | 2-3h | ⏳ Planifié |
| 16 | Tests | 6-8h | ⏳ Planifié |
| 17 | Responsive + UX | 8-10h | ⏳ Planifié |
| 18 | Sécurité | 6-8h | ⏳ Planifié |
| 19 | Déploiement | 4-6h | ⏳ Planifié |
| 20 | Documentation | 4-6h | ⏳ Planifié |

**Total estimé:** 120-160 heures

---

## 🏃 Démarrage Rapide

### Prérequis

- Python 3.10+
- MySQL 8.0+
- Node.js 16+ (optionnel, pour les outils frontend)
- Git

### Installation Backend

```bash
# 1. Cloner le repo
git clone https://github.com/yourusername/qr-menu.git
cd qr-menu

# 2. Créer un environnement virtuel Python
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

# 4. Installer les dépendances
cd backend
pip install -r requirements.txt

# 5. Créer le fichier .env
cp .env.example .env
# Éditer .env avec vos paramètres

# 6. Lancer le serveur
python -m uvicorn app.main:app --reload
```

Le serveur tournera sur `http://localhost:8000`

### Installation Frontend

```bash
# Le frontend ne nécessite pas d'installation
# Ouvrir un navigateur et accéder à
http://localhost:8000/frontend/index.html
```

---

## 📊 Architecture Base de Données

### Relations

```
USER (1) ──────→ (N) CAFE
CAFE (1) ──────→ (N) CATEGORY
CAFE (1) ──────→ (N) QRCODE
CATEGORY (1) ──→ (N) PRODUCT
```

### Entités

#### USER
```sql
id (PK) INT AUTO_INCREMENT
name VARCHAR(255) NOT NULL
email VARCHAR(255) UNIQUE NOT NULL
password_hash VARCHAR(255) NOT NULL
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

#### CAFE
```sql
id (PK) INT AUTO_INCREMENT
user_id (FK) INT NOT NULL
name VARCHAR(255) NOT NULL
slug VARCHAR(255) UNIQUE NOT NULL
logo VARCHAR(255)
description TEXT
address VARCHAR(255)
phone VARCHAR(20)
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### CATEGORY
```sql
id (PK) INT AUTO_INCREMENT
cafe_id (FK) INT NOT NULL
name VARCHAR(255) NOT NULL
position INT
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### PRODUCT
```sql
id (PK) INT AUTO_INCREMENT
category_id (FK) INT NOT NULL
name VARCHAR(255) NOT NULL
description TEXT
price DECIMAL(10,3) NOT NULL
image VARCHAR(255)
available BOOLEAN DEFAULT TRUE
position INT
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### QRCODE
```sql
id (PK) INT AUTO_INCREMENT
cafe_id (FK) INT UNIQUE NOT NULL
url VARCHAR(500) NOT NULL
image_path VARCHAR(255)
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

---

## 🔐 Sécurité

- ✅ Mots de passe hashés avec bcrypt
- ✅ JWT pour l'authentification
- ✅ Validation Pydantic sur toutes les entrées
- ✅ Protection CORS
- ✅ Variables d'environnement (.env)
- ✅ Pas de données sensibles en dur
- ✅ Protection contre les IDOR
- ✅ Validation des uploads

---

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Avec couverture
pytest --cov=app tests/
```

---

## 📝 API REST

### Authentication

```
POST   /api/auth/register     - Créer un compte
POST   /api/auth/login        - Se connecter
GET    /api/auth/me           - Données utilisateur
POST   /api/auth/logout       - Se déconnecter
```

### Cafes

```
GET    /api/cafes             - Lister les cafés de l'utilisateur
POST   /api/cafes             - Créer un café
GET    /api/cafes/{id}        - Détails d'un café
PUT    /api/cafes/{id}        - Mettre à jour un café
DELETE /api/cafes/{id}        - Supprimer un café
```

### Public Menu

```
GET    /cafe/{slug}           - Menu public du café
```

### Catégories

```
GET    /api/categories        - Lister les catégories
POST   /api/categories        - Créer une catégorie
PUT    /api/categories/{id}   - Modifier une catégorie
DELETE /api/categories/{id}   - Supprimer une catégorie
```

### Produits

```
GET    /api/products          - Lister les produits
POST   /api/products          - Créer un produit
PUT    /api/products/{id}     - Modifier un produit
DELETE /api/products/{id}     - Supprimer un produit
```

### QR Code

```
POST   /api/qrcodes           - Générer un QR Code
GET    /api/qrcodes/{cafe_id} - Obtenir le QR Code d'un café
```

---

## 🎨 Idées de Différenciation

1. **QR Code Personnalisé avec Branding** — QR avec logo du café
2. **Menu Multilingue FR/AR/EN** — Support complet du marché tunisien
3. **Mode Offline** — Menu accessible sans internet
4. **Analytics Simples** — Voir les produits les plus vus
5. **Promotions** — Badges "Nouveau" et "Promotion"
6. **Horaires d'Ouverture** — Afficher si le café est ouvert
7. **Galerie Photos Avancée** — Multiple photos par produit
8. **Dashboard Mobile** — Gérer le menu depuis le téléphone
9. **Design Ultra-Rapide** — < 100ms de chargement
10. **Paiement Intégré** — Architecture prête pour la Phase Pro

---

## 📦 Déploiement

### Production

```bash
# Générer build
python -m pip install --upgrade pip
pip install -r requirements.txt

# Lancer avec production settings
ENVIRONMENT=production python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Hébergement Recommandé

- **Backend:** Heroku (free tier available)
- **Database:** PlanetScale (MySQL gratuit)
- **Storage:** Firebase Storage ou AWS S3
- **Frontend:** Netlify ou Vercel

---

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

---

## 👤 Auteur

Développé par un étudiant tunisien en licence de développement web.

---

## 💬 Support

Pour toute question ou problème, ouvrir une issue sur GitHub.

---

## 🗺 Roadmap Future

### Version Pro
- Commandes en ligne
- Paiement intégré
- Gestion des tables
- Notifications
- Statistiques avancées

### Version AI
- Recommandations IA
- Assistant IA
- Analyse des ventes
- Upselling intelligent

### Version Enterprise
- POS (Point of Sale)
- KDS (Kitchen Display System)
- Multiple établissements
- Analytics avancés
- API externe

---

**Dernière mise à jour:** 2026-09-04  
**Statut:** 🔄 Développement en cours — Phase 2 — Architecture

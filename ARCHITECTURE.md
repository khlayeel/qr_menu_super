# 📐 ARCHITECTURE DÉTAILLÉE — QR MENU

## 1. Vue d'ensemble de l'Architecture

### Diagramme de flux

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS/PROPRIÉTAIRES                     │
├─────────────────────────────────────────────────────────────────┤
│
│  Propriétaire du café                 Client du café
│       ↓                                      ↓
│   Dashboard                           Scanner QR Code
│   (HTML/CSS/JS)                            ↓
│       ↓                                Menu Public
│   localStorage token                  (HTML/CSS/JS)
│       ↓                                      ↓
│  API Request                          API Request
│
├─────────────────────────────────────────────────────────────────┤
│                        BACKEND (Python/FastAPI)                  │
├─────────────────────────────────────────────────────────────────┤
│
│   ↓ (JWT Validation)
│   ├─ Authentication Middleware
│   │    ├─ User Login/Register
│   │    └─ Token Verification
│   │
│   ├─ API Routers
│   │    ├─ /auth/* → Authentication endpoints
│   │    ├─ /cafes/* → Cafe management
│   │    ├─ /categories/* → Category CRUD
│   │    ├─ /products/* → Product CRUD
│   │    └─ /qrcodes/* → QR Code generation
│   │
│   ├─ Services (Business Logic)
│   │    ├─ UserService
│   │    ├─ CafeService
│   │    ├─ CategoryService
│   │    ├─ ProductService
│   │    └─ QRCodeService
│   │
│   ├─ Models (SQLAlchemy ORM)
│   │    ├─ User
│   │    ├─ Cafe
│   │    ├─ Category
│   │    ├─ Product
│   │    └─ QRCode
│   │
│   └─ Database Connection (SQLAlchemy)
│
├─────────────────────────────────────────────────────────────────┤
│                   DATABASE (MySQL)                               │
├─────────────────────────────────────────────────────────────────┤
│
│   users
│   cafes
│   categories
│   products
│   qrcodes
│
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Couches de l'Application

### 2.1 Frontend (HTML/CSS/JavaScript)

**Responsabilité:** Interface utilisateur, interaction utilisateur

**Fichiers:**
- `index.html` → Page d'accueil
- `login.html` → Formulaire de connexion
- `dashboard.html` → Dashboard propriétaire
- `menu.html` → Menu public
- `css/style.css` → Styles principaux
- `css/menu.css` → Styles menu public
- `js/app.js` → Utilities globales
- `js/auth.js` → Logique authentification
- `js/dashboard.js` → Logique dashboard
- `js/menu.js` → Logique menu public

**Responsabilités:**
- ✅ Afficher l'interface
- ✅ Capturer les entrées utilisateur
- ✅ Effectuer les appels API
- ✅ Stocker le token JWT localement
- ✅ Gérer l'état de l'application simple

---

### 2.2 Backend (Python/FastAPI)

**Responsabilité:** Logique métier, validation, sécurité

#### 2.2.1 Structure Backend

```
backend/
├── app/
│   ├── main.py
│   │   └─ FastAPI app initialization
│   │   └─ CORS configuration
│   │   └─ Route mounting
│   │
│   ├── database.py
│   │   └─ SQLAlchemy engine
│   │   └─ Session factory
│   │   └─ get_db() dependency
│   │
│   ├── core/
│   │   └─ config.py
│   │      └─ Settings from .env
│   │      └─ Database configuration
│   │      └─ JWT configuration
│   │
│   ├── models/          (ORM Models - Phase 6)
│   │   ├─ user.py
│   │   ├─ cafe.py
│   │   ├─ category.py
│   │   ├─ product.py
│   │   └─ qrcode.py
│   │
│   ├── schemas/         (Pydantic Models - Phase 7)
│   │   ├─ user.py
│   │   ├─ cafe.py
│   │   ├─ category.py
│   │   ├─ product.py
│   │   └─ qrcode.py
│   │
│   ├── routers/         (API Endpoints - Phase 7+)
│   │   ├─ auth.py
│   │   ├─ cafes.py
│   │   ├─ categories.py
│   │   ├─ products.py
│   │   ├─ qrcodes.py
│   │   └─ public.py
│   │
│   ├── services/        (Business Logic - Phase 8+)
│   │   ├─ user_service.py
│   │   ├─ cafe_service.py
│   │   ├─ category_service.py
│   │   ├─ product_service.py
│   │   └─ qrcode_service.py
│   │
│   └── utils/           (Helpers)
│       ├─ security.py
│       ├─ uploads.py
│       └─ validation.py
│
└── tests/               (Unit Tests - Phase 16)
    ├─ test_auth.py
    ├─ test_cafes.py
    └─ test_products.py
```

#### 2.2.2 Flux de Requête API

```
Client HTTP Request
       ↓
FastAPI Application
       ↓
CORS Middleware
       ↓
Router (e.g., POST /api/cafes)
       ↓
Authentication Middleware (JWT Validation)
       ↓
Request Handler (async function)
       ↓
Pydantic Validation (schema)
       ↓
Service Layer (business logic)
       ↓
Database Layer (SQLAlchemy ORM)
       ↓
MySQL Database
       ↓
Response Construction
       ↓
JSON Response
       ↓
Client
```

---

## 3. Flux de Données

### 3.1 Flow de Connexion

```
1. User Input
   └─ email + password
   
2. Frontend (auth.js)
   └─ POST /api/auth/login
   └─ { email, password }
   
3. Backend (auth router)
   └─ Validate input (Pydantic)
   └─ Find user in database
   └─ Verify password (bcrypt.compare)
   └─ Generate JWT token
   
4. Response
   └─ { access_token, token_type }
   
5. Frontend
   └─ Store token in localStorage
   └─ Redirect to dashboard
```

### 3.2 Flow de Création de Produit

```
1. User Input (Dashboard)
   └─ name, price, category_id, description, image
   
2. Frontend (dashboard.js)
   └─ POST /api/products
   └─ Headers: Authorization: Bearer {token}
   └─ Body: { name, price, category_id, ... }
   
3. Backend (products router)
   └─ Extract token from headers
   └─ Verify token (get user_id)
   └─ Validate input (Pydantic)
   └─ Call product_service.create_product()
   
4. Service Layer
   └─ Verify cafe ownership
   └─ Create Product model
   └─ Save to database
   
5. Response
   └─ { id, name, price, ... }
   
6. Frontend
   └─ Show success message
   └─ Add product to list
   └─ Refresh UI
```

### 3.3 Flow de Visualisation du Menu Public

```
1. Client scanne QR Code
   └─ URL: https://example.com/cafe/cafe-el-bahri
   
2. Frontend (menu.js)
   └─ Extract slug from URL
   └─ GET /api/cafes/cafe-el-bahri (public endpoint)
   
3. Backend (public router)
   └─ Find cafe by slug
   └─ Load all categories (from cafe_id)
   └─ Load all products (from categories)
   └─ Return with images
   
4. Response
   └─ {
        cafe: { name, description, logo, ... },
        categories: [...],
        products: [...]
      }
   
5. Frontend
   └─ Render cafe info
   └─ Render categories tabs
   └─ Render products grid
   └─ Show images and prices
```

---

## 4. Modèles de Données (ERD)

### Relationships

```
┌────────────┐         ┌──────────┐
│   USER     │    1    │  CAFE    │     1
├────────────┤─────┬───┼──────────┤──┬──┐
│ id (PK)    │     │   │ id (PK)  │  │  │
│ name       │     │   │ user_id  │  │  │
│ email      │     │   │ name     │  │  │
│ password   │     │   │ slug     │  │  │
│ created_at │     │   │ logo     │  │  │
└────────────┘     │   └──────────┘  │  │
                   │                  │  │
                   │                  │  │
            ┌──────┴───────────┐      │  │
            │                  │      │  │
         (N)│ (1)           (1)│      │  │ (N)
            │                  │      │  │
       ┌────▼──────────┐      │  ┌───▼──▼──────┐
       │  CATEGORY     │      │  │  QRCODE     │
       ├───────────────┤      │  ├─────────────┤
       │ id (PK)       │      │  │ id (PK)     │
       │ cafe_id (FK)  │      │  │ cafe_id(FK) │
       │ name          │      │  │ url         │
       │ position      │      │  │ image_path  │
       └───────────────┘      │  │ created_at  │
          │(1)                 │  └─────────────┘
          │                    │
       (N)│                    │
          │                    │ (unique)
       ┌──▼──────────┐         │
       │  PRODUCT    │◄────────┘
       ├─────────────┤
       │ id (PK)     │
       │ category_id │
       │ name        │
       │ description │
       │ price       │
       │ image       │
       │ available   │
       │ position    │
       └─────────────┘
```

---

## 5. Sécurité

### 5.1 Authentication Flow

```
1. Login
   └─ Username/Password → bcrypt hash check
   └─ Generate JWT with user_id
   └─ Return token to client
   
2. Authenticated Requests
   └─ Client sends JWT in Authorization header
   └─ Backend validates JWT signature
   └─ Extract user_id from JWT
   └─ Check authorization (user owns resource)
   
3. Password Storage
   └─ Never store plaintext passwords
   └─ bcrypt with salt rounds
   └─ Cost = 12 (configurable)
```

### 5.2 Authorization

```
- Only authenticated users can access protected endpoints
- Users can only see/modify their own cafes
- Users can only see/modify products in their cafes
- Public endpoints (menu view) don't require auth
```

---

## 6. Configuration & Dépendances

### 6.1 Variables d'Environnement (.env)

```env
# Database
DATABASE_URL=mysql+pymysql://user:pass@localhost/db

# JWT
SECRET_KEY=super-secret-key
JWT_SECRET=jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Server
DEBUG=True
ENVIRONMENT=development
HOST=127.0.0.1
PORT=8000

# File Uploads
UPLOAD_DIR=uploads/
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# App
APP_NAME=QR Menu
APP_VERSION=0.1.0
```

---

## 7. Performance & Optimisation

### 7.1 Database Optimization

```
- Indexes on foreign keys
- Indexes on slug (fast lookup)
- Indexes on cafe_id
- Efficient pagination
```

### 7.2 Frontend Optimization

```
- Lazy loading images
- Caching (Service Workers - future)
- Minimal CSS/JS (no frameworks)
- Responsive images
```

### 7.3 API Optimization

```
- Caching with ETags
- Compression (gzip)
- Connection pooling
- Query optimization
```

---

## 8. Error Handling

### 8.1 Backend Errors

```python
# HTTP Status Codes
200 OK               - Request successful
201 Created          - Resource created
400 Bad Request      - Invalid input
401 Unauthorized     - No auth token
403 Forbidden        - No permission
404 Not Found        - Resource not found
409 Conflict         - Unique constraint violation
500 Server Error     - Unexpected error
```

### 8.2 Frontend Errors

```javascript
// User-friendly messages
- "Email ou mot de passe incorrect"
- "Ce produit n'existe pas"
- "Vous n'avez pas l'autorisation"
- "Une erreur est survenue, réessayez"
```

---

## 9. Testing Strategy

### 9.1 Unit Tests

```python
# Tests par couche
tests/
├── test_auth.py       - Authentication logic
├── test_cafes.py      - Cafe CRUD operations
├── test_products.py   - Product operations
└── test_services.py   - Business logic
```

### 9.2 Integration Tests

```python
# End-to-end flows
- Register → Login → Create Cafe → Add Product → View Menu
```

### 9.3 Frontend Tests

```javascript
- Form validation
- API calls
- Local storage management
```

---

## 10. Déploiement

### 10.1 Production Build

```bash
# Backend
pip install -r requirements.txt
ENVIRONMENT=production uvicorn app.main:app

# Frontend
# Static files served by backend
```

### 10.2 Environment Configuration

```
Development     → LOCAL DATABASE, DEBUG=True
Staging        → STAGING DATABASE, DEBUG=False
Production     → PRODUCTION DATABASE, DEBUG=False
```

---

## 11. Next Steps

**Phase 3:** Installation Python et environnement virtuel  
**Phase 4:** Créer FastAPI et configurer MySQL  
**Phase 5:** SQLAlchemy + Alembic migrations  

---

**Dernière mise à jour:** 2026-09-04

# ============================================
# DATABASE CONFIGURATION - QR MENU BASIC
# ============================================
# Configuration de la connexion SQLAlchemy à MySQL

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Créer l'engine SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Affiche les requêtes SQL en développement
    pool_pre_ping=True,   # Vérifie la connexion avant d'utiliser
    connect_args={
        "charset": "utf8mb4",  # Support pour caractères spéciaux (arabe, etc)
    }
)

# Créer une session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Fonction pour obtenir une session de la base de données
# Utilisée dans les dépendances FastAPI
def get_db():
    """
    Dépendance FastAPI pour obtenir une session database
    
    Usage:
        @app.get("/")
        async def get_data(db: Session = Depends(get_db)):
            # Utiliser db
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================
# CONFIGURATION SETTINGS - QR MENU BASIC
# ============================================
# Configuration centralisée de l'application
# Les valeurs sont lues depuis .env

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    """Configuration de l'application avec pydantic-settings"""
    
    # ====== App Settings ======
    APP_NAME: str = "QR Menu"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # ====== Server ======
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # ====== Database ======
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/qr_menu_db"
    
    # ====== Security & JWT ======
    SECRET_KEY: str = "your-secret-key-change-this"
    JWT_SECRET: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # ====== File Uploads ======
    UPLOAD_DIR: str = "uploads/"
    MAX_FILE_SIZE: int = 5242880  # 5MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    
    # ====== CORS ======
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # ====== URLs ======
    FRONTEND_URL: str = "http://localhost:8000"
    API_URL: str = "http://localhost:8000/api"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instance globale de settings
settings = Settings()

# Afficher la configuration en développement
if settings.DEBUG:
    print(f"[CONFIG] {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"[CONFIG] Environment: {settings.ENVIRONMENT}")
    print(f"[CONFIG] Database: {settings.DATABASE_URL}")

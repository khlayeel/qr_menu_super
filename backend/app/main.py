# ============================================
# MAIN APPLICATION - QR MENU BASIC
# ============================================
# Point d'entrée de l'application FastAPI

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

# Import des routers (à créer dans les phases suivantes)
from app.routers import auth, cafes, categories, products, qrcodes

# Configuration
from app.core.config import settings

# Créer l'application FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API pour QR Menu - Menu digital pour cafés",
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# ============ CORS Middleware ============
# Permet les requêtes cross-origin du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Servir les fichiers statiques ============
# Pour le frontend et les uploads
uploads_dir = Path(settings.UPLOAD_DIR)
uploads_dir.mkdir(exist_ok=True)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ============ Routes ============

@app.get("/", tags=["Health"])
async def root():
    """Racine de l'API - vérifier que le serveur fonctionne"""
    return {
        "message": "Bienvenue sur QR Menu API",
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

# À débloquer au fur et à mesure des phases:
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(cafes.router, prefix="/api/cafes", tags=["Cafes"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(qrcodes.router, prefix="/api/qrcodes", tags=["QR Codes"])
# app.include_router(cafes.router, prefix="/api/cafes", tags=["Cafes"])
# app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
# app.include_router(products.router, prefix="/api/products", tags=["Products"])
# app.include_router(qrcodes.router, prefix="/api/qrcodes", tags=["QR Codes"])

# ============ Middleware pour logging ============
# À implémenter dans les phases futures

# ============ Exception handlers ============
# À implémenter dans les phases futures

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

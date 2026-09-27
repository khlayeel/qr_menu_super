# ============================================
# Models package - SQLAlchemy ORM models
# ============================================
# Importer tous les modèles ici pour que Base.metadata les connaisse
# (nécessaire pour Alembic et pour Base.metadata.create_all)

from app.models.user import User
from app.models.cafe import Cafe
from app.models.category import Category
from app.models.product import Product

__all__ = ["User", "Cafe", "Category", "Product"]

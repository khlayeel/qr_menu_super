# ============================================
# ROUTER - Catégories
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.cafe import Cafe
from app.models.category import Category
from app.schemas.category import CategoryRead, CategoryCreate, CategoryUpdate
from app.routers.deps import get_current_user

router = APIRouter()


def _get_owned_cafe(current_user: User, db: Session) -> Cafe:
    """Récupère le café du propriétaire connecté, ou lève une 404."""
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")
    return cafe


def _get_owned_category(category_id: int, current_user: User, db: Session) -> Category:
    """Récupère une catégorie, en vérifiant qu'elle appartient bien au café du propriétaire connecté."""
    cafe = _get_owned_cafe(current_user, db)
    category = db.query(Category).filter(Category.id == category_id, Category.cafe_id == cafe.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie introuvable")
    return category


# ===== Lecture publique (pour menu.html) =====

@router.get("/public/{cafe_slug}", response_model=List[CategoryRead])
def list_public_categories(cafe_slug: str, db: Session = Depends(get_db)):
    """Liste les catégories d'un café, accessible sans connexion (menu client)."""
    cafe = db.query(Cafe).filter(Cafe.slug == cafe_slug).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    return db.query(Category).filter(Category.cafe_id == cafe.id).order_by(Category.position).all()


# ===== Gestion protégée (pour dashboard.html) =====

@router.get("/", response_model=List[CategoryRead])
def list_my_categories(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Liste les catégories du café du propriétaire connecté."""
    cafe = _get_owned_cafe(current_user, db)
    return db.query(Category).filter(Category.cafe_id == cafe.id).order_by(Category.position).all()


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crée une nouvelle catégorie pour le café du propriétaire connecté."""
    cafe = _get_owned_cafe(current_user, db)
    category = Category(cafe_id=cafe.id, **payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Modifie une catégorie appartenant au propriétaire connecté."""
    category = _get_owned_category(category_id, current_user, db)
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Supprime une catégorie (et ses produits, via cascade) appartenant au propriétaire connecté."""
    category = _get_owned_category(category_id, current_user, db)
    db.delete(category)
    db.commit()
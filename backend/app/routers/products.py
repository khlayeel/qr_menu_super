# ============================================
# ROUTER - Produits
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.cafe import Cafe
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductRead, ProductCreate, ProductUpdate
from app.routers.deps import get_current_user
from app.utils.files import save_upload

router = APIRouter()


def _get_owned_cafe(current_user: User, db: Session) -> Cafe:
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")
    return cafe


def _get_owned_category(category_id: int, current_user: User, db: Session) -> Category:
    cafe = _get_owned_cafe(current_user, db)
    category = db.query(Category).filter(Category.id == category_id, Category.cafe_id == cafe.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catégorie introuvable")
    return category


def _get_owned_product(product_id: int, current_user: User, db: Session) -> Product:
    """Récupère un produit, en vérifiant qu'il appartient bien à une catégorie du café du propriétaire."""
    cafe = _get_owned_cafe(current_user, db)
    product = (
        db.query(Product)
        .join(Category, Product.category_id == Category.id)
        .filter(Product.id == product_id, Category.cafe_id == cafe.id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit introuvable")
    return product


# ===== Lecture publique (pour menu.html) =====

@router.get("/public/{cafe_slug}", response_model=List[ProductRead])
def list_public_products(cafe_slug: str, db: Session = Depends(get_db)):
    """Liste tous les produits d'un café, accessible sans connexion (menu client)."""
    cafe = db.query(Cafe).filter(Cafe.slug == cafe_slug).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    return (
        db.query(Product)
        .join(Category, Product.category_id == Category.id)
        .filter(Category.cafe_id == cafe.id)
        .order_by(Product.position)
        .all()
    )


# ===== Gestion protégée (pour dashboard.html) =====

@router.get("/", response_model=List[ProductRead])
def list_my_products(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Liste tous les produits du café du propriétaire connecté."""
    cafe = _get_owned_cafe(current_user, db)
    return (
        db.query(Product)
        .join(Category, Product.category_id == Category.id)
        .filter(Category.cafe_id == cafe.id)
        .order_by(Product.position)
        .all()
    )


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crée un produit, en s'assurant que la catégorie ciblée appartient bien au propriétaire connecté."""
    _get_owned_category(payload.category_id, current_user, db)  # lève 404 si pas la bonne catégorie
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Modifie un produit appartenant au propriétaire connecté."""
    product = _get_owned_product(product_id, current_user, db)

    update_data = payload.model_dump(exclude_unset=True)
    if "category_id" in update_data:
        _get_owned_category(update_data["category_id"], current_user, db)  # empêche de déplacer vers une catégorie qui n'est pas la sienne

    for field, value in update_data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Supprime un produit appartenant au propriétaire connecté."""
    product = _get_owned_product(product_id, current_user, db)
    db.delete(product)
    db.commit()


@router.post("/{product_id}/image", response_model=ProductRead)
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload une image pour un produit et met à jour son champ 'image'."""
    product = _get_owned_product(product_id, current_user, db)
    image_url = save_upload(file, subfolder="products")
    product.image = image_url
    db.commit()
    db.refresh(product)
    return product
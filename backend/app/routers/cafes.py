# ============================================
# ROUTER - Cafés
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.cafe import Cafe
from app.schemas.cafe import CafeRead, CafeUpdate
from app.routers.deps import get_current_user
from app.utils.files import save_upload

router = APIRouter()


@router.get("/me", response_model=CafeRead)
def get_my_cafe(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")
    return cafe


@router.put("/me", response_model=CafeRead)
def update_my_cafe(
    payload: CafeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cafe, field, value)

    db.commit()
    db.refresh(cafe)
    return cafe


@router.post("/me/logo", response_model=CafeRead)
def upload_cafe_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload le logo du café connecté."""
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")

    logo_url = save_upload(file, subfolder="cafes")
    cafe.logo = logo_url
    db.commit()
    db.refresh(cafe)
    return cafe


@router.get("/{slug}", response_model=CafeRead)
def get_cafe_by_slug(slug: str, db: Session = Depends(get_db)):
    cafe = db.query(Cafe).filter(Cafe.slug == slug).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Café introuvable")
    return cafe
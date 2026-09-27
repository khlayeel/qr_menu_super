# ============================================
# ROUTER - Auth (login uniquement, pas d'inscription publique)
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.utils.security import verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Connecte le propriétaire du café et renvoie un token JWT."""
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
        )

    token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=token)
# ============================================
# ROUTER - QR Codes
# ============================================
import io
import qrcode
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.cafe import Cafe
from app.routers.deps import get_current_user
from app.core.config import settings

router = APIRouter()


@router.get("/me")
def get_my_qrcode(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Génère et renvoie le QR code (image PNG) pointant vers le menu du café connecté."""
    cafe = db.query(Cafe).filter(Cafe.owner_id == current_user.id).first()
    if not cafe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun café associé à ce compte")

    menu_url = f"{settings.FRONTEND_URL}/menu.html?cafe={cafe.slug}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={"Content-Disposition": f'attachment; filename="qrcode-{cafe.slug}.png"'},
    )
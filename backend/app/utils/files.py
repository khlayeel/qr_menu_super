# ============================================
# UTILS - Gestion des fichiers uploadés
# ============================================
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

ALLOWED_EXTENSIONS = set(settings.ALLOWED_EXTENSIONS)


def save_upload(file: UploadFile, subfolder: str = "products") -> str:
    """
    Sauvegarde un fichier uploadé sur le disque et renvoie son chemin public (ex: /uploads/products/xxx.jpg).
    Valide l'extension et la taille avant d'écrire quoi que ce soit.
    """
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Extension non autorisée. Autorisées: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    contents = file.file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fichier trop volumineux (max {settings.MAX_FILE_SIZE // 1024 // 1024} Mo)",
        )

    target_dir = Path(settings.UPLOAD_DIR) / subfolder
    target_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}.{extension}"
    target_path = target_dir / unique_name

    with open(target_path, "wb") as f:
        f.write(contents)

    return f"/uploads/{subfolder}/{unique_name}"
# ============================================
# SCHEMA - Texte multilingue partagé
# ============================================
from pydantic import BaseModel
from typing import Optional


class LocalizedText(BaseModel):
    fr: str
    en: Optional[str] = None
    ar: Optional[str] = None
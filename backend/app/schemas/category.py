# ============================================
# SCHEMA - Category
# ============================================
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.common import LocalizedText


class CategoryBase(BaseModel):
    name: LocalizedText
    icon: Optional[str] = None
    position: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[LocalizedText] = None
    icon: Optional[str] = None
    position: Optional[int] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cafe_id: int
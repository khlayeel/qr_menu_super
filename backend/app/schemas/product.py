# ============================================
# SCHEMA - Product
# ============================================
from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from app.schemas.common import LocalizedText


class ProductBase(BaseModel):
    name: LocalizedText
    description: Optional[LocalizedText] = None
    price: Decimal
    image: Optional[str] = None
    available: bool = True
    position: int = 0


class ProductCreate(ProductBase):
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[LocalizedText] = None
    description: Optional[LocalizedText] = None
    price: Optional[Decimal] = None
    image: Optional[str] = None
    available: Optional[bool] = None
    position: Optional[int] = None
    category_id: Optional[int] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    category_id: int
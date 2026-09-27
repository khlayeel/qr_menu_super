# ============================================
# SCHEMA - Cafe
# ============================================
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CafeBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None


class CafeCreate(CafeBase):
    pass


class CafeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None


class CafeRead(CafeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    owner_id: int
    created_at: datetime
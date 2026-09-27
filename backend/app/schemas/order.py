# ============================================
# SCHEMA - Order
# ============================================
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Literal
from decimal import Decimal
from datetime import datetime
from app.schemas.common import LocalizedText


OrderStatus = Literal["pending", "accepted", "in_preparation", "ready", "completed", "cancelled"]


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    table_number: str = Field(min_length=1, max_length=20)
    comment: Optional[str] = None
    items: List[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_id: Optional[int] = None
    product_name_snapshot: Optional[LocalizedText] = None
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    public_id: str
    cafe_id: int
    table_number: str
    status: OrderStatus
    comment: Optional[str] = None
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemRead] = []


class OrderTrackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    public_id: str
    table_number: str
    status: OrderStatus
    comment: Optional[str] = None
    total_price: Decimal
    created_at: datetime
    items: List[OrderItemRead] = []


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
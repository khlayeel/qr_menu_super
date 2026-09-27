# ============================================
# MODEL - Order
# ============================================
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.types import JSONText


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    table_number = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    comment = Column(Text, nullable=True)
    total_price = Column(Numeric(10, 3), nullable=False, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cafe = relationship("Cafe", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"), nullable=True)

    product_name_snapshot = Column(JSONText, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 3), nullable=False)
    subtotal = Column(Numeric(10, 3), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", backref="order_items")
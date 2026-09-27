# ============================================
# MODEL - Product
# ============================================
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.types import JSONText


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(JSONText, nullable=False)
    description = Column(JSONText, nullable=True)
    price = Column(Numeric(10, 3), nullable=False)
    image = Column(String(255), nullable=True)
    available = Column(Boolean, default=True)
    position = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
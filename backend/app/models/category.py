# ============================================
# MODEL - Category
# ============================================
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.types import JSONText


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), nullable=False)

    name = Column(JSONText, nullable=False)
    icon = Column(String(255), nullable=True)
    position = Column(Integer, default=0)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    cafe = relationship("Cafe", back_populates="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
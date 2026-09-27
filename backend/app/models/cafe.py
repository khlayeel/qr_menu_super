# ============================================
# MODEL - Cafe
# ============================================
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    name = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    logo = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    phone = Column(String(30), nullable=True)
    opening_hours = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="cafe")
    categories = relationship("Category", back_populates="cafe", cascade="all, delete-orphan")
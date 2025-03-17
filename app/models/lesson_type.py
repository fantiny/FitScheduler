from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class LessonType(Base):
    __tablename__ = "lesson_types"
    __table_args__ = {'extend_existing': True}

    lesson_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    bookings = relationship("Booking", back_populates="lesson_type", cascade="all, delete-orphan")
    coach_lessons = relationship("CoachLesson", back_populates="lesson_type", cascade="all, delete-orphan") 
from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, Date, Time, DECIMAL, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'extend_existing': True}

    booking_id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, comment="学员用户ID")
    coach_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, comment="教练用户ID")
    venue_id = Column(Integer, ForeignKey("venues.venue_id"), nullable=False)
    lesson_type_id = Column(Integer, ForeignKey("lesson_types.lesson_type_id"), nullable=False)
    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    lesson_price = Column(DECIMAL(10, 2), nullable=False)
    facility_fee = Column(DECIMAL(10, 2), default=0)
    service_fee = Column(DECIMAL(10, 2), default=0)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.payment_method_id"))
    status = Column(String(20), nullable=False, default="PENDING")
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="bookings")
    coach = relationship("User", foreign_keys=[coach_id], back_populates="coach_bookings")
    venue = relationship("Venue", back_populates="bookings")
    lesson_type = relationship("LessonType", back_populates="bookings")
    payment_method = relationship("PaymentMethod", back_populates="bookings")
    rating = relationship("Rating", back_populates="booking", uselist=False)

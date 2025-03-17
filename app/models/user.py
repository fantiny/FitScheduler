from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    profile_image = Column(String(255))
    role = Column(String(20), nullable=False, default="USER")  # USER, COACH, ADMIN
    
    # 用户特有字段
    membership_rank = Column(String(20), default="STANDARD")
    booking_count = Column(Integer, default=0)
    
    # 教练特有字段
    bio = Column(Text)
    specialization = Column(String(100))
    hourly_rate = Column(DECIMAL(10, 2))
    rating = Column(DECIMAL(3, 2), default=0)
    review_count = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 用户关系
    payment_methods = relationship("PaymentMethod", back_populates="user", cascade="all, delete-orphan")
    bookings = relationship("Booking", foreign_keys="Booking.user_id", back_populates="user", cascade="all, delete-orphan")
    ratings_given = relationship("Rating", foreign_keys="Rating.user_id", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", foreign_keys="Favorite.user_id", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    # 教练关系
    coach_venues = relationship("CoachVenue", back_populates="coach", cascade="all, delete-orphan")
    coach_bookings = relationship("Booking", foreign_keys="Booking.coach_id", back_populates="coach", cascade="all, delete-orphan")
    coach_ratings = relationship("Rating", foreign_keys="Rating.coach_id", back_populates="coach", cascade="all, delete-orphan")
    coach_lessons = relationship("CoachLesson", back_populates="coach", cascade="all, delete-orphan")
    coach_availability = relationship("CoachAvailability", back_populates="coach", cascade="all, delete-orphan")
    coach_favorites = relationship("Favorite", foreign_keys="Favorite.coach_id", back_populates="coach", cascade="all, delete-orphan")

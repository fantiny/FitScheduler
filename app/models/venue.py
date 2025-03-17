from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    access_info = Column(String(255))
    description = Column(Text)
    thumbnail_url = Column(String(255))
    rating = Column(DECIMAL(3, 2), default=0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    bookings = relationship("Booking", back_populates="venue", cascade="all, delete-orphan")
    tags = relationship("VenueTag", backref="venue", cascade="all, delete-orphan")
    images = relationship("VenueImage", backref="venue", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="venue", cascade="all, delete-orphan")
    coaches = relationship("CoachVenue", back_populates="venue", cascade="all, delete-orphan")
    coach_availability = relationship("CoachAvailability", back_populates="venue", cascade="all, delete-orphan")

class VenueTag(Base):
    __tablename__ = "venue_tags"

    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    tag_name = Column(String(50), nullable=False)

class VenueImage(Base):
    __tablename__ = "venue_images"

    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False)

class CoachVenue(Base):
    __tablename__ = "coach_venues"
    __table_args__ = {'extend_existing': True}

    coach_venue_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="教练用户ID")
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    coach = relationship("User", back_populates="coach_venues")
    venue = relationship("Venue", back_populates="coaches")

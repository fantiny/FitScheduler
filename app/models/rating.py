from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = {'extend_existing': True}

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="学员用户ID")
    coach_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="教练用户ID")
    score = Column(DECIMAL(3, 2), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    booking = relationship("Booking", back_populates="rating")
    user = relationship("User", foreign_keys=[user_id], back_populates="ratings_given")
    coach = relationship("User", foreign_keys=[coach_id], back_populates="coach_ratings") 
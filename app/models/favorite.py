from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = {'extend_existing': True}

    favorite_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    coach_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="favorites")
    coach = relationship("User", foreign_keys=[coach_id], back_populates="coach_favorites")
    venue = relationship("Venue", back_populates="favorites") 
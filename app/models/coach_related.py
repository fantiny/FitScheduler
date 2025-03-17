from sqlalchemy import Column, Integer, String, DateTime, Time, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class CoachLesson(Base):
    __tablename__ = "coach_lessons"
    __table_args__ = {'extend_existing': True}

    coach_lesson_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="教练用户ID")
    lesson_type_id = Column(Integer, ForeignKey("lesson_types.lesson_type_id", ondelete="CASCADE"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    # Relationships
    coach = relationship("User", back_populates="coach_lessons")
    lesson_type = relationship("LessonType", back_populates="coach_lessons")

class CoachAvailability(Base):
    __tablename__ = "coach_availability"
    __table_args__ = {'extend_existing': True}

    availability_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, comment="教练用户ID")
    venue_id = Column(Integer, ForeignKey("venues.venue_id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 1=Monday, 7=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationships
    coach = relationship("User", back_populates="coach_availability")
    venue = relationship("Venue", back_populates="coach_availability") 
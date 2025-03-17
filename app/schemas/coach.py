from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime, time
from decimal import Decimal

# Coach venue schemas
class CoachVenueBase(BaseModel):
    user_id: int
    venue_id: int

class CoachVenueCreate(CoachVenueBase):
    pass

class CoachVenue(CoachVenueBase):
    coach_venue_id: int

    class Config:
        orm_mode = True

# Lesson type schemas
class LessonTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_minutes: int
    base_price: Decimal

class LessonTypeCreate(LessonTypeBase):
    pass

class LessonType(LessonTypeBase):
    lesson_type_id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Coach lesson schemas
class CoachLessonBase(BaseModel):
    user_id: int
    lesson_type_id: int
    price: Decimal

class CoachLessonCreate(CoachLessonBase):
    pass

class CoachLesson(CoachLessonBase):
    coach_lesson_id: int

    class Config:
        orm_mode = True

# Coach availability schemas
class CoachAvailabilityBase(BaseModel):
    user_id: int
    venue_id: int
    day_of_week: int
    start_time: time
    end_time: time

class CoachAvailabilityCreate(CoachAvailabilityBase):
    pass

class CoachAvailability(CoachAvailabilityBase):
    availability_id: int

    class Config:
        orm_mode = True

# Coach schemas
class CoachBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None
    hourly_rate: Optional[Decimal] = None
    is_active: bool = True
    profile_image: Optional[str] = None

class CoachCreate(CoachBase):
    password: str

class CoachUpdate(CoachBase):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class Coach(CoachBase):
    user_id: int
    rating: Optional[Decimal] = None
    review_count: int = 0
    created_at: datetime
    updated_at: datetime
    role: str = "COACH"

    class Config:
        from_attributes = True
        
    # 以下关系字段通常由ORM查询填充
    coach_venues: List[CoachVenue] = []
    coach_lessons: List[CoachLesson] = []
    coach_availability: List[CoachAvailability] = []

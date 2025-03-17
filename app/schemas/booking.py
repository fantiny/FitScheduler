from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime, date, time
from decimal import Decimal

# Booking schemas
class BookingBase(BaseModel):
    coach_id: int
    venue_id: int
    lesson_type_id: int
    booking_date: date
    start_time: time
    end_time: time
    lesson_price: Decimal
    facility_fee: Decimal = Field(default=0)
    service_fee: Decimal = Field(default=0)
    total_price: Decimal
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    payment_method_id: Optional[int] = None

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    booking_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    payment_method_id: Optional[int] = None
    notes: Optional[str] = None

class Booking(BookingBase):
    booking_id: int
    booking_reference: str
    status: str
    payment_method_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Rating schemas
class RatingBase(BaseModel):
    booking_id: int
    user_id: int
    coach_id: int
    score: Decimal
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    rating_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Favorite schemas
class FavoriteBase(BaseModel):
    user_id: int
    coach_id: Optional[int] = None
    venue_id: Optional[int] = None

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    favorite_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Notification schemas
class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None

class Notification(NotificationBase):
    notification_id: int
    created_at: datetime

    class Config:
        from_attributes = True

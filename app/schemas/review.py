from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

class ReviewBase(BaseModel):
    booking_id: int
    user_id: int
    coach_id: int
    score: Decimal = Field(ge=0, le=5, decimal_places=2)
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    """
    Schema for creating a new review
    """
    pass

class ReviewUpdate(BaseModel):
    score: Optional[Decimal] = Field(None, ge=0, le=5, decimal_places=2)
    comment: Optional[str] = None

class Review(ReviewBase):
    rating_id: int
    created_at: datetime

    class Config:
        from_attributes = True 
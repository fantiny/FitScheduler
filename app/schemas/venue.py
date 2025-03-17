from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Venue tag schemas
class VenueTagBase(BaseModel):
    tag_name: str

class VenueTagCreate(VenueTagBase):
    venue_id: int

class VenueTag(VenueTagBase):
    tag_id: int
    venue_id: int

    class Config:
        orm_mode = True

# Venue image schemas
class VenueImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class VenueImageCreate(VenueImageBase):
    venue_id: int

class VenueImage(VenueImageBase):
    image_id: int
    venue_id: int

    class Config:
        orm_mode = True

# Venue schemas
class VenueBase(BaseModel):
    venue_name: str
    address: str
    access_info: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    venue_name: Optional[str] = None
    address: Optional[str] = None
    access_info: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

class VenueInDBBase(VenueBase):
    venue_id: int
    rating: Decimal
    rating_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Venue(VenueInDBBase):
    tags: List[VenueTag] = []
    images: List[VenueImage] = []

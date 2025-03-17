from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    phone: Optional[str] = None
    is_active: Optional[bool] = True
    membership_rank: Optional[str] = "STANDARD"

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    user_id: int
    profile_image: Optional[str] = None
    booking_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Payment method schemas
class PaymentMethodBase(BaseModel):
    payment_type: str
    payment_details: str
    is_default: bool = False

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(BaseModel):
    payment_type: Optional[str] = None
    payment_details: Optional[str] = None
    is_default: Optional[bool] = None

class PaymentMethodInDBBase(PaymentMethodBase):
    payment_method_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PaymentMethod(PaymentMethodInDBBase):
    pass

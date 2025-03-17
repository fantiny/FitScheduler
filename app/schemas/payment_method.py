from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class PaymentMethodBase(BaseModel):
    card_number: str  # Last 4 digits only
    card_type: str
    expiry_month: int
    expiry_year: int
    is_default: bool = False

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodUpdate(PaymentMethodBase):
    card_number: Optional[str] = None
    card_type: Optional[str] = None
    expiry_month: Optional[int] = None
    expiry_year: Optional[int] = None
    is_default: Optional[bool] = None

class PaymentMethod(PaymentMethodBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 
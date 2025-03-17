from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class PaymentTypeEnum(enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    ONLINE_PAYMENT = "ONLINE_PAYMENT"

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    payment_method_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False)
    
    # 信用卡特有字段
    card_number = Column(String(16))  # Last 4 digits only
    card_type = Column(String(50))  # visa, mastercard, etc.
    expiry_month = Column(Integer)
    expiry_year = Column(Integer)
    
    # 通用字段
    payment_details = Column(String(255))
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payment_methods")
    bookings = relationship("Booking", back_populates="payment_method") 
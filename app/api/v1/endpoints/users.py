from datetime import datetime
from typing import Any, List
import logging

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import dependencies
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.models.payment_method import PaymentMethod
from app.schemas.user import User as UserSchema, UserUpdate
from app.schemas.payment_method import PaymentMethod as PaymentMethodSchema, PaymentMethodCreate, PaymentMethodUpdate

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Get current user
    """
    return current_user

@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Update own user
    """
    try:
        logger.info(f"Updating user profile for user_id: {current_user.user_id}")
        update_data = user_in.dict(exclude_unset=True)
        
        # 如果提供了新密码，对其进行哈希处理
        if "password" in update_data and update_data["password"]:
            logger.info("Processing password update")
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            if hasattr(current_user, field):
                logger.debug(f"Updating field: {field}")
                setattr(current_user, field, value)
        
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        logger.info("User profile updated successfully")
        return current_user
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user profile: {str(e)}"
        )

# Payment methods
@router.get("/me/payment-methods", response_model=List[PaymentMethodSchema])
def read_user_payment_methods(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Get current user's payment methods
    """
    payment_methods = db.query(PaymentMethod).filter(
        PaymentMethod.user_id == current_user.user_id
    ).all()
    return payment_methods

@router.post("/me/payment-methods", response_model=PaymentMethodSchema)
def create_user_payment_method(
    *,
    db: Session = Depends(get_db),
    payment_in: PaymentMethodCreate,
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Create new payment method for current user
    """
    # If this is the first payment method or setting as default
    if payment_in.is_default:
        # Set all existing payment methods to non-default
        db.query(PaymentMethod).filter(
            PaymentMethod.user_id == current_user.user_id,
            PaymentMethod.is_default == True
        ).update({"is_default": False})
    
    payment_method = PaymentMethod(
        user_id=current_user.user_id,
        **payment_in.dict()
    )
    db.add(payment_method)
    db.commit()
    db.refresh(payment_method)
    return payment_method

@router.put("/me/payment-methods/{payment_method_id}", response_model=PaymentMethodSchema)
def update_user_payment_method(
    *,
    db: Session = Depends(get_db),
    payment_method_id: int,
    payment_in: PaymentMethodUpdate,
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Update payment method
    """
    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.payment_method_id == payment_method_id,
        PaymentMethod.user_id == current_user.user_id
    ).first()
    
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found",
        )
    
    # If setting this payment method as default
    if payment_in.is_default:
        # Set all existing payment methods to non-default
        db.query(PaymentMethod).filter(
            PaymentMethod.user_id == current_user.user_id,
            PaymentMethod.is_default == True
        ).update({"is_default": False})
    
    for field, value in payment_in.dict(exclude_unset=True).items():
        setattr(payment_method, field, value)
    
    db.add(payment_method)
    db.commit()
    db.refresh(payment_method)
    return payment_method

@router.delete("/me/payment-methods/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_payment_method(
    *,
    db: Session = Depends(get_db),
    payment_method_id: int,
    current_user: User = Depends(dependencies.get_current_user),
) -> None:
    """
    Delete a payment method belonging to the current user
    """
    payment_method = db.query(PaymentMethod).filter(
        PaymentMethod.id == payment_method_id,
        PaymentMethod.user_id == current_user.user_id
    ).first()
    if not payment_method:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment method not found"
        )
    db.delete(payment_method)
    db.commit()
    return None

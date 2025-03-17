from datetime import timedelta
from typing import Any
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import dependencies
from app.core.security import create_access_token, verify_password, get_password_hash
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.user_id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserSchema)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Register new user
    """
    try:
        logger.debug(f"Attempting to register user with email: {user_in.email}")
        
        user = db.query(User).filter(User.email == user_in.email).first()
        if user:
            logger.debug(f"User with email {user_in.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists in the system",
            )
        
        logger.debug("Hashing password")
        hashed_password = get_password_hash(user_in.password)
        
        logger.debug("Creating user object")
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            phone=user_in.phone,
            password_hash=hashed_password,
            is_active=user_in.is_active,
            membership_rank=user_in.membership_rank
        )
        
        logger.debug("Adding user to database")
        db.add(db_user)
        
        logger.debug("Committing transaction")
        db.commit()
        
        logger.debug("Refreshing user object")
        db.refresh(db_user)
        
        logger.debug("Registration successful")
        return db_user
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )

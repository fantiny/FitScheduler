from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import dependencies
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    db: Session = Depends(dependencies.get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the current authenticated user from the token with enhanced validation.
    
    Args:
        db: Database session
        token: JWT token from request
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If authentication fails for any reason
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token format",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Extract user ID from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise invalid_token_exception
            
        # Check token expiration manually (in addition to JWT's built-in check)
        exp = payload.get("exp")
        if exp is None:
            raise invalid_token_exception
            
        # Verify the token hasn't expired
        if datetime.utcnow().timestamp() > exp:
            raise expired_exception
            
    except ExpiredSignatureError:
        # Specific error for expired tokens
        raise expired_exception
    except JWTError:
        # General JWT validation error
        raise credentials_exception
    
    # Get the user from the database
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user account",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user 
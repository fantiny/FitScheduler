from typing import List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api import dependencies
from app.schemas.booking import BookingCreate, BookingUpdate, Booking
from app.services.booking import BookingService
from app.models.user import User
from app.utils.validation import validate_booking_time, validate_booking_fields, validate_booking_price

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=Booking)
def create_booking(
    *,
    db: Session = Depends(dependencies.get_db),
    booking_in: BookingCreate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Create new booking.
    
    The user_id is automatically extracted from the authentication token,
    so clients don't need to include it in the request body.
    """
    try:
        logger.info(f"Creating new booking for user_id: {current_user.user_id}")
        
        # Validate booking data
        validate_booking_time(
            booking_date=booking_in.booking_date,
            start_time=booking_in.start_time,
            end_time=booking_in.end_time
        )
        
        validate_booking_fields(
            venue_id=booking_in.venue_id,
            coach_id=booking_in.coach_id,
            lesson_type_id=booking_in.lesson_type_id
        )
        
        validate_booking_price(
            lesson_price=float(booking_in.lesson_price),
            facility_fee=float(booking_in.facility_fee),
            service_fee=float(booking_in.service_fee),
            total_price=float(booking_in.total_price)
        )
        
        # Create booking
        booking = BookingService(db).create_booking(obj_in=booking_in, user_id=current_user.user_id)
        logger.info(f"Booking created successfully: {booking.booking_id}")
        return booking
    except ValueError as e:
        logger.error(f"Validation error creating booking: {str(e)}")
        detail = str(e)
        if "conflict" in detail.lower():
            # Return 409 Conflict for scheduling conflicts
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail
            )
        else:
            # Return 400 Bad Request for validation errors
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating booking: {str(e)}"
        )

@router.get("/", response_model=List[Booking])
def get_bookings(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    venue_id: Optional[int] = None,
    coach_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Retrieve bookings.
    """
    bookings = BookingService(db).get_bookings(
        user_id=current_user.user_id,
        skip=skip,
        limit=limit,
        venue_id=venue_id,
        coach_id=coach_id,
        status=status
    )
    return bookings

@router.get("/{booking_id}", response_model=Booking)
def get_booking(
    *,
    db: Session = Depends(dependencies.get_db),
    booking_id: int,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Get booking by ID.
    """
    booking = BookingService(db).get_booking(id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return booking

@router.put("/{booking_id}", response_model=Booking)
def update_booking(
    *,
    db: Session = Depends(dependencies.get_db),
    booking_id: int,
    booking_in: BookingUpdate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Update booking.
    """
    booking = BookingService(db).get_booking(id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    booking = BookingService(db).update_booking(
        db_obj=booking,
        obj_in=booking_in
    )
    return booking

@router.delete("/{booking_id}", status_code=204)
def cancel_booking(
    *,
    db: Session = Depends(dependencies.get_db),
    booking_id: int,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Cancel booking.
    """
    booking = BookingService(db).get_booking(id=booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    BookingService(db).cancel_booking(id=booking_id)
    return None 
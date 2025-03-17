from datetime import datetime, date, time, timedelta
from fastapi import HTTPException, status

def validate_booking_time(booking_date: date, start_time: time, end_time: time) -> None:
    """
    Validate booking time constraints.
    
    Args:
        booking_date: Date of booking
        start_time: Start time
        end_time: End time
        
    Raises:
        HTTPException: If validation fails
    """
    today = datetime.now().date()
    
    # Check if booking date is in the past
    if booking_date < today:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book for a date in the past"
        )
    
    # Check if booking date is too far in the future (e.g., more than 3 months)
    max_future_date = today + timedelta(days=90)
    if booking_date > max_future_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking date too far in the future (maximum 90 days ahead)"
        )
    
    # Check if start time is before end time
    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # Check for minimum booking duration (e.g., 30 minutes)
    start_datetime = datetime.combine(booking_date, start_time)
    end_datetime = datetime.combine(booking_date, end_time)
    duration = end_datetime - start_datetime
    
    if duration < timedelta(minutes=30):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking duration must be at least 30 minutes"
        )
    
    # Check for maximum booking duration (e.g., 3 hours)
    if duration > timedelta(hours=3):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking duration cannot exceed 3 hours"
        )
    
def validate_booking_fields(venue_id: int, coach_id: int, lesson_type_id: int) -> None:
    """
    Validate booking foreign key fields.
    
    Args:
        venue_id: Venue ID
        coach_id: Coach ID
        lesson_type_id: Lesson type ID
        
    Raises:
        HTTPException: If validation fails
    """
    if venue_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid venue ID"
        )
        
    if coach_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid coach ID"
        )
        
    if lesson_type_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid lesson type ID"
        )
        
def validate_booking_price(lesson_price: float, facility_fee: float, 
                          service_fee: float, total_price: float) -> None:
    """
    Validate booking price calculations.
    
    Args:
        lesson_price: Lesson price
        facility_fee: Facility fee
        service_fee: Service fee
        total_price: Total price
        
    Raises:
        HTTPException: If validation fails
    """
    if lesson_price < 0 or facility_fee < 0 or service_fee < 0 or total_price < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prices cannot be negative"
        )
    
    # Check if total price equals sum of individual prices
    calculated_total = lesson_price + facility_fee + service_fee
    
    # Allow for small floating point differences
    if abs(calculated_total - total_price) > 0.01:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Total price ({total_price}) does not match calculated total ({calculated_total})"
        ) 
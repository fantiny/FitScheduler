from typing import List, Optional, Union, Dict, Any
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from sqlalchemy import or_
import uuid

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate

class BookingService:
    def __init__(self, db: Session):
        self.db = db

    def get_booking(self, id: int) -> Optional[Booking]:
        return self.db.query(Booking).filter(Booking.booking_id == id).first()

    def get_bookings(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        venue_id: Optional[int] = None,
        coach_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Booking]:
        query = self.db.query(Booking).filter(Booking.user_id == user_id)
        
        if venue_id:
            query = query.filter(Booking.venue_id == venue_id)
        
        if coach_id:
            query = query.filter(Booking.coach_id == coach_id)
        
        if status:
            query = query.filter(Booking.status == status)
        
        return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()

    def create_booking(self, obj_in: BookingCreate, user_id: int) -> Booking:
        """
        Create a new booking with enhanced error handling.
        
        Args:
            obj_in: Booking data from request
            user_id: User ID extracted from authentication token
            
        Returns:
            Created booking object
            
        Raises:
            ValueError: If booking data is invalid
            HTTPException: If there's a conflict or other booking issue
        """
        try:
            # Generate a unique booking reference
            booking_reference = f"BK{datetime.utcnow().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
            
            # 创建预订对象数据
            booking_data = obj_in.dict(exclude_unset=True)
            
            # 添加从认证令牌中获取的用户ID和其他系统生成字段
            booking_data["user_id"] = user_id
            booking_data["booking_reference"] = booking_reference
            booking_data["status"] = "PENDING"
            
            # Check for time conflicts
            self._check_booking_conflicts(
                venue_id=booking_data["venue_id"],
                coach_id=booking_data["coach_id"],
                booking_date=booking_data["booking_date"],
                start_time=booking_data["start_time"],
                end_time=booking_data["end_time"]
            )
            
            # 创建数据库对象
            db_obj = Booking(**booking_data)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
            
        except ValueError as e:
            self.db.rollback()
            raise ValueError(f"Invalid booking data: {str(e)}")
        except Exception as e:
            self.db.rollback()
            if "conflict" in str(e).lower():
                raise ValueError(f"Booking conflict: {str(e)}")
            raise Exception(f"Error creating booking: {str(e)}")

    def _check_booking_conflicts(
        self, 
        venue_id: int, 
        coach_id: int, 
        booking_date: date, 
        start_time: time, 
        end_time: time
    ) -> None:
        """
        Check for booking conflicts (coach or venue already booked for this time).
        
        Args:
            venue_id: Venue ID
            coach_id: Coach ID
            booking_date: Date of booking
            start_time: Start time
            end_time: End time
            
        Raises:
            ValueError: If there's a booking conflict
        """
        # Convert times to strings for comparison
        start_time_str = start_time.strftime("%H:%M:%S") if isinstance(start_time, time) else start_time
        end_time_str = end_time.strftime("%H:%M:%S") if isinstance(end_time, time) else end_time
        
        # Check for coach conflicts
        coach_bookings = self.db.query(Booking).filter(
            Booking.coach_id == coach_id,
            Booking.booking_date == booking_date,
            Booking.status.in_(["PENDING", "CONFIRMED"]),
        ).all()
        
        for booking in coach_bookings:
            booking_start = booking.start_time.strftime("%H:%M:%S")
            booking_end = booking.end_time.strftime("%H:%M:%S")
            
            # Check if there's any overlap
            if (start_time_str < booking_end and end_time_str > booking_start):
                raise ValueError(f"Coach is already booked from {booking_start} to {booking_end}")
                
        # Check for venue conflicts
        venue_bookings = self.db.query(Booking).filter(
            Booking.venue_id == venue_id,
            Booking.booking_date == booking_date,
            Booking.status.in_(["PENDING", "CONFIRMED"]),
        ).all()
        
        for booking in venue_bookings:
            booking_start = booking.start_time.strftime("%H:%M:%S")
            booking_end = booking.end_time.strftime("%H:%M:%S")
            
            # Check if there's any overlap
            if (start_time_str < booking_end and end_time_str > booking_start):
                raise ValueError(f"Venue is already booked from {booking_start} to {booking_end}")

    def update_booking(
        self,
        db_obj: Booking,
        obj_in: Union[BookingUpdate, Dict[str, Any]]
    ) -> Booking:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def cancel_booking(self, id: int) -> None:
        booking = self.get_booking(id)
        if booking:
            booking.status = "CANCELLED"
            self.db.add(booking)
            self.db.commit() 
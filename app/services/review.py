from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.rating import Rating
from app.schemas.review import ReviewCreate, ReviewUpdate

class ReviewService:
    def __init__(self, db: Session):
        self.db = db

    def get_review(self, id: int) -> Optional[Rating]:
        return self.db.query(Rating).filter(Rating.rating_id == id).first()

    def get_reviews(
        self,
        skip: int = 0,
        limit: int = 100,
        venue_id: Optional[int] = None,
        coach_id: Optional[int] = None,
        rating: Optional[int] = None
    ) -> List[Rating]:
        query = self.db.query(Rating)
        
        if venue_id:
            query = query.join(Rating.booking).filter(Rating.booking.has(venue_id=venue_id))
        
        if coach_id:
            query = query.filter(Rating.coach_id == coach_id)
        
        if rating:
            query = query.filter(Rating.score == rating)
        
        return query.order_by(Rating.created_at.desc()).offset(skip).limit(limit).all()

    def create_review(self, obj_in: ReviewCreate, user_id: int) -> Rating:
        db_obj = Rating(
            booking_id=obj_in.booking_id,
            user_id=user_id,
            coach_id=obj_in.coach_id,
            score=obj_in.score,
            comment=obj_in.comment
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update_review(
        self,
        db_obj: Rating,
        obj_in: Union[ReviewUpdate, Dict[str, Any]]
    ) -> Rating:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete_review(self, id: int) -> None:
        review = self.get_review(id)
        if review:
            self.db.delete(review)
            self.db.commit() 
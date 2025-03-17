from typing import List, Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.coach import CoachCreate, CoachUpdate

class CoachService:
    def __init__(self, db: Session):
        self.db = db

    def get_coach(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.user_id == id, User.role == "COACH").first()

    def get_coach_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email, User.role == "COACH").first()

    def get_coaches(
        self,
        skip: int = 0,
        limit: int = 100,
        venue_id: Optional[int] = None,
        sport_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[User]:
        query = self.db.query(User).filter(User.role == "COACH")
        
        if venue_id:
            query = query.join(User.coach_venues).filter(User.coach_venues.any(venue_id=venue_id))
        
        if sport_type:
            query = query.filter(User.specialization == sport_type)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_filter),
                    User.bio.ilike(search_filter),
                    User.specialization.ilike(search_filter)
                )
            )
        
        return query.offset(skip).limit(limit).all()

    def create_coach(self, obj_in: CoachCreate) -> User:
        db_obj = User(
            username=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            password_hash=get_password_hash(obj_in.password),
            role="COACH",
            bio=obj_in.bio,
            specialization=obj_in.specialization,
            hourly_rate=obj_in.hourly_rate,
            is_active=obj_in.is_active,
            profile_image=obj_in.profile_image if hasattr(obj_in, "profile_image") else None
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update_coach(
        self,
        db_obj: User,
        obj_in: Union[CoachUpdate, Dict[str, Any]]
    ) -> User:
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
            
        # 处理name到username的映射
        if "name" in update_data:
            update_data["username"] = update_data.pop("name")
        
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete_coach(self, id: int) -> None:
        coach = self.get_coach(id)
        if coach:
            self.db.delete(coach)
            self.db.commit() 
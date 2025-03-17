from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.lesson_type import LessonType
from app.schemas.coach import LessonTypeCreate

class LessonTypeService:
    def get_lesson_types(self, db: Session) -> List[LessonType]:
        """Get all lesson types"""
        return db.query(LessonType).filter(LessonType.is_active == True).all()
    
    def get_lesson_type_by_id(self, db: Session, lesson_type_id: int) -> Optional[LessonType]:
        """Get a specific lesson type by ID"""
        return db.query(LessonType).filter(
            LessonType.lesson_type_id == lesson_type_id,
            LessonType.is_active == True
        ).first()
    
    def create_lesson_type(self, db: Session, lesson_type: LessonTypeCreate) -> LessonType:
        """Create a new lesson type"""
        lesson_type_data = lesson_type.dict()
        
        db_lesson_type = LessonType(
            name=lesson_type_data.get('type_name'),
            description=lesson_type_data.get('description'),
            base_price=lesson_type_data.get('base_price'),
            duration_minutes=lesson_type_data.get('duration_minutes'),
            is_active=True
        )
        
        db.add(db_lesson_type)
        db.commit()
        db.refresh(db_lesson_type)
        
        return db_lesson_type 
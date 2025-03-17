import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.coach import LessonType, LessonTypeCreate
from app.services.lesson_type import LessonTypeService
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[LessonType])
def get_lesson_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all lesson types"""
    try:
        logger.info(f"User {current_user.user_id} retrieving all lesson types")
        lesson_type_service = LessonTypeService()
        lesson_types = lesson_type_service.get_lesson_types(db)
        return lesson_types
    except Exception as e:
        logger.error(f"Error retrieving lesson types: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve lesson types"
        )

@router.get("/{lesson_type_id}", response_model=LessonType)
def get_lesson_type(
    lesson_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific lesson type by ID"""
    try:
        logger.info(f"User {current_user.user_id} retrieving lesson type {lesson_type_id}")
        lesson_type_service = LessonTypeService()
        lesson_type = lesson_type_service.get_lesson_type_by_id(db, lesson_type_id)
        
        if not lesson_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lesson type with ID {lesson_type_id} not found"
            )
        
        return lesson_type
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving lesson type {lesson_type_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not retrieve lesson type {lesson_type_id}"
        )

@router.post("/", response_model=LessonType, status_code=status.HTTP_201_CREATED)
def create_lesson_type(
    lesson_type: LessonTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new lesson type"""
    try:
        logger.info(f"User {current_user.user_id} creating new lesson type")
        lesson_type_service = LessonTypeService()
        created_lesson_type = lesson_type_service.create_lesson_type(db, lesson_type)
        return created_lesson_type
    except Exception as e:
        logger.error(f"Error creating lesson type: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create lesson type"
        ) 
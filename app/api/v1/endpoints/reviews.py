from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import dependencies
from app.db.session import get_db
from app.schemas.review import ReviewCreate, ReviewUpdate, Review
from app.services.review import ReviewService
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Review)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Create new review.
    """
    review = ReviewService(db).create_review(obj_in=review_in, user_id=current_user.user_id)
    return review

@router.get("/", response_model=List[Review])
def get_reviews(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    venue_id: Optional[int] = None,
    coach_id: Optional[int] = None,
    rating: Optional[int] = None
):
    """
    Retrieve reviews.
    """
    reviews = ReviewService(db).get_reviews(
        skip=skip,
        limit=limit,
        venue_id=venue_id,
        coach_id=coach_id,
        rating=rating
    )
    return reviews

@router.get("/{review_id}", response_model=Review)
def get_review(
    *,
    db: Session = Depends(get_db),
    review_id: int
):
    """
    Get review by ID.
    """
    review = ReviewService(db).get_review(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=Review)
def update_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    review_in: ReviewUpdate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Update review.
    """
    review = ReviewService(db).get_review(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    review = ReviewService(db).update_review(
        db_obj=review,
        obj_in=review_in
    )
    return review

@router.delete("/{review_id}", status_code=204)
def delete_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Delete review.
    """
    review = ReviewService(db).get_review(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    ReviewService(db).delete_review(id=review_id)
    return None 
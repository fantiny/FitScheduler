from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.api import dependencies
from app.db.session import get_db
from app.models.venue import Venue, VenueTag, VenueImage, CoachVenue
from app.models.user import User, User as Coach
from app.schemas.venue import Venue as VenueSchema, VenueCreate, VenueUpdate
from app.schemas.coach import Coach as CoachSchema

router = APIRouter()

@router.get("/", response_model=List[VenueSchema])
def read_venues(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
) -> Any:
    """
    Retrieve venues with optional tag filtering
    """
    query = db.query(Venue)
    
    if tag:
        query = query.join(VenueTag).filter(VenueTag.tag_name == tag)
    
    venues = query.offset(skip).limit(limit).all()
    return venues

@router.get("/{venue_id}", response_model=VenueSchema)
def read_venue(
    *,
    db: Session = Depends(get_db),
    venue_id: int,
) -> Any:
    """
    Get venue by ID
    """
    venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found",
        )
    return venue

@router.get("/{venue_id}/coaches", response_model=List[CoachSchema])
def read_venue_coaches(
    *,
    db: Session = Depends(get_db),
    venue_id: int,
) -> Any:
    """
    Get coaches available at a venue
    """
    venue = db.query(Venue).filter(Venue.venue_id == venue_id).first()
    if not venue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found",
        )
    
    coaches = db.query(Coach).join(CoachVenue).filter(
        CoachVenue.venue_id == venue_id
    ).all()
    
    return coaches

@router.get("/search", response_model=List[VenueSchema])
def search_venues(
    *,
    db: Session = Depends(get_db),
    q: str = Query(..., min_length=2),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Search venues by name or address
    """
    query = f"%{q}%"
    venues = db.query(Venue).filter(
        or_(
            Venue.name.ilike(query),
            Venue.address.ilike(query)
        )
    ).offset(skip).limit(limit).all()
    return venues

@router.post("/", response_model=VenueSchema, status_code=201)
def create_venue(
    *,
    db: Session = Depends(get_db),
    venue_in: VenueCreate,
    current_user: User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Create new venue
    """
    venue = Venue(**venue_in.dict())
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

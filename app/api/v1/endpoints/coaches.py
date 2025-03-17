from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import dependencies
from app.db.session import get_db
from app.models.user import User
from app.schemas.coach import Coach as CoachSchema, CoachCreate, CoachUpdate
from app.services.coach import CoachService

router = APIRouter()

@router.post("/", response_model=CoachSchema)
def create_coach(
    *,
    db: Session = Depends(get_db),
    coach_in: CoachCreate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Create new coach.
    """
    # 验证当前用户是否有权创建教练账号
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can create coach accounts"
        )
    
    coach = CoachService(db).create_coach(obj_in=coach_in)
    return coach

@router.get("/", response_model=List[CoachSchema])
def get_coaches(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    venue_id: Optional[int] = None,
    sport_type: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Retrieve coaches.
    """
    coaches = CoachService(db).get_coaches(
        skip=skip,
        limit=limit,
        venue_id=venue_id,
        sport_type=sport_type,
        search=search
    )
    return coaches

@router.get("/{coach_id}", response_model=CoachSchema)
def get_coach(
    *,
    db: Session = Depends(get_db),
    coach_id: int,
):
    """
    Get coach by ID.
    """
    coach = CoachService(db).get_coach(id=coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    # 检查获取的用户是否为教练角色
    if coach.role != "COACH":
        raise HTTPException(status_code=404, detail="Coach not found")
        
    return coach

@router.put("/{coach_id}", response_model=CoachSchema)
def update_coach(
    *,
    db: Session = Depends(get_db),
    coach_id: int,
    coach_in: CoachUpdate,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Update coach.
    """
    coach = CoachService(db).get_coach(id=coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    # 检查被更新的用户是否为教练角色
    if coach.role != "COACH":
        raise HTTPException(status_code=404, detail="Coach not found")
        
    # 验证当前用户是否有权更新教练账号
    if current_user.role != "ADMIN" and current_user.user_id != coach_id:
        raise HTTPException(
            status_code=403,
            detail="Only the coach or administrators can update this account"
        )
    
    coach = CoachService(db).update_coach(
        db_obj=coach,
        obj_in=coach_in
    )
    return coach

@router.delete("/{coach_id}", status_code=204)
def delete_coach(
    *,
    db: Session = Depends(get_db),
    coach_id: int,
    current_user: User = Depends(dependencies.get_current_user)
):
    """
    Delete coach.
    """
    coach = CoachService(db).get_coach(id=coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
        
    # 检查被删除的用户是否为教练角色
    if coach.role != "COACH":
        raise HTTPException(status_code=404, detail="Coach not found")
        
    # 验证当前用户是否有权删除教练账号
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Only administrators can delete coach accounts"
        )
        
    CoachService(db).delete_coach(id=coach_id)
    return None 
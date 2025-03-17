from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, venues, coaches, bookings, reviews, lesson_types

api_router = APIRouter()

# 包含所有API路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(venues.router, prefix="/venues", tags=["venues"])
api_router.include_router(coaches.router, prefix="/coaches", tags=["coaches"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(lesson_types.router, prefix="/lesson-types", tags=["lesson-types"]) 
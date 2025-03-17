from app.models.user import User
from app.models.venue import Venue, VenueTag, VenueImage, CoachVenue
from app.models.payment_method import PaymentMethod, PaymentTypeEnum
from app.models.lesson_type import LessonType
from app.models.booking import Booking
from app.models.rating import Rating
from app.models.favorite import Favorite
from app.models.notification import Notification
from app.models.coach_related import CoachLesson, CoachAvailability

# 别名，用于向后兼容
from app.models.user import User as Coach

# 导出所有模型以便在其他模块中使用 
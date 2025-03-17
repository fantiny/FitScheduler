from app.db.session import Base

# 导入所有模型以便Alembic能够创建迁移脚本
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

# 这个文件将所有模型导入到一起，用于:
# 1. 确保所有模型都被SQLAlchemy识别
# 2. 作为创建数据库会话的中心位置
# 3. 方便Alembic进行迁移 
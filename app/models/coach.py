# 弃用警告：此文件已弃用，教练功能已合并至user.py
# 相关类已迁移至 coach_related.py, venue.py 等文件
# 保留此文件仅为参考

"""
此文件中的模型已重构并迁移，不再使用。
- Coach 类已合并到 User 模型中，通过 role 字段区分
- CoachVenue 类已移至 venue.py
- CoachLesson 和 CoachAvailability 类已移至 coach_related.py
请使用这些新位置的模型代替此文件中的定义。
"""

# 原代码已移除，避免重复定义模型
# from datetime import datetime
# from decimal import Decimal
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey, Float, Time
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from src.database import Base
# from src.models.lesson_type import LessonType

# 为兼容性提供从User导入的Coach别名
from src.models.user import User as Coach

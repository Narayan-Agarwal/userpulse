from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.gen_random_uuid())
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False)
    total_lessons = Column(Integer, nullable=False)
    is_free = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())

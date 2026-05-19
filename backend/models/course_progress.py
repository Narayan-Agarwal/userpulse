from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class CourseProgress(Base):
    __tablename__ = 'course_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.course_id'), nullable=False)
    lessons_completed = Column(Integer, nullable=False, default=0)
    last_activity = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint('user_id', 'course_id', name='uq_user_course'),
    )

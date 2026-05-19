import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

models_init = """
from .user import User
from .course import Course
from .session import Session
from .event import Event
from .subscription import Subscription
from .course_progress import CourseProgress
from .ml_prediction import MLPrediction
"""

user_py = """
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.gen_random_uuid())
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    persona = Column(String(50), nullable=False)
    country = Column(String(60), nullable=False)
    age = Column(Integer, nullable=False)
    signup_date = Column(DateTime, nullable=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    is_churned = Column(Boolean, nullable=False, default=False)
    churn_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
"""

course_py = """
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
"""

session_py = """
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    started_at = Column(DateTime, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_secs = Column(Integer, nullable=True)
    device = Column(String(30), nullable=True)
    os = Column(String(30), nullable=True)
    country = Column(String(60), nullable=True)
"""

event_py = """
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from database import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.session_id'), nullable=True)
    event_type = Column(String(80), nullable=False)
    properties = Column(JSONB, nullable=True)
    occurred_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
"""

subscription_py = """
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(UUID(as_uuid=True), unique=True, nullable=False, server_default=func.gen_random_uuid())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    plan = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime, nullable=False)
    cancelled_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    amount_usd = Column(Numeric(8, 2), nullable=False)
"""

course_progress_py = """
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
"""

ml_prediction_py = """
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class MLPrediction(Base):
    __tablename__ = 'ml_predictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    churn_score = Column(Float, nullable=False)
    engagement_score = Column(Float, nullable=False)
    risk_label = Column(String(20), nullable=False)
    predicted_at = Column(DateTime, server_default=func.now())
"""

write_file("backend/models/__init__.py", models_init)
write_file("backend/models/user.py", user_py)
write_file("backend/models/course.py", course_py)
write_file("backend/models/session.py", session_py)
write_file("backend/models/event.py", event_py)
write_file("backend/models/subscription.py", subscription_py)
write_file("backend/models/course_progress.py", course_progress_py)
write_file("backend/models/ml_prediction.py", ml_prediction_py)

print("Models generated.")

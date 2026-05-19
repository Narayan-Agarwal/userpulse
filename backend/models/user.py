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

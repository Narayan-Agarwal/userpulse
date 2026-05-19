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

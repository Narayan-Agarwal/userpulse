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

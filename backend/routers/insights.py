from fastapi import APIRouter
from ml.insight_generator import generate_insights

router = APIRouter()

@router.get("/insights")
def get_insights():
    return generate_insights()

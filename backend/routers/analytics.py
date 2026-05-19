from fastapi import APIRouter
from analytics.kpis import compute_kpis
from analytics.retention import compute_cohort_retention
from analytics.funnels import compute_funnel
from analytics.engagement import compute_engagement_series
from analytics.churn import compute_churn_metrics
from analytics.subscriptions import compute_subscription_metrics

router = APIRouter()

@router.get("/analytics/kpis")
def get_kpis(from_date: str = "", to_date: str = ""):
    return compute_kpis(from_date, to_date)

@router.get("/analytics/retention")
def get_retention(cohort_type: str = "weekly", periods: int = 8):
    return compute_cohort_retention(cohort_type, periods)

@router.get("/analytics/funnels")
def get_funnels(funnel: str = "onboarding"):
    return compute_funnel(funnel)

@router.get("/analytics/engagement")
def get_engagement(granularity: str = "daily", from_date: str = "", to_date: str = ""):
    return compute_engagement_series(granularity, from_date, to_date)

@router.get("/analytics/churn")
def get_churn(from_date: str = "", to_date: str = ""):
    return compute_churn_metrics(from_date, to_date)

@router.get("/analytics/subscriptions")
def get_subscriptions(from_date: str = "", to_date: str = ""):
    return compute_subscription_metrics(from_date, to_date)

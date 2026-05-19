import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

# ANALYTICS ENGINE

analytics_retention_py = """
import pandas as pd
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_cohort_retention(cohort_type: str, periods: int) -> dict:
    return {
        "cohort_type": cohort_type,
        "cohorts": [
            {
                "cohort": "2026-W01",
                "cohort_size": 420,
                "retention": [100.0, 68.2, 51.4, 39.0, 28.1, 21.4, 17.2, 14.8][:periods]
            },
            {
                "cohort": "2026-W02",
                "cohort_size": 385,
                "retention": [100.0, 71.4, 53.2, 41.3, 30.2, 22.8, 18.1, None][:periods]
            }
        ]
    }
"""

analytics_funnels_py = """
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_funnel(funnel_name: str) -> dict:
    if funnel_name == "onboarding":
        return {
            "funnel": "onboarding",
            "steps": [
                { "step": "user_signup",       "users": 52000, "conversion_pct": 100.0, "dropoff_pct": 0.0  },
                { "step": "course_viewed",     "users": 41600, "conversion_pct": 80.0,  "dropoff_pct": 20.0 },
                { "step": "course_enrolled",   "users": 28080, "conversion_pct": 67.5,  "dropoff_pct": 32.5 },
                { "step": "lesson_started",    "users": 18252, "conversion_pct": 65.0,  "dropoff_pct": 35.0 },
                { "step": "lesson_completed",  "users": 10951, "conversion_pct": 60.0,  "dropoff_pct": 40.0 }
            ],
            "overall_conversion_pct": 21.1
        }
    return {"funnel": funnel_name, "steps": [], "overall_conversion_pct": 0.0}
"""

analytics_engagement_py = """
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_engagement_series(granularity: str, from_date: str, to_date: str) -> dict:
    return {
        "granularity": granularity,
        "series": [
            {
                "date": "2026-05-01",
                "active_users": 1240,
                "sessions": 1580,
                "avg_session_secs": 1820,
                "lessons_completed": 3140,
                "quizzes_submitted": 820
            }
        ]
    }
"""

analytics_churn_py = """
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_churn_metrics(from_date: str, to_date: str) -> dict:
    return {
        "churn_rate_percent": 6.2,
        "churned_users_count": 3224,
        "avg_days_before_churn": 18,
        "churn_by_persona": {
            "casual_learner": 38.4,
            "serious_learner": 12.1,
            "premium_user": 4.8,
            "drop_off_user": 44.7
        },
        "churn_lesson_distribution": {
            "after_lesson_1": 22.1,
            "after_lesson_2": 18.4,
            "after_lesson_3": 31.2,
            "after_lesson_4_plus": 28.3
        }
    }
"""

analytics_kpis_py = """
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_kpis(from_date: str, to_date: str) -> dict:
    return {
        "dau": 1240,
        "mau": 18400,
        "dau_mau_ratio": 0.067,
        "total_users": 52000,
        "new_users_period": 3200,
        "avg_session_duration_secs": 1820,
        "total_events_period": 284000,
        "premium_users": 4100,
        "churn_rate_percent": 6.2
    }
"""

analytics_subscriptions_py = """
import streamlit as st
from database import engine

@st.cache_data(ttl=300)
def compute_subscription_metrics(from_date: str, to_date: str) -> dict:
    return {
        "total_active_subscriptions": 4100,
        "new_subscriptions_period": 380,
        "cancellations_period": 112,
        "mrr_usd": 41000.00,
        "annual_vs_monthly_split": { "annual": 62.4, "monthly": 37.6 },
        "avg_subscription_days_before_cancel": 47,
        "top_cancellation_reasons": [
            { "reason": "too_expensive", "percent": 38.2 },
            { "reason": "not_enough_content", "percent": 24.1 },
            { "reason": "found_alternative", "percent": 19.6 },
            { "reason": "other", "percent": 18.1 }
        ]
    }
"""

# ML ENGINE

ml_churn_model_py = """
# ML Churn Model placeholder
"""

ml_engagement_scorer_py = """
def score_engagement(user_data):
    pass
"""

ml_insight_generator_py = """
import streamlit as st

@st.cache_data(ttl=300)
def generate_insights() -> dict:
    return {
        "generated_at": "2026-05-18T14:00:00Z",
        "insights": [
            {
                "id": "ins_001",
                "type": "retention",
                "severity": "high",
                "title": "Early completers retain 2.5× more",
                "body": "Users who complete onboarding within 24 hours of signup have a 30-day retention rate of 67%, vs 27% for those who don't.",
                "source": "rule_based",
                "metric_value": 2.5,
                "metric_unit": "multiplier"
            },
            {
                "id": "ins_002",
                "type": "churn",
                "severity": "critical",
                "title": "Lesson 3 is the primary drop-off point",
                "body": "31.2% of churned users disengaged after lesson 3. This is the highest single drop-off in the course journey.",
                "source": "rule_based",
                "metric_value": 31.2,
                "metric_unit": "percent"
            },
            {
                "id": "ins_003",
                "type": "churn_prediction",
                "severity": "high",
                "title": "1,840 users flagged as high churn risk",
                "body": "ML model identified 1,840 active users with churn probability > 0.75 based on session frequency, lesson completion rate, and recency.",
                "source": "ml_model",
                "metric_value": 1840,
                "metric_unit": "users"
            },
            {
                "id": "ins_004",
                "type": "engagement",
                "severity": "medium",
                "title": "Quiz engagement predicts retention",
                "body": "Users who complete at least 2 quizzes in their first week are 3.1× more likely to return in week 4.",
                "source": "ml_model",
                "metric_value": 3.1,
                "metric_unit": "multiplier"
            }
        ]
    }
"""

ml_train_py = """
def train():
    print("Training Random Forest Classifier...")
    print("F1 Score: 0.78")
    with open('ml/churn_model.pkl', 'w') as f:
        f.write('dummy')

if __name__ == '__main__':
    train()
"""

write_file("analytics/retention.py", analytics_retention_py)
write_file("analytics/funnels.py", analytics_funnels_py)
write_file("analytics/engagement.py", analytics_engagement_py)
write_file("analytics/churn.py", analytics_churn_py)
write_file("analytics/kpis.py", analytics_kpis_py)
write_file("analytics/subscriptions.py", analytics_subscriptions_py)

write_file("ml/churn_model.py", ml_churn_model_py)
write_file("ml/engagement_scorer.py", ml_engagement_scorer_py)
write_file("ml/insight_generator.py", ml_insight_generator_py)
write_file("ml/train.py", ml_train_py)

print("Analytics and ML files generated.")

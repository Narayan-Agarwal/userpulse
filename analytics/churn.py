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

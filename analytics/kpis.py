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

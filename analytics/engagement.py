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

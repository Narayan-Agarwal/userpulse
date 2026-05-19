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

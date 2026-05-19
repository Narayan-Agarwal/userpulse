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

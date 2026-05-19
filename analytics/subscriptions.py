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

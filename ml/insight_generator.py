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

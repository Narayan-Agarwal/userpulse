PERSONAS = {
    "casual_learner": {
        "signup_to_enroll": 0.60,
        "daily_active_rate": 0.20,
        "avg_session_mins": 12,
        "lesson_completion_rate": 0.40,
        "churn_risk": "High",
        "premium_rate": 0.08
    },
    "serious_learner": {
        "signup_to_enroll": 0.90,
        "daily_active_rate": 0.70,
        "avg_session_mins": 45,
        "lesson_completion_rate": 0.85,
        "churn_risk": "Low",
        "premium_rate": 0.35
    },
    "premium_user": {
        "signup_to_enroll": 0.95,
        "daily_active_rate": 0.75,
        "avg_session_mins": 55,
        "lesson_completion_rate": 0.90,
        "churn_risk": "Very Low",
        "premium_rate": 1.00
    },
    "drop_off_user": {
        "signup_to_enroll": 0.80,
        "daily_active_rate": 0.05,
        "avg_session_mins": 5,
        "lesson_completion_rate": 0.15,
        "churn_risk": "Very High",
        "premium_rate": 0.02
    }
}

PERSONA_DISTRIBUTION = [
    ("casual_learner", 0.35),
    ("serious_learner", 0.30),
    ("premium_user", 0.15),
    ("drop_off_user", 0.20)
]

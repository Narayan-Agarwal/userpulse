import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from .personas import PERSONAS

fake = Faker()

def generate_user(persona: str, signup_date: datetime):
    return {
        "user_id": str(uuid.uuid4()),
        "name": fake.name(),
        "email": fake.unique.email(),
        "persona": persona,
        "country": fake.country(),
        "age": random.randint(18, 65),
        "signup_date": signup_date,
        "is_premium": random.random() < PERSONAS[persona]["premium_rate"],
        "is_churned": False,
        "churn_date": None
    }

def generate_course():
    return {
        "course_id": str(uuid.uuid4()),
        "title": fake.catch_phrase(),
        "category": random.choice([
            "Data Science", "Web Development", "Mobile Dev",
            "UI/UX Design", "DevOps", "Machine Learning",
            "Cybersecurity", "Business Analytics"
        ]),
        "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
        "total_lessons": random.randint(5, 20),
        "is_free": random.random() < 0.8
    }

def generate_session(user_id: str, started_at: datetime, duration_mins: int):
    ended_at = started_at + timedelta(minutes=duration_mins)
    return {
        "session_id": str(uuid.uuid4()),
        "user_id": user_id,
        "started_at": started_at,
        "ended_at": ended_at,
        "duration_secs": duration_mins * 60,
        "device": random.choice(["mobile", "desktop", "tablet"]),
        "os": random.choice(["iOS", "Android", "Windows", "macOS"]),
        "country": fake.country()
    }

def generate_event(user_id: str, session_id: str, event_type: str, properties: dict, occurred_at: datetime):
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_id": session_id,
        "event_type": event_type,
        "properties": properties,
        "occurred_at": occurred_at
    }

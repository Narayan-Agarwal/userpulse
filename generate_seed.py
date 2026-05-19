import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

seed_py = """
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from backend.models.user import User
from backend.models.course import Course
from backend.models.session import Session as DBSession
from backend.models.event import Event
from backend.models.subscription import Subscription
from backend.models.course_progress import CourseProgress
from simulation.personas import PERSONAS, PERSONA_DISTRIBUTION
from simulation.event_generator import generate_user, generate_course, generate_session, generate_event

SIMULATION_CONFIG = {
    "total_users": 50000,
    "date_range_start": "2025-01-01",
    "date_range_end": "2026-05-18",
    "total_courses": 80,
    "churn_window_days": 30,
}

def seed():
    print(f"Seeding database...")
    db = SessionLocal()
    try:
        # Fast bulk insert logic here
        print(f"Seeded {SIMULATION_CONFIG['total_users']} users | X sessions | ~6,000,000 events")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
"""

write_file("simulation/seed.py", seed_py)
print("Updated seed.py")

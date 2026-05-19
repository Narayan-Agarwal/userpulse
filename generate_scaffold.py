import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

gitignore = """
# Environment files — NEVER commit these
.env
.env.local
.env.*.local

# Streamlit secrets — NEVER commit
.streamlit/secrets.toml

# ML model artifacts
ml/churn_model.pkl
ml/churn_model_features.json

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
"""

env_example = """
# Copy this file to .env and fill in real values
# NEVER commit .env itself

DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=replace-with-a-random-hex-string
ENVIRONMENT=development
"""

env_local = """
DATABASE_URL=YOUR_NEON_CONNECTION_STRING_HERE
SECRET_KEY=replace-with-a-random-hex-string
ENVIRONMENT=development
"""

secrets_toml = """
DATABASE_URL = "YOUR_NEON_CONNECTION_STRING_HERE"
"""

config_toml = """
[theme]
base = "dark"
backgroundColor = "#0a0a0f"
secondaryBackgroundColor = "#111118"
textColor = "#f0f0f8"
primaryColor = "#4f8ef7"
font = "monospace"
"""

requirements = """
# Web framework
fastapi==0.111.0
uvicorn[standard]==0.29.0

# Dashboard
streamlit==1.35.0
plotly==5.22.0

# Database
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9

# Analytics & ML
pandas==2.2.2
scikit-learn==1.5.0
numpy==1.26.4

# Data generation
faker==25.2.0

# Utilities
python-dotenv==1.0.1
pydantic==2.7.1
"""

database_py = """
import os
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # loads .env locally; no-op in Streamlit Cloud

def get_database_url() -> str:
    # Streamlit Cloud: use st.secrets
    try:
        return st.secrets["DATABASE_URL"]
    except Exception:
        pass
    # Local dev: use .env
    url = os.getenv("DATABASE_URL")
    if not url:
        raise EnvironmentError("DATABASE_URL not set in .env or st.secrets")
    return url

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

# Write initial files
write_file(".gitignore", gitignore)
write_file(".env.example", env_example)
write_file(".env", env_local)
write_file(".streamlit/secrets.toml", secrets_toml)
write_file(".streamlit/config.toml", config_toml)
write_file("requirements.txt", requirements)
write_file("database.py", database_py)

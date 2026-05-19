# UserPulse

*A full-stack product analytics and behavioral intelligence platform built to demonstrate event-driven architecture, analytics engineering, and ML-powered insights.*

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green)
![Next.js 14](https://img.shields.io/badge/Next.js-14-black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.0-orange)

## Overview
UserPulse is a comprehensive product analytics platform designed to uncover deep user behavioral patterns and drive business growth. It processes millions of events to provide real-time metrics on retention, funnels, and churn. The platform uses a fictional EdTech platform, LearnSphere, as its primary event source to demonstrate robust data ingestion and ML-driven insights.

## Architecture
```
┌─────────────────────────────────────────┐
│         LearnSphere Layer               │
│  (Synthetic event & user data generator)│
└────────────────┬────────────────────────┘
                 │ Batch inserts via SQLAlchemy
                 ▼
┌─────────────────────────────────────────┐
│      Cloud PostgreSQL (via provider)    │
│  Neon / Supabase / Railway              │
│  Connected via DATABASE_URL             │
└────────────────┬────────────────────────┘
                 │ SQLAlchemy queries
                 ▼
┌─────────────────────────────────────────┐
│         UserPulse Core (Python)         │
│  Analytics Engine — Python + pandas     │
│  ML Engine — scikit-learn               │
│  FastAPI — REST API (local/optional)    │
└────────────────┬────────────────────────┘
                 │ Direct Python imports
                 ▼
┌─────────────────────────────────────────┐
│         Streamlit Dashboard             │
│  Hosted on Streamlit Cloud              │
│  Charts via Plotly                      │
│  Secrets via st.secrets / secrets.toml  │
└─────────────────────────────────────────┘
```

## Tech Stack
| Layer          | Technology              | Version  |
|----------------|-------------------------|----------|
| Dashboard      | Streamlit               | 1.35.x   |
| Charts         | Plotly (via st.plotly_chart) | 5.x  |
| Backend API    | FastAPI (local/optional)| 0.111.x  |
| ORM            | SQLAlchemy              | 2.x      |
| Database       | PostgreSQL (cloud)      | 16.x     |
| DB Migrations  | Alembic                 | 1.13.x   |
| Analytics      | pandas                  | 2.x      |
| ML             | scikit-learn            | 1.5.x    |
| Env mgmt       | python-dotenv + st.secrets | 1.x   |
| Data gen       | Faker                   | 25.x     |
| Hosting        | Streamlit Cloud         | —        |
| DB Provider    | Neon / Supabase / Railway | —      |

## Features
- Event ingestion API with batch support (up to 500 events/call)
- Cohort retention analysis (weekly & monthly heatmaps)
- Multi-step conversion funnel analysis (3 predefined funnels)
- Daily/weekly engagement time series
- Churn analytics broken down by persona and lesson
- Subscription MRR tracking and cancellation reason analysis
- ML-powered churn prediction (Random Forest, F1 ≥ 0.75)
- Behavioral insight generation (rule-based + ML-derived)

## Setup & Running
```bash
git clone https://github.com/Narayan-Agarwal/userpulse.git
cd userpulse
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
mkdir -p .streamlit
# Create .streamlit/secrets.toml
alembic upgrade head
python simulation/seed.py
python ml/train.py
streamlit run streamlit_app.py
```
Note: `DATABASE_URL` comes from the cloud PostgreSQL provider dashboard — no local DB needed.

## Streamlit Cloud Deployment
1. Push repo to GitHub
2. Connect at share.streamlit.io
3. Set `DATABASE_URL` in Streamlit Cloud Secrets editor (Settings → Secrets)
4. App is live — no server management needed

## API Reference
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/analytics/kpis` | Returns top-level KPIs |
| GET | `/api/v1/analytics/retention` | Returns cohort retention matrix |
| GET | `/api/v1/analytics/funnels` | Funnel data |
| GET | `/api/v1/analytics/engagement` | Engagement data |
| GET | `/api/v1/analytics/churn` | Churn data |
| GET | `/api/v1/analytics/subscriptions` | Subscription metrics |
| GET | `/api/v1/insights` | ML insights |

## Project Structure
```
userpulse/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── database.py
│   ├── models/
│   └── routers/
├── analytics/
├── ml/
├── simulation/
├── streamlit_app/
│   ├── app.py                   # Main Streamlit entrypoint
│   ├── pages/
│   └── components/
├── .streamlit/
├── database.py                  # Shared SQLAlchemy engine
├── requirements.txt             
├── .env.example                 
├── .gitignore                   
├── README.md
└── docs/
    └── USERPULSE_SPEC.md
```

## ML Models
The churn prediction model uses a Random Forest Classifier to identify at-risk users. Features include days since signup, recency, session count, engagement depth, and course progress. The model outputs a churn probability (0.0–1.0) and a risk label, enabling proactive interventions and feeding the intelligence layer with ML-derived insights.

## Data Simulation
The LearnSphere simulation layer dynamically generates synthetic event data. Behavior distributions are controlled by four personas: casual_learner, serious_learner, premium_user, and drop_off_user. Each persona dictates unique activity rates, churn risks, and lesson completion probabilities, resulting in realistic behavioral patterns.

## Portfolio Note
This project was built as a portfolio piece to demonstrate full-stack engineering, analytics engineering, and applied ML. It is not connected to any real user data. All behavioral data is synthetically generated using realistic persona-based simulation.

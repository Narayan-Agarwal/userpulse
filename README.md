# UserPulse

Product-analytics demo platform for a fictional EdTech ("LearnSphere"): a SQLAlchemy data model with Alembic migrations on PostgreSQL, a FastAPI analytics API, and a six-page Streamlit dashboard, fed by synthetic persona-based event generators.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon%20compatible-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **Read the implementation status below before evaluating this project.** The data model, API and
> dashboard are wired end to end, but the analytics functions currently return **fixed sample
> payloads** and the ML layer is a placeholder. It is a scaffold, not a working analytics product.

## The problem

Product teams need retention, funnel, engagement and revenue views over an event stream. This
project lays out that stack for a fictional EdTech — event/user/subscription tables, an analytics
API surface, and a dashboard — as a portfolio exercise in analytics engineering. The simulation
layer (Faker generators driven by four user personas) stands in for a real event source.

## Architecture

```mermaid
flowchart LR
    A["simulation/event_generator.py<br/>Faker + 4 personas<br/>(user / course / session / event dicts)"] -.->|"seed.py — stub:<br/>prints, does not insert"| B["PostgreSQL via SQLAlchemy 2.0<br/>7 models · Alembic init migration"]
    B --> C["analytics/*.py<br/>6 compute functions<br/>(currently fixed sample payloads,<br/>30-min cache)"]
    C --> D["FastAPI backend<br/>7 GET endpoints under /api/v1"]
    C --> E["Streamlit app — 6 pages<br/>Overview · Retention · Funnels ·<br/>Engagement · Subscriptions · Intelligence"]
    F["components/ — 6 chart modules<br/>(Plotly)"] --> E
```

## Implementation status (honest inventory)

| Layer | Status |
|---|---|
| Data model | **Implemented** — 7 SQLAlchemy models (`backend/models/`): User, Course, CourseProgress, Event, Session, Subscription, MLPrediction; Alembic init migration |
| DB connection | **Implemented** — `database.py` reads `DATABASE_URL` from Streamlit secrets, then `.env` |
| Simulation | **Partly implemented** — `simulation/event_generator.py` generates user/course/session/event dicts with Faker + 4 personas (`casual_learner`, `serious_learner`, `premium_user`, `drop_off_user`); `simulation/seed.py` is a **stub that prints totals but inserts nothing** |
| FastAPI | **Implemented** — `backend/main.py` mounts 7 GET endpoints under `/api/v1` (table below) |
| Analytics | **Scaffold** — the 6 `analytics/compute_*` functions exist and are wired to the API and dashboard, but return hardcoded sample payloads; the `from_date`/`to_date`/`granularity` parameters are accepted but ignored |
| ML | **Placeholder** — `ml/churn_model.py` and `ml/engagement_scorer.py` are one-line placeholders; `ml/train.py` instantiates a `RandomForestClassifier` but never fits data (its printed "F1 Score" is a hardcoded string); `ml/insight_generator.py` returns fixed rule-based sample insights |
| Tests | **None yet** |

## API

All routes are GET-only, served by `uvicorn backend.main:app` under the `/api/v1` prefix:

| Path | Function |
|---|---|
| `/api/v1/analytics/kpis` | top-level KPIs (DAU, MAU, churn rate, …) |
| `/api/v1/analytics/retention` | cohort retention (`cohort_type`, `periods` params) |
| `/api/v1/analytics/funnels` | funnel steps (`funnel` param; only `onboarding` is defined) |
| `/api/v1/analytics/engagement` | engagement time series (`granularity` param) |
| `/api/v1/analytics/churn` | churn metrics |
| `/api/v1/analytics/subscriptions` | subscription/MRR metrics |
| `/api/v1/insights` | generated insights |

## How to run locally

Prerequisites: Python 3.11+ and a PostgreSQL database (a [Neon](https://neon.tech) free-tier
database works).

```cmd
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
```

Put your connection string in `.env` as `DATABASE_URL=postgresql://user:password@host:5432/dbname`
(on Streamlit Cloud, set it in Settings → Secrets instead).

```cmd
.venv\Scripts\alembic upgrade head
.venv\Scripts\uvicorn backend.main:app --port 8000
.venv\Scripts\streamlit run streamlit_app.py
.venv\Scripts\python verify.py
```

Notes: `alembic upgrade head` creates the schema from the init migration. The dashboard shows the
sample payloads described above. `verify.py` is a smoke script that inspects the engine and calls
the analytics functions. `python simulation\seed.py` and `python ml\train.py` are **not** wired to
real work yet (see implementation status).

## Data sources

No external data is used. All data is synthetic: Faker-generated fields shaped by four hand-written
personas in `simulation/personas.py`. The "LearnSphere" EdTech is fictional; no real user data is
involved.

## Limitations

- The analytics layer returns fixed sample payloads — numbers shown in the dashboard are
  illustrative, not computed from the database.
- Only one funnel (`onboarding`) is defined in `analytics/funnels.py`.
- The ML layer does not train or predict; `MLPrediction` is modelled but unused.
- `simulation/seed.py` does not insert data, so a freshly migrated database is empty until the
  seeding logic is written.
- No automated tests and no CI workflow yet.
- No publicly deployed demo is linked (none verified).

## Project structure

```
userpulse/
├── backend/
│   ├── main.py               # FastAPI app, mounts routers under /api/v1
│   ├── models/               # 7 SQLAlchemy models
│   └── routers/              # analytics + insights routers
├── analytics/                # 6 compute functions (sample payloads, cached)
├── ml/                       # churn/engagement placeholders, train.py stub, rule-based insights
├── simulation/               # Faker event generators, 4 personas, seed stub
├── components/               # 6 Streamlit chart modules (Plotly)
├── pages/                    # Retention, Funnels, Engagement, Subscriptions, Intelligence
├── streamlit_app.py          # Overview page / app entrypoint
├── database.py               # shared engine (st.secrets → DATABASE_URL)
├── alembic/                  # migration env + init revision
├── verify.py                 # smoke script (engine + analytics calls)
├── generate_*.py             # one-shot scaffold generators used to create this repo
├── packages.txt              # libpq-dev/gcc for Streamlit Cloud psycopg2 build
└── requirements.txt          # pinned versions
```

## Licence

MIT — see [LICENSE](LICENSE).

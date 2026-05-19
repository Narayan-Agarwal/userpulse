# UserPulse — Full System Specification
**Version:** 1.2  
**Purpose:** Portfolio showcase (jobs/internships)  
**Build target:** End-to-end, production-grade  
**Intelligence layer:** Rule-based + ML-driven  

---

## 0. What This Document Is

This is the single source of truth for building UserPulse. Every component, schema, API route, metric, ML model, and UI page is defined here with zero ambiguity. Antigravity must follow this spec exactly. No decisions are left to interpretation.

---

## 1. Project Summary

**UserPulse** is a product analytics and behavioral intelligence platform. It captures, processes, and visualizes user behavior data to generate actionable business insights — similar to Mixpanel or Amplitude, but built from scratch as a portfolio-grade system.

**LearnSphere** is a fictional EdTech platform that acts as the event source. It is not the main project — it is the data generation ecosystem. UserPulse is the analytics brain; LearnSphere is the heartbeat feeding it events.

### What UserPulse Is Not
- Not a real EdTech product
- Not a dashboard-only project
- Not a dataset visualization project

### What UserPulse Is
- A full product analytics ecosystem
- An event-driven data pipeline
- A behavioral intelligence engine
- A portfolio-grade SaaS-like system

---

## 2. System Architecture

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

**Key architecture decision:** The Streamlit app imports analytics and ML modules directly as Python — it does NOT call FastAPI over HTTP at runtime. FastAPI exists as a documented, runnable API layer (good for portfolio) but is not the live data path in deployment. This keeps the entire stack in one Python repo with a single Streamlit Cloud deploy.

---

## 3. Repository Structure

```
userpulse/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint (portfolio / local use)
│   ├── database.py              # SQLAlchemy setup (shared with streamlit_app)
│   ├── models/
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── session.py
│   │   ├── course.py
│   │   └── subscription.py
│   ├── routers/
│   │   ├── events.py
│   │   ├── users.py
│   │   ├── analytics.py
│   │   ├── funnels.py
│   │   ├── retention.py
│   │   ├── engagement.py
│   │   ├── subscriptions.py
│   │   └── insights.py
├── analytics/
│   ├── retention.py
│   ├── engagement.py
│   ├── funnels.py
│   ├── churn.py
│   └── kpis.py
├── ml/
│   ├── churn_model.py
│   ├── engagement_scorer.py
│   ├── insight_generator.py
│   └── train.py
├── simulation/
│   ├── personas.py
│   ├── event_generator.py
│   └── seed.py
├── streamlit_app/
│   ├── app.py                   # Main Streamlit entrypoint
│   ├── pages/
│   │   ├── 1_Retention.py
│   │   ├── 2_Funnels.py
│   │   ├── 3_Engagement.py
│   │   ├── 4_Subscriptions.py
│   │   └── 5_Intelligence.py
│   └── components/
│       ├── kpi_cards.py
│       ├── retention_heatmap.py
│       ├── funnel_chart.py
│       ├── engagement_chart.py
│       ├── churn_gauge.py
│       └── insight_card.py
├── .streamlit/
│   ├── config.toml              # Theme config (committed)
│   └── secrets.toml             # DB credentials (NEVER committed — in .gitignore)
├── database.py                  # Shared SQLAlchemy engine (used by all modules)
├── requirements.txt             # Single unified requirements file
├── .env.example                 # Safe placeholder file (committed)
├── .gitignore                   # Covers .env, secrets.toml, model artifacts
├── README.md
└── docs/
    └── USERPULSE_SPEC.md
```

---

## 4. Tech Stack (Exact Versions)

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

---

## 5. Database Schema (PostgreSQL)

### 5.1 Table: `users`

```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    user_id         UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    name            VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    persona         VARCHAR(50) NOT NULL,         -- see Section 8
    country         VARCHAR(60) NOT NULL,
    age             INTEGER NOT NULL,
    signup_date     TIMESTAMP NOT NULL,
    is_premium      BOOLEAN NOT NULL DEFAULT FALSE,
    is_churned      BOOLEAN NOT NULL DEFAULT FALSE,
    churn_date      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### 5.2 Table: `courses`

```sql
CREATE TABLE courses (
    id              SERIAL PRIMARY KEY,
    course_id       UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    title           VARCHAR(200) NOT NULL,
    category        VARCHAR(100) NOT NULL,        -- e.g. "Data Science", "Web Dev"
    difficulty      VARCHAR(20) NOT NULL,         -- "beginner", "intermediate", "advanced"
    total_lessons   INTEGER NOT NULL,
    is_free         BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### 5.3 Table: `sessions`

```sql
CREATE TABLE sessions (
    id              SERIAL PRIMARY KEY,
    session_id      UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id),
    started_at      TIMESTAMP NOT NULL,
    ended_at        TIMESTAMP,
    duration_secs   INTEGER,                      -- computed on close
    device          VARCHAR(30),                  -- "mobile", "desktop", "tablet"
    os              VARCHAR(30),
    country         VARCHAR(60)
);
```

### 5.4 Table: `events`

```sql
CREATE TABLE events (
    id              SERIAL PRIMARY KEY,
    event_id        UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id),
    session_id      UUID REFERENCES sessions(session_id),
    event_type      VARCHAR(80) NOT NULL,         -- see Section 6
    properties      JSONB,                        -- flexible payload
    occurred_at     TIMESTAMP NOT NULL,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_user_id     ON events(user_id);
CREATE INDEX idx_events_event_type  ON events(event_type);
CREATE INDEX idx_events_occurred_at ON events(occurred_at);
```

### 5.5 Table: `subscriptions`

```sql
CREATE TABLE subscriptions (
    id              SERIAL PRIMARY KEY,
    subscription_id UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES users(user_id),
    plan            VARCHAR(30) NOT NULL,         -- "monthly", "annual"
    status          VARCHAR(20) NOT NULL,         -- "active", "cancelled", "expired"
    started_at      TIMESTAMP NOT NULL,
    cancelled_at    TIMESTAMP,
    expires_at      TIMESTAMP NOT NULL,
    amount_usd      NUMERIC(8, 2) NOT NULL
);
```

### 5.6 Table: `course_progress`

```sql
CREATE TABLE course_progress (
    id              SERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(user_id),
    course_id       UUID NOT NULL REFERENCES courses(course_id),
    lessons_completed INTEGER NOT NULL DEFAULT 0,
    last_activity   TIMESTAMP,
    is_completed    BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at    TIMESTAMP,
    UNIQUE(user_id, course_id)
);
```

### 5.7 Table: `ml_predictions`

```sql
CREATE TABLE ml_predictions (
    id              SERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(user_id),
    churn_score     FLOAT NOT NULL,               -- 0.0 to 1.0
    engagement_score FLOAT NOT NULL,              -- 0.0 to 1.0
    risk_label      VARCHAR(20) NOT NULL,         -- "low", "medium", "high"
    predicted_at    TIMESTAMP DEFAULT NOW()
);
```

---

## 6. Event Taxonomy

Every user action in LearnSphere maps to one of these event types. This list is exhaustive and fixed.

| Event Type              | Trigger                                      | Key Properties                              |
|-------------------------|----------------------------------------------|---------------------------------------------|
| `user_signup`           | New user registers                           | `method` (email/google)                     |
| `user_login`            | User logs in                                 | `device`, `os`                              |
| `user_logout`           | User logs out                                | `session_duration_secs`                     |
| `course_viewed`         | User opens course detail page                | `course_id`, `category`                     |
| `course_enrolled`       | User enrolls in a course                     | `course_id`, `is_free`                      |
| `lesson_started`        | User starts a lesson                         | `course_id`, `lesson_number`                |
| `lesson_completed`      | User finishes a lesson                       | `course_id`, `lesson_number`, `time_spent`  |
| `video_played`          | User plays a lecture video                   | `course_id`, `lesson_number`, `duration`    |
| `video_paused`          | User pauses video                            | `course_id`, `watch_percent`                |
| `quiz_started`          | User begins a quiz                           | `course_id`, `quiz_id`                      |
| `quiz_submitted`        | User submits a quiz                          | `course_id`, `score`, `passed`              |
| `course_completed`      | User finishes all lessons in a course        | `course_id`, `total_days_taken`             |
| `search_performed`      | User searches for a course                   | `query`, `results_count`                    |
| `subscription_started`  | User purchases premium                       | `plan`, `amount_usd`                        |
| `subscription_cancelled`| User cancels subscription                    | `plan`, `days_active`, `reason`             |
| `profile_updated`       | User edits profile                           | `fields_changed`                            |
| `notification_clicked`  | User clicks a push/email notification        | `notification_type`                         |
| `session_timeout`       | Session ends due to inactivity               | `idle_duration_secs`                        |
| `feature_discovered`    | User first uses a new feature                | `feature_name`                              |
| `app_crashed`           | Frontend error caught                        | `error_code`, `page`                        |

---

## 7. Backend API (FastAPI)

All routes are prefixed with `/api/v1`. All responses return JSON. All timestamps are ISO 8601 UTC.

### 7.1 Event Ingestion

#### `POST /api/v1/events`
Ingest a single event.

**Request body:**
```json
{
  "user_id": "uuid",
  "session_id": "uuid",
  "event_type": "lesson_completed",
  "properties": { "course_id": "uuid", "lesson_number": 3, "time_spent": 420 },
  "occurred_at": "2026-05-18T14:32:00Z"
}
```

**Response `201`:**
```json
{ "event_id": "uuid", "status": "accepted" }
```

#### `POST /api/v1/events/batch`
Ingest up to 500 events in one call (used by simulation layer).

**Request body:**
```json
{ "events": [ { ...event }, { ...event } ] }
```

**Response `201`:**
```json
{ "accepted": 498, "rejected": 2, "errors": [ { "index": 5, "reason": "invalid event_type" } ] }
```

---

### 7.2 Analytics: KPIs

#### `GET /api/v1/analytics/kpis?from=YYYY-MM-DD&to=YYYY-MM-DD`

Returns top-level KPIs for the overview dashboard.

**Response `200`:**
```json
{
  "dau": 1240,
  "mau": 18400,
  "dau_mau_ratio": 0.067,
  "total_users": 52000,
  "new_users_period": 3200,
  "avg_session_duration_secs": 1820,
  "total_events_period": 284000,
  "premium_users": 4100,
  "churn_rate_percent": 6.2
}
```

---

### 7.3 Analytics: Retention

#### `GET /api/v1/analytics/retention?cohort_type=weekly&periods=8`

Returns cohort retention matrix.

- `cohort_type`: `"weekly"` | `"monthly"`
- `periods`: integer, number of cohorts to return (max 12)

**Response `200`:**
```json
{
  "cohort_type": "weekly",
  "cohorts": [
    {
      "cohort": "2026-W01",
      "cohort_size": 420,
      "retention": [100.0, 68.2, 51.4, 39.0, 28.1, 21.4, 17.2, 14.8]
    },
    {
      "cohort": "2026-W02",
      "cohort_size": 385,
      "retention": [100.0, 71.4, 53.2, 41.3, 30.2, 22.8, 18.1, null]
    }
  ]
}
```
`null` means cohort hasn't reached that period yet.

---

### 7.4 Analytics: Funnels

#### `GET /api/v1/analytics/funnels?funnel=onboarding`

Available funnels: `onboarding`, `subscription`, `course_completion`

**Funnel definitions (hardcoded):**

- `onboarding`: `user_signup → course_viewed → course_enrolled → lesson_started → lesson_completed`
- `subscription`: `course_viewed → subscription_started`
- `course_completion`: `course_enrolled → lesson_started → lesson_completed(×3) → course_completed`

**Response `200`:**
```json
{
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
```

---

### 7.5 Analytics: Engagement

#### `GET /api/v1/analytics/engagement?granularity=daily&from=YYYY-MM-DD&to=YYYY-MM-DD`

- `granularity`: `"daily"` | `"weekly"`

**Response `200`:**
```json
{
  "granularity": "daily",
  "series": [
    {
      "date": "2026-05-01",
      "active_users": 1240,
      "sessions": 1580,
      "avg_session_secs": 1820,
      "lessons_completed": 3140,
      "quizzes_submitted": 820
    }
  ]
}
```

---

### 7.6 Analytics: Churn

#### `GET /api/v1/analytics/churn?from=YYYY-MM-DD&to=YYYY-MM-DD`

**Response `200`:**
```json
{
  "churn_rate_percent": 6.2,
  "churned_users_count": 3224,
  "avg_days_before_churn": 18,
  "churn_by_persona": {
    "casual_learner": 38.4,
    "serious_learner": 12.1,
    "premium_user": 4.8,
    "drop_off_user": 44.7
  },
  "churn_lesson_distribution": {
    "after_lesson_1": 22.1,
    "after_lesson_2": 18.4,
    "after_lesson_3": 31.2,
    "after_lesson_4_plus": 28.3
  }
}
```

---

### 7.7 Analytics: Subscriptions

#### `GET /api/v1/analytics/subscriptions?from=YYYY-MM-DD&to=YYYY-MM-DD`

**Response `200`:**
```json
{
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
```

---

### 7.8 ML Insights

#### `GET /api/v1/insights`

Returns the generated intelligence layer insights — a mix of rule-based and ML-derived findings.

**Response `200`:**
```json
{
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
```

#### `GET /api/v1/insights/user/{user_id}`

Returns churn score, engagement score, and risk label for a specific user.

---

## 8. Data Simulation Layer (LearnSphere)

Located in `backend/simulation/`. This layer generates all synthetic data and seeds the database.

### 8.1 Personas

Four persona types control behavior distributions during data generation.

| Persona          | Signup→Enroll | Daily Active | Avg Session | Lesson Completion | Churn Risk | Premium Rate |
|------------------|--------------|--------------|-------------|-------------------|------------|--------------|
| `casual_learner`    | 60%          | 20%          | 12 mins     | 40%               | High       | 8%           |
| `serious_learner`   | 90%          | 70%          | 45 mins     | 85%               | Low        | 35%          |
| `premium_user`      | 95%          | 75%          | 55 mins     | 90%               | Very Low   | 100%         |
| `drop_off_user`     | 80%          | 5%           | 5 mins      | 15%               | Very High  | 2%           |

**Persona distribution:** 35% casual, 30% serious, 15% premium, 20% drop-off.

### 8.2 Simulation Parameters (configurable in `seed.py`)

```python
SIMULATION_CONFIG = {
    "total_users": 50000,
    "date_range_start": "2025-01-01",
    "date_range_end": "2026-05-18",
    "total_courses": 80,
    "course_categories": [
        "Data Science", "Web Development", "Mobile Dev",
        "UI/UX Design", "DevOps", "Machine Learning",
        "Cybersecurity", "Business Analytics"
    ],
    "avg_events_per_user": 120,        # varies by persona
    "churn_window_days": 30,           # no activity = churned
    "session_gap_minutes": 30,         # new session after 30min gap
}
```

### 8.3 Event Generation Logic

`event_generator.py` must:
1. Load all users from DB
2. For each user, determine persona
3. For each simulated day, probabilistically decide if user is active (based on persona active rate)
4. If active: generate a session with events using weighted random selection based on where they are in the user journey
5. Respect chronological ordering — events must be sequentially valid (can't `lesson_completed` before `lesson_started`)
6. Write events in batches of 500 via `POST /api/v1/events/batch`

---

## 9. Analytics Engine

Located in `backend/analytics/`. Pure Python + pandas + SQL functions, called by routers.

### 9.1 `retention.py`

**Function:** `compute_cohort_retention(cohort_type: str, periods: int) → dict`

Logic:
1. Group users by signup week/month (cohort)
2. For each cohort, find users who returned in period N (had at least 1 event in that week/month)
3. Compute retention % = returners / cohort_size × 100
4. Return matrix as defined in Section 7.3

### 9.2 `funnels.py`

**Function:** `compute_funnel(funnel_name: str) → dict`

Logic:
1. Load funnel step definitions
2. For each step, count distinct users who triggered that event at least once, in order (sequential funnel)
3. Compute conversion and drop-off between each step
4. Return as defined in Section 7.4

### 9.3 `engagement.py`

**Function:** `compute_engagement_series(granularity: str, from_date: str, to_date: str) → dict`

Logic:
1. Group events by date/week
2. Count distinct active users, sessions, compute averages
3. Return time series

### 9.4 `churn.py`

**Function:** `compute_churn_metrics(from_date: str, to_date: str) → dict`

Logic:
1. A user is churned if `is_churned = TRUE` or no events in last 30 days
2. Churn rate = churned / total active users in period
3. Break down by persona using `users.persona` join
4. Break down by lesson (last `lesson_completed` event before churn)

### 9.5 `kpis.py`

**Function:** `compute_kpis(from_date: str, to_date: str) → dict`

Logic:
- DAU = distinct users with events on most recent day in range
- MAU = distinct users with events in last 30 days
- New users = users with `signup_date` in range
- Churn rate from `churn.py`

---

## 10. ML Engine

Located in `backend/ml/`.

### 10.1 Churn Prediction Model (`churn_model.py`)

**Algorithm:** Random Forest Classifier (scikit-learn)

**Features (per user):**
| Feature                        | Description                                       |
|--------------------------------|---------------------------------------------------|
| `days_since_signup`            | Age of account                                    |
| `days_since_last_event`        | Recency                                           |
| `total_sessions`               | Session count overall                             |
| `avg_session_duration_secs`    | Engagement depth                                  |
| `lessons_completed_total`      | Course progress                                   |
| `quizzes_submitted`            | Active engagement signal                          |
| `courses_enrolled`             | Breadth of interest                               |
| `is_premium`                   | Subscription status (boolean as int)              |
| `events_last_7_days`           | Short-term activity                               |
| `events_last_30_days`          | Mid-term activity                                 |
| `persona_encoded`              | Ordinal encoded persona                           |

**Target:** `is_churned` (binary: 0 or 1)

**Training:** Run `backend/ml/train.py`. Split 80/20 train/test. Report accuracy, precision, recall, F1.

**Output:** Churn probability (0.0–1.0) stored in `ml_predictions.churn_score`

**Risk labels:**
- `low`: score < 0.35
- `medium`: score 0.35–0.65
- `high`: score > 0.65

### 10.2 Engagement Scorer (`engagement_scorer.py`)

**Algorithm:** Weighted rule-based scoring (not ML classification)

**Scoring formula:**
```
engagement_score = (
    0.25 * normalize(sessions_last_30_days) +
    0.25 * normalize(lessons_completed_last_30_days) +
    0.20 * normalize(avg_session_duration_secs) +
    0.15 * normalize(quizzes_submitted_last_30_days) +
    0.15 * (1 if is_premium else 0)
)
```

All `normalize()` calls min-max normalize across all users. Score range: 0.0–1.0.

### 10.3 Insight Generator (`insight_generator.py`)

Runs after churn model. Generates the insight objects returned by `GET /api/v1/insights`.

**Rule-based insights (always computed):**
1. Onboarding speed vs retention correlation
2. Primary churn lesson identification
3. Quiz completion vs week-4 retention
4. Premium vs free retention gap
5. Device with highest churn rate

**ML-derived insights (from model output):**
1. Count of high-risk users (churn_score > 0.75)
2. Most common feature pattern among high-risk users
3. Engagement score distribution histogram summary

All insights are stored as structured JSON in memory (not DB). Regenerated on each call to `/api/v1/insights`.

---

## 11. Frontend (Streamlit)

The dashboard is a multi-page Streamlit app. It imports analytics and ML modules directly — no HTTP calls to FastAPI at runtime. All charts use Plotly via `st.plotly_chart(fig, use_container_width=True)`.

### 11.1 Streamlit Theme (``.streamlit/config.toml``)

This file IS committed (no secrets here — only visual config):

```toml
[theme]
base = "dark"
backgroundColor = "#0a0a0f"
secondaryBackgroundColor = "#111118"
textColor = "#f0f0f8"
primaryColor = "#4f8ef7"
font = "monospace"
```

### 11.2 Page Structure

Streamlit multi-page apps use the `pages/` directory. File names control sidebar order and labels.

| File                          | Sidebar Label     | Icon |
|-------------------------------|-------------------|------|
| `streamlit_app/app.py`        | Overview          | 📊   |
| `pages/1_Retention.py`        | Retention         | 🔁   |
| `pages/2_Funnels.py`          | Funnels           | 🎯   |
| `pages/3_Engagement.py`       | Engagement        | ⚡   |
| `pages/4_Subscriptions.py`    | Subscriptions     | 💳   |
| `pages/5_Intelligence.py`     | Intelligence      | 🧠   |

Each page file must call `st.set_page_config(layout="wide")` as its first Streamlit call.

---

### 11.3 Page Specifications

#### Page 1: Overview (`app.py`)

```python
# Layout
st.title("UserPulse")
st.caption("Product Analytics & Behavioral Intelligence")

# Global date filter — stored in st.session_state
col_from, col_to = st.columns(2)
date_from = col_from.date_input("From", value=30_days_ago)
date_to   = col_to.date_input("To",   value=today)

# KPI row — 6 columns
cols = st.columns(6)
# Each col: cols[i].metric(label, value, delta)
# Metrics: DAU, MAU, DAU/MAU Ratio, Total Users, Churn Rate %, MRR USD

# Charts — 2 columns
left, right = st.columns(2)
left:  Plotly bar chart — daily active users (last 30 days)
right: Plotly line chart — sessions over time

# Insight preview — top 2 insights rendered as st.info() / st.warning() / st.error()
# based on severity: medium=info, high=warning, critical=error
```

---

#### Page 2: Retention (`1_Retention.py`)

```python
cohort_type = st.radio("Cohort", ["Weekly", "Monthly"], horizontal=True)
periods     = st.slider("Periods", min_value=4, max_value=12, value=8)

# Plotly heatmap (go.Heatmap)
# x-axis: period labels ("Week 0", "Week 1", ...)
# y-axis: cohort labels ("2026-W01", ...)
# z: retention values (0–100)
# colorscale: RdYlGn (red → yellow → green)
# text annotations: show value in each cell, gray for null

# Summary below chart:
st.metric("Best Cohort", cohort_name, f"{value}% week-4 retention")
st.metric("Avg Week-1 Retention", f"{avg}%")
```

---

#### Page 3: Funnels (`2_Funnels.py`)

```python
funnel_name = st.selectbox("Funnel", ["onboarding", "subscription", "course_completion"])

# Plotly funnel chart (go.Funnel)
# values: user counts per step
# text: show conversion % and drop-off % on each bar
# highlight the step with largest drop-off in red

# Callout below chart:
st.error(f"⚠ Biggest drop-off: '{step_name}' loses {pct}% of users")
st.metric("Overall Conversion", f"{overall_pct}%")
```

---

#### Page 4: Engagement (`3_Engagement.py`)

```python
col1, col2, col3 = st.columns(3)
date_from    = col1.date_input("From")
date_to      = col2.date_input("To")
granularity  = col3.radio("Granularity", ["daily", "weekly"], horizontal=True)

# Plotly multi-line chart (go.Figure with multiple go.Scatter traces)
# Traces: Active Users, Sessions, Lessons Completed
# All on same x-axis (date)

# Stats row below chart
c1, c2, c3 = st.columns(3)
c1.metric("Avg Session Duration", f"{mins}m {secs}s")
c2.metric("Total Events", f"{count:,}")
c3.metric("Quizzes Submitted", f"{count:,}")
```

---

#### Page 5: Subscriptions (`4_Subscriptions.py`)

```python
# KPI row — 4 metrics
st.metric("Active Subscriptions", ...)
st.metric("New This Period", ...)
st.metric("Cancellations", ...)
st.metric("MRR (USD)", f"${mrr:,.0f}")

# Two charts side by side
left, right = st.columns(2)

left:  Plotly donut chart (go.Pie, hole=0.5) — Annual vs Monthly split
right: Plotly horizontal bar chart — top cancellation reasons (sorted descending)

# Churn gauge below
# go.Indicator with mode="gauge+number"
# gauge range: 0–20%
# threshold colors: green <5%, amber 5–10%, red >10%
```

---

#### Page 6: Intelligence (`5_Intelligence.py`)

```python
st.button("🔄 Refresh Insights")  # re-runs insight_generator

# Render insights in 2-column grid
# For each insight:
#   severity → st.error (critical), st.warning (high), st.info (medium)
#   Inside each: title in bold, body text, metric badge, source tag
#   Source: "🔬 Rule-Based" or "🤖 ML Model"

# Example render:
with st.error(""):          # critical severity
    st.markdown(f"**{insight['title']}**")
    st.write(insight['body'])
    col1, col2 = st.columns(2)
    col1.caption(f"Metric: {insight['metric_value']} {insight['metric_unit']}")
    col2.caption(f"Source: {'🤖 ML Model' if insight['source'] == 'ml_model' else '🔬 Rule-Based'}")
```

---

### 11.4 Shared Component Functions (`streamlit_app/components/`)

Each file exports a single function called by page files:

| File                   | Function Signature                                      |
|------------------------|---------------------------------------------------------|
| `kpi_cards.py`         | `render_kpi_row(kpis: dict, columns: list[st.delta_generator])` |
| `retention_heatmap.py` | `render_heatmap(data: dict) -> go.Figure`              |
| `funnel_chart.py`      | `render_funnel(data: dict) -> go.Figure`               |
| `engagement_chart.py`  | `render_engagement(data: dict) -> go.Figure`           |
| `churn_gauge.py`       | `render_gauge(churn_rate: float) -> go.Figure`         |
| `insight_card.py`      | `render_insight(insight: dict)`                        |

---

### 11.5 Data Flow in Streamlit Pages

Pages import analytics functions directly — no HTTP:

```python
# Example in 1_Retention.py
import sys
sys.path.append("../")           # makes root modules importable

from analytics.retention import compute_cohort_retention
from streamlit_app.components.retention_heatmap import render_heatmap

data = compute_cohort_retention(cohort_type="weekly", periods=8)
fig  = render_heatmap(data)
st.plotly_chart(fig, use_container_width=True)
```

`@st.cache_data(ttl=300)` must be applied to all analytics functions to avoid re-querying the DB on every widget interaction. TTL = 300 seconds (5 minutes).

---

## 12. Secrets & Environment Variable Management

### 12.1 The Problem
The repo is public on GitHub. No real credentials must ever be committed.

### 12.2 `.gitignore` — Must Include These Entries

Antigravity must create this `.gitignore` at the repo root:

```gitignore
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
```

### 12.3 `.env.example` — Safe Placeholder (Committed to Repo)

This file is committed. It shows the shape of secrets without real values:

```env
# Copy this file to .env and fill in real values
# NEVER commit .env itself

DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=replace-with-a-random-hex-string
ENVIRONMENT=development
```

### 12.4 Local Development — `.env` (Not Committed)

Developer copies `.env.example` → `.env` and fills in the real `DATABASE_URL` from their cloud PostgreSQL provider dashboard.

```env
DATABASE_URL=postgresql://userpulse:actualpassword@ep-xxxx.us-east-1.aws.neon.tech/userpulse?sslmode=require
SECRET_KEY=aef92c1d...
ENVIRONMENT=development
```

The `database.py` module reads this using `python-dotenv`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 12.5 Streamlit Cloud Deployment — `st.secrets`

On Streamlit Cloud, secrets are set in the dashboard UI (Settings → Secrets), NOT in any file. Streamlit Cloud injects them as `st.secrets`.

The file `.streamlit/secrets.toml` is used **only for local Streamlit testing**. It must be in `.gitignore`.

```toml
# .streamlit/secrets.toml — LOCAL ONLY, never committed
DATABASE_URL = "postgresql://userpulse:actualpassword@host/userpulse?sslmode=require"
```

`database.py` must support both local and Streamlit Cloud by checking both sources:

```python
import os
import streamlit as st
from dotenv import load_dotenv

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
```

### 12.6 What the Developer Must Do Manually (One Time)

1. Get the `DATABASE_URL` connection string from their cloud PostgreSQL provider dashboard (Neon / Supabase / Railway)
2. Create `.env` locally and paste it in
3. Create `.streamlit/secrets.toml` locally and paste it in for local Streamlit testing
4. In Streamlit Cloud dashboard → Settings → Secrets, paste `DATABASE_URL = "..."` in the secrets editor

That is the only manual credential step. Nothing else requires a key or token.

---

## 13. Local Development Setup

No Docker. No local PostgreSQL. The database runs in the cloud — you only need Python.

### Prerequisites

| Tool    | Version | Purpose                    |
|---------|---------|----------------------------|
| Python  | 3.11+   | Everything                 |
| pip     | latest  | Package management         |
| git     | latest  | Version control            |

Node.js is NOT required. There is no JavaScript in this project.

### Step 1 — Clone & Install

```bash
git clone https://github.com/your-username/userpulse.git
cd userpulse
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Configure Secrets

```bash
cp .env.example .env
# Open .env and paste your DATABASE_URL from your cloud PostgreSQL dashboard
# It looks like: postgresql://user:pass@host/dbname?sslmode=require
```

Also create the local Streamlit secrets file:

```bash
mkdir -p .streamlit
# Create .streamlit/secrets.toml with:
# DATABASE_URL = "postgresql://user:pass@host/dbname?sslmode=require"
```

### Step 3 — Run Database Migrations

```bash
alembic upgrade head
# Verify: all 7 tables created in your cloud PostgreSQL
```

### Step 4 — Seed the Database

```bash
python simulation/seed.py
# Expected: "Seeded 50,000 users | X sessions | ~6,000,000 events"
# This takes 5–15 minutes depending on connection speed
```

### Step 5 — Train the ML Model

```bash
python ml/train.py
# Expected output: F1 score >= 0.75
# Saves: ml/churn_model.pkl (gitignored)
```

### Step 6 — Run the Streamlit App

```bash
streamlit run streamlit_app/app.py
# Dashboard at http://localhost:8501
```

### Step 7 — Run FastAPI (Optional, for API docs)

```bash
uvicorn backend.main:app --port 8000 --reload
# API docs at http://localhost:8000/docs
```

### `requirements.txt` (Single Unified File)

```
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
```

---

## 14. Build Order for Antigravity

Execute in this exact order. Do not move to the next step until the current one is verified.

1. **Scaffold** — create full repo directory structure with all folders and placeholder files. Create `.gitignore`, `.env.example`, `.streamlit/config.toml`
2. **Database** — write all SQLAlchemy models, configure `database.py` with `get_database_url()` (reads from both `.env` and `st.secrets`), run `alembic upgrade head` against cloud PostgreSQL, verify all 7 tables exist
3. **Simulation** — implement `personas.py`, `event_generator.py`, `seed.py`. Run seed. Verify row counts: ~50,000 users, ~6,000,000 events in cloud DB
4. **Analytics engine** — implement all 5 functions in `analytics/`. Add `@st.cache_data(ttl=300)` decorator to each. Unit test each function with a direct Python call before wiring to UI
5. **ML engine** — implement `engagement_scorer.py`, run `ml/train.py` (verify F1 ≥ 0.75), implement `insight_generator.py`. Verify `ml/churn_model.pkl` is in `.gitignore`
6. **FastAPI backend** — implement all routers in `backend/`. These call the same `analytics/` and `ml/` functions. Test via `/docs` swagger UI
7. **Streamlit app** — implement `app.py` + all 5 pages + all 6 component functions. Test each page locally with `streamlit run streamlit_app/app.py`
8. **Integration check** — verify: every chart renders with real data, `@st.cache_data` working, date filters update charts, no hardcoded values
9. **Streamlit Cloud deploy** — push to GitHub, connect repo in Streamlit Cloud dashboard, add `DATABASE_URL` in Streamlit Cloud Secrets editor, verify live URL works
10. **README** — write `README.md` as defined in Section 16

---

## 15. Success Criteria

The project is complete when all of the following pass:

- [ ] Cloud PostgreSQL has all 7 tables with correct schema
- [ ] `.gitignore` covers `.env`, `.streamlit/secrets.toml`, `*.pkl`
- [ ] `.env.example` is committed with placeholder values only
- [ ] Seeded database has ~50,000 users with realistic persona-driven event distributions
- [ ] `analytics/kpis.py` returns all 9 fields with non-zero values (direct Python call)
- [ ] `analytics/retention.py` returns a matrix with at least 6 cohorts
- [ ] `analytics/funnels.py` for `onboarding` returns 5 steps with correct drop-offs
- [ ] `ml/train.py` reports F1 score ≥ 0.75 on test split
- [ ] `insight_generator.py` returns minimum 4 insights (2 rule-based, 2 ML-derived)
- [ ] All 6 Streamlit pages render without Python exceptions
- [ ] Retention heatmap (Plotly) shows RdYlGn color gradient
- [ ] Funnel chart (Plotly go.Funnel) shows drop-off percentages between steps
- [ ] Churn gauge changes color at correct thresholds (green/amber/red)
- [ ] Date filters on Overview and Engagement pages cause data to re-fetch
- [ ] `@st.cache_data(ttl=300)` applied to all analytics functions
- [ ] No hardcoded data anywhere — all values from analytics functions
- [ ] App deploys on Streamlit Cloud and loads from cloud PostgreSQL
- [ ] `README.md` exists and matches Section 16

---

## 16. README Specification

Antigravity must write `README.md` at the repo root. It must contain exactly these sections in this order:

### 16.1 Header
- Project name: **UserPulse**
- One-line description: *"A full-stack product analytics and behavioral intelligence platform built to demonstrate event-driven architecture, analytics engineering, and ML-powered insights."*
- Badges: Python 3.11+, FastAPI, Next.js 14, PostgreSQL, scikit-learn (use shields.io static badges)

### 16.2 Overview
3–4 sentences explaining what UserPulse is, what problem it solves, and that LearnSphere is the fictional event source powering it. No bullet points — prose only.

### 16.3 Architecture Diagram
Reproduce the ASCII architecture diagram from Section 2 of this spec inside a code block.

### 16.4 Tech Stack
Reproduce the tech stack table from Section 4.

### 16.5 Features
Bullet list of exactly these 8 features:
- Event ingestion API with batch support (up to 500 events/call)
- Cohort retention analysis (weekly & monthly heatmaps)
- Multi-step conversion funnel analysis (3 predefined funnels)
- Daily/weekly engagement time series
- Churn analytics broken down by persona and lesson
- Subscription MRR tracking and cancellation reason analysis
- ML-powered churn prediction (Random Forest, F1 ≥ 0.75)
- Behavioral insight generation (rule-based + ML-derived)

### 16.6 Setup & Running
Reproduce the full local setup steps from Section 13, formatted clearly with code blocks. Include a note that DATABASE_URL comes from the cloud PostgreSQL provider dashboard — no local DB needed.

### 16.7 Streamlit Cloud Deployment
Short section explaining:
1. Push repo to GitHub
2. Connect at share.streamlit.io
3. Set `DATABASE_URL` in Streamlit Cloud Secrets editor (Settings → Secrets)
4. App is live — no server management needed

### 16.8 API Reference
Table of all API endpoints with method, path, and one-line description. Derive from Section 7. Note that FastAPI is optional/local-only in this deployment.

### 16.9 Project Structure
Reproduce the repo tree from Section 3.

### 16.10 ML Models
Short section (4–6 sentences) explaining the churn prediction model: algorithm, features used, output, and how insights are derived from it.

### 16.11 Data Simulation
3–4 sentences explaining the LearnSphere simulation layer, the 4 personas, and how they generate realistic behavioral patterns.

### 16.12 Portfolio Note
One short paragraph: *"This project was built as a portfolio piece to demonstrate full-stack engineering, analytics engineering, and applied ML. It is not connected to any real user data. All behavioral data is synthetically generated using realistic persona-based simulation."*

---

*End of specification. Version 1.2 — May 2026.*

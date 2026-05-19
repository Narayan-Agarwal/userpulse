from fastapi import FastAPI
from backend.routers import analytics, insights

app = FastAPI(title="UserPulse API")

app.include_router(analytics.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "ok"}

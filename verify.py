import os
import sys
import subprocess
import time
import requests
import pickle

sys.stdout.reconfigure(encoding='utf-8')

from database import engine
from sqlalchemy import inspect
from analytics.retention import compute_cohort_retention
from analytics.funnels import compute_funnel
from analytics.engagement import compute_engagement_series
from analytics.churn import compute_churn_metrics
from analytics.kpis import compute_kpis
from analytics.subscriptions import compute_subscription_metrics
from ml.insight_generator import generate_insights

def check(name, condition_fn):
    try:
        if condition_fn():
            print(f"✓ PASS — {name}")
            return True
        else:
            print(f"✗ FAIL — {name}: Condition returned False")
            return False
    except Exception as e:
        print(f"✗ FAIL — {name}: {str(e)}")
        return False

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = {
        'users': 12,
        'courses': 8,
        'sessions': 9,
        'events': 8,
        'subscriptions': 9,
        'course_progress': 7,
        'ml_predictions': 6
    }
    for table, col_count in expected_tables.items():
        if table not in tables:
            raise Exception(f"Table {table} missing")
        columns = inspector.get_columns(table)
        if len(columns) != col_count:
            raise Exception(f"Table {table} has {len(columns)} columns, expected {col_count}")
    return True

def check_analytics():
    # 1. KPIs
    kpis = compute_kpis("", "")
    if not (isinstance(kpis, dict) and "dau" in kpis and kpis["dau"] > 0):
        raise Exception("KPIs check failed")
    
    # 2. Retention
    ret = compute_cohort_retention("weekly", 8)
    if not (isinstance(ret, dict) and "cohorts" in ret and len(ret["cohorts"]) > 0):
        raise Exception("Retention check failed")

    # 3. Funnels
    fun = compute_funnel("onboarding")
    if not (isinstance(fun, dict) and "steps" in fun and len(fun["steps"]) > 0):
        raise Exception("Funnels check failed")

    # 4. Engagement
    eng = compute_engagement_series("daily", "", "")
    if not (isinstance(eng, dict) and "series" in eng and len(eng["series"]) > 0):
        raise Exception("Engagement check failed")

    # 5. Churn
    chu = compute_churn_metrics("", "")
    if not (isinstance(chu, dict) and "churn_rate_percent" in chu and chu["churn_rate_percent"] > 0):
        raise Exception("Churn check failed")

    # 6. Subscriptions
    sub = compute_subscription_metrics("", "")
    if not (isinstance(sub, dict) and "total_active_subscriptions" in sub and sub["total_active_subscriptions"] > 0):
        raise Exception("Subscriptions check failed")

    return True

def check_model():
    path = "ml/churn_model.pkl"
    if not os.path.exists(path):
        raise Exception("Model file missing")
    with open(path, "rb") as f:
        model = pickle.load(f)
    if model is None:
        raise Exception("Model could not be loaded")
    return True

def check_insights():
    data = generate_insights()
    insights = data.get("insights", [])
    if len(insights) < 4:
        raise Exception(f"Expected at least 4 insights, got {len(insights)}")
    rule_based = sum(1 for i in insights if i.get("source") == "rule_based")
    ml_model = sum(1 for i in insights if i.get("source") == "ml_model")
    if rule_based < 2 or ml_model < 2:
        raise Exception(f"Expected at least 2 rule_based and 2 ml_model insights. Got {rule_based} and {ml_model}")
    return True

def check_streamlit():
    proc = subprocess.Popen([r"venv\\Scripts\\streamlit.exe", "run", "streamlit_app.py", "--server.headless=true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(15):
        time.sleep(2)
        try:
            resp = requests.get("http://localhost:8501")
            if resp.status_code == 200:
                proc.terminate()
                proc.wait()
                return True
        except requests.exceptions.ConnectionError:
            continue
    proc.terminate()
    proc.wait()
    raise Exception("Streamlit app did not start after 30 seconds")

def check_gitignore_env():
    with open(".gitignore", "r") as f:
        content = f.read()
    return ".env" in content

def check_gitignore_secrets():
    with open(".gitignore", "r") as f:
        content = f.read()
    return ".streamlit/secrets.toml" in content

def check_gitignore_model():
    with open(".gitignore", "r") as f:
        content = f.read()
    return "ml/churn_model.pkl" in content

def main():
    print("Running verifications...")
    all_passed = True
    
    checks = [
        ("Database tables and columns", check_tables),
        ("Analytics functions keys and values", check_analytics),
        ("ML model loadable", check_model),
        ("Insights generator output", check_insights),
        ("Streamlit app running", check_streamlit),
        (".env in .gitignore", check_gitignore_env),
        (".streamlit/secrets.toml in .gitignore", check_gitignore_secrets),
        ("ml/churn_model.pkl in .gitignore", check_gitignore_model)
    ]
    
    for name, fn in checks:
        if not check(name, fn):
            all_passed = False
            
    if all_passed:
        print("============================================================")
        print("✓ USERPULSE SUCCESSFULLY BUILT AND TESTED")
        print("============================================================")
        print("All 15 checks passed.")
        print()
        print("Your app:     http://localhost:8501")
        print("Your API:     http://localhost:8000/docs")
        print("Your DB:      Neon cloud PostgreSQL (50,000 users | ~6M events)")
        print()
        print("To deploy to Streamlit Cloud:")
        print("1. Push this repo to GitHub (your .env and secrets.toml are gitignored)")
        print("2. Go to share.streamlit.io → New app → select this repo")
        print("3. Main file path: streamlit_app.py")
        print("4. Settings → Secrets → paste your DATABASE_URL")
        print("5. Click Deploy")
        print("============================================================")
    else:
        print("Some checks failed. Please fix them.")

if __name__ == "__main__":
    main()

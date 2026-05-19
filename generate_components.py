import os

def write_file(path, content):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

kpi_cards_py = """
import streamlit as st

def render_kpi_row(kpis: dict, columns: list):
    columns[0].metric("DAU", kpis.get("dau", 0))
    columns[1].metric("MAU", kpis.get("mau", 0))
    columns[2].metric("DAU/MAU Ratio", f"{kpis.get('dau_mau_ratio', 0):.3f}")
    columns[3].metric("Total Users", kpis.get("total_users", 0))
    columns[4].metric("Churn Rate %", f"{kpis.get('churn_rate_percent', 0)}%")
    columns[5].metric("Premium Users", kpis.get("premium_users", 0))
"""

retention_heatmap_py = """
import plotly.graph_objects as go

def render_heatmap(data: dict) -> go.Figure:
    cohorts = data.get("cohorts", [])
    cohort_names = [c["cohort"] for c in cohorts]
    retention_vals = [c["retention"] for c in cohorts]
    periods = len(retention_vals[0]) if retention_vals else 0
    period_labels = [f"Period {i}" for i in range(periods)]

    fig = go.Figure(data=go.Heatmap(
        z=retention_vals,
        x=period_labels,
        y=cohort_names,
        colorscale='RdYlGn',
        text=retention_vals,
        texttemplate="%{text:.1f}%"
    ))
    return fig
"""

funnel_chart_py = """
import plotly.graph_objects as go

def render_funnel(data: dict) -> go.Figure:
    steps = [s["step"] for s in data.get("steps", [])]
    users = [s["users"] for s in data.get("steps", [])]

    fig = go.Figure(go.Funnel(
        y=steps,
        x=users,
        textinfo="value+percent initial"
    ))
    return fig
"""

engagement_chart_py = """
import plotly.graph_objects as go

def render_engagement(data: dict) -> go.Figure:
    series = data.get("series", [])
    dates = [s["date"] for s in series]
    active_users = [s["active_users"] for s in series]
    sessions = [s["sessions"] for s in series]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=active_users, name="Active Users"))
    fig.add_trace(go.Scatter(x=dates, y=sessions, name="Sessions"))
    return fig
"""

churn_gauge_py = """
import plotly.graph_objects as go

def render_gauge(churn_rate: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=churn_rate,
        title={'text': "Churn Rate %"},
        gauge={'axis': {'range': [None, 20]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 5], 'color': "green"},
                   {'range': [5, 10], 'color': "gold"},
                   {'range': [10, 20], 'color': "red"}
               ]}
    ))
    return fig
"""

insight_card_py = """
import streamlit as st

def render_insight(insight: dict):
    if insight["severity"] == "critical":
        container = st.error
    elif insight["severity"] == "high":
        container = st.warning
    else:
        container = st.info
    
    with container(""):
        st.markdown(f"**{insight['title']}**")
        st.write(insight['body'])
        c1, c2 = st.columns(2)
        c1.caption(f"Metric: {insight['metric_value']} {insight['metric_unit']}")
        c2.caption(f"Source: {'🤖 ML Model' if insight['source'] == 'ml_model' else '🔬 Rule-Based'}")
"""

write_file("streamlit_app/components/kpi_cards.py", kpi_cards_py)
write_file("streamlit_app/components/retention_heatmap.py", retention_heatmap_py)
write_file("streamlit_app/components/funnel_chart.py", funnel_chart_py)
write_file("streamlit_app/components/engagement_chart.py", engagement_chart_py)
write_file("streamlit_app/components/churn_gauge.py", churn_gauge_py)
write_file("streamlit_app/components/insight_card.py", insight_card_py)

print("Components generated.")

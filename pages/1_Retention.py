import streamlit as st
import sys
import os
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analytics.retention import compute_cohort_retention

st.set_page_config(layout="wide", page_title="Retention", page_icon="🔁")
st.title("Retention Analysis")

cohort_type = st.radio("Cohort", ["Weekly", "Monthly"], horizontal=True)
periods = st.slider("Periods", min_value=4, max_value=12, value=8)

data = compute_cohort_retention(cohort_type.lower(), periods)

cohort_names = [c["cohort"] for c in data["cohorts"]]
retention_vals = [c["retention"] for c in data["cohorts"]]
period_labels = [f"Period {i}" for i in range(periods)]

fig = go.Figure(data=go.Heatmap(
    z=retention_vals,
    x=period_labels,
    y=cohort_names,
    colorscale='RdYlGn',
    text=retention_vals,
    texttemplate="%{text:.1f}%"
))

st.plotly_chart(fig, use_container_width=True)
st.metric("Best Cohort", cohort_names[0] if cohort_names else "N/A")

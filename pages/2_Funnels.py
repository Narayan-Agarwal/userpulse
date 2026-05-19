import streamlit as st
import sys
import os
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analytics.funnels import compute_funnel

st.set_page_config(layout="wide", page_title="Funnels", page_icon="🎯")
st.title("Funnel Analysis")

funnel_name = st.selectbox("Funnel", ["onboarding", "subscription", "course_completion"])
data = compute_funnel(funnel_name)

steps = [s["step"] for s in data.get("steps", [])]
users = [s["users"] for s in data.get("steps", [])]

fig = go.Figure(go.Funnel(
    y=steps,
    x=users,
    textinfo="value+percent initial"
))

st.plotly_chart(fig, use_container_width=True)
st.metric("Overall Conversion", f"{data.get('overall_conversion_pct', 0)}%")

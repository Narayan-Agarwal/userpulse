import streamlit as st
import sys
import os
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analytics.engagement import compute_engagement_series

st.set_page_config(layout="wide", page_title="Engagement", page_icon="⚡")
st.title("Engagement Analysis")

col1, col2, col3 = st.columns(3)
date_from = col1.date_input("From")
date_to = col2.date_input("To")
granularity = col3.radio("Granularity", ["daily", "weekly"], horizontal=True)

data = compute_engagement_series(granularity, str(date_from), str(date_to))
series = data.get("series", [])

if series:
    dates = [s["date"] for s in series]
    active_users = [s["active_users"] for s in series]
    sessions = [s["sessions"] for s in series]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=active_users, name="Active Users"))
    fig.add_trace(go.Scatter(x=dates, y=sessions, name="Sessions"))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available.")

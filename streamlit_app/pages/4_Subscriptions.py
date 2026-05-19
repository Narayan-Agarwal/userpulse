import streamlit as st
import sys
import os
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from analytics.subscriptions import compute_subscription_metrics
from analytics.churn import compute_churn_metrics

st.set_page_config(layout="wide", page_title="Subscriptions", page_icon="💳")
st.title("Subscriptions & Churn")

subs = compute_subscription_metrics("", "")
churn = compute_churn_metrics("", "")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Active Subscriptions", subs["total_active_subscriptions"])
c2.metric("New This Period", subs["new_subscriptions_period"])
c3.metric("Cancellations", subs["cancellations_period"])
c4.metric("MRR (USD)", f"${subs['mrr_usd']:,.0f}")

left, right = st.columns(2)
# Doughnut chart
annual = subs["annual_vs_monthly_split"]["annual"]
monthly = subs["annual_vs_monthly_split"]["monthly"]
fig1 = go.Figure(data=[go.Pie(labels=["Annual", "Monthly"], values=[annual, monthly], hole=0.5)])
left.plotly_chart(fig1, use_container_width=True)

# Churn Gauge
churn_rate = churn["churn_rate_percent"]
fig2 = go.Figure(go.Indicator(
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
right.plotly_chart(fig2, use_container_width=True)

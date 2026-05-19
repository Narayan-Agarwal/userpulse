import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analytics.kpis import compute_kpis

st.set_page_config(layout="wide", page_title="UserPulse Overview", page_icon="📊")

st.title("UserPulse")
st.caption("Product Analytics & Behavioral Intelligence")

col_from, col_to = st.columns(2)
date_from = col_from.date_input("From")
date_to   = col_to.date_input("To")

kpis = compute_kpis(str(date_from), str(date_to))

cols = st.columns(6)
cols[0].metric("DAU", kpis['dau'])
cols[1].metric("MAU", kpis['mau'])
cols[2].metric("DAU/MAU Ratio", f"{kpis['dau_mau_ratio']:.3f}")
cols[3].metric("Total Users", kpis['total_users'])
cols[4].metric("Churn Rate %", f"{kpis['churn_rate_percent']}%")
cols[5].metric("Premium Users", kpis['premium_users'])

st.info("💡 **Tip**: Use the sidebar to navigate to detailed reports.")

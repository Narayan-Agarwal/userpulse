import streamlit as st

def render_kpi_row(kpis: dict, columns: list):
    columns[0].metric("DAU", kpis.get("dau", 0))
    columns[1].metric("MAU", kpis.get("mau", 0))
    columns[2].metric("DAU/MAU Ratio", f"{kpis.get('dau_mau_ratio', 0):.3f}")
    columns[3].metric("Total Users", kpis.get("total_users", 0))
    columns[4].metric("Churn Rate %", f"{kpis.get('churn_rate_percent', 0)}%")
    columns[5].metric("Premium Users", kpis.get("premium_users", 0))

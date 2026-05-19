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

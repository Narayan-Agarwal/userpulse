import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ml.insight_generator import generate_insights

st.set_page_config(layout="wide", page_title="Intelligence", page_icon="🧠")
st.title("Behavioral Intelligence Insights")

if st.button("🔄 Refresh Insights"):
    generate_insights.clear()

data = generate_insights()

cols = st.columns(2)
for i, insight in enumerate(data.get("insights", [])):
    col = cols[i % 2]
    with col:
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

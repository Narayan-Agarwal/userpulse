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

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

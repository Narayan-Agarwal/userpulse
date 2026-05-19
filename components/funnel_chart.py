import plotly.graph_objects as go

def render_funnel(data: dict) -> go.Figure:
    steps = [s["step"] for s in data.get("steps", [])]
    users = [s["users"] for s in data.get("steps", [])]

    fig = go.Figure(go.Funnel(
        y=steps,
        x=users,
        textinfo="value+percent initial"
    ))
    return fig

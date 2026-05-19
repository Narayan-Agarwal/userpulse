import plotly.graph_objects as go

def render_engagement(data: dict) -> go.Figure:
    series = data.get("series", [])
    dates = [s["date"] for s in series]
    active_users = [s["active_users"] for s in series]
    sessions = [s["sessions"] for s in series]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=active_users, name="Active Users"))
    fig.add_trace(go.Scatter(x=dates, y=sessions, name="Sessions"))
    return fig

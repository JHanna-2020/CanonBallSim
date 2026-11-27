import math
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go
from sim_cpp import sim_engine
import random

V0_SIGMA = 1.0
THETA_SIGMA_DEG = 0.5
PHI_SIGMA_DEG = 1.0 
_rng = random.Random(42)
V0_MIN = 0.1
THETA_MIN_DEG = 1.0
THETA_MAX_DEG = 89.0
def run_batch(v0: float, theta_deg, phi_deg, num_balls):
    if num_balls == 1:
        return[run(v0, theta_deg, phi_deg)]
    else:
        batch = []
        for _ in range(num_balls):
            v0_i = _rng.gauss(v0, V0_SIGMA)
            theta_i = _rng.gauss(theta_deg, THETA_SIGMA_DEG)
            phi_i = _rng.gauss(phi_deg, PHI_SIGMA_DEG)
            v0_i = max(V0_MIN, v0_i)
            theta_i = max(THETA_MIN_DEG, min(theta_i, THETA_MAX_DEG))
            batch.append([v0_i, math.radians(theta_i), math.radians(phi_i)])
        return sim_engine.run_multiple_simulations(batch)

def run(v0: float, theta_deg: float, phi_deg: float) -> list[list[float]]:
    theta_rad = math.radians(theta_deg)
    phi_rad = math.radians(phi_deg)
    return sim_engine.run_simulation([v0, theta_rad, phi_rad])


app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "sans-serif", "maxWidth": "1000px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H2("3D Cannonball Simulation"),
        html.Label("Initial Velocity (m/s)"),
        dcc.Slider(id="v0-slider", min=5, max=150, step=1, value=50, marks={5: "5", 50: "50", 100: "100", 150: "150"}),
        html.Label("Launch Angle Theta (deg)"),
        dcc.Slider(id="theta-slider", min=1, max=89, step=1, value=45, marks={1: "1°", 45: "45°", 89: "89°"}),
        html.Label("Azimuth Angle Phi (deg)"),
        dcc.Slider(id="phi-slider", min=0, max=360, step=5, value=30, marks={0: "0°", 90: "90°", 180: "180°", 270: "270°", 360: "360°"}),
        html.Label("Number of Balls"),
        dcc.Slider(id="balls-slider", min=1, max=30, step=1, value=1, marks={1: "1", 10: "10", 20: "20", 30: "30"}),
        html.Div(id="impact-summary", style={"marginTop": "16px", "fontWeight": "bold"}),
        dcc.Graph(id="trajectory-plot", style={"height": "650px"}),
    ],
)


@app.callback(
    Output("trajectory-plot", "figure"),
    Output("impact-summary", "children"),
    Input("v0-slider", "value"),
    Input("theta-slider", "value"),
    Input("phi-slider", "value"),
    Input("balls-slider", "value")
)
def update_simulation(v0: float, theta_deg: float, phi_deg: float, num_balls : int):
    trajectories = run_batch(v0, theta_deg, phi_deg, num_balls)
    traces = []
    for trajectory in trajectories:
        xs = [s[0] for s in trajectory]
        ys = [s[1] for s in trajectory]
        zs = [s[2] for s in trajectory]
        traces.append(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(width=3), showlegend=False))
    fig = go.Figure(data=traces)
    fig.update_layout(
        scene=dict(
            xaxis_title="X Distance (m)",
            yaxis_title="Y Distance (m)",
            zaxis_title="Z Height (m)",
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=20, b=0),
    )

    # summary = f"Steps: {len(trajectory)} | Impact: ({impact[0]:.2f} m, {impact[1]:.2f} m, {impact[2]:.2f} m)"
    summary = f"Balls: {len(trajectories)}"
    return fig, summary

if __name__ == "__main__":
    app.run(debug=False)

import os, json
import pandas as pd
import numpy as np
from itertools import product
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go

# -----------------------------
# User inputs
# -----------------------------
header_path = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
CSV_MAPS_folder = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
input_json = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"

# -----------------------------
# Load configuration
# -----------------------------
with open(input_json) as f:
    config = json.load(f)

sweep_vars = {k: eval(v) for k, v in config.items() if "X" in k}
sweepNames = config["sweepNames"]

mat_names = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages"]
headers_lists = [json.load(open(os.path.join(header_path, f"{name}.json"))) for name in mat_names]
headers_array = sum(headers_lists, [])

mat_lists = [pd.read_csv(os.path.join(CSV_MAPS_folder, f"{name}_Map.csv"), header=None).values for name in mat_names]
combined_matrix = np.hstack(mat_lists)

# -----------------------------
# Build figures
# -----------------------------
figures = {}
for idx, component in enumerate(headers_array):
    z_vals = combined_matrix[:, idx]
    x_vals = np.arange(len(z_vals))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=z_vals, mode="lines+markers",
        name=component, selected=dict(marker=dict(color="red", size=12)),
        unselected=dict(marker=dict(color="blue", size=6))
    ))
    fig.update_layout(title=component)
    figures[component] = fig

# -----------------------------
# Dash app
# -----------------------------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Plots"),
    dcc.Dropdown(
        id="figure-dropdown",
        options=[{"label": k, "value": k} for k in figures.keys()],
        value=list(figures.keys())[0]
    ),
dcc.Graph(
    id="figure-graph",
    config={
        "editable": True,          # allows editing annotations etc.
        "displayModeBar": True,    # shows the mode bar
        "modeBarButtonsToAdd": ["select2d", "lasso2d"],  # enable box & lasso select
    }
),

    html.Button("Export Selected to HTML", id="export-btn"),
    html.Div(id="export-msg")
])

@app.callback(
    Output("figure-graph", "figure"),
    Input("figure-dropdown", "value")
)
def update_graph(selected_fig):
    return figures[selected_fig]

@app.callback(
    Output("export-msg", "children"),
    Input("export-btn", "n_clicks"),
    State("figure-dropdown", "value"),
    prevent_initial_call=True
)
def export_html(n, selected_fig):
    filename = f"{selected_fig}_export.html"
    figures[selected_fig].write_html(filename)
    return f"Figure saved as {filename}"

if __name__ == "__main__":
    app.run(debug=True)

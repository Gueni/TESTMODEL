

import os
import re
import dash
import json
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from itertools import product, zip_longest
from dash import dcc, html, Input, Output, State, callback_context

# Initialize the Dash app
app         = dash.Dash(__name__)
server      = app.server 


def load_config():
    """Load configuration from environment variables and JSON file"""

    # Get paths from environment variables
    header_path                 = os.environ.get('DASH_HEADER_PATH', r"")
    csv_maps_folder             = os.environ.get('DASH_CSV_MAPS', r"")
    input_json_path             = os.environ.get('DASH_INPUT_JSON', r"")
    port                        = int(os.environ.get('DASH_PORT', '8050'))
    
    # Load additional configuration from JSON file
    try:
        with open(input_json_path, 'r') as f:
            json_config     = json.load(f)
        
        # Extract configuration from JSON with fallbacks
        permute             = json_config.get('permute', True)
        harmonics           = json_config.get('harmonics', [])
        Y_Lengths           = json_config.get('Y_Lengths', [])
        
    except Exception as e:
        print(f"Error loading JSON config: {e}, using defaults")
    
    return {
        'header_path'       : header_path       ,
        'csv_maps_folder'   : csv_maps_folder   ,
        'input_json'        : input_json_path   ,
        'Y_Lengths'         : Y_Lengths         ,
        'permute'           : permute           ,
        'harmonics'         : harmonics         ,
        'port'              : port
    }

# Load configuration
config_data         = load_config()

# Assign to your original variables
header_path         = config_data['header_path']
CSV_MAPS_folder     = config_data['csv_maps_folder']
input_json          = config_data['input_json']
Y_Lengths           = config_data['Y_Lengths']
permute             = config_data['permute']
harmonics           = config_data['harmonics']

def load_config_and_data():
    """Load configuration and matrix data"""
    with open(input_json) as f:
        config      = json.load(f)
    
    # Load headers and matrices
    mat_names       = ["Peak_Currents", "RMS_Currents", "AVG_Currents", "Peak_Voltages", "RMS_Voltages", "AVG_Voltages", "FFT_Current", "FFT_Voltage", "Dissipations", "Elec_Stats", "Temps", "Thermal_Stats"]
    
    headers_lists   = []
    for name in mat_names:
        file_path   = os.path.join(header_path, f"{name}.json")
        with open(file_path) as f:
            data    = json.load(f)
        headers_lists.append(data if isinstance(data, list) else [data])
    
    cumsum              = np.cumsum(Y_Lengths[1:]).tolist()
    all_headers         = sum(headers_lists, [])
    fft_start, fft_end  = cumsum[5], cumsum[7]
    FFT_headers         = list(map(lambda h: f"{h}_FFT", all_headers[fft_start:fft_end]))
    headers_array       = all_headers[:fft_start] + all_headers[fft_end:]

    # Load matrices
    mat_lists       = []
    for name in mat_names:
        file_path   = os.path.join(CSV_MAPS_folder, f"{name}_Map.csv")
        df          = pd.read_csv(file_path, header=None)
        mat_lists.append(df.values)

    combined_matrix         = np.hstack(mat_lists[:6] + mat_lists[8:])
    combined_fft_matrix     = np.hstack(mat_lists[6:8])

    return config, headers_array, FFT_headers, combined_matrix, combined_fft_matrix, mat_names, headers_lists

# Load initial data
config, headers_array, FFT_headers, combined_matrix, combined_fft_matrix, mat_names, headers_lists = load_config_and_data()

# Determine plot mode based on your original logic
sweep_vars          = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
sweep_keys          = list(sweep_vars.keys())
active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
plot_2D             = len(active_sweep_keys) == 1
single_X_key        = active_sweep_keys[0] if plot_2D else None

# Generate all combinations
all_combos = (list(product(*sweep_vars.values())) if permute else 
              np.where((arr := np.array(list(zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, 
                      [v[-1] for v in sweep_vars.values()], arr).tolist())
fft_combos = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))

# 3D Barchart function (same as your original)
def barchart3D(x_vals, y_vals, z_vals, title, z_title, x_title, y_title,
               colorscale='Viridis', opacity=1):
    fig, ann = go.Figure(), []

    x_vals, y_vals, z_vals = map(lambda arr: np.array(arr, dtype=float),
                                 (x_vals, y_vals, z_vals))

    x_unique = np.unique(x_vals)
    y_unique = np.unique(y_vals)

    dx_base = np.min(np.diff(x_unique)) if len(x_unique) > 1 else 1.0
    dy_base = np.min(np.diff(y_unique)) if len(y_unique) > 1 else 1.0

    nx, ny = len(x_unique), len(y_unique)
    scale_factor = 0.6 / np.sqrt(max(nx, ny))

    dx = dx_base * (0.8 * scale_factor + 0.2)
    dy = dy_base * (0.8 * scale_factor + 0.2)

    dx, dy = max(dx, 1e-6), max(dy, 1e-6)

    for i, z_max in enumerate(z_vals):
        x_cnt, y_cnt = x_vals[i], y_vals[i]
        x_min, x_max = x_cnt - dx/2, x_cnt + dx/2
        y_min, y_max = y_cnt - dy/2, y_cnt + dy/2
        x = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
        y = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
        z = [0, 0, 0, 0, z_max, z_max, z_max, z_max]

        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            alphahull=0,
            intensity=z,
            colorscale=colorscale,
            showscale=False,
            opacity=opacity,
            hoverinfo='skip'
        ))

        fig.add_trace(go.Mesh3d(
            x=[x_min, x_max, x_max, x_min],
            y=[y_min, y_min, y_max, y_max],
            z=[z_max, z_max, z_max, z_max],
            color='rgba(0,0,0,0)',
            opacity=0.01,
            hovertemplate=(
                f"<b>{x_title}</b>: {x_cnt:.2f}<br>"
                f"<b>{y_title}</b>: {y_cnt:.2f}<br>"
                f"<b>{z_title}</b>: {z_max:.2f}<extra></extra>"
            ),
            hoverlabel=dict(
                bgcolor='rgba(30,30,30,0.8)',
                font_color='white',
                bordercolor='white'
            ),
            showlegend=False
        ))

        ann.append(dict(
            showarrow=False,
            x=x_cnt, y=y_cnt, z=z_max,
            text=f'{z_max:.2f}',
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.3)',
            xanchor='center', yanchor='middle'
        ))

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', yanchor='top'),
        scene=dict(
            xaxis=dict(autorange='reversed'),
            yaxis=dict(autorange='reversed'),
            xaxis_title=x_title,
            yaxis_title=y_title,
            zaxis_title=z_title,
            annotations=ann,
            xaxis_title_font=dict(size=10),
            yaxis_title_font=dict(size=10),
            zaxis_title_font=dict(size=10),
            xaxis_tickfont=dict(size=10),
            yaxis_tickfont=dict(size=10),
            zaxis_tickfont=dict(size=10),
        ),
        hoverlabel=dict(
            bgcolor='rgba(50,50,50,0.8)',
            font_color='white',
            bordercolor='white'
        )
    )

    return fig

def format_fixed_title(fixed_dict, sweepNames):
    """Format the fixed title"""
    items = list(fixed_dict.items())
    pattern = re.compile(r'\d+')  # Pre-compile regex
    return "<br>".join(" | ".join(f"{sweepNames[int(pattern.search(k).group())-1]} = {v}" 
                                  for k, v in items[j:j+2]) 
                      for j in range(0, len(items), 2))

def get_fixed_vars():
    """Get fixed variables based on plot mode"""
    if plot_2D:
        # For 2D: all variables except the single sweep variable
        return {k: v for k, v in sweep_vars.items() if k != single_X_key and v != [0]}
    else:
        # For 3D: all variables except Var1 and Var2
        var1, var2 = config["Var1"], config["Var2"]
        sweepNames = config["sweepNames"]
        pattern = re.compile(r'\d+')  # Pre-compile regex
        return {k: v for k, v in sweep_vars.items() 
                if k not in [var1, var2] and v != [0] 
                and not sweepNames[int(pattern.search(k).group())-1].startswith("X")}

# Define the app layout with dynamic mode selection
pattern     = re.compile(r'\d+')  # Pre-compile regex
app.layout  = html.Div([
    html.Div([
        html.H1("PYPLECS DASHBOARD", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
        
        html.Div([
            # Display current mode based on configuration
            html.Div([
                html.H4(f"Current Mode: {'2D' if plot_2D else '3D'} Plotting", 
                       style={'color': '#e74c3c', 'marginBottom': 20}),
                html.P(f"Active Sweep Variables: {len(active_sweep_keys)}", 
                      style={'marginBottom': 10}),
                html.P(f"Sweep Variables: {', '.join([config['sweepNames'][int(pattern.search(str(k)).group())-1] if k and pattern.search(str(k)) else 'Unknown' for k in active_sweep_keys])}",
                      style={'marginBottom': 20}),
            ], style={'backgroundColor': '#fff3cd', 'padding': '15px', 'borderRadius': '5px', 
                     'border': '1px solid #ffeaa7', 'marginBottom': 20}),
            
            html.Div([
                html.Label("Data Category:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='data-category',
                    options=[{'label': cat, 'value': cat} for cat in [
                        'Peak_Currents', 'RMS_Currents', 'AVG_Currents', 
                        'Peak_Voltages', 'RMS_Voltages', 'AVG_Voltages',
                        'Dissipations', 'Elec_Stats', 'Temps', 'Thermal_Stats',
                        'FFT_Current', 'FFT_Voltage'
                    ]],
                    value='Peak_Currents',
                    clearable=False
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '4%'}),
            
            html.Div([
                html.Label("Component:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='component-selector', clearable=False)
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Fixed Parameters:", style={'fontWeight': 'bold', 'marginTop': 20}),
                html.Div(id='fixed-params-controls')
            ], style={'marginTop': 20}),
            
            html.Button('Generate Plot', id='generate-plot', n_clicks=0,
                       style={'marginTop': 20, 'padding': '10px 20px', 
                              'backgroundColor': '#3498db', 'color': 'white',
                              'border': 'none', 'borderRadius': '5px',
                              'cursor': 'pointer'}),
            
            # Clear selections button
            html.Button('Clear Selections', id='clear-selections', n_clicks=0,
                       style={'marginTop': 10, 'marginLeft': '10px', 'padding': '10px 20px', 
                              'backgroundColor': '#e74c3c', 'color': 'white',
                              'border': 'none', 'borderRadius': '5px',
                              'cursor': 'pointer'})
            
        ], style={'backgroundColor': '#f8f9fa', 'padding': 20, 'borderRadius': 10}),
        
    ], style={'marginBottom': 30}),
    
    # Main plot container - now with a specific Graph component for click events
    html.Div([
        dcc.Graph(
            id='main-plot',
            style={'height': '600px', 'marginTop': 20},
            config={'displayModeBar': True}
        )
    ], id='plot-container', style={'marginTop': 30}),
    
    # Store for selected points
    dcc.Store(id='selected-points-store', data={}),
    
    # Display selected points information
    html.Div(id='selection-info', style={'marginTop': 20}),
    
    html.Div([
        html.Hr(),
        html.P(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 12}),
        html.P(f"Configuration: {len(active_sweep_keys)} active sweep variable(s) - {'2D' if plot_2D else '3D'} mode",
               style={'textAlign': 'center', 'color': '#95a5a6', 'fontSize': 10}),
        html.P("Click on points to select them. Selected points will show persistent data tips.",
               style={'textAlign': 'center', 'color': '#3498db', 'fontSize': 11, 'fontStyle': 'italic'})
    ], style={'marginTop': 50})
])

# Callbacks
@app.callback(
    Output('component-selector', 'options'),
    Input('data-category', 'value')
)
def update_component_options(selected_category):
    """Update component options based on selected category"""
    if selected_category in ['FFT_Current', 'FFT_Voltage']:
        if selected_category == 'FFT_Current':
            components = FFT_headers[:len(headers_lists[6])]
        else:
            components = FFT_headers[len(headers_lists[6]):]
    else:
        category_index = mat_names.index(selected_category)
        components = headers_lists[category_index]
    
    return [{'label': comp, 'value': comp} for comp in components]

@app.callback(
    Output('component-selector', 'value'),
    Input('component-selector', 'options')
)
def set_default_component(options):
    """Set default component when options change"""
    if options:
        return options[0]['value']
    return None

@app.callback(
    Output('fixed-params-controls', 'children'),
    Input('data-category', 'value')  # Trigger when data category changes
)
def update_fixed_params_controls(data_category):
    """Create controls for fixed parameters based on plot mode"""
    fixed_vars = get_fixed_vars()
    pattern = re.compile(r'\d+')  # Pre-compile regex
    if not fixed_vars:
        return html.P("No fixed parameters available for this configuration.")
    
    controls = []
    for i, (key, values) in enumerate(fixed_vars.items()):
        param_name = config["sweepNames"][int(pattern.search(key).group())-1]
        controls.append(
            html.Div([
                html.Label(f"{param_name}:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id=f'fixed-{key}',
                    options=[{'label': str(val), 'value': val} for val in values],
                    value=values[0],
                    clearable=False
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 
                     'marginBottom': 10} if i % 2 == 0 else 
                     {'width': '48%', 'display': 'inline-block', 'marginBottom': 10})
        )
    
    return controls

def create_persistent_annotations(selected_points_data, component, plot_2D, sweep_label=None):
    """Create persistent annotations for selected points"""
    annotations = []
    
    if selected_points_data and component in selected_points_data:
        selected_x = selected_points_data[component].get('x', [])
        selected_y = selected_points_data[component].get('y', [])
        selected_z = selected_points_data[component].get('z', [])
        
        for i, (x, y) in enumerate(zip(selected_x, selected_y)):
            if plot_2D:
                # 2D annotations
                annotation_text = f"Point {i+1}:<br>{sweep_label}: {x:.4f}<br>{component}: {y:.4f}"
                annotations.append(dict(
                    x=x,
                    y=y,
                    xref="x",
                    yref="y",
                    text=annotation_text,
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="red",
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="red",
                    borderwidth=1,
                    borderpad=4,
                    font=dict(size=10, color="black"),
                    ax=20,
                    ay=-30
                ))
            else:
                # 3D annotations
                z = selected_z[i] if i < len(selected_z) else 0
                annotation_text = f"Point {i+1}:<br>X: {x:.4f}<br>Y: {y:.4f}<br>Z: {z:.4f}"
                annotations.append(dict(
                    x=x,
                    y=y,
                    z=z,
                    text=annotation_text,
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="red",
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="red",
                    borderwidth=1,
                    borderpad=4,
                    font=dict(size=10, color="black"),
                    ax=20,
                    ay=-30
                ))
    
    return annotations

def generate_2d_plot(component, fixed_params, selected_points_data=None):
    """Generate 2D plot based on component and fixed parameters"""
    relative_tol = 0.001
    absolute_tol = 1e-12
    
    sweep_values = sweep_vars[single_X_key]
    sweep_label = config["sweepNames"][int(pattern.search(single_X_key).group())-1]

    # Find rows that match the fixed parameters
    matching_rows = []
    for i, combo in enumerate(all_combos):
        combo_dict = dict(zip(sweep_keys, combo))
        if all(combo_dict.get(k) == v for k, v in fixed_params.items()):
            matching_rows.append((i, combo_dict[single_X_key]))
    
    if not matching_rows:
        return go.Figure().add_annotation(
            text="No data found for selected fixed parameters", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    matching_rows = np.array(matching_rows)
    x_vals = matching_rows[:, 1]
    
    # Get data column
    if component in headers_array:
        z_column = headers_array.index(component)
        z_vals = combined_matrix[matching_rows[:, 0].astype(int), z_column]
    else:
        z_column = FFT_headers.index(component)
        z_vals = combined_fft_matrix[matching_rows[:, 0].astype(int), z_column]
    
    # Handle constant values
    if np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
        x_plot = np.array([x_vals[0], x_vals[-1]])
        z_plot = np.array([z_vals[0], z_vals[-1]])
    else:
        x_plot = x_vals
        z_plot = z_vals
    
    # Format title with fixed parameters
    fixed_dict = fixed_params
    title_suffix = format_fixed_title(fixed_dict, config["sweepNames"]) if fixed_dict else ""
    
    # Check if this is an FFT component for bar plot
    is_fft = component in FFT_headers
    
    fig = go.Figure()
    
    if is_fft:
        # 2D Bar plot for FFT
        fig.add_trace(go.Bar(
            x=x_plot,
            y=z_plot,
            name=component,
            marker_color='lightblue',
            hovertemplate=f"<b>{sweep_label}</b>: %{{x}}<br><b>{component}</b>: %{{y:.4f}}<extra></extra>"
        ))
    else:
        # Regular line plot
        fig.add_trace(go.Scatter(
            x=x_plot, 
            y=z_plot, 
            mode='lines+markers',
            name=component,
            line=dict(color='blue', width=2),
            marker=dict(size=8, color='blue'),
            hovertemplate=f"<b>{sweep_label}</b>: %{{x}}<br><b>{component}</b>: %{{y:.4f}}<extra></extra>"
        ))
    
    # Add selected points as highlighted markers
    if selected_points_data and component in selected_points_data:
        selected_x = selected_points_data[component].get('x', [])
        selected_y = selected_points_data[component].get('y', [])
        
        if len(selected_x) > 0 and len(selected_y) > 0:
            fig.add_trace(go.Scatter(
                x=selected_x,
                y=selected_y,
                mode='markers',
                name='Selected Points',
                marker=dict(
                    size=12,
                    color='red',
                    symbol='circle',
                    line=dict(width=2, color='darkred')
                ),
                hovertemplate=f"<b>Selected Point</b><br>{sweep_label}: %{{x}}<br>{component}: %{{y:.4f}}<extra></extra>"
            ))
            
            # Add persistent annotations for selected points
            annotations = create_persistent_annotations(selected_points_data, component, True, sweep_label)
            fig.update_layout(annotations=annotations)
    
    full_title = f"{component}<br>{title_suffix}" if title_suffix else component
    
    fig.update_layout(
        title=dict(text=full_title, x=0.5),
        xaxis_title=sweep_label, 
        yaxis_title=component,
        xaxis_title_font=dict(size=12),
        yaxis_title_font=dict(size=12),
        xaxis_tickfont=dict(size=10),
        yaxis_tickfont=dict(size=10),
        margin=dict(l=50, r=50, t=80 if title_suffix else 50, b=50),
        hovermode='closest'
    )
    
    return fig

def generate_3d_plot(component, fixed_params, selected_points_data=None):
    """Generate 3D plot based on component and fixed parameters"""
    relative_tol = 0.001
    absolute_tol = 1e-12
    
    var1, var2 = config["Var1"], config["Var2"]
    sweepNames = config["sweepNames"]
    
    # Find rows that match the fixed parameters
    rows = []
    for i, combo in enumerate(all_combos):
        combo_dict = dict(zip(sweep_keys, combo))
        if all(combo_dict.get(k) == v for k, v in fixed_params.items()):
            rows.append((i, combo_dict[var1], combo_dict[var2]))
    
    if not rows:
        return go.Figure().add_annotation(
            text="No data found for selected fixed parameters", 
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
    
    rows = np.array(rows)
    
    # Get data
    if component in headers_array:
        z_column = headers_array.index(component)
        z_vals = combined_matrix[rows[:, 0].astype(int), z_column]
    else:
        z_column = FFT_headers.index(component)
        z_vals = combined_fft_matrix[rows[:, 0].astype(int), z_column]
    
    x_vals, y_vals = rows[:, 1], rows[:, 2]
    
    # Check if this is an FFT component for 3D barchart
    is_fft = component in FFT_headers
    
    if is_fft:
        # Use 3D barchart for FFT data
        # For FFT, x_vals represent harmonics, y_vals represent the sweep variable
        x_plot = np.tile(np.array(harmonics), int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
        y_plot = y_vals
        z_plot = z_vals
        
        fixed_dict = fixed_params
        title_suffix = format_fixed_title(fixed_dict, sweepNames) if fixed_dict else ""
        full_title = f"{component}<br>{title_suffix}" if title_suffix else component
        
        fig = barchart3D(
            x_plot, y_plot, z_plot, 
            full_title, 'Magnitude', 
            'Harmonic Order', 
            sweepNames[int(pattern.search(var2).group())-1]
        )
        
    else:
        # Regular 3D surface plot
        X, Y = np.meshgrid(np.unique(x_vals), np.unique(y_vals))
        Z = np.full_like(X, np.nan, dtype=float)
        
        xi = np.searchsorted(np.unique(y_vals), y_vals)
        yi = np.searchsorted(np.unique(x_vals), x_vals)
        Z[xi, yi] = z_vals
        
        # Handle constant values
        if np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
            X = np.array([X[0, :], X[-1, :]])
            Y = np.array([Y[0, :], Y[-1, :]])
            Z = np.array([Z[0, :], Z[-1, :]])
        
        fixed_dict = fixed_params
        title_suffix = format_fixed_title(fixed_dict, sweepNames) if fixed_dict else ""
        full_title = f"{component}<br>{title_suffix}" if title_suffix else component
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
        
        # Add selected points if any
        if selected_points_data and component in selected_points_data:
            selected_x = selected_points_data[component].get('x', [])
            selected_y = selected_points_data[component].get('y', [])
            selected_z = selected_points_data[component].get('z', [])
            
            if len(selected_x) > 0:
                fig.add_trace(go.Scatter3d(
                    x=selected_x,
                    y=selected_y,
                    z=selected_z,
                    mode='markers',
                    name='Selected Points',
                    marker=dict(
                        size=6,
                        color='red',
                        symbol='circle',
                        line=dict(width=2, color='darkred')
                    ),
                    hovertemplate=f"<b>Selected Point</b><br>X: %{{x}}<br>Y: %{{y}}<br>Z: %{{z:.4f}}<extra></extra>"
                ))
                
                # Add persistent annotations for selected points
                annotations = create_persistent_annotations(selected_points_data, component, False)
                if annotations:
                    fig.update_layout(scene_annotations=annotations)
        
        fig.update_layout(
            title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
            scene=dict(
                xaxis=dict(autorange='reversed'),
                yaxis=dict(autorange='reversed'),
                xaxis_title=sweepNames[int(pattern.search(var1).group())-1],
                yaxis_title=sweepNames[int(pattern.search(var2).group())-1],
                zaxis_title=component,
                xaxis_title_font=dict(size=10),
                yaxis_title_font=dict(size=10),
                zaxis_title_font=dict(size=10),
                xaxis_tickfont=dict(size=10),
                yaxis_tickfont=dict(size=10),
                zaxis_tickfont=dict(size=10)
            )
        )
    
    return fig

@app.callback(
    Output('main-plot', 'figure'),
    Output('selected-points-store', 'data'),
    Output('selection-info', 'children'),
    Input('generate-plot', 'n_clicks'),
    Input('clear-selections', 'n_clicks'),
    Input('main-plot', 'clickData'), 
    State('data-category', 'value'),
    State('component-selector', 'value'),
    State('fixed-params-controls', 'children'),
    State('selected-points-store', 'data')
)
def update_plot(n_clicks_generate, n_clicks_clear, click_data, data_category, component, fixed_controls, stored_selections):
    """Generate and display the plot based on automatic mode detection with persistent selections"""
    ctx = callback_context
    if not ctx.triggered:
        # Return empty figure initially
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Select parameters and click 'Generate Plot' to view results",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        return empty_fig, stored_selections, ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Handle clear selections
    if trigger_id == 'clear-selections':
        stored_selections = {}
        # Regenerate plot without selections but keep the same parameters
        if n_clicks_generate > 0 and component:
            fig = generate_plot_with_params(data_category, component, fixed_controls, {})
            info = html.Div("All selections cleared.", className="selection-info")
            return fig, {}, info
        else:
            # Return to initial state
            empty_fig = go.Figure()
            empty_fig.update_layout(
                title="Select parameters and click 'Generate Plot' to view results",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
            return empty_fig, {}, ""
    
    # Handle point selection
    if trigger_id == 'main-plot' and click_data and component:
        point_data = click_data['points'][0]
        
        # Initialize component in selections if not exists
        if component not in stored_selections:
            stored_selections[component] = {'x': [], 'y': [], 'z': []}
        
        # Add the clicked point
        if plot_2D:
            stored_selections[component]['x'].append(point_data['x'])
            stored_selections[component]['y'].append(point_data['y'])
        else:
            stored_selections[component]['x'].append(point_data['x'])
            stored_selections[component]['y'].append(point_data['y'])
            stored_selections[component]['z'].append(point_data['z'])
        
        # Create selection info
        if plot_2D:
            pattern = re.compile(r'\d+')  # Pre-compile regex
            sweep_label = config["sweepNames"][int(pattern.search(single_X_key).group())-1]
            info_text = f"Selected Point {len(stored_selections[component]['x'])}: {sweep_label} = {point_data['x']:.4f}, {component} = {point_data['y']:.4f}"
        else:
            info_text = f"Selected Point {len(stored_selections[component]['x'])}: X = {point_data['x']:.4f}, Y = {point_data['y']:.4f}, Z = {point_data['z']:.4f}"
        
        info = html.Div([
            html.Strong("Selected Points:"),
            html.Br(),
            html.Span(info_text, style={'fontSize': '12px', 'color': '#27ae60'})
        ], className="selection-info")
        
        # Regenerate plot with updated selections
        fig = generate_plot_with_params(data_category, component, fixed_controls, stored_selections)
        return fig, stored_selections, info
    
    # Handle generate plot
    if trigger_id == 'generate-plot' and n_clicks_generate > 0 and component:
        # Create selection info if there are selections
        info = ""
        if stored_selections and component in stored_selections:
            num_points = len(stored_selections[component]['x'])
            info = html.Div([
                html.Strong(f"Selected Points: {num_points} point(s)"),
                html.Br(),
                html.Span("Click 'Clear Selections' to remove all data tips", style={'fontSize': '11px', 'color': '#7f8c8d'})
            ], className="selection-info")
        
        fig = generate_plot_with_params(data_category, component, fixed_controls, stored_selections)
        return fig, stored_selections, info
    
    # Default return
    empty_fig = go.Figure()
    empty_fig.update_layout(
        title="Select parameters and click 'Generate Plot' to view results",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    return empty_fig, stored_selections, ""

def generate_plot_with_params(data_category, component, fixed_controls, stored_selections):
    """Helper function to generate plot with given parameters"""
    try:
        # Get fixed parameters from all the fixed-* dropdowns
        fixed_params = {}
        if fixed_controls and isinstance(fixed_controls, list):
            for control in fixed_controls:
                if 'id' in control['props'] and 'fixed-' in control['props']['id']:
                    param_key = control['props']['id'].replace('fixed-', '')
                    # Get the current value from the callback context
                    ctx = callback_context
                    if ctx.states:
                        for state_key, state_value in ctx.states.items():
                            if param_key in state_key.prop_id:
                                fixed_params[param_key] = state_value
                                break
        
        # If no fixed params found in context, use defaults
        if not fixed_params and fixed_controls:
            for control in fixed_controls:
                if 'id' in control['props'] and 'fixed-' in control['props']['id']:
                    param_key = control['props']['id'].replace('fixed-', '')
                    if param_key in sweep_vars:
                        fixed_params[param_key] = sweep_vars[param_key][0]
        
        # Use the automatically determined plot mode
        if plot_2D:
            fig = generate_2d_plot(component, fixed_params, stored_selections)
        else:
            fig = generate_3d_plot(component, fixed_params, stored_selections)
        
        # Add click event support
        fig.update_layout(clickmode='event+select')
        
        return fig
        
    except Exception as e:
        import traceback
        # Return error figure
        error_fig = go.Figure()
        error_fig.add_annotation(
            text=f"Error generating plot: {str(e)}",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
        )
        return error_fig

# Add some custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>PYPLECS DASHBOARD</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #ecf0f1;
            }
            .dashboard-container {
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .mode-info {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .fixed-params-grid {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
            }
            .fixed-param-item {
                flex: 1 1 calc(50% - 10px);
                min-width: 200px;
            }
            .selection-info {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=config_data['port'], use_reloader=False)
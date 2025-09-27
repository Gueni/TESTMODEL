#?-------------------------------------------------------------------------------------------------------------------------------
#?  Import Libraries
#?-------------------------------------------------------------------------------------------------------------------------------
import os, json
from natsort import natsorted
import pandas as pd, numpy as np
from itertools import product
import re
import plotly.graph_objects as go
import datetime
import plotly.io as pio
from plotly.io import to_html

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Header Files to JSON Array
#?-------------------------------------------------------------------------------------------------------------------------------
# Combine all JSON files in a directory into a single array
f_path      = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
all_files   = os.listdir(f_path)

# Excluded files: only header.json and Peak_Losses.json (FFT files included now)
j_files     = natsorted([f for f in all_files if f not in {'header.json', 'Peak_Losses.json'}])
j_array     = []

for f in j_files:
    data = json.load(open(os.path.join(f_path, f)))
    if "FFT" in f:  # suffix FFT headers
        if isinstance(data, list):
            j_array.extend([d + "_FFT" for d in data])
        else:
            j_array.append(data + "_FFT")
    else:
        if isinstance(data, list):
            j_array.extend(data)
        else:
            j_array.append(data)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Combine CSV Files into Normal + FFT
#?-------------------------------------------------------------------------------------------------------------------------------
folder      = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
excluded    = ['Peak_Losses.csv']

# Normal CSVs (surface/line data)
normal_files = [f for f in os.listdir(folder) if f.endswith('.csv') 
                and not f.startswith("FFT_") and f not in excluded]

# FFT CSVs (bar plot data, harmonics per iteration)
fft_files    = [f for f in os.listdir(folder) if f.startswith("FFT_") and f.endswith('.csv')]

# Combine normal CSVs into one matrix
combined_matrix = np.hstack([
    pd.read_csv(os.path.join(folder, f), header=None).values
    for f in sorted(normal_files)
])

# Load FFT data into dict {filename: dataframe}
fft_data = {
    f: pd.read_csv(os.path.join(folder, f), header=None)
    for f in fft_files
}

#?-------------------------------------------------------------------------------------------------------------------
#?  Find Sweep Variables and Their Combinations
#?-------------------------------------------------------------------------------------------------------------------
input_json  = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
with open(input_json) as f: 
    config = json.load(f)

# Sweep variables (exclude [0])
sweep_vars = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}

# All combinations of sweep variables
all_combos  = list(product(*[vals for vals in sweep_vars.values() if vals != [0]]))

#?-------------------------------------------------------------------------------------------------------------------
#? Automatically determine fixed variables
#?-------------------------------------------------------------------------------------------------------------------
other_vars = {k: eval(v) for k, v in config.items()
              if re.fullmatch(r"X\d+", k)
              and k not in [config["Var1"], config["Var2"]]
              and eval(v) != [0]
              and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X")
             }

fixed_combos = list(product(*other_vars.values()))
fixed_keys   = list(other_vars.keys())

#?-------------------------------------------------------------------------------------------------------------------
#? Select Rows Based on Automatically Determined Fixed Variables
#?-------------------------------------------------------------------------------------------------------------------
var1, var2 = config["Var1"], config["Var2"]
sweep_keys = list(sweep_vars.keys())

rows_by_fixed = {}
for fixed_values in fixed_combos:
    fixed = dict(zip(fixed_keys, fixed_values))
    rows = np.array([
        (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
        for i, combo in enumerate(all_combos)
        if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
    ])
    if len(rows) > 0:
        rows_by_fixed[tuple(fixed_values)] = (fixed, rows)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Plotting Logic (Normal + FFT)
#?-------------------------------------------------------------------------------------------------------------------------------
list_of_plots = []

for component in j_array:
    if component.endswith("_FFT"):
        # Which FFT file?
        fft_file = "FFT_Current_Map.csv" if "Current" in component else "FFT_Voltage_Map.csv"
        df = fft_data[fft_file]

        # Assumption: col0=iteration, col1=harmonic order, col2=value
        iteration_col = df.iloc[:, 0]
        harmonic_col  = df.iloc[:, 1]
        magnitude_col = df.iloc[:, 2]

        for iteration in iteration_col.unique():
            mask = iteration_col == iteration
            fig = go.Figure(data=[go.Bar(
                x=harmonic_col[mask],
                y=magnitude_col[mask],
                marker_color='royalblue',
                name=component
            )])
            fig.update_layout(
                title=f"{component} | Iteration {iteration}",
                xaxis_title="Harmonic Order",
                yaxis_title="Magnitude"
            )
            list_of_plots.append(fig)

    else:
        # Normal 2D/3D plots
        for fixed_values, (fixed, rows) in rows_by_fixed.items():
            z_axis   = component
            z_column = j_array.index(z_axis)
            x_vals   = rows[:, 1]
            y_vals   = rows[:, 2]
            # Normal logic: use combined_matrix
            z_column = j_array.index(z_axis)
            if z_column >= combined_matrix.shape[1]:
                # Skip this component because it's FFT-only
                continue
            z_vals   = combined_matrix[rows[:, 0].astype(int), z_column]
            # Meshgrid
            x_unique = np.unique(x_vals)
            y_unique = np.unique(y_vals)
            X, Y = np.meshgrid(x_unique, y_unique)
            Z = np.full_like(X, fill_value=np.nan, dtype=float)
            xi = np.searchsorted(x_unique, x_vals)
            yi = np.searchsorted(y_unique, y_vals)
            Z[yi, xi] = z_vals

            # Dynamic axis names
            var1_name = config["sweepNames"][int(re.search(r'\d+', config["Var1"]).group())-1]
            var2_name = config["sweepNames"][int(re.search(r'\d+', config["Var2"]).group())-1]
            fixed_title = " | ".join(
                f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" 
                for k, v in fixed.items()
            )

            # Decide 2D/3D
            num_sweep_vars = sum(1 for vals in sweep_vars.values() if len(vals) > 1 and vals != [0])
            plot_type = "2D" if num_sweep_vars < 3 else "3D"

            match plot_type:
                case "2D":
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=z_vals,
                        mode='lines',
                        fill='tozeroy',
                        line=dict(color='royalblue'),
                        name=z_axis
                    ))
                    fig.update_layout(
                        title=f"{z_axis}  @ {fixed_title}",
                        xaxis_title=var1_name,
                        yaxis_title=z_axis,
                    )
                case "3D":
                    fig = go.Figure(data=[go.Surface(
                        x=X,
                        y=Y,
                        z=Z,
                        colorscale='Viridis',
                        colorbar=dict(title=z_axis)
                    )])
                    fig.update_layout(
                        title=f'{z_axis} @ {fixed_title}',
                        scene=dict(
                            xaxis_title=var1_name,
                            yaxis_title=var2_name,
                            zaxis_title=z_axis
                        )
                    )
            list_of_plots.append(fig)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Generate HTML Report 
#?-------------------------------------------------------------------------------------------------------------------------------
split_3D = True  # toggle

base64_file = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
html_base   = r"D:\WORKSPACE\BJT-MODEL\results\result"
script_name = os.path.basename(__file__)
UTC         = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
date        = str(datetime.datetime.now().replace(microsecond=0))

with open(base64_file, 'r') as f:
    base64_img = ''.join(line.strip() for line in f)

if split_3D:
    n_fixed = len(fixed_combos)
    for idx, component in enumerate(j_array):
        html_file = f"{html_base}_{UTC}_{component}.html"
        start = idx * n_fixed
        end   = start + n_fixed
        component_plots = list_of_plots[start:end]

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('''
            <style>
                .container { position: relative; width: 100%; height: 150px; }
                .logo { position: absolute; top: 0; right: 0; height: 120px; }
                .info { position: absolute; left: 10px; font-weight: bold; }
                .script_name { top: 10px; }
                .date       { top: 50px; }
                .utc        { top: 90px; }
            </style>
            ''')
            f.write(f'''
            <div class="container">
                <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
                <div class="info script_name">Simulation: {script_name}</div>
                <div class="info date">Date & Time: {date}</div>
                <div class="info utc">Simulation ID: {UTC}</div>
            </div>
            ''')
            f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
            for fig in component_plots:
                fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
            f.write('</div>\n')
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

else:
    html_file = f"{html_base}_{UTC}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('''
        <style>
            .container { position: relative; width: 100%; height: 150px; }
            .logo { position: absolute; top: 0; right: 0; height: 120px; }
            .info { position: absolute; left: 10px; font-weight: bold; }
            .script_name { top: 10px; }
            .date       { top: 50px; }
            .utc        { top: 90px; }
        </style>
        ''')
        f.write(f'''
        <div class="container">
            <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
            <div class="info script_name">Simulation: {script_name}</div>
            <div class="info date">Date & Time: {date}</div>
            <div class="info utc">Simulation ID: {UTC}</div>
        </div>
        ''')
        f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
        for fig in list_of_plots:
            fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
            f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
        f.write('</div>\n')
        f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

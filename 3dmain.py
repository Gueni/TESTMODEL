
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
from plotly.io import to_html

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Define Variables
#?-------------------------------------------------------------------------------------------------------------------------------
f_path                                          = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
all_files                                       = os.listdir(f_path)
j_array  ,list_of_plots                         = [], []
folder                                          = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
excluded                                        = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
input_json                                      = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
with open(input_json) as f:config               = json.load(f)
var1, var2                                      = config["Var1"], config["Var2"]
split_3D                                        = False  
base64_file                                     = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
html_base                                       = r"D:\WORKSPACE\BJT-MODEL\results\result" 
script_name                                     = os.path.basename(__file__)
UTC                                             = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
date                                            = str(datetime.datetime.now().replace(microsecond=0))
with open(base64_file, 'r') as f: base64_img    = ''.join(line.strip() for line in f)
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Header Files to JSON Array
#?-------------------------------------------------------------------------------------------------------------------------------
j_files     = natsorted([f for f in all_files if f not in {'header.json', 'FFT_Current.json', 'FFT_Voltage.json','Peak_Losses.json'}])
[j_array.extend(data) if isinstance((data := json.load(open(os.path.join(f_path, f)))), list) else j_array.append(data) for f in j_files]
# print(f"Processed {len(j_files)} files")
# print(f"Combined array length: {len(j_array)}")
# print("Array contents:", j_array)
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Combine CSV Files into a Single Matrix
#?-------------------------------------------------------------------------------------------------------------------------------
# Load and combine CSV files, excluding specific ones
# The combined_matrix will contain the horizontally stacked data from the CSV files
combined_matrix = np.hstack(                                                            #   Horizontally stack arrays
                            [pd.read_csv(os.path.join(folder, f), header=None).values   #   Read each CSV file without headers
                            for f in sorted(os.listdir(folder))                         #   Sort files alphabetically
                            if f.endswith('.csv') and f not in excluded]                #   Exclude specific files
                            )
# print(f"Combined matrix shape: {combined_matrix.shape}")
# print("Combined matrix contents:", combined_matrix)
# print("column_5:", combined_matrix[:, j_array.index("CT Trafo Primary Current AVG")])
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Find Sweep Variables and Their Combinations
#?-------------------------------------------------------------------------------------------------------------------------------
# Extract sweep variables (keys matching "X" followed by digits)
sweep_vars = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
# print("Sweep Variables:", sweep_vars)
# Generate all combinations of sweep variables that have more than one value
# Lexicographic order (default of itertools.product)
all_combos  = list(product(*[vals for vals in sweep_vars.values() if vals != [0]]))  # each row = one simulation case
# print("All Combinations:", all_combos)
#?-------------------------------------------------------------------------------------------------------------------
#? Automatically determine fixed variables
#?-------------------------------------------------------------------------------------------------------------------
# Extract all sweep variables that are not Var1 or Var2 and not [0]
other_vars = {k: eval(v) for k, v in config.items()
              if re.fullmatch(r"X\d+", k)         # X variables only
              and k not in [config["Var1"], config["Var2"]]
              and eval(v) != [0]                  # ignore zero lists
              and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X") # real name
             }

# Generate all combinations of these fixed variables
fixed_combos = list(product(*other_vars.values()))

# Generate a list of their keys in order
fixed_keys = list(other_vars.keys())
#?-------------------------------------------------------------------------------------------------------------------
#? Select Rows Based on Automatically Determined Fixed Variables
#?-------------------------------------------------------------------------------------------------------------------
sweep_keys = list(sweep_vars.keys())                             # all sweep variable keys

# Identify other sweep variables that will act as "fixed" for plotting
other_vars = {k: eval(v) for k, v in config.items()
              if re.fullmatch(r"X\d+", k)                     # X variables only
              and k not in [var1, var2]                       # exclude Var1 and Var2
              and eval(v) != [0]                               # ignore zero lists
              and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X") # real name
             }

# Generate all combinations of these fixed variables
fixed_combos = list(product(*other_vars.values()))
fixed_keys   = list(other_vars.keys())

# Loop over each fixed combination to select rows for plotting
for fixed_values in fixed_combos:
    fixed = dict(zip(fixed_keys, fixed_values))  # create fixed dictionary for this iteration
    try :
        # select rows matching this fixed combination
        rows = np.array([
            (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
            for i, combo in enumerate(all_combos)
            if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
        ])
    except: len(rows) == 0; print("No matching rows found for fixed combination:", fixed)

# print("Selected Rows:", rows)
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Plotting the 3D Surface
#?-------------------------------------------------------------------------------------------------------------------------------
for component, fixed_values in product(j_array, fixed_combos):

        fixed           = dict(zip(fixed_keys, fixed_values))
        z_column        = j_array.index(component)
        x_vals          = rows[:, 1]
        y_vals          = rows[:, 2]
        z_vals          = combined_matrix[rows[:, 0].astype(int), z_column]
        var1_name       = config["sweepNames"][int(re.search(r'\d+', config["Var1"]).group())-1]
        var2_name       = config["sweepNames"][int(re.search(r'\d+', config["Var2"]).group())-1]
        fixed_title     = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k, v in fixed.items())
        plot_type       = "2D" if sum(1 for vals in sweep_vars.values() if len(vals) > 1 and vals != [0]) < 3 else "3D"

        match plot_type:
            case "2D":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals,y=z_vals,mode='lines',fill='tozeroy',line=dict(color='royalblue'),name=component))
                fig.update_layout(title=f"{component}  @ {fixed_title}",xaxis_title=var1_name,yaxis_title=component)
            case "3D":
                x_unique  = np.unique(x_vals)
                y_unique  = np.unique(y_vals)
                X, Y      = np.meshgrid(x_unique, y_unique)
                Z         = np.full_like(X, fill_value=np.nan, dtype=float)
                xi        = np.searchsorted(x_unique, x_vals)
                yi        = np.searchsorted(y_unique, y_vals)
                Z[yi, xi] = z_vals
                fig       = go.Figure(data=[go.Surface(x=X,y=Y,z=Z,colorscale='Viridis',colorbar=dict(title=component))])
                fig.update_layout(  title=f'{component} @ {fixed_title}',
                                    scene=dict(xaxis_title=var1_name,yaxis_title=var2_name,zaxis_title=component)
                                )
        list_of_plots.append(fig)
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Generate HTML Report 
#?-------------------------------------------------------------------------------------------------------------------------------
def write_html_report(html_file, plots):
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write('''
                    <style> .container      {position: relative;width: 100%;height: 150px;}
                            .logo           {position: absolute;top: 0;right: 0;height: 120px;}
                            .info           {position: absolute;left: 10px;font-weight: bold;}
                            .script_name    { top: 10px; }
                            .date           { top: 50px; }
                            .utc            { top: 90px; }
                    </style>''')
        f.write(f'''<div class="container">
                    <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
                    <div class="info script_name">Simulation: {script_name}</div>
                    <div class="info date">Date & Time: {date}</div>
                    <div class="info utc">Simulation ID: {UTC}</div>
                </div>''')
        f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
        for fig in plots:
            fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
            f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
        f.write('</div>\n')
        f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

if split_3D:
    for idx, component in enumerate(j_array):
        start, end      = idx * len(fixed_combos), (idx + 1) * len(fixed_combos)
        write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end])
else:
    write_html_report(f"{html_base}_{UTC}.html", list_of_plots)
#?-------------------------------------------------------------------------------------------------------------------------------
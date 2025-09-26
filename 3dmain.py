
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

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Header Files to JSON Array
#?-------------------------------------------------------------------------------------------------------------------------------
# Combine all JSON files in a directory into a single array, excluding specific files
# Excluded files: 'header.json', 'FFT_Current.json', 'FFT_Voltage.json'
# j_array will contain the combined data

f_path      = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
all_files   = os.listdir(f_path)
j_files     = natsorted([f for f in all_files if f not in {'header.json', 'FFT_Current.json', 'FFT_Voltage.json','Peak_Losses.json'}])
j_array     = []
[j_array.extend(data) if isinstance((data := json.load(open(os.path.join(f_path, f)))), list) else j_array.append(data) for f in j_files]

# print(f"Processed {len(j_files)} files")
# print(f"Combined array length: {len(j_array)}")
# print("Array contents:", j_array)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Combine CSV Files into a Single Matrix
#?-------------------------------------------------------------------------------------------------------------------------------

# Define the folder containing CSV files and combine them into a single CSV file
# Excluded files: 'FFT_Voltage_Map.csv', 'FFT_Current_Map.csv'
folder      = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
excluded    = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']

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

# Load configuration from JSON file
input_json  = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
with open(input_json) as f:config = json.load(f)

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

var1, var2 = config["Var1"], config["Var2"]                     # variables for axes
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

    # select rows matching this fixed combination
    rows = np.array([
        (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
        for i, combo in enumerate(all_combos)
        if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
    ])
    
    if len(rows) == 0:
        continue  # skip if no rows match

# print("Selected Rows:", rows)


#?-------------------------------------------------------------------------------------------------------------------------------
#?  Plotting the 3D Surface
#?-------------------------------------------------------------------------------------------------------------------------------

list_of_plots = []  # to store plot references if needed
# Loop over each fixed combination to create plots
for component in j_array:
    for fixed_values in fixed_combos:
        # Create fixed dictionary for this plot
        fixed = dict(zip(fixed_keys, fixed_values))
        z_axis = component  #! change as needed
        # Extract Z values
        z_column = j_array.index(z_axis)  # change as needed
        x_vals = rows[:, 1]
        y_vals = rows[:, 2]
        z_vals = combined_matrix[rows[:, 0], z_column]
        
        # Build meshgrid
        x_unique = np.unique(x_vals)
        y_unique = np.unique(y_vals)
        X, Y = np.meshgrid(x_unique, y_unique)
        Z = np.full_like(X, fill_value=np.nan, dtype=float)
        xi = np.searchsorted(x_unique, x_vals)
        yi = np.searchsorted(y_unique, y_vals)
        Z[yi, xi] = z_vals
        
        # Dynamic axis titles and plot title
        var1_name = config["sweepNames"][int(re.search(r'\d+', config["Var1"]).group())-1]
        var2_name = config["sweepNames"][int(re.search(r'\d+', config["Var2"]).group())-1]
        fixed_title = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" 
                                for k, v in fixed.items())
        
        # Decide 2D or 3D
        num_sweep_vars = sum(1 for vals in sweep_vars.values() if len(vals) > 1)
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
                fig.show()
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
                # fig.show()
        list_of_plots.append(fig)  # store reference if needed


#?-------------------------------------------------------------------------------------------------------------------------------
#?  Append Plotly Figures to HTML (2 columns layout)
#?-------------------------------------------------------------------------------------------------------------------------------

from plotly.io import to_html
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Generate HTML Report 
#?-------------------------------------------------------------------------------------------------------------------------------
base64_file = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
html_file   = r"D:\WORKSPACE\BJT-MODEL\results\result.html"
script_name = os.path.basename(__file__)
UTC         = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
date        = str(datetime.datetime.now().replace(microsecond=0))
# Read the base64 image
with open(base64_file, 'r') as f:base64_img = ''.join(line.strip() for line in f)

# Open HTML file and write content
with open(html_file, 'w', encoding='utf-8') as f:
    # Style for container and image positioning
    f.write('''
    <style>
        .container {
            position: relative;
            width: 100%;
            height: 150px; /* adjust height if needed */
        }
        .logo {
            position: absolute;
            top: 0;
            right: 0;
            height: 120px; /* adjust size if needed */
        }
        .info {
            position: absolute;
            left: 10px;
            font-weight: bold;
        }
        .script_name { top: 10px; }
        .date       { top: 50px; }
        .utc        { top: 90px; }
    </style>
    ''')

    # Container div with image and multiple info divs
    f.write(f'''
    <div class="container">
        <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
        <div class="info script_name">Simulation: {script_name}</div>
        <div class="info date">Date & Time: {date}</div>
        <div class="info utc">Simulation ID: {UTC}</div>
    </div>
    ''')

    # Start a container for the plots
    f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')

    for i, fig in enumerate(list_of_plots):
        # Convert figure to HTML div
        fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
        # Wrap each figure in a div with 50% width
        f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
    f.write('</div>\n')
    # Add Plotly.js library only once at the end
    f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')



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


def repo_3d(header_path                                     = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES",
            CSV_MAPS_folder                                  = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS",
            input_json                                      = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json",
            html_base                                       = r"D:\WORKSPACE\BJT-MODEL\results\result"):
    """
    Generate 3D surface and bar chart plots from simulation data stored in JSON headers and CSV maps,
    then compile them into interactive HTML reports. Supports FFT and non-FFT data separately.

    Args:
        header_path (str): Path to the JSON header files.
        CSV_MAPS_folder (str): Path to the folder containing CSV simulation data.
        input_json (str): JSON file specifying sweep variables and settings.
        html_base (str): Base path for saving HTML reports.
    """
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Define Variables
    #?-------------------------------------------------------------------------------------------------------------------------------
    headers_array  ,list_of_plots, fft_plots        = [], [], []
    all_header_files                                = os.listdir(header_path)
    
    # Exclude specific CSV and JSON headers that are not used for plotting
    excluded                                        = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
    excluded_headers                                = {'header.json', 'Peak_Losses.json'}
    
    # Load configuration JSON file (defines sweep variables, Var1, Var2, etc.)
    with open(input_json) as f:config               = json.load(f)
    var1, var2                                      = config["Var1"], config["Var2"]
    split_3D                                        = True  
    
    # Read base64 image for embedding logo in HTML reports
    base64_file                                     = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
    script_name                                     = os.path.basename(__file__)
    UTC                                             = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date                                            = str(datetime.datetime.now().replace(microsecond=0))
    with open(base64_file, 'r') as f: base64_img    = ''.join(line.strip() for line in f)
    
    # Harmonic indices and fundamental frequency for FFT plots
    harmonics                                       = [1,2] 
    F_fund                                          = 1e5 
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Header Files to JSON Array
    #?-------------------------------------------------------------------------------------------------------------------------------
    # Load and parse JSON header files, separating FFT and non-FFT headers into two lists
    headers_files   = natsorted([f for f in all_header_files if f not in excluded_headers])
    headers_lists   = [data if isinstance((data := json.load(open(os.path.join(header_path, f)))), list) else [data] for f in headers_files]
    FFT_headers     = sum(headers_lists[5:7], [])
    headers_array   = sum(headers_lists[:5] + headers_lists[7:], [])
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Combine CSV Files into a Single Matrix
    #?-------------------------------------------------------------------------------------------------------------------------------
    # Read all CSV files (excluding FFT ones) and horizontally stack them into a single matrix
    combined_matrix = np.hstack(                                                            
                                [pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values   
                                for f in sorted(os.listdir(CSV_MAPS_folder))                         
                                if f.endswith('.csv') and f not in excluded]                
                                )

    # Read FFT-specific CSV files and combine them separately
    combined_fft_matrix = np.hstack(
                                    [pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values 
                                    for f in natsorted([f for f in os.listdir(CSV_MAPS_folder) 
                                    if f.endswith('.csv') and f in excluded])]
                                )
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Find Sweep Variables and Their Combinations
    #?-------------------------------------------------------------------------------------------------------------------------------
    # Extract sweep variables (X1, X2, etc.) from config and build all combinations
    sweep_vars = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    all_combos = list(product(*sweep_vars.values()))
    
    # Build FFT combinations by repeating sweep combinations for each harmonic
    fft_combos = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))
    #?-------------------------------------------------------------------------------------------------------------------------------
    #? Select Rows Based on Automatically Determined Fixed Variables
    #?-------------------------------------------------------------------------------------------------------------------------------
    # Identify sweep keys and other fixed variables from config
    sweep_keys = list(sweep_vars.keys())                            
    other_vars = {k: eval(v) for k, v in config.items()
                if re.fullmatch(r"X\d+", k)                    
                and k not in [var1, var2]                    
                and eval(v) != [0]                       
                and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X") 
                }
    fixed_combos = list(product(*other_vars.values()))
    fixed_keys   = list(other_vars.keys())

    # Select rows from matrix that match fixed variable combinations
    for fixed_values in fixed_combos:
        fixed = dict(zip(fixed_keys, fixed_values)) 
        try :
            rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(all_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
            ])
            fft_rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(fft_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
            ])
        except: 
            len(rows) == 0 or len(fft_rows) == 0; print("No matching rows found for fixed combination:", fixed)
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Plotting the 3D Surface
    #?-------------------------------------------------------------------------------------------------------------------------------
    # Generate 3D surface plots for each header variable across sweep variables
    for component, fixed_values in product(headers_array, fixed_combos):

            fixed           = dict(zip(fixed_keys, fixed_values))
            z_column        = headers_array.index(component)
            x_vals          = rows[:, 1]
            y_vals          = rows[:, 2]
            z_vals          = combined_matrix[rows[:, 0].astype(int), z_column]
            var1_name       = config["sweepNames"][int(re.search(r'\d+', config["Var1"]).group())-1]
            var2_name       = config["sweepNames"][int(re.search(r'\d+', config["Var2"]).group())-1]
            fixed_title     = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k, v in fixed.items())

            # Build meshgrid for surface plot interpolation
            x_unique  = np.unique(x_vals)
            y_unique  = np.unique(y_vals)
            X, Y      = np.meshgrid(x_unique, y_unique)
            Z         = np.full_like(X, fill_value=np.nan, dtype=float)
            xi        = np.searchsorted(x_unique, x_vals)
            yi        = np.searchsorted(y_unique, y_vals)
            Z[yi, xi] = z_vals

            # Create surface plot and add to list
            fig       = go.Figure(data=[go.Surface(x=X,y=Y,z=Z,colorscale='Viridis',colorbar=dict(title=component))])
            fig.update_layout(  title=f'{component} @ {fixed_title}',
                                        scene=dict(xaxis_title=var1_name,yaxis_title=var2_name,zaxis_title=component)
                                    )
            list_of_plots.append(fig)
    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  FFT Plotting the 3D Bar Charts
    #?-------------------------------------------------------------------------------------------------------------------------------

    # Helper function to generate 3D bar chart (cuboid Mesh3d for each FFT point)
    def fft_barchart3d(x_vals, y_vals, z_vals, title, z_title, colorscale='Viridis', opacity=0.8):
        fig = go.Figure()
        ann = []

        # Determine bar widths in x and y directions
        dx = np.min(np.diff(np.sort(np.unique(x_vals)))) * 0.4 if len(x_vals)>1 else 1.0
        dy = np.min(np.diff(np.sort(np.unique(y_vals)))) * 0.4 if len(y_vals)>1 else 1.0

        # Loop through z values and add each as a 3D cuboid bar
        for i, z_max in enumerate(z_vals):
            x_cnt, y_cnt = x_vals[i], y_vals[i]
            x_min, x_max = x_cnt-dx/2, x_cnt+dx/2
            y_min, y_max = y_cnt-dy/2, y_cnt+dy/2

            fig.add_trace(go.Mesh3d(
                x=[x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max],
                y=[y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min],
                z=[0,0,0,0,z_max,z_max,z_max,z_max],
                alphahull=0, intensity=[0,0,0,0,z_max,z_max,z_max,z_max],
                coloraxis='coloraxis', opacity=opacity
            ))

            # Add text annotation at bar top
            ann.append(dict(showarrow=False, x=x_cnt, y=y_cnt, z=z_max,
                            text=f'{z_max:.2f}', font=dict(color='white', size=10),
                            bgcolor='rgba(0,0,0,0.3)', xanchor='center', yanchor='middle'))

        # Update layout with axes and color settings
        fig.update_layout(title=title,
                        scene=dict(xaxis_title="Frequency [Hz]",
                                    yaxis_title="Sweep Var",
                                    zaxis_title=z_title,
                                    annotations=ann),
                        coloraxis=dict(colorscale=colorscale))
        return fig

    # Generate FFT bar chart plots for each FFT component
    for component, fixed_values in product(FFT_headers, fixed_combos):
        fixed       = dict(zip(fixed_keys, fixed_values))
        z_column    = FFT_headers.index(component)
        y_vals      = fft_rows[:, 2]

        # Generate harmonic x values for FFT bar chart
        harm_xval   = np.array(harmonics) * F_fund 
        x_vals      = np.tile(harm_xval, int(np.ceil(len(y_vals) / len(harm_xval))))[:len(y_vals)]
        z_vals      = combined_fft_matrix[fft_rows[:, 0].astype(int), z_column]

        var1_name   = config["sweepNames"][int(re.search(r'\d+', config["Var1"]).group())-1]
        var2_name   = config["sweepNames"][int(re.search(r'\d+', config["Var2"]).group())-1]
        fixed_title = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k, v in fixed.items())

        # Meshgrid setup for bar chart alignment
        x_unique    = np.unique(x_vals)
        y_unique    = np.unique(y_vals)
        X, Y        = np.meshgrid(x_unique, y_unique)
        Z           = np.full_like(X, fill_value=np.nan, dtype=float)
        xi          = np.searchsorted(x_unique, x_vals)
        yi          = np.searchsorted(y_unique, y_vals)
        Z[yi, xi]   = z_vals

        # Flatten mesh for bar plotting
        Xf          = X.flatten()
        Yf          = Y.flatten()
        Zf          = Z.flatten()

        # Create bar chart and append to FFT plots
        fig         = fft_barchart3d(x_vals, y_vals, z_vals, f"{component} @ {fixed_title}", component)

        fft_plots.append(fig)

    #?-------------------------------------------------------------------------------------------------------------------------------
    #?  Generate HTML Report 
    #?-------------------------------------------------------------------------------------------------------------------------------

    # Helper function to write HTML report with embedded plots and simulation info
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
            # Insert header with logo, script name, date, and UTC simulation ID
            f.write(f'''<div class="container">
                        <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
                        <div class="info script_name">Simulation: {script_name}</div>
                        <div class="info date">Date & Time: {date}</div>
                        <div class="info utc">Simulation ID: {UTC}</div>
                    </div>''')

            # Insert plots side by side in HTML layout
            f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
            for fig in plots:
                fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
            f.write('</div>\n')
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

    # Save separate HTML reports for each variable if split_3D is enabled
    if split_3D:
        for idx, component in enumerate(headers_array):
            start, end      = idx * len(fixed_combos), (idx + 1) * len(fixed_combos)
            write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end])

        for idx, component in enumerate(FFT_headers):
            start, end      = idx * len(fixed_combos), (idx + 1) * len(fixed_combos)
            write_html_report(f"{html_base}_{UTC}_{component}.html", fft_plots[start:end])
    else:
        # Save single combined reports if split_3D is disabled
        write_html_report(f"{html_base}_{UTC}.html", list_of_plots)
        write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots)
    #?-------------------------------------------------------------------------------------------------------------------------------


# Call the function to generate reports
repo_3d()

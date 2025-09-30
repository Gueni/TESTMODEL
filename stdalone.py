#?-------------------------------------------------------------------------------------------------------------------------------
#?  Import Libraries
#?-------------------------------------------------------------------------------------------------------------------------------
import os, json
from natsort import natsorted
import pandas as pd, numpy as np
from itertools import product, zip_longest
import re
import plotly.graph_objects as go
import datetime
from plotly.io import to_html

def fft_barchart3d(x_vals, y_vals, z_vals, title, z_title, 
                   x_title, y_title, 
                   colorscale='Viridis', opacity=1):

    fig = go.Figure()
    ann = []

    # Ensure x_vals and y_vals are numpy arrays
    x_vals = np.array(x_vals, dtype=float)
    y_vals = np.array(y_vals, dtype=float)
    z_vals = np.array(z_vals, dtype=float)

    # Compute bar widths safely
    unique_x = np.unique(x_vals)
    unique_y = np.unique(y_vals)
    dx = np.min(np.diff(unique_x)) * 0.4 if len(unique_x) > 1 else 1.0
    dy = np.min(np.diff(unique_y)) * 0.4 if len(unique_y) > 1 else 1.0

    # Ensure widths are never zero
    dx = max(dx, 1e-6)
    dy = max(dy, 1e-6)

    # Create each bar
    for i, z_max in enumerate(z_vals):
        x_cnt, y_cnt = x_vals[i], y_vals[i]
        x_min, x_max = x_cnt - dx/2, x_cnt + dx/2
        y_min, y_max = y_cnt - dy/2, y_cnt + dy/2

        # Add Mesh3d cuboid for the bar
        fig.add_trace(go.Mesh3d(
            x=[x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max],
            y=[y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min],
            z=[0, 0, 0, 0, z_max, z_max, z_max, z_max],
            alphahull=0,
            intensity=[0, 0, 0, 0, z_max, z_max, z_max, z_max],
            coloraxis='coloraxis',
            opacity=opacity
        ))

        # Add annotation on top of the bar
        ann.append(dict(
            showarrow=False,
            x=x_cnt,
            y=y_cnt,
            z=z_max,
            text=f'{z_max:.2f}',
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.3)',
            xanchor='center',
            yanchor='middle'
        ))

    # Layout with centered multi-line title
    fig.update_layout(
        title=dict(
            text=title,    # you can pass f"{component} <br>{fixed_title}" when calling
            x=0.5,         # center horizontally
            xanchor='center',
            yanchor='top'
        ),
        scene=dict(
            xaxis_title=x_title,
            yaxis_title=y_title,
            zaxis_title=z_title,
            annotations=ann
        ),
        coloraxis=dict(colorscale=colorscale)
    )
    return fig

def create_dropdown_figure(component, fixed_combos_data, plot_type="3D", config=None, var1=None, var2=None, harmonics=None, F_fund=None):
    """
    Create a single figure with dropdown for different fixed combinations
    Supports both regular 2D/3D plots and FFT bar charts
    """
    fig = go.Figure()
    
    # Create dropdown buttons
    dropdown_buttons = []
    
    # Add traces for each fixed combination and create dropdown buttons
    for i, (fixed_key, data) in enumerate(fixed_combos_data.items()):
        x_vals, y_vals, z_vals, fixed_dict = data
        
        if plot_type == "2D":
            # For 2D plots
            fig.add_trace(
                go.Scatter(
                    x=x_vals, 
                    y=z_vals, 
                    mode='lines+markers', 
                    fill='tozeroy', 
                    name=component,
                    visible=(i == 0)  # Only first trace visible initially
                )
            )
        elif plot_type == "FFT":
            # For FFT bar charts - create temporary figure and add its traces
            temp_fig = fft_barchart3d(
                x_vals, y_vals, z_vals, 
                f"{component}", 'Magnitude',
                x_title='Frequency [Hz]',
                y_title=config["sweepNames"][int(re.search(r'\d+', var2).group())-1] if var2 else "Y",
                colorscale='Viridis', opacity=1
            )
            
            # Add all traces from the temporary figure
            for trace in temp_fig.data:
                trace.visible = (i == 0)  # Only first combo visible initially
                fig.add_trace(trace)
        else:
            # For 3D surface plots
            x_unique = np.unique(x_vals)
            y_unique = np.unique(y_vals)
            X, Y = np.meshgrid(x_unique, y_unique)
            Z = np.full_like(X, np.nan, dtype=float)
            xi = np.searchsorted(x_unique, x_vals)
            yi = np.searchsorted(y_unique, y_vals)
            Z[yi, xi] = z_vals
            
            fig.add_trace(
                go.Surface(
                    x=X, y=Y, z=Z, 
                    colorscale='Viridis', 
                    colorbar=dict(title=component),
                    visible=(i == 0)  # Only first trace visible initially
                )
            )
        
        # Create dropdown button for this fixed combination
        fixed_title = "<br>".join(" | ".join(list(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" 
                                for k,v in fixed_dict.items())[i:i+2]) for i in range(0, len(fixed_dict), 2))
        
        # Calculate visibility array based on plot type
        if plot_type == "FFT":
            # For FFT, we need to handle multiple traces per combo
            traces_per_combo = len(temp_fig.data) if 'temp_fig' in locals() else 1
            start_idx = i * traces_per_combo
            visibility = [False] * len(fig.data)
            for j in range(start_idx, start_idx + traces_per_combo):
                visibility[j] = True
        else:
            # For regular plots, one trace per combo
            visibility = [j == i for j in range(len(fixed_combos_data))]
        
        dropdown_buttons.append({
            'label': fixed_title,
            'method': 'update',
            'args': [
                {'visible': visibility},
                {'title.text': f'{component}<br>{fixed_title}'}  # Only update text, not entire title config
            ]
        })
    
    # Set layout based on plot type
    first_fixed_key = list(fixed_combos_data.keys())[0]
    first_fixed_dict = fixed_combos_data[first_fixed_key][3]  # Get the dict from data tuple
    first_fixed_title = "<br>".join(" | ".join(list(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" 
                                for k,v in first_fixed_dict.items())[i:i+2]) for i in range(0, len(first_fixed_dict), 2))
    
    if plot_type == "2D":
        fig.update_layout(
            title=dict(
                text=f'{component}<br>{first_fixed_title}',
                x=0.5,         # center horizontally
                xanchor='center',
                yanchor='top'
            ),
            xaxis_title=config["sweepNames"][int(re.search(r'\d+', var1).group())-1] if var1 else "X",
            yaxis_title=component,
            updatemenus=[{
                'type': 'dropdown',
                'x': 1.15,  # Position further to the right
                'y': 0.5,   # Center vertically
                'xanchor': 'left',
                'yanchor': 'middle',
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'bgcolor': 'lightgray',
                'bordercolor': 'black',
                'font': {'size': 12},
                'pad': {'r': 20}  # Add padding on the right
            }],
            margin=dict(r=200)  # Add right margin for dropdown
        )
    else:
        # For 3D and FFT plots
        scene_config = dict(
            xaxis_title=config["sweepNames"][int(re.search(r'\d+', var1).group())-1] if var1 else "X",
            yaxis_title=config["sweepNames"][int(re.search(r'\d+', var2).group())-1] if var2 else "Y",
            zaxis_title=component
        ) if plot_type == "3D" else None
        
        layout_updates = {
            'title': dict(
                text=f'{component}<br>{first_fixed_title}',
                x=0.5,         # center horizontally
                xanchor='center',
                yanchor='top'
            ),
            'updatemenus': [{
                'type': 'dropdown',
                'x': 1.15,  # Position further to the right
                'y': 0.5,   # Center vertically
                'xanchor': 'left',
                'yanchor': 'middle',
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'bgcolor': 'lightgray',
                'bordercolor': 'black',
                'font': {'size': 12},
                'pad': {'r': 20}  # Add padding on the right
            }],
            'margin': dict(r=200)  # Add right margin for dropdown
        }
        
        if scene_config:
            layout_updates['scene'] = scene_config
            
        fig.update_layout(**layout_updates)
    
    return fig

def repo_3d(header_path                                     = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES",
            CSV_MAPS_folder                                  = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS",
            input_json                                      = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json",
            html_base                                       = r"D:\WORKSPACE\BJT-MODEL\results\result"):
    """
    Generate 2D/3D plots and FFT plots automatically based on sweep variables.
    1 active sweep → 2D, 2+ active sweeps → 3D.
    """
    headers_array, list_of_plots, fft_plots = [], [], []
    all_header_files = os.listdir(header_path)

    excluded = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
    excluded_headers = {'header.json', 'Peak_Losses.json'}

    # Load config
    with open(input_json) as f:
        config = json.load(f)
    var1, var2 = config["Var1"], config["Var2"]

    base64_file = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
    script_name = os.path.basename(__file__)
    UTC = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date = str(datetime.datetime.now().replace(microsecond=0))
    with open(base64_file, 'r') as f:
        base64_img = ''.join(line.strip() for line in f)

    permute = True
    harmonics = [1, 2]
    F_fund = 1e5

    # Load header files
    headers_files = natsorted([f for f in all_header_files if f not in excluded_headers])
    headers_lists = [data if isinstance((data := json.load(open(os.path.join(header_path, f)))), list) else [data] for f in headers_files]
    FFT_headers = sum(headers_lists[5:7], [])
    headers_array = sum(headers_lists[:5] + headers_lists[7:], [])

    # Combine CSV files
    combined_matrix = np.hstack(
        [pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values
         for f in sorted(os.listdir(CSV_MAPS_folder))
         if f.endswith('.csv') and f not in excluded]
    )
    combined_fft_matrix = np.hstack(
        [pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values
         for f in natsorted([f for f in os.listdir(CSV_MAPS_folder) if f.endswith('.csv') and f in excluded])]
    )

    # Detect sweep variables
    sweep_vars = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    sweep_keys = list(sweep_vars.keys())
    active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0]]
    print("Active sweep variables:", active_sweep_keys)
    # Determine plot type
    plot_2D = len(active_sweep_keys) == 1
    single_X_key = active_sweep_keys[0] if plot_2D else None
    print("Plot type:", "2D" if plot_2D else "3D")
    # Build all sweep combinations
    all_combos = (list(product(*sweep_vars.values())) if permute
                  else np.where((arr := np.array(list(zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None,
                                [v[-1] for v in sweep_vars.values()], arr).tolist())
    fft_combos = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))
    print(f"Total combinations: {len(all_combos)} | FFT combinations: {len(fft_combos)}")
    #------------------------ 2D mode ------------------------#
    if plot_2D:
        print("2D mode detected. Single sweep variable:", single_X_key)
        sweep_values = sweep_vars[single_X_key]

        # Non-FFT plots
        for component in headers_array:
            z_column = headers_array.index(component)
            # Take first len(sweep_values) rows from CSV (assumes same order)
            z_vals = combined_matrix[:len(sweep_values), z_column]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=sweep_values, y=z_vals, mode='lines+markers', fill='tozeroy', name=component))
            fig.update_layout(
                title=dict(
                    text=component,
                    x=0.5,         # center horizontally
                    xanchor='center',
                    yanchor='top'
                ),
                xaxis_title=config["sweepNames"][int(re.search(r'\d+', single_X_key).group())-1],
                yaxis_title=component
            )
            list_of_plots.append(fig)

        # FFT plots
        for component in FFT_headers:
            z_column = FFT_headers.index(component)
            z_vals = combined_fft_matrix[:len(sweep_values), z_column]
            x_vals = np.array(harmonics) * F_fund
            # Repeat sweep values for each harmonic
            x_plot = np.tile(x_vals, int(np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]
            fig = go.Figure()
            fig.add_trace(go.Bar(x=x_plot, y=z_vals, name=component))
            fig.update_layout(
                title=dict(
                    text=component,
                    x=0.5,         # center horizontally
                    xanchor='center',
                    yanchor='top'
                ),
                xaxis_title='Frequency [Hz]', 
                yaxis_title=component
            )
            fft_plots.append(fig)

    #------------------------ 3D mode ------------------------#
    else:
        # Other fixed variables
        sweep_keys = list(sweep_vars.keys())                            
        other_vars = {k: eval(v) for k, v in config.items()
                    if re.fullmatch(r"X\d+", k)                    
                    and k not in [var1, var2]                    
                    and eval(v) != [0]                       
                    and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X") 
                    }
        fixed_keys = list(other_vars.keys())
        fixed_combos = (list(product(*other_vars.values())) if permute
                        else np.where((arr := np.array(list(zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None,
                                      [v[-1] for v in other_vars.values()], arr).tolist())

        # Select rows for each fixed combination
        rows_dict = {}
        fft_rows_dict = {}

        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(all_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())
            ])
            fft_rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(fft_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())
            ])
            rows_dict[tuple(fixed_values)] = rows
            fft_rows_dict[tuple(fixed_values)] = fft_rows
        print("Fixed variable combinations:", fixed_combos)
        print(f"rows_dict : {rows_dict}")
        print(f"fft_rows_dict : {fft_rows_dict}")
        
        # Store data for dropdown figures (only used when split_3D = False)
        dropdown_data = {}
        fft_dropdown_data = {}
        
        # Prepare data for dropdown figures
        for component in headers_array:
            z_column = headers_array.index(component)
            component_data = {}
            
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_keys, fixed_values))
                rows = rows_dict[tuple(fixed_values)]
                if len(rows) == 0:
                    continue
                
                x_vals = rows[:,1]
                y_vals = rows[:,2]
                z_vals = combined_matrix[rows[:,0].astype(int), z_column]
                
                # Use string representation as hashable key
                fixed_key = "|".join([f"{k}={v}" for k, v in fixed_dict.items()])
                component_data[fixed_key] = (x_vals, y_vals, z_vals, fixed_dict)
            
            dropdown_data[component] = component_data
        
        # Prepare FFT data for dropdown figures
        for component in FFT_headers:
            z_column = FFT_headers.index(component)
            component_data = {}
            
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_keys, fixed_values))
                fft_rows = fft_rows_dict[tuple(fixed_values)]
                if len(fft_rows) == 0:
                    continue
                
                y_vals = fft_rows[:,2]
                x_vals = np.tile(np.array(harmonics)*F_fund, int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
                z_vals = combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
                
                # Use string representation as hashable key
                fixed_key = "|".join([f"{k}={v}" for k, v in fixed_dict.items()])
                component_data[fixed_key] = (x_vals, y_vals, z_vals, fixed_dict)
            
            fft_dropdown_data[component] = component_data
        
        # ORIGINAL BEHAVIOR - Create separate figures for each fixed combination
        for component, fixed_values in product(headers_array, fixed_combos):
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            fixed_title = "<br>".join(" | ".join(list(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k,v in fixed_dict.items())[i:i+2]) for i in range(0, len(fixed_dict), 2))

            z_column = headers_array.index(component)
            rows = rows_dict[tuple(fixed_values)]
            if len(rows) == 0:
                continue
            x_vals = rows[:,1]
            y_vals = rows[:,2]
            z_vals = combined_matrix[rows[:,0].astype(int), z_column]
            x_unique = np.unique(x_vals)
            y_unique = np.unique(y_vals)
            X, Y = np.meshgrid(x_unique, y_unique)
            Z = np.full_like(X, np.nan, dtype=float)
            xi = np.searchsorted(x_unique, x_vals)
            yi = np.searchsorted(y_unique, y_vals)
            Z[yi, xi] = z_vals
            fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title=component))])
            fig.update_layout(
                title=dict(
                    text=f'{component} <br>{fixed_title}',  # multi-line title
                    x=0.5,          # center horizontally (0 = left, 1 = right)
                    xanchor='center', 
                    yanchor='top'   # optional: align vertical top
                ),
                scene=dict(
                    xaxis_title=config["sweepNames"][int(re.search(r'\d+', var1).group())-1],
                    yaxis_title=config["sweepNames"][int(re.search(r'\d+', var2).group())-1],
                    zaxis_title=component
                )
            )

            list_of_plots.append(fig)

        #------------------------ 3D FFT plots ------------------------#
        for component, fixed_values in product(FFT_headers, fixed_combos):
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            fixed_title = "<br>".join(" | ".join(list(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k,v in fixed_dict.items())[i:i+2]) for i in range(0, len(fixed_dict), 3))

            z_column = FFT_headers.index(component)
            fft_rows = fft_rows_dict[tuple(fixed_values)]
            if len(fft_rows) == 0:
                continue

            y_vals = fft_rows[:,2]
            x_vals = np.tile(np.array(harmonics)*F_fund, int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
            z_vals = combined_fft_matrix[fft_rows[:,0].astype(int), z_column]


            fig = fft_barchart3d(x_vals, y_vals, z_vals, f"{component} @ <br>{fixed_title}", 'Magnitude' ,
                                 x_title='Frequency [Hz]',
                                 y_title= config["sweepNames"][int(re.search(r'\d+', var2).group())-1],
                                 colorscale='Viridis', opacity=1)

            fft_plots.append(fig)

    #------------------------ HTML report ------------------------#
    def write_html_report(html_file, plots, split_3D=False):
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('''
                        <style> 
                        .container      {position: relative;width: 100%;height: 150px;}
                        .logo           {position: absolute;top: 0;right: 0;height: 120px;}
                        .info           {position: absolute;left: 10px;font-weight: bold;}
                        .script_name    { top: 10px; }
                        .date           { top: 50px; }
                        .utc            { top: 90px; }
                        .plot-container {display: flex; flex-direction: column; gap: 40px; margin-top: 20px;}
                        .plot-item {width: 100%; margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 40px;}
                        .plot-item:last-child {border-bottom: none;}
                        </style>''')
            f.write(f'''<div class="container">
                        <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
                        <div class="info script_name">Simulation: {script_name}</div>
                        <div class="info date">Date & Time: {date}</div>
                        <div class="info utc">Simulation ID: {UTC}</div>
                    </div>''')
            
            if split_3D:
                # Original layout - 2 figures per row
                f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
                for fig in plots:
                    fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                    f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
                f.write('</div>\n')
            else:
                # New layout - 1 figure per row with dropdown on the right
                f.write('<div class="plot-container">\n')
                for fig in plots:
                    fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                    f.write(f'<div class="plot-item">{fig_html}</div>\n')
                f.write('</div>\n')
            
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

    # Save HTML
    split_3D = False  # Set to False to use dropdown feature
    
    if split_3D:
        # ORIGINAL BEHAVIOR - split into multiple files (multiple figures per component)
        print("Using ORIGINAL behavior - split into multiple files")
        for idx, component in enumerate(headers_array):
            start, end = idx*max(1,len(list_of_plots)//len(headers_array)), (idx+1)*max(1,len(list_of_plots)//len(headers_array))
            write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end], split_3D=True)
        for idx, component in enumerate(FFT_headers):
            start, end = idx*max(1,len(fft_plots)//len(FFT_headers)), (idx+1)*max(1,len(fft_plots)//len(FFT_headers))
            write_html_report(f"{html_base}_{UTC}_{component}.html", fft_plots[start:end], split_3D=True)
    else:
        # NEW BEHAVIOR - single files with dropdowns (only for 3D mode)
        print("Using NEW behavior - single files with dropdowns")
        if plot_2D:
            # For 2D mode, use original behavior (no dropdowns)
            print("2D mode - using original plotting behavior")
            write_html_report(f"{html_base}_{UTC}.html", list_of_plots, split_3D=True)
            write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots, split_3D=True)
        else:
            # For 3D mode with dropdowns - replace the plots with dropdown versions
            print("3D mode - creating dropdown figures")
            
            # Clear the original plots and create dropdown versions instead
            list_of_plots.clear()
            fft_plots.clear()
            
            # Create dropdown figures for non-FFT plots
            for component in headers_array:
                if component in dropdown_data and dropdown_data[component]:
                    print(f"Creating dropdown figure for {component}")
                    fig = create_dropdown_figure(
                        component, 
                        dropdown_data[component], 
                        plot_type="3D", 
                        config=config, 
                        var1=var1, 
                        var2=var2
                    )
                    list_of_plots.append(fig)
            
            # Create dropdown figures for FFT plots
            for component in FFT_headers:
                if component in fft_dropdown_data and fft_dropdown_data[component]:
                    print(f"Creating FFT dropdown figure for {component}")
                    fig = create_dropdown_figure(
                        component,
                        fft_dropdown_data[component],
                        plot_type="FFT",
                        config=config,
                        var2=var2
                    )
                    fft_plots.append(fig)

            # Write the HTML files with dropdown figures (one per row)
            write_html_report(f"{html_base}_{UTC}.html", list_of_plots[1:4], split_3D=False)
            write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots[1:4], split_3D=False)

# Call function
repo_3d()
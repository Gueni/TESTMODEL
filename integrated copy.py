#?------------------------------------------------
#?  Import Libraries
#?------------------------------------------------
import os, json
from natsort import natsorted
import pandas as pd, numpy as np
from itertools import product, zip_longest
import re
import plotly.graph_objects as go
import datetime
from plotly.io import to_html

def fft_barchart3d(x_vals, y_vals, z_vals, title, z_title, x_title, y_title, colorscale='Viridis', opacity=1):

    fig         = go.Figure()
    ann         = []
    # Ensure x_vals and y_vals are numpy arrays
    x_vals      = np.array(x_vals, dtype=float)
    y_vals      = np.array(y_vals, dtype=float)
    z_vals      = np.array(z_vals, dtype=float)

    # Compute bar widths safely
    unique_x    = np.unique(x_vals)
    unique_y    = np.unique(y_vals)
    dx          = np.min(np.diff(unique_x)) * 0.4 if len(unique_x) > 1 else 1.0
    dy          = np.min(np.diff(unique_y)) * 0.4 if len(unique_y) > 1 else 1.0

    # Ensure widths are never zero
    dx          = max(dx, 1e-6)
    dy          = max(dy, 1e-6)

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
            alphahull=0,intensity=[0, 0, 0, 0, z_max, z_max, z_max, z_max],coloraxis='coloraxis',opacity=opacity))
        
        # Add annotation on top of the bar
        ann.append(dict(showarrow=False,x=x_cnt,y=y_cnt,z=z_max,text=f'{z_max:.2f}',font=dict(color='white', size=10),bgcolor='rgba(0,0,0,0.3)',xanchor='center',yanchor='middle'))

    # Layout with centered multi-line title
    fig.update_layout(
        title=dict(text=title,x=0.5,xanchor='center',yanchor='top'),
        scene=dict(xaxis_title=x_title,yaxis_title=y_title,zaxis_title=z_title,annotations=ann),coloraxis=dict(colorscale=colorscale))
    return fig

def write_html_report(html_file, plots, base64_img, script_name, date, UTC, split_3D=False):
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

def format_fixed_title(fixed_dict, sweepNames):
    """Format the fixed title in the same way as dropdown case"""
    return "<br>".join(
        " | ".join(f"{sweepNames[int(re.search(r'\d+', k).group())-1]} = {v}"
                for k, v in list(fixed_dict.items())[j:j+2])
        for j in range(0, len(fixed_dict), 2)
    )

def repo_3d(header_path= r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES",
            CSV_MAPS_folder= r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS",
            input_json= r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json",
            html_base= r"D:\WORKSPACE\BJT-MODEL\results\result"):

    #?------------------------------------------------
    #?  Setup
    #?------------------------------------------------
    headers_array, list_of_plots, fft_plots = [], [], []
    all_header_files = os.listdir(header_path)
    split_3D = False   # default; only applies if plot_2D=False
    excluded = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
    excluded_headers = {'header.json', 'Peak_Losses.json'}

    with open(input_json) as f:
        config = json.load(f)
    var1, var2 = config["Var1"], config["Var2"]
    sweepNames = config["sweepNames"]

    base64_file = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
    script_name = os.path.basename(__file__)
    UTC = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date = str(datetime.datetime.now().replace(microsecond=0))
    with open(base64_file, 'r') as f:
        base64_img = ''.join(line.strip() for line in f)

    permute = True
    harmonics = [1, 2]
    F_fund = 1e5

    #?------------------------------------------------
    #?  Load headers and matrices
    #?------------------------------------------------
    headers_files   = natsorted([f for f in all_header_files if f not in excluded_headers])
    headers_lists   = [data if isinstance((data := json.load(open(os.path.join(header_path, f)))), list) else [data] for f in headers_files]
    FFT_headers     = sum(headers_lists[5:7], [])
    headers_array   = sum(headers_lists[:5] + headers_lists[7:], [])

    combined_matrix = np.hstack([pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values
                                 for f in sorted(os.listdir(CSV_MAPS_folder))
                                 if f.endswith('.csv') and f not in excluded])
    combined_fft_matrix = np.hstack([pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values
                                     for f in natsorted([f for f in os.listdir(CSV_MAPS_folder) if f.endswith('.csv') and f in excluded])])

    #?------------------------------------------------
    #?  Sweep variables
    #?------------------------------------------------
    sweep_vars          = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    sweep_keys          = list(sweep_vars.keys())
    active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0]]

    plot_2D             = len(active_sweep_keys) == 1
    single_X_key        = active_sweep_keys[0] if plot_2D else None

    all_combos = (list(product(*sweep_vars.values())) if permute
                  else np.where((arr := np.array(list(zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None,
                                [v[-1] for v in sweep_vars.values()], arr).tolist())
    fft_combos = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))

    #?------------------------------------------------
    #?  Plotting: 2D case
    #?------------------------------------------------
    if plot_2D:
        sweep_values = sweep_vars[single_X_key]

        # Normal signals
        for component in headers_array:
            z_column    = headers_array.index(component)
            z_vals      = combined_matrix[:len(sweep_values), z_column]
            fig         = go.Figure()
            fig.add_trace(go.Scatter(x=sweep_values, y=z_vals, mode='lines+markers', fill='tozeroy', name=component))
            
            # Create title in the same format as dropdown case
            fixed_dict = {}
            for k, v in sweep_vars.items():
                if k != single_X_key and v != [0]:
                    fixed_dict[k] = v[0] if isinstance(v, list) else v
            
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title = f'{component}<br>{fixed_title}' if fixed_dict else component
            
            fig.update_layout(
                title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                xaxis_title=sweepNames[int(re.search(r'\d+', single_X_key).group())-1],
                yaxis_title=component
            )
            list_of_plots.append(fig)

        # FFT
        for component in FFT_headers:
            z_column    = FFT_headers.index(component)
            z_vals      = combined_fft_matrix[:len(sweep_values), z_column]
            x_vals      = np.array(harmonics) * F_fund
            x_plot      = np.tile(x_vals, int(np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]
            fig         = go.Figure()
            fig.add_trace(go.Bar(x=x_plot, y=z_vals, name=component))
            
            # Create title in the same format as dropdown case
            fixed_dict = {}
            for k, v in sweep_vars.items():
                if k != single_X_key and v != [0]:
                    fixed_dict[k] = v[0] if isinstance(v, list) else v
            
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title = f'{component}<br>{fixed_title}' if fixed_dict else component
            
            fig.update_layout(
                title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                xaxis_title='Frequency [Hz]', 
                yaxis_title=component
            )
            fft_plots.append(fig)

        # Write HTML reports (no splitting, no dropdowns)
        write_html_report(f"{html_base}_{UTC}.html", list_of_plots, base64_img, script_name, date, UTC, split_3D=False)
        write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots, base64_img, script_name, date, UTC, split_3D=False)
        return  # done

    #?------------------------------------------------
    #?  3D case: prepare fixed combos
    #?------------------------------------------------
    sweep_keys  = list(sweep_vars.keys())
    other_vars  = {k: eval(v) for k, v in config.items()
                   if re.fullmatch(r"X\d+", k) and k not in [var1, var2]
                   and eval(v) != [0] and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X")}
    fixed_keys      = list(other_vars.keys())
    fixed_combos    = (list(product(*other_vars.values())) if permute
                       else np.where((arr := np.array(list(zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None,
                                     [v[-1] for v in other_vars.values()], arr).tolist())

    rows_dict ,fft_rows_dict = {}, {}
    for fixed_values in fixed_combos:
        fixed_dict = dict(zip(fixed_keys, fixed_values))
        rows       = np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                               for i, combo in enumerate(all_combos)
                               if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
        fft_rows   = np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                               for i, combo in enumerate(fft_combos)
                               if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
        rows_dict[tuple(fixed_values)]     = rows
        fft_rows_dict[tuple(fixed_values)] = fft_rows

    #?------------------------------------------------
    #?  Case A: split_3D=True → per-combo HTML, no dropdown
    #?------------------------------------------------
    if split_3D:
        for component, fixed_values in product(headers_array, fixed_combos):
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            z_column   = headers_array.index(component)
            rows       = rows_dict[tuple(fixed_values)]
            if len(rows) == 0: continue
            x_vals, y_vals, z_vals = rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), z_column]
            X, Y = np.meshgrid(np.unique(x_vals), np.unique(y_vals))
            Z    = np.full_like(X, np.nan, dtype=float)
            Z[np.searchsorted(np.unique(y_vals), y_vals), np.searchsorted(np.unique(x_vals), x_vals)] = z_vals
            
            # Create title in the same format as dropdown case
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title = f'{component}<br>{fixed_title}'
            
            fig  = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title=component))])
            fig.update_layout(
                title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                scene=dict(
                    xaxis_title=sweepNames[int(re.search(r'\d+', var1).group())-1],
                    yaxis_title=sweepNames[int(re.search(r'\d+', var2).group())-1],
                    zaxis_title=component
                )
            )
            list_of_plots.append(fig)

        for component, fixed_values in product(FFT_headers, fixed_combos):
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            z_column   = FFT_headers.index(component)
            fft_rows   = fft_rows_dict[tuple(fixed_values)]
            if len(fft_rows) == 0: continue
            y_vals     = fft_rows[:,2]
            x_vals     = np.tile(np.array(harmonics)*F_fund, int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
            z_vals     = combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
            
            # Create title in the same format as dropdown case
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title = f'{component}<br>{fixed_title}'
            
            fig = fft_barchart3d(
                x_vals, y_vals, z_vals, full_title, 'Magnitude',
                x_title='Frequency [Hz]',
                y_title=sweepNames[int(re.search(r'\d+', var2).group())-1]
            )
            fft_plots.append(fig)

        # Write multiple files
        for idx, component in enumerate(headers_array):
            start, end = idx*max(1,len(list_of_plots)//len(headers_array)), (idx+1)*max(1,len(list_of_plots)//len(headers_array))
            write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end], base64_img, script_name, date, UTC, split_3D=True)
        for idx, component in enumerate(FFT_headers):
            start, end = idx*max(1,len(fft_plots)//len(FFT_headers)), (idx+1)*max(1,len(fft_plots)//len(FFT_headers))
            write_html_report(f"{html_base}_{UTC}_{component}.html", fft_plots[start:end], base64_img, script_name, date, UTC, split_3D=True)
        return

    #?------------------------------------------------
    #?  Case B: split_3D=False → use dropdowns
    #?------------------------------------------------
    def make_dropdown(component, fixed_combos_data, plot_type="3D"):
        fig, dropdown_buttons = go.Figure(), []
        sweepNames = config["sweepNames"]

        group_trace_indices = []  # keep track of indices per group
        current_index = 0

        for i, (_, data) in enumerate(fixed_combos_data.items()):
            x_vals, y_vals, z_vals, fixed_dict = data

            if plot_type == "FFT":
                temp_fig = fft_barchart3d(
                    x_vals, y_vals, z_vals, component, 'Magnitude',
                    x_title=sweepNames[int(re.search(r'\d+', var1).group())-1] if var1 else "X",
                    y_title=sweepNames[int(re.search(r'\d+', var2).group())-1] if var2 else "Y"
                )
                for trace in temp_fig.data:
                    trace.visible = False  # initially hidden
                    fig.add_trace(trace)
                n_traces = len(temp_fig.data)

            else:  # 3D Surface mode
                X, Y = np.meshgrid(np.unique(x_vals), np.unique(y_vals))
                Z = np.full_like(X, np.nan, dtype=float)
                Z[np.searchsorted(np.unique(y_vals), y_vals),
                np.searchsorted(np.unique(x_vals), x_vals)] = z_vals

                fig.add_trace(go.Surface(
                    x=X, y=Y, z=Z, colorscale='Viridis',
                    colorbar=dict(title=component),
                    visible=False  # initially hidden
                ))
                n_traces = 1

            # store which traces belong to this group
            group_trace_indices.append((current_index, current_index + n_traces))
            current_index += n_traces

        # Make the first group visible by default
        first_start, first_end = group_trace_indices[0]
        for j in range(first_start, first_end):
            fig.data[j].visible = True

        # Create dropdown buttons
        for i, (_, data) in enumerate(fixed_combos_data.items()):
            fixed_dict = data[3]
            start_idx, end_idx = group_trace_indices[i]

            # Title for dropdown label - using the same format function
            fixed_title = format_fixed_title(fixed_dict, sweepNames)

            # Visibility mask: hide all except this group
            visibility = [False] * len(fig.data)
            for j in range(start_idx, end_idx):
                visibility[j] = True

            dropdown_buttons.append({
                'label': fixed_title,
                'method': 'update',
                'args': [
                    {'visible': visibility},
                    {'title.text': f'{component}<br>{fixed_title}'}
                ]
            })

        # Initial title
        first_dict = next(iter(fixed_combos_data.values()))[3]
        first_title = format_fixed_title(first_dict, sweepNames)

        layout_base = dict(
            title=dict(text=f'{component}<br>{first_title}',
                    x=0.5, xanchor='center', yanchor='top'),
            updatemenus=[dict(type='dropdown', x=1.15, y=0.5,
                            xanchor='left', yanchor='middle',
                            buttons=dropdown_buttons,
                            direction='down', showactive=True,
                            bgcolor='lightgray', bordercolor='black',
                            font={'size': 12}, pad={'r': 20})],
            margin=dict(r=200)
        )

        if plot_type == "3D":
            layout_base['scene'] = dict(
                xaxis_title=sweepNames[int(re.search(r'\d+', var1).group())-1] if var1 else "X",
                yaxis_title=sweepNames[int(re.search(r'\d+', var2).group())-1] if var2 else "Y",
                zaxis_title=component
            )

        fig.update_layout(**layout_base)
        return fig

    # Prepare dropdown data
    dropdown_data, fft_dropdown_data = {}, {}
    for component in headers_array:
        comp_data = {}
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            rows = rows_dict[tuple(fixed_values)]
            if len(rows) == 0: continue
            x_vals, y_vals, z_vals = rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), headers_array.index(component)]
            comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
        dropdown_data[component] = comp_data

    for component in FFT_headers:
        comp_data = {}
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            fft_rows   = fft_rows_dict[tuple(fixed_values)]
            if len(fft_rows) == 0: continue
            y_vals     = fft_rows[:,2]
            x_vals     = np.tile(np.array(harmonics)*F_fund, int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
            z_vals     = combined_fft_matrix[fft_rows[:,0].astype(int), FFT_headers.index(component)]
            comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
        fft_dropdown_data[component] = comp_data

    # Create dropdown figs
    for component in headers_array:
        if dropdown_data[component]:
            list_of_plots.append(make_dropdown(component, dropdown_data[component], plot_type="3D"))
    for component in FFT_headers:
        if fft_dropdown_data[component]:
            fft_plots.append(make_dropdown(component, fft_dropdown_data[component], plot_type="FFT"))

    write_html_report(f"{html_base}_{UTC}.html", list_of_plots[1:4], base64_img, script_name, date, UTC, split_3D=False)
    write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots[1:4], base64_img, script_name, date, UTC, split_3D=False)

repo_3d()
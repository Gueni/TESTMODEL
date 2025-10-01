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
from plotly.io import dp.to_html.

header_path         = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
CSV_MAPS_folder     = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
input_json          = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
html_base           = r"D:\WORKSPACE\BJT-MODEL\results\result"

def barchart3D(x_vals, y_vals, z_vals, title, z_title, x_title, y_title, colorscale='Viridis', opacity=1):
    """
    Create a 3D bar chart using Plotly Mesh3d cuboids.
        - Each bar is represented as a Mesh3d cuboid.
        - The bar width is automatically calculated from the spacing between unique x and y values.
        - An annotation is added at the top of each bar, showing its height.

    Parameters :
                    x_vals      : (array) The x-coordinates of the bar positions.
                    y_vals      : (array) The y-coordinates of the bar positions.
                    z_vals      : (array) The heights (z-axis values) of the bars.
                    title       : (str)   Title of the chart.
                    z_title     : (str)   Label for the Z-axis.
                    x_title     : (str)   Label for the X-axis.
                    y_title     : (str)   Label for the Y-axis.
                    colorscale  : (str)   optional Plotly colorscale name (default is 'Viridis').
                    opacity     : (float) optional Opacity of the bars (default is 1, fully opaque).

    Returns    :
                    fig : plotly.graph_objects.Figure : A Plotly Figure object containing the 3D bar chart.

    """
    # Create an empty Plotly figure and Collect annotations for bar tops
    fig         = dp.go.Figure()
    ann         = []

    # Ensure x_vals, y_vals, and z_vals are numpy arrays of type float
    x_vals, y_vals, z_vals = map(lambda arr: dp.np.array(arr, dtype=float), (x_vals, y_vals, z_vals))

    # Compute bar widths safely from unique coordinate spacings
    dx          = dp.np.min(dp.np.diff(dp.np.unique(x_vals))) * 0.4 if len(dp.np.unique(x_vals)) > 1 else 1.0
    dy          = dp.np.min(dp.np.diff(dp.np.unique(y_vals))) * 0.4 if len(dp.np.unique(y_vals)) > 1 else 1.0

    # Ensure widths are never zero (avoid degenerate bars)
    dx, dy      = max(dx, 1e-6), max(dy, 1e-6) 

    # Loop over all z-values to create cuboid bars
    for i, z_max in enumerate(z_vals):
        x_cnt, y_cnt = x_vals[i], y_vals[i]  
        x_min, x_max = x_cnt - dx/2, x_cnt + dx/2
        y_min, y_max = y_cnt - dy/2, y_cnt + dy/2
        x            = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
        y            = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
        z            = [0, 0, 0, 0, z_max, z_max, z_max, z_max]

        # Add a cuboid Mesh3d trace for the bar
        fig.add_trace(dp.go.Mesh3d(x=x,y=y,z=z,alphahull=0,intensity=z,coloraxis='coloraxis',opacity=opacity))

        # Add annotation on top of the bar showing height
        ann.append(dict(showarrow=False,x=x_cnt, y=y_cnt, z=z_max,text=f'{z_max:.2f}',font=dict(color='white', size=10),bgcolor='rgba(0,0,0,0.3)',xanchor='center', yanchor='middle'))

    # Update layout: axis labels, fonts, title, colors
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', yanchor='top'),
        scene=dict(xaxis_title=x_title,yaxis_title=y_title,zaxis_title=z_title,annotations=ann,xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),
                   zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10)),
        coloraxis=dict(colorscale=colorscale))

    return fig

def repo_3d(header_path=header_path, CSV_MAPS_folder=CSV_MAPS_folder,input_json=input_json, html_base=html_base):
    """
    Generate 2D or 3D simulation plots (including FFT) from matrix and JSON data
    and export them as interactive HTML reports. Supports both single-variable
    2D plots and multi-variable 3D surfaces with dropdown selection.

    Parameters:
        header_path (str)       : Path to the folder containing JSON header files.

    """
    #?------------------------------------------------
    #?  Initialize variables and read inputs
    #?------------------------------------------------
    headers_array, list_of_plots, fft_plots     = [], [], []
    all_header_files                            = dp.os.listdir(header_path)
    iterSplit                                   = False
    excluded                                    = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
    excluded_headers                            = {'header.json', 'Peak_Losses.json'}
    with open(input_json) as f:config           = dp.json.load(f)
    var1, var2                                  = dp.JSON["Var1"], dp.JSON["Var2"]
    sweepNames                                  = dp.JSON["sweepNames"]
    base64_file                                 = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Lodp.go.txt"
    script_name                                 = dp.os.path.basename(__file__)
    UTC                                         = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date                                        = str(datetime.datetime.now().replace(microsecond=0))
    with open(base64_file, 'r') as f:base64_img = ''.join(line.strip() for line in f)
    permute                                     = True
    harmonics                                   = [1, 2]
    F_fund                                      = 1e5

    def format_fixed_title(fixed_dict, sweepNames):
        """Format the fixed title in the same way as dropdown case"""
        return "<br>".join(" | ".join(f"{sweepNames[int(dp.re.search(r'\d+', k).group())-1]} = {v}"for k, v in list(fixed_dict.items())[j:j+2])for j in range(0, len(fixed_dict), 2))

    def write_html_report(html_file, plots, base64_img, script_name, date, UTC, iterSplit=False):
        """Export interactive Plotly figures to a styled HTML report with logo, metadata, and optional multi-figure layout."""
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
                
            if iterSplit:
                    # 2 figures per row
                    f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
                    for fig in plots:
                        fig_html = dp.to_html.(fig, include_plotlyjs='cdn', full_html=False)
                        f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
                    f.write('</div>\n')
            else:
                    # 1 figure per row with dropdown on the right
                    f.write('<div class="plot-container">\n')
                    for fig in plots:
                        fig_html = dp.to_html.(fig, include_plotlyjs='cdn', full_html=False)
                        f.write(f'<div class="plot-item">{fig_html}</div>\n')
                    f.write('</div>\n')
                
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

    #?------------------------------------------------
    #?  Load headers and matrices
    #?------------------------------------------------
    headers_files       = natsorted([f for f in all_header_files if f not in excluded_headers])
    headers_lists       = [data if isinstance((data := dp.json.load(open(dp.os.path.join(header_path, f)))), list) else [data] for f in headers_files]
    FFT_headers         = sum(headers_lists[5:7], [])
    headers_array       = sum(headers_lists[:5] + headers_lists[7:], [])
    combined_matrix     = dp.np.hstack([dp.pd.read_csv(dp.os.path.join(CSV_MAPS_folder, f), header=None).values for f in sorted(dp.os.listdir(CSV_MAPS_folder)) if f.endswith('.csv') and f not in excluded])
    combined_fft_matrix = dp.np.hstack([dp.pd.read_csv(dp.os.path.join(CSV_MAPS_folder, f), header=None).values for f in natsorted([f for f in dp.os.listdir(CSV_MAPS_folder) if f.endswith('.csv') and f in excluded])])
    #?------------------------------------------------
    #?  Determine active sweep keys combinations
    #?------------------------------------------------
    sweep_vars          = {k: eval(v) for k, v in config.items() if dp.re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    sweep_keys          = list(sweep_vars.keys())
    active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0]]
    plot_2D             = len(active_sweep_keys) == 1
    single_X_key        = active_sweep_keys[0] if plot_2D else None
    all_combos          = (list(product(*sweep_vars.values())) if permute else dp.np.where((arr := dp.np.array(list(zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in sweep_vars.values()], arr).tolist())
    fft_combos          = list(map(tuple, dp.np.repeat(all_combos, len(harmonics), axis=0).astype(object)))
    #?------------------------------------------------
    #?  Plotting: 2D case
    #?------------------------------------------------
    if plot_2D:
        sweep_values    = sweep_vars[single_X_key]
        fig             = dp.go.Figure()
        fixed_dict      = {}

        # Normal signals 2D plotting
        for component in headers_array:
            z_column    = headers_array.index(component)
            z_vals      = combined_matrix[:len(sweep_values), z_column]
            fig.add_trace(dp.go.Scatter(x=sweep_values, y=z_vals, mode='lines+markers', fill='tozeroy', name=component))
            fixed_dict.update({k: v[0] if isinstance(v, list) else v for k, v in sweep_vars.items() if k != single_X_key and v != [0]})
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title  = f'{component}<br>{fixed_title}' if fixed_dict else component
            fig.update_layout(title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),xaxis_title=sweepNames[int(dp.re.search(r'\d+', single_X_key).group())-1],
                              yaxis_title=component,xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10))
            list_of_plots.append(fig)

        # FFT 2D plotting
        for component in FFT_headers:
            z_column    = FFT_headers.index(component)
            z_vals      = combined_fft_matrix[:len(sweep_values), z_column]
            x_vals      = dp.np.array(harmonics) * F_fund
            x_plot      = dp.np.tile(x_vals, int(dp.np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]
            fig.add_trace(dp.go.Bar(x=x_plot, y=z_vals, name=component))
            fixed_dict.update({k: v[0] if isinstance(v, list) else v for k, v in sweep_vars.items() if k != single_X_key and v != [0]})
            fixed_title = format_fixed_title(fixed_dict, sweepNames)
            full_title  = f'{component}<br>{fixed_title}' if fixed_dict else component
            fig.update_layout(title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),xaxis_title='Frequency [Hz]',yaxis_title=component,
                              xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10))
            fft_plots.append(fig)

        # Write HTML reports (no splitting, no dropdowns)
        write_html_report(f"{html_base}_{UTC}.html", list_of_plots, base64_img, script_name, date, UTC, iterSplit=False)
        write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots, base64_img, script_name, date, UTC, iterSplit=False)
        return
    #?------------------------------------------------
    #?  3D case: prepare fixed combos
    #?------------------------------------------------
    sweep_keys                  = list(sweep_vars.keys())
    other_vars                  = {k: eval(v) for k, v in config.items() if dp.re.fullmatch(r"X\d+", k) and k not in [var1, var2] and eval(v) != [0] and not dp.JSON["sweepNames"][int(dp.re.search(r'\d+', k).group())-1].startswith("X")}
    fixed_keys                  = list(other_vars.keys())
    fixed_combos                = (list(product(*other_vars.values())) if permute else dp.np.where((arr := dp.np.array(list(zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in other_vars.values()], arr).tolist())
    rows_dict ,fft_rows_dict    = {}, {}

    for fixed_values in fixed_combos:
        fixed_dict                          = dict(zip(fixed_keys, fixed_values))
        rows                                = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(all_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
        fft_rows                            = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(fft_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
        rows_dict[tuple(fixed_values)]      = rows
        fft_rows_dict[tuple(fixed_values)]  = fft_rows
    #?------------------------------------------------
    #?  Case A: iterSplit=True → per-combo HTML, no dropdown
    #?------------------------------------------------
    if iterSplit:
        for component, fixed_values in product(headers_array, fixed_combos):
            fixed_dict              =  dict(zip(fixed_keys, fixed_values))
            z_column                =  headers_array.index(component)
            rows                    =  rows_dict[tuple(fixed_values)]
            if len(rows)            == 0: continue #todo : add logic error for empty rows later
            x_vals, y_vals, z_vals  =  rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), z_column]
            X, Y                    =  dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
            Z                       =  dp.np.full_like(X, dp.np.nan, dtype=float)
            Xi , Yi                 =  dp.np.searchsorted(dp.np.unique(y_vals), y_vals), dp.np.searchsorted(dp.np.unique(x_vals), x_vals)
            Z[Xi,Yi]                =  z_vals
            full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
            fig                     =  dp.go.Figure(data=[dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title=component))])
            fig.update_layout(  title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                                scene=dict(xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                           xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10)))
            list_of_plots.append(fig)

        for component, fixed_values in product(FFT_headers, fixed_combos):
            fixed_dict              =  dict(zip(fixed_keys, fixed_values))
            z_column                =  FFT_headers.index(component)
            fft_rows                =  fft_rows_dict[tuple(fixed_values)]
            if len(fft_rows)        == 0: continue
            y_vals                  =  fft_rows[:,2]
            x_vals                  =  dp.np.tile(dp.np.array(harmonics)*F_fund, int(dp.np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
            z_vals                  =  combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
            full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
            fig                     =  barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Frequency [Hz]',y_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1])
            fft_plots.append(fig)

        # Write multiple html files
        for idx, component in enumerate(headers_array):
            start, end = idx*max(1,len(list_of_plots)//len(headers_array)), (idx+1)*max(1,len(list_of_plots)//len(headers_array))
            write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end], base64_img, script_name, date, UTC, iterSplit=True)
        for idx, component in enumerate(FFT_headers):
            start, end = idx*max(1,len(fft_plots)//len(FFT_headers)), (idx+1)*max(1,len(fft_plots)//len(FFT_headers))
            write_html_report(f"{html_base}_{UTC}_{component}.html", fft_plots[start:end], base64_img, script_name, date, UTC, iterSplit=True)
        return
    #?------------------------------------------------
    #?  Case B: iterSplit=False → 1 file ,use dropdowns
    #?------------------------------------------------
    def make_dropdown(full_title, component, fixed_combos_data, plot_type="3D"):
        """
        Create a Plotly figure with multiple traces (3D Surface or 3D bar chart) and a dropdown menu
        to switch between different sets of fixed parameter combinations.

        Each item in `fixed_combos_data` corresponds to a group of traces representing a fixed combination 
        of parameters. The dropdown allows the user to toggle visibility between these groups.
    
        - Each group of traces is initially hidden except the first group.
        - Dropdown menu entries are dynamically generated using the `fixed_dict` values.
        - Figure layout is automatically adjusted for scene axis titles and font sizes.
        - For `plot_type="FFT"`, x-axis is labeled as "Frequency [Hz]" and z-axis as "Magnitude".
        - For `plot_type="3D"`, axis titles use `sweepNames` from the global `config` dictionary.

        Parameters :
                    full_title          : str The overall title for the figure (used internally in trace generation).
                    component           : str Name of the component or measurement being plotted (used in axis labels and figure title).
                    fixed_combos_data   : dict Dictionary where each key is an identifier and each value is a tuple: (x_vals, y_vals, z_vals, fixed_dict)
                            - x_vals, y_vals    : array-like, coordinates for the plot (can be irregularly spaced)
                            - z_vals            : array-like, values corresponding to each (x, y) point
                            - fixed_dict        : dict, mapping of fixed sweep parameters for this group (used in dropdown label)
                    plot_type           : str, optional Type of plot to generate. Options:
                            - "3D"              : 3D surface plot
                            - "FFT"             : 3D bar chart (magnitude vs frequency)
        Returns    :
                    fig                 : plotly.graph_objects.Figure Plotly figure object with traces corresponding to all groups in `fixed_combos_data`and a 
                    dropdown menu to select the active group.
        """
        fig, dropdown_buttons ,sweepNames   = dp.go.Figure(), [] , dp.JSON["sweepNames"]
        group_trace_indices ,current_index  = []  ,0

        for i, (_, data) in enumerate(fixed_combos_data.items()):
            x_vals, y_vals, z_vals, fixed_dict = data

            if plot_type == "FFT":
                temp_fig = barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Frequency [Hz]',y_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1])
                for trace in temp_fig.data:
                    trace.visible = False  # initially hidden
                    fig.add_trace(trace)
                n_traces = len(temp_fig.data)

            else:  # 3D Surface mode
                X, Y    = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
                Z       = dp.np.full_like(X, dp.np.nan, dtype=float)
                Z[dp.np.searchsorted(dp.np.unique(y_vals), y_vals),
                dp.np.searchsorted(dp.np.unique(x_vals), x_vals)] = z_vals
                fig.add_trace(dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis',visible=False))
                n_traces = 1
            # store which traces belong to this group
            group_trace_indices.append((current_index, current_index + n_traces))
            current_index += n_traces

        # Make the first group visible by default
        first_start, first_end = group_trace_indices[0]
        for j in range(first_start, first_end): fig.data[j].visible = True

        # Create dropdown buttons
        for i, (_, data) in enumerate(fixed_combos_data.items()):
            fixed_dict          = data[3]
            start_idx, end_idx  = group_trace_indices[i]

            # Title for dropdown label - using the same format function
            fixed_title = format_fixed_title(fixed_dict, sweepNames)

            # Visibility mask: hide all except this group
            visibility = [False] * len(fig.data)
            for j in range(start_idx, end_idx): visibility[j] = True
            dropdown_buttons.append({'label': fixed_title,'method': 'update','args': [{'visible': visibility},{'title.text': f'{component}<br>{fixed_title}'}]})

        # Initial title
        first_dict  = next(iter(fixed_combos_data.values()))[3]
        first_title = format_fixed_title(first_dict, sweepNames)

        # In the make_dropdown function, update the layout_base:
        layout_base = dict(
            title=dict( text=f'{component}<br>{first_title}',x=0.5, xanchor='center', yanchor='top'),updatemenus=[dict(type='dropdown', x=1.15, y=0.5,xanchor='left', yanchor='middle',
                        buttons=dropdown_buttons,direction='down', showactive=True,bgcolor='lightgray', bordercolor='black',font={'size': 12}, pad={'r': 20})],margin=dict(r=200))

        # Set the scene configuration:
        if plot_type == "3D": layout_base['scene'] = dict(xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                                          xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))
        if plot_type == "FFT":layout_base['scene'] = dict(xaxis_title='Frequency [Hz]',yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title='Magnitude',xaxis_title_font=dict(size=10),
                                                          yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))

        fig.update_layout(**layout_base)
        return fig

    # Prepare dropdown data
    dropdown_data, fft_dropdown_data    = {}, {}

    for component in headers_array:
        comp_data = {}
        for fixed_values in fixed_combos:
            fixed_dict                  =  dict(zip(fixed_keys, fixed_values))
            full_title                  =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
            rows                        =  rows_dict[tuple(fixed_values)]
            if len(rows)                == 0: continue
            x_vals, y_vals, z_vals      =  rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), headers_array.index(component)]
            comp_data[str(fixed_dict)]  =  (x_vals, y_vals, z_vals, fixed_dict)
        dropdown_data[component]        =  comp_data

    for component in FFT_headers:
        comp_data = {}
        for fixed_values in fixed_combos:
            fixed_dict                  =  dict(zip(fixed_keys, fixed_values))
            full_title                  =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
            fft_rows                    =  fft_rows_dict[tuple(fixed_values)]
            if len(fft_rows)            == 0: continue
            y_vals                      =  fft_rows[:,2]
            x_vals                      =  dp.np.tile(dp.np.array(harmonics)*F_fund, int(dp.np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
            z_vals                      =  combined_fft_matrix[fft_rows[:,0].astype(int), FFT_headers.index(component)]
            comp_data[str(fixed_dict)]  =  (x_vals, y_vals, z_vals, fixed_dict)
        fft_dropdown_data[component]    =  comp_data

    # Create dropdown figs
    for component in headers_array:
        if dropdown_data[component]:
            list_of_plots.append(make_dropdown(full_title,component, dropdown_data[component], plot_type="3D"))

    for component in FFT_headers:
        if fft_dropdown_data[component]:
            fft_plots.append(make_dropdown(full_title, component, fft_dropdown_data[component], plot_type="FFT"))

    write_html_report(f"{html_base}_{UTC}.html", list_of_plots[1:4], base64_img, script_name, date, UTC, iterSplit=False)
    write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots[1:4], base64_img, script_name, date, UTC, iterSplit=False)

repo_3d()
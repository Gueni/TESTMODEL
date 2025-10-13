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
from torch import layout

header_path         = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
CSV_MAPS_folder     = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
input_json          = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
html_base           = r"D:\WORKSPACE\BJT-MODEL\results\result"
Y_Lengths           = [1,77,77,77,69,69,69,69,69,62,15,18,8,148]

def barchart3D(x_vals, y_vals, z_vals, title, z_title, x_title, y_title,
               colorscale='Viridis', opacity=1):
    import numpy as np
    import plotly.graph_objects as go

    fig, ann = go.Figure(), []

    x_vals, y_vals, z_vals = map(lambda arr: np.array(arr, dtype=float),
                                 (x_vals, y_vals, z_vals))

    x_unique = np.unique(x_vals)
    y_unique = np.unique(y_vals)

    # Base spacing between unique points
    dx_base = np.min(np.diff(x_unique)) if len(x_unique) > 1 else 1.0
    dy_base = np.min(np.diff(y_unique)) if len(y_unique) > 1 else 1.0

    # Scale width inversely with the number of unique bars
    # e.g. if you have 100 bars, bars will be thinner than if you have 10
    nx, ny = len(x_unique), len(y_unique)
    scale_factor = 0.6 / np.sqrt(max(nx, ny))  # adjustable constant, tweak as needed

    dx = dx_base * (0.8 * scale_factor + 0.2)  # prevent being too thin
    dy = dy_base * (0.8 * scale_factor + 0.2)

    # Keep small minimums to avoid division errors
    dx, dy = max(dx, 1e-6), max(dy, 1e-6)

    for i, z_max in enumerate(z_vals):
        x_cnt, y_cnt = x_vals[i], y_vals[i]
        x_min, x_max = x_cnt - dx/2, x_cnt + dx/2
        y_min, y_max = y_cnt - dy/2, y_cnt + dy/2
        x = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
        y = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
        z = [0, 0, 0, 0, z_max, z_max, z_max, z_max]

        # Visible bar
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            alphahull=0,
            intensity=z,
            colorscale=colorscale,
            showscale=False,          # 🚫 hides the colorbar
            opacity=opacity,
            hoverinfo='skip'
        ))

        # Transparent hover plane
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

        # Annotation on top
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
        scene=dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,
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
    relative_tol    = 0.001
    absolute_tol    = 1e-12
    headers_array, list_of_plots, fft_plots     = [], [], []
    iterSplit                                   = False
    with open(input_json) as f:config           = json.load(f)
    var1, var2                                  = config["Var1"], config["Var2"]
    sweepNames                                  = config["sweepNames"]
    base64_file                                 = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
    script_name                                 = os.path.basename(__file__)
    UTC                                         = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date                                        = str(datetime.datetime.now().replace(microsecond=0))
    with open(base64_file, 'r') as f:base64_img = ''.join(line.strip() for line in f)
    permute                                     = True
    harmonics                                   = [1, 2]

    def format_fixed_title(fixed_dict, sweepNames):
        """Format the fixed title in the same way as dropdown case"""
        return "<br>".join(" | ".join(f"{sweepNames[int(re.search(r'\d+', k).group())-1]} = {v}"for k, v in list(fixed_dict.items())[j:j+2])for j in range(0, len(fixed_dict), 2))

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
                        fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                        f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
                    f.write('</div>\n')
            else:
                    # 1 figure per row with dropdown on the right
                    f.write('<div class="plot-container">\n')
                    for fig in plots:
                        fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                        f.write(f'<div class="plot-item">{fig_html}</div>\n')
                    f.write('</div>\n')
                
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

    #?------------------------------------------------
    #?  Load headers and matrices
    #?------------------------------------------------
    mat_names           = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage","Dissipations","Elec_Stats","Temps","Thermal_Stats"]
    headers_lists       = [data if isinstance((data := json.load(open(os.path.join(header_path, f"{name}.json")))), list) else [data] for name in mat_names]
    cumsum              = np.cumsum(Y_Lengths[1:]).tolist()
    all_headers         = sum(headers_lists, [])
    fft_start, fft_end  = cumsum[5], cumsum[7]
    FFT_headers = list(map(lambda h: f"{h}_FFT", all_headers[fft_start:fft_end]))
    headers_array       = all_headers[:fft_start] + all_headers[fft_end:]
    mat_lists           = [pd.read_csv(os.path.join(CSV_MAPS_folder, f), header=None).values for f in [f"{name}_Map.csv" for name in mat_names]]
    combined_matrix     = np.hstack((mat_lists[:6] + mat_lists[8:])) 
    combined_fft_matrix = np.hstack((mat_lists[6:8]))  
    #?  Determine active sweep keys combinations
    #?------------------------------------------------
    sweep_vars          = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    sweep_keys          = list(sweep_vars.keys())
    active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0]]
    plot_2D             = len(active_sweep_keys) == 1
    single_X_key        = active_sweep_keys[0] if plot_2D else None
    all_combos          = (list(product(*sweep_vars.values())) if permute else np.where((arr := np.array(list(zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in sweep_vars.values()], arr).tolist())
    fft_combos          = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))
    #?------------------------------------------------
    #?  Plotting: 2D case
    #?------------------------------------------------
    if plot_2D:
        sweep_values = sweep_vars[single_X_key]
        sweep_label = sweepNames[int(re.search(r'\d+', single_X_key).group())-1]
        fixed_vars = {k: v for k, v in sweep_vars.items() if k != single_X_key and v != [0]}
        fixed_combos = list(product(*fixed_vars.values())) if fixed_vars else [()]

        # Clear the plot lists
        list_of_plots, fft_plots = [], []

        # --- NORMAL SIGNALS ---
        for component in headers_array:
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                z_column = headers_array.index(component)
                z_vals = combined_matrix[:len(sweep_values), z_column]

                # If all Z values are nearly the same
                if np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
                    x_plot = np.array([sweep_values[0], sweep_values[-1]])
                    z_plot = np.array([z_vals[0], z_vals[-1]])
                else:
                    x_plot = sweep_values
                    z_plot = z_vals

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=x_plot, y=z_plot, mode='lines+markers',
                    name=f"{component} {format_fixed_title(fixed_dict, sweepNames)}"
                ))

                fig.update_layout(
                    title=dict(text=f"{component}<br>{format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
                    xaxis_title=sweep_label, yaxis_title=component,
                    xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
                    xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
                    margin=dict(r=50)
                )
                list_of_plots.append(fig)

        # --- FFT SIGNALS ---
        for component in FFT_headers:
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                z_column = FFT_headers.index(component)
                z_vals = combined_fft_matrix[:len(sweep_values), z_column]
                x_vals = np.array(harmonics)

                x_plot = np.tile(x_vals, int(np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=x_plot, y=z_vals, name=f"{component} {format_fixed_title(fixed_dict, sweepNames)}"
                ))
                fig.update_layout(
                    title=dict(text=f"{component}<br>{format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
                    xaxis_title='Harmonic Order', yaxis_title=component,
                    xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
                    xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
                    margin=dict(r=50)
                )
                fft_plots.append(fig)

        # --- WRITE HTML FILES ---
        if iterSplit:
            # One HTML per component
            for idx, component in enumerate(headers_array):
                start = idx * len(fixed_combos)
                end = start + len(fixed_combos)
                component_plots = list_of_plots[start:end]
                if component_plots:
                    html_path = f"{html_base}_{component}_{UTC}.html"
                    write_html_report(html_path, component_plots, base64_img, script_name, date, UTC, iterSplit=True)

            for idx, component in enumerate(FFT_headers):
                start = idx * len(fixed_combos)
                end = start + len(fixed_combos)
                component_plots = fft_plots[start:end]
                if component_plots:
                    html_path = f"{html_base}_FFT_{component}_{UTC}.html"
                    write_html_report(html_path, component_plots, base64_img, script_name, date, UTC, iterSplit=True)
        else:
            # Group figures by their original categories
            category_groups = dict(zip(mat_names, headers_lists))
            fft_categories = {"FFT_Current": FFT_headers[:len(headers_lists[6])],
                            "FFT_Voltage": FFT_headers[len(headers_lists[6]):]}

            # Build category-based plot lists
            grouped_signal_figs = {cat: [] for cat in category_groups.keys()}
            grouped_fft_figs = {cat: [] for cat in fft_categories.keys()}

            for idx, component in enumerate(headers_array):
                start = idx * len(fixed_combos)
                end = start + len(fixed_combos)
                component_plots = list_of_plots[start:end]
                
                for cat, comps in category_groups.items():
                    if component in comps:
                        grouped_signal_figs[cat].extend(component_plots)
                        break

            for idx, component in enumerate(FFT_headers):
                start = idx * len(fixed_combos)
                end = start + len(fixed_combos)
                component_plots = fft_plots[start:end]
                
                for cat, comps in fft_categories.items():
                    if component in comps:
                        grouped_fft_figs[cat].extend(component_plots)
                        break

            # Write separate HTMLs per category
            for cat, figs in grouped_signal_figs.items():
                if figs:
                    write_html_report(f"{html_base}_{UTC}_{cat}.html",
                                    figs, base64_img, script_name, date, UTC, iterSplit=False)

            for cat, figs in grouped_fft_figs.items():
                if figs:
                    write_html_report(f"{html_base}_{UTC}_{cat}.html",
                                    figs, base64_img, script_name, date, UTC, iterSplit=False)

    else:
        #?------------------------------------------------
        #?  3D case: prepare fixed combos
        #?------------------------------------------------
        sweep_keys                  = list(sweep_vars.keys())
        other_vars                  = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and k not in [var1, var2] and eval(v) != [0] and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X")}
        fixed_keys                  = list(other_vars.keys())
        fixed_combos                = (list(product(*other_vars.values())) if permute else np.where((arr := np.array(list(zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in other_vars.values()], arr).tolist())
        rows_dict ,fft_rows_dict    = {}, {}

        for fixed_values in fixed_combos:
            fixed_dict                          = dict(zip(fixed_keys, fixed_values))
            rows                                = np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(all_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
            fft_rows                            = np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(fft_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
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
                X, Y                    =  np.meshgrid(np.unique(x_vals), np.unique(y_vals))
                Z                       =  np.full_like(X, np.nan, dtype=float)
                Xi , Yi                 =  np.searchsorted(np.unique(y_vals), y_vals), np.searchsorted(np.unique(x_vals), x_vals)
                Z[Xi,Yi]                =  z_vals
                # If all Y values are nearly the same
                if np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                        # Keep only first and last rows and columns
                        X = np.array([X[0, :], X[-1, :]])       # first & last row
                        Y = np.array([Y[0, :], Y[-1, :]])
                        Z = np.array([Z[0, :], Z[-1, :]])

                full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                fig                     =  go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title=component))])
                fig.update_layout(  title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                                    scene=dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title=sweepNames[int(re.search(r'\d+', var1).group())-1],yaxis_title=sweepNames[int(re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                            xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10)))
                list_of_plots.append(fig)

            for component, fixed_values in product(FFT_headers, fixed_combos):
                fixed_dict              =  dict(zip(fixed_keys, fixed_values))
                z_column                =  FFT_headers.index(component)
                fft_rows                =  fft_rows_dict[tuple(fixed_values)]
                if len(fft_rows)        == 0: continue
                y_vals                  =  fft_rows[:,2]
                x_vals                  =  np.tile(np.array(harmonics), int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
                z_vals                  =  combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
                full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                fig                     =  barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Harmonic Order',y_title=sweepNames[int(re.search(r'\d+', var2).group())-1])
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
            - For `plot_type="FFT"`, x-axis is labeled as "Harmonic Order" and z-axis as "Magnitude".
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
            fig, dropdown_buttons ,sweepNames   = go.Figure(), [] , config["sweepNames"]
            group_trace_indices ,current_index  = []  ,0

            for i, (_, data) in enumerate(fixed_combos_data.items()):
                x_vals, y_vals, z_vals, fixed_dict = data

                if plot_type == "FFT":
                    temp_fig = barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Harmonic Order',y_title=sweepNames[int(re.search(r'\d+', var2).group())-1])
                    for trace in temp_fig.data:
                        trace.visible = False  # initially hidden
                        fig.add_trace(trace)
                    n_traces = len(temp_fig.data)

                else:  # 3D Surface mode

                    X, Y    = np.meshgrid(np.unique(x_vals), np.unique(y_vals))
                    Z       = np.full_like(X, np.nan, dtype=float)
                    Z[np.searchsorted(np.unique(y_vals), y_vals),
                    np.searchsorted(np.unique(x_vals), x_vals)] = z_vals
                    
                    # If all Y values are nearly the same
                    if np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                        # Keep only first and last rows and columns
                        X = np.array([X[0, :], X[-1, :]])       # first & last row
                        Y = np.array([Y[0, :], Y[-1, :]])
                        Z = np.array([Z[0, :], Z[-1, :]])

                    # Add this line to flip the x-axis:
                    X = np.flip(X, axis=1)  # Flip horizontally (along columns)
                    # Also flip Z accordingly to maintain data alignment
                    Z = np.flip(Z, axis=1)

                    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis',visible=False))
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
            if plot_type == "3D": layout_base['scene'] = dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title=sweepNames[int(re.search(r'\d+', var1).group())-1],yaxis_title=sweepNames[int(re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                                            xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))
            if plot_type == "FFT":layout_base['scene'] = dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title='Harmonic Order',yaxis_title=sweepNames[int(re.search(r'\d+', var2).group())-1],zaxis_title='Magnitude',xaxis_title_font=dict(size=10),
                                                            yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))

            fig.update_layout(**layout_base)
            return fig

        #?------------------------------------------------
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
                x_vals                      =  np.tile(np.array(harmonics), int(np.ceil(len(y_vals)/len(harmonics))))[:len(y_vals)]
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

        # write_html_report(f"{html_base}_{UTC}.html", list_of_plots[:4], base64_img, script_name, date, UTC, iterSplit=False)
        # write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots[:4], base64_img, script_name, date, UTC, iterSplit=False)
        # #?------------------------------------------------
        #?  Group figures by their original categories
        #?------------------------------------------------
        category_groups = dict(zip(mat_names, headers_lists))
        fft_categories  = {"FFT_Current": FFT_headers[:len(headers_lists[6])],
                            "FFT_Voltage": FFT_headers[len(headers_lists[6]):]}

        # Build category-based plot lists
        grouped_signal_figs = {cat: [] for cat in category_groups.keys()}
        grouped_fft_figs    = {cat: [] for cat in fft_categories.keys()}

        for component, figs in zip(headers_array, list_of_plots):
                for cat, comps in category_groups.items():
                    if component in comps:
                        grouped_signal_figs[cat].append(figs)
                        break

        for component, figs in zip(FFT_headers, fft_plots):
                for cat, comps in fft_categories.items():
                    if component in comps:
                        grouped_fft_figs[cat].append(figs)
                        break

        #?------------------------------------------------
        #?  Write separate HTMLs per category
        #?------------------------------------------------
        for cat, figs in grouped_signal_figs.items():
                if figs:
                    write_html_report(f"{html_base}_{UTC}_{cat}.html",
                                    figs, base64_img, script_name, date, UTC, iterSplit=False)

        for cat, figs in grouped_fft_figs.items():
                if figs:
                    write_html_report(f"{html_base}_{UTC}_{cat}.html",
                                    figs, base64_img, script_name, date, UTC, iterSplit=False)

repo_3d()
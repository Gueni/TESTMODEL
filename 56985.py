
    def repo_3d(self,fileLog,simutil,standalone_exist=False):
        """
            Generate 2D or 3D simulation plots (including FFT) from matrix and JSON data
            and export them as interactive HTML reports. Supports both single-variable
            2D plots and multi-variable 3D surfaces with dropdown selection.

            Parameters  :   fileLog     (object)    : fileLog class object.
                            simutil     (object)    : simutil class object.
        """
        #?------------------------------------------------
        #?  Initialize Local variables and read inputs
        #?------------------------------------------------
        headers_array, list_of_plots, fft_plots     = [], [], []                                                             # Headers array and figures lists
        header_path                                 = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/"    # Headers files path
        var1, var2                                  = dp.JSON["Var1"], dp.JSON["Var2"]                                       # Varrying X lists (X2 , X3 ...)
        sweepNames                                  = dp.JSON["sweepNames"]                                                  # Names of X lists (Input Voltage ...)
        html_folder                                 = fileLog.resultfolder + "/HTML_GRAPHS/"                                 # 3D or 2D HTML result folder path
        relative_tol, absolute_tol                  = 0.001 , 1e-12                                                          # Relative tolerane / absolute tolerance for all close values skipping
        dp.os.makedirs(dp.os.path.dirname(html_folder), exist_ok=True)

        #?------------------------------------------------
        #?  Initialize Local Functions
        #?------------------------------------------------
        def format_fixed_title(fixed_dict, sweepNames=[]):
            """Format the fixed title in the same way as dropdown case"""
            return "<br>".join(" | ".join(f"{sweepNames[int(''.join(filter(str.isdigit, k)))-1]} = {v}" for k, v in list(fixed_dict.items())[j:j+2]) for j in range(0, len(fixed_dict), 2))

        def write_html_report(html_file, plots):
            """Export interactive Plotly figures to a styled HTML report with logo, metadata, and optional multi-figure layout."""
            plot_items        =   ''
            html_content      =   self.prep_html_template(Time_series = False)

            plot_items += '<div class="plot-container">\n'
            for i, fig in enumerate(plots):
                    # Set figure height for consistency
                    fig.update_layout(height=720, margin=dict(t=50, b=50, l=50, r=50))
                    fig_html = dp.to_html(fig, include_plotlyjs='cdn', full_html=False, div_id=f"plot-{i}")
                    plot_items += f'<div class="plot-item">{fig_html}</div>\n'
            plot_items += '</div>\n'

            # Replace plot items
            html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)

            # Write the populated HTML
            with open(html_file, 'w', encoding='utf-8') as file: file.write(html_content)
            file.close()

        def make_dropdown(full_title, component, fixed_combos_data, plot_type="3D"):
                """
                Create a Plotly figure with multiple traces (3D Surface or 3D bar chart) and a dropdown menu
                to switch between different sets of fixed parameter combinations.

                Each item in `fixed_combos_data` corresponds to a group of traces representing a fixed combination
                of parameters. The dropdown allows the user to toggle visibility between these groups.

                - Each group of traces is initially hidden except the first group.
                - Dropdown menu entries are dynamically generated using the `fixed_dict` values.
                - Figure layout is automatically adjusted for scene axis titles and font sizes.
                - For `plot_type="FFT"`, x-axis is labeled as "Harmonics" and z-axis as "Magnitude".
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
                        temp_fig = self.barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Harmonics',y_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1])
                        for trace in temp_fig.data:
                            trace.visible = False  # initially hidden
                            fig.add_trace(trace)
                        n_traces = len(temp_fig.data)

                    else:  # 3D Surface mode
                        X, Y    = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
                        Z       = dp.np.full_like(X, dp.np.nan, dtype=float)
                        Z[dp.np.searchsorted(dp.np.unique(y_vals), y_vals),dp.np.searchsorted(dp.np.unique(x_vals), x_vals)] = z_vals
                        # If all Y values are nearly the same
                        if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                                # Keep only first and last rows and columns
                                X = dp.np.array([X[0, :], X[-1, :]])       # first & last row
                                Y = dp.np.array([Y[0, :], Y[-1, :]])
                                Z = dp.np.array([Z[0, :], Z[-1, :]])
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
                if plot_type == "3D": layout_base['scene'] = dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                                                xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))
                if plot_type == "FFT":layout_base['scene'] = dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title='Harmonics',yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title='Magnitude',xaxis_title_font=dict(size=10),
                                                                yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10))

                fig.update_layout(**layout_base)
                return fig
            #?------------------------------------------------
            #?  Load headers and matrices
            #?------------------------------------------------

                import os, natsort
        

        #!========================================================
        import os, natsort
        csv_maps_dir        = dp.os.path.join(fileLog.resultfolder, "CSV_MAPS")

        if standalone_exist:
            # Load headers from time series standalone files
            csv_time_series_dir     = dp.os.path.join(fileLog.resultfolder, "CSV_TIME_SERIES")
            time_series_files       = natsort.natsorted(glob.glob(csv_time_series_dir + "/*Standalone*.csv"))
            
            if time_series_files:
                df              = dp.pd.read_csv(time_series_files[0])
                base_headers    = df.columns[1:].tolist()  # Skip first column (Time)
                base_headers    = [dp.re.sub(r'[^a-zA-Z0-9]', '_', header) for header in base_headers]
            
            mat_names           = ["Standalone_RMS","Standalone_AVG","Standalone_MAX","Standalone_MIN","Standalone_FFT"]
            
            # Load matrices from standalone MAP files
            standalone_matrices = {}
            all_headers = []  # Collect all headers from all files
            
            for file_type, file_name in zip(['RMS', 'AVG', 'MAX', 'MIN', 'FFT'], mat_names):
                file_path = dp.os.path.join(csv_maps_dir, file_name + '_MAP.csv')
                if dp.os.path.exists(file_path):
                    df = dp.pd.read_csv(file_path, header=None)
                    # Skip header row if present
                    if df.shape[0] > 0 and any(isinstance(val, str) for val in df.iloc[0]):
                        df = df.iloc[1:]
                    standalone_matrices[file_type] = df.values.astype(float)
                    
                    # Generate headers for this file type
                    if file_type == 'FFT':
                        # FFT headers - use base headers or create numbered headers
                        file_headers = [f"{h}_FFT" for h in base_headers] if base_headers else [f"FFT_{i}" for i in range(df.shape[1])]
                    else:
                        # RMS/AVG/MAX/MIN headers
                        file_headers = [f"{h}_{file_type}" for h in base_headers] if base_headers else [f"{file_type}_{i}" for i in range(df.shape[1])]
                    
                    all_headers.append(file_headers)
            
            # Build headers_lists from collected headers
            headers_lists = all_headers  # This now has 5 lists: RMS, AVG, MAX, MIN, FFT headers
            
            # Extract headers_array (all non-FFT headers combined)
            headers_array = []
            for i in range(4):  # First 4 are RMS, AVG, MAX, MIN
                headers_array.extend(headers_lists[i])
            
            # Extract FFT_headers (5th list)
            FFT_headers = headers_lists[4] if len(headers_lists) > 4 else []
            
            # Combine non-FFT matrices
            combined_matrix = None
            for file_type in ['RMS', 'AVG', 'MAX', 'MIN']:
                if file_type in standalone_matrices:
                    if combined_matrix is None:
                        combined_matrix = standalone_matrices[file_type]
                    else:
                        combined_matrix = dp.np.hstack((combined_matrix, standalone_matrices[file_type]))
            
            # FFT matrix
            combined_fft_matrix = standalone_matrices.get('FFT')
            
        else:
            #!========================================================
            # Define matrix and header name same order as in Y_length and get the headers lists accordingly.
            mat_names           = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage","Dissipations","Elec_Stats","Temps","Thermal_Stats"]
            headers_lists       = [data if isinstance((data := dp.json.load(open(dp.os.path.join(header_path, f"{name}.json")))), list) else [data] for name in mat_names]

            # Define sum cumulative increment and slice to get signals and fft headers lists.
            cumsum              = dp.np.cumsum(dp.Y_Length[1:]).tolist()
            all_headers         = sum(headers_lists, [])
            fft_start, fft_end  = cumsum[5], cumsum[7]
            FFT_headers         = all_headers[fft_start:fft_end]
            headers_array       = all_headers[:fft_start] + all_headers[fft_end:]

            # Combined matrix for signals and ffts
            combined_matrix     = dp.np.hstack((simutil.MAT_list[:6] + simutil.MAT_list[8:12]))
            combined_fft_matrix = dp.np.hstack((simutil.MAT_list[6:8]))

        signal_units        = [dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in headers_array]
        FFT_units           = [dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in FFT_headers]

        #?------------------------------------------------
        #?  Determine active sweep keys combinations
        #?------------------------------------------------
        # Get all sweeping Xlist from json file and determine which are active in the simulation sweep
        sweep_vars          = {k: eval(v) for k, v in dp.JSON.items() if dp.re.fullmatch(r"X\d+", k) and eval(v) != [0]}
        sweep_keys          = list(sweep_vars.keys())
        active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0] and len(v)>1]

        # Decide 2D plotting or 3D  based on number of active sweep Xlists and use the single X list for 2D if it is the case
        plot_2D             = len(active_sweep_keys) == 1
        single_X_key        = active_sweep_keys[0] if plot_2D else None

        # Generate all combinations for the sweep based on algorithm (permute = True : permuted sweeps combo | permute = False : non permuted sequential sweeps combo)
        all_combos          = (list(dp.product(*sweep_vars.values())) if dp.JSON["permute"] else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in sweep_vars.values()], arr).tolist())

        # For FFT combinations it is the same but repeated for the number of harmonics
        if dp.JSON['FFT']   : fft_combos          = list(map(tuple, dp.np.repeat(all_combos, len(dp.harmonics), axis=0).astype(object)))
        #?------------------------------------------------
        #?  Plotting: 2D case
        #?------------------------------------------------
        if plot_2D:
            sweep_values = sweep_vars[single_X_key]
            sweep_label = sweepNames[int(dp.re.search(r'\d+', single_X_key).group())-1]
            fixed_vars = {k: v for k, v in sweep_vars.items() if k != single_X_key and v != [0]}
            fixed_combos = list(dp.product(*fixed_vars.values())) if fixed_vars else [()]

            # Clear the plot lists
            list_of_plots, fft_plots = [], []

            # --- NORMAL SIGNALS ---
            for component in headers_array:
                for fixed_values in fixed_combos:
                    fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                    z_column = headers_array.index(component)
                    z_vals = combined_matrix[:len(sweep_values), z_column]

                    # If all Z values are nearly the same
                    if dp.np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
                        x_plot = dp.np.array([sweep_values[0], sweep_values[-1]])
                        z_plot = dp.np.array([z_vals[0], z_vals[-1]])
                    else:
                        x_plot = sweep_values
                        z_plot = z_vals

                    fig = dp.go.Figure()
                    fig.add_trace(dp.go.Scatter(
                        x=sweep_values, y=z_vals, mode='lines',
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
                    x_vals = dp.np.array(dp.harmonics)
                    x_plot = dp.np.tile(x_vals, int(dp.np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]

                    fig = dp.go.Figure()
                    fig.add_trace(dp.go.Bar(
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
            if dp.JSON["iterSplit"]:
                # One HTML per component
                for idx, component in enumerate(headers_array):
                    start = idx * len(fixed_combos)
                    end = start + len(fixed_combos)
                    component_plots = list_of_plots[start:end]
                    if component_plots:
                        if standalone_exist:
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_{component}_{self.utc}.html"))).replace('\\','/'), component_plots)
                        else:   
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{component}_{self.utc}.html"))).replace('\\','/'), component_plots)

                for idx, component in enumerate(FFT_headers):
                    start = idx * len(fixed_combos)
                    end = start + len(fixed_combos)
                    component_plots = fft_plots[start:end]
                    if component_plots:
                        if standalone_exist:
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_FFT_{component}_{self.utc}.html"))).replace('\\','/'), component_plots)
                        else:
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{component}_{self.utc}.html"))).replace('\\','/'), component_plots)
            else:
                # Group figures by their original categories
                category_groups = dict(zip(mat_names, headers_lists))
                if standalone_exist:
                    # For standalone, simpler FFT categorization
                    fft_categories = {"Standalone_FFT": FFT_headers}  # All FFT in one category
                else:
                    # Original logic for normal data
                    fft_categories = {"FFT_Current": FFT_headers[:len(headers_lists[6])],"FFT_Voltage": FFT_headers[len(headers_lists[6]):]}

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
                    if figs:write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{cat}_{self.utc}.html"))).replace('\\','/'),figs)
                if dp.JSON["FFT"]:
                    for cat, figs in grouped_fft_figs.items():
                        if figs:write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{cat}_{self.utc}.html"))).replace('\\','/'),figs)
        else:
            #?------------------------------------------------
            #?  3D case: prepare fixed combos
            #?------------------------------------------------
            # Get all the other active Xlists which are not the chosen varying Xlists in json input and generate the fixed constants
            # combinations same logic with permute variable
            sweep_keys                  = list(sweep_vars.keys())
            other_vars                  = {k: eval(v) for k, v in dp.JSON.items() if dp.re.fullmatch(r"X\d+", k) and k not in [var1, var2] and eval(v) != [0] and not dp.JSON["sweepNames"][int(dp.re.search(r'\d+', k).group())-1].startswith("X")}
            fixed_keys                  = list(other_vars.keys())
            fixed_combos                = (list(dp.product(*other_vars.values())) if dp.JSON["permute"] else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in other_vars.values()], arr).tolist())
            rows_dict ,fft_rows_dict    = {}, {}

            # Return the Selected Rows of data for each fixed combo
            for fixed_values in fixed_combos:
                fixed_dict                          = dict(zip(fixed_keys, fixed_values))
                rows                                = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(all_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
                rows_dict[tuple(fixed_values)]      = rows
                if dp.JSON['FFT']:
                    fft_rows                            = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) for i, combo in enumerate(fft_combos) if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
                    fft_rows_dict[tuple(fixed_values)]  = fft_rows
            #?------------------------------------------------
            #?  Case A: iterSplit=True → per-component HTML, no dropdown
            #?------------------------------------------------
            if dp.JSON["iterSplit"]:

                # 3D Plots for each component in normal signals matrix
                for component, fixed_values in dp.product(headers_array, fixed_combos):
                    fixed_dict              =  dict(zip(fixed_keys, fixed_values))
                    z_column                =  headers_array.index(component)
                    rows                    =  rows_dict[tuple(fixed_values)]
                    x_vals, y_vals, z_vals  =  rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), z_column]
                    X, Y                    =  dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
                    Z                       =  dp.np.full_like(X, dp.np.nan, dtype=float)
                    Xi , Yi                 =  dp.np.searchsorted(dp.np.unique(y_vals), y_vals), dp.np.searchsorted(dp.np.unique(x_vals), x_vals)
                    Z[Xi,Yi]                =  z_vals
                    # If all Y values are nearly the same
                    if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                            # Keep only first and last rows and columns
                            X = dp.np.array([X[0, :], X[-1, :]])       # first & last row
                            Y = dp.np.array([Y[0, :], Y[-1, :]])
                            Z = dp.np.array([Z[0, :], Z[-1, :]])

                    full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                    fig                     =  dp.go.Figure(data=[dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict())])
                    fig.update_layout(  title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
                                        scene=dict(xaxis=dict(autorange='reversed') ,  yaxis=dict(autorange='reversed') ,xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],
                                        yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],zaxis_title=component,
                                                xaxis_title_font=dict(size=10),yaxis_title_font=dict(size=10),zaxis_title_font=dict(size=10),xaxis_tickfont=dict(size=10),yaxis_tickfont=dict(size=10),zaxis_tickfont=dict(size=10)))
                    list_of_plots.append(fig)

                # 3D Plots for each component in FFT matrix
                if dp.JSON['FFT']:
                    for component, fixed_values in dp.product(FFT_headers, fixed_combos):
                        fixed_dict              =  dict(zip(fixed_keys, fixed_values))
                        z_column                =  FFT_headers.index(component)
                        fft_rows                =  fft_rows_dict[tuple(fixed_values)]
                        y_vals                  =  fft_rows[:,2]
                        x_vals                  =  dp.np.tile(dp.np.array(dp.harmonics), int(dp.np.ceil(len(y_vals)/len(dp.harmonics))))[:len(y_vals)]
                        z_vals                  =  combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
                        full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                        fig                     =  self.barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',x_title='Harmonics',y_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1])
                        fft_plots.append(fig)

                # Write multiple html files each component has a separate file in which there are multiple plots each for a constants combination
                for idx, component in enumerate(headers_array):
                    start, end = idx*max(1,len(list_of_plots)//len(headers_array)), (idx+1)*max(1,len(list_of_plots)//len(headers_array))
                    if standalone_exist:
                        write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_{self.utc}_{component}.html"))).replace('\\','/'), list_of_plots[start:end])
                    else:
                        write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{self.utc}_{component}.html"))).replace('\\','/'), list_of_plots[start:end])

                if dp.JSON['FFT']:
                    for idx, component in enumerate(FFT_headers):
                        start, end = idx*max(1,len(fft_plots)//len(FFT_headers)), (idx+1)*max(1,len(fft_plots)//len(FFT_headers))
                        if standalone_exist:
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_FFT_{self.utc}_{component}.html"))).replace('\\','/'), fft_plots[start:end])
                        else:
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{self.utc}_{component}.html"))).replace('\\','/'), fft_plots[start:end])
            else:
                #?------------------------------------------------
                #?  Case B: iterSplit=False → 1 file ,use dropdowns
                #?------------------------------------------------
                # Prepare dropdown data
                dropdown_data, fft_dropdown_data    = {}, {}

                # Generate dropdown menus for normal signals
                for component in headers_array:
                    comp_data = {}
                    for fixed_values in fixed_combos:
                        fixed_dict                  =  dict(zip(fixed_keys, fixed_values))
                        full_title                  =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                        rows                        =  rows_dict[tuple(fixed_values)]
                        x_vals, y_vals, z_vals      =  rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), headers_array.index(component)]
                        comp_data[str(fixed_dict)]  =  (x_vals, y_vals, z_vals, fixed_dict)
                    dropdown_data[component]        =  comp_data

                # Generate dropdown menus for FFT signals
                if dp.JSON['FFT']:
                    for component in FFT_headers:
                        comp_data = {}
                        for fixed_values in fixed_combos:
                            fixed_dict                  =  dict(zip(fixed_keys, fixed_values))
                            full_title                  =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                            fft_rows                    =  fft_rows_dict[tuple(fixed_values)]
                            y_vals                      =  fft_rows[:,2]
                            x_vals                      =  dp.np.tile(dp.np.array(dp.harmonics), int(dp.np.ceil(len(y_vals)/len(dp.harmonics))))[:len(y_vals)]
                            z_vals                      =  combined_fft_matrix[fft_rows[:,0].astype(int), FFT_headers.index(component)]
                            comp_data[str(fixed_dict)]  =  (x_vals, y_vals, z_vals, fixed_dict)
                        fft_dropdown_data[component]    =  comp_data

                # Create dropdown figures for normal signals
                for component in headers_array:
                    if dropdown_data[component]:list_of_plots.append(make_dropdown(full_title,component, dropdown_data[component], plot_type="3D"))

                # Create dropdown figures for FFT signals
                if dp.JSON['FFT']:
                    for component in FFT_headers:
                        if fft_dropdown_data[component]:fft_plots.append(make_dropdown(full_title, component, fft_dropdown_data[component], plot_type="FFT"))

                #?------------------------------------------------
                #?  Group figures by their original categories
                #?------------------------------------------------
                category_groups = dict(zip(mat_names, headers_lists))
                if standalone_exist:
                    # For standalone, simpler FFT categorization
                    fft_categories = {"Standalone_FFT": FFT_headers}  # All FFT in one category
                else:
                    # Original logic for normal data
                    fft_categories = {"FFT_Current": FFT_headers[:len(headers_lists[6])],"FFT_Voltage": FFT_headers[len(headers_lists[6]):]}

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
                    if figs:write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{self.utc}_{cat}.html"))).replace('\\','/'), figs)
                if dp.JSON["FFT"]:
                    for cat, figs in grouped_fft_figs.items():
                        if figs:write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{self.utc}_{cat}.html"))).replace('\\','/'), figs)

 
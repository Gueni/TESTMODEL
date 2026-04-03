def graph_scopes(self, fileLog, simutil, standalone_exist=False):
    """
    Generate 2D or 3D simulation plots (including FFT) from matrix and JSON data
    and export them as interactive HTML reports. Supports both single-variable
    2D plots and multi-variable 3D surfaces with dropdown selection.
    """
    # Initialize and get configuration
    config = self._initialize_graph_config(fileLog, simutil, standalone_exist)
    
    # Determine plot type and prepare data
    plot_type = self._determine_plot_type(config)
    sweep_data = self._prepare_sweep_data(config, simutil)
    
    # Generate and export plots
    if plot_type == "2D":
        self._generate_2d_plots(config, sweep_data)
    else:
        self._generate_3d_plots(config, sweep_data)

def _initialize_graph_config(self, fileLog, simutil, standalone_exist):
    """Initialize common configuration and data structures"""
    config = {
        'headers_array': [],
        'list_of_plots': [],
        'fft_plots': [],
        'html_folder': f"{fileLog.resultfolder}/HTML_GRAPHS/",
        'relative_tol': 0.001,
        'absolute_tol': 1e-12,
        'standalone_exist': standalone_exist,
        'utc': self.utc,
        'iterSplit': dp.iterSplit,
        'fft_enabled': dp.JSON["FFT"],
        'perturbation': dp.JSON["perturbation"],
        'sweepNames': dp.JSON["sweepNames"],
        'harmonics': dp.harmonics,
        'permute': dp.JSON["permute"]
    }
    
    dp.os.makedirs(config['html_folder'], exist_ok=True)
    
    # Load matrix data
    self._load_matrix_data(config, fileLog, simutil, standalone_exist)
    
    return config

def _load_matrix_data(self, config, fileLog, simutil, standalone_exist):
    """Load headers and matrices based on standalone or normal mode"""
    if standalone_exist:
        self._load_standalone_data(config, fileLog)
    else:
        self._load_normal_data(config, simutil)

def _load_standalone_data(self, config, fileLog):
    """Load data for standalone mode"""
    csv_maps_dir = f"{fileLog.resultfolder}/CSV_MAPS"
    csv_time_series_dir = f"{fileLog.resultfolder}/CSV_TIME_SERIES"
    
    time_series_files = fileLog.natsort_files(csv_time_series_dir, standalone=True)
    if time_series_files:
        df = dp.pd.read_csv(time_series_files[0])
        base_headers = [dp.re.sub(r'[^a-zA-Z0-9]', '_', header) for header in df.columns[1:].tolist()]
    
    # Determine matrix names based on sensitivity
    if (config['perturbation'] != 0) and (dp.JSON["nvars"] is None):
        mat_names = ["Standalone_RMS","Standalone_AVG","Standalone_MAX","Standalone_MIN",
                     "Standalone_RMS_Sens","Standalone_AVG_Sens","Standalone_MAX_Sens",
                     "Standalone_MIN_Sens","Standalone_FFT","Standalone_FFT_Sens"]
        mat_suffix = ['RMS', 'AVG', 'MAX', 'MIN', 'RMS_Sens', 'AVG_Sens', 'MAX_Sens', 'MIN_Sens', 'FFT', 'FFT_Sens']
        d, N = 8, 2
    else:
        mat_names = ["Standalone_RMS","Standalone_AVG","Standalone_MAX","Standalone_MIN","Standalone_FFT"]
        mat_suffix = ['RMS', 'AVG', 'MAX', 'MIN', 'FFT']
        d, N = 4, 1
    
    # Load matrices
    standalone_matrices = {}
    headers_lists = []
    
    for file_type, file_name in zip(mat_suffix, mat_names):
        file_path = dp.os.path.join(csv_maps_dir, file_name + '_Map.csv')
        df = dp.pd.read_csv(file_path, header=None)
        standalone_matrices[file_type] = df.values.astype(float)
        file_headers = [f"{h}_{file_type}" for h in base_headers] if base_headers else [f"{file_type}_{i}" for i in range(df.shape[1])]
        headers_lists.append(file_headers)
    
    # Build headers array
    for i in range(d):
        config['headers_array'].extend(headers_lists[i])
    config['FFT_headers'] = headers_lists[d] * N
    
    # Combine matrices
    combined_matrix = None
    for file_type in mat_suffix[0:d]:
        if combined_matrix is None:
            combined_matrix = standalone_matrices[file_type]
        else:
            combined_matrix = dp.np.hstack((combined_matrix, standalone_matrices[file_type]))
    config['combined_matrix'] = combined_matrix
    
    # FFT matrix
    if (config['perturbation'] != 0) and (dp.JSON["nvars"] is None):
        config['combined_fft_matrix'] = dp.np.hstack((standalone_matrices.get('FFT'), standalone_matrices.get('FFT_Sens')))
    else:
        config['combined_fft_matrix'] = standalone_matrices.get('FFT')
    
    config['mat_names'] = mat_names
    config['headers_lists'] = headers_lists

def _load_normal_data(self, config, simutil):
    """Load data for normal mode"""
    header_path = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/"
    mat_names = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages",
                 "RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage",
                 "Dissipations","Elec_Stats","Temps","Thermal_Stats"]
    
    headers_lists = [data if isinstance((data := dp.json.load(open(dp.os.path.join(header_path, f"{name}.json")))), list) else [data] for name in mat_names]
    
    cumsum = dp.np.cumsum(dp.Y_Length[1:]).tolist()
    all_headers = sum(headers_lists, [])
    fft_start, fft_end = cumsum[5], cumsum[7]
    config['FFT_headers'] = all_headers[fft_start:fft_end]
    config['headers_array'] = all_headers[:fft_start] + all_headers[fft_end:]
    
    config['combined_matrix'] = dp.np.hstack((simutil.MAT_list[:6] + simutil.MAT_list[8:12]))
    config['combined_fft_matrix'] = dp.np.hstack((simutil.MAT_list[6:8]))
    config['mat_names'] = mat_names
    config['headers_lists'] = headers_lists

def _determine_plot_type(self, config):
    """Determine if we should do 2D or 3D plotting"""
    sweep_vars = {k: v for k, v in self.Xs_to_dict(dp.simutil.sweepMatrix).items() if v != [0]}
    active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
    return "2D" if len(active_sweep_keys) == 1 else "3D"

def _prepare_sweep_data(self, config, simutil):
    """Prepare sweep combinations and related data"""
    sweep_vars = {k: v for k, v in self.Xs_to_dict(simutil.sweepMatrix).items() if v != [0]}
    sweep_keys = list(sweep_vars.keys())
    active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
    
    # Generate combinations
    all_combos = self._generate_combinations(sweep_vars, config['permute'])
    fft_combos = list(map(tuple, dp.np.repeat(all_combos, len(config['harmonics']), axis=0).astype(object))) if config['fft_enabled'] else None
    
    return {
        'sweep_vars': sweep_vars,
        'sweep_keys': sweep_keys,
        'active_sweep_keys': active_sweep_keys,
        'all_combos': all_combos,
        'fft_combos': fft_combos
    }

def _generate_combinations(self, sweep_vars, permute):
    """Generate combinations based on permute flag"""
    import itertools
    
    if permute:
        combos = list(itertools.product(*sweep_vars.values()))
    else:
        arr = dp.np.array(
            list(itertools.zip_longest(*sweep_vars.values(), fillvalue=None)),
            dtype=object
        )
        filled = dp.np.where(
            arr == None,
            [v[-1] for v in sweep_vars.values()],
            arr
        )
        combos = filled.tolist()
    
    return [tuple(c) for c in combos]

def _generate_2d_plots(self, config, sweep_data):
    """Generate 2D plots"""
    single_X_key = sweep_data['active_sweep_keys'][0]
    sweep_values = sweep_data['sweep_vars'][single_X_key]
    sweep_label = config['sweepNames'][int(dp.re.search(r'\d+', single_X_key).group())-1]
    
    # Get fixed variables
    fixed_vars = {k: v for k, v in sweep_data['sweep_vars'].items() 
                  if k != single_X_key and v != [0]}
    fixed_combos = self._generate_combinations(fixed_vars, config['permute']) if fixed_vars else [()]
    
    # Generate signal plots
    signal_plots = self._generate_2d_signal_plots(
        config, sweep_values, sweep_label, fixed_vars, fixed_combos
    )
    
    # Generate FFT plots if enabled
    fft_plots = []
    if config['fft_enabled']:
        fft_plots = self._generate_2d_fft_plots(
            config, sweep_values, fixed_vars, fixed_combos
        )
    
    # Export plots
    self._export_2d_plots(config, signal_plots, fft_plots, fixed_combos)

def _generate_2d_signal_plots(self, config, sweep_values, sweep_label, fixed_vars, fixed_combos):
    """Generate 2D signal plots"""
    plots = []
    
    for component in config['headers_array']:
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
            z_column = config['headers_array'].index(component)
            z_vals = config['combined_matrix'][:len(sweep_values), z_column]
            
            x_plot, z_plot = self._prepare_2d_plot_data(
                sweep_values, z_vals, config['perturbation'], config['relative_tol'], config['absolute_tol']
            )
            
            fig = self._create_2d_line_plot(
                x_plot, z_plot, component, fixed_dict, sweep_label, config['sweepNames']
            )
            plots.append(fig)
    
    return plots

def _generate_2d_fft_plots(self, config, sweep_values, fixed_vars, fixed_combos):
    """Generate 2D FFT plots"""
    plots = []
    
    for component in config['FFT_headers']:
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
            z_column = config['FFT_headers'].index(component)
            z_vals = config['combined_fft_matrix'][:len(sweep_values), z_column]
            
            x_vals = dp.np.array(config['harmonics'])
            x_plot = dp.np.tile(x_vals, int(dp.np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]
            
            fig = self._create_2d_bar_plot(
                x_plot, z_vals, component, fixed_dict, config['sweepNames']
            )
            plots.append(fig)
    
    return plots

def _prepare_2d_plot_data(self, x_vals, y_vals, perturbation, rel_tol, abs_tol):
    """Prepare data for 2D plotting, handling constant values"""
    if perturbation == 0:
        if dp.np.allclose(y_vals, y_vals[0], rtol=rel_tol, atol=abs_tol):
            return dp.np.array([x_vals[0], x_vals[-1]]), dp.np.array([y_vals[0], y_vals[-1]])
    return x_vals, y_vals

def _create_2d_line_plot(self, x_vals, y_vals, component, fixed_dict, sweep_label, sweepNames):
    """Create 2D line plot"""
    fig = dp.go.Figure()
    fig.add_trace(dp.go.Scatter(
        x=x_vals, y=y_vals, mode='lines',
        name=f"{component} {self._format_fixed_title(fixed_dict, sweepNames)}"
    ))
    fig.update_layout(
        title=dict(text=f"{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
        xaxis_title=sweep_label, yaxis_title=component,
        xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
        xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
        margin=dict(r=50)
    )
    return fig

def _create_2d_bar_plot(self, x_vals, y_vals, component, fixed_dict, sweepNames):
    """Create 2D bar plot for FFT"""
    fig = dp.go.Figure()
    fig.add_trace(dp.go.Bar(
        x=x_vals, y=y_vals,
        name=f"{component} {self._format_fixed_title(fixed_dict, sweepNames)}"
    ))
    fig.update_layout(
        title=dict(text=f"{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
        xaxis_title='Harmonic Order', yaxis_title=component,
        xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
        xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
        margin=dict(r=50)
    )
    return fig

def _generate_3d_plots(self, config, sweep_data):
    """Generate 3D plots"""
    var1, var2 = dp.JSON["Var1"], dp.JSON["Var2"]
    
    # Get fixed combinations
    other_vars = self._get_other_variables(sweep_data['sweep_vars'], var1, var2, config['sweepNames'])
    fixed_combos = self._generate_combinations(other_vars, config['permute'])
    
    # Prepare row indices for data extraction
    rows_dict, fft_rows_dict = self._prepare_3d_row_indices(
        sweep_data, other_vars, fixed_combos
    )
    
    if config['iterSplit']:
        # Per-component HTML files
        signal_plots = self._generate_3d_signal_plots_per_component(
            config, rows_dict, fixed_combos, var1, var2
        )
        fft_plots = self._generate_3d_fft_plots_per_component(
            config, fft_rows_dict, fixed_combos, var2
        ) if config['fft_enabled'] else []
        self._export_3d_plots_per_component(config, signal_plots, fft_plots)
    else:
        # Single HTML with dropdowns
        signal_plots, fft_plots = self._generate_3d_dropdown_plots(
            config, rows_dict, fft_rows_dict, fixed_combos, var1, var2
        )
        self._export_3d_grouped_plots(config, signal_plots, fft_plots)

def _get_other_variables(self, sweep_vars, var1, var2, sweepNames):
    """Get other variables that are not the main varying ones"""
    return {
        k: v for k, v in sweep_vars.items() 
        if dp.re.fullmatch(r"X\d+", k) and k not in [var1, var2] 
        and v != [0] and not sweepNames[int(dp.re.search(r'\d+', k).group())-1].startswith("X")
    }

def _prepare_3d_row_indices(self, sweep_data, other_vars, fixed_combos):
    """Prepare row indices for data extraction in 3D plots"""
    rows_dict = {}
    fft_rows_dict = {}
    sweep_keys = sweep_data['sweep_keys']
    var1, var2 = dp.JSON["Var1"], dp.JSON["Var2"]
    
    for fixed_values in fixed_combos:
        fixed_keys = list(other_vars.keys())
        fixed_dict = dict(zip(fixed_keys, fixed_values))
        
        rows = dp.np.array([
            (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) 
            for i, combo in enumerate(sweep_data['all_combos']) 
            if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())
        ])
        rows_dict[tuple(fixed_values)] = rows
        
        if sweep_data['fft_combos'] is not None:
            fft_rows = dp.np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) 
                for i, combo in enumerate(sweep_data['fft_combos']) 
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())
            ])
            fft_rows_dict[tuple(fixed_values)] = fft_rows
    
    return rows_dict, fft_rows_dict

def _generate_3d_signal_plots_per_component(self, config, rows_dict, fixed_combos, var1, var2):
    """Generate 3D signal plots for per-component export"""
    plots = []
    
    for component in config['headers_array']:
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(list(rows_dict.keys())[0] if rows_dict else [], fixed_values))
            z_column = config['headers_array'].index(component)
            rows = rows_dict[tuple(fixed_values)]
            
            x_vals, y_vals, z_vals = rows[:,1], rows[:,2], config['combined_matrix'][rows[:,0].astype(int), z_column]
            
            fig = self._create_3d_surface_plot(
                x_vals, y_vals, z_vals, component, fixed_dict, 
                var1, var2, config['sweepNames'], config['perturbation'],
                config['relative_tol'], config['absolute_tol'], config['permute']
            )
            plots.append(fig)
    
    return plots

def _generate_3d_fft_plots_per_component(self, config, fft_rows_dict, fixed_combos, var2):
    """Generate 3D FFT plots for per-component export"""
    plots = []
    
    for component in config['FFT_headers']:
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(list(fft_rows_dict.keys())[0] if fft_rows_dict else [], fixed_values))
            z_column = config['FFT_headers'].index(component)
            fft_rows = fft_rows_dict[tuple(fixed_values)]
            
            y_vals = fft_rows[:,2]
            x_vals = dp.np.tile(dp.np.array(config['harmonics']), 
                               int(dp.np.ceil(len(y_vals)/len(config['harmonics']))))[:len(y_vals)]
            z_vals = config['combined_fft_matrix'][fft_rows[:,0].astype(int), z_column]
            
            full_title = f'{component}<br>{self._format_fixed_title(fixed_dict, config["sweepNames"])}'
            fig = self.barchart3D(
                x_vals, y_vals, z_vals, full_title, 'Magnitude',
                x_title='Harmonics', 
                y_title=config['sweepNames'][int(dp.re.search(r'\d+', var2).group())-1]
            )
            plots.append(fig)
    
    return plots

def _create_3d_surface_plot(self, x_vals, y_vals, z_vals, component, fixed_dict, 
                    var1, var2, sweepNames, perturbation, rel_tol, abs_tol, permute):
    """Create 3D surface plot"""

    full_title = f'{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}'

    if permute:
        # ===== SURFACE MODE =====
        X, Y = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
        Z = dp.np.full_like(X, dp.np.nan, dtype=float)

        Xi = dp.np.searchsorted(dp.np.unique(y_vals), y_vals)
        Yi = dp.np.searchsorted(dp.np.unique(x_vals), x_vals)
        Z[Xi, Yi] = z_vals

        # Handle constant values
        if perturbation == 0:
            if dp.np.allclose(z_vals, Z[0, 0], rtol=rel_tol, atol=abs_tol):
                X = dp.np.array([X[0, :], X[-1, :]])
                Y = dp.np.array([Y[0, :], Y[-1, :]])
                Z = dp.np.array([Z[0, :], Z[-1, :]])

        fig = dp.go.Figure(data=[
            dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')
        ])

    else:
        # ===== TRAJECTORY MODE (permute=False) =====
        fig = dp.go.Figure(data=[
            dp.go.Scatter3d(
                x=x_vals,
                y=y_vals,
                z=z_vals,
                mode='lines+markers'   # 🔥 important
            )
        ])

    fig.update_layout(
        title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
        scene=dict(
            xaxis=dict(autorange='reversed'),
            yaxis=dict(autorange='reversed'),
            xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],
            yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],
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

def _generate_3d_dropdown_plots(self, config, rows_dict, fft_rows_dict, fixed_combos, var1, var2):
    """Generate 3D plots with dropdown menus"""
    signal_plots = []
    fft_plots = []
    
    # Prepare dropdown data for signals
    for component in config['headers_array']:
        comp_data = {}
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(list(rows_dict.keys())[0] if rows_dict else [], fixed_values))
            rows = rows_dict[tuple(fixed_values)]
            x_vals, y_vals, z_vals = rows[:,1], rows[:,2], config['combined_matrix'][rows[:,0].astype(int), config['headers_array'].index(component)]
            comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
        
        if comp_data:
            signal_plots.append(self.make_dropdown(None, component, comp_data, plot_type="3D"))
    
    # Prepare dropdown data for FFT
    if config['fft_enabled']:
        for component in config['FFT_headers']:
            comp_data = {}
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(list(fft_rows_dict.keys())[0] if fft_rows_dict else [], fixed_values))
                fft_rows = fft_rows_dict[tuple(fixed_values)]
                y_vals = fft_rows[:,2]
                x_vals = dp.np.tile(dp.np.array(config['harmonics']), 
                                   int(dp.np.ceil(len(y_vals)/len(config['harmonics']))))[:len(y_vals)]
                z_vals = config['combined_fft_matrix'][fft_rows[:,0].astype(int), config['FFT_headers'].index(component)]
                comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
            
            if comp_data:
                fft_plots.append(self.make_dropdown(None, component, comp_data, plot_type="FFT"))
    
    return signal_plots, fft_plots

def _export_2d_plots(self, config, signal_plots, fft_plots, fixed_combos):
    """Export 2D plots to HTML files"""
    if config['iterSplit']:
        self._export_2d_plots_per_component(config, signal_plots, fft_plots, fixed_combos)
    else:
        self._export_2d_grouped_plots(config, signal_plots, fft_plots)

def _export_2d_plots_per_component(self, config, signal_plots, fft_plots, fixed_combos):
    """Export 2D plots as separate HTML files per component"""
    # Signal plots
    for idx, component in enumerate(config['headers_array']):
        start = idx * len(fixed_combos)
        end = start + len(fixed_combos)
        component_plots = signal_plots[start:end]
        if component_plots:
            filename = self._get_html_filename(config, f"_{component}")
            self._write_html_report(filename, component_plots)
    
    # FFT plots
    if config['fft_enabled']:
        for idx, component in enumerate(config['FFT_headers']):
            start = idx * len(fixed_combos)
            end = start + len(fixed_combos)
            component_plots = fft_plots[start:end]
            if component_plots:
                filename = self._get_html_filename(config, f"_{component}")
                self._write_html_report(filename, component_plots)

def _export_2d_grouped_plots(self, config, signal_plots, fft_plots):
    """Export 2D plots grouped by category"""
    # Group signal plots by category
    category_groups = dict(zip(config['mat_names'], config['headers_lists']))
    grouped_signal_figs = {cat: [] for cat in category_groups.keys()}
    
    for component, fig in zip(config['headers_array'], signal_plots):
        for cat, comps in category_groups.items():
            if component in comps:
                grouped_signal_figs[cat].append(fig)
                break
    
    # Write grouped signal plots
    for cat, figs in grouped_signal_figs.items():
        if figs:
            filename = self._get_html_filename(config, f"_{cat}")
            self._write_html_report(filename, figs)
    
    # Group and write FFT plots
    if config['fft_enabled']:
        if config['standalone_exist']:
            fft_categories = {"Standalone_FFT": config['FFT_headers']}
        else:
            fft_categories = {"FFT_Current": config['FFT_headers'][:len(config['headers_lists'][6])],
                             "FFT_Voltage": config['FFT_headers'][len(config['headers_lists'][6]):]}
        
        grouped_fft_figs = {cat: [] for cat in fft_categories.keys()}
        for component, fig in zip(config['FFT_headers'], fft_plots):
            for cat, comps in fft_categories.items():
                if component in comps:
                    grouped_fft_figs[cat].append(fig)
                    break
        
        for cat, figs in grouped_fft_figs.items():
            if figs:
                filename = self._get_html_filename(config, f"_{cat}")
                self._write_html_report(filename, figs)

def _export_3d_plots_per_component(self, config, signal_plots, fft_plots):
    """Export 3D plots as separate HTML files per component"""
    # Signal plots
    for idx, component in enumerate(config['headers_array']):
        start = idx * max(1, len(signal_plots) // len(config['headers_array']))
        end = (idx + 1) * max(1, len(signal_plots) // len(config['headers_array']))
        filename = self._get_html_filename(config, f"_{config['utc']}_{component}")
        self._write_html_report(filename, signal_plots[start:end])
    
    # FFT plots
    if config['fft_enabled'] and fft_plots:
        for idx, component in enumerate(config['FFT_headers']):
            start = idx * max(1, len(fft_plots) // len(config['FFT_headers']))
            end = (idx + 1) * max(1, len(fft_plots) // len(config['FFT_headers']))
            filename = self._get_html_filename(config, f"_{config['utc']}_{component}")
            self._write_html_report(filename, fft_plots[start:end])

def _export_3d_grouped_plots(self, config, signal_plots, fft_plots):
    """Export 3D plots grouped by category"""
    # Group signal plots by category
    category_groups = dict(zip(config['mat_names'], config['headers_lists']))
    grouped_signal_figs = {cat: [] for cat in category_groups.keys()}
    
    for component, fig in zip(config['headers_array'], signal_plots):
        for cat, comps in category_groups.items():
            if component in comps:
                grouped_signal_figs[cat].append(fig)
                break
    
    # Write grouped signal plots
    for cat, figs in grouped_signal_figs.items():
        if figs:
            filename = self._get_html_filename(config, f"_{config['utc']}_{cat}")
            self._write_html_report(filename, figs)
    
    # Group and write FFT plots
    if config['fft_enabled'] and fft_plots:
        if config['standalone_exist']:
            fft_categories = {"Standalone_FFT": config['FFT_headers']}
        else:
            fft_categories = {"FFT_Current": config['FFT_headers'][:len(config['headers_lists'][6])],
                             "FFT_Voltage": config['FFT_headers'][len(config['headers_lists'][6]):]}
        
        grouped_fft_figs = {cat: [] for cat in fft_categories.keys()}
        for component, fig in zip(config['FFT_headers'], fft_plots):
            for cat, comps in fft_categories.items():
                if component in comps:
                    grouped_fft_figs[cat].append(fig)
                    break
        
        for cat, figs in grouped_fft_figs.items():
            if figs:
                filename = self._get_html_filename(config, f"_{config['utc']}_{cat}")
                self._write_html_report(filename, figs)

def _get_html_filename(self, config, suffix):
    """Generate HTML filename based on mode and suffix"""
    base_name = "HTML_GRAPH"
    if config['standalone_exist']:
        base_name += "_Standalone"
    return dp.os.path.normpath(dp.os.path.join(config['html_folder'], f"{base_name}{suffix}.html")).replace('\\', '/')

def _write_html_report(self, html_file, plots):
    """Export interactive Plotly figures to a styled HTML report"""
    plot_items = ''
    html_content = self.prep_html_template(Time_series=False)
    
    plot_items += '<div class="plot-container">\n'
    for i, fig in enumerate(plots):
        fig.update_layout(height=720, margin=dict(t=50, b=50, l=50, r=50))
        fig_html = dp.to_html(fig, include_plotlyjs='cdn', full_html=False, div_id=f"plot-{i}")
        plot_items += f'<div class="plot-item">{fig_html}</div>\n'
    plot_items += '</div>\n'
    
    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
    
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)

def _format_fixed_title(self, fixed_dict, sweepNames=[]):
    """Format the fixed title in the same way as dropdown case"""
    items = list(fixed_dict.items())
    formatted = []
    for j in range(0, len(items), 2):
        chunk = items[j:j+2]
        formatted.append(" | ".join(f"{sweepNames[int(''.join(filter(str.isdigit, k)))-1]} = {v}" for k, v in chunk))
    return "<br>".join(formatted)

def make_dropdown(self, full_title, component, fixed_combos_data, plot_type="3D"):
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
                        if dp.JSON["perturbation"]==0:
                            if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                                # Keep only first and last rows and columns
                                X = dp.np.array([X[0, :], X[-1, :]])       # first & last row
                                Y = dp.np.array([Y[0, :], Y[-1, :]])
                                Z = dp.np.array([Z[0, :], Z[-1, :]])
                        
                        if dp.JSON["permute"]:
                            X, Y = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
                            Z = dp.np.full_like(X, dp.np.nan, dtype=float)

                            Xi = dp.np.searchsorted(dp.np.unique(y_vals), y_vals)
                            Yi = dp.np.searchsorted(dp.np.unique(x_vals), x_vals)
                            Z[Xi, Yi] = z_vals

                            fig.add_trace(dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', visible=False))
                        else:
                            fig.add_trace(dp.go.Scatter3d(
                                x=x_vals,
                                y=y_vals,
                                z=z_vals,
                                mode='lines+markers',
                                visible=False
                            ))
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
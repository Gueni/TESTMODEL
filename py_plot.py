
    def _detect_sensitivity_files(self, csv_maps_dir):
        """Detect if sensitivity files exist in the CSV_MAPS directory."""
        return any(f.endswith('_Sens_Map.csv') for f in os.listdir(csv_maps_dir))

    def _load_standalone_data(self, fileLog, csv_maps_dir, csv_time_series_dir):
        """Load standalone data from CSV_MAPS files (regular and sensitivity)."""
        time_series_files = fileLog.natsort_files(csv_time_series_dir, standalone=True)
        standalone_matrices = {}
        headers_lists = []
        headers_array = []
        
        # Detect sensitivity files
        sens_files_exist = self._detect_sensitivity_files(csv_maps_dir)
        
        if time_series_files:
            df = dp.pd.read_csv(time_series_files[0])
            base_headers = [dp.re.sub(r'[^a-zA-Z0-9]', '_', header) for header in df.columns[1:].tolist()]
        
        print("base_headers", base_headers)
        print(f"Sensitivity files detected: {sens_files_exist}")
        
        # Define matrix types for regular data
        mat_names = ["Standalone_RMS", "Standalone_AVG", "Standalone_MAX", "Standalone_MIN", "Standalone_FFT"]
        mat_suffix = ['RMS', 'AVG', 'MAX', 'MIN', 'FFT']
        
        # Load regular matrices
        for file_type, file_name in zip(mat_suffix, mat_names):
            file_path = dp.os.path.join(csv_maps_dir, file_name + '_Map.csv')
            if dp.os.path.exists(file_path):
                df = dp.pd.read_csv(file_path, header=None)
                standalone_matrices[file_type] = df.values.astype(float)
                file_headers = [f"{h}_{file_type}" for h in base_headers] if base_headers else [f"{file_type}_{i}" for i in range(df.shape[1])]
                headers_lists.append(file_headers)
            else:
                standalone_matrices[file_type] = None
                headers_lists.append([])
        
        # Load sensitivity matrices if they exist
        if sens_files_exist:
            sens_mat_names = [f"Standalone_Sens_{name.split('_')[-1]}" for name in mat_names]
            sens_mat_suffix = [f"Sens_{suffix}" for suffix in mat_suffix]
            
            for file_type, file_name in zip(sens_mat_suffix, sens_mat_names):
                file_path = dp.os.path.join(csv_maps_dir, file_name + '_Map.csv')
                if dp.os.path.exists(file_path):
                    df = dp.pd.read_csv(file_path, header=None)
                    standalone_matrices[file_type] = df.values.astype(float)
                    # Add "_Sens" to headers to distinguish sensitivity data
                    file_headers = [f"{h}_{file_type}" for h in base_headers] if base_headers else [f"{file_type}_{i}" for i in range(df.shape[1])]
                    headers_lists.append(file_headers)
                else:
                    standalone_matrices[file_type] = None
                    headers_lists.append([])
        
        d = 4  # Number of non-FFT types (RMS, AVG, MAX, MIN)
        return standalone_matrices, headers_lists, base_headers, sens_files_exist, d

    def _build_standalone_headers_and_matrices(self, standalone_matrices, headers_lists, sens_files_exist, d):
        """Build headers and combined matrices for standalone data (regular + sensitivity)."""
        # Build headers_array for non-sensitivity files
        headers_array = []
        for i in range(d):
            if i < len(headers_lists) and headers_lists[i]:
                headers_array.extend(headers_lists[i])
        
        # Build sensitivity headers if they exist
        sens_headers = []
        if sens_files_exist:
            for i in range(d, 2*d):
                if i < len(headers_lists) and headers_lists[i]:
                    sens_headers.extend(headers_lists[i])
        
        # FFT headers (regular and sensitivity)
        FFT_headers = headers_lists[d] if d < len(headers_lists) and headers_lists[d] else []
        sens_FFT_headers = headers_lists[2*d] if sens_files_exist and 2*d < len(headers_lists) and headers_lists[2*d] else []
        
        # Combine non-FFT matrices (regular)
        combined_matrix = None
        mat_suffix = ['RMS', 'AVG', 'MAX', 'MIN']
        for file_type in mat_suffix:
            if standalone_matrices.get(file_type) is not None:
                if combined_matrix is None:
                    combined_matrix = standalone_matrices[file_type]
                else:
                    combined_matrix = dp.np.hstack((combined_matrix, standalone_matrices[file_type]))
        
        # Combine sensitivity matrices if they exist
        combined_sens_matrix = None
        if sens_files_exist:
            sens_suffix = ['Sens_RMS', 'Sens_AVG', 'Sens_MAX', 'Sens_MIN']
            for file_type in sens_suffix:
                if standalone_matrices.get(file_type) is not None:
                    if combined_sens_matrix is None:
                        combined_sens_matrix = standalone_matrices[file_type]
                    else:
                        combined_sens_matrix = dp.np.hstack((combined_sens_matrix, standalone_matrices[file_type]))
        
        # FFT matrices
        combined_fft_matrix = standalone_matrices.get('FFT')
        combined_sens_fft_matrix = standalone_matrices.get('Sens_FFT') if sens_files_exist else None
        
        # Combine regular and sensitivity matrices
        if sens_files_exist and combined_sens_matrix is not None:
            headers_array.extend(sens_headers)
            FFT_headers.extend(sens_FFT_headers)
            
            combined_matrix = dp.np.hstack((combined_matrix, combined_sens_matrix)) if combined_matrix is not None else combined_sens_matrix
            if combined_fft_matrix is not None and combined_sens_fft_matrix is not None:
                combined_fft_matrix = dp.np.hstack((combined_fft_matrix, combined_sens_fft_matrix))
            elif combined_sens_fft_matrix is not None:
                combined_fft_matrix = combined_sens_fft_matrix
        
        return headers_array, FFT_headers, combined_matrix, combined_fft_matrix, sens_files_exist

    def _load_normal_data(self, simutil, header_path, csv_maps_dir):
        """Load normal simulation data from matrices and JSON headers (including sensitivity)."""
        mat_names = ["Peak_Currents", "RMS_Currents", "AVG_Currents", "Peak_Voltages", 
                    "RMS_Voltages", "AVG_Voltages", "FFT_Current", "FFT_Voltage", 
                    "Dissipations", "Elec_Stats", "Temps", "Thermal_Stats"]
        
        # Detect if sensitivity files exist in CSV_MAPS (for normal case)
        sens_files_exist = self._detect_sensitivity_files(csv_maps_dir)
        print(f"Sensitivity files detected in normal mode: {sens_files_exist}")
        
        # Load regular headers
        headers_lists = []
        for name in mat_names:
            json_path = dp.os.path.join(header_path, f"{name}.json")
            if dp.os.path.exists(json_path):
                data = dp.json.load(open(json_path))
                headers_lists.append(data if isinstance(data, list) else [data])
            else:
                headers_lists.append([f"{name}_{i}" for i in range(simutil.MAT_list[0].shape[1])])
        
        # Load sensitivity headers if they exist
        if sens_files_exist:
            sens_mat_names = [f"Sens_{name}" for name in mat_names]
            for sens_name in sens_mat_names:
                sens_json_path = dp.os.path.join(header_path, f"{sens_name}.json")
                if dp.os.path.exists(sens_json_path):
                    sens_data = dp.json.load(open(sens_json_path))
                    headers_lists.append(sens_data if isinstance(sens_data, list) else [sens_data])
                else:
                    # Create placeholder headers if JSON doesn't exist
                    headers_lists.append([f"{sens_name}_{i}" for i in range(simutil.MAT_list[0].shape[1])])
        
        # Calculate cumulative sums for Y_Length
        cumsum = dp.np.cumsum(dp.Y_Length[1:]).tolist()
        all_headers = sum(headers_lists, [])
        
        num_regular_matrices = len(mat_names)
        
        if sens_files_exist:
            # For sensitivity, adjust slicing to include both regular and sensitivity data
            regular_headers_count = len(sum(headers_lists[:num_regular_matrices], []))
            
            fft_start, fft_end = cumsum[5], cumsum[7]
            
            # Regular FFT headers
            FFT_headers = all_headers[fft_start:fft_end]
            headers_array = all_headers[:fft_start] + all_headers[fft_end:regular_headers_count]
            
            # Sensitivity FFT headers
            sens_fft_start = regular_headers_count + cumsum[5]
            sens_fft_end = regular_headers_count + cumsum[7]
            sens_FFT_headers = all_headers[sens_fft_start:sens_fft_end]
            sens_headers_array = all_headers[regular_headers_count:sens_fft_start] + all_headers[sens_fft_end:]
            
            # Extend arrays with sensitivity data
            headers_array.extend(sens_headers_array)
            FFT_headers.extend(sens_FFT_headers)
            
            # Combine matrices (regular + sensitivity)
            regular_matrices = simutil.MAT_list[:6] + simutil.MAT_list[8:12]
            
            # Check if sensitivity matrices exist in simutil.MAT_list
            if len(simutil.MAT_list) > num_regular_matrices:
                sens_matrices = simutil.MAT_list[num_regular_matrices:]
                combined_matrix = dp.np.hstack(regular_matrices + sens_matrices)
            else:
                combined_matrix = dp.np.hstack(regular_matrices)
            
            # Combine FFT matrices
            regular_fft_matrices = simutil.MAT_list[6:8]
            if len(simutil.MAT_list) > num_regular_matrices + 2:
                sens_fft_matrices = simutil.MAT_list[num_regular_matrices + 6:num_regular_matrices + 8]
                combined_fft_matrix = dp.np.hstack(regular_fft_matrices + sens_fft_matrices)
            else:
                combined_fft_matrix = dp.np.hstack(regular_fft_matrices)
        else:
            # No sensitivity - original behavior
            fft_start, fft_end = cumsum[5], cumsum[7]
            FFT_headers = all_headers[fft_start:fft_end]
            headers_array = all_headers[:fft_start] + all_headers[fft_end:]
            
            combined_matrix = dp.np.hstack((simutil.MAT_list[:6] + simutil.MAT_list[8:12]))
            combined_fft_matrix = dp.np.hstack((simutil.MAT_list[6:8]))
        
        return headers_array, FFT_headers, combined_matrix, combined_fft_matrix, headers_lists, mat_names, sens_files_exist

    def _get_headers_lists_for_grouping(self, headers_lists, mat_names, sens_files_exist):
        """Get the appropriate headers lists for grouping reports."""
        if sens_files_exist:
            # Create separate categories for regular and sensitivity data
            num_regular = len(mat_names)
            regular_headers_lists = headers_lists[:num_regular]
            sens_headers_lists = headers_lists[num_regular:]
            
            # Create combined category names
            combined_mat_names = mat_names + [f"Sens_{name}" for name in mat_names]
            combined_headers_lists = regular_headers_lists + sens_headers_lists
            
            return combined_mat_names, combined_headers_lists
        else:
            return mat_names, headers_lists

    def _group_and_write_reports(self, headers_array, FFT_headers, list_of_plots, fft_plots, 
                                html_folder, standalone_exist, utc, headers_lists, mat_names, sens_files_exist):
        """Group figures by categories and write HTML reports (handles sensitivity)."""
        # Get appropriate headers lists with sensitivity support
        category_names, category_headers_lists = self._get_headers_lists_for_grouping(headers_lists, mat_names, sens_files_exist)
        category_groups = dict(zip(category_names, category_headers_lists))
        
        # Handle FFT categories
        if standalone_exist:
            if sens_files_exist:
                fft_categories = {
                    "Standalone_FFT": FFT_headers[:len(FFT_headers)//2],
                    "Standalone_Sens_FFT": FFT_headers[len(FFT_headers)//2:]
                }
            else:
                fft_categories = {"Standalone_FFT": FFT_headers}
        else:
            if sens_files_exist:
                # Split FFT headers between regular and sensitivity
                num_regular_fft = len(FFT_headers) // 2
                fft_categories = {
                    "FFT_Current": FFT_headers[:num_regular_fft//2],
                    "FFT_Voltage": FFT_headers[num_regular_fft//2:num_regular_fft],
                    "FFT_Sens_Current": FFT_headers[num_regular_fft:num_regular_fft + num_regular_fft//2],
                    "FFT_Sens_Voltage": FFT_headers[num_regular_fft + num_regular_fft//2:]
                }
            else:
                fft_categories = {
                    "FFT_Current": FFT_headers[:len(FFT_headers)//2],
                    "FFT_Voltage": FFT_headers[len(FFT_headers)//2:]
                }
        
        # Build category-based plot lists
        grouped_signal_figs = {cat: [] for cat in category_groups.keys()}
        grouped_fft_figs = {cat: [] for cat in fft_categories.keys()}
        
        # Group signal plots
        for component, fig in zip(headers_array, list_of_plots):
            for cat, comps in category_groups.items():
                if component in comps:
                    grouped_signal_figs[cat].append(fig)
                    break
        
        # Group FFT plots
        for component, fig in zip(FFT_headers, fft_plots):
            for cat, comps in fft_categories.items():
                if component in comps:
                    grouped_fft_figs[cat].append(fig)
                    break
        
        # Write separate HTMLs per category
        for cat, figs in grouped_signal_figs.items():
            if figs:
                prefix = "Standalone_" if standalone_exist else ""
                self._write_html_report(
                    dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{utc}_{cat}.html")).replace('\\', '/'), 
                    figs
                )
        
        if dp.JSON["FFT"]:
            for cat, figs in grouped_fft_figs.items():
                if figs:
                    prefix = "Standalone_" if standalone_exist else ""
                    self._write_html_report(
                        dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{utc}_{cat}.html")).replace('\\', '/'), 
                        figs
                    )

    def graph_scopes(self, fileLog, simutil, standalone_exist=False):
        """
        Generate 2D or 3D simulation plots (including FFT) from matrix and JSON data
        and export them as interactive HTML reports. Supports both single-variable
        2D plots and multi-variable 3D surfaces with dropdown selection.
        Automatically detects and handles sensitivity analysis files (_Sens_Map.csv).
        
        Parameters: 
            fileLog (object): fileLog class object.
            simutil (object): simutil class object.
            standalone_exist (bool): Whether standalone data exists.
        """
        # Initialize paths
        csv_maps_dir = f"{fileLog.resultfolder}/CSV_MAPS"
        csv_time_series_dir = f"{fileLog.resultfolder}/CSV_TIME_SERIES"
        html_folder = fileLog.resultfolder + "/HTML_GRAPHS/"
        header_path = (dp.os.getcwd()).replace("\\", "/") + "/Script/assets/HEADER_FILES/"
        
        dp.os.makedirs(dp.os.path.dirname(html_folder), exist_ok=True)
        
        # Load data based on standalone flag (both handle sensitivity automatically)
        if standalone_exist:
            standalone_matrices, headers_lists, base_headers, sens_files_exist, d = self._load_standalone_data(
                fileLog, csv_maps_dir, csv_time_series_dir)
            headers_array, FFT_headers, combined_matrix, combined_fft_matrix, sens_files_exist = self._build_standalone_headers_and_matrices(
                standalone_matrices, headers_lists, sens_files_exist, d)
            mat_names = ["Standalone_RMS", "Standalone_AVG", "Standalone_MAX", "Standalone_MIN", "Standalone_FFT"]
        else:
            headers_array, FFT_headers, combined_matrix, combined_fft_matrix, headers_lists, mat_names, sens_files_exist = self._load_normal_data(
                simutil, header_path, csv_maps_dir)
        
        print(f"Sensitivity mode: {sens_files_exist}")
        print(f"Headers array length: {len(headers_array)}")
        print(f"FFT headers length: {len(FFT_headers)}")
        
        # Get sweep variables and determine plot type
        sweep_vars = {k: v for k, v in self.Xs_to_dict(simutil.sweepMatrix).items() if v != [0]}
        sweep_keys = list(sweep_vars.keys())
        
        var1, var2 = dp.JSON["Var1"], dp.JSON["Var2"]
        sweepNames = dp.JSON["sweepNames"]
        
        plot_2D, single_X_key, all_combos, fft_combos = self._determine_plot_type_and_combos(simutil, sweep_vars, sweep_keys)
        
        # Generate plots based on plot type
        if plot_2D:
            list_of_plots, fft_plots, fixed_combos, fixed_vars = self._create_2D_plots(
                headers_array, FFT_headers, combined_matrix, combined_fft_matrix,
                sweep_vars, sweep_keys, sweepNames, all_combos, standalone_exist)
            
            # Write HTML files for 2D plots
            if dp.iterSplit:
                # One HTML per component (handles both regular and sensitivity)
                for idx, component in enumerate(headers_array):
                    start = idx * len(fixed_combos)
                    end = start + len(fixed_combos)
                    component_plots = list_of_plots[start:end]
                    if component_plots:
                        prefix = "Standalone_" if standalone_exist else ""
                        suffix = "_Sens" if sens_files_exist and idx >= len(headers_array)//2 else ""
                        self._write_html_report(
                            dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{component}{suffix}_{self.utc}.html")).replace('\\', '/'), 
                            component_plots
                        )
                
                if dp.JSON['FFT'] and fft_plots:
                    for idx, component in enumerate(FFT_headers):
                        start = idx * len(fixed_combos)
                        end = start + len(fixed_combos)
                        component_plots = fft_plots[start:end]
                        if component_plots:
                            prefix = "Standalone_" if standalone_exist else ""
                            suffix = "_Sens" if sens_files_exist and idx >= len(FFT_headers)//2 else ""
                            self._write_html_report(
                                dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{component}{suffix}_{self.utc}.html")).replace('\\', '/'), 
                                component_plots
                            )
            else:
                # Group figures by categories (handles sensitivity automatically)
                self._group_and_write_reports(
                    headers_array, FFT_headers, list_of_plots, fft_plots, 
                    html_folder, standalone_exist, self.utc, headers_lists, mat_names, sens_files_exist
                )
        
        else:  # 3D case
            fixed_keys, fixed_combos, rows_dict, fft_rows_dict = self._get_fixed_combinations(simutil, sweep_vars, sweep_keys, var1, var2)
            
            if dp.iterSplit:
                list_of_plots, fft_plots = self._create_3D_plots_per_component(
                    headers_array, FFT_headers, combined_matrix, combined_fft_matrix,
                    fixed_combos, fixed_keys, rows_dict, fft_rows_dict, sweepNames, var1, var2, standalone_exist)
                
                # Write separate HTML files for each component
                for idx, component in enumerate(headers_array):
                    start, end = idx * max(1, len(list_of_plots) // len(headers_array)), (idx + 1) * max(1, len(list_of_plots) // len(headers_array))
                    prefix = "Standalone_" if standalone_exist else ""
                    suffix = "_Sens" if sens_files_exist and idx >= len(headers_array)//2 else ""
                    self._write_html_report(
                        dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{self.utc}_{component}{suffix}.html")).replace('\\', '/'), 
                        list_of_plots[start:end]
                    )
                
                if dp.JSON['FFT'] and fft_plots:
                    for idx, component in enumerate(FFT_headers):
                        start, end = idx * max(1, len(fft_plots) // len(FFT_headers)), (idx + 1) * max(1, len(fft_plots) // len(FFT_headers))
                        prefix = "Standalone_" if standalone_exist else ""
                        suffix = "_Sens" if sens_files_exist and idx >= len(FFT_headers)//2 else ""
                        self._write_html_report(
                            dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_{prefix}{self.utc}_{component}{suffix}.html")).replace('\\', '/'), 
                            fft_plots[start:end]
                        )
            
            else:  # Use dropdown menus
                dropdown_data, fft_dropdown_data = self._prepare_dropdown_data(
                    headers_array, FFT_headers, combined_matrix, combined_fft_matrix,
                    fixed_combos, fixed_keys, rows_dict, fft_rows_dict, sweepNames, var1, var2)
                
                # Create dropdown figures - remove full_title parameter
                list_of_plots = [self._make_dropdown(component, dropdown_data[component], plot_type="3D") 
                                for component in headers_array if dropdown_data.get(component)]
                
                if dp.JSON['FFT'] and fft_dropdown_data:
                    fft_plots = [self._make_dropdown(component, fft_dropdown_data[component], plot_type="FFT") 
                                for component in FFT_headers if fft_dropdown_data.get(component)]
                
                # Group and write reports (handles sensitivity automatically)
                self._group_and_write_reports(
                    headers_array, FFT_headers, list_of_plots, fft_plots, 
                    html_folder, standalone_exist, self.utc, headers_lists, mat_names, sens_files_exist
                )

    def _determine_plot_type_and_combos(self, simutil, sweep_vars, sweep_keys):
        """Determine plot type (2D vs 3D) and generate sweep combinations."""
        active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
        plot_2D = len(active_sweep_keys) == 1
        single_X_key = active_sweep_keys[0] if plot_2D else None
        
        # Generate all combinations for the sweep
        if dp.JSON["permute"]:
            all_combos = list(dp.product(*sweep_vars.values()))
        else:
            # For non-permuted sweeps, we need to handle different length lists correctly
            # Get the maximum length
            values_list = list(sweep_vars.values())
            max_len = max(len(v) for v in values_list)
            
            # Create combinations by taking elements at same index
            all_combos = []
            for i in range(max_len):
                combo = []
                for v in values_list:
                    if i < len(v):
                        combo.append(v[i])
                    else:
                        # If this list is shorter, use its last value
                        combo.append(v[-1])
                all_combos.append(tuple(combo))
        
        # For FFT combinations
        if dp.JSON['FFT'] and all_combos:
            fft_combos = []
            for combo in all_combos:
                # Repeat each combo for the number of harmonics
                for _ in range(len(dp.harmonics)):
                    fft_combos.append(combo)
        else:
            fft_combos = None
        
        return plot_2D, single_X_key, all_combos, fft_combos

    def _create_2D_plots(self, headers_array, FFT_headers, combined_matrix, combined_fft_matrix, 
                        sweep_vars, sweep_keys, sweepNames, all_combos, standalone_exist):
        """Create 2D plots (line plots and bar charts)."""
        list_of_plots, fft_plots = [], []
        relative_tol, absolute_tol = 0.001, 1e-12
        
        # Check if we have valid data
        if combined_matrix is None or combined_matrix.size == 0:
            print("Warning: No data available for 2D plots")
            return list_of_plots, fft_plots, [], {}
        
        # Determine active sweep keys
        active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
        if not active_sweep_keys:
            print("Warning: No active sweep keys found")
            return list_of_plots, fft_plots, [], {}
        
        single_X_key = active_sweep_keys[0]
        sweep_values = sweep_vars[single_X_key]
        sweep_label = sweepNames[int(dp.re.search(r'\d+', single_X_key).group())-1]
        
        fixed_vars = {k: v for k, v in sweep_vars.items() if k != single_X_key and v != [0]}
        
        # Generate fixed combinations
        if dp.JSON["permute"]:
            if fixed_vars:
                fixed_combos = list(dp.product(*fixed_vars.values()))
            else:
                fixed_combos = [()]
        else:
            if fixed_vars:
                values_list = list(fixed_vars.values())
                max_len = max(len(v) for v in values_list)
                fixed_combos = []
                for i in range(max_len):
                    combo = []
                    for v in values_list:
                        if i < len(v):
                            combo.append(v[i])
                        else:
                            combo.append(v[-1])
                    fixed_combos.append(tuple(combo))
            else:
                fixed_combos = [()]
        
        # Ensure we don't exceed matrix bounds
        max_rows = combined_matrix.shape[0]
        num_sweep_values = min(len(sweep_values), max_rows)
        
        # Normal signals
        for component in headers_array:
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                z_column = headers_array.index(component)
                
                # Check if z_column is within bounds
                if z_column >= combined_matrix.shape[1]:
                    print(f"Warning: Column {z_column} out of bounds for component {component}")
                    continue
                    
                z_vals = combined_matrix[:num_sweep_values, z_column]
                
                # Handle constant values
                if dp.JSON["perturbation"] == 0:
                    if dp.np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
                        x_plot = dp.np.array([sweep_values[0], sweep_values[-1]])
                        z_plot = dp.np.array([z_vals[0], z_vals[-1]])
                    else:
                        x_plot = sweep_values[:num_sweep_values]
                        z_plot = z_vals
                else:
                    x_plot = sweep_values[:num_sweep_values]
                    z_plot = z_vals
                
                fig = dp.go.Figure()
                fig.add_trace(dp.go.Scatter(x=x_plot, y=z_plot, mode='lines',
                                            name=f"{component} {self._format_fixed_title(fixed_dict, sweepNames)}"))
                fig.update_layout(
                    title=dict(text=f"{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
                    xaxis_title=sweep_label, yaxis_title=component,
                    xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
                    xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
                    margin=dict(r=50)
                )
                list_of_plots.append(fig)
        
        # FFT signals
        if dp.JSON['FFT'] and combined_fft_matrix is not None and combined_fft_matrix.size > 0:
            max_fft_rows = combined_fft_matrix.shape[0]
            num_fft_sweep_values = min(len(sweep_values), max_fft_rows)
            
            for component in FFT_headers:
                for fixed_values in fixed_combos:
                    fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                    z_column = FFT_headers.index(component)
                    
                    if z_column >= combined_fft_matrix.shape[1]:
                        print(f"Warning: FFT column {z_column} out of bounds for component {component}")
                        continue
                        
                    z_vals = combined_fft_matrix[:num_fft_sweep_values, z_column]
                    x_vals = dp.np.array(dp.harmonics)
                    x_plot = dp.np.tile(x_vals, int(dp.np.ceil(num_fft_sweep_values/len(x_vals))))[:num_fft_sweep_values]
                    
                    fig = dp.go.Figure()
                    fig.add_trace(dp.go.Bar(x=x_plot, y=z_vals, 
                                            name=f"{component} {self._format_fixed_title(fixed_dict, sweepNames)}"))
                    fig.update_layout(
                        title=dict(text=f"{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}", x=0.5),
                        xaxis_title='Harmonic Order', yaxis_title=component,
                        xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10),
                        xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10),
                        margin=dict(r=50)
                    )
                    fft_plots.append(fig)
        
        return list_of_plots, fft_plots, fixed_combos, fixed_vars

    def _format_fixed_title(self, fixed_dict, sweepNames):
        """Format the fixed title in the same way as dropdown case."""
        return "<br>".join(" | ".join(f"{sweepNames[int(''.join(filter(str.isdigit, k)))-1]} = {v}" 
                                    for k, v in list(fixed_dict.items())[j:j+2]) 
                        for j in range(0, len(fixed_dict), 2))

    def _get_fixed_combinations(self, simutil, sweep_vars, sweep_keys, var1, var2):
        """Get fixed combinations for 3D plotting."""
        other_vars = {k: v for k, v in self.Xs_to_dict(simutil.sweepMatrix).items() 
                    if dp.re.fullmatch(r"X\d+", k) and k not in [var1, var2] and v != [0] 
                    and not dp.JSON["sweepNames"][int(dp.re.search(r'\d+', k).group())-1].startswith("X")}
        
        fixed_keys = list(other_vars.keys())
        
        # Generate fixed combinations
        if dp.JSON["permute"]:
            if other_vars:
                fixed_combos = list(dp.product(*other_vars.values()))
            else:
                fixed_combos = [()]
        else:
            # For non-permuted sweeps with fixed variables
            if other_vars:
                values_list = list(other_vars.values())
                max_len = max(len(v) for v in values_list)
                fixed_combos = []
                for i in range(max_len):
                    combo = []
                    for v in values_list:
                        if i < len(v):
                            combo.append(v[i])
                        else:
                            combo.append(v[-1])
                    fixed_combos.append(tuple(combo))
            else:
                fixed_combos = [()]
        
        # Generate all sweep combinations (same logic as above)
        if dp.JSON["permute"]:
            all_combos = list(dp.product(*sweep_vars.values()))
        else:
            values_list = list(sweep_vars.values())
            max_len = max(len(v) for v in values_list)
            all_combos = []
            for i in range(max_len):
                combo = []
                for v in values_list:
                    if i < len(v):
                        combo.append(v[i])
                    else:
                        combo.append(v[-1])
                all_combos.append(tuple(combo))
        
        # Return the Selected Rows of data for each fixed combo
        rows_dict, fft_rows_dict = {}, {}
        
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            rows = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) 
                            for i, combo in enumerate(all_combos) 
                            if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
            rows_dict[tuple(fixed_values)] = rows
            
            if dp.JSON['FFT'] and all_combos:
                # Generate FFT combos by repeating each combo for harmonics
                fft_combos = []
                for combo in all_combos:
                    for _ in range(len(dp.harmonics)):
                        fft_combos.append(combo)
                
                fft_rows = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) 
                                    for i, combo in enumerate(fft_combos) 
                                    if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
                fft_rows_dict[tuple(fixed_values)] = fft_rows
        
        return fixed_keys, fixed_combos, rows_dict, fft_rows_dict

    def _create_3D_plots_per_component(self, headers_array, FFT_headers, combined_matrix, combined_fft_matrix,
                                        fixed_combos, fixed_keys, rows_dict, fft_rows_dict, sweepNames, var1, var2, standalone_exist):
        """Create separate 3D plots for each component (iterSplit=True)."""
        list_of_plots, fft_plots = [], []
        relative_tol, absolute_tol = 0.001, 1e-12
        
        for component, fixed_values in dp.product(headers_array, fixed_combos):
            fixed_dict = dict(zip(fixed_keys, fixed_values))
            z_column = headers_array.index(component)
            rows = rows_dict[tuple(fixed_values)]
            
            x_vals, y_vals, z_vals = rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), z_column]
            X, Y = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
            Z = dp.np.full_like(X, dp.np.nan, dtype=float)
            Xi, Yi = dp.np.searchsorted(dp.np.unique(y_vals), y_vals), dp.np.searchsorted(dp.np.unique(x_vals), x_vals)
            Z[Xi, Yi] = z_vals
            
            if dp.JSON["perturbation"] == 0:
                if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                    X = dp.np.array([X[0, :], X[-1, :]])
                    Y = dp.np.array([Y[0, :], Y[-1, :]])
                    Z = dp.np.array([Z[0, :], Z[-1, :]])
            
            fig = self._create_3d_surface_plot(component, fixed_dict, X, Y, Z, sweepNames, var1, var2)
            list_of_plots.append(fig)
        
        if dp.JSON['FFT'] and combined_fft_matrix is not None:
            for component, fixed_values in dp.product(FFT_headers, fixed_combos):
                fixed_dict = dict(zip(fixed_keys, fixed_values))
                z_column = FFT_headers.index(component)
                fft_rows = fft_rows_dict[tuple(fixed_values)]
                y_vals = fft_rows[:,2]
                x_vals = dp.np.tile(dp.np.array(dp.harmonics), int(dp.np.ceil(len(y_vals)/len(dp.harmonics))))[:len(y_vals)]
                z_vals = combined_fft_matrix[fft_rows[:,0].astype(int), z_column]
                fig = self.barchart3D(x_vals, y_vals, z_vals, 
                                    f'{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}', 
                                    'Magnitude', x_title='Harmonics', 
                                    y_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1])
                fft_plots.append(fig)
        
        return list_of_plots, fft_plots

    def _create_3d_surface_plot(self, component, fixed_dict, X, Y, Z, sweepNames, var1, var2):
        """Create a single 3D surface plot."""
        full_title = f'{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}'
        fig = dp.go.Figure(data=[dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict())])
        fig.update_layout(
            title=dict(text=full_title, x=0.5, xanchor='center', yanchor='top'),
            scene=dict(
                xaxis=dict(autorange='reversed'),
                yaxis=dict(autorange='reversed'),
                xaxis_title=sweepNames[int(dp.re.search(r'\d+', var1).group())-1],
                yaxis_title=sweepNames[int(dp.re.search(r'\d+', var2).group())-1],
                zaxis_title=component,
                xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10), zaxis_title_font=dict(size=10),
                xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10), zaxis_tickfont=dict(size=10)
            )
        )
        return fig

    def _prepare_dropdown_data(self, headers_array, FFT_headers, combined_matrix, combined_fft_matrix,
                            fixed_combos, fixed_keys, rows_dict, fft_rows_dict, sweepNames, var1, var2):
        """Prepare data for dropdown menus."""
        dropdown_data, fft_dropdown_data = {}, {}
        
        for component in headers_array:
            comp_data = {}
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_keys, fixed_values))
                rows = rows_dict[tuple(fixed_values)]
                x_vals, y_vals, z_vals = rows[:,1], rows[:,2], combined_matrix[rows[:,0].astype(int), headers_array.index(component)]
                comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
            dropdown_data[component] = comp_data
        
        if dp.JSON['FFT'] and combined_fft_matrix is not None:
            for component in FFT_headers:
                comp_data = {}
                for fixed_values in fixed_combos:
                    fixed_dict = dict(zip(fixed_keys, fixed_values))
                    fft_rows = fft_rows_dict[tuple(fixed_values)]
                    y_vals = fft_rows[:,2]
                    x_vals = dp.np.tile(dp.np.array(dp.harmonics), int(dp.np.ceil(len(y_vals)/len(dp.harmonics))))[:len(y_vals)]
                    z_vals = combined_fft_matrix[fft_rows[:,0].astype(int), FFT_headers.index(component)]
                    comp_data[str(fixed_dict)] = (x_vals, y_vals, z_vals, fixed_dict)
                fft_dropdown_data[component] = comp_data
        
        return dropdown_data, fft_dropdown_data

    def _write_html_report(self, html_file, plots):
        """Export interactive Plotly figures to a styled HTML report."""
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

    def _make_dropdown(self, component, fixed_combos_data, plot_type="3D"):
        """
        Create a Plotly figure with multiple traces and a dropdown menu.
        
        Parameters:
            component: str - Name of the component being plotted
            fixed_combos_data: dict - Dictionary of fixed combinations data
            plot_type: str - "3D" for surface plots, "FFT" for bar charts
        """
        fig, dropdown_buttons, sweepNames = dp.go.Figure(), [], dp.JSON["sweepNames"]
        group_trace_indices, current_index = [], 0
        
        for i, (_, data) in enumerate(fixed_combos_data.items()):
            x_vals, y_vals, z_vals, fixed_dict = data
            
            if plot_type == "FFT":
                temp_fig = self.barchart3D(x_vals, y_vals, z_vals, 
                                        f'{component}<br>{self._format_fixed_title(fixed_dict, sweepNames)}', 
                                        'Magnitude',
                                        x_title='Harmonics', 
                                        y_title=sweepNames[int(dp.re.search(r'\d+', dp.JSON["Var2"]).group())-1])
                for trace in temp_fig.data:
                    trace.visible = False
                    fig.add_trace(trace)
                n_traces = len(temp_fig.data)
            else:  # 3D Surface mode
                X, Y = dp.np.meshgrid(dp.np.unique(x_vals), dp.np.unique(y_vals))
                Z = dp.np.full_like(X, dp.np.nan, dtype=float)
                Z[dp.np.searchsorted(dp.np.unique(y_vals), y_vals), 
                dp.np.searchsorted(dp.np.unique(x_vals), x_vals)] = z_vals
                
                if dp.JSON["perturbation"] == 0:
                    relative_tol, absolute_tol = 0.001, 1e-12
                    if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                        X = dp.np.array([X[0, :], X[-1, :]])
                        Y = dp.np.array([Y[0, :], Y[-1, :]])
                        Z = dp.np.array([Z[0, :], Z[-1, :]])
                
                fig.add_trace(dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', visible=False))
                n_traces = 1
            
            group_trace_indices.append((current_index, current_index + n_traces))
            current_index += n_traces
        
        # Make the first group visible
        if group_trace_indices:
            first_start, first_end = group_trace_indices[0]
            for j in range(first_start, first_end):
                fig.data[j].visible = True
        
        # Create dropdown buttons
        for i, (_, data) in enumerate(fixed_combos_data.items()):
            fixed_dict = data[3]
            start_idx, end_idx = group_trace_indices[i]
            fixed_title = self._format_fixed_title(fixed_dict, sweepNames)
            
            visibility = [False] * len(fig.data)
            for j in range(start_idx, end_idx):
                visibility[j] = True
            dropdown_buttons.append({'label': fixed_title, 'method': 'update', 
                                    'args': [{'visible': visibility}, {'title.text': f'{component}<br>{fixed_title}'}]})
        
        # Initial title
        first_dict = next(iter(fixed_combos_data.values()))[3]
        first_title = self._format_fixed_title(first_dict, sweepNames)
        
        layout_base = dict(
            title=dict(text=f'{component}<br>{first_title}', x=0.5, xanchor='center', yanchor='top'),
            updatemenus=[dict(type='dropdown', x=1.15, y=0.5, xanchor='left', yanchor='middle',
                            buttons=dropdown_buttons, direction='down', showactive=True,
                            bgcolor='lightgray', bordercolor='black', font={'size': 12}, pad={'r': 20})],
            margin=dict(r=200)
        )
        
        # Configure scene
        if plot_type == "3D":
            layout_base['scene'] = dict(
                xaxis=dict(autorange='reversed'), yaxis=dict(autorange='reversed'),
                xaxis_title=sweepNames[int(dp.re.search(r'\d+', dp.JSON["Var1"]).group())-1],
                yaxis_title=sweepNames[int(dp.re.search(r'\d+', dp.JSON["Var2"]).group())-1],
                zaxis_title=component,
                xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10), zaxis_title_font=dict(size=10),
                xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10), zaxis_tickfont=dict(size=10)
            )
        elif plot_type == "FFT":
            layout_base['scene'] = dict(
                xaxis=dict(autorange='reversed'), yaxis=dict(autorange='reversed'),
                xaxis_title='Harmonics',
                yaxis_title=sweepNames[int(dp.re.search(r'\d+', dp.JSON["Var2"]).group())-1],
                zaxis_title='Magnitude',
                xaxis_title_font=dict(size=10), yaxis_title_font=dict(size=10), zaxis_title_font=dict(size=10),
                xaxis_tickfont=dict(size=10), yaxis_tickfont=dict(size=10), zaxis_tickfont=dict(size=10)
            )
        
        fig.update_layout(**layout_base)
        return fig
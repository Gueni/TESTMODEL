def generate_iteration_report(self, data_source, html_path, auto_open, report_type='signal', **kwargs):
    """
    Generates an iteration report in HTML format for various data sources.
    
    Parameters:
        self            : (object) The object of the class containing the function
        data_source     : (str or list) Path to directory containing CSV files, path to FFT CSV file, 
                          or list of standalone CSV file paths
        html_path       : (str) The path where the HTML file should be saved
        auto_open       : (bool) If True, opens the generated HTML report in a new browser window
        report_type     : (str) Type of report: 'signal', 'fft', or 'standalone'
        **kwargs        : Additional parameters based on report_type:
                          For 'signal': 
                              label_dict (dict), Y_axis_label (str)
                          For 'fft':
                              title (str), FFT_file (str)
    """
    
    # Common initialization
    include_plotlyjs = 'cdn'
    plot_items = ''
    html_content = self.prep_html_template(Time_series=False)
    figure_list = []
    
    # Process based on report type
    if report_type == 'signal':
        # Signal report processing
        path = data_source
        label_dict = kwargs.get('label_dict', {})
        Y_axis_label = kwargs.get('Y_axis_label', '')
        
        labels_dict = dict(label_dict)
        dict_keys = list(labels_dict.keys())
        
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv') 
                    and not f.endswith('_MAP.csv') 
                    and not f.endswith('_Standalone.csv')]
        
        if len(csv_files) >= 1:
            csv_files = dp.natsorted(csv_files)
            dfs = [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]
            
            for each in dict_keys:
                fig = dp.make_subplots()
                C = 1
                for df in dfs:
                    fig.add_trace(
                        dp.go.Scatter(
                            x=df.iloc[:, 0],
                            y=df.iloc[:, labels_dict.get(each)],
                            name=str("Iter :" + str(C) + " | ") + each,
                            mode="lines",
                            line=dict(shape='linear')
                        )
                    )
                    fig.update_layout(
                        showlegend=True,
                        title=each,
                        xaxis=dict(title='Time [ S ]'),
                        yaxis=dict(side="left", title=Y_axis_label,
                                 titlefont=dict(color="#1f77b4"),
                                 tickfont=dict(color="#1f77b4")),
                        plot_bgcolor='#f8fafd'
                    )
                    C += 1
                figure_list.append(fig)
                
                # Handle split reports for each key
                if dp.JSON['iterSplit']:
                    plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    html_content = self.prep_html_template(Time_series=False)
                    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    output_path = f"{html_path}_{each}.html"
                    with open(output_path, 'w', encoding='utf-8') as file:
                        file.write(html_content)
    
    elif report_type == 'fft':
        # FFT report processing
        csv_path = data_source
        title = kwargs.get('title', '')
        FFT_file = kwargs.get('FFT_file', '')
        
        headers = dp.json.load(open((dp.os.getcwd()).replace("\\", "/") + 
                                   f"/Script/assets/HEADER_FILES/{FFT_file}", 'r'))
        df = dp.pd.read_csv(csv_path, header=None, index_col=None)
        num_iterations = df.shape[0] // len(dp.harmonics)
        
        for column in range(df.shape[1]):
            fig = dp.go.Figure()
            
            for iteration in range(num_iterations):
                iteration_data = df.iloc[iteration * len(dp.harmonics): 
                                       (iteration + 1) * len(dp.harmonics), column]
                fig.add_trace(
                    dp.go.Bar(
                        x=dp.harmonics,
                        y=iteration_data,
                        name=f'{headers[column]} {title} : Iteration {iteration + 1}'
                    )
                )
            
            fig.update_layout(
                title=f'FFT Magnitudes - {headers[column]}',
                showlegend=True,
                xaxis_title='Harmonic Orders',
                yaxis_title='Magnitude',
                xaxis=dict(tickvals=dp.harmonics, ticktext=dp.harmonics),
                barmode='stack'
            )
            figure_list.append(fig)
            
            # Handle split reports for each column
            if dp.JSON['iterSplit']:
                plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                html_content = self.prep_html_template(Time_series=False)
                html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                output_path = f"{html_path}_{headers[column]}.html"
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(html_content)
    
    elif report_type == 'standalone':
        # Standalone report processing
        csv_files = data_source
        
        if len(csv_files) >= 1:
            dfs = [dp.pd.read_csv(f) for f in csv_files]
            
            if dfs:
                all_columns = dfs[0].columns.tolist()
                plot_columns = all_columns[1:] if len(all_columns) > 1 else all_columns
                plot_columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', each) for each in plot_columns]
                
                for each in plot_columns:
                    fig = dp.make_subplots()
                    C = 1
                    for df in dfs:
                        df.columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', col) for col in df.columns]
                        signal_units = [
                            dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] 
                            if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" 
                            for s in df.columns.values
                        ]
                        
                        fig.add_trace(
                            dp.go.Scatter(
                                x=df.iloc[:, 0],
                                y=df[each],
                                name=str("Iter :" + str(C) + " | ") + each,
                                mode="lines",
                                line=dict(shape='linear')
                            )
                        )
                        fig.update_layout(
                            showlegend=True,
                            title=each,
                            xaxis=dict(title='Time [S]'),
                            yaxis=dict(side="left", title=signal_units[C-1],
                                     titlefont=dict(color="#1f77b4"),
                                     tickfont=dict(color="#1f77b4")),
                            plot_bgcolor='#f8fafd'
                        )
                        C += 1
                    figure_list.append(fig)
                    
                    # Handle split reports for each column
                    if dp.JSON['iterSplit']:
                        plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                        html_content = self.prep_html_template(Time_series=False)
                        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                        output_path = f"{html_path}_Standalone_{each}.html"
                        with open(output_path, 'w', encoding='utf-8') as file:
                            file.write(html_content)
    
    # Handle consolidated report if iterSplit is disabled
    if not dp.JSON['iterSplit']:
        plot_items = ''
        for fig_i in figure_list:
            plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
        
        html_content = self.prep_html_template(Time_series=False)
        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
        
        # Determine output filename based on report type
        if report_type == 'signal':
            output_path = f"{html_path}_{kwargs.get('type', 'signal')}.html"
        elif report_type == 'fft':
            output_path = f"{html_path}_{kwargs.get('type', 'fft')}.html"
        else:  # standalone
            output_path = f"{html_path}_Standalone_Iterations.html"
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    
    # Auto-open if requested
    if auto_open and figure_list:
        dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())    














# For signal report
obj.generate_iteration_report(
    data_source='/path/to/csv/files',
    html_path='/path/to/output',
    auto_open=True,
    report_type='signal',
    label_dict={'Voltage': 1, 'Current': 2},
    Y_axis_label='Amplitude',
    type='voltage'
)

# For FFT report
obj.generate_iteration_report(
    data_source='/path/to/fft/file.csv',
    html_path='/path/to/output',
    auto_open=True,
    report_type='fft',
    title='FFT Analysis',
    FFT_file='fft_headers.json',
    type='current'
)

# For standalone report
obj.generate_iteration_report(
    data_source=['file1.csv', 'file2.csv'],
    html_path='/path/to/output',
    auto_open=True,
    report_type='standalone'
)






























def generate_iteration_report(self, data_source, html_path, auto_open, report_type='signal', **kwargs):
    """Generate iteration report for signal, FFT, or standalone data."""
    
    # Configuration based on report type
    configs = {
        'signal': {
            'get_files': lambda: [f for f in os.listdir(data_source) if f.endswith('.csv') 
                                 and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')],
            'get_data': lambda f: dp.pd.read_csv(os.path.join(data_source, f)),
            'get_plots': lambda df, labels: [(df.iloc[:,0], df.iloc[:,labels.get(k)]) for k in labels],
            'get_title': lambda key, i, df: f"Iter :{i+1} | {key}",
            'get_y_label': lambda df, i: kwargs.get('Y_axis_label', ''),
            'split_prefix': lambda key: f"{html_path}_{key}",
            'consolidated_suffix': f"{html_path}_{kwargs.get('type', 'signal')}.html"
        },
        'fft': {
            'headers': dp.json.load(open(f"{dp.os.getcwd()}/Script/assets/HEADER_FILES/{kwargs.get('FFT_file')}")) if 'FFT_file' in kwargs else [],
            'get_data': lambda: dp.pd.read_csv(data_source, header=None, index_col=None),
            'process': lambda: (lambda df: [
                (dp.harmonics, 
                 df.iloc[i*len(dp.harmonics):(i+1)*len(dp.harmonics), c])
                for c in range(df.shape[1]) for i in range(df.shape[0] // len(dp.harmonics))
            ])(dp.pd.read_csv(data_source, header=None, index_col=None)),
            'get_title': lambda key, i, _: f"{key} {kwargs.get('title','')} : Iteration {i+1}",
            'get_y_label': lambda *_: 'Magnitude',
            'split_prefix': lambda key: f"{html_path}_{key}",
            'consolidated_suffix': f"{html_path}_{kwargs.get('type', 'fft')}.html",
            'use_bar': True
        },
        'standalone': {
            'get_files': lambda: data_source,
            'get_data': lambda f: dp.pd.read_csv(f),
            'get_plots': lambda df, cols: [(df.iloc[:,0], df[dp.re.sub(r'[^a-zA-Z0-9]', '_', c)]) 
                                          for c in cols[1:]] if len(cols) > 1 else [],
            'get_title': lambda key, i, _: f"Iter :{i+1} | {key}",
            'get_y_label': lambda df, i: dp.unit_map.get(
                dp.pattern.search(" ".join(df.columns[i].split()[-2:])).group().lower() 
                if dp.pattern.search(" ".join(df.columns[i].split()[-2:])) else "", "[-]"),
            'split_prefix': lambda key: f"{html_path}_Standalone_{key}",
            'consolidated_suffix': f"{html_path}_Standalone_Iterations.html"
        }
    }
    
    cfg = configs[report_type]
    figure_list, plot_items = [], ''
    
    # Get data files and load dataframes
    files = cfg.get_files() if 'get_files' in cfg else [data_source]
    if not files: return
    
    dfs = [cfg.get_data(f) for f in (dp.natsorted(files) if isinstance(files, list) else files)]
    
    # Determine plot keys/columns
    if report_type == 'signal':
        keys = list(kwargs.get('label_dict', {}).keys())
    elif report_type == 'fft':
        keys = cfg['headers']
    else:  # standalone
        keys = [dp.re.sub(r'[^a-zA-Z0-9]', '_', c) for c in dfs[0].columns[1:]]
    
    # Generate figures
    for idx, key in enumerate(keys):
        fig = dp.make_subplots() if report_type != 'fft' else dp.go.Figure()
        
        for i, df in enumerate(dfs if report_type != 'fft' else [None]):
            if report_type == 'fft':
                plots = [(dp.harmonics, df.iloc[i*len(dp.harmonics):(i+1)*len(dp.harmonics), idx]) 
                        for df in [cfg.get_data()] for i in range(df.shape[0] // len(dp.harmonics))]
            else:
                label_dict = kwargs.get('label_dict', {}) if report_type == 'signal' else {}
                plots = cfg.get_plots(df, [key] if report_type == 'standalone' else label_dict)
            
            for x, y in ([plots[idx]] if report_type != 'fft' else plots):
                trace_func = dp.go.Bar if cfg.get('use_bar') else dp.go.Scatter
                fig.add_trace(trace_func(x=x, y=y, name=cfg.get_title(key, i, df), 
                                        mode="lines" if not cfg.get('use_bar') else None))
                
                if report_type != 'fft':
                    fig.update_layout(title=key, xaxis_title='Time [S]', 
                                     yaxis_title=cfg.get_y_label(df, i), plot_bgcolor='#f8fafd')
        
        if report_type == 'fft':
            fig.update_layout(title=f'FFT Magnitudes - {key}', xaxis_title='Harmonic Orders',
                            xaxis=dict(tickvals=dp.harmonics, ticktext=dp.harmonics), barmode='stack')
        
        figure_list.append(fig)
        
        # Handle split reports
        if dp.JSON['iterSplit']:
            html_content = self.prep_html_template(False).replace("{{PLOT_ITEMS}}", 
                         fig.to_html(full_html=False, include_plotlyjs='cdn'))
            with open(f"{cfg['split_prefix'](key)}.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
    
    # Handle consolidated report
    if not dp.JSON['iterSplit'] and figure_list:
        html_content = self.prep_html_template(False).replace("{{PLOT_ITEMS}}", 
                     ''.join(f.to_html(full_html=False, include_plotlyjs='cdn') for f in figure_list))
        with open(cfg['consolidated_suffix'], 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    # Auto-open
    if auto_open and figure_list:
        dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())




















def iterreports(self, report_type, **kwargs):
    """
    Unified method for generating iteration reports (signal, FFT, or standalone).
    
    Parameters:
        report_type (str): Type of report - 'signal', 'fft', or 'standalone'
        
    For 'signal' report_type:
        path (str): Path to directory containing CSV files
        label_dict (dict): Dictionary with column names as keys and indexes as values
        html_path (str): Path where HTML file should be saved
        Y_axis_label (str): Label for Y-axis
        type (str): Sets the type to current or voltage
        auto_open (bool): If True, opens HTML automatically
        
    For 'fft' report_type:
        FFT_file (str): FFT json header file
        title (str): Title to be included in the report
        csv_path (str): Path to the CSV file containing data
        html_path (str): Path to save the generated HTML report
        type (str): Sets the type to current or voltage
        auto_open (bool): If True, opens HTML automatically
        
    For 'standalone' report_type:
        csv_files (list): List of CSV standalone files
        html_path (str): Path where HTML file should be saved
        auto_open (bool): If True, opens HTML automatically
    """
    
    include_plotlyjs = 'cdn'
    plot_items = ''
    html_content = self.prep_html_template(Time_series=False)
    
    # SIGNAL REPORT
    if report_type == 'signal':
        path = kwargs.get('path')
        label_dict = kwargs.get('label_dict', {})
        html_path = kwargs.get('html_path')
        Y_axis_label = kwargs.get('Y_axis_label')
        report_subtype = kwargs.get('type')
        auto_open = kwargs.get('auto_open', False)
        
        labels_dict = dict(label_dict)
        dict_keys = list(labels_dict.keys())
        
        # Get CSV files
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv') 
                    and not f.endswith('_MAP.csv') 
                    and not f.endswith('_Standalone.csv')]
        
        if len(csv_files) >= 1:
            csv_files = dp.natsorted(csv_files)
            dfs = [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]
            
            fig_list = []
            for each in dict_keys:
                fig = dp.make_subplots()
                for C, df in enumerate(dfs, 1):
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
                fig_list.append(fig)
            
            # Handle split reports
            if dp.JSON['iterSplit']:
                for i, each in enumerate(dict_keys):
                    plot_items = fig_list[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    html_content = self.prep_html_template(Time_series=False)
                    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    with open(f"{html_path}_{each}.html", 'w', encoding='utf-8') as file:
                        file.write(html_content)
            else:
                for fig_i in fig_list:
                    plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                with open(f"{html_path}_{report_subtype}.html", 'w', encoding='utf-8') as file:
                    file.write(html_content)
                
                if auto_open:
                    dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())
    
    # FFT REPORT
    elif report_type == 'fft':
        FFT_file = kwargs.get('FFT_file')
        title = kwargs.get('title', '')
        csv_path = kwargs.get('csv_path')
        html_path = kwargs.get('html_path')
        report_subtype = kwargs.get('type')
        auto_open = kwargs.get('auto_open', False)
        
        # Load FFT headers and data
        headers_path = (dp.os.getcwd()).replace("\\", "/") + f"/Script/assets/HEADER_FILES/{FFT_file}"
        headers = dp.json.load(open(headers_path, 'r'))
        df = dp.pd.read_csv(csv_path, header=None, index_col=None)
        
        num_iterations = df.shape[0] // len(dp.harmonics)
        figure_list = []
        
        # Generate figures for each column
        for column in range(df.shape[1]):
            fig = dp.go.Figure()
            
            for iteration in range(num_iterations):
                start_idx = iteration * len(dp.harmonics)
                end_idx = (iteration + 1) * len(dp.harmonics)
                iteration_data = df.iloc[start_idx:end_idx, column]
                
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
            
            # Handle split reports
            if dp.JSON['iterSplit']:
                plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                html_content = self.prep_html_template(Time_series=False)
                html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                with open(f"{html_path}_{headers[column]}.html", 'w', encoding='utf-8') as file:
                    file.write(html_content)
        
        # Consolidated report
        if not dp.JSON['iterSplit']:
            plot_items = ''
            for fig_i in figure_list:
                plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
            html_content = self.prep_html_template(Time_series=False)
            html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
            with open(f"{html_path}_{report_subtype}.html", 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            if auto_open:
                dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())
    
    # STANDALONE REPORT
    elif report_type == 'standalone':
        csv_files = kwargs.get('csv_files')
        html_path = kwargs.get('html_path')
        auto_open = kwargs.get('auto_open', False)
        
        if len(csv_files) >= 1:
            dfs = [dp.pd.read_csv(f) for f in csv_files]
            
            if dfs:
                all_columns = dfs[0].columns.tolist()
                plot_columns = all_columns[1:] if len(all_columns) > 1 else all_columns
                plot_columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', each) for each in plot_columns]
                
                fig_list = []
                for each in plot_columns:
                    fig = dp.make_subplots()
                    
                    for C, df in enumerate(dfs, 1):
                        # Clean column names
                        df.columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', col) for col in df.columns]
                        
                        # Get signal units
                        signal_units = []
                        for s in df.columns.values:
                            match = dp.pattern.search(" ".join(s.split()[-2:]))
                            if match:
                                signal_units.append(dp.unit_map[match.group().lower()])
                            else:
                                signal_units.append("[-]")
                        
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
                    fig_list.append(fig)
                    
                    # Handle split reports
                    if dp.JSON['iterSplit']:
                        plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                        html_content = self.prep_html_template(Time_series=False)
                        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                        with open(f"{html_path}_Standalone_{each}.html", 'w', encoding='utf-8') as file:
                            file.write(html_content)
                
                # Consolidated report
                if not dp.JSON['iterSplit']:
                    plot_items = ''
                    for fig_i in fig_list:
                        plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    html_content = self.prep_html_template(Time_series=False)
                    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    with open(f"{html_path}_Standalone_Iterations.html", 'w', encoding='utf-8') as file:
                        file.write(html_content)
                    
                    if auto_open:
                        dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())











def auto_plot(self, simutil, fileLog, misc, open=False, iterReport=False):
    """
    Generates an HTML report containing multiple plots.

    Args:
        misc (object): Miscellaneous object containing utility functions.
        open (bool, optional): If True, open the generated HTML report automatically.
        iterReport (bool, optional): If True, generate iterations HTML report.
    """

    # start the timer .define directories and file paths. get the list of CSV files 
    # in the results directory for time series data and MAPS
    # set FFT csv file paths and sort files. initialize counter and legend flag based on configuration
    misc.tic()
    ResDir = (dp.os.getcwd()).replace("\\", "/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"
    MAPS_dir = (dp.os.getcwd()).replace("\\", "/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"
    FFT_curr_path = MAPS_dir+"/FFT_Current_Map.csv"
    FFT_volt_path = MAPS_dir+"/FFT_Voltage_Map.csv"
    file_list = fileLog.natsort_files(ResDir)
    legend = True if dp.JSON['TF_Config'] == 'DCDC_D' else False
    c = 0
    standalone_csv_files = fileLog.natsort_files(ResDir, standalone=True)

    # generate iteration reports if iterReport is True using unified method
    if iterReport:
        # Signal reports for currents and voltages
        self.iterreports('signal',
                        path=ResDir,
                        label_dict=dp.pmap_multi['Peak_Currents'],
                        html_path=fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,
                        Y_axis_label="[ A ]",
                        type="Currents",
                        auto_open=open)
        
        self.iterreports('signal',
                        path=ResDir,
                        label_dict=dp.pmap_multi['Peak_Voltages'],
                        html_path=fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,
                        Y_axis_label="[ V ]",
                        type="Voltages",
                        auto_open=open)

        # FFT reports if enabled
        if dp.JSON['FFT']:
            self.iterreports('fft',
                           FFT_file="FFT_Current.json",
                           title=" ",
                           csv_path=FFT_curr_path,
                           html_path=fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,
                           type="Currents_FFT",
                           auto_open=open)
            
            self.iterreports('fft',
                           FFT_file="FFT_Voltage.json",
                           title=" ",
                           csv_path=FFT_volt_path,
                           html_path=fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,
                           type="Voltages_FFT",
                           auto_open=open)

    # loop through each CSV file, generate plots, and append to HTML report
    for x in range(len(file_list)):
        FFT_figs = self.fft_bar_plot(FFT_curr_path, FFT_volt_path, x)
        figures_list = self.plot_scopes(file_list[x], dp.pmap_plt, Legend=legend)
        figures_list_ = self.interleaved(figures_list, FFT_figs)

        # drop extra columns from the CSV file if DCDC_S or DCDC_D
        # and generate control figures and extend to the main figure list
        if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':
            simutil.postProcessing.drop_Extra_Cols(file_list[x], sum(dp.Y_list[0:3]), sum(dp.Y_list[0:4]))
            figures_list_ctrl = self.plot_scopes(file_list[x], dp.pmap_plt_ctrl, Legend=True)
            figures_list_.extend(figures_list_ctrl)

        c += 1

        # generate standalone time series and iteration html reports
        if standalone_csv_files:
            std_figures_list = self.plot_std(standalone_csv_files[x])
            self.append_to_html(standalone_csv_files[x], std_figures_list,
                              fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_Standalone_" + str(c) + ".html",
                              auto_open=open, i=c-1, standalone=True)

            if iterReport:
                # Standalone iteration report using unified method
                self.iterreports('standalone',
                               csv_files=standalone_csv_files,
                               html_path=fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,
                               auto_open=open)

        self.append_to_html(file_list[x], figures_list_,
                          fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_" + str(c) + ".html",
                          auto_open=open, i=c-1)
        self.constants_list, self.constants_vals, self.constants_units, figures_list_ = [], [], [], []

    # Generate 2D or 3D html report for signals and FFT
    if iterReport:
        self.repo_3d(fileLog, simutil)

    # log the completion of HTML report generation and clear file list
    fileLog.line_separator()
    fileLog.log(f"Generating HTML Report    {'= '.rjust(49+17, ' ')}{str(misc.toc())} seconds.\n")
    file_list.clear()








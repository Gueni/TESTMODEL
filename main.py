    def iter_report_signal(self,path,label_dict,html_path,Y_axis_label,type,auto_open):
        """
            Generates an iteration report in HTML format for a set of CSV files located in a given directory.

            Parameters:
                self            : (object) The object of the class containing the function.
                path            : (str) The path to the directory containing the CSV files.
                label_dict      : (dict) A dictionary containing the column names as keys and the corresponding indexes as values.
                html_path       : (str) The path where the HTML file should be saved.
                Y_axis_label    : (str) The label for the Y-axis of the generated graphs.
                auto_open       : (bool) If True, opens the generated HTML report in a new browser window automatically.
        """
        # Initialize variables and read CSV files from the specified directory
        fig_list          =   []
        include_plotlyjs  =   'cdn'
        labels_dict       =   dict(label_dict)
        dict_keys         =   list(labels_dict.keys())
        csv_files         =   [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]
        plot_items        =   ''
        html_content      =   self.prep_html_template(Time_series = False)

        # Load one or more CSV files, sorts them, and converts them into DataFrames.For each key in dict_keys, a Plotly subplot
        # is created and populated with line plots of the corresponding data column vs. time from each CSV, labeled by iteration.
        if len(csv_files) >= 1:
            csv_files     =   dp.natsorted(csv_files)
            dfs           =   [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]
            for each in dict_keys :
                fig = dp.make_subplots()
                C         =   1
                for df in dfs :
                    fig.add_trace(
                        dp.go.Scatter(
                            x       = df.iloc[:,0]                                 ,
                            y       = df.iloc[:,labels_dict.get(each)]             ,
                            name    = str("Iter :" + str(C) + " | ") + each   ,
                            mode    = "lines"                                      ,
                            line    = dict(shape = 'linear')
                        )
                    )

                    fig.update_layout(
                        showlegend      =   True                                    ,
                        title           =   each                                    ,
                        xaxis           =   dict(title='Time [ S ]')                ,
                        yaxis           =   dict(side= "left",title= Y_axis_label,titlefont= dict(color="#1f77b4") ,tickfont= dict(color="#1f77b4")),
                        plot_bgcolor    =   '#f8fafd'
                    )
                    C+=1
                fig_list.append(fig)

            # If 'iterSplit' is enabled in the JSON settings, a separate HTML report is generated for each key.
            if dp.JSON['iterSplit']:
                for i in range(len(dict_keys)):
                        
                    plot_items      =  fig_list[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    # Get FRESH HTML template for each file (CRITICAL!)
                    html_content    = self.prep_html_template(Time_series=False)
                    html_content    = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    with open(html_path + "_" + dict_keys[i] + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                    file.close()

            # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
            if not dp.JSON['iterSplit']:
                for fig_i in fig_list:
                    plot_items      +=  fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)

                # Replace plot items
                html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)

                # Write the populated HTML
                with open(html_path + "_" + type + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                file.close()

            # If auto_open is enabled, the generated HTML report is automatically opened in the default web browser.
            if auto_open: dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())











def iter_report_fft(self, FFT_file,title, csv_path, html_path, type ,auto_open):
    """
    Generate an HTML report with FFT magnitudes for multiple iterations.

    Args:
        title       (str)   : Title to be included in the report.
        csv_path    (str)   : Path to the CSV file containing data.
        html_path   (str)   : Path to save the generated HTML report.
        auto_open   (bool)  : Whether to automatically open the HTML report in a web browser.
        type        (str)   : sets the type to current or voltage.
        FFT_file    (str)   : FFT json header file.
    """

    # Set Plotly to load JavaScript from the CDN Load FFT headers from the specified JSON file.
    # Read the FFT CSV data into a pandas DataFrame without headers or index columns .Initialize an empty list to store generated Plotly figures.
    # Calculate the number of iterations based on the total number of rows and the number of harmonics.
    include_plotlyjs          = 'cdn'
    headers                   = dp.json.load(open((dp.os.getcwd()).replace("\\","/") + f"/Script/assets/HEADER_FILES/{FFT_file}" , 'r'))
    df                        = dp.pd.read_csv(csv_path, header=None,index_col=None)
    figure_list               = []
    num_iterations            = df.shape[0] // len(dp.harmonics)

    # Loop through each column in the DataFrame to create bar plots of FFT magnitudes.Initialize a new Plotly figure for the current column.
    # Add a bar trace for each iteration, slicing the data according to harmonics.Update the figure layout with titles, axis labels, tick settings,
    # and stacked bar mode.Append the configured figure to the figure_list.
    for column in range(df.shape[1]):
        fig                   = dp.go.Figure()

        for iteration in range(num_iterations):
            iteration_data    = df.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), column]
            fig.add_trace(
                dp.go.Bar(
                        x     =   dp.harmonics                                                          ,
                        y     =   iteration_data                                                        ,
                        name  =   f'{headers[column]} {title} : Iteration {iteration + 1}'
                        ))

        fig.update_layout(
                            title           =   f'FFT Magnitudes - {headers[column]}'                   ,
                            showlegend      =   True                                                    ,
                            xaxis_title     =   'Harmonic Orders'                                       ,
                            yaxis_title     =   'Magnitude'                                             ,
                            xaxis           =   dict (tickvals = dp.harmonics ,ticktext = dp.harmonics) ,
                            barmode         =   'stack'
                        )
        figure_list.append(fig)

        # If 'iterSplit' is enabled, create a separate HTML report for each FFT column.
        if dp.JSON['iterSplit']:
            # Get FRESH plot_items and html_content for EACH file
            plot_items = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
            html_content = self.prep_html_template(Time_series=False)
            html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)

            file_path = html_path + "_" + str(headers[column]) + ".html"
            with open(file_path, 'w', encoding='utf-8') as file: 
                file.write(html_content)
    
    # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
    if not dp.JSON['iterSplit']:
        plot_items = ''
        for fig_i in figure_list:
            plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
        
        # Get fresh HTML template
        html_content = self.prep_html_template(Time_series=False)
        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)

        # Write the populated HTML
        file_path = html_path + "_" + type + ".html"
        with open(file_path, 'w', encoding='utf-8') as file: 
            file.write(html_content)

    # If auto_open is enabled, the generated HTML report is automatically opened in the default web browser.
    # Need to decide which file to open when iterSplit is True
    if auto_open:
        if dp.JSON['iterSplit'] and figure_list:
            # Open the last file created
            last_file_path = html_path + "_" + str(headers[-1]) + ".html"
            dp.webbrowser.open(dp.pathlib.Path(last_file_path).absolute().as_uri())
        elif not dp.JSON['iterSplit']:
            file_path = html_path + "_" + type + ".html"
            dp.webbrowser.open(dp.pathlib.Path(file_path).absolute().as_uri())
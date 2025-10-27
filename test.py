def gen_iter_report(self, path, label_dict, html_path, Y_axis_label, type, auto_open):
    """
    Generates an iteration report in HTML format for a set of CSV files located in a given directory.

    Parameters:
    -----------
    self : object
        The object of the class containing the function.

    path : str
        The path to the directory containing the CSV files.

    label_dict : dict
        A dictionary containing the column names as keys and the corresponding indexes as values.

    html_path : str
        The path where the HTML file should be saved.

    Y_axis_label : str
        The label for the Y-axis of the generated graphs.

    auto_open : bool
        If True, opens the generated HTML report in a new browser window automatically.
    type : string
           sets the type to current , voltage .

    Returns:
    --------
    None

    """
    include_plotlyjs = 'cdn'
    labels_dict = dict(label_dict)
    dict_keys = list(labels_dict.keys())
    
    # Separate regular CSV files and Standalone CSV files
    regular_csv_files = [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]
    standalone_csv_files = [f for f in os.listdir(path) if f.endswith('_Standalone.csv')]
    
    # Process regular CSV files (original logic)
    if len(regular_csv_files) >= 1:
        self._process_csv_files(regular_csv_files, path, labels_dict, dict_keys, html_path, Y_axis_label, type, auto_open, include_plotlyjs, "_" + type)
    
    # Process Standalone CSV files (new logic)
    if len(standalone_csv_files) >= 1:
        self._process_csv_files(standalone_csv_files, path, labels_dict, dict_keys, html_path, Y_axis_label, type, auto_open, include_plotlyjs, "_Standalone_" + type)

def _process_csv_files(self, csv_files, path, labels_dict, dict_keys, html_path, Y_axis_label, type, auto_open, include_plotlyjs, file_suffix):
    """
    Helper function to process CSV files and generate HTML reports
    """
    fig_list = []
    
    csv_files = dp.natsorted(csv_files)  # Sort the file list Alphanumerically.
    
    # Read each csv into a Pandas dataframe with appropriate header handling
    dfs = []
    for f in csv_files:
        if f.endswith('_Standalone.csv'):
            # For Standalone files, use header=0 to read the first row as column names
            df = dp.pd.read_csv(os.path.join(path, f), header=0)
        else:
            # For regular files, use the original behavior (no header)
            df = dp.pd.read_csv(os.path.join(path, f))
        dfs.append(df)
    
    for each in dict_keys:
        fig = dp.make_subplots()
        C = 1
        for df, csv_file in zip(dfs, csv_files):
            # Handle column access based on whether it's a Standalone file or not
            if csv_file.endswith('_Standalone.csv'):
                # For Standalone files, use column names directly
                x_data = df.iloc[:, 0]  # First column
                # Try to get column by name, fall back to index if not found
                if each in df.columns:
                    y_data = df[each]
                else:
                    y_data = df.iloc[:, labels_dict.get(each)]
            else:
                # For regular files, use the original index-based access
                x_data = df.iloc[:, 0]
                y_data = df.iloc[:, labels_dict.get(each)]
            
            fig.add_trace(
                dp.go.Scatter(
                    x=x_data,
                    y=y_data,
                    name=str("Iter :" + str(C) + " | ") + each,
                    mode="lines",
                    line=dict(shape='linear')
                )
            )

            fig.update_layout(
                showlegend=True,
                title=each,
                xaxis=dict(title='Time [ S ]'),
                yaxis=dict(
                    side="left",
                    title=Y_axis_label,
                    titlefont=dict(color="#1f77b4"),
                    tickfont=dict(color="#1f77b4")
                ),
                plot_bgcolor='#f8fafd'
            )
            C += 1
        fig_list.append(fig)
        
        # Generate HTML files based on iterSplit setting
        if dp.JSON['iterSplit']:
            date = str(dp.datetime.datetime.now().replace(microsecond=0))
            with open(html_path + "_" + each + file_suffix + ".html", 'w') as f:
                f.write(self.title)
                f.write('<style>    .container  {position: relative;text-align: right;color: black;}    \
                                    .Simulation {position: absolute;top: 10px;left: 16px;}              \
                                    .DateTime   {position: absolute;top: 50px;left: 16px;}              \
                                    .Sim_ID     {position: absolute;top: 90px;left: 16px;}              \
                            </style>'\
                            f'<div class="container">  \
                                        <img src="data:image/png;base64,{self.image}"/> \
                                        <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>\
                                        <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div> \
                                        <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div> \
                            </div>')

                f.write(self.separator)
                f.write(fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                f.write(self.separator)
            f.close()

    if not dp.JSON['iterSplit']:
        date = str(dp.datetime.datetime.now().replace(microsecond=0))
        with open(html_path + file_suffix + ".html", 'w') as f:
            f.write(self.title)
            f.write('<style>    .container  {position: relative;text-align: right;color: black;}    \
                                    .Simulation {position: absolute;top: 10px;left: 16px;}              \
                                    .DateTime   {position: absolute;top: 50px;left: 16px;}              \
                                    .Sim_ID     {position: absolute;top: 90px;left: 16px;}              \
                            </style>'\
                            f'<div class="container">  \
                                        <img src="data:image/png;base64,{self.image}"/> \
                                        <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>\
                                        <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div> \
                                        <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div> \
                            </div>')

            f.write(self.separator)
            for fig_i in fig_list:
                f.write(fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                f.write(self.separator)
        f.close()
    
    if auto_open and (len(regular_csv_files) > 0 or len(standalone_csv_files) > 0):
        import pathlib, webbrowser
        uri = pathlib.Path(html_path).absolute().as_uri()
        webbrowser.open(uri)
def gen_iter_report(self, path, html_path, auto_open):
    """
    Generates an iteration report in HTML format for a set of CSV files located in a given directory.

    Parameters:
    -----------
    self : object
        The object of the class containing the function.

    path : str
        The path to the directory containing the CSV files.

    html_path : str
        The path where the HTML file should be saved.

    auto_open : bool
        If True, opens the generated HTML report in a new browser window automatically.

    Returns:
    --------
    None

    """
    fig_list = []
    include_plotlyjs = 'cdn'
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]    # Get all csv files in the directory

    if len(csv_files) >= 1:
        csv_files = dp.natsorted(csv_files)                                                               # Sort the file list Alphanumerically.
        dfs = [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]              # Read each csv into a Pandas dataframe
        
        # Get all column names from the first CSV (assuming all CSVs have same structure)
        if dfs:
            all_columns = dfs[0].columns.tolist()
            # Skip the first column (assuming it's time/x-axis)
            plot_columns = all_columns[1:] if len(all_columns) > 1 else all_columns
            
            for each in plot_columns:
                fig = dp.make_subplots()
                C = 1
                for df in dfs:
                    fig.add_trace(
                        dp.go.Scatter(
                            x = df.iloc[:, 0],
                            y = df[each],
                            name = str("Iter :" + str(C) + " | ") + each,
                            mode = "lines",
                            line = dict(shape='linear')
                        )
                    )

                    # Determine Y-axis label based on column name pattern
                    y_axis_label = "Value"
                    each_lower = each.lower()
                    if any(word in each_lower for word in ['current', 'amp']):
                        y_axis_label = "Current [A]"
                    elif any(word in each_lower for word in ['voltage', 'volt']):
                        y_axis_label = "Voltage [V]"
                    elif any(word in each_lower for word in ['loss', 'dissipation']):
                        y_axis_label = "Loss [W]"
                    elif any(word in each_lower for word in ['power']):
                        y_axis_label = "Power [W]"
                    elif any(word in each_lower for word in ['temperature', 'temp']):
                        y_axis_label = "Temperature [°C]"

                    fig.update_layout(
                        showlegend = True,
                        title = each,
                        xaxis = dict(title='Time [S]'),
                        yaxis = dict(
                            side = "left",
                            title = y_axis_label,
                            titlefont = dict(color="#1f77b4"),
                            tickfont = dict(color="#1f77b4")
                        ),
                        plot_bgcolor = '#f8fafd'
                    )
                    C += 1
                fig_list.append(fig)
                #!-----------------------------------------------------------------------------------
                #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
                #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent
                #* page loads faster.
                if dp.JSON['iterSplit']:
                    date = str(dp.datetime.datetime.now().replace(microsecond=0))
                    with open(html_path + "_" + each + ".html", 'w') as f:
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
            with open(html_path + ".html", 'w') as f:  # Removed _type from filename
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
        if auto_open:
            import pathlib, webbrowser
            uri = pathlib.Path(html_path).absolute().as_uri()
            webbrowser.open(uri)
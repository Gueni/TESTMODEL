
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                                                ____            ____  _       _
#?                                                               |  _ \ _   _    |  _ \| | ___ | |_
#?                                                               | |_) | | | |   | |_) | |/ _ \| __|
#?                                                               |  __/| |_| |   |  __/| | (_) | |_
#?                                                               |_|    \__, |___|_|   |_|\___/ \__|
#?                                                                      |___/_____|
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class HTML_REPORT:
    def __init__(self,ResultsPath='',utc=''):
        """
        Initialize the HTML_REPORT class with various attributes and load configuration data from a JSON file.
        """
        self.ResultsPath                =   ResultsPath                                                                                                     # Path to store results
        self.utc                        =   utc                                                                                                             # UTC timestamp string
        self.hostname                   =   str(dp.socket.gethostname())                                                                                    # Host machine name
        self.script_name                =   dp.scriptname                                                                                                   # Current script name
        self.values_dict                =   dict()                                                                                                          # Dictionary to store values
        self.valkey_list                =   []                                                                                                              # List of value keys
        self.values_list                =   []                                                                                                              # List of values
        self.headerColor                =   '#009ADA'                                                                                                       # Hex color for header
        self.title                      =   f"{self.script_name}_Report_{self.utc}_{self.hostname}"                                                         # HTML page title template
        self.tab_val_list               =   []                                                                                                              # List for table values
        self.iter_param_key             =   []                                                                                                              # List of iteration parameter keys
        self.iter_param_val             =   []                                                                                                              # List of iteration parameter values
        self.iter_param_unt             =   []                                                                                                              # List of iteration parameter units
        self.note                       =   "N/A"                                                                                                           # Note field with default "N/A"
        self.constants_list             =   []                                                                                                              # List of constant names
        self.constants_vals             =   []                                                                                                              # List of constant values
        self.constants_units            =   []                                                                                                              # List of constant units
        self.json_path                  =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", "Input_vars.json").replace("\\", "/")                       # Path to JSON file
        with open(self.json_path) as f  :   self.data = dp.json.load(f)                                                                                     # Load JSON data into self.data
        for i in range(1, 11)           :   setattr(self, f"X{i}", eval(self.data[f"X{i}"]))                                                                # Dynamically set X1-X10 attributes
        self.html_template              =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", "HTML_REPORT_TEMPLATE.html").replace("\\", "/")             # Html report template file.
        self.date                       =   str(dp.datetime.datetime.now().replace(microsecond=0))                                                          # Date and time variable.
        self.html_template_iter         =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", "HTML_REPORT_TEMPLATE_iter.html").replace("\\", "/")        # Iteration Html report template file.
        self.stylesheet                 =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", "styles.css").replace("\\", "/")                            # CSS style sheet.
        self.interleaved                =   lambda l1 , l2 : list(x for x in dp.chain.from_iterable(dp.zip_longest(l1,l2)) if x is not None)
        self.Xs_to_dict                 =   lambda Xs : dict((f"X{i+1}",v) for i,v in enumerate(Xs))

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

    def mdlvar_params_table(self,i):
        """
            Generate plotly table figure for modelvar dictionary containing sub-dictionaries
            and simulation parameters for the current iteration.The layout also include a dropdown menu
            which helps select , interactively,which sub-dictionary to display. Defualt is all data.

            Parameters  : i     (int)       : Number of the current iteration.
            Return      : fig   (object)    : Plotly figure : table.
        """
        dropdown_level      =   3
        dropdown_buttons    =   []
        data_dict           =   self.tab_val_list[i]

        def brackets_notation(d, parent_keys=None):
            """Flatten a nested dictionary using bracket notation"""
            if parent_keys is None:
                parent_keys = []

            items = []
            for k, v in d.items():
                current_keys = parent_keys + [k]
                if isinstance(v, dict):
                    items.extend(brackets_notation(v, current_keys))
                else:
                    # Create bracket notation: ["key1"]["key2"]["key3"]
                    bracket_path = ''.join([f'["{key}"]' for key in current_keys])
                    items.append((bracket_path, v))
            return items

        def get_paths_at_level(d, current_level=1, target_level=1, current_path=None):
            """Get dictionary paths at specified level"""
            if current_path is None: current_path = []
            paths   = []

            # If we've reached the target level, return current path as an option
            if current_level == target_level:
                if current_path:  # Only add if we have a path
                    path_str = "->".join(current_path)
                    paths.append(("->".join(current_path), current_path.copy()))
            else:
                # If we haven't reached target level yet, continue traversing
                for key, value in d.items():
                    if isinstance(value, dict):
                        new_path = current_path + [key]
                        paths.extend(get_paths_at_level(value, current_level + 1, target_level, new_path))

            # Always include "all" option at any level
            if current_level == 1: paths.insert(0, ("all", []))

            return paths

        def get_subdict_by_path(d, path_keys):
            """Get sub-dictionary by path keys"""
            if not path_keys: return d
            current = d
            for key in path_keys:
                if isinstance(current, dict) and key in current: current = current[key]
                else: return {}
            return current if isinstance(current, dict) else {path_keys[-1]: current}

        available_paths         = get_paths_at_level(data_dict, target_level=dropdown_level)
        flattened_items         = brackets_notation(data_dict)
        parameters              = [item[0] for item in flattened_items]
        values                  = [str(item[1]) for item in flattened_items]
        table                   = dp.go.Table(      header  =   dict(
                                                                    values      =   ['PARAMETERS', 'VALUE']                    ,
                                                                    fill_color  =   self.headerColor                           ,
                                                                    align       =   'center'
                                                            ),
                                                    cells   =   dict(
                                                                    values      =   [parameters, values]                       ,
                                                                    align       =   ['left', 'left']
                                                            ),
                                                    domain  =   dict(x=[0, 1], y=[0, 0.9])  # Table occupies bottom 90%

                                        )

        for path_label, path_keys in available_paths:
            if path_label == "all": # Show all parameters
                flattened_items = brackets_notation(data_dict)
                params          = [item[0] for item in flattened_items]
                vals            = [str(item[1]) for item in flattened_items]
            else:   # Get specific sub-dictionary at the chosen level
                sub_dict        = get_subdict_by_path(data_dict, path_keys)
                if isinstance(sub_dict, dict) and sub_dict:
                    flattened_items = brackets_notation(sub_dict, path_keys)
                    params          = [item[0] for item in flattened_items]
                    vals            = [str(item[1]) for item in flattened_items]
                else:   # If it's not a dict or empty, show it as a single parameter
                    if path_keys:
                        bracket_path    = ''.join([f'["{key}"]' for key in path_keys])
                        params          = [bracket_path]
                        vals            = [str(sub_dict)]
                    else:
                        params          = []
                        vals            = []

            args=[{"cells": {
                                    "values": [params, vals]  ,
                                    "align"       :   ['left', 'left']                           ,
                                    "line_color"  :   'darkslategray'
                                    }}]
            dropdown_buttons.append(dict(label=path_label,method="update",args=args))


        fig = dp.go.Figure(data=[table])

        # Layout with clear section separation
        fig.update_layout(
            height          =   500,
            margin          =   dict(t=10, l=20, r=20, b=10),
            plot_bgcolor    =   'white',
            paper_bgcolor   =   'white',
            updatemenus     =   [dict(
                                        buttons     =   dropdown_buttons,
                                        direction   =   "down",
                                        showactive  =   True,
                                        x           =   0.0,
                                        xanchor     =   "left",
                                        y           =   0.95,
                                        yanchor     =   "middle",
                                        bgcolor     =   "white",
                                        bordercolor =   "#2E86AB",
                                        borderwidth =   1,
                                        font        =   dict(size=12),
                                        active      =   0
                                    )
                                ]
        )

        return fig

    def operational_params_table(self,csv_file):
        """
            Reads in a CSV file containing data and creates a table of constants by taking the mean values of certain columns.
            The columns to use are defined in a constant dictionaries list. The resulting table is displayed using Plotly,
            a Python visualization library, and returned.

            Parameters  :   csv_file (str)      : The path to a CSV file containing the data to use for calculating the constants.
            Return      :   fig   (object)      : A Plotly figure object representing the constant table.
        """

        # Read in the CSV file and create a DataFrame
        df                      =   dp.pd.read_csv(csv_file)

        # Loop through the constant dictionaries and calculate the mean values for each column
        # Append the constant names, values, and units to separate lists
        for _ , val in dp.constant_dict.items():
            column_values = df.iloc[:, val[1]]
            column_values = column_values.to_numpy()
            column_values = column_values[-50:]
            self.constants_list.append(val[0])
            self.constants_vals.append(dp.np.mean(column_values).round(2))
            self.constants_units.append(val[2])

        # Create a Plotly table to display the constants
        # Use alternating row colors for better readability and set header color
        # set table layout and title
        constants_tab           =   dp.go.Table(    header  =   dict(
                                                                values      =   ['PARAMETER','VALUE','UNIT']                                      ,
                                                                fill_color  =   self.headerColor                                                  ,
                                                                font_size   =   12                                                                ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(
                                                                values      =   [self.constants_list,self.constants_vals,self.constants_units]    ,
                                                                align       =   ['left', 'center']
                                                            )
                                        )

        # Create a subplot to hold the table
        fig = dp.go.Figure(data=[constants_tab])

        # Layout with clear section separation
        fig.update_layout(
            height          =   450 ,
                        margin          =   dict(t=30, l=20, r=20, b=30)
        )

        return fig

    def focused_params_table(self,i=0):
        """
            Generate plotly table figure for the focusedparameters dictionary for the current iteration.

            Parameters  : i     (int)       : Number of the current iteration.
            Return      : fig   (object)    : Plotly figure : table.
        """
        #* Focused parameters values table-------------------------------------
        # Create a Plotly table to display the focused parameters
        updated_vals_table       =   dp.go.Table(    header  =   dict(
                                                                values      =   ['FOCUSED PARAMETERS', 'VALUE','UNIT']                      ,
                                                                fill_color  =   self.headerColor                                     ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(   values      =  [self.iter_param_key[i], self.iter_param_val[i] ,self.iter_param_unt[i]],
                                                                align       =   ['left', 'left'] ,
                                                            )
                                        )

        fig = dp.go.Figure(data=[updated_vals_table])

        # Layout with clear section separation
        fig.update_layout(
            height=200,
            margin          =   dict(t=30, l=20, r=20, b=20)
        )
        return fig
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
    def multiplot(self,csv_file):
        """
        Generate a plot of voltage and current data from a Plecs simulation output file.
        This function reads voltage and current data from a CSV file generated by a Plecs simulation.
        The data is assumed to be organized in columns, with the first column containing the time values.
        The function generates a plot with two y-axes, one for the current data and one for the voltage data.
        The plot includes a menu that allows the user to toggle the display of the current and voltage data.

        Args:
            csv_file (str): The path to the CSV file containing the data.

        Returns:
            A plotly.graph_objs._figure.Figure object representing the plot.

        Raises:
            FileNotFoundError: If the specified CSV file does not exist.
        """

        # Genarate dataframe from csv file.
        # Retrieve data index dictionaries from plecs_mapping module.
        # Get keys from previously defined dictionaries (to be used as labels)
        dff                     = dp.pd.read_csv(csv_file)
        Voltages_labels_dict    = dp.pmap_multi['Peak_Voltages']
        Currents_labels_dict    = dp.pmap_multi['Peak_Currents']
        PWM_labels_dict         = dp.pwm_dict
        voltage_keys            = list(Voltages_labels_dict.keys())
        Current_keys            = list(Currents_labels_dict.keys())
        PWM_keys                = list(PWM_labels_dict.keys())
        fig                     = dp.make_subplots(specs=[[{"secondary_y": True}]])

        # Create and add Traces for th Current Plots.
        for each in Current_keys:fig.add_trace(dp.go.Scatter(x= dff.iloc[:,0],y= dff.iloc[:,Currents_labels_dict.get(each)],name= each,mode= "lines",line= dict(shape = 'linear', dash = 'dot')),secondary_y=False)

        # Create and add Traces for th Voltage Plots.
        for each in voltage_keys:fig.add_trace(dp.go.Scatter(x= dff.iloc[:,0],y= dff.iloc[:,Voltages_labels_dict.get(each)],name= each,mode= "lines",line= dict(shape = 'linear')),secondary_y=True)

        # Create and add Traces for th PWM Plots.
        for each in PWM_keys:fig.add_trace(dp.go.Scatter(x= dff.iloc[:,0],y= dff.iloc[:,PWM_labels_dict.get(each)],name= each,mode= "lines+markers",line= dict(shape = 'linear', dash = 'dashdot')),secondary_y=True)

        # Define button for showing all plots.
        button_all          = dict(
                                    label   = 'CURRENTS & VOLTAGES & PWM'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'CURRENTS & VOLTAGES & PWM'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )
        # Define button for showing Current plots.
        button_curr          = dict(
                                    label   = 'CURRENTS'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [False for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [False for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'CURRENTS'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )
        # Define button for showing all plots.
        button_volt          = dict(
                                    label   = 'VOLTAGES'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [False for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'VOLTAGES'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )
        # Define button for showing PWM plots.
        button_pwm          = dict(
                                    label   = 'PWM SIGNALS'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [False for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'PWM SIGNALS'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )
        # Define button for showing PWM and voltages plots.
        button_pwm_volt          = dict(
                                    label   = 'PWM & VOLTAGES'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'PWM SIGNALS & VOLTAGES'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )
        # Define button for showing PWM and currentsplots.
        button_pwm_curr          = dict(
                                    label   = 'PWM & CURRENTS'                                             ,
                                    method  = 'update'                                          ,
                                    args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \
                                                                [False for j in range(len(list(Voltages_labels_dict.values())))]+ \
                                                                [True for j in range(len(list(Voltages_labels_dict.values())))],
                                                'title'     : 'PWM SIGNALS & CURRENTS'                             ,
                                                'showlegend': True
                                                }
                                            ],
                                    )

        # Initialize and Define layout arguments for overall plots.Set titles, axis labels, colors, and background color.
        # Add the update menu with buttons to the layout.Set the initial visibility of all traces to True.
        fig.update_layout(
            height          =   500,
            margin          =   dict(t=20, l=20, r=20, b=20),
            updatemenus     =   [dp.go.layout.Updatemenu(active  = 0,buttons = [button_all,button_curr,button_volt,button_pwm,button_pwm_volt,button_pwm_curr],direction = 'up',x= 0,xanchor = 'left',y= -0.1,yanchor = 'top')],
            xaxis           =   dict(title='Time [ s ]')                            ,
            yaxis           =   dict(side= "left",title= "Current [ A ]",titlefont= dict(color="#1f77b4"),tickfont= dict(color="#1f77b4")),
            yaxis2          =   dict(side="right",title="Voltage [ V ]",titlefont=dict(color="#1f77b4"),tickfont=dict(color="#1f77b4")),
            plot_bgcolor    =   '#f8fafd'
            )

        return fig

    def plot_scopes(self,fName,odict,xticks=None,yticks=None,xaxis_range=None,yaxis_range=None,Legend=True):
        """
            Generates a list of subplots for the data in a CSV file, based on the specifications in the input dictionaries.

            Parameters
            ----------
            fName : str
                The path of the CSV file to read.
            odict : dict
                A dictionary of dictionaries specifying the data to plot in each subplot. The keys are the names of the subplots,
                and the values are dictionaries with the following keys:
                - 0: a list of strings, representing the names of the columns in the CSV file to plot on the y-axis.
                - 1: a list of strings, representing the names of the traces to plot in each column.
                - 2: a list of integers, representing the indices of the columns in the CSV file to plot.
                - 3: a list of strings, representing the titles of the y-axes for each column.
            splt_titles : list of str
                A list of strings representing the titles of the subplots.
            xticks : float or None, optional
                The tick interval for the x-axis. If None, the default tick interval is used.
            yticks : float or None, optional
                The tick interval for the y-axis. If None, the default tick interval is used.
            xaxis_range : list of float or None, optional
                The range of values to display on the x-axis. If None, the default range is used.
            yaxis_range : list of float or None, optional
                The range of values to display on the y-axis. If None, the default range is used.
            Legend          :       bool.
                                If True activates the legend in the figure, default is True.

            Returns
            -------
            list of plotly.graph_objs._figure.Figure
                A list of subplots, each represented as a Plotly Figure object.

            Raises
            ------
            FileNotFoundError
                If the specified CSV file does not exist.
        """

        # Initialize an empty list to hold the figures
        # Read the CSV file into a Pandas DataFrame
        figure_list     = []
        df              = dp.pd.read_csv(fName)

        # Loop through the input dictionary and create a subplot for each key
        # Set the titles, axis labels, and other properties of the subplot
        for key, _ in odict.items():
                titles      = [odict[key][x][1][0] for x in range(len(odict[key]))]
                fig         = dp.make_subplots(rows=len(odict[key]), cols=1,subplot_titles=titles,shared_xaxes=True,vertical_spacing=0.08)

                # Loop through the columns specified in the input dictionary and add traces to the subplot
                for j in range(len(odict[key])):
                    for i in range(len(odict[key][j][0])):
                        X,Y     =   df.iloc[:,0],df.iloc[:,odict[key][j][2][i]]

                        # Handle the case where all Y values are the same
                        # If all Y values are the same, only plot the first and last values
                        if len(set(Y)) == 1:
                            new_df = dp.pd.DataFrame({'X': [X.iloc[0], X.iloc[-1]], 'Y': [Y.iloc[0], Y.iloc[-1]]})
                            fig.add_trace(dp.go.Scatter(x=new_df['X'], y=new_df['Y'], name=odict[key][j][0][i]), row=j+1, col=1)

                        # Otherwise, plot all the Y values
                        else:
                            fig.add_trace(dp.go.Scatter(x=X, y=Y, name=odict[key][j][0][i]), row=j+1, col=1)

                    # Set the y-axis title and other properties for each subplot
                    fig['layout'][f'yaxis{j+1}']['title']= odict[key][j][3][i]

                # Set the x-axis title and other properties for the entire figure
                # Update the x-axis and y-axis ranges and tick intervals if specified
                fig['layout'][f'xaxis{j+1}']['title']= 'Time [s]'
                fig.update_xaxes(range=xaxis_range, dtick=xticks)
                fig.update_yaxes(range=yaxis_range, dtick=yticks)

                # If Legend is True, show the legend for the figure
                if Legend   ==  True:

                    # Special handling for DCDC_D configuration to always show legend
                    if dp.JSON['TF_Config'] == 'DCDC_D':
                        fig.update_layout(title={'text' : str(key) },showlegend = True)

                    # For other configurations, show legend only if there are multiple traces
                    else:
                        # Check if there are multiple traces in the subplot
                        # If there are multiple traces, show the legend else hide it
                        if len(odict[key])>1:
                            fig.update_layout(title={'text' : str(key) },showlegend = True)

                        else:
                            fig.update_layout(
                                            showlegend      =   False           ,
                                            plot_bgcolor    =   '#f8fafd'     ,
                                            yaxis2          =   dict(anchor='free',position=0,side='left')
                                            )
                else:

                    # If Legend is False, hide the legend for the figure
                    fig.update_layout(showlegend = False)

                # Set hover mode to "x unified" for better interactivity
                # Remove hover template to use default hover behavior
                # Add the figure to the list of figures
                fig.update_traces(hovertemplate=None)
                fig.update_layout(hovermode="x unified"
                )
                figure_list.append(fig)

        # Return the list of figures
        return figure_list

    def plot_std(self,csv_file):
        """
        Create Plotly figures from CSV standalone data with Time as x-axis and signals as y-axis (with header).

        Parameters  :   csv_file (str)  : Path to the CSV file
        Returns     :   list     (list) : List of Plotly figure objects
        """
        # Read CSV file and Get signal names (all columns except first)
        df                           = dp.pd.read_csv(csv_file)
        time_col   ,signal_names     = df.columns[0] ,df.columns[1:]
        figures                      = []
        units                        = [dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in signal_names]

        # Create individual figure for each signal
        for i, (signal_name, unit) in enumerate(zip(signal_names, units)):
            fig = dp.go.Figure()
            fig.add_trace(dp.go.Scatter(x=df[time_col],y=df[signal_name],mode='lines',showlegend=False,line=dict(color='blue')))
            fig.update_layout(title=dp.re.sub(r'[^a-zA-Z0-9]', '_', signal_name) ,xaxis_title=time_col,yaxis_title=f"{unit}",template="plotly_white")
            figures.append(fig)

        return figures

    def fft_bar_plot(self,current_fft_csv, voltage_fft_csv, iteration):
        """
        Generate a bar plot of FFT magnitudes for current and voltage signals.

        Parameters  :
                            current_fft_csv      :         String
                                                            Path to the CSV file containing current data.
                            voltage_fft_csv      :         String
                                                            Path to the CSV file containing voltage data.
                            iteration            :         int
                                                            Iteration index.
            Returns        :  figure_list          :         list
                                                            List of plotly figures.
        """

        # Load current and voltage FFT headers from JSON.
        # Read current and voltage FFT CSV data into pandas DataFrames without headers or index columns.
        # Initialize an empty list to store generated Plotly figures.
        Current_headers               = dp.json.load(open((dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Current.json" , 'r'))
        Voltage_headers               = dp.json.load(open((dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Voltage.json" , 'r'))
        dfcurr                        = dp.pd.read_csv(current_fft_csv, header=None,index_col=None)
        dfvolt                        = dp.pd.read_csv(voltage_fft_csv, header=None,index_col=None)
        figure_list                   = []

        # Loop through each entry in dp.plt_title_list to create subplots.
        for i in range(len(dp.plt_title_list)):

            # Create a Plotly subplot with a secondary y-axis for combined current and voltage plotting.
            fig                   = dp.make_subplots(rows=1, cols=1,specs=[[{"secondary_y": True}]])

            # Determine the indices of current columns to plot from Current_headers based on plt_title_list structure.
            # Determine the indices of voltage columns to plot from Voltage_headers based on plt_title_list structure.
            current_idx_list      = [Current_headers.index(dp.plt_title_list[i][1] + " FFT")] if len(dp.plt_title_list[i])<5 else [ Current_headers.index(dp.plt_title_list[i][1] + " FFT") , Current_headers.index(dp.plt_title_list[i][2] + " FFT")  ]
            voltage_idx_list      = [Voltage_headers.index(dp.plt_title_list[i][2] + " FFT")] if len(dp.plt_title_list[i])<5 else [ Voltage_headers.index(dp.plt_title_list[i][3] + " FFT") , Voltage_headers.index(dp.plt_title_list[i][4] + " FFT")  ]

            # Extract the titles for current traces from plt_title_list.
            # Extract the titles for voltage traces from plt_title_list.
            current_titles        = [dp.plt_title_list[i][1]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][1] , dp.plt_title_list[i][2]  ]
            voltage_titles        = [dp.plt_title_list[i][2]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][3] , dp.plt_title_list[i][4]  ]

            # If FFT plotting is enabled in the JSON settings, add bar traces for current and voltage.
            # Current traces are plotted on the primary y-axis, and voltage traces on the secondary y-axis.
            # The data for each trace is sliced according to the current iteration and harmonics length.
            # If FFT plotting is disabled, return an empty list immediately.
            if dp.JSON['FFT'] :
                for c, name in enumerate(current_titles):
                    fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfcurr.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), current_idx_list[c]], name=name), row=1, col=1,secondary_y=False)
                for j, name in enumerate(voltage_titles):
                    fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfvolt.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), voltage_idx_list[j]], name=name), row=1, col=1,secondary_y=True)
            else:
                    return []

            # Update the layout of the FFT figure with a title, axis labels, tick settings, and background color.
            # The primary y-axis shows current magnitudes and the secondary y-axis shows voltage magnitudes.
            # Bar traces are overlaid for comparison, and the configured figure is appended to figure_list.
            fig.update_layout(
                                title           =   f'FFT Magnitudes - {dp.plt_title_list[i][0]}'               ,
                                xaxis_title     =   'Harmonic Orders'                                           ,
                                xaxis           =   dict (tickvals = dp.harmonics ,ticktext = dp.harmonics)     ,
                                yaxis           =   dict(
                                                        side        = "left"                                    ,
                                                        title       = "Current Magnitude"                       ,
                                                        titlefont   = dict(color="#1f77b4")                     ,
                                                        tickfont    = dict(color="#1f77b4"))                    ,
                                yaxis2          =   dict(
                                                        side        = "right"                                   ,
                                                        title       = "Voltage Magnitude"                       ,
                                                        titlefont   = dict(color="#1f77b4")                     ,
                                                        tickfont    = dict(color="#1f77b4"))                    ,
                                plot_bgcolor    =   '#f8fafd'                                                   ,
                                barmode         =   'overlay'
                            )
            figure_list.append(fig)

        return figure_list

    def barchart3D(self,x_vals, y_vals, z_vals, title, z_title, x_title, y_title, opacity=1):
        """
            Emulate the creation of a 3D bar chart in plotly using mesh3D.

            Parameters      :   x_vals  (array-like)    : array of X values.
                                y_vals  (array-like)    : array of Y values.
                                z_vals  (array-like)    : array of Z values.
                                title   (String)        : title of the plot.
                                z_title (String)        : z axis title.
                                x_title (String)        : x axis title.
                                y_title (String)        : y axis title.
                                opacity (float)         : cuboid opacity. default to 1.
            Return          :   fig     (object)        : plotly figure.
        """
        fig, ann                = dp.go.Figure(), []
        x_vals                  = dp.np.array(x_vals, dtype=int)
        y_vals, z_vals          = map(lambda arr: dp.np.array(arr, dtype=float),(y_vals, z_vals))
        x_unique ,y_unique      = dp.np.unique(x_vals) , dp.np.unique(y_vals)

        # Base spacing between unique points
        dx_base = dp.np.min(dp.np.diff(x_unique)) if len(x_unique) > 1 else 1.0
        dy_base = dp.np.min(dp.np.diff(y_unique)) if len(y_unique) > 1 else 1.0

        # Scale width inversely with the number of unique bars ==> if you have 20 bars, bars will be thinner than if you have 2
        nx, ny = len(x_unique), len(y_unique)
        scale_factor = 0.6 / dp.np.sqrt(max(nx, ny))

        # prevent being too thin
        dx = dx_base * (0.8 * scale_factor + 0.2)
        dy = dy_base * (0.8 * scale_factor + 0.2)

        # Keep small minimums to avoid division errors
        dx, dy = max(dx, 1e-6), max(dy, 1e-6)

        for i, z_max in enumerate(z_vals):
            x_cnt, y_cnt    = x_vals[i], y_vals[i]
            x_min, x_max    = x_cnt - dx/2, x_cnt + dx/2
            y_min, y_max    = y_cnt - dy/2, y_cnt + dy/2
            x               = [x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max]
            y               = [y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min]
            z               = [0, 0, 0, 0, z_max, z_max, z_max, z_max]

            # Visible bar
            fig.add_trace(dp.go.Mesh3d(x=x, y=y, z=z,alphahull=0,color="royalblue",showscale=False,opacity=opacity,hoverinfo='none'))

            # Transparent hover plane
            fig.add_trace(dp.go.Mesh3d(
                x=[x_min, x_max, x_max, x_min],
                y=[y_min, y_min, y_max, y_max],
                z=[z_max, z_max, z_max, z_max],
                color='rgba(0,0,0,0)',
                opacity=0.0,
                hovertemplate=(f"<b>{x_title}</b>: {x_cnt:.2f}<br>"f"<b>{y_title}</b>: {y_cnt:.2f}<br>"f"<b>{z_title}</b>: {z_max:.2f}<extra></extra>"),
                hoverlabel=dict(bgcolor='rgba(30,30,30,0.8)',font_color='white',bordercolor='white'),showlegend=False
                ))

        fig.update_layout(
            title=dict(text=title, x=0.5, xanchor='center', yanchor='top'),
            scene=dict(
                xaxis=dict(title=x_title,tickmode='array',tickvals=x_vals,ticktext=[str(int(v)) for v in x_vals],
                title_font=dict(size=10),tickfont=dict(size=10),autorange='reversed'),
                yaxis=dict(title=y_title,title_font=dict(size=10),tickfont=dict(size=10),autorange='reversed'),
                zaxis=dict(title=z_title,title_font=dict(size=10),tickfont=dict(size=10)),
                annotations=ann
                ),
            hoverlabel=dict(bgcolor='rgba(50,50,50,0.8)',font_color='white',bordercolor='white')
        )

        return fig
#*-------------------------------------------------------------------------------------------------------------------------------------------------------------
    def iter_reports(self, report_type, **kwargs):
        """
        Unified method for generating iteration reports (signals, FFT, or standalone).

        Parameters:
            report_type (str): Type of report - 'signal', 'fft', or 'standalone'

            For 'signal' report_type:

                path (str)          : Path to directory containing CSV files
                label_dict (dict)   : Dictionary with column names as keys and indexes as values
                html_path (str)     : Path where HTML file should be saved
                Y_axis_label (str)  : Label for Y-axis
                type (str)          : Sets the type to current or voltage
                auto_open (bool)    : If True, opens HTML automatically

            For 'fft' report_type:

                FFT_file (str)      : FFT json header file
                title (str)         : Title to be included in the report
                csv_path (str)      : Path to the CSV file containing data
                html_path (str)     : Path to save the generated HTML report
                type (str)          : Sets the type to current or voltage
                auto_open (bool)    : If True, opens HTML automatically

            For 'standalone' report_type:

                csv_files (list)    : List of CSV standalone files
                html_path (str)     : Path where HTML file should be saved
                auto_open (bool)    : If True, opens HTML automatically
        """

        include_plotlyjs        = 'cdn'
        plot_items              = ''
        html_content            = self.prep_html_template(Time_series=False)

        #--------- SIGNAL REPORTS ---------------------------------------------
        if report_type == 'signal':

            path            = kwargs.get('path')
            label_dict      = kwargs.get('label_dict', {})
            html_path       = kwargs.get('html_path')
            Y_axis_label    = kwargs.get('Y_axis_label')
            report_subtype  = kwargs.get('type')
            auto_open       = kwargs.get('auto_open', False)
            labels_dict     = dict(label_dict)
            dict_keys       = list(labels_dict.keys())
            csv_files       = [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]

            if len(csv_files) >= 1:

                csv_files   = dp.natsorted(csv_files)
                dfs         = [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]
                fig_list    = []

                for each in dict_keys:

                    fig = dp.make_subplots()
                    for C, df in enumerate(dfs, 1):
                        fig.add_trace(
                            dp.go.Scatter(
                                            x       =   df.iloc[:, 0]                           ,
                                            y       =   df.iloc[:, labels_dict.get(each)]       ,
                                            name    =   str("Iter :" + str(C) + " | ") + each   ,
                                            mode    =   "lines"                                 ,
                                            line    =   dict(shape='linear')
                                        )
                                    )
                        fig.update_layout(
                                            showlegend      =   True                                                                                                    ,
                                            title           =   each                                                                                                    ,
                                            xaxis           =   dict(title='Time [ s ]')                                                                                ,
                                            yaxis           =   dict(side="left", title=Y_axis_label,titlefont=dict(color="#1f77b4"),tickfont=dict(color="#1f77b4")),
                                            plot_bgcolor    = '#f8fafd'
                                        )
                    fig_list.append(fig)

                # If 'iterSplit' is enabled in the JSON settings, a separate HTML report is generated for each key.
                if dp.iterSplit:
                    for i in range(len(dict_keys)):
                        plot_items      =  fig_list[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                        html_content    = self.prep_html_template(Time_series=False) # Get FRESH HTML template for each file
                        html_content    = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                        with open(html_path + "_" + dict_keys[i] + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                        file.close()

                # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
                if not dp.iterSplit:
                    for fig_i in fig_list:
                        plot_items      +=  fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    with open(html_path + "_" + str(report_subtype) + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                    file.close()

        #--------- FFT REPORTS ------------------------------------------------
        elif report_type == 'fft':

            FFT_file        = kwargs.get('FFT_file')
            title           = kwargs.get('title', '')
            csv_path        = kwargs.get('csv_path')
            html_path       = kwargs.get('html_path')
            report_subtype  = kwargs.get('type')
            auto_open       = kwargs.get('auto_open', False)
            headers_path    = (dp.os.getcwd()).replace("\\", "/") + f"/Script/assets/HEADER_FILES/{FFT_file}"
            headers         = dp.json.load(open(headers_path, 'r'))
            df              = dp.pd.read_csv(csv_path, header=None, index_col=None)
            num_iterations  = df.shape[0] // len(dp.harmonics)
            figure_list     = []

            # Generate figures for each column
            for column in range(df.shape[1]):

                fig = dp.go.Figure()

                for iteration in range(num_iterations):
                    start_idx       = iteration * len(dp.harmonics)
                    end_idx         = (iteration + 1) * len(dp.harmonics)
                    iteration_data  = df.iloc[start_idx:end_idx, column]

                    fig.add_trace(
                                    dp.go.Bar(
                                        x       =   dp.harmonics                                            ,
                                        y       =   iteration_data                                          ,
                                        name    =   f'{headers[column]} {title} : Iteration {iteration + 1}'
                                    )
                                )

                fig.update_layout(
                                    title       =   f'FFT Magnitudes - {headers[column]}'                   ,
                                    showlegend  =   True                                                    ,
                                    xaxis_title =   'Harmonic Orders'                                       ,
                                    yaxis_title =   'Magnitude'                                             ,
                                    xaxis       =   dict(tickvals=dp.harmonics, ticktext=dp.harmonics)      ,
                                    barmode     =   'stack'
                                )

                figure_list.append(fig)

                # If 'iterSplit' is enabled, create a separate HTML report for each FFT column.
                if dp.iterSplit:
                    # Get FRESH plot_items and html_content for EACH file
                    plot_items      = fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                    html_content    = self.prep_html_template(Time_series=False)
                    html_content    = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    file_path       = html_path + "_" + str(headers[column]) + ".html"
                    with open(file_path, 'w', encoding='utf-8') as file: file.write(html_content)

            # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
            if not dp.iterSplit:
                plot_items      = ''
                for fig_i in figure_list:
                    plot_items += fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                html_content    = self.prep_html_template(Time_series=False)
                html_content    = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                file_path       = html_path + "_" + report_subtype + ".html"
                with open(file_path, 'w', encoding='utf-8') as file: file.write(html_content)

        #--------- STANDALONE  SIGNAL REPORTS ---------------------------------
        elif report_type == 'standalone':

            csv_files   = kwargs.get('csv_files')
            html_path   = kwargs.get('html_path')
            auto_open   = kwargs.get('auto_open', False)

            if len(csv_files) >= 1:
                dfs     = [dp.pd.read_csv(f) for f in csv_files]

                if dfs:
                    all_columns     = dfs[0].columns.tolist()
                    # Skip the first column (assuming it's time/x-axis)
                    plot_columns    = all_columns[1:] if len(all_columns) > 1 else all_columns
                    plot_columns    = [dp.re.sub(r'[^a-zA-Z0-9]', '_', each) for each in plot_columns]
                    fig_list        = []

                    for each in plot_columns:
                        fig         = dp.make_subplots()
                        C=1
                        for df in dfs:
                            # Clean column names
                            df.columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', col) for col in df.columns]
                            signal_units = [dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in df.columns.values]
                            # Find which column index 'each' corresponds to in the current dataframe
                            col_idx      = df.columns.get_loc(each) if each in df.columns else 1
                            fig.add_trace(
                                    dp.go.Scatter(
                                                    x       =   df.iloc[:, 0]                           ,
                                                    y       =   df[each]                                ,
                                                    name    =   str("Iter :" + str(C) + " | ") + each   ,
                                                    mode    =   "lines"                                 ,
                                                    line    =   dict(shape='linear')
                                                )
                                        )

                            fig.update_layout(
                                                showlegend  =   True                                                                                                            ,
                                                title       =   each                                                                                                            ,
                                                xaxis       =   dict(title='Time [s]')                                                                                          ,
                                                yaxis       =   dict(side="left", title=signal_units[col_idx],titlefont=dict(color="#1f77b4"),tickfont=dict(color="#1f77b4"))   ,
                                                plot_bgcolor=   '#f8fafd'
                                            )
                            C += 1
                        fig_list.append(fig)

                    # If 'iterSplit' is enabled in the JSON settings, a separate HTML report is generated for each key.
                    if dp.iterSplit:
                        for i in range(len(plot_columns)):

                            plot_items      =  fig_list[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                            html_content    = self.prep_html_template(Time_series=False)
                            html_content    = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                            with open(html_path + "_Standalone_" + plot_columns[i] + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                            file.close()

                    # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
                    if not dp.iterSplit:
                        for fig_i in fig_list:
                            plot_items      +=  fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                        with open(html_path + "_Standalone_Iterations.html", 'w', encoding='utf-8') as file: file.write(html_content)
                        file.close()

        # If auto_open is enabled, the generated HTML report is automatically opened in the default web browser.
        if auto_open: dp.webbrowser.open(dp.Path(html_path).absolute().as_uri())

    def graph_scopes(self,fileLog,simutil,standalone_exist=False):
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
                        if dp.JSON["perturbation"]==0:
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

        #!========================================================

        csv_maps_dir            = f"{fileLog.resultfolder}/CSV_MAPS"
        csv_time_series_dir     = f"{fileLog.resultfolder}/CSV_TIME_SERIES"

        if standalone_exist:
            # Load headers from time series standalone files
            time_series_files       = fileLog.natsort_files(csv_time_series_dir,standalone=True)
            standalone_matrices     = {}
            headers_lists           = []  # Collect all headers from all files
            headers_array           = []

            if time_series_files:
                df              = dp.pd.read_csv(time_series_files[0])
                base_headers    = [dp.re.sub(r'[^a-zA-Z0-9]', '_', header) for header in df.columns[1:].tolist()]# Skip first column (Time)

            print("base_headers",base_headers)


            mat_names           = ["Standalone_RMS","Standalone_AVG","Standalone_MAX","Standalone_MIN","Standalone_FFT"]
            mat_suffix          = ['RMS', 'AVG', 'MAX', 'MIN', 'FFT']
            d,N                 = 4,1

            for file_type, file_name in zip(mat_suffix, mat_names):
                file_path                       = dp.os.path.join(csv_maps_dir, file_name + '_Map.csv')
                df                              = dp.pd.read_csv(file_path, header=None)
                standalone_matrices[file_type]  = df.values.astype(float)
                # if   file_type == 'FFT'         : file_headers = [f"{h}_FFT" for h in base_headers] if base_headers else [f"FFT_{i}" for i in range(df.shape[1])]
                # elif file_type == 'FFT_Sens'    : file_headers = [f"{h}_FFT_Sens" for h in base_headers] if base_headers else [f"FFT_Sens_{i}" for i in range(df.shape[1])]
                file_headers = [f"{h}_{file_type}" for h in base_headers] if base_headers else [f"{file_type}_{i}" for i in range(df.shape[1])]
                headers_lists.append(file_headers)

            print("hearderlist",headers_lists)
            for i in range(d)       : headers_array.extend(headers_lists[i])
            FFT_headers             = headers_lists[d]*N

            # Combine non-FFT matrices
            combined_matrix = None
            for file_type in mat_suffix[0:d]:
                    if combined_matrix is None:
                        combined_matrix = standalone_matrices[file_type]
                    else:
                        combined_matrix = dp.np.hstack((combined_matrix, standalone_matrices[file_type]))


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
        sweep_vars          = {k: v for k, v in self.Xs_to_dict(simutil.sweepMatrix).items() if v != [0]}
        print("sweep_vars = ",sweep_vars)
        sweep_keys          = list(sweep_vars.keys())
        print("sweep_keys = ",sweep_keys)

        active_sweep_keys   = [k for k, v in sweep_vars.items() if v != [0] and len(v)>1]
        print("active_sweep_keys = ",active_sweep_keys)

        # Decide 2D plotting or 3D  based on number of active sweep Xlists and use the single X list for 2D if it is the case
        plot_2D             = len(active_sweep_keys) == 1
        single_X_key        = active_sweep_keys[0] if plot_2D else None

        # Generate all combinations for the sweep based on algorithm (permute = True : permuted sweeps combo | permute = False : non permuted sequential sweeps combo)
        all_combos          = (list(dp.product(*sweep_vars.values())) if dp.JSON["permute"] else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in sweep_vars.values()], arr).tolist())
        print("all_combos = ",all_combos)

        # For FFT combinations it is the same but repeated for the number of harmonics
        if dp.JSON['FFT']   : fft_combos          = list(map(tuple, dp.np.repeat(all_combos, len(dp.harmonics), axis=0).astype(object)))
        print("fft_combos = ",fft_combos)

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
                    if dp.JSON["perturbation"]==0:
                        if dp.np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
                            x_plot = dp.np.array([sweep_values[0], sweep_values[-1]])
                            z_plot = dp.np.array([z_vals[0], z_vals[-1]])
                    else:
                        x_plot = sweep_values
                        z_plot = z_vals

                    fig = dp.go.Figure()
                    fig.add_trace(dp.go.Scatter(
                        x=x_plot, y=z_plot, mode='lines',
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
            if dp.iterSplit:
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
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_{component}_{self.utc}.html"))).replace('\\','/'), component_plots)
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
            other_vars                  = {k: v for k, v in self.Xs_to_dict(simutil.sweepMatrix).items() if dp.re.fullmatch(r"X\d+", k) and k not in [var1, var2] and v != [0] and not dp.JSON["sweepNames"][int(dp.re.search(r'\d+', k).group())-1].startswith("X")}
            print("other_vars = ",other_vars)

            fixed_keys                  = list(other_vars.keys())
            print("fixed_keys = ",fixed_keys)

            fixed_combos                = (list(dp.product(*other_vars.values())) if dp.JSON["permute"] else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None, [v[-1] for v in other_vars.values()], arr).tolist())
            print("fixed_combos = ",fixed_combos)

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
            if dp.iterSplit:

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
                    if dp.JSON["perturbation"]==0 :
                        if dp.np.allclose(z_vals, Z[0, 0], rtol=relative_tol, atol=absolute_tol):
                            # Keep only first and last rows and columns
                            X = dp.np.array([X[0, :], X[-1, :]])       # first & last row
                            Y = dp.np.array([Y[0, :], Y[-1, :]])
                            Z = dp.np.array([Z[0, :], Z[-1, :]])

                    full_title              =  f'{component}<br>{format_fixed_title(fixed_dict, sweepNames)}'
                    fig                     =  dp.go.Figure(data=[dp.go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict())])
                    fig.update_layout(
                                        title               =   dict(
                                                                        text                =   full_title                                              ,
                                                                        x                   =   0.5                                                     ,
                                                                        xanchor             =   'center'                                                ,
                                                                        yanchor             =   'top'
                                                                    ),
                                        scene               =   dict(
                                                                        xaxis               =   dict(autorange='reversed')                              ,
                                                                        yaxis               =   dict(autorange='reversed')                              ,
                                                                        xaxis_title         =   sweepNames[int(dp.re.search(r'\d+', var1).group())-1]   ,
                                                                        yaxis_title         =   sweepNames[int(dp.re.search(r'\d+', var2).group())-1]   ,
                                                                        zaxis_title         =   component                                               ,
                                                                        xaxis_title_font    =   dict(size=10)                                           ,
                                                                        yaxis_title_font    =   dict(size=10)                                           ,
                                                                        zaxis_title_font    =   dict(size=10)                                           ,
                                                                        xaxis_tickfont      =   dict(size=10)                                           ,
                                                                        yaxis_tickfont      =   dict(size=10)                                           ,
                                                                        zaxis_tickfont      =   dict(size=10)
                                                                    )
                                    )

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
                            write_html_report((dp.os.path.normpath(dp.os.path.join(html_folder, f"HTML_GRAPH_Standalone_{self.utc}_{component}.html"))).replace('\\','/'), fft_plots[start:end])
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
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
    def prep_html_template(self,Time_series = True):
        """
            Load and prepare the html template to be used depending on the Time_series argument.
            By default the template to be used is the time series one.

            Parameters :
                            Time_series  (bool)   : select the desired html template file.
            Return     :
                            html_content (string) : string of modified html source code.
        """
        def minify_css(css):
            # Remove comments, whitespace, etc.
            css = dp.re.sub(r'/\*.*?\*/', '', css, flags=dp.re.DOTALL)
            css = dp.re.sub(r'\s+', ' ', css)
            css = dp.re.sub(r';\s*', ';', css)
            css = dp.re.sub(r':\s*', ':', css)
            css = dp.re.sub(r'\s*\{\s*', '{', css)
            css = dp.re.sub(r'\s*\}\s*', '}', css)
            return css.strip()

        if Time_series:
            # load the time series html file template.
            with open(self.html_template, 'r', encoding='utf-8') as file: html_content = file.read()
        else:
            # load the iterations html file template.
            with open(self.html_template_iter, 'r', encoding='utf-8') as file: html_content = file.read()

        # the CSS styling sheet content gets ported in both cases.
        with open(self.stylesheet, 'r')  as f: css = minify_css(f.read())
        html_content = dp.re.sub(r'<style>.*?</style>'  , f'<style>{css}</style>' , html_content, flags=dp.re.DOTALL)

        with open(dp.BMW_Base64_Logo, 'r', encoding='utf-8') as logo_file: logo_base64 = logo_file.read().strip()

        # Replace the variables
        html_content = html_content.replace("{{TITLE}}"         , self.title)
        html_content = html_content.replace("{{SCRIPT_NAME}}"   , self.script_name)
        html_content = html_content.replace("{{DATE_TIME}}"     , self.date)
        html_content = html_content.replace("{{SIMULATION_ID}}" , self.utc)
        html_content = html_content.replace("{{LOGO_BASE64}}"   , logo_base64)

        file.close()
        return html_content

    def append_to_html(self,csv_filename,figure, filename,auto_open, i=1,include_plotlyjs='cdn',standalone = False):
        """
            Appends figures to an existing html file.

            Parameters        :     csv_filename        (String)    The path to a CSV file containing the data to use for calculating the data.
                                    figure              (Object)    Plotly lib graph objects class object.
                                    filename            (String)    Path of the html file.
                                    auto_open           (bool)      Determines whether the file should open automatically. Defaults to False.
                                    include_plotlyjs    (String)    Defaults to 'cdn'. check to html  : https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.to_html
                                    standalone          (bool)      if Ture use standalone html filling , else append normally.
        """
        if not standalone:
            multiplot       = self.multiplot(csv_filename)
            param_table     = self.mdlvar_params_table(i)
            focused_table   = self.focused_params_table(i)

            if dp.JSON["figureName"] and dp.JSON["figureComment"]:

                self.FigureNames                =   [dp.plt_title_list[i][0] for i in range(len(dp.plt_title_list))]
                self.fftFigureNames             =   [f'FFT {dp.plt_title_list[i][0]}' for i in range(len(dp.plt_title_list))]
                self.CtrlFigureNames            =   list(dp.pmap_plt_ctrl.keys())
                self.FigTitles                  =   (self.interleaved(self.FigureNames, self.fftFigureNames)) + self.CtrlFigureNames
                self.Comments                   =   [" " for _ in range((2*len(dp.plt_title_list))+ len(self.CtrlFigureNames))]

            html_content              = self.prep_html_template()
            table_items               = ''
            focused_table_items       = ''
            multiplot_item            = ''
            plot_items                = ''
            constant_items            = ''
            table_items              += param_table.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
            focused_table_items      += focused_table.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
            multiplot_item           += multiplot.to_html(full_html=False, include_plotlyjs=include_plotlyjs)

            if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                for b in range(len(dp.JSON["figureName"])): self.Comments[self.FigTitles.index(dp.JSON["figureName"][b])] =  dp.JSON["figureComment"][b]

            for i in range(len(figure)):
                plot_items      += figure[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)

                if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                    if not self.Comments[i] == " " :
                        plot_items += f'<input type="text" class="comment-box" style="font-size:9pt;height:50px;width:1500px;" value="{self.comments[i]}" readonly="readonly">'

            # Generate a table of constants from the CSV file and write its HTML representation to the report.
            # Clear the stored constants lists to reset for the next use.
            constant_tables      = self.operational_params_table(csv_filename)
            constant_items      +=  constant_tables.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
            self.constants_list.clear()
            self.constants_vals.clear()
            self.constants_units.clear()

            # If figure names and comments are used, clear all related lists to reset the state for future reports.
            if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                self.FigTitles.clear()
                self.FigureNames.clear()
                self.fftFigureNames.clear()
                self.Comments.clear()

            # Replace plot items
            html_content        = html_content.replace("{{TABLE_ITEMS}}", table_items)
            html_content        = html_content.replace("{{FOCUSED_ITEMS}}", focused_table_items)
            html_content        = html_content.replace("{{NOTE_TEXT}}", self.note)
            html_content        = html_content.replace("{{multiplot_ITEMS}}", multiplot_item)
            html_content        = html_content.replace("{{PLOT_ITEMS}}", plot_items)
            html_content        = html_content.replace("{{constants_ITEMS_TABLE}}", constant_items)

        else :
            html_content        = self.prep_html_template(Time_series=False)
            plot_items          = ''

            for i in range(len(figure)):
                plot_items      += figure[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs)

            html_content        = html_content.replace("{{PLOT_ITEMS}}", plot_items)

        # Write the populated HTML
        with open(filename, 'w', encoding='utf-8') as file: file.write(html_content)
        file.close()

        # If auto_open is True, automatically open the generated HTML file in the default web browser.
        if auto_open: dp.webbrowser.open(dp.Path(filename).absolute().as_uri())

    def auto_plot(self,simutil,fileLog,misc,open=False,iterReport=False):
        """
        Generates an HTML report containing multiple plots.

        Args:
            misc (object)               : Miscellaneous object containing utility functions.
            Open (bool, optional)       : If True, open the generated HTML report automatically. Defaults to False.
            iterReport (bool, optional) : If True, generate iterations HTML report. Defaults to False.
        """

        # start the timer. define directories and file paths. get the list of CSV files in the results directory for time series data and MAPS
        # set FFT csv file paths and sort files. initialize counter and legend flag based on configuration
        misc.tic()
        ResDir                  =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"
        MAPS_dir                =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"
        FFT_curr_path           =   MAPS_dir+"/FFT_Current_Map.csv"
        FFT_volt_path           =   MAPS_dir+"/FFT_Voltage_Map.csv"
        file_list               =   fileLog.natsort_files(ResDir)
        legend                  =   True if dp.JSON['TF_Config'] == 'DCDC_D' else False
        c  ,d                     =   0,0
        standalone_csv_files    =   fileLog.natsort_files(ResDir,standalone=True)

        # generate iteration reports if iterReport is True
        if dp.JSON['TF_Config'] and iterReport :

            # Signal reports for currents
            self.iter_reports(
                            'signal'                                                                                ,
                            path            =   ResDir                                                              ,
                            label_dict      =   dp.pmap_multi['Peak_Currents']                                      ,
                            html_path       =   fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc ,
                            Y_axis_label    =   "[ A ]"                                                             ,
                            type            =   "Currents"                                                          ,
                            auto_open       =   open
                            )

            # Signal reports for voltages
            self.iter_reports(
                            'signal'                                                                                ,
                            path            =   ResDir                                                              ,
                            label_dict      =   dp.pmap_multi['Peak_Voltages']                                      ,
                            html_path       =   fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc ,
                            Y_axis_label    =   "[ V ]"                                                             ,
                            type            =   "Voltages"                                                          ,
                            auto_open       =   open
                            )

            # if FFT reports is enabled
            if dp.JSON['FFT']:

                # FFT reports for currents
                self.iter_reports(
                            'fft'                                                                                   ,
                            FFT_file        =   "FFT_Current.json"                                                  ,
                            title           =   " "                                                                 ,
                            csv_path        =   FFT_curr_path                                                       ,
                            html_path       =   fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc ,
                            type            =   "Currents_FFT"                                                      ,
                            auto_open       =   open
                            )

                # FFT reports for voltages
                self.iter_reports(
                            'fft'                                                                                   ,
                            FFT_file        =   "FFT_Voltage.json"                                                  ,
                            title           =   " "                                                                 ,
                            csv_path        =   FFT_volt_path                                                       ,
                            html_path       =   fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc ,
                            type            =   "Voltages_FFT"                                                      ,
                            auto_open       =   open
                            )

        if dp.JSON['TF_Config'] :
            # loop through each CSV file, generate plots, and append to HTML report
            for x  in range(len(file_list)):

                FFT_figs                =   self.fft_bar_plot(FFT_curr_path,FFT_volt_path,x)
                figures_list            =   self.plot_scopes(file_list[x],dp.pmap_plt,Legend=legend)
                figures_list_           =   self.interleaved(figures_list,FFT_figs)

                # drop extra columns from the CSV file if DCDC_S or DCDC_D
                # and generate control figures and extend to the main figure list
                if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':
                    simutil.postProcessing.drop_Extra_Cols(file_list[x],sum(dp.Y_list[0:3]),sum(dp.Y_list[0:4])) # drop uneeded columns from the csv file.
                    figures_list_ctrl   =   self.plot_scopes(file_list[x],dp.pmap_plt_ctrl,Legend=True)
                    figures_list_.extend(figures_list_ctrl)

                # increment counter and append plots to HTML report
                # clear lists for next iteration
                c+=1

                self.append_to_html(file_list[x] , figures_list_,fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_" + str(c) + ".html", auto_open=open , i=c-1)
                self.constants_list,self.constants_vals,self.constants_units,figures_list_  = [],[],[],[]

        # generate standalone time series and iteration  html reports
        if standalone_csv_files:
            for x  in range(len(standalone_csv_files)):
                std_figures_list                =   self.plot_std(standalone_csv_files[x])
                d+=1
                self.append_to_html(standalone_csv_files[x] , std_figures_list,fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_Standalone_" + str(d) + ".html", auto_open=open , i=d-1 ,standalone=True)

                if iterReport:
                    # Standalone iteration report
                    self.iter_reports(
                                'standalone'                                                                            ,
                                csv_files       =   standalone_csv_files                                                ,
                                html_path       =   fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc ,
                                auto_open       =   open
                                )

        # Generate 2D or 3D html report for signals and FFT
        if iterReport:
            if dp.JSON['TF_Config'] : self.graph_scopes(fileLog,simutil)
            if dp.standalone_exist : self.graph_scopes(fileLog,simutil,standalone_exist=True)

        # log the completion of HTML report generation and clear file list
        fileLog.line_separator()
        fileLog.log('{} = {}'.format("Generating HTML Report".ljust(fileLog.PADDING_WIDTH  , ' '),f"{str(misc.toc())} seconds.\n"))
        file_list.clear()
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            
            # Create dropdown figures
            list_of_plots = [self._make_dropdown(full_title, component, dropdown_data[component], plot_type="3D") 
                            for component in headers_array if dropdown_data.get(component)]
            
            if dp.JSON['FFT'] and fft_dropdown_data:
                fft_plots = [self._make_dropdown(full_title, component, fft_dropdown_data[component], plot_type="FFT") 
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
    all_combos = (list(dp.product(*sweep_vars.values())) if dp.JSON["permute"] 
                  else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, 
                                   [v[-1] for v in sweep_vars.values()], arr).tolist())
    
    # For FFT combinations
    if dp.JSON['FFT']:
        fft_combos = list(map(tuple, dp.np.repeat(all_combos, len(dp.harmonics), axis=0).astype(object)))
    else:
        fft_combos = None
    
    return plot_2D, single_X_key, all_combos, fft_combos

def _create_2D_plots(self, headers_array, FFT_headers, combined_matrix, combined_fft_matrix, 
                      sweep_vars, sweep_keys, sweepNames, all_combos, standalone_exist):
    """Create 2D plots (line plots and bar charts)."""
    list_of_plots, fft_plots = [], []
    relative_tol, absolute_tol = 0.001, 1e-12
    
    # Determine active sweep keys
    active_sweep_keys = [k for k, v in sweep_vars.items() if v != [0] and len(v) > 1]
    single_X_key = active_sweep_keys[0]
    sweep_values = sweep_vars[single_X_key]
    sweep_label = sweepNames[int(dp.re.search(r'\d+', single_X_key).group())-1]
    
    fixed_vars = {k: v for k, v in sweep_vars.items() if k != single_X_key and v != [0]}
    fixed_combos = list(dp.product(*fixed_vars.values())) if fixed_vars else [()]
    
    # Normal signals
    for component in headers_array:
        for fixed_values in fixed_combos:
            fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
            z_column = headers_array.index(component)
            z_vals = combined_matrix[:len(sweep_values), z_column]
            
            # Handle constant values
            if dp.JSON["perturbation"] == 0:
                if dp.np.allclose(z_vals, z_vals[0], rtol=relative_tol, atol=absolute_tol):
                    x_plot = dp.np.array([sweep_values[0], sweep_values[-1]])
                    z_plot = dp.np.array([z_vals[0], z_vals[-1]])
                else:
                    x_plot = sweep_values
                    z_plot = z_vals
            else:
                x_plot = sweep_values
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
    if dp.JSON['FFT'] and combined_fft_matrix is not None:
        for component in FFT_headers:
            for fixed_values in fixed_combos:
                fixed_dict = dict(zip(fixed_vars.keys(), fixed_values))
                z_column = FFT_headers.index(component)
                z_vals = combined_fft_matrix[:len(sweep_values), z_column]
                x_vals = dp.np.array(dp.harmonics)
                x_plot = dp.np.tile(x_vals, int(dp.np.ceil(len(sweep_values)/len(x_vals))))[:len(sweep_values)]
                
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
    fixed_combos = (list(dp.product(*other_vars.values())) if dp.JSON["permute"] 
                    else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*other_vars.values(), fillvalue=None)), dtype=object)) == None, 
                                     [v[-1] for v in other_vars.values()], arr).tolist())
    
    # Return the Selected Rows of data for each fixed combo
    rows_dict, fft_rows_dict = {}, {}
    all_combos = (list(dp.product(*sweep_vars.values())) if dp.JSON["permute"] 
                  else dp.np.where((arr := dp.np.array(list(dp.zip_longest(*sweep_vars.values(), fillvalue=None)), dtype=object)) == None, 
                                   [v[-1] for v in sweep_vars.values()], arr).tolist())
    
    for fixed_values in fixed_combos:
        fixed_dict = dict(zip(fixed_keys, fixed_values))
        rows = dp.np.array([(i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)]) 
                           for i, combo in enumerate(all_combos) 
                           if all(combo[sweep_keys.index(k)] == v for k, v in fixed_dict.items())])
        rows_dict[tuple(fixed_values)] = rows
        
        if dp.JSON['FFT']:
            fft_combos = list(map(tuple, dp.np.repeat(all_combos, len(dp.harmonics), axis=0).astype(object)))
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

def _make_dropdown(self, full_title, component, fixed_combos_data, plot_type="3D"):
    """
    Create a Plotly figure with multiple traces and a dropdown menu.
    
    Parameters:
        full_title: str - The overall title for the figure
        component: str - Name of the component being plotted
        fixed_combos_data: dict - Dictionary of fixed combinations data
        plot_type: str - "3D" for surface plots, "FFT" for bar charts
    """
    fig, dropdown_buttons, sweepNames = dp.go.Figure(), [], dp.JSON["sweepNames"]
    group_trace_indices, current_index = [], 0
    
    for i, (_, data) in enumerate(fixed_combos_data.items()):
        x_vals, y_vals, z_vals, fixed_dict = data
        
        if plot_type == "FFT":
            temp_fig = self.barchart3D(x_vals, y_vals, z_vals, full_title, 'Magnitude',
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
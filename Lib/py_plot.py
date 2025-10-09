
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
    """
    This Class is used for creating a full html report using tables , plots ...
    Functions / methods included in this calss :

    """
    def __init__(self,ResultsPath='',utc='',standalone =False):
        """
        Initialize the HTML_REPORT class with various attributes and load configuration data from a JSON file.
        
        """

        self.ResultsPath                =   ResultsPath                                                                                                     # Path to store results
        self.utc                        =   utc                                                                                                             # UTC timestamp string 
        self.hostname                   =   str(dp.socket.gethostname())                                                                                    # Host machine name
        self.script_name                =   dp.scriptname                                                                                                   # Current script name
        self.values_dict                =   dict()                                                                                                          # Dictionary to store values
        self.config_dicts               =   dict()                                                                                                          # Dictionary to store configuration data
        self.configkey_list             =   []                                                                                                              # List of configuration keys
        self.configval_list             =   []                                                                                                              # List of configuration values
        self.valkey_list                =   []                                                                                                              # List of value keys
        self.values_list                =   []                                                                                                              # List of values 
        self.headerColor                =   '#009ADA'                                                                                                     # Hex color for header
        self.even_rc                    =   '#E0E0E0'                                                                                                     # Row color for even rows
        self.odd_rc                     =   'white'                                                                                                         # Row color for odd rows
        self.title                      =   f"<html><head><title>{self.script_name}_Report_{self.utc}_{self.hostname}</title></head><body></body></html>"   # HTML page title template
        self.separator                  =   "<html><body><hr style='height:1px;border:none;color:#333;background-color:#333;'></body></html>"               # HTML horizontal separator
        self.image                      =   ''                                                                                                              # Placeholder for image data
        self.tab_val_list               =   []                                                                                                              # List for table values
        self.tab_conf_list              =   []                                                                                                              # List for table configurations
        self.iter_param_key             =   []                                                                                                              # List of iteration parameter keys
        self.iter_param_val             =   []                                                                                                              # List of iteration parameter values
        self.iter_param_unt             =   []                                                                                                              # List of iteration parameter units
        self.note                       =   "N/A"                                                                                                           # Note field with default "N/A"
        self.constants_list             =   []                                                                                                              # List of constant names
        self.constants_vals             =   []                                                                                                              # List of constant values
        self.constants_units            =   []                                                                                                              # List of constant units
        self.json_file                  =   "Standalone_variables.json" if standalone else "Input_vars.json"                                                # Select JSON file based on standalone mode
        self.json_path                  =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", self.json_file).replace("\\", "/")                          # Path to JSON file
        with open(self.json_path) as f  :   self.data = dp.json.load(f)                                                                                     # Load JSON data into self.data
        for i in range(1, 11)           :   setattr(self, f"X{i}", eval(self.data[f"X{i}"]))                                                                # Dynamically set X1–X10 attributes
        self.base64_img()                                                                                                                                   # Load base64 image data

    def base64_img(self):
        """
            Read a text file containing a base64 encoded image and store it as a string in the `image` attribute of the object.

            The function reads the contents of a specified text file, assumed to contain a base64 encoded image. It reads the file line
            by line, converts each line to a string, and concatenates the resulting strings to form a single string containing the
            entire encoded image. The resulting string is stored in the `image` attribute of the object.

            Parameters:
            -----------
            None

            Returns:
            --------
            None
        """

        # Read base64 image from text file and store in self.image
        with open(dp.BMW_Base64_Logo,'r') as fin: lines = fin.readlines()

        # loop through lines and concatenate to self.image
        for line in lines: self.image+=line
        
        # Close the file
        fin.close()

    def set_tab_dict(self,misc,input_dict):
        """
            Extract relevant configuration information from a dictionary of nested dictionaries, and store in lists.

            The function takes a dictionary of nested dictionaries as input, and extracts the relevant configuration information
            by iterating over the dictionary and checking for the presence of certain keys. The relevant sub-dictionaries are
            stored in a hard-coded configuration dictionary, and the values for each configuration are stored in a separate
            dictionary. The resulting dictionaries are stored in lists.

            Parameters:
            -----------
            misc : miscellaneous
                An instance of the `miscellaneous` class, containing various utility functions.

            input_dict : dict
                A dictionary of nested dictionaries, containing various configuration information.

            Returns: None
        """

        # Deep copy the input dictionary to avoid modifying the original
        # Extract relevant configuration information from the input dictionary
        # and store in lists for later use

        source_mdlvar			=	dp.copy.deepcopy(input_dict)
        self.config_dicts		= 	{ 'ToFile'			:	source_mdlvar['Common']['ToFile']}
        self.values_dict 		= 	misc.keys_exists(self.config_dicts,source_mdlvar)
        self.tab_val_list.append(self.values_dict)
        self.tab_conf_list.append(self.config_dicts)

    def table_data(self, dictt, key_list, val_list, prefix=''):
        """
        Extract data from a nested dictionary and store in two separate lists.

        The function takes a nested dictionary as input, and recursively extracts the keys and values from the dictionary.
        The keys are stored in a list, with a prefix string to indicate the nested structure of the key. The values are
        stored in a separate list, converted to a string format.

        Parameters:
        -----------
        dictt : dict
            The nested dictionary from which to extract data.

        key_list : list
            The list to store the extracted keys.

        val_list : list
            The list to store the extracted values.

        prefix : str, optional
            A prefix string to add to the keys to indicate the nested structure of the key. Defaults to an empty string.

        Returns: None
        """
        # Recursively extract keys and values from nested dictionary
        if isinstance(dictt, dict):
            for k, v2 in dictt.items():
                p2 = "{}['{}']".format(prefix, k)
                self.table_data(v2, key_list,val_list,p2)

        # append key and value to respective lists
        else:
            key_list.append(prefix)
            val_list.append(str(dictt))

    def add_constant_table(self,csv_file):
        """
        Reads in a CSV file containing data and creates a table of constants by taking the mean values of certain columns.
        The columns to use are defined in a constant dictionaries list. The resulting table is displayed using Plotly,
        a Python visualization library, and returned.

        Parameters:
        csv_file (str): The path to a CSV file containing the data to use for calculating the constants.

        Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object representing the constant table.
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
        
        # get number of rows for table
        const_Nrow              =   len(self.constants_vals)

        # Create a Plotly table to display the constants
        # Use alternating row colors for better readability and set header color
        # set table layout and title

        constants_tab           =   dp.go.Table(    header  =   dict(
                                                                values      =   ['PARAMETER','VALUE','UNIT']                                      ,
                                                                fill_color  =   self.headerColor                                                  ,
                                                                font_size   =   12                                                                ,
                                                                line_color  =   'darkslategray'                                                   ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(
                                                                values      =   [self.constants_list,self.constants_vals,self.constants_units]    ,
                                                                fill_color  =   [[self.odd_rc,self.even_rc]*const_Nrow]                           ,
                                                                align       =   ['left', 'center']                                                ,
                                                                font_size   =   10                                                                ,
                                                                line_color  =   'darkslategray'
                                                            )
                                        )

        # Create a subplot to hold the table 
        # set layout and title for the subplot 
        # row and column specifications for the subplot
        # shared x-axes and horizontal spacing

        table_figure            =   dp.make_subplots(
                                                    rows                    =   1                                                                 ,
                                                    cols                    =   1                                                                 ,
                                                    shared_xaxes            =   True                                                              ,
                                                    horizontal_spacing      =   0.03                                                              ,
                                                    specs                   =   [[{"type": "table"}]]
                                        )

        # Update layout and add the table trace to the subplot
        table_figure.update_layout( title_text="Operational Steady-State Parameters:",font_size=16)
        table_figure.add_trace(constants_tab,row=1, col=1)

        return table_figure

    def add_table(self,i=0):
        """
        Constructs two tables out of given data from two dictionaries one for configuratdions
        the other for values.

        Returns:
            object : plotly graph object.
        """
        # Clear Configuration and Values lists
        self.configkey_list.clear()
        self.configval_list.clear()

        # Clear Values keys and Values lists
        self.valkey_list.clear()
        self.values_list.clear()

        # Populate Configuration and Values lists using the table_data method
        self.table_data(self.tab_conf_list[i],self.configkey_list,self.configval_list)
        self.table_data(self.tab_val_list[i],self.valkey_list,self.values_list)
        
        # Set table height and number of rows for each table
        table_height            =   600
        config_Nrow             =   len(self.configval_list)
        val_Nrow                =   len(self.values_list)
        param_Nrow              =   len(self.iter_param_val[i])

        #* subsystems configuration table------------------------------------
        # Create a Plotly table to display the subsystem configurations
        # Use alternating row colors for better readability and set header color
        # set table layout and title and values for header and cells

        config_table            =   dp.go.Table(    header  =   dict(
                                                                values      =   ['SUBSYSTEM', 'CONFIGURATION']                       ,
                                                                fill_color  =   self.headerColor                                     ,
                                                                font_size   =   12                                                   ,
                                                                line_color  =   'darkslategray'                                      ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(
                                                                values      =   [self.configkey_list, self.configval_list]           ,
                                                                fill_color  =   [[self.odd_rc,self.even_rc]*config_Nrow]             ,
                                                                align       =   ['left', 'center']                                   ,
                                                                font_size   =   10                                                   ,
                                                                line_color  =   'darkslategray'
                                                            )
                                        )
        #* parameters values table-------------------------------------------
        # Create a Plotly table to display the parameter values
        # Use alternating row colors for better readability and set header color
        # set table layout and title and values for header and cells

        val_table               =   dp.go.Table(    header  =   dict(
                                                                values      =   ['ALL PARAMETERS', 'VALUE']                         ,
                                                                fill_color  =   self.headerColor                                    ,
                                                                font_size   =   12                                                  ,
                                                                line_color  =   'darkslategray'                                     ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(
                                                                values      =   [self.valkey_list, self.values_list]                 ,
                                                                fill_color  =   [[self.odd_rc,self.even_rc]*val_Nrow]                ,
                                                                align       =   ['left', 'center']                                   ,
                                                                font_size   =   10                                                   ,
                                                                line_color  =   'darkslategray'
                                                            )
                                        )
        #* Focused parameters values table-------------------------------------
        # Create a Plotly table to display the focused parameters
        # Use alternating row colors for better readability and set header color
        # set table layout and title and values for header and cells

        updated_vals_table       =   dp.go.Table(    header  =   dict(
                                                                values      =   ['FOCUSED PARAMETERS', 'VALUE', 'UNIT']                      ,
                                                                fill_color  =   self.headerColor                                     ,
                                                                font_size   =   12                                                   ,
                                                                line_color  =   'darkslategray'                                      ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(   values      =  [self.iter_param_key[i], self.iter_param_val[i], self.iter_param_unt[i]],
                                                                fill_color  =   [[self.odd_rc,self.even_rc]*param_Nrow]              ,
                                                                align       =   ['left', 'center']                                   ,
                                                                font_size   =   10                                                   ,
                                                                line_color  =   'darkslategray'
                                                            )
                                        )

        #* simulation notes table-------------------------------------------
        # Create a Plotly table to display the simulation notes
        # set table layout and title and values for header and cells

        readme_message           =   dp.go.Table(    header  =   dict(   values      =   ['SIMULATION NOTES']                        ,
                                                                fill_color  =   self.headerColor                                     ,
                                                                font_size   =   12                                                   ,
                                                                line_color  =   'darkslategray'                                      ,
                                                                align       =   'center'
                                                            ),

                                                    cells   =   dict(   values      =   [self.note]                                  ,
                                                                align       =   ['left']                                             ,
                                                                font_size   =   12                                                   ,
                                                                line_color  =   'darkslategray'                                      ,
                                                            )
                                        )

        #* subplot for all tables-------------------------------------------
        # Create a subplot to hold all the tables
        # set layout and title for the subplot
        # row and column specifications for the subplot
        # shared x-axes and horizontal spacing

        table_figure            =   dp.make_subplots(
                                                    rows                            =   2                                            ,
                                                    cols                            =   2                                            ,
                                                    shared_xaxes                    =   True                                         ,
                                                    horizontal_spacing              =   0.03                                         ,
                                                    specs                           =   [[{"type": "table"}, {"type": "table"}],[{"type": "table"}, {"type": "table"}]]
                                        )

        # Update layout and add the table traces to the subplot
        # Add traces for each table to the appropriate subplot cell

        table_figure.update_layout(height=table_height, title_text="Simulation Model Configurations & Parameters:",font_size=16)
        table_figure.add_trace(config_table,row=1, col=1)
        table_figure.add_trace(val_table,row=1, col=2)
        table_figure.add_trace(readme_message,row=2, col=1)
        table_figure.add_trace(updated_vals_table,row=2, col=2)

        # return the complete table figure
        return table_figure
    
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
                fig.update_layout(hovermode="x unified")
                figure_list.append(fig)

        # Return the list of figures
        return figure_list

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

        # Initialize an empty figure and create figure with secondary y-axis
        fig = dp.make_subplots(specs=[[{"secondary_y": True}]])
        
        # Create and add Traces for th Current Plots.
        for each in Current_keys:
            fig.add_trace(
                dp.go.Scatter(
                    x       = dff.iloc[:,0]                                 ,
                    y       = dff.iloc[:,Currents_labels_dict.get(each)]    ,
                    name    = each                                          ,
                    mode    = "lines"                                       ,
                    line    = dict(shape = 'linear', dash = 'dot')
                ),secondary_y=False
            )

        # Create and add Traces for th Voltage Plots.
        for each in voltage_keys:
            fig.add_trace(
                dp.go.Scatter(
                    x       = dff.iloc[:,0]                                 ,
                    y       = dff.iloc[:,Voltages_labels_dict.get(each)]    ,
                    name    = each                                          ,
                    mode    = "lines"                                       ,
                    line    = dict(shape = 'linear')
                ),secondary_y=True
            )

        # Create and add Traces for th PWM Plots.
        for each in PWM_keys:
            fig.add_trace(
                dp.go.Scatter(
                    x       = dff.iloc[:,0]                                 ,
                    y       = dff.iloc[:,PWM_labels_dict.get(each)]         ,
                    name    = each                                          ,
                    mode    = "lines+markers"                               ,
                    line    = dict(shape = 'linear', dash = 'dashdot')
                ),secondary_y=True
            )

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
        
        # Initialize and Define layout arguments for overall plots.
        # Set titles, axis labels, colors, and background color.
        # Add the update menu with buttons to the layout.
        # Set the initial visibility of all traces to True.
        # Set the initial title of the plot.

        fig.update_layout(
            updatemenus     =   [dp.go.layout.Updatemenu(
                                    active  = 0                                     ,
                                    buttons = [button_all,button_curr,button_volt,button_pwm,button_pwm_volt,button_pwm_curr]  ,
                                    direction = 'up'                                ,
                                    x       = 0                                     ,
                                    xanchor = 'left'                                ,
                                    y       = -0.1                                  ,
                                    yanchor = 'top'  )
                                ],
            title           =   "VOLTAGES VS CURRENTS VS PWM"                                               ,
            xaxis           =   dict(title='Time [ s ]')                            ,
            yaxis           =   dict(
                                    side        = "left"                            ,
                                    title       = "Current [ A ]"                   ,
                                    titlefont   = dict(color="#1f77b4")             ,
                                    tickfont    = dict(color="#1f77b4")
                                ),
            yaxis2          =   dict(
                                    side="right"                                    ,
                                    title="Voltage [ V ]"                           ,
                                    titlefont=dict(color="#1f77b4")                 ,
                                    tickfont=dict(color="#1f77b4")                  ,
                                ),
            plot_bgcolor    =   '#f8fafd'
            )

        # return the complete figure
        return fig

    def gen_iter_report(self,path,label_dict,html_path,Y_axis_label,type,auto_open):
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

        # Initialize variables and read CSV files from the specified directory
        fig_list          =   []
        include_plotlyjs  =   'cdn'
        labels_dict       =   dict(label_dict)
        dict_keys         =   list(labels_dict.keys())
        csv_files         =   [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]

        # Load one or more CSV files, sorts them, and converts them into DataFrames.  
        # For each key in dict_keys, a Plotly subplot is created and populated with line plots  
        # of the corresponding data column vs. time from each CSV, labeled by iteration.  
        # The layout is customized (titles, axes, legend, background), and figures are stored in fig_list.     
        #      
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
                        yaxis           =   dict(
                                                side        = "left"                ,
                                                title       = Y_axis_label          ,
                                                titlefont   = dict(color="#1f77b4") ,
                                                tickfont    = dict(color="#1f77b4")
                                            ),
                        plot_bgcolor    =   '#f8fafd'
                    )
                    C+=1
                fig_list.append(fig)

                # If 'iterSplit' is enabled in the JSON settings, a separate HTML report is generated for each key.  
                # The report includes a styled header with simulation metadata (script name, date/time, ID) and a  
                # base64-encoded image. Plotly figures are then embedded into the HTML, surrounded by separators,  
                # and the complete content is saved as a standalone HTML file.  

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

            # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.  
            # The header section includes metadata (script name, date/time, simulation ID) and a base64 image.  
            # All Plotly figures stored in fig_list are sequentially embedded into the HTML, separated by dividers,  
            # and the final report is saved as one combined HTML file.  
            
            if not dp.JSON['iterSplit']:
                date = str(dp.datetime.datetime.now().replace(microsecond=0))
                with open(html_path + "_" + type + ".html", 'w') as f:
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
            
            # If auto_open is enabled, the generated HTML report is automatically opened in the default web browser.  
            # The file path is first converted to an absolute URI, then passed to the webbrowser module for launching.  
            
            if auto_open:
                import pathlib, webbrowser
                uri = pathlib.Path(html_path).absolute().as_uri()
                webbrowser.open(uri)

    def return_headers(self,header_file):
        """
       Returns list of headers from json header file.

       Parameters  :
                      header_file   :       String
                                            Path to the json header file.
        Returns    :  header        :       list
                                            List of headers .
        """
        
        # Open the header_file in read mode and load its contents as JSON into the variable 'header'.  
        # After reading, the file is closed and the parsed header data is returned. 

        with open(header_file, 'r') as f: header = dp.json.load(f)
        f.close()
        return header

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
                                                         List of plotly figures. .
        """
        
        # Load current and voltage FFT headers from JSON files using the return_headers method.  
        # Read current and voltage FFT CSV data into pandas DataFrames without headers or index columns.  
        # Initialize an empty list to store generated Plotly figures.  

        Current_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Current.json")
        Voltage_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Voltage.json")
        dfcurr                        = dp.pd.read_csv(current_fft_csv, header=None,index_col=None)
        dfvolt                        = dp.pd.read_csv(voltage_fft_csv, header=None,index_col=None)
        figure_list                   = []
        
        # Loop through each entry in dp.plt_title_list to create subplots.
        for i in range(len(dp.plt_title_list)):
            
            # Create a Plotly subplot with a secondary y-axis for combined current and voltage plotting.  
            
            fig                   = dp.make_subplots(rows=1, cols=1,specs=[[{"secondary_y": True}]])
            
            # Determine the indices of current columns to plot from Current_headers based on plt_title_list structure.  
            # Determine the indices of voltage columns to plot from Voltage_headers based on plt_title_list structure.  

            current_idx_list      = [Current_headers.index(dp.plt_title_list[i][1])] if len(dp.plt_title_list[i])<5 else [ Current_headers.index(dp.plt_title_list[i][1]) , Current_headers.index(dp.plt_title_list[i][2])  ]
            voltage_idx_list      = [Voltage_headers.index(dp.plt_title_list[i][2])] if len(dp.plt_title_list[i])<5 else [ Voltage_headers.index(dp.plt_title_list[i][3]) , Voltage_headers.index(dp.plt_title_list[i][4])  ]

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
                                                        titlefont   = dict(color="#1f77b4")                   ,
                                                        tickfont    = dict(color="#1f77b4"))                  ,
                                yaxis2          =   dict(
                                                        side        = "right"                                   ,
                                                        title       = "Voltage Magnitude"                       ,
                                                        titlefont   = dict(color="#1f77b4")                   ,
                                                        tickfont    = dict(color="#1f77b4"))                  ,
                                plot_bgcolor    =   '#f8fafd'                                                 ,
                                barmode         =   'overlay'
                            )
            figure_list.append(fig)

        return figure_list

    def shuffle_lists(self, list1, list2):
        """
        Shuffle two lists by interleaving their elements.

        Args:
            list1 (list): First list to be shuffled.
            list2 (list): Second list to be shuffled.

        Returns:
            list        : Shuffled list containing interleaved elements from list1 and list2.

        """

        # Interleave elements from list1 and list2 into a new list, list3.  
        # For each index, append the element from list1, then append the corresponding element from list2 if it exists.  
        # Return the combined interleaved list.  

        list3 = []
        for i in range(len(list1)):
            list3.append(list1[i])
            if list2:
                list3.append(list2[i])
        return list3

    def fft_gen_iter_report(self, FFT_file,title, csv_path, html_path, type ,auto_open):
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
        # Set Plotly to load JavaScript from the CDN.  
        # Load FFT headers from the specified JSON file using return_headers.  
        # Read the FFT CSV data into a pandas DataFrame without headers or index columns.  
        # Initialize an empty list to store generated Plotly figures.  
        # Calculate the number of iterations based on the total number of rows and the number of harmonics. 

        include_plotlyjs          = 'cdn'
        headers                   = self.return_headers( (dp.os.getcwd()).replace("\\","/") + f"/Script/assets/HEADER_FILES/{FFT_file}")
        df                        = dp.pd.read_csv(csv_path, header=None,index_col=None)
        figure_list               = []
        num_iterations            = df.shape[0] // len(dp.harmonics)

        # Loop through each column in the DataFrame to create bar plots of FFT magnitudes.  
        # Initialize a new Plotly figure for the current column.  
        # Add a bar trace for each iteration, slicing the data according to harmonics.  
        # Update the figure layout with titles, axis labels, tick settings, and stacked bar mode.  
        # Append the configured figure to the figure_list.  

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
            # The report includes metadata (script name, date/time, simulation ID) and a base64 image.  
            # The Plotly figure for the current column is embedded, surrounded by HTML separators,  
            # and the file is saved with a unique name per column.  
            
            if dp.JSON['iterSplit']:
                date = str(dp.datetime.datetime.now().replace(microsecond=0))
                with open(html_path + "_" + str(headers[column]) + "_FFT.html", 'w') as f:
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

        # If 'iterSplit' is disabled, generate a single consolidated HTML report for all FFT figures.  
        # The report header includes metadata (script name, date/time, simulation ID) and a base64 image.  
        # All figures in figure_list are embedded sequentially with HTML separators,  
        # and the report is saved as one combined HTML file. 

        if not dp.JSON['iterSplit']:
            date = str(dp.datetime.datetime.now().replace(microsecond=0))
            with open(html_path + "_" + type + "_FFT.html", 'w') as f:
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
                for fig_i in figure_list:
                    f.write(fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                    f.write(self.separator)
            f.close()

        # If auto_open is True, automatically open the generated HTML report in the default web browser.  
        # The file path is converted to an absolute URI and passed to the webbrowser module for opening.  
     
        if auto_open:
            import pathlib, webbrowser
            uri = pathlib.Path(html_path).absolute().as_uri()
            webbrowser.open(uri)

    def append_to_html(self,csv_filename,figure, filename,auto_open, i=1,include_plotlyjs='cdn'):
        """
        Appends figures to an existing html file.

        Args:
            figure (object)                     : plotly lib graph objects class object.
            filename (string)                   : path of the html file.
            include_plotlyjs (str, optional)    : Defaults to 'cdn'. check tohtml  : https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.to_html
            auto_open (bool, optional)          : Determines whether the file should open automatically. Defaults to False.
       
         """
        
        #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output 
        #* that references the Plotly CDN ("content delivery network").
        #* This offloads the work of providing the necessary javascript from your server to a more 
        #* scalable one. A browser will typically cache this making subsequent page loads faster.
        
        # generate the multiplot and tables
        # set date and time for the report

        multiplot       = self.multiplot(csv_filename)
        tables          = self.add_table(i)
        date            = str(dp.datetime.datetime.now().replace(microsecond=0))
       
        # If both figureName and figureComment flags are enabled in the JSON settings, prepare figure metadata.  
        # Extract the main figure names from plt_title_list.  
        # Create corresponding FFT figure names by prefixing 'FFT ' to each main figure name.  
        # Extract control figure names from the keys of pmap_plt_ctrl.  
        # Combine and shuffle the main and FFT figure names, then append control figure names.  
        # Initialize a list of empty comments corresponding to all figures.  

        if dp.JSON["figureName"] and dp.JSON["figureComment"]:
            
            self.FigureNames                =   [dp.plt_title_list[i][0] for i in range(len(dp.plt_title_list))]
            self.fftFigureNames             =   [f'FFT {dp.plt_title_list[i][0]}' for i in range(len(dp.plt_title_list))]
            self.CtrlFigureNames            =   list(dp.pmap_plt_ctrl.keys())
            self.FigTitles                  =   (self.shuffle_lists(self.FigureNames, self.fftFigureNames)) + self.CtrlFigureNames
            self.Comments                   =   [" " for _ in range((2*len(dp.plt_title_list))+ len(self.CtrlFigureNames))]

        # Open the specified filename for writing and generate an HTML report.  
        # The report header includes metadata (script name, date/time, simulation ID) and a base64 image.  
        # The main tables and multiplot figures are embedded using their HTML representations,  
        # separated by horizontal dividers, and Plotly JS inclusion is controlled via include_plotlyjs.  
        
        with open(filename, 'w') as f:
            f.write(self.title)
            f.write('<style>    .container  {position: relative;text-align: right;color: black;}                                        \
                                .Simulation {position: absolute;top: 10px;left: 16px;}                                                  \
                                .DateTime   {position: absolute;top: 50px;left: 16px;}                                                  \
                                .Sim_ID     {position: absolute;top: 90px;left: 16px;}                                                  \
                    </style>'                                                                                                           \
                    f'<div class="container">                                                                                           \
                                <img src="data:image/png;base64,{self.image}"/>                                                         \
                                <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>     \
                                <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div>                \
                                <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div>             \
                    </div>')

            f.write(self.separator)
            f.write(tables.to_html(include_plotlyjs=include_plotlyjs))
            f.write(self.separator)
            f.write(multiplot.to_html(include_plotlyjs=include_plotlyjs))
            f.write(self.separator)
            
            # If figure names and comments are provided in JSON, update self.Comments to match the figure titles.  
            # Loop through all figures and write their HTML representation to the file.  
            # If a comment exists for this figure, add it as a read-only HTML input field below the figure.  
            # Add a horizontal separator after each figure (and its comment, if present).  

            if dp.JSON["figureName"] and dp.JSON["figureComment"]:

                for b in range(len(dp.JSON["figureName"])):
                    self.Comments[self.FigTitles.index(dp.JSON["figureName"][b])] =  dp.JSON["figureComment"][b]

            for i in range(len(figure)):

                f.write(figure[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                if dp.JSON["figureName"] and dp.JSON["figureComment"]:

                    if not self.Comments[i] == " " :
                        f.write(f'<input type="text" style="font-size:9pt;height:50px;width:1500px;" value="{self.Comments[i]}" readonly="readonly">')

                f.write(self.separator)
            
            # Generate a table of constants from the CSV file and write its HTML representation to the report.  
            # Clear the stored constants lists to reset for the next use.  
            
            constant_tables = self.add_constant_table(csv_filename)
            f.write(constant_tables.to_html(include_plotlyjs=include_plotlyjs))
            self.constants_list.clear()
            self.constants_vals.clear()
            self.constants_units.clear()

            # If figure names and comments are used, clear all related lists to reset the state for future reports.  

            if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                self.FigTitles.clear()
                self.FigureNames.clear()
                self.fftFigureNames.clear()
                self.Comments.clear()

            # Write HTML for a simple web interface allowing the user to upload a header JSON file and raw data.  
            # Includes labeled file inputs, a container for dynamic checkboxes, and a disabled download button.  
            # The interface functionality is expected to be handled by the linked "app.js" script.  
            
            f.write('<html>                                                                     \
                        <body>                                                                  \
                            <div>                                                               \
                                <br />                                                          \
                                <label for="files" class="btn">SELECT HEADER FILE</label>       \
                                <br />                                                          \
                                <br />                                                          \
                                <input type="file" id="LoadJasonFile" onchange="uploadJson()"/> \
                                <br />                                                          \
                                <br />                                                          \
                                <label for="files" class="btn">SELECT RAW DATA</label>          \
                                <br />                                                          \
                                <br />                                                          \
                                <input type="file" id="fileInput" onchange="uploadFile()" />    \
                                <br />                                                          \
                            <div>                                                               \
                            <br />                                                              \
                            <div id="checkboxContainer"></div>                                  \
                                <br />                                                          \
                                <button id="downloadButton" disabled>Download</button>          \
                                <br />                                                          \
                        </body>                                                                 \
                        <script src="app.js"></script>                                          \
                    </html>')
        f.close()
        
        # If auto_open is True, automatically open the generated HTML file in the default web browser.  
        # Converts the file path to an absolute URI and opens it using the webbrowser module.  
       
        if auto_open:
            import pathlib, webbrowser
            uri = pathlib.Path(filename).absolute().as_uri()
            webbrowser.open(uri)

    def auto_plot(self,simutil,fileLog,misc,open=False,iterReport=False):
        """
        Generates an HTML report containing multiple plots.

        Args:
            misc (object)               : Miscellaneous object containing utility functions.
            Open (bool, optional)       : If True, open the generated HTML report automatically. Defaults to False.
            iterReport (bool, optional) : If True, generate iterations HTML report. Defaults to False.
        """
        # start the timer
        # define directories and file paths
        # get the list of CSV files in the results directory for time series data and MAPS
        # set FFT csv file paths and sort files 
        # initialize counter and legend flag based on configuration

        misc.tic()
        ResDir          =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"
        MAPS_dir        =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"
        FFT_curr_path   =   MAPS_dir+"/FFT_Current_Map.csv"
        FFT_volt_path   =   MAPS_dir+"/FFT_Voltage_Map.csv"
        file_list       =   fileLog.natsort_files(ResDir)
        legend          =   True if dp.JSON['TF_Config'] == 'DCDC_D' else False
        c               =   0

        # drop extra columns from the FFT csv files if DCDC_S or DCDC_D
        if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':
            simutil.postProcessing.drop_Extra_Cols(FFT_curr_path,dp.idx_start,dp.idx_end)

        # generate iteration reports if iterReport is True
        if iterReport:
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Currents'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ A ]" ,"Currents",open)
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Voltages'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ V ]" ,"Voltages",open)
       
        # generate FFT iteration reports if iterReport is True and FFT is enabled
        if iterReport and dp.JSON['FFT']:
            self.fft_gen_iter_report( "FFT_Current.json", " Currents_FFT" ,FFT_curr_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc  ,"Currents_FFT" ,open)
            self.fft_gen_iter_report( "FFT_Voltage.json", "Voltages_FFT" ,FFT_volt_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_"  + self.utc  ,"Voltages_FFT" ,open)

        # loop through each CSV file, generate plots, and append to HTML report
        for x  in range(len(file_list)):
        
            FFT_figs                =   self.fft_bar_plot(FFT_curr_path,FFT_volt_path,x)
            figures_list            =   self.plot_scopes(file_list[x],dp.pmap_plt,Legend=legend)
            figures_list_           =   self.shuffle_lists(figures_list,FFT_figs)
          
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
       
        # log the completion of HTML report generation and clear file list
        fileLog.Separator()
        fileLog.log(f"Generating HTML Report    {'= '.rjust(49+17, ' ')}{str(misc.toc())} seconds.\n")
        file_list.clear()

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------


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

class HTML_REPORT:
    """
    This Class is used for creating a full html report using tables , plots ...
    Functions / methods included in this calss :

    """
    def __init__(self,ResultsPath='',utc='',standalone =False):                                                                 # Class constructor with default parameters

        self.ResultsPath                =   ResultsPath                                                                     # Set ResultsPath instance variable
        self.utc                        =   utc                                                                             # Set UTC timestamp string
        self.hostname                   =   str(dp.socket.gethostname())                                                    # Get and store system hostname
        self.script_name                =   dp.scriptname                                                                   # Store script name (commented alternative method)
        self.values_dict                =   dict()                                                                           # Initialize empty values dictionary
        self.config_dicts               =   dict()                                                                          # Initialize empty config dictionaries
        self.configkey_list             =   []                                                                              # Initialize empty config keys list
        self.configval_list             =   []                                                                              # Initialize empty config values list
        self.valkey_list                =   []                                                                              # Initialize empty value keys list
        self.values_list                =   []                                                                              # Initialize empty values list
        self.headerColor                =   '#009ADA'                                                                       # Set header color (blue)
        self.even_rc                    =   '#E0E0E0'                                                                       # Set even row color (light gray)
        self.odd_rc                     =   'white'                                                                         # Set odd row color (white)
        self.title                      =   f"<html><head><title>{self.script_name}_Report_{self.utc}_{self.hostname}</title></head><body></body></html>"  # Create HTML title string
        self.separator                  =   "<html><body><hr style='height:1px;border:none;color:#333;background-color:#333;'></body></html>"            # Create HTML separator
        self.image                      =   ''                                                                             # Initialize empty image string
        self.tab_val_list               =   []                                                                              # Initialize empty tab values list
        self.tab_conf_list              =   []                                                                              # Initialize empty tab configs list
        self.iter_param_key             =   []                                                                              # Initialize empty param keys list
        self.iter_param_val             =   []                                                                              # Initialize empty param values list
        self.iter_param_unt             =   []                                                                              # Initialize empty param units list
        self.note                       =   "N/A"                                                                           # Set default note value
        self.constants_list             =   []                                                                              # Initialize empty constants list
        self.constants_vals             =   []                                                                              # Initialize empty constant values list
        self.constants_units            =   []                                                                              # Initialize empty constant units list
        self.standalone                 =   standalone                                                                      # Set standalone flag
        self.json_file                  =   "Standalone_variables.json" if standalone else "Input_vars.json"                # Set JSON filename based on mode
        self.json_path                  =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", self.json_file).replace("\\", "/")  # Build full JSON file path

        with open(self.json_path) as file:                                                                                  # Open JSON config file
            self.data = dp.json.load(file)                                                                                  # Load JSON data into instance

        self.X1, self.X2, self.X3, self.X4, self.X5, self.X6, self.X7, self.X8, self.X9, self.X10 = (                     # Unpack X1-X10 from JSON
            eval(self.data[f'X{i}']) for i in range(1, 11)                                                                 # Evaluate each X value
        )

        self.pattern                    =   self.data['permute']                                                            # Store permutation pattern
        self.dimension_names            =   self.data['Dimension_Names']                                                    # Store dimension names
        self.matrix                     =   [self.X1, self.X2, self.X3, self.X4, self.X5, self.X6, self.X7, self.X8, self.X9, self.X10]  # Create matrix of all X values
        self.startpoint                 =   [X[0] for X in self.matrix]                                                     # Create list of starting values
        self.separate_files             =   self.data['plotFiles']                                                          # Store plot files flag
        self.var1                       =   eval(self.data[self.data["Var1"]])                                               # Evaluate and store first variable
        self.variable_2                 =   self.data["Var2"]                                                              # Store second variable name
        self.base64_img()                                                                                                   # Call base64 image method

    def base64_img(self):                                                                                                      # Method to load base64 encoded image
            """                                                                                                                # Docstring begins
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
            """                                                                                                                 # Docstring ends
            with open(dp.BMW_Base64_Logo,'r') as fin:                                                                          # Open base64 image file in read mode
                lines = fin.readlines()                                                                                        # Read all lines from file
            for line in lines:                                                                                                 # Iterate through each line
                self.image+=line                                                                                                # Append line to image attribute
            fin.close()                                                                                                        # Close the file (redundant due to 'with' statement)

    def set_tab_dict(self,misc,input_dict):                                                                                    # Method to process and store configuration dictionaries
            """                                                                                                                # Docstring begins
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

                Returns:
                --------
                None
            """                                                                                                                 # Docstring ends
            source_mdlvar                   =       dp.copy.deepcopy(input_dict)                                                 # Create deep copy of input dictionary
            self.config_dicts               =       { # Hard coded !!                                                           # Create hard-coded configuration dictionary

                                                    'Probes'                  :       source_mdlvar['Common']['Probes']              ,  # Extract Probes configuration
                                                    'ToFile'                  :       source_mdlvar['Common']['ToFile']              ,  # Extract ToFile configuration
                                                    'PSFBconfigs'             :       source_mdlvar['Common']['PSFBconfigs']         ,  # Extract PSFBconfigs
                                                    'RboxConfigs'             :       source_mdlvar['Common']['RboxConfigs']           # Extract RboxConfigs

                                                    }
            self.values_dict                =       misc.keys_exists(self.config_dicts,source_mdlvar)                             # Validate keys using misc method
            self.tab_val_list.append(self.values_dict)                                                                          # Append values dictionary to list
            self.tab_conf_list.append(self.config_dicts)                                                                        # Append config dictionary to list

    def table_data(self, dictt, key_list, val_list, prefix=''):                                                                # Method to recursively extract data from nested dict
            """                                                                                                                # Docstring begins
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

            Returns:
            --------
            None
            """                                                                                                                 # Docstring ends
            if isinstance(dictt, dict):                                                                                         # Check if current item is a dictionary
                for k, v2 in dictt.items():                                                                                     # Iterate through dictionary items
                    p2 = "{}['{}']".format(prefix, k)                                                                           # Create nested key path string
                    self.table_data(v2, key_list,val_list,p2)                                                                   # Recursively process nested dictionary
            else:                                                                                                               # If current item is not a dictionary (base case)
                key_list.append(prefix)                                                                                         # Append the full key path to key_list
                val_list.append(str(dictt)) # self.val_list.append(repr(dictt)) #if you want full long value.                   # Append string representation of value to val_list

    def add_constant_table(self,csv_file):                                                                                     # Method to create table of constants from CSV data
            """                                                                                                                # Docstring begins
            Reads in a CSV file containing data and creates a table of constants by taking the mean values of certain columns.
            The columns to use are defined in a constant dictionaries list. The resulting table is displayed using Plotly,
            a Python visualization library, and returned.

            Parameters:
            csv_file (str): The path to a CSV file containing the data to use for calculating the constants.

            Returns:
            plotly.graph_objs._figure.Figure: A Plotly figure object representing the constant table.
            """                                                                                                                 # Docstring ends

            df                      =   dp.pd.read_csv(csv_file)                                                               # Read CSV file into pandas DataFrame
            for key , val in dp.constant_dict.items():                                                                         # Iterate through constant dictionary items
                column_values = df.iloc[:, val[1]]                                                                             # Get column values by index from dict
                column_values = column_values.to_numpy()                                                                      # Convert to numpy array
                column_values = column_values[-50:]                                                                           # Take last 50 values (steady-state)
                self.constants_list.append(val[0])                                                                             # Append parameter name to list
                self.constants_vals.append(dp.np.mean(column_values).round(2))                                               # Append mean value rounded to 2 decimals
                self.constants_units.append(val[2])                                                                            # Append unit to units list
            const_Nrow              =   len(self.constants_vals)                                                               # Get number of constants for row coloring

            constants_tab           =   dp.go.Table(    header  =   dict(                                                      # Create Plotly table object
                                                                    values      =   ['PARAMETER','VALUE','UNIT']                                      ,  # Column headers
                                                                    fill_color  =   self.headerColor                                                  ,  # Header color
                                                                    font_size   =   12                                                                ,  # Header font size
                                                                    line_color  =   'darkslategray'                                                   ,  # Border color
                                                                    align       =   'center'                                                           # Text alignment
                                                                ),

                                                        cells   =   dict(                                                      # Table cells configuration
                                                                    values      =   [self.constants_list,self.constants_vals,self.constants_units]    ,  # Cell values
                                                                    fill_color  =   [[self.odd_rc,self.even_rc]*const_Nrow]                           ,  # Alternating row colors
                                                                    align       =   ['left', 'center']                                                ,  # Column alignment
                                                                    font_size   =   10                                                                ,  # Cell font size
                                                                    line_color  =   'darkslategray'                                                    # Cell border color
                                                                )
                                            )

            table_figure            =   dp.make_subplots(                                                                      # Create Plotly subplot figure
                                                        rows                    =   1                                                                 ,  # Single row
                                                        cols                    =   1                                                                 ,  # Single column
                                                        shared_xaxes            =   True                                                              ,  # Shared x-axis
                                                        horizontal_spacing      =   0.03                                                              ,  # Horizontal spacing
                                                        specs                   =   [[{"type": "table"}]]                                              # Specify table type
                                            )

            table_figure.update_layout( title_text="Operational Steady-State Parameters:",font_size=16)                        # Update layout with title
            table_figure.add_trace(constants_tab,row=1, col=1)                                                               # Add table to figure

            return table_figure                                                                                                # Return the Plotly figure object

    def add_table(self,i=0):                                                                                                    # Method to create configuration and parameter tables
            """                                                                                                                # Docstring begins
            Constructs two tables out of given data from two dictionaries one for configuratdions
            the other for values.

            Returns:
                object : plotly graph object.
            """                                                                                                                 # Docstring ends
            table_height            =   600                                                                                     # Set fixed table height
            self.configkey_list.clear()                                                                                        # Clear config keys list
            self.configval_list.clear()                                                                                        # Clear config values list
            self.valkey_list.clear()                                                                                           # Clear parameter keys list
            self.values_list.clear()                                                                                           # Clear parameter values list
            self.table_data(self.tab_conf_list[i],self.configkey_list,self.configval_list)                                     # Extract config data
            self.table_data(self.tab_val_list[i],self.valkey_list,self.values_list)                                           # Extract parameter data
            config_Nrow             =   len(self.configval_list)                                                               # Get config row count
            val_Nrow                =   len(self.values_list)                                                                  # Get parameter row count
            param_Nrow              =   len(self.iter_param_val[i])                                                            # Get focused param row count

            #* subsystems configuration table------------------------------------
            config_table            =   dp.go.Table(    header  =   dict(                                                      # Create config table
                                                                    values      =   ['SUBSYSTEM', 'CONFIGURATION']                       ,  # Column headers
                                                                    fill_color  =   self.headerColor                                     ,  # Header color
                                                                    font_size   =   12                                                   ,  # Header font size
                                                                    line_color  =   'darkslategray'                                      ,  # Border color
                                                                    align       =   'center'                                              # Text alignment
                                                                ),

                                                        cells   =   dict(                                                      # Table cells config
                                                                    values      =   [self.configkey_list, self.configval_list]           ,  # Cell values
                                                                    fill_color  =   [[self.odd_rc,self.even_rc]*config_Nrow]             ,  # Alternating row colors
                                                                    align       =   ['left', 'center']                                   ,  # Column alignment
                                                                    font_size   =   10                                                   ,  # Cell font size
                                                                    line_color  =   'darkslategray'                                      # Cell border color
                                                                )
                                            )
            #* parameters values table-------------------------------------------
            val_table               =   dp.go.Table(    header  =   dict(                                                      # Create parameters table
                                                                    values      =   ['ALL PARAMETERS', 'VALUE']                         ,  # Column headers
                                                                    fill_color  =   self.headerColor                                    ,  # Header color
                                                                    font_size   =   12                                                  ,  # Header font size
                                                                    line_color  =   'darkslategray'                                     ,  # Border color
                                                                    align       =   'center'                                             # Text alignment
                                                                ),

                                                        cells   =   dict(                                                      # Table cells config
                                                                    values      =   [self.valkey_list, self.values_list]                 ,  # Cell values
                                                                    fill_color  =   [[self.odd_rc,self.even_rc]*val_Nrow]                ,  # Alternating row colors
                                                                    align       =   ['left', 'center']                                   ,  # Column alignment
                                                                    font_size   =   10                                                   ,  # Cell font size
                                                                    line_color  =   'darkslategray'                                      # Cell border color
                                                                )
                                            )
            #* parameters values table-------------------------------------------
            updated_vals_table       =   dp.go.Table(    header  =   dict(                                                     # Create focused params table
                                                                        values      =   ['FOCUSED PARAMETERS', 'VALUE', 'UNIT']                      ,  # Column headers
                                                                    fill_color  =   self.headerColor                                     ,  # Header color
                                                                    font_size   =   12                                                   ,  # Header font size
                                                                    line_color  =   'darkslategray'                                      ,  # Border color
                                                                    align       =   'center'                                              # Text alignment
                                                                ),

                                                        cells   =   dict(   values      =  [self.iter_param_key[i], self.iter_param_val[i], self.iter_param_unt[i]],  # Cell values
                                                                    fill_color  =   [[self.odd_rc,self.even_rc]*param_Nrow]              ,  # Alternating row colors
                                                                    align       =   ['left', 'center']                                   ,  # Column alignment
                                                                    font_size   =   10                                                   ,  # Cell font size
                                                                    line_color  =   'darkslategray'                                      # Cell border color
                                                                )
                                            )

            #* parameters values table-------------------------------------------
            readme_message           =   dp.go.Table(    header  =   dict(   values      =   ['SIMULATION NOTES']                        ,  # Single column header
                                                                    fill_color  =   self.headerColor                                     ,  # Header color
                                                                    font_size   =   12                                                   ,  # Header font size
                                                                    line_color  =   'darkslategray'                                      ,  # Border color
                                                                    align       =   'center'                                              # Text alignment
                                                                ),

                                                        cells   =   dict(   values      =   [self.note]                                  ,  # Note content
                                                                    align       =   ['left']                                             ,  # Left alignment
                                                                    font_size   =   12                                                   ,  # Font size
                                                                    line_color  =   'darkslategray'                                      # Border color
                                                                )
                                            )


            table_figure            =   dp.make_subplots(                                                                      # Create subplot figure
                                                        rows                            =   2                                            ,  # 2 rows
                                                        cols                            =   2                                            ,  # 2 columns
                                                        shared_xaxes                    =   True                                         ,  # Shared x-axis
                                                        horizontal_spacing              =   0.03                                         ,  # Horizontal spacing
                                                        specs                           =   [[{"type": "table"}, {"type": "table"}],[{"type": "table"}, {"type": "table"}]]  # Table specs
                                            )


            table_figure.update_layout(height=table_height, title_text="Simulation Model Configurations & Parameters:",font_size=16)  # Update layout
            table_figure.add_trace(config_table,row=1, col=1)                                                                 # Add config table
            table_figure.add_trace(val_table,row=1, col=2)                                                                     # Add parameters table
            table_figure.add_trace(readme_message,row=2, col=1)                                                               # Add notes table
            table_figure.add_trace(updated_vals_table,row=2, col=2)                                                           # Add focused params table

            return table_figure                                                                                                # Return the figure

    def multiplot(self,csv_file):                                                                                            # Method to create interactive multi-plot
            """Generate a plot of voltage and current data from a Plecs simulation output file.                              # Docstring begins

            Args:
                csv_file (str): The path to the CSV file containing the data.

            Returns:
                A plotly.graph_objs._figure.Figure object representing the plot.

            Raises:
                FileNotFoundError: If the specified CSV file does not exist.

            This function reads voltage and current data from a CSV file generated by a Plecs simulation.
            The data is assumed to be organized in columns, with the first column containing the time values.
            The function generates a plot with two y-axes, one for the current data and one for the voltage data.
            The plot includes a menu that allows the user to toggle the display of the current and voltage data.
            """                                                                                                             # Docstring ends
            #? Genarate dataframe from csv file.
            dff                     = dp.pd.read_csv(csv_file)                                                              # Read simulation data from CSV
            #? Retrieve data index dictionaries from plecs_mapping module.
            Voltages_labels_dict    = dp.pmap_multi['Peak_Voltages']                                                       # Get voltage mapping dictionary
            Currents_labels_dict    = dp.pmap_multi['Peak_Currents']                                                       # Get current mapping dictionary
            PWM_labels_dict         = dp.pwm_dict                                                                          # Get PWM mapping dictionary
            #? Get keys from previously defined dictionaries (to be used as labels)
            voltage_keys            = list(Voltages_labels_dict.keys())                                                     # Extract voltage signal names
            Current_keys            = list(Currents_labels_dict.keys())                                                     # Extract current signal names
            PWM_keys                = list(PWM_labels_dict.keys())                                                          # Extract PWM signal names
            #? Initialize an empty figure.
            # Create figure with secondary y-axis
            fig = dp.make_subplots(specs=[[{"secondary_y": True}]])                                                        # Create plot with dual y-axes
            #? Create and add Traces for th Current Plots.
            for each in Current_keys:                                                                                      # Loop through current signals
                fig.add_trace(                                                                                            # Add current trace
                    dp.go.Scatter(                                                                                        # Create scatter plot
                        x       = dff.iloc[:,0]                                 ,                                        # X-axis (time)
                        y       = dff.iloc[:,Currents_labels_dict.get(each)]    ,                                        # Y-axis (current values)
                        name    = each                                          ,                                        # Trace name
                        mode    = "lines"                                       ,                                        # Display mode
                        line    = dict(shape = 'linear', dash = 'dot')                                                   # Line style
                    ),secondary_y=False                                                                                   # Place on primary y-axis
                )
            #? Create and add Traces for th Voltage Plots.
            for each in voltage_keys:                                                                                     # Loop through voltage signals
                fig.add_trace(                                                                                            # Add voltage trace
                    dp.go.Scatter(                                                                                        # Create scatter plot
                        x       = dff.iloc[:,0]                                 ,                                        # X-axis (time)
                        y       = dff.iloc[:,Voltages_labels_dict.get(each)]    ,                                        # Y-axis (voltage values)
                        name    = each                                          ,                                        # Trace name
                        mode    = "lines"                                       ,                                        # Display mode
                        line    = dict(shape = 'linear')                                                                 # Line style
                    ),secondary_y=True                                                                                   # Place on secondary y-axis
                )
            #? Create and add Traces for th PWM Plots.
            for each in PWM_keys:                                                                                        # Loop through PWM signals
                fig.add_trace(                                                                                            # Add PWM trace
                    dp.go.Scatter(                                                                                        # Create scatter plot
                        x       = dff.iloc[:,0]                                 ,                                        # X-axis (time)
                        y       = dff.iloc[:,PWM_labels_dict.get(each)]         ,                                        # Y-axis (PWM values)
                        name    = each                                          ,                                        # Trace name
                        mode    = "lines+markers"                               ,                                        # Display mode
                        line    = dict(shape = 'linear', dash = 'dashdot')                                               # Line style
                    ),secondary_y=True                                                                                   # Place on secondary y-axis
                )
            #? Define button for showing all plots.
            button_all          = dict(                                                                                   # Button to show all traces
                                        label   = 'CURRENTS & VOLTAGES & PWM'                                             ,  # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \  # Currents visible
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))]+ \  # Voltages visible
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))],    # PWM visible
                                                    'title'     : 'CURRENTS & VOLTAGES & PWM'                             ,  # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Define button for showing Current plots.
            button_curr          = dict(                                                                                  # Button to show only currents
                                        label   = 'CURRENTS'                                             ,                # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \  # Currents visible
                                                                    [False for j in range(len(list(Voltages_labels_dict.values())))]+ \ # Voltages hidden
                                                                    [False for j in range(len(list(Voltages_labels_dict.values())))],   # PWM hidden
                                                    'title'     : 'CURRENTS'                             ,                # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Define button for showing all plots.
            button_volt          = dict(                                                                                  # Button to show only voltages
                                        label   = 'VOLTAGES'                                             ,                # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \ # Currents hidden
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))]+ \  # Voltages visible
                                                                    [False for j in range(len(list(Voltages_labels_dict.values())))],   # PWM hidden
                                                    'title'     : 'VOLTAGES'                             ,                # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Define button for showing PWM plots.
            button_pwm          = dict(                                                                                   # Button to show only PWM
                                        label   = 'PWM SIGNALS'                                             ,             # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \ # Currents hidden
                                                                    [False for j in range(len(list(Voltages_labels_dict.values())))]+ \ # Voltages hidden
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))],    # PWM visible
                                                    'title'     : 'PWM SIGNALS'                             ,             # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Define button for showing PWM and voltages plots.
            button_pwm_volt          = dict(                                                                             # Button for PWM + voltages
                                        label   = 'PWM & VOLTAGES'                                             ,          # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [False for i in range(len(list(Currents_labels_dict.values())))]+ \ # Currents hidden
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))]+ \  # Voltages visible
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))],    # PWM visible
                                                    'title'     : 'PWM SIGNALS & VOLTAGES'                             ,  # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Define button for showing PWM and currentsplots.
            button_pwm_curr          = dict(                                                                             # Button for PWM + currents
                                        label   = 'PWM & CURRENTS'                                             ,          # Button label
                                        method  = 'update'                                          ,                     # Update method
                                        args    = [{'visible'   :   [True for i in range(len(list(Currents_labels_dict.values())))]+ \  # Currents visible
                                                                    [False for j in range(len(list(Voltages_labels_dict.values())))]+ \ # Voltages hidden
                                                                    [True for j in range(len(list(Voltages_labels_dict.values())))],    # PWM visible
                                                    'title'     : 'PWM SIGNALS & CURRENTS'                             ,  # Plot title
                                                    'showlegend': True                                                      # Show legend
                                                    }
                                                ],
                                        )
            #? Initialize and Define layout arguments for overall plots.
            fig.update_layout(                                                                                            # Final plot configuration
                updatemenus     =   [dp.go.layout.Updatemenu(                                                            # Add dropdown menu
                                        active  = 0                                     ,                                # Default active button
                                        buttons = [button_all,button_curr,button_volt,button_pwm,button_pwm_volt,button_pwm_curr]  ,  # All buttons
                                        direction = 'up'                                ,                                # Menu direction
                                        x       = 0                                     ,                                # X position
                                        xanchor = 'left'                                ,                                # X anchor
                                        y       = -0.1                                  ,                                # Y position
                                        yanchor = 'top'  )                              ,                                # Y anchor
                                    ],
                title           =   "VOLTAGES VS CURRENTS VS PWM"                                               ,         # Main title
                xaxis           =   dict(title='Time [ s ]')                            ,                                 # X-axis label
                yaxis           =   dict(                                                                                 # Primary y-axis config
                                        side        = "left"                            ,                                 # Position
                                        title       = "Current [ A ]"                   ,                                 # Label
                                        titlefont   = dict(color="#1f77b4")             ,                                 # Color
                                        tickfont    = dict(color="#1f77b4")                                              # Tick color
                                    ),
                yaxis2          =   dict(                                                                                 # Secondary y-axis config
                                        side="right"                                    ,                                 # Position
                                        title="Voltage [ V ]"                           ,                                 # Label
                                        titlefont=dict(color="#1f77b4")                 ,                                 # Color
                                        tickfont=dict(color="#1f77b4")                  ,                                 # Tick color
                                    ),
                plot_bgcolor    =   '#f8fafd'                                                                             # Background color
                )

            #?----------------------------------------------------
            return fig                                                                                                    # Return the configured figure

    def append_to_html(self,csv_filename,figure, filename,auto_open, i=1,include_plotlyjs='cdn'):                          # Define method to append figures to HTML
            """                                                                                                               # Docstring begins
            Appends figures to an existing html file.                                                                        # Method description

            Args:                                                                                                             # Arguments section
                figure (object)                     : plotly lib graph objects class object.                                  # Figure argument
                filename (string)                   : path of the html file.                                                  # Filename argument
                include_plotlyjs (str, optional)    : Defaults to 'cdn'. check tohtml  : https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.to_html
                auto_open (bool, optional)          : Determines whether the file should open automatically. Defaults to False.
            """                                                                                                               # Docstring ends
            #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
            #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent page loads faster.
            multiplot       = self.multiplot(csv_filename)                                                                    # Generate multiplot from CSV
            tables          = self.add_table(i)                                                                               # Add tables with index i
            date            = str(dp.datetime.datetime.now().replace(microsecond=0))                                          # Get current datetime without microseconds
            if dp.JSON["figureName"] and dp.JSON["figureComment"]:                                                            # Check if figure names and comments exist in JSON
                self.FigureNames                =   [dp.plt_title_list[i][0] for i in range(len(dp.plt_title_list))]          # Create list of figure names
                self.fftFigureNames             =   [f'FFT {dp.plt_title_list[i][0]}' for i in range(len(dp.plt_title_list))] # Create list of FFT figure names
                self.CtrlFigureNames            =   list(dp.pmap_plt_ctrl.keys())                                             # Get control figure names
                self.FigTitles                  =   (self.shuffle_lists(self.FigureNames, self.fftFigureNames)) + self.CtrlFigureNames  # Combine and shuffle figure names
                self.Comments                   =   [" " for _ in range((2*len(dp.plt_title_list))+ len(self.CtrlFigureNames))]         # Initialize empty comments

            with open(filename, 'w') as f:                                                                                    # Open HTML file for writing
                f.write(self.title)                                                                                           # Write HTML title
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
                    </div>')                                                                                                  # Write header with logo and info

                f.write(self.separator)                                                                                      # Write HTML separator
                f.write(tables.to_html(include_plotlyjs=include_plotlyjs))                                                   # Write tables as HTML
                f.write(self.separator)                                                                                      # Write HTML separator
                f.write(multiplot.to_html(include_plotlyjs=include_plotlyjs))                                                # Write multiplot as HTML
                f.write(self.separator)                                                                                      # Write HTML separator
                if dp.JSON["figureName"] and dp.JSON["figureComment"]:                                                        # Check if figure names/comments exist
                    # assign the comments based on json :                                                                     # Comment for JSON processing
                    for b in range(len(dp.JSON["figureName"])):                                                               # Loop through figure names
                        self.Comments[self.FigTitles.index(dp.JSON["figureName"][b])] =  dp.JSON["figureComment"][b]          # Assign comments based on JSON
                for i in range(len(figure)):                                                                                  # Loop through figures
                    f.write(figure[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs))                            # Write figure as HTML
                    if dp.JSON["figureName"] and dp.JSON["figureComment"]:                                                    # Check if comments exist
                        if not self.Comments[i] == " " :                                                                      # Check if comment is not empty
                            f.write(f'<input type="text" style="font-size:9pt;height:50px;width:1500px;" value="{self.Comments[i]}" readonly="readonly">')  # Write comment box
                    f.write(self.separator)                                                                                   # Write HTML separator
                constant_tables = self.add_constant_table(csv_filename)                                                      # Generate constant tables
                f.write(constant_tables.to_html(include_plotlyjs=include_plotlyjs))                                           # Write constant tables as HTML
                self.constants_list.clear()                                                                                   # Clear constants list
                self.constants_vals.clear()                                                                                   # Clear constants values
                self.constants_units.clear()                                                                                  # Clear constants units
                if dp.JSON["figureName"] and dp.JSON["figureComment"]:                                                        # Check if figure names/comments exist
                    self.FigTitles.clear()                                                                                    # Clear figure titles
                    self.FigureNames.clear()                                                                                  # Clear figure names
                    self.fftFigureNames.clear()                                                                              # Clear FFT figure names
                    self.Comments.clear()                                                                                     # Clear comments
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
                    </html>')                                                                   # Write footer HTML with controls
            f.close()                                                                                                        # Close file (redundant due to 'with')
            if auto_open:                                                                                                    # Check if auto-open enabled
                import pathlib, webbrowser                                                                                   # Import required modules
                uri = pathlib.Path(filename).absolute().as_uri()                                                             # Convert path to URI
                webbrowser.open(uri)                                                                                         # Open in web browser

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
        fig_list          =   []                                                                               # Initialize empty figure list
        include_plotlyjs  =   'cdn'                                                                            # Set to use CDN for Plotly JS
        labels_dict       =   dict(label_dict)                                                                 # Create copy of label dictionary
        dict_keys         =   list(labels_dict.keys())                                                         # Get list of keys from label dictionary
        csv_files         =   [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv')]    # Get all csv files in directory excluding MAP files

        if len(csv_files) >= 1:                                                                                # Check if there are CSV files to process
            csv_files     =   dp.natsorted(csv_files)                                                          # Sort files naturally/alphanumerically
            dfs           =   [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]                       # Read each CSV into a DataFrame
            for each in dict_keys :                                                                            # Loop through each key in label dictionary
                fig = dp.make_subplots()                                                                       # Create empty subplot figure
                C         =   1                                                                               # Initialize iteration counter
                for df in dfs :                                                                                # Loop through each DataFrame
                    fig.add_trace(                                                                             # Add trace to figure
                        dp.go.Scatter(                                                                         # Create scatter plot
                            x       = df.iloc[:,0] ,                                                          # Set x-axis data (first column)
                            y       = df.iloc[:,labels_dict.get(each)] ,                                       # Set y-axis data (from specified column)
                            name    = str("Iter :" + str(C) + " | ") + each ,                                  # Set trace name with iteration info
                            mode    = "lines" ,                                                                # Set to line plot mode
                            line    = dict(shape = 'linear')                                                   # Set line style
                        )
                    )

                    fig.update_layout(                                                                         # Update figure layout
                        showlegend      =   True ,                                                             # Show legend
                        title           =   each ,                                                             # Set title from key
                        xaxis           =   dict(title='Time [ S ]') ,                                        # Set x-axis title
                        yaxis           =   dict(                                                             # Configure y-axis
                                                side        = "left" ,                                         # Position y-axis on left
                                                title       = Y_axis_label ,                                   # Set y-axis title
                                                titlefont   = dict(color="#1f77b4") ,                          # Set title color
                                                tickfont    = dict(color="#1f77b4")                            # Set tick color
                                            ),
                        plot_bgcolor    =   '#f8fafd'                                                         # Set background color
                    )
                    C+=1                                                                                       # Increment iteration counter
                fig_list.append(fig)                                                                           # Add figure to figure list
                #!-----------------------------------------------------------------------------------
                #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
                #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent
                #* page loads faster.
                if dp.JSON['iterSplit']:                                                                       # Check if split by iteration is enabled
                    date = str(dp.datetime.datetime.now().replace(microsecond=0))                              # Get current timestamp
                    with open(html_path + "_" + each + ".html", 'w') as f:                                    # Open HTML file for writing
                        f.write(self.title)                                                                    # Write report title
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

                        f.write(self.separator)                                                                # Add separator
                        f.write(fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs))              # Write figure as HTML
                        f.write(self.separator)                                                                # Add separator
                    f.close()                                                                                 # Close file

            if not dp.JSON['iterSplit']:                                                                      # Check if not split by iteration
                date = str(dp.datetime.datetime.now().replace(microsecond=0))                                # Get current timestamp
                with open(html_path + "_" + type + ".html", 'w') as f:                                      # Open HTML file for writing
                    f.write(self.title)                                                                      # Write report title
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

                    f.write(self.separator)                                                                  # Add separator
                    for fig_i in fig_list:                                                                   # Loop through all figures
                        f.write(fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs))          # Write figure as HTML
                        f.write(self.separator)                                                              # Add separator
                f.close()                                                                                  # Close file
            if auto_open:                                                                                   # Check if auto-open enabled
                import pathlib, webbrowser                                                                 # Import required modules
                uri = pathlib.Path(html_path).absolute().as_uri()                                          # Get absolute URI of HTML file
                webbrowser.open(uri)                                                                       # Open in default web browser

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
        figure_list     = []                                                                                                      # Initialize empty figure list
        df              = dp.pd.read_csv(fName)                                                                                   # Read CSV file into DataFrame
        for key, _ in odict.items():                                                                                             # Loop through each key in odict
                titles      = [odict[key][x][1][0] for x in range(len(odict[key]))]                                              # Extract subplot titles
                fig         = dp.make_subplots(rows=len(odict[key]), cols=1,subplot_titles=titles,shared_xaxes=True,vertical_spacing=0.08)  # Create subplot figure
                for j in range(len(odict[key])):                                                                                  # Loop through each subplot
                    for i in range(len(odict[key][j][0])):                                                                       # Loop through each trace in subplot
                        X,Y     =   df.iloc[:,0],df.iloc[:,odict[key][j][2][i]]                                                  # Get x and y data
                        if len(set(Y)) == 1:                                                                                      # Check if all y values are identical
                            # If all Y values are the same, only plot the first and last values
                            new_df = dp.pd.DataFrame({'X': [X.iloc[0], X.iloc[-1]], 'Y': [Y.iloc[0], Y.iloc[-1]]})               # Create minimal DataFrame
                            fig.add_trace(dp.go.Scatter(x=new_df['X'], y=new_df['Y'], name=odict[key][j][0][i]), row=j+1, col=1)  # Add simplified trace
                        else:                                                                                                    # If y values vary
                            fig.add_trace(dp.go.Scatter(x=X, y=Y, name=odict[key][j][0][i]), row=j+1, col=1)                     # Add full trace
                    fig['layout'][f'yaxis{j+1}']['title']= odict[key][j][3][i]                                                   # Set y-axis title
                fig['layout'][f'xaxis{j+1}']['title']= 'Time [s]'                                                               # Set x-axis title
                fig.update_xaxes(range=xaxis_range, dtick=xticks)                                                                # Update x-axis range and ticks
                fig.update_yaxes(range=yaxis_range, dtick=yticks)                                                                # Update y-axis range and ticks
                if Legend   ==  True:                                                                                            # Check legend flag
                    if dp.JSON['TF_Config'] == 'DCDC_D':                                                                         # Check special configuration
                        fig.update_layout(title={'text' : str(key) },showlegend = True)                                          # Update layout with title and legend
                    else:                                                                                                        # Default configuration
                        if len(odict[key])>1:                                                                                   # Check if multiple subplots
                            fig.update_layout(title={'text' : str(key) },showlegend = True)                                      # Update layout with title and legend
                        else:                                                                                                    # Single subplot case
                            fig.update_layout(                                                                                   # Update layout
                                            showlegend      =   False,                                                           # Hide legend
                                            plot_bgcolor    =   '#f8fafd',                                                      # Set background color
                                            yaxis2          =   dict(                                                           # Configure y-axis
                                                                    anchor      =   'free',                                     # Set anchor
                                                                    position    =   0,                                          # Set position
                                                                    side        =   'left'                                      # Set side
                                                                ))
                else:                                                                                                            # Legend disabled
                    fig.update_layout(showlegend = False)                                                                        # Hide legend
                fig.update_traces(hovertemplate=None)                                                                           # Clear hover templates
                fig.update_layout(hovermode="x unified")                                                                        # Set unified hover mode
                figure_list.append(fig)                                                                                          # Add figure to list

        return figure_list                                                                                                      # Return list of figures

    def return_headers(self,header_file):
        """
       Returns list of headers from json header file.

       Parameters  :
                      header_file   :       String
                                            Path to the json header file.
        Returns    :  header        :       list
                                            List of headers .
        """
        with open(header_file, 'r') as f:                                                                                         # Open header file in read mode
            header = dp.json.load(f)                                                                                             # Load JSON data from file
        f.close()                                                                                                                 # Close file (redundant due to 'with')
        return header                                                                                                             # Return the loaded headers

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
            Current_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Current.json")  # Get current headers from JSON
            Voltage_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Voltage.json")  # Get voltage headers from JSON
            dfcurr                        = dp.pd.read_csv(current_fft_csv, header=None,index_col=None)                                            # Read current CSV data
            dfvolt                        = dp.pd.read_csv(voltage_fft_csv, header=None,index_col=None)                                            # Read voltage CSV data
            figure_list                   = []                                                                                                      # Initialize empty figure list
            for i in range(len(dp.plt_title_list)):                                                                                                 # Loop through plot titles
                fig                   = dp.make_subplots(rows=1, cols=1,specs=[[{"secondary_y": True}]])                                           # Create subplot figure
                current_idx_list      = [Current_headers.index(dp.plt_title_list[i][1])] if len(dp.plt_title_list[i])<5 else [ Current_headers.index(dp.plt_title_list[i][1]) , Current_headers.index(dp.plt_title_list[i][2])  ]  # Get current indices
                voltage_idx_list      = [Voltage_headers.index(dp.plt_title_list[i][2])] if len(dp.plt_title_list[i])<5 else [ Voltage_headers.index(dp.plt_title_list[i][3]) , Voltage_headers.index(dp.plt_title_list[i][4])  ]  # Get voltage indices
                current_titles        = [dp.plt_title_list[i][1]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][1] , dp.plt_title_list[i][2]  ]                                                      # Get current titles
                voltage_titles        = [dp.plt_title_list[i][2]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][3] , dp.plt_title_list[i][4]  ]                                                      # Get voltage titles

                if dp.JSON['FFT'] :                                                                                                                                                                             # Check if FFT is enabled
                    for c, name in enumerate(current_titles):                                                                                                                                                   # Loop through current traces
                        fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfcurr.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), current_idx_list[c]], name=name), row=1, col=1,secondary_y=False)  # Add current bar trace
                    for j, name in enumerate(voltage_titles):                                                                                                                                                   # Loop through voltage traces
                        fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfvolt.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), voltage_idx_list[j]], name=name), row=1, col=1,secondary_y=True)   # Add voltage bar trace
                else:                                                                                                                                                                                          # If FFT not enabled
                        return []                                                                                                                                                                              # Return empty list
                fig.update_layout(                                                                                                                                                                             # Update figure layout
                    title           =   f'FFT Magnitudes - {dp.plt_title_list[i][0]}',                                                                                                                         # Set title
                    xaxis_title     =   'Harmonic Orders',                                                                                                                                                     # Set x-axis title
                    xaxis           =   dict (                                                                                                                                                                 # Configure x-axis
                                                tickvals = dp.harmonics ,                                                                                                                                      # Set tick values
                                                ticktext = dp.harmonics                                                                                                                                        # Set tick labels
                                            ),                                                                                                                                                                 
                    yaxis           =   dict(                                                                                                                                                                 # Configure left y-axis
                                        side        = "left"                            ,                                                                                                                     # Position on left
                                        title       = "Current Magnitude"                   ,                                                                                                                 # Set title
                                        titlefont   = dict(color="#1f77b4")             ,                                                                                                                     # Set title color
                                        tickfont    = dict(color="#1f77b4")                                                                                                                                   # Set tick color
                                    ),                                                                                                                                                                        
                    yaxis2          =   dict(                                                                                                                                                                 # Configure right y-axis
                                        side="right"                                    ,                                                                                                                     # Position on right
                                        title="Voltage Magnitude"                           ,                                                                                                                 # Set title
                                        titlefont=dict(color="#1f77b4")                 ,                                                                                                                     # Set title color
                                        tickfont=dict(color="#1f77b4")                  ,                                                                                                                     # Set tick color
                                    ),                                                                                                                                                                        
                    plot_bgcolor    =   '#f8fafd'             ,                                                                                                                                               # Set background color
                    barmode         =   'overlay'                                                                                                                                                             # Set bar mode to overlay
                )                                                                                                                                                                                             
                figure_list.append(fig)                                                                                                                                                                       # Add figure to list

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

        list3 = []                                                                                                            # Initialize empty result list
        for i in range(len(list1)):                                                                                           # Iterate through indices of list1
            list3.append(list1[i])                                                                                            # Append current element from list1
            if list2:                                                                                                        # Check if list2 exists
                list3.append(list2[i])                                                                                        # Append current element from list2
        return list3                                                                                                          # Return the shuffled list

    def fft_gen_iter_report(self, FFT_file,title, csv_path, html_path, type ,auto_open):                                        # Define function to generate HTML FFT report for multiple iterations
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
        include_plotlyjs          = 'cdn'                                                                                     # Use Plotly CDN for JS resources
        headers                   = self.return_headers( (dp.os.getcwd()).replace("\\","/") + f"/Script/assets/HEADER_FILES/{FFT_file}")   # Load headers from FFT JSON file
        df                        = dp.pd.read_csv(csv_path, header=None,index_col=None)                                       # Load CSV data into DataFrame without headers
        figure_list               = []                                                                                        # Initialize list to store figures
        num_iterations            = df.shape[0] // len(dp.harmonics)                                                          # Calculate number of iterations from rows/harmonics
        for column in range(df.shape[1]):                                                                                     # Loop through each column in DataFrame
            fig                   = dp.go.Figure()                                                                            # Create a new Plotly figure
            for iteration in range(num_iterations):                                                                           # Loop through iterations
                iteration_data    = df.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), column]       # Extract data for current iteration
                fig.add_trace(                                                                                                # Add bar trace for this iteration
                    dp.go.Bar(
                            x     =   dp.harmonics,                                                                           # Harmonic order on x-axis
                            y     =   iteration_data,                                                                         # FFT magnitudes on y-axis
                            name  =   f'{headers[column]} {title} : Iteration {iteration + 1}'                                # Label with header and iteration
                        )
                    )
            fig.update_layout(                                                                                                # Update layout of figure
                title           =   f'FFT Magnitudes - {headers[column]}',                                                    # Set chart title
                showlegend      =   True                                 ,                                                    # Show legend
                xaxis_title     =   'Harmonic Orders',                                                                        # Label x-axis
                yaxis_title     =   'Magnitude',                                                                             # Label y-axis
                xaxis           =   dict (                                                                                   # Configure x-axis ticks
                                            tickvals = dp.harmonics ,
                                            ticktext = dp.harmonics
                                        ),
                barmode         =   'stack'                                                                                  # Stack bars for iterations
            )
            figure_list.append(fig)                                                                                           # Store figure in list

            #!-----------------------------------------------------------------------------------
            #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
            #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent
            #* page loads faster.
            if dp.JSON['iterSplit']:                                                                                          # Check if results should be split into separate files
                date = str(dp.datetime.datetime.now().replace(microsecond=0))                                                  # Get current date/time without microseconds
                with open(html_path + "_" + str(headers[column]) + "_FFT.html", 'w') as f:                                     # Open individual HTML file for this column
                    f.write(self.title)                                                                                       # Write report title
                    f.write('<style>    .container  {position: relative;text-align: right;color: black;}    \
                                        .Simulation {position: absolute;top: 10px;left: 16px;}              \
                                        .DateTime   {position: absolute;top: 50px;left: 16px;}              \
                                        .Sim_ID     {position: absolute;top: 90px;left: 16px;}              \
                            </style>'f'<div class="container">  \
                                        <img src="data:image/png;base64,{self.image}"/> \
                                        <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>\
                                        <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div> \
                                        <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div> \
                            </div>')                                                                                          # Write header block with logo, sim name, date, ID
                    f.write(self.separator)                                                                                   # Write separator
                    f.write(fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs))                                   # Embed figure HTML
                    f.write(self.separator)                                                                                   # Write separator
                f.close()                                                                                                     # Close file

        if not dp.JSON['iterSplit']:                                                                                          # If not splitting, create single combined HTML
            date = str(dp.datetime.datetime.now().replace(microsecond=0))                                                      # Get current date/time
            with open(html_path + "_" + type + "_FFT.html", 'w') as f:                                                         # Open combined HTML file
                f.write(self.title)                                                                                           # Write report title
                f.write('<style>    .container  {position: relative;text-align: right;color: black;}    \
                                    .Simulation {position: absolute;top: 10px;left: 16px;}              \
                                    .DateTime   {position: absolute;top: 50px;left: 16px;}              \
                                    .Sim_ID     {position: absolute;top: 90px;left: 16px;}              \
                        </style>'f'<div class="container">  \
                                    <img src="data:image/png;base64,{self.image}"/> \
                                    <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>\
                                    <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div> \
                                    <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div> \
                        </div>')                                                                                              # Write header block with sim info
                f.write(self.separator)                                                                                       # Write separator
                for fig_i in figure_list:                                                                                     # Loop through all figures
                    f.write(fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs))                                # Embed figure HTML
                    f.write(self.separator)                                                                                   # Write separator
            f.close()                                                                                                         # Close file

        if auto_open:                                                                                                         # If auto_open is True
            import pathlib, webbrowser                                                                                        # Import libraries for browser interaction
            uri = pathlib.Path(html_path).absolute().as_uri()                                                                 # Convert HTML path to URI
            webbrowser.open(uri)                                                                                              # Open report in web browser

    def auto_plot(self,simutil,fileLog,misc,open=False,iterReport=False):                                                     # Define function to auto-generate HTML plots and reports
        """                                                                                                                    # Function docstring
        Generates an HTML report containing multiple plots.                                                                    # Description of purpose

        Args:                                                                                                                  # Arguments section
            misc (object)               : Miscellaneous object containing utility functions.                                   # Argument misc
            Open (bool, optional)       : If True, open the generated HTML report automatically. Defaults to False.            # Argument open
            iterReport (bool, optional) : If True, generate iterations HTML report. Defaults to False.                         # Argument iterReport
        """                                                                                                                    # End docstring
        misc.tic()                                                                                                            # Start timing the process
        ResDir          =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"    # Directory for time-series CSVs
        MAPS_dir        =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"          # Directory for MAP CSVs
        FFT_curr_path   =   MAPS_dir+"/FFT_Current_Map.csv"                                                                    # Path to FFT Current map CSV
        FFT_volt_path   =   MAPS_dir+"/FFT_Voltage_Map.csv"                                                                    # Path to FFT Voltage map CSV
        c               =   0                                                                                                  # Counter for reports
        file_list       =   fileLog.natsort_files(ResDir)                                                                      # Get sorted list of CSV files
        legend          =   True if dp.JSON['TF_Config'] == 'DCDC_D' else False                                                # Enable legend only for DCDC_D config
        if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':                                                                       # If transformer config is DCDC_S or DCDC_D
            simutil.postProcessing.drop_Extra_Cols(FFT_curr_path,dp.idx_start,dp.idx_end)                                      # Drop extra columns from FFT current map CSV
        if iterReport:                                                                                                         # If iteration reports should be generated
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Currents'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ A ]" ,"Currents",open)  # Generate iteration report for currents
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Voltages'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ V ]" ,"Voltages",open)  # Generate iteration report for voltages
        if iterReport and dp.JSON['FFT']:                                                                                      # If FFT and iteration report enabled
            self.fft_gen_iter_report( "FFT_Current.json", " Currents_FFT" ,FFT_curr_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc  ,"Currents_FFT" ,open)  # Generate FFT report for currents
            self.fft_gen_iter_report( "FFT_Voltage.json", "Voltages_FFT" ,FFT_volt_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_"  + self.utc  ,"Voltages_FFT" ,open)  # Generate FFT report for voltages

        for x  in range(len(file_list)):                                                                                       # Iterate over each result file
            FFT_figs                =   self.fft_bar_plot(FFT_curr_path,FFT_volt_path,x)                                       # Generate FFT bar plots for current and voltage
            figures_list            =   self.plot_scopes(file_list[x],dp.pmap_plt,Legend=legend)                               # Generate scope plots for CSV file
            figures_list_           =   self.shuffle_lists(figures_list,FFT_figs)                                              # Shuffle scope plots and FFT plots together
            if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':                                                                   # If config is DCDC_S or DCDC_D
                simutil.postProcessing.drop_Extra_Cols(file_list[x],sum(dp.Y_list[0:3]),sum(dp.Y_list[0:4]))                   # Drop extra columns from CSV file
                figures_list_ctrl   =   self.plot_scopes(file_list[x],dp.pmap_plt_ctrl,Legend=True)                            # Generate additional control scope plots
                figures_list_.extend(figures_list_ctrl)                                                                        # Append control plots to figure list
            c+=1                                                                                                              # Increment counter
            self.append_to_html(file_list[x] , figures_list_,fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_" + str(c) + ".html", auto_open=open , i=c-1)  # Append figures to HTML report
            self.constants_list,self.constants_vals,self.constants_units,figures_list_  = [],[],[],[]                          # Reset constants and figure lists

        fileLog.log(f"Generating HTML Report    {'= '.rjust(49+17, ' ')}{str(misc.toc())} seconds.\n")                         # Log generation time
        file_list.clear()                                                                                                      # Clear file list
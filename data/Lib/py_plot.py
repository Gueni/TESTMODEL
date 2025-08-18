
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

        self.ResultsPath                =   ResultsPath
        self.utc                        =   utc
        self.hostname                   =   str(dp.socket.gethostname())
        self.script_name                =   dp.scriptname       #dp.os.path.basename(dp.sys.argv[0])[:-3]
        self.values_dict                =   dict()
        self.config_dicts               =   dict()
        self.configkey_list             =   []
        self.configval_list             =   []
        self.valkey_list                =   []
        self.values_list                =   []
        self.headerColor                =   '#009ADA'
        self.even_rc                    =   '#E0E0E0'
        self.odd_rc                     =   'white'
        self.title                      =   f"<html><head><title>{self.script_name}_Report_{self.utc}_{self.hostname}</title></head><body></body></html>"
        self.separator                  =   "<html><body><hr style='height:1px;border:none;color:#333;background-color:#333;'></body></html>"
        self.image                      =   ''
        self.tab_val_list               =   []
        self.tab_conf_list              =   []
        self.iter_param_key             =   []
        self.iter_param_val             =   []
        self.iter_param_unt             =   []
        self.note                       =   "N/A"
        self.constants_list             =   []
        self.constants_vals             =   []
        self.constants_units            =   []
        self.standalone                 =   standalone
        self.json_file                  =   "Standalone_variables.json" if standalone else "Input_vars.json"
        self.json_path                  =   dp.os.path.join(dp.os.getcwd(), "Script", "assets", self.json_file).replace("\\", "/")

        with open(self.json_path) as file:
            self.data = dp.json.load(file)

        self.X1, self.X2, self.X3, self.X4, self.X5, self.X6, self.X7, self.X8, self.X9, self.X10 = (
            eval(self.data[f'X{i}']) for i in range(1, 11)
        )

        self.pattern                    =   self.data['permute']
        self.dimension_names            =   self.data['Dimension_Names']
        self.matrix                     =   [self.X1, self.X2, self.X3, self.X4, self.X5, self.X6, self.X7, self.X8, self.X9, self.X10]
        self.startpoint                 =   [X[0] for X in self.matrix]
        self.separate_files             =   self.data['plotFiles']
        self.var1                       =   eval(self.data[self.data["Var1"]])
        self.variable_2                 =   self.data["Var2"]
        self.base64_img()

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
        with open(dp.BMW_Base64_Logo,'r') as fin:
            lines = fin.readlines()
        for line in lines:
            self.image+=line
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

            Returns:
            --------
            None
        """
        source_mdlvar			=	dp.copy.deepcopy(input_dict)
        self.config_dicts		= 	{ # Hard coded !!

        							'Probes'  			: 	source_mdlvar['Common']['Probes']			,
        							'ToFile'			:	source_mdlvar['Common']['ToFile']			,
        							'PSFBconfigs'  		: 	source_mdlvar['Common']['PSFBconfigs'] 	,
        							'RboxConfigs'  		: 	source_mdlvar['Common']['RboxConfigs']

               						}
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

        Returns:
        --------
        None
        """
        if isinstance(dictt, dict):
            for k, v2 in dictt.items():
                p2 = "{}['{}']".format(prefix, k)
                self.table_data(v2, key_list,val_list,p2)
        else:
            key_list.append(prefix)
            val_list.append(str(dictt)) # self.val_list.append(repr(dictt)) #if you want full long value.

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

        df                      =   dp.pd.read_csv(csv_file)
        for key , val in dp.constant_dict.items():
            column_values = df.iloc[:, val[1]]
            column_values = column_values.to_numpy()
            column_values = column_values[-50:]
            self.constants_list.append(val[0])
            self.constants_vals.append(dp.np.mean(column_values).round(2))
            self.constants_units.append(val[2])
        const_Nrow              =   len(self.constants_vals)

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

        table_figure            =   dp.make_subplots(
                                                    rows                    =   1                                                                 ,
                                                    cols                    =   1                                                                 ,
                                                    shared_xaxes            =   True                                                              ,
                                                    horizontal_spacing      =   0.03                                                              ,
                                                    specs                   =   [[{"type": "table"}]]
                                        )

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
        table_height            =   600
        self.configkey_list.clear()
        self.configval_list.clear()
        self.valkey_list.clear()
        self.values_list.clear()
        self.table_data(self.tab_conf_list[i],self.configkey_list,self.configval_list)
        self.table_data(self.tab_val_list[i],self.valkey_list,self.values_list)
        config_Nrow             =   len(self.configval_list)
        val_Nrow                =   len(self.values_list)
        param_Nrow              =   len(self.iter_param_val[i])

        #* subsystems configuration table------------------------------------
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
        #* parameters values table-------------------------------------------
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

        #* parameters values table-------------------------------------------
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


        table_figure            =   dp.make_subplots(
                                                    rows                            =   2                                            ,
                                                    cols                            =   2                                            ,
                                                    shared_xaxes                    =   True                                         ,
                                                    horizontal_spacing              =   0.03                                         ,
                                                    specs                           =   [[{"type": "table"}, {"type": "table"}],[{"type": "table"}, {"type": "table"}]]
                                        )


        table_figure.update_layout(height=table_height, title_text="Simulation Model Configurations & Parameters:",font_size=16)
        table_figure.add_trace(config_table,row=1, col=1)
        table_figure.add_trace(val_table,row=1, col=2)
        table_figure.add_trace(readme_message,row=2, col=1)
        table_figure.add_trace(updated_vals_table,row=2, col=2)

        return table_figure

    def subplot(self,name_list,filename,x_axis,y_axis,xlabel_list,ylabel_list,
                titles,n_rows,n_cols,xticks=None,yticks=None,xaxis_range=None,yaxis_range=None):
        """
        creates a subplot by default of 3 and returns a figure.

        Args:
            filename (string)                   : path /name of the csv file containing the data.
            x_axis (list)                       : list of x axes column numbers (indicates the index of column inside the data file).
            y_axis (list)                       : list of y axes column numbers (indicates the index of column inside the data file).
            xlabel_list (list)                  : list of labels for the x axes.
            ylabel_list (list)                  : list of lables for the y axes.
            titles (list)                       : list of titles for the different subplots.
            nrows (int, optional)               : number of rows in the subplot figure. Defaults to 3.
            ncols (int, optional)               : number of columns in the subplot figure. Defaults to 1.
            xticks (float, optional)            : x axis ticks step. Defaults to None.
            yticks (float, optional)            : y axis ticks step. Defaults to None.
            xaxis_range (list, optional)        : range/slice of x axis values [start,end]. Defaults to None.
            yaxis_range (list, optional)        : range/slice of y axis values [start,end]. Defaults to None.

        Returns:
            fig (object)                        : Figure object containing all subplots.
        """
        if int(n_rows) <= 4:
            df          = dp.pd.read_csv(filename)
            fig         = dp.make_subplots(rows=n_rows, cols=n_cols,subplot_titles=titles,shared_xaxes=True,vertical_spacing=0.08)
            for i in range(n_rows):
                X,Y     =   df.iloc[:,x_axis[i]], df.iloc[:,y_axis[i]]
                if len(set(Y)) == 1:
                    # If all Y values are the same, only plot the first and last values
                    new_df = dp.pd.DataFrame({'X': [X.iloc[0], X.iloc[-1]], 'Y': [Y.iloc[0], Y.iloc[-1]]})
                    fig.add_trace(dp.go.Scatter(x=new_df['X'], y=new_df['Y'], name=name_list[i]), row=i+1, col=1)
                else:
                    fig.add_trace(dp.go.Scatter(x=X, y=Y, name=name_list[i]), row=i+1, col=1)
                fig['layout'][f'xaxis{i+1}']['title']= xlabel_list[i]
                fig['layout'][f'yaxis{i+1}']['title']= ylabel_list[i]

                fig.update_xaxes(range=xaxis_range, dtick=xticks)
                fig.update_yaxes(range=yaxis_range, dtick=yticks)

                fig.update_layout(
                    showlegend      =   False                       ,
                    yaxis2          =   dict(
                                            anchor      =   'free'  ,
                                            position    =   0       ,
                                            side        =   'left'
                                            )                       ,
                    # paper_bgcolor   =   '#f8fafd'                  ,
                    plot_bgcolor    =   '#f8fafd'

                    )

        return fig

    def multiplot(self,csv_file):
        """Generate a plot of voltage and current data from a Plecs simulation output file.

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
        """
        #? Genarate dataframe from csv file.
        dff                     = dp.pd.read_csv(csv_file)
        #? Retrieve data index dictionaries from plecs_mapping module.
        Voltages_labels_dict    = dp.pmap_multi['Peak_Voltages']
        Currents_labels_dict    = dp.pmap_multi['Peak_Currents']
        PWM_labels_dict         = dp.pwm_dict
        #? Get keys from previously defined dictionaries (to be used as labels)
        voltage_keys            = list(Voltages_labels_dict.keys())
        Current_keys            = list(Currents_labels_dict.keys())
        PWM_keys                = list(PWM_labels_dict.keys())
        #? Initialize an empty figure.
        # Create figure with secondary y-axis
        fig = dp.make_subplots(specs=[[{"secondary_y": True}]])
        #? Create and add Traces for th Current Plots.
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
        #? Create and add Traces for th Voltage Plots.
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
        #? Create and add Traces for th PWM Plots.
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
        #? Define button for showing all plots.
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
        #? Define button for showing Current plots.
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
        #? Define button for showing all plots.
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
        #? Define button for showing PWM plots.
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
        #? Define button for showing PWM and voltages plots.
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
        #? Define button for showing PWM and currentsplots.
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
        #? Initialize and Define layout arguments for overall plots.
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

        #?----------------------------------------------------
        return fig

    def append_to_html(self,csv_filename,figure, filename,auto_open, i=1,include_plotlyjs='cdn'):
        """
        Appends figures to an existing html file.

        Args:
            figure (object)                     : plotly lib graph objects class object.
            filename (string)                   : path of the html file.
            include_plotlyjs (str, optional)    : Defaults to 'cdn'. check tohtml  : https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.to_html
            auto_open (bool, optional)          : Determines whether the file should open automatically. Defaults to False.
        """
        #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
        #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent page loads faster.
        multiplot       = self.multiplot(csv_filename)
        tables          = self.add_table(i)
        date            = str(dp.datetime.datetime.now().replace(microsecond=0))
        if dp.JSON["figureName"] and dp.JSON["figureComment"]:
            self.FigureNames                =   [dp.plt_title_list[i][0] for i in range(len(dp.plt_title_list))]
            self.fftFigureNames             =   [f'FFT {dp.plt_title_list[i][0]}' for i in range(len(dp.plt_title_list))]
            self.CtrlFigureNames            =   list(dp.pmap_plt_ctrl.keys())
            self.FigTitles                  =   (self.shuffle_lists(self.FigureNames, self.fftFigureNames)) + self.CtrlFigureNames
            self.Comments                   =   [" " for _ in range((2*len(dp.plt_title_list))+ len(self.CtrlFigureNames))]

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
            if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                # assign the comments based on json :
                for b in range(len(dp.JSON["figureName"])):
                    self.Comments[self.FigTitles.index(dp.JSON["figureName"][b])] =  dp.JSON["figureComment"][b]
            for i in range(len(figure)):
                f.write(figure[i].to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                    if not self.Comments[i] == " " :
                        f.write(f'<input type="text" style="font-size:9pt;height:50px;width:1500px;" value="{self.Comments[i]}" readonly="readonly">')
                f.write(self.separator)
            constant_tables = self.add_constant_table(csv_filename)
            f.write(constant_tables.to_html(include_plotlyjs=include_plotlyjs))
            self.constants_list.clear()
            self.constants_vals.clear()
            self.constants_units.clear()
            if dp.JSON["figureName"] and dp.JSON["figureComment"]:
                self.FigTitles.clear()
                self.FigureNames.clear()
                self.fftFigureNames.clear()
                self.Comments.clear()
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
        if auto_open:
            import pathlib, webbrowser
            uri = pathlib.Path(filename).absolute().as_uri()
            webbrowser.open(uri)

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
        fig_list          =   []
        include_plotlyjs  =   'cdn'
        labels_dict       =   dict(label_dict)
        dict_keys         =   list(labels_dict.keys())
        csv_files         =   [f for f in os.listdir(path) if f.endswith('.csv') and not f.endswith('_MAP.csv') and not f.endswith('_Standalone.csv')]    # Get all csv files in the directory

        if len(csv_files) >= 1:
            csv_files     =   dp.natsorted(csv_files)                                                               # Sort the file list Alphanumerically.
            dfs           =   [dp.pd.read_csv(os.path.join(path, f)) for f in csv_files]              # Read each csv into a Pandas dataframe
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
            if auto_open:
                import pathlib, webbrowser
                uri = pathlib.Path(html_path).absolute().as_uri()
                webbrowser.open(uri)

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
        figure_list     = []
        df              = dp.pd.read_csv(fName)
        for key, _ in odict.items():
                titles      = [odict[key][x][1][0] for x in range(len(odict[key]))]
                fig         = dp.make_subplots(rows=len(odict[key]), cols=1,subplot_titles=titles,shared_xaxes=True,vertical_spacing=0.08)
                for j in range(len(odict[key])):
                    for i in range(len(odict[key][j][0])):
                        X,Y     =   df.iloc[:,0],df.iloc[:,odict[key][j][2][i]]
                        if len(set(Y)) == 1:
                            # If all Y values are the same, only plot the first and last values
                            new_df = dp.pd.DataFrame({'X': [X.iloc[0], X.iloc[-1]], 'Y': [Y.iloc[0], Y.iloc[-1]]})
                            fig.add_trace(dp.go.Scatter(x=new_df['X'], y=new_df['Y'], name=odict[key][j][0][i]), row=j+1, col=1)
                        else:
                            fig.add_trace(dp.go.Scatter(x=X, y=Y, name=odict[key][j][0][i]), row=j+1, col=1)
                    fig['layout'][f'yaxis{j+1}']['title']= odict[key][j][3][i]
                fig['layout'][f'xaxis{j+1}']['title']= 'Time [s]'
                fig.update_xaxes(range=xaxis_range, dtick=xticks)
                fig.update_yaxes(range=yaxis_range, dtick=yticks)
                if Legend   ==  True:
                    if dp.JSON['TF_Config'] == 'DCDC_D':
                        fig.update_layout(title={'text' : str(key) },showlegend = True)
                    else:
                        if len(odict[key])>1:
                            fig.update_layout(title={'text' : str(key) },showlegend = True)
                        else:
                            fig.update_layout(
                                            showlegend      =   False,
                                            plot_bgcolor    =   '#f8fafd',
                                            yaxis2          =   dict(
                                                                    anchor      =   'free',
                                                                    position    =   0,
                                                                    side        =   'left'
                                                                ))
                else:
                    fig.update_layout(showlegend = False)
                fig.update_traces(hovertemplate=None)
                fig.update_layout(hovermode="x unified")
                figure_list.append(fig)

        return figure_list

    def return_headers(self,header_file):
        """
       Returns list of headers from json header file.

       Parameters  :
                      header_file   :       String
                                            Path to the json header file.
        Returns    :  header        :       list
                                            List of headers .
        """
        with open(header_file, 'r') as f:
            header = dp.json.load(f)
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
        Current_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Current.json")
        Voltage_headers               = self.return_headers( (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/FFT_Voltage.json")
        dfcurr                        = dp.pd.read_csv(current_fft_csv, header=None,index_col=None)
        dfvolt                        = dp.pd.read_csv(voltage_fft_csv, header=None,index_col=None)
        figure_list                   = []
        for i in range(len(dp.plt_title_list)):
            fig                   = dp.make_subplots(rows=1, cols=1,specs=[[{"secondary_y": True}]])
            current_idx_list      = [Current_headers.index(dp.plt_title_list[i][1])] if len(dp.plt_title_list[i])<5 else [ Current_headers.index(dp.plt_title_list[i][1]) , Current_headers.index(dp.plt_title_list[i][2])  ]
            voltage_idx_list      = [Voltage_headers.index(dp.plt_title_list[i][2])] if len(dp.plt_title_list[i])<5 else [ Voltage_headers.index(dp.plt_title_list[i][3]) , Voltage_headers.index(dp.plt_title_list[i][4])  ]

            current_titles        = [dp.plt_title_list[i][1]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][1] , dp.plt_title_list[i][2]  ]
            voltage_titles        = [dp.plt_title_list[i][2]] if len(dp.plt_title_list[i])<5 else [dp.plt_title_list[i][3] , dp.plt_title_list[i][4]  ]

            if dp.JSON['FFT'] :
                for c, name in enumerate(current_titles):
                    fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfcurr.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), current_idx_list[c]], name=name), row=1, col=1,secondary_y=False)
                for j, name in enumerate(voltage_titles):
                    fig.add_trace(dp.go.Bar(x=dp.harmonics, y=dfvolt.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), voltage_idx_list[j]], name=name), row=1, col=1,secondary_y=True)
            else:
                    return []
            fig.update_layout(
                title           =   f'FFT Magnitudes - {dp.plt_title_list[i][0]}',
                xaxis_title     =   'Harmonic Orders',
                xaxis           =   dict (
                                            tickvals = dp.harmonics ,
                                            ticktext = dp.harmonics
                                        ),
                yaxis           =   dict(
                                    side        = "left"                            ,
                                    title       = "Current Magnitude"                   ,
                                    titlefont   = dict(color="#1f77b4")             ,
                                    tickfont    = dict(color="#1f77b4")
                                ),
                yaxis2          =   dict(
                                    side="right"                                    ,
                                    title="Voltage Magnitude"                           ,
                                    titlefont=dict(color="#1f77b4")                 ,
                                    tickfont=dict(color="#1f77b4")                  ,
                                ),
                plot_bgcolor    =   '#f8fafd'             ,
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
        include_plotlyjs          = 'cdn'
        headers                   = self.return_headers( (dp.os.getcwd()).replace("\\","/") + f"/Script/assets/HEADER_FILES/{FFT_file}")
        df                        = dp.pd.read_csv(csv_path, header=None,index_col=None)
        figure_list               = []
        num_iterations            = df.shape[0] // len(dp.harmonics)
        for column in range(df.shape[1]):
            fig                   = dp.go.Figure()
            for iteration in range(num_iterations):
                iteration_data    = df.iloc[iteration * len(dp.harmonics): (iteration + 1) * len(dp.harmonics), column]
                fig.add_trace(
                    dp.go.Bar(
                            x     =   dp.harmonics,
                            y     =   iteration_data,
                            name  =   f'{headers[column]} {title} : Iteration {iteration + 1}'
                        )
                    )
            fig.update_layout(
                title           =   f'FFT Magnitudes - {headers[column]}',
                showlegend      =   True                                 ,
                xaxis_title     =   'Harmonic Orders',
                yaxis_title     =   'Magnitude',
                xaxis           =   dict (
                                            tickvals = dp.harmonics ,
                                            ticktext = dp.harmonics
                                        ),
                barmode         =   'stack'
            )
            figure_list.append(fig)

            #!-----------------------------------------------------------------------------------
            #* The include_plotlyjs="cdn" parameter causes a script tag to be included in the HTML output that references the Plotly CDN ("content delivery network").
            #* This offloads the work of providing the necessary javascript from your server to a more scalable one. A browser will typically cache this making subsequent
            #* page loads faster.
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

        if auto_open:
            import pathlib, webbrowser
            uri = pathlib.Path(html_path).absolute().as_uri()
            webbrowser.open(uri)

    def auto_plot(self,simutil,fileLog,misc,open=False,iterReport=False):
        """
        Generates an HTML report containing multiple plots.

        Args:
            misc (object)               : Miscellaneous object containing utility functions.
            Open (bool, optional)       : If True, open the generated HTML report automatically. Defaults to False.
            iterReport (bool, optional) : If True, generate iterations HTML report. Defaults to False.
        """
        misc.tic()
        ResDir          =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"
        MAPS_dir        =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"
        FFT_curr_path   =   MAPS_dir+"/FFT_Current_Map.csv"
        FFT_volt_path   =   MAPS_dir+"/FFT_Voltage_Map.csv"
        c               =   0
        file_list       =   fileLog.natsort_files(ResDir)
        legend          = True if dp.JSON['TF_Config'] == 'DCDC_D' else False
        if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':
            simutil.postProcessing.drop_Extra_Cols(FFT_curr_path,dp.idx_start,dp.idx_end)
        if iterReport:
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Currents'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ A ]" ,"Currents",open)
            self.gen_iter_report( ResDir , dp.pmap_multi['Peak_Voltages'] , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc,"[ V ]" ,"Voltages",open)
        if iterReport and dp.JSON['FFT']:
            self.fft_gen_iter_report( "FFT_Current.json", " Currents_FFT" ,FFT_curr_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc  ,"Currents_FFT" ,open)
            self.fft_gen_iter_report( "FFT_Voltage.json", "Voltages_FFT" ,FFT_volt_path , fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_"  + self.utc  ,"Voltages_FFT" ,open)

        for x  in range(len(file_list)):
            FFT_figs                =   self.fft_bar_plot(FFT_curr_path,FFT_volt_path,x)
            figures_list            =   self.plot_scopes(file_list[x],dp.pmap_plt,Legend=legend)
            figures_list_           =   self.shuffle_lists(figures_list,FFT_figs)
            if dp.JSON['TF_Config'] == 'DCDC_S' or 'DCDC_D':
                simutil.postProcessing.drop_Extra_Cols(file_list[x],sum(dp.Y_list[0:3]),sum(dp.Y_list[0:4])) # drop uneeded columns from the csv file.
                figures_list_ctrl   =   self.plot_scopes(file_list[x],dp.pmap_plt_ctrl,Legend=True)
                figures_list_.extend(figures_list_ctrl)
            c+=1
            self.append_to_html(file_list[x] , figures_list_,fileLog.resultfolder + "/HTML_REPORTS" + "/HTML_REPORT_" + self.utc + "_" + str(c) + ".html", auto_open=open , i=c-1)
            self.constants_list,self.constants_vals,self.constants_units,figures_list_  = [],[],[],[]
        fileLog.log("--------------------------------------------------------------------------------------------------------------------------")
        fileLog.log(f"Generating HTML Report    {'= '.rjust(49+17, ' ')}{str(misc.toc())} seconds.\n")
        file_list.clear()

    def generate_combinations(self, var1, var2, matrix,startpoint,pattern):

             '''
             This Function generates all necessary combinations depending on the variables chosen by the user.

             Args:
                 var1                  (list)        : The first variable.
                 var2                  (list or None): The second variable. Pass None if only one variable is desired.
                 matrix                (list)        : Matrix containing the ten dimensions.

             Returns:
                 result                (list)        : List of all possible combinations.
                 constant_combinations (list)        : List of constant combinations.
                 variable_indices      (list)        : List that contains indices of the variables choosen by the user.
                 const_index           (list)        : List that contains inices of the constants.

             '''
             postProcessing  =	  dp.PP.Processing()

             if pattern == True :
                 # Get the indices of the variables in the matrix
                 variable_indices = []
                 if var1 is not None:
                     variable_indices.append(matrix.index(var1))
                 if var2 is not None:
                     variable_indices.append(matrix.index(var2))

                 # Get the indices of the constants in the matrix
                 constant_indices = list(set(range(len(matrix))) - set(variable_indices))

                 # Get the indices of the constants that are zero
                 zero_indices = [idx for idx in constant_indices if len(matrix[idx]) == 1 and matrix[idx][0] == 0]

                 # Get index of constants in the matrix that doesn't have a single element equal to zero
                 const_index =  [i for i in constant_indices if i not in zero_indices]

                 # Create a list to store the possible values for each list
                 list_values = [[] for _ in range(len(const_index))]
                 for i, idx in enumerate(const_index):
                     for j in range(len(matrix[idx])):
                         # Append the possible value to the list
                         list_values[i].append(matrix[idx][j])

                 result = []
                 list_combinations = []
                 # Iterate over all possible combinations of list values
                 for lists in dp.itertools.product(*list_values):
                     list_combinations.append(lists)
                     # Iterate over all possible combinations of variable indices
                     for indices in dp.itertools.product(*(range(len(matrix[var_idx])) for var_idx in variable_indices)):
                         combination = []
                         # Iterate over all indices in the matrix
                         for idx in range(len(matrix)):
                             # If the index is a variable, append the corresponding value from the matrix using the variable indices
                             if idx in variable_indices:
                                 var_idx = variable_indices.index(idx)
                                 combination.append(matrix[idx][indices[var_idx]])
                             # If the index is in zero_indices, append 0
                             elif idx in zero_indices:
                                 combination.append(0)
                             else:
                                 # If the index is a list, append the corresponding value from the lists using the list indices
                                 list_idx = const_index.index(idx)
                                 combination.append(lists[list_idx])
                         result.append(combination)

                 return result, list_combinations, variable_indices,const_index
             else:
                 x,_=postProcessing.findIndex(startpoint,matrix,False)
                 # Get all possible combinations
                 combinations = postProcessing.findStart(matrix,x,False)

                 return combinations

    def subplots_3D (self,dict_name, column_name, col_idx, path, var1, var2, matrix,startpoint, Dimension_Names,pattern):

        '''
        This Function generate 3D plots.

        Args:
            dict_name        ( String )            : Name of dictionary in plecs_mapping file.
            column_name      ( String )            : Name of the column which is the key of mappig dict.
            col_idx          ( Int )               : the column index which is the value of mappig dict.
            var1             ( List )              : The first Variable.
            var2             ( List )              : The second Variable.
            matrix           ( List )              : Matrix contains the ten dimensions.
            Dimension_Names  ( List )              : List contains the ten dimennsions names.

            Return:
            figures_list ( List )                  : List contains all figures.

        '''

        df            = dp.pd.read_csv(path, header=None, index_col=None)
        postProcessing  =	  dp.PP.Processing()
        # Define The Parula colorscale
        parula_colors = [
            [0.0, 'rgb(53,42,135)'  ],
            [0.1, 'rgb(15,92,221)'  ],
            [0.2, 'rgb(18,125,216)' ],
            [0.3, 'rgb(7,156,207)'  ],
            [0.4, 'rgb(21,177,180)' ],
            [0.5, 'rgb(89,189,140)' ],
            [0.6, 'rgb(165,190,107)'],
            [0.7, 'rgb(225,185,82)' ],
            [0.8, 'rgb(252,206,46)' ],
            [0.9, 'rgb(249,251,14)' ],
            [1.0, 'rgb(234,248,31)' ]
        ]
        figures_list = []
        n            = len(var1) * len(var2)
        data         = []
        X, Y         = dp.np.meshgrid(var2, var1)
        if pattern == True:
            # Iterate through all combinations
            result, list_combinations, var_indices, const_indices = self.generate_combinations(var1, var2, matrix,startpoint,pattern)
            for i in range(0, len(result), len(var2) * len(var1)):
                k = result[i:i + len(var2) * len(var1)]
                # Retreive the corresponding data from the dataframe and append to z
                for j in range(len(k)):
                    _, w = postProcessing.findIndex(k[j], matrix)
                    w = df.iloc[w, col_idx]
                    data.append(round(w,5))

            for p in range(0, len(data), n):
                title_str = ''
                for i in range(len(const_indices)):
                    title_str += f'{Dimension_Names[const_indices[i]]} = {str(list_combinations[p//n][i])}<br>'
                fig_title = f"{title_str}"
                plot = dp.go.Surface(
                    z=list(dp.chunked(data[p:p + n], len(var2))),
                    x=X,
                    y=Y,
                    colorscale=parula_colors
                )
                plot.colorbar.len = 0.8
                fig = dp.go.Figure(plot)
                fig.update_layout(
                        title           ={
                            'text': dict_name + ':  ' + column_name + '  ' + '<br>' + fig_title,
                            'y': 0.95,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top',
                            'font': {
                                'family': 'Time New Roman',
                                'size': 20,
                                'color': '#0000EE'
                            }
                        },
                        margin          =   dict(   l=40, r=20, b=80, t=80)                ,
                        scene_camera    =   dict(   eye    = dict(x=2, y=2, z=1.25)        ,
                                                    center = dict(x=0,y=0,z=0)             ,
                                                    up     = dict(x=0,y=0,z=1)
                                                ),
                        scene           =   dict(
                                                    xaxis_title = Dimension_Names[var_indices[1]]   ,
                                                    yaxis_title = Dimension_Names[var_indices[0]]   ,
                                                    zaxis_title = column_name,
                                                    xaxis = dict(autorange='reversed'),
                                                    yaxis = dict(autorange='reversed')
                                                ),
                        # Make the plot responsive to screen sizes
                        autosize        =   True
                        )
                figures_list.append(fig)

        else:
            var1_index = matrix.index(var1)
            var2_index = matrix.index(var2)
            combinations = self.generate_combinations(var1,var2,matrix,startpoint,False)
            #Get Data from CSV file
            for j in range(len(combinations)):
                w = df.iloc[j,col_idx]
                data.append(round(w,5))

            nested_lists = [data[i:i+len(var1)] for i in range(0, len(data), len(var1))]
            for k in nested_lists:

                x_grid = dp.np.linspace(min(var1), max(var1), 100)
                y_grid = dp.np.linspace(min(var2), max(var2), 100)
                X_grid, Y_grid = dp.np.meshgrid(x_grid, y_grid)

                # Interpolate Z values using grid data
                from scipy.interpolate import griddata
                Z_grid = griddata((var1, var2), k, (X_grid, Y_grid))
                # Create a 3D surface plot
                fig = dp.go.Figure(data=[dp.go.Surface(x=X_grid, y=Y_grid, z=Z_grid)])

                # Set axis labels
                fig.update_layout(

                                    title           ={
                                        'text': dict_name + ':  ' + column_name ,
                                        'y': 0.95,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top',
                                        'font': {
                                            'family': 'Time New Roman',
                                            'size': 20,
                                            'color': '#0000EE'
                                        }
                                    },
                                    margin          =   dict(   l=40, r=20, b=80, t=80)                ,
                                    scene_camera    =   dict(   eye    = dict(x=2, y=2, z=1.25)        ,
                                                                center = dict(x=0,y=0,z=0)             ,
                                                                up     = dict(x=0,y=0,z=1)
                                                            ),
                                    scene           =   dict(
                                                                xaxis_title = Dimension_Names[var1_index]   ,
                                                                yaxis_title = Dimension_Names[var2_index]   ,
                                                                zaxis_title = column_name,
                                                                xaxis = dict(autorange='reversed'),
                                                                yaxis = dict(autorange='reversed')
                                                            ),
                                    # Make the plot responsive to screen sizes
                                    autosize        =   True )

                figures_list.append(fig)
        return figures_list

    def subplots_2D(self,dict_name,column_name, col_idx ,path, var1,matrix,startpoint,Dimension_Names,pattern):
        '''
        This Function generate all necessary combinations to plot 3D.

        Args:
            dict_name        ( String )            : Name of dictionnary in plecs_mapping file.
            column_name      ( String )            : Name of the column which is the key of mappig dict.
            col_idx          ( Int )               : Name of the column which is the value of mappig dict.
            path             ( String )            : Path of CSV files.
            var1             ( List )              : The X-axis choosen by the user.
            matrix           ( List )              : Matrix contains the ten dimensions.
            Dimension_Names  ( List )              : List contains the ten dimennsions names.
        Return:
            figures_list ( List )                  : List contains all figures.


        '''
        df = dp.pd.read_csv(path,header=None,index_col=None)
        postProcessing  =	  dp.PP.Processing()
        # X  = dp.np.array(var1)
        figures_list    =   []
        n = len(var1)
        data= []

        if (pattern == True) :
            # Iterate through all combinations
            result,list_combinations ,Variables_indices ,const_indices  = self.generate_combinations(var1,None,matrix,startpoint,True)
            for i in range(0,len(result),n):
                k = result[i:i+n]
            # Retreive the corresponding data from the dataframe and append to z
                for j in range(len(k)):
                    _,w =  postProcessing.findIndex(k[j],matrix)
                    w   = df.iloc[w,col_idx]
                    data.append(w)
            for p in range(0,len(data),n):
                title_str =''
                for i in range(len(Variables_indices)):
                    title_str += f'{Dimension_Names[const_indices[i]]} = {list_combinations[p//n][i]}<br>'
                fig_title = f"{title_str}"
                fig = dp.go.Figure(data = dp.go.Scatter(x=var1,y=data[p:p+n]))
                fig.update_layout(title={
                              'text' : dict_name +  ':  '  + column_name +  '  ' + '<br>'  + fig_title,
                              'y' : 0.95 ,
                              'x' : 0.5,
                              'xanchor':'center',
                              'yanchor' : 'top',
                              'font' : {
                                'family': 'Time New Roman',
                                'size': 20,
                                'color': '#0000EE'
                              }} ,
                              xaxis = dict(title = Dimension_Names[Variables_indices[0]],titlefont=dict(
                                family='Arial',
                                size=18,
                                color='black')),
                              yaxis = dict(title = column_name,titlefont=dict(
                                family='Arial',
                                size=18,
                                color='black')),


                              margin=dict(l=40, r=20, b=80, t=80))

                figures_list.append(fig)
        else:
            var1_index = self.matrix.index(var1)
            combinations = self.generate_combinations(var1,None,matrix,startpoint,False)
            #Get Data from CSV file
            for j in range(len(combinations)):
                w = df.iloc[j,col_idx]
                data.append(round(w,5))

            nested_lists = [data[i:i+len(var1)] for i in range(0, len(data), len(var1))]
            for k in nested_lists:

                fig = dp.go.Figure(data = dp.go.Scatter(x=var1,y=k))

                # Set axis labels
                fig.update_layout(

                                    title           ={
                                        'text': dict_name + ':  ' + column_name ,
                                        'y': 0.95,
                                        'x': 0.5,
                                        'xanchor': 'center',
                                        'yanchor': 'top',
                                        'font': {
                                            'family': 'Time New Roman',
                                            'size': 20,
                                            'color': '#0000EE'
                                        }
                                    },
                                    margin          =   dict(   l=40, r=20, b=80, t=80)                ,
                                    scene_camera    =   dict(   eye    = dict(x=2, y=2, z=1.25)        ,
                                                                center = dict(x=0,y=0,z=0)             ,
                                                                up     = dict(x=0,y=0,z=1)
                                                            ),
                                    scene           =   dict(
                                                                xaxis_title = Dimension_Names[var1_index]   ,
                                                                yaxis_title = column_name
                                                            ),
                                    # Make the plot responsive to screen sizes
                                    autosize        =   True )

                figures_list.append(fig)
        return figures_list

    def combine_figs_to_html(self,plotly_figs, html_fname, include_plotlyjs='cdn',separator=None, auto_open=False):
        """
        This function takes a list figures to combine them into an HTML file and open the file.
        Figures are displayed in separate div element side by side in rows ( rows : n , Columns : 2 )
        Args:
            plotly_figs ( list )        : list of plotly figures
            html_fname( string)         : name of HTML file
            include_plotlyjs ( string ) : string to specify how to include plotly.js library,
                                          default to 'cdn' so the library will be loaded from a CDN.
            separator ( string )        :  separator between figures.
            auto_open ( bool)           : open the html file in the browser automatically after saving.
        """
        separator                  =   "<html><body><hr style='height:1px;border:none;color:#333;background-color:#333;'></body></html>\n\n"
        date = str(dp.datetime.datetime.now().replace(microsecond=0))
        # Write the HTML body with the plot figures
        with open(html_fname, 'w') as f:
            f.write('<style>    .container  {position: relative;text-align: right;color: black;}                                            \
                                .Simulation {position: absolute;top: 10px;left: 16px;}                                                      \
                                .DateTime   {position: absolute;top: 50px;left: 16px;}                                                      \
                                .Sim_ID     {position: absolute;top: 90px;left: 16px;}                                                      \
                    </style>'                                                                                                               \
                    f'<div class="container">                                                                                               \
                                    <img src="data:image/png;base64,{self.image}"/>                                                         \
                                    <div class  =   "Simulation"><b> Simulation     :</b> {" ".rjust(60, " ")} {self.script_name}</div>     \
                                    <div class  =   "DateTime"> <b> Date & Time     :</b> {" ".rjust(60, " ")} {date} </div>                \
                                    <div class  =   "Sim_ID"> <b> Simulation ID     :</b> {" ".ljust(60, " ")} {self.utc}</div>             \
                    </div>')
            f.write(separator)
            f.write('<div style="display: flex; flex-wrap: wrap; justify-content: space-between;">\n')
            for fig in plotly_figs:
                f.write('<div style="display: inline-block; width: 49%; height: 680px;">\n')
                f.write(fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs))
                f.write('</div>\n')
            f.write('</div></body></html>\n')
        if auto_open:
            uri = dp.pathlib.Path(html_fname).absolute().as_uri()
            browser = dp.webbrowser.get()
            browser.open_new_tab(uri)

    def flatten(self,lst):
        '''
        This function takes a nested list as input and returns a flattened list.
        Args:
            lst       ( list )       : Nested list of plotly figures.
        Return:
            flatt_lst ( list )       : List Contains plotly figures for 2D or 3D plots.
        '''
        flatt__lst = []
        for item in lst:
            if isinstance(item, list):
                flatt__lst.extend(self.flatten(item))
            else:
                flatt__lst.append(item)
        return flatt__lst

    def plots_sweeps(self, var1, var2, matrix, Dimension_Names, separate_files=False):

            '''
            This function generates html file of  2D or 3D plots based on input variables

            Args:
                var1              ( list )        : The First variable plotted on the x-axis
                var2              ( List )        : The second variable plotted on the y-axis, if var2 is None a 2D plotted is generated
                matrix            ( List )        : Nested list contains the ten dimensions.
                Dimension_Names   ( List )        : List contains the Labels of the dimensions
                Seperate_files    ( Bool )        : A Boolean value indicating whether the plots should be saved to separate HTML files or no.

            '''
            ResDir      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"
            # ResDir      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name + "_"+self.utc+dp.suffix
            file_list   = []
            plots_list  = []

            zeros_indices = [i for i, x in enumerate(matrix) if len(x) == 1 and x[0] == 0]

            # Iterate over files in results directory and create a list of paths of CSV files that don't have all values equal to zero
            file_list = [str(filename.path.replace("\\","/")) for filename in dp.os.scandir(ResDir) if filename.is_file() and
                         filename.path.endswith('_Map.csv') and not all(val == '0' for val in next(dp.csv.reader(open(filename.path))))]

            # 3D plot condition
            if (var2 is not None) and (len(zeros_indices) < 8):
                for path in file_list:

                    for dict_name, mapping in dp.pmap.DCDC_Tofile_mapping_3D.items():
                        if dict_name in path:
                            mapping = dp.pmap.DCDC_Tofile_mapping_3D[dict_name]
                            for col_name, col_idx in mapping.items():
                                plots = self.subplots_3D(dict_name, col_name, col_idx, path, var1, var2, matrix, Dimension_Names)
                                plots_list.append(plots)
                                if separate_files:
                                    # Get the dict name and column name from the path to generate a unique filename for each HTML file
                                    html_file_name = dict_name + '_' + col_name + '_' + path.split('/')[-1].split('_')[0] + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list),ResDir + "/" + html_file_name)
                                    plots_list = []  # Clear the plots_list after generating the HTML file
                            if not separate_files:
                                # Get the dict name from the path to generate a single HTML file for all columns
                                html_file_name = dict_name + '_' + path.split('/')[-1].split('_')[0] + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" +html_file_name)
                                plots_list = []  # Clear the plots_list after generating the HTML file

            # 2D plot condition
            elif (len(zeros_indices) == 8):
                for path in file_list:
                    for dict_name, mapping in dp.pmap.DCDC_Tofile_mapping_3D.items():
                        if dict_name in path:
                            mapping = dp.pmap.DCDC_Tofile_mapping_3D[dict_name]
                            for col_name, col_idx in mapping.items():
                                plots = self.subplots_2D(dict_name, col_name, col_idx, path, var1, matrix, Dimension_Names)
                                plots_list.append(plots)
                                if separate_files:
                                    # Get the dict name and column name from the path to generate a unique filename for each HTML file
                                    html_file_name = dict_name + '_' + col_name + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list),ResDir + "/" + html_file_name)
                                    plots_list = []  # Clear the plots_list after generating the HTML file
                            if not separate_files:
                                # Get the dict name from the path to generate a single HTML file for all columns
                                html_file_name = dict_name + '_' + path.split('/')[-1].split('_')[0] + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                plots_list = []

    def plots_sweeps_Standalone(self, var1, var2, matrix,  Dimension_Names,  mapping, path = '', utc=None, dictionaries=[], separate_files=False):
        '''
        This function generates 2D or 3D plots based on input variables

        Args:
                  var1              (list)    : The First variable plotted on the x-axis
                  var2              (list)    : The second variable plotted on the y-axis, if var2 is None a 2D plot is generated
                  matrix            (list)    : Nested list containing the ten dimensions.
                  Dimension_Names   (list)    : List containing the Labels of the dimensions
                  mapping           (dict)    : Mapping Dictionary for CSV columns.
                  path              (str)     : Path to the directory containing CSV files.
                  utc               (int)     : UTC value (required when plotting from a single CSV file)
                  dictionaries      (list)    : List containing names of sub-dicts (required for multiple CSV files)
                  separate_files    (bool)    : A boolean value indicating whether the plots should be saved to separate HTML files or not.
        '''
        file_list  = []
        plots_list = []
        zeros_indices = [i for i, x in enumerate(matrix) if len(x) == 1 and x[0] == 0]
        if not dictionaries and (utc is None) :
            file_utc = dp.re.search(r'\d+', os.path.basename(path)).group()
            ResDir      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/Results_Standalone/" + f"results_{str(file_utc)}"
            dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
            # 3D plot condition
            if (var2 is not None) and (len(zeros_indices) < 8):
                for i in range(len(mapping)):
                    plots = self.subplots_3D(dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path.replace("\\","/")).group(1), mapping[i], i, path, var1, var2, matrix, Dimension_Names)
                    plots_list.append(plots)
                    if separate_files:
                        html_file_name = dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path).group(1) + '_' + mapping[i] + '_' + '.html'
                        self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                        plots_list = []
                if not separate_files:
                    html_file_name = dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path).group(1) + '.html'
                    self.combine_figs_to_html(self.flatten(plots_list), ResDir  + "/" + html_file_name)
                    plots_list = []

            # 2D plot condition
            elif (len(zeros_indices) == 8):
                for i in range(len(mapping)):
                    plots = self.subplots_2D(dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path.replace("\\","/")).group(1),mapping[i], i, path, var1,matrix, Dimension_Names)
                    plots_list.append(plots)
                    if separate_files:
                        html_file_name = dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path).group(1) + '_' + mapping[i] + '_' + '.html'
                        self.combine_figs_to_html(self.flatten(plots_list),ResDir + "/" + html_file_name)
                        plots_list = []
                if not separate_files:
                    html_file_name = dp.re.search(r'results_(?:.*?)_(.*?)_Map.csv', path).group(1) + '.html'
                    self.combine_figs_to_html(self.flatten(plots_list),ResDir + '/' +html_file_name)
                    plots_list = []
        else:
            folder = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res"
            file_list = [os.path.join(root, file).replace("\\","/") for root, _, files in os.walk(folder)
            for folder_name in files
            if str(utc) in folder_name
            for file in files if file.endswith('_Map.csv')]
            # 3D plot condition
            if (var2 is not None) and (len(zeros_indices) < 8):
                ResDir      =  (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/Results_Standalone/" + f"results_{str(utc)}"
                dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
                for csv_file in file_list:
                    for dict_name in dictionaries:
                        if dict_name in csv_file:
                            map = mapping[dict_name]
                            for col_name, col_idx in map.items():
                                plots = self.subplots_3D(dict_name, col_name, col_idx, csv_file, var1, var2, matrix, Dimension_Names)
                                plots_list.append(plots)
                                if separate_files:
                                    html_file_name = dict_name + '_' + col_name + '_' + csv_file.split('/')[-1].split('_')[0] + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                    plots_list = []
                            if not separate_files:
                                html_file_name = dict_name + '_' + csv_file.split('/')[-1].split('_')[0]  + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                plots_list = []

            # 2D plot condition
            elif (len(zeros_indices) == 8):
                ResDir      =  (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/Results_Standalone/" + f"results_{str(utc)}"
                dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
                for csv_file in file_list:
                    for dict_name in dictionaries:
                        if dict_name in csv_file:
                            map = mapping[dict_name]
                            for col_name, col_idx in mapping.items():
                                plots = self.subplots_2D(dict_name, col_name, col_idx, csv_file, var1, matrix, Dimension_Names)
                                plots_list.append(plots)
                                if separate_files:
                                    html_file_name = dict_name + '_' + col_name + '_' + csv_file.split('/')[-1].split('_')[0]  + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                    plots_list = []
                            if not separate_files:
                                html_file_name = dict_name + '_' + csv_file.split('/')[-1].split('_')[0] + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                plots_list = []

    def point_values(self,point,Map,matrix,path = '',utc = None, dict_names = []):
        """
         Retrieve values from CSV files based on a given point and mapping.

         Args:
             path          (str)           : The path to the CSV file(s) or directory containing CSV files.
             point         (tuple)         : The coordinates of the point to search for in the matrix.
             Map           (dict)          : A dictionary that maps column names to their corresponding indices in the CSV files.
             matrix        (list)          : The matrix containing the data.
             dict_names (list, optional)   : A list of dictionary names used to filter the CSV files. Defaults to an empty list.

         Returns:
             str: A string representation of the values found for the given point and mapping.

        """
        postProcessing  =	  dp.PP.Processing()
        _,idx = postProcessing.findIndex(point,matrix)
        values = []
        values_list = []
        if len(dict_names) == 0 and utc == None :
            file_utc = dp.re.search(r'\d+', os.path.basename(path)).group()
            ResDir      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/Results_Standalone/" + f"results_{str(file_utc)}"
            dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
            for i in range(len(Map)):
                df = dp.pd.read_csv(path.replace("\\","/"),header=None, index_col=None)
                values.append(df.iloc[idx,i])
                b = str(Map[i]).ljust(50)+'  :  ' + str(values[i]).ljust(20)
                values_list.append(b)
                # Join the list of 'b' values into a single string
                result = '\n\n'.join(values_list)
                # Writing the result to a text file
                with open(ResDir + "/" + "findpoint.txt", "w") as file:
                    file.write(result)
        else:
            ResDir      =  (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/" + f"results_{str(utc)}"
            dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
            folder      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res"
            file_list   = [os.path.join(root, file).replace("\\","/") for root, _, files in os.walk(folder)
                           for folder_name in files
                           if str(utc) in folder_name
                           for file in files if file.endswith('_Map.csv')]
            for i, csv_file in enumerate(file_list):
                if i!= 0:
                    values_list.append("-----------------------------------------------------------------------------------------------")  # Add separator
                for dict_name in dict_names:
                    if dict_name in csv_file:
                         values_list.append("Dictionary : " + dict_name)
                         df = dp.pd.read_csv(csv_file,header=None, index_col=None)
                         map = Map[dict_name]
                         for col_name, col_idx in map.items():
                            values.append(df.iloc[idx,col_idx])
                            b = str(col_name).ljust(50)+'  :  ' + str(values[-1]).ljust(20)
                            values_list.append(b)
                            values.pop()    # Remove the last appended value from 'values

                # Join the list of 'b' values into a single string
                result = '\n\n'.join(values_list)
                # Writing the result to a text file
                with open(ResDir +  f"/findpoint_{str(utc)}.txt", "w") as file:
                    file.write(result)
        return result

    def plots_sweeps_json(self):
        '''
        Generates 2D or 3D plots based on input variables.

        '''
        file_list  = []
        plots_list = []

        zeros_indices = [i for i, x in enumerate(self.matrix) if len(x) == 1 and x[0] == 0]
        folder_headers = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES"
        mapping_files = [os.path.join(folder_headers, file).replace("\\","/") for file in os.listdir(folder_headers) if file.endswith('.json')]
        mapping_base_filenames = [os.path.splitext(os.path.basename(file))[0] for file in mapping_files]

        if self.standalone == True and self.Folder_utc_csv  is  None:
            path            = self.data['path']
            path_base_filename = dp.os.path.splitext(os.path.basename(path))[0]
            ResDir      = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/Standalone/Results_Standalone/"
            dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
            # 3D plot condition
            if (self.variable_2 is not None )  and (len(zeros_indices) < 8):
                var2 = eval(self.data[self.data["Var2"]])
                for i in mapping_base_filenames:
                    if i in path_base_filename:
                        json_path = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/" + str(i) + ".json"
                        with open(json_path) as file:
                            map   =  dp.json.load(file)
                            for j in range(len(map)):
                                plots  = self.subplots_3D(i, map[j], j, path, self.var1, var2, self.matrix,self.startpoint, self.dimension_names,self.pattern)
                                plots_list.append(plots)
                                if self.separate_files:
                                    html_file_name = i + '_' + map[j] + '_' + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                    plots_list = []
                            if not self.separate_files:
                                html_file_name = i + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list), ResDir  + "/" + html_file_name)
                                plots_list = []

            # 2D plot condition
            elif (len(zeros_indices) == 8):
                for i in mapping_base_filenames:
                    if i in path_base_filename:
                        json_path = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/" + str(i) + ".json"
                        with open(json_path) as file:
                            map   =  dp.json.load(file)
                            for j in range(len(map)):
                                plots = self.subplots_2D(i,map[j], j, path, self.var1,self.matrix, self.startpoint,self.dimension_names,self.pattern)
                                plots_list.append(plots)
                                if self.separate_files:
                                    html_file_name = i + '_' + map[i] + '_' + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list),ResDir + "/" + html_file_name)
                                    plots_list = []
                            if not self.separate_files:
                                html_file_name = i + '.html'
                                self.combine_figs_to_html(self.flatten(plots_list),ResDir + '/' +html_file_name)
                                plots_list = []
        else:
            base_path = (dp.os.getcwd()).replace("\\", "/") + "/Script/" + "D".upper() + "ata/Res/"
            if self.standalone == True:
                for folder_name in os.listdir(base_path):
                    folder_path = os.path.join(base_path, folder_name)
                    if os.path.isdir(folder_path) and str(self.Folder_utc_csv) in folder_name:
                        folder = folder_path + "/CSV_MAPS/"
            else:
                folder = base_path + self.script_name + "_" + str(self.utc) +  "/CSV_MAPS/"
            file_list = [os.path.join(root, file).replace("\\", "/") for root, _, files in os.walk(folder)
                        for file in files if file.endswith('_Map.csv')  and not all(all(float(value) == 0
                        for value in row) for row in dp.csv.reader(open(os.path.join(root, file).replace("\\", "/"), 'r')))]
            # 3D plot condition
            if (self.variable_2 is not None) and (len(zeros_indices) < 8):
                var2 = eval(self.data[self.data["Var2"]])

                ResDir      = base_path + "Standalone/Results_Standalone/" + f"results_{str(self.Folder_utc_csv)}" if self.standalone == True else base_path + self.script_name + "_" + str(self.utc) +  "/HTML_REPORTS/" +f"results_{str(self.utc)}"
                dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
                for csv_file in file_list:
                    for i in mapping_base_filenames:
                        if i in csv_file:
                            json_path = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/" + str(i) + ".json"
                            with open(json_path) as file:
                                map   =  dp.json.load(file)
                                for j in range(len(map)):
                                    plots = self.subplots_3D(i, map[j], j, csv_file, self.var1, var2, self.matrix,self.startpoint, self.dimension_names,self.pattern)
                                    plots_list.append(plots)
                                    if self.separate_files:
                                        if self.standalone ==True :
                                            html_file_name = i.replace("_Map.csv","") + "_"+ map[j] + f"_{str(self.Folder_utc_csv)}" + '.html'
                                        else:
                                            html_file_name = i.replace("_Map.csv","") +"_"+ map[j] + '.html'
                                        self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                        plots_list = []
                                if not self.separate_files:
                                    if self.standalone ==True :
                                        html_file_name = i.replace("_Map.csv","") + f"_{str(self.Folder_utc_csv)}" + '.html'
                                    else:
                                        html_file_name = i.replace("_Map.csv","") + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                    plots_list = []

            # 2D plot condition
            elif (len(zeros_indices) == 8):
                base_path = (dp.os.getcwd()).replace("\\", "/") + "/Script/" + "D".upper() + "ata/Res/"
                ResDir      = base_path + "Standalone/Results_Standalone/" + f"results_{str(self.Folder_utc_csv)}" if self.standalone == True else base_path + self.script_name + "_" + str(self.utc) +  "/HTML_REPORTS/" +f"results_{str(self.utc)}"
                dp.os.makedirs(ResDir) if not dp.os.path.exists(ResDir) else None
                for csv_file in file_list:
                    for i in mapping_base_filenames:
                        if i in csv_file:
                            json_path = (dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES/" + str(i) + ".json"
                            with open(json_path) as file:
                                map   =  dp.json.load(file)
                                for j in range(len(map)):
                                    plots = self.subplots_2D(i, map[j], j, csv_file, self.var1, self.matrix,self.startpoint, self.dimension_names,self.pattern)
                                    plots_list.append(plots)
                                    if self.separate_files:
                                        if self.standalone ==True :
                                            html_file_name = i.replace("_Map.csv","") + "_"+ map[j] + f"_{str(self.Folder_utc_csv)}" + '.html'
                                        else:
                                            html_file_name = i.replace("_Map.csv","") +"_"+ map[j] + '.html'
                                        self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                        plots_list = []
                                if not self.separate_files:
                                    if self.standalone ==True :
                                        html_file_name = i.replace("_Map.csv","") + f"_{str(self.Folder_utc_csv)}" + '.html'
                                    else:
                                        html_file_name = i.replace("_Map.csv","") + '.html'
                                    self.combine_figs_to_html(self.flatten(plots_list), ResDir + "/" + html_file_name)
                                    plots_list = []
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

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
        self.script_name                =   dp.scriptname
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
        with open(self.json_path) as f  :   self.data = dp.json.load(f)
        for i in range(1, 11)           :   setattr(self, f"X{i}", eval(self.data[f"X{i}"]))
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

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

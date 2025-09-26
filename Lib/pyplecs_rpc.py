
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                            ______   ______  _     _____ ____ ____        ____  ____   ____
#?                                           |  _ / / / /  _ /| |   | ____/ ___/ ___|      |  _ /|  _ / / ___|
#?                                           | |_) / V /| |_) | |   |  _|| |   /___ / _____| |_) | |_) | |
#?                                           |  __/ | | |  __/| |___| |__| |___ ___) |_____|  _ <|  __/| |___
#?                                           |_|    |_| |_|   |_____|_____/____|____/      |_| /_/_|    /____|
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1, os.getcwd() + '/Script/assets')
import Dependencies as dp

#Calling on Enviromment variables
for key in ["HTTP_PROXY", "HTTPS_PROXY"]:
    if key in list(dict(dp.os.environ).keys()):
        dp.os.environ.pop(key)

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class PlecsRPC:

    def __init__(self,url,port,mdlVars,slvOpts,anlOpts,METHOD="JSON") :
        """
        PlecsRPC Constructor to initialize global variables.

        Args:
            url         (string)        : Could be a local address, an ip adress  or a link : http//:127.0.0.1 for localhost.
            port        (string)        : Port to connect to the xmlrpc server over.
            path        (string)        : String leading to the path of the model.
            mdlVars     (dictionary)    : Dictionary to specify variable values.
            solverOpts  (dictionary)    : Dictionary to specify solver settings.
            METHOD      (string)        : RPC connection medium, XML or JSON.
        """

        self.url                        =   url                                  # Host Local address    : http://localhost
        self.port                       =   port                                 # Port to connect over  : exemple 61677, default is 1080
        self.mdlVars                    =   mdlVars                              # Assign Parameters Dictionary "Modelvars"
        self.slvOpts                    =   slvOpts                              # Assign Parameters Dictionary "SolverOpts"
        self.anlOpts                    =   anlOpts                              # Assign Parameters Dictionary "AnalysisOpts"
        self.OptStruct                  =   []                                   # Initialize simulation parameters vector
        self.METHOD			            =   METHOD				                 # Desired RPC connection medium. Default is JSON. Alternative is XML.
        self.command                    =   dp.command                           # Path to PLECS executable file
        self.path                       =   ''                                   # Path to the plecs model file

    def set_plecs_priority(self,PRIORITY):
        """
        Sets the priority level of the PLECS.exe process to the specified level.

        Args:
        - self: instance of the class that this method belongs to.
        - PRIORITY (string): The priority level to assign to the process. It can be 'HIGH', 'LOW' or 'NORMAL'.

        Returns: None
        - This method doesn't return any values.

        Description:
        - This method searches for all running processes in the system with the name 'PLECS.exe'.
        - Once the process is found, the method sets its priority level to the specified value.
        - If the specified priority is 'HIGH', the process priority will be set to 'HIGH_PRIORITY_CLASS'.
        - If the specified priority is 'LOW', the process priority will be set to 'BELOW_NORMAL_PRIORITY_CLASS'.
        - If the specified priority is 'NORMAL', the process priority will be set to 'NORMAL_PRIORITY_CLASS'.

        Exceptions:
        - This method can raise exceptions if the process is not found, or if there are permission issues while setting the process priority.

        Example Usage:
        - Set the priority of PLECS.exe process to HIGH:
            instance.set_plecs_priority('HIGH')
        """

        # search for the plecs process and set its priority
        # if the process is found set its priority accordingly
        # otherwise raise an exception 

        proc_iter       = dp.psutil.process_iter(attrs=["pid", "name"])
        for p in proc_iter:
            if p.info["name"] == "PLECS.exe":
                print (p.pid)
                proc = dp.psutil.Process(p.pid)
                if  PRIORITY == 'HIGH':
                    proc.nice(dp.psutil.HIGH_PRIORITY_CLASS)
                elif PRIORITY == 'LOW':
                    proc.nice(dp.psutil.BELOW_NORMAL_PRIORITY_CLASS)
                else:
                    proc.nice(dp.psutil.NORMAL_PRIORITY_CLASS)

    def open_plecs(self):
        """
        Opens the PLECS simulation software in HIGH priority mode.

        This function uses the subprocess module to execute the PLECS executable file. 
        The PLECS executable file path is specified in `self.command`. If the executable 
        file is found and can be executed, it is opened in HIGH priority mode using the 
        `ABOVE_NORMAL_PRIORITY_CLASS` flag from the psutil module.

        Parameters:
        -----------
        self : object
            The instance of the class containing the `open_plecs` method.

        Returns:
        --------
        None

        Raises:
        -------
        Exception : If the PLECS executable file cannot be found or executed.

        """

        # open plecs in high priority mode 
        # raise an exception if the plecs executable file is not found or cannot be executed

        try:
            pid = dp.subprocess.Popen([self.command], creationflags=dp.psutil.ABOVE_NORMAL_PRIORITY_CLASS).pid
        except Exception:
            print('Plecs opening problem',pid)

    def kill_plecs(self):
        """
        This function searches for a running process with the name "PLECS.exe"
        using the `psutil` module and kills the process.

        Parameters:
        -----------
        self : instance of a class
            An instance of a class that contains this method.
        """

        # search for the plecs process and kill it
        # if the process is found kill it
        # otherwise do nothing

        proc_iter = dp.psutil.process_iter(attrs=["pid", "name"])
        for p in proc_iter:
            if p.info["name"] == "PLECS.exe":
                print (p.pid)
                p.kill()

    def get_plecs_cpu(self):
        """
        This method returns the CPU max usage of the PLECS.exe process running on the system.

        Returns:
            Tuple: A tuple containing two values.
                The first value is an integer representing the CPU usage percentage.
                The second value is an integer representing the number of CPU cores that can execute the PLECS.exe process.
        """
        
        # search for the plecs process and get its cpu usage
        # if the process is found return its cpu usage and the number of cpu cores that can execute it

        proc_iter   = dp.psutil.process_iter(attrs=["pid", "name"])
        cpu_usage   = None
        for p in proc_iter:
            if p.info["name"] == "PLECS.exe":
                cpu_usage = p.cpu_percent(interval=2)
                try:
                    cores = len(p.cpu_affinity())
                except dp.psutil.AccessDenied:
                    cores = 0
        return cpu_usage,cores

    def optStruct(self,instances=1,iteration_range=[0],parallel=False):
        """
        Reconstructs the simstruct for the model
        based on the modelvar and solveropt dictionaries
        passed in from the local dependecies.

        Args:
            instances (int)       : Number of instances to be generated, default is 1.
            parallel  (bool)      : Flag to indicate if parallel simulations will be performed.
        """

        # if only one instance is required and parallel simulations are not needed
        # return a single dictionary containing the model variables, solver options, analysis options and name

        if (instances == 1 and not parallel):
            self.OptStruct  =   {'ModelVars':self.mdlVars, 'SolverOpts':self.slvOpts, 'AnalysisOpts':self.anlOpts, 'Name':'Iter_1'}
            return

        # if multiple instances are required or parallel simulations are needed
        # create a list of dictionaries containing the model variables, solver options, analysis options and name
        # each dictionary corresponds to one instance of the simulation 

        mdl_list        =   [dp.copy.deepcopy(self.mdlVars) for _ in range(instances)]
        slv_list        =   [dp.copy.deepcopy(self.slvOpts) for _ in range(instances)]
        anl_list        =   [dp.copy.deepcopy(self.anlOpts) for _ in range(instances)]
        nms_list        =   ["Iter_"+str(iteration_range[i]+1) for i in range(len(iteration_range))]
        self.OptStruct  =   [{'ModelVars':mdl_list[x],'SolverOpts':slv_list[x],'AnalysisOpts':anl_list[x], 'Name':nms_list[x]} for x in range(instances)]

    def PlecsConnect(self):
        """
        Establishes a connection to a Plecs simulation running on a remote server
        using either XML-RPC or JSON-RPC protocol.

        Args:
        - self: the current instance of the PlecsConnect class
            - url (str): the URL of the remote server running the Plecs simulation
            - port (str): the port number used for the XML-RPC or JSON-RPC connection
            - METHOD (str): the protocol used for the connection, either "XML" or "JSON"
            - server (object): the server object used for the XML-RPC or JSON-RPC connection

        Returns:
        - None
        """

        # set connection parameters 
        url           =   self.url
        port          =   self.port

        # import RPC module based on the desired connection method and
        # establish connection to the plecs server using the specified method
        # raise an exception if the connection cannot be established

        if self.METHOD == "JSON":
            self.server  = dp.jsonrpc_requests.Server(url + ":" + port)

        elif self.METHOD == "XML":
            self.server  = dp.xmlrpc.client.Server(url + ":" + port)

    def Open_Model(self,modelname):
        """
        this function takes the name of the model and searches for the
        corresponding Plecs model then opens it before the simulation.


        Args:
            modelname (string)       : The name of the plecs model.
        """

        # search for the plecs model in the current working directory and its subdirectories
        # if the model is found open it
        # otherwise print an error message and exit the program
        root_dir = os.getcwd()
        plecs_files = []
        for name in os.listdir(root_dir):
            if os.path.isdir(os.path.join(root_dir, name)):
                for file in os.listdir(os.path.join(root_dir, name)):
                    if os.path.isfile(os.path.join(root_dir, name, file)) and file.endswith('.plecs'):
                        plecs_files.append(file)
                    else:
                        if os.path.isdir(os.path.join(root_dir, name, file)):
                            for item in os.listdir(os.path.join(root_dir, name, file)):
                                if os.path.isfile(os.path.join(root_dir, name, file, item)) and item.endswith('.plecs'):
                                    plecs_files.append(item)

        # if the model is found open it
        # otherwise print an error message and exit the program                                    
        if modelname in plecs_files:
            for path in dp.glob.glob(f'{root_dir}/**/*.plecs', recursive=True):
                if modelname == path.split('\\')[-1]:
                    dp.cp_mdl = path
                    os.startfile(path)
        else:
            print("Check the model name Please")
            os._exit(0)

    def get_Absolute_Path(self,modelname):
        """
        This function allows us to take the absolute path of the model
        you want to simulate it.


             Args:
             modelname (string)       : The name of the plecs model.

        """
        # search for the plecs model in the current working directory and its subdirectories
        # if the model is found return its absolute path
        # otherwise return an empty string

        for folder, subfolders, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(".plecs") and file ==modelname:
                        path = os.path.realpath(os.path.join(folder, file))
        return path

    def get_Relative_path(self,Model):
        """
        Get the relative Path of the plecs model that you want to simulate it.

        Args:
        file_path (String)       : the path of the model.

        """

        # get the relative path of the plecs model
        # raise an exception if the path cannot be found

        try:
            file_path = (os.path.join(os.path.dirname(os.path.abspath(__file__)),Model)).replace("\\","/")
            return file_path
        except:
            print("Error")

    def LoadModel(self,path):
        """
        Loads the PLECS model file specified by the path.

        Parameters:
        -----------
        path : str
            A string that represents the path to the PLECS model file.

        Returns:
        --------
        If the path is valid and refers to a PLECS file, the model will be loaded over the XML-RPC server.
        Otherwise, it returns an error message.
        """

        # get the file extension of the path
        # if the path is valid and refers to a plecs file load it over the xmlrpc server
        # otherwise print an error message

        ext = dp.os.path.splitext(path)[-1].lower()
        if (path is not None) and (ext == ".plecs"):
            try :
                self.server.plecs.load(path)
            except Exception as e:
                return e
        else:
            print('Simulation Path is invalid or Empty')

    def LaunchSim(self,instances,path,parallel=False,callback=""):
        """
        Launches a simulation using the given path to the simulation model file.

        Args:
            path (str): The path to the simulation model file.

        Returns:
            dict: A dictionary containing the results of the simulation, including
                the time values and the corresponding simulated values.

        """
        # Extract the model name from the given path and launch the simulation
        # if only one instance is required and parallel simulations are not needed
        # launch the simulation without a callback function
        # otherwise, launch the simulation with a callback function

        SIM_NAME     =  os.path.split(path)
        modelname    =  (list(SIM_NAME)[-1]).split('.')[0]

        if (instances == 1 and not parallel):
            results =   self.server.plecs.simulate(modelname,self.OptStruct)
        else:
            results =   self.server.plecs.simulate(modelname,self.OptStruct,callback)

        return results

    def LaunchAnalysis(self,instances,path,analysisName,parallel=False,callback=""):
        """
        Interfaces with Plecs and launches the analysis.

        Args:
            path (str): the path to the Plecs simulation file to be analyzed.
            analysisName (str, optional): the name of the analysis to be launched. Defaults to 'Steady_State_Analysis'.

        Returns:
            Any: the results of the analysis, which may vary depending on the type of analysis.

        Raises:
            IOError: if the file specified by path cannot be found or read.
            ValueError: if the Plecs server is not connected or if the analysis name is invalid.
            PlecsError: if an error occurs while communicating with the Plecs server during the analysis.

        """

        # Extract the model name from the given path and launch the analysis
        # and if only one instance is required and parallel simulations are not needed
        # launch the analysis without a callback function
        # otherwise, launch the analysis with a callback function

        SIM_NAME     =  os.path.split(path)
        modelname    =  (list(SIM_NAME)[-1]).split('.')[0]

        if (instances == 1 and not parallel):
            results =   self.server.plecs.analyze(modelname,analysisName,self.OptStruct)
        else:
            results =   self.server.plecs.analyze(modelname,analysisName,self.OptStruct,callback)

        return results

    def CloseModel(self,path):
        """
        Close a PLECS model file.

        Args:
            path (str): The path to the PLECS model file that should be closed.

        Returns:
            None.

        Raises:
            None.
        """

        # Close the plecs model specified by the path over the xmlrpc server

        self.server.plecs.close(path)

    def ClearTrace(self, modelname, scopes):
        """
        Clears the traces for specified scopes in a given model.
        
        This function removes all existing trace data from the specified scopes
        in the model. It extracts the base model name by removing any file extension
        and attempts to clear traces for each scope. If any errors occur during
        the clearing process, they are silently ignored.
        
        Args:
            modelname (str): The name of the model, which may include a file extension.
            scopes (list): A list of scope names within the model whose traces should be cleared.
            
        Returns:
            None
        """

        # Extract the base model name by removing any file extension
        # Attempt to clear traces for each specified scope
        # Silently ignore any errors that occur during the clearing process

        modelname = (modelname.split('.'))[0]

        try:
            for scope in scopes:
                self.server.plecs.scope(modelname+'/'+scope, 'ClearTraces')
        except:
            pass


    def SaveTraces(self, modelname, scopes, path):
        """
        Saves trace data from specified scopes to a designated directory.
        
        This function exports trace data from the specified scopes to files in the
        given path. It creates a subdirectory named 'Scopes_Traces' and saves each
        scope's traces to individual files. Scope names with slashes are converted
        to underscores for filesystem compatibility.
        
        Args:
            modelname (str): The name of the model, which may include a file extension.
            scopes (list): A list of scope names within the model whose traces should be saved.
            path (str): The base directory path where the trace files will be saved.
            
        Returns:
            None
        """

        # Ensure the target directory exists
        # Create a subdirectory named 'Scopes_Traces' within the specified path
        # Extract the base model name by removing any file extension
        # Attempt to save traces for each specified scope to the designated directory
        # Silently ignore any errors that occur during the saving process

        modelname = (modelname.split('.'))[0]
        path = path + '/Scopes_Traces'

        try:
            for scope in scopes:
                self.server.plecs.scope(modelname+'/'+scope, 'SaveTraces', path+'/'+scope.replace("/", "_"))
        except:
            pass


    def holdTrace(self, modelname, scopes):
        """
        Holds (pauses) the tracing for specified scopes in a given model.
        
        This function pauses the data collection for the specified scopes in the model,
        maintaining the current trace data without clearing it. Useful for examining
        specific moments in a simulation without losing the captured data.
        
        Args:
            modelname (str): The name of the model, which may include a file extension.
            scopes (list): A list of scope names within the model whose tracing should be paused.
            
        Returns:
            None
        """
       
        # Extract the base model name by removing any file extension
        # Attempt to hold traces for each specified scope
        # Silently ignore any errors that occur during the process

        modelname = (modelname.split('.'))[0]

        try:
            for scope in scopes:
                self.server.plecs.scope(modelname+'/'+scope, 'HoldTrace')
        except:
            pass


    def holdTraceCallback(self, scopes):
        """
        Generates a callback script for holding traces of specified scopes.
        
        This function creates a PLECS callback script as a string that can be used
        to pause tracing for multiple scopes. The generated script contains commands
        to hold the trace for each specified scope.
        
        Args:
            scopes (list): A list of scope names for which the hold trace callback should be generated.
            
        Returns:
            str: A string containing the PLECS callback script with commands to hold traces
                for all specified scopes.
        """

        # Generate a PLECS callback script to hold traces for the specified scopes
        # Return the generated script as a string
        # Each scope will have a command to hold its trace

        callback = """"""

        for scope in scopes:
            callback = callback + f"plecs('scope', './{scope}', 'HoldTrace', name);"

        return callback

    def modelInit_path(self,modelname):
        """
        Call redundant functions/methods in a script.

        Args:
            obj (object)        : object from class pyplecs_rpc
            modelname (string)  : name of the plecs model to run
            misc (object)       : object from the class miscellaneous
        """

        # Open the plecs model and get its absolute path
        # raise an exception if the model cannot be found or opened

        self.Open_Model(modelname)
        self.path   =   self.get_Absolute_Path(modelname)

    def modelinit_opts(self,maxThreads=1,iteration_range=[0],parallel=False):
        """
        Initialize simulation options and prepare for parallel execution if enabled.
        
        This method configures the simulation environment by setting up thread structures
        for parallel processing, establishing connection to the PLECS model, and loading
        the model for simulation. It includes a brief delay to ensure proper initialization
        before attempting to connect.

        Args:
            maxThreads (int): Maximum number of threads to use for parallel simulation.
                            Defaults to 1 (sequential execution).
            iteration_range (list): Range of iterations to simulate. Defaults to [0].
            parallel (bool): Flag indicating whether to enable parallel execution.
                            Defaults to False.

        Returns: None
        """

        # Set up thread structures for parallel execution if enabled
        # Establish connection to the PLECS model
        # Load the PLECS model for simulation
        # Include a brief delay to ensure proper initialization before connecting
        
        self.optStruct(maxThreads,iteration_range,parallel)
        dp.time.sleep(5)
        self.PlecsConnect()
        self.LoadModel(self.path)

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
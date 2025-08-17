
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                                 
#?                                            ______   ______  _     _____ ____ ____        ____  ____   ____                                                                                                                                    
#?                                           |  _ / / / /  _ /| |   | ____/ ___/ ___|      |  _ /|  _ / / ___|                                                                                                                                  
#?                                           | |_) / V /| |_) | |   |  _|| |   /___ / _____| |_) | |_) | |                                                                                                                              
#?                                           |  __/ | | |  __/| |___| |__| |___ ___) |_____|  _ <|  __/| |___                                                                                                                                
#?                                           |_|    |_| |_|   |_____|_____/____|____/      |_| /_/_|    /____|                                                                                                                                  
#?                                                                                                                                                                                                                                                
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                                               
#?                                                                                                                                                                                                                                                

# This Script works as a library containing All Necessary functions used generically                                                                                                                                                        
# by all other Scripts to conduct automated Simulation in PLECS environement over xml-RPC local connection.                                                                                                                                

import os,sys                                                                                                                                                                                                                                    
sys.path.insert(1, os.getcwd() + '/Script/assets')                                                                                                                                                                                   
import Dependencies as dp                                                                                                                                                                                                               

#Calling on Enviromment variables                                                                                                                                                                                                              
for key in ["HTTP_PROXY", "HTTPS_PROXY"]:                                                                                                                                                                                                
    if key in list(dict(dp.os.environ).keys()):                                                                                                                                                                                         
        dp.os.environ.pop(key)                                                                                                                                                                                                              
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
        self.command                    =   dp.command                                                                                                                                                                                               
        self.path                       =   ''                                                                                                                                                                                                       

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
        proc_iter       = dp.psutil.process_iter(attrs=["pid", "name"])                                                                                                                                                                                  # Get process iterator
        for p in proc_iter:                                                                                                                                                                                                                             # Iterate through processes
            if p.info["name"] == "PLECS.exe":                                                                                                                                                                                                           # Check if process is PLECS.exe
                print (p.pid)                                                                                                                                                                                                                           # Print process ID
                proc = dp.psutil.Process(p.pid)                                                                                                                                                                                                         # Get process object
                if  PRIORITY == 'HIGH':                                                                                                                                                                                                                # Check for HIGH priority
                    proc.nice(dp.psutil.HIGH_PRIORITY_CLASS)                                                                                                                                                                                            # Set high priority
                elif PRIORITY == 'LOW':                                                                                                                                                                                                                 # Check for LOW priority
                    proc.nice(dp.psutil.BELOW_NORMAL_PRIORITY_CLASS)                                                                                                                                                                                   # Set low priority
                else:                                                                                                                                                                                                                                   # Default case
                    proc.nice(dp.psutil.NORMAL_PRIORITY_CLASS)                                                                                                                                                                                          # Set normal priority

    def open_plecs(self):                                                                                                                                                                                                                               # Define open_plecs method
        """
        Opens the PLECS simulation software in HIGH priority mode.

        This function uses the subprocess module to execute the PLECS executable file. The PLECS executable file path is 
        specified in `self.command`. If the executable file is found and can be executed, it is opened in HIGH priority 
        mode using the `ABOVE_NORMAL_PRIORITY_CLASS` flag from the psutil module.

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

        Examples:
        ---------
        >>> my_sim = Simulation()
        >>> my_sim.open_plecs()
        """
        try:                                                                                                                                                                                                                                            # Try block
            pid = dp.subprocess.Popen([self.command], creationflags=dp.psutil.ABOVE_NORMAL_PRIORITY_CLASS).pid                                                                                                                                          # Open PLECS with high priority
        except Exception:                                                                                                                                                                                                                               # Exception handling
            print('Plecs opening problem',pid)                                                                                                                                                                                                          # Print error message

    def kill_plecs(self):                                                                                                                                                                                                                               # Define kill_plecs method
        """
        This function searches for a running process with the name "PLECS.exe"
        using the `psutil` module and kills the process.

        Parameters:
        -----------
        self : instance of a class
            An instance of a class that contains this method.
        """
        proc_iter = dp.psutil.process_iter(attrs=["pid", "name"])                                                                                                                                                                                       # Get process iterator
        for p in proc_iter:                                                                                                                                                                                                                             # Iterate through processes
            if p.info["name"] == "PLECS.exe":                                                                                                                                                                                                           # Check if process is PLECS.exe
                print (p.pid)                                                                                                                                                                                                                           # Print process ID
                p.kill()                                                                                                                                                                                                                                # Kill the process

    def get_plecs_cpu(self):                                                                                                                                                                                                                            # Define get_plecs_cpu method
        """
        This method returns the CPU max usage of the PLECS.exe process running on the system.

        Returns:
            Tuple: A tuple containing two values.
                The first value is an integer representing the CPU usage percentage.
                The second value is an integer representing the number of CPU cores that can execute the PLECS.exe process.
        """
        proc_iter   = dp.psutil.process_iter(attrs=["pid", "name"])                                                                                                                                                                                    # Get process iterator
        cpu_usage   = None                                                                                                                                                                                                                              # Initialize cpu_usage
        for p in proc_iter:                                                                                                                                                                                                                             # Iterate through processes
            if p.info["name"] == "PLECS.exe":                                                                                                                                                                                                           # Check if process is PLECS.exe
                cpu_usage = p.cpu_percent(interval=2)                                                                                                                                                                                                   # Get CPU usage
                try:                                                                                                                                                                                                                                    # Try block
                    # get the number of CPU cores that can execute this process
                    cores = len(p.cpu_affinity())                                                                                                                                                                                                       # Get CPU affinity cores
                except dp.psutil.AccessDenied:                                                                                                                                                                                                          # Handle access denied
                    cores = 0                                                                                                                                                                                                                           # Set cores to 0
        return cpu_usage,cores                                                                                                                                                                                                                          # Return CPU usage and cores

    def optStruct(self,instances=1,iteration_range=[0],parallel=False):                                                                                                                                                                                # Define optStruct method
        """
        Reconstructs the simstruct for the model
        based on the modelvar and solveropt dictionaries
        passed in from the local dependecies.

        Args:
            instances (int)       : Number of instances to be generated, default is 1.
            parallel  (bool)      : Flag to indicate if parallel simulations will be performed.
        """
        if (instances == 1 and not parallel):                                                                                                                                                                                                           # Check for single instance
            self.OptStruct  =   {'ModelVars':self.mdlVars, 'SolverOpts':self.slvOpts, 'AnalysisOpts':self.anlOpts, 'Name':'Iter_1'}                                                                                                                    # Create single instance structure
            return                                                                                                                                                                                                                                      # Return early

        mdl_list        =   [dp.copy.deepcopy(self.mdlVars) for _ in range(instances)]                                                                                                                                                                 # Create model vars list
        slv_list        =   [dp.copy.deepcopy(self.slvOpts) for _ in range(instances)]                                                                                                                                                                 # Create solver opts list
        anl_list        =   [dp.copy.deepcopy(self.anlOpts) for _ in range(instances)]                                                                                                                                                                 # Create analysis opts list
        nms_list        =   ["Iter_"+str(iteration_range[i]+1) for i in range(len(iteration_range))]                                                                                                                                                   # Create names list
        self.OptStruct  =   [{'ModelVars':mdl_list[x],'SolverOpts':slv_list[x],'AnalysisOpts':anl_list[x], 'Name':nms_list[x]} for x in range(instances)]                                                                                             # Create option structure list

    def PlecsConnect(self):                                                                                                                                                                                                                             # Define PlecsConnect method
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
        url           =   self.url                                                                                                                                                                                                                     # Get URL
        port          =   self.port                                                                                                                                                                                                                     # Get port

        # import RPC module
        if self.METHOD == "JSON":                                                                                                                                                                                                                      # Check for JSON method
            self.server  = dp.jsonrpc_requests.Server(url + ":" + port)                                                                                                                                                                                # Create JSON-RPC server

        elif self.METHOD == "XML":                                                                                                                                                                                                                     # Check for XML method
            self.server  = dp.xmlrpc.client.Server(url + ":" + port)                                                                                                                                                                                   # Create XML-RPC server

    def Open_Model(self,modelname):                                                                                                                                                                                                                    # Define Open_Model method
        """
        this function takes the name of the model and searches for the
        corresponding Plecs model then opens it before the simulation.


        Args:
            modelname (string)       : The name of the plecs model.
        """

        root_dir = os.getcwd()                                                                                                                                                                                                                         # Get current working directory
        plecs_files = []                                                                                                                                                                                                                               # Initialize plecs files list
        for name in os.listdir(root_dir):                                                                                                                                                                                                               # Iterate through root directory
            if os.path.isdir(os.path.join(root_dir, name)):                                                                                                                                                                                            # Check if item is directory
                for file in os.listdir(os.path.join(root_dir, name)):                                                                                                                                                                                  # Iterate through directory
                    if os.path.isfile(os.path.join(root_dir, name, file)) and file.endswith('.plecs'):                                                                                                                                                 # Check if file is PLECS file
                        plecs_files.append(file)                                                                                                                                                                                                        # Add to plecs files list
                    else:                                                                                                                                                                                                                               # Else case
                        if os.path.isdir(os.path.join(root_dir, name, file)):                                                                                                                                                                           # Check if item is directory
                            for item in os.listdir(os.path.join(root_dir, name, file)):                                                                                                                                                                 # Iterate through subdirectory
                                if os.path.isfile(os.path.join(root_dir, name, file, item)) and item.endswith('.plecs'):                                                                                                                               # Check if file is PLECS file
                                    plecs_files.append(item)                                                                                                                                                                                           # Add to plecs files list
        if modelname in plecs_files:                                                                                                                                                                                                                   # Check if model exists
            for path in dp.glob.glob(f'{root_dir}/**/*.plecs', recursive=True):                                                                                                                                                                        # Search for PLECS files recursively
                if modelname == path.split('\\')[-1]:                                                                                                                                                                                                   # Check if filename matches
                    dp.cp_mdl = path                                                                                                                                                                                                                   # Set model path
                    os.startfile(path)                                                                                                                                                                                                                  # Open model file
        else:                                                                                                                                                                                                                                          # Else case
            print("Check the model name Please")                                                                                                                                                                                                        # Print error message
            os._exit(0)                                                                                                                                                                                                                                # Exit program

    def get_Absolute_Path(self,modelname):                                                                                                                                                                                                             # Define get_Absolute_Path method
        """
        This function allows us to take the absolute path of the model
        you want to simulate it.


             Args:
             modelname (string)       : The name of the plecs model.

        """

        for folder, subfolders, files in os.walk(os.getcwd()):                                                                                                                                                                                         # Walk through directory tree
            for file in files:                                                                                                                                                                                                                         # Iterate through files
                if file.endswith(".plecs") and file ==modelname:                                                                                                                                                                                       # Check if file is target model
                        path = os.path.realpath(os.path.join(folder, file))                                                                                                                                                                            # Get absolute path
        return path                                                                                                                                                                                                                                    # Return path

    def get_Relative_path(self,Model):                                                                                                                                                                                                                 # Define get_Relative_path method
        """
        Get the relative Path of the plecs model that you want to simulate it.

        Args:
        file_path (String)       : the path of the model.

        """
        try:                                                                                                                                                                                                                                            # Try block
            file_path = (os.path.join(os.path.dirname(os.path.abspath(__file__)),Model)).replace("\\","/")                                                                                                                                              # Get relative path
            return file_path                                                                                                                                                                                                                            # Return path
        except:                                                                                                                                                                                                                                        # Exception handling
            print("Error")                                                                                                                                                                                                                             # Print error message

    def LoadModel(self,path):                                                                                                                                                                                                                           # Define LoadModel method
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
        ext = dp.os.path.splitext(path)[-1].lower()                                                                                                                                                                                                    # Get file extension
        #test if the path is valid and it refers to a plecs file
        if (path is not None) and (ext == ".plecs"):                                                                                                                                                                                                   # Check valid PLECS path
            try :                                                                                                                                                                                                                                      # Try block
                #load the plecs model file over the xmlrpc server
                self.server.plecs.load(path)                                                                                                                                                                                                            # Load model
            #raise an error otherwise
            except Exception as e:                                                                                                                                                                                                                     # Exception handling
                # print(e)
                return e                                                                                                                                                                                                                               # Return error
        else:                                                                                                                                                                                                                                          # Else case
            print('Simulation Path is invalid or Empty')                                                                                                                                                                                               # Print error message

    def LaunchSim(self,instances,path,parallel=False,callback=""):                                                                                                                                                                                     # Define LaunchSim method
        """
        Launches a simulation using the given path to the simulation model file.

        Args:
            path (str): The path to the simulation model file.

        Returns:
            dict: A dictionary containing the results of the simulation, including
                the time values and the corresponding simulated values.

        """
        SIM_NAME     =  os.split(path)                                                                                                                                                                                                                 # Split path
        modelname    =  (list(SIM_NAME)[-1]).split('.')[0]                                                                                                                                                                                              # Get model name

        # launch plecs simulation
        # try:
        if (instances == 1 and not parallel):                                                                                                                                                                                                          # Check single instance
            results =   self.server.plecs.simulate(modelname,self.OptStruct)                                                                                                                                                                           # Run simulation
        else:                                                                                                                                                                                                                                          # Else case
            results =   self.server.plecs.simulate(modelname,self.OptStruct,callback)                                                                                                                                                                 # Run parallel simulation
        # except xmlrpc.client.Fault:
        #     results = {'time': [], 'Values': []}

        return results                                                                                                                                                                                                                                 # Return results

    def LaunchAnalysis(self,instances,path,analysisName,parallel=False,callback=""):                                                                                                                                                                   # Define LaunchAnalysis method
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
        SIM_NAME     =  os.split(path)                                                                                                                                                                                                                 # Split path
        modelname    =  (list(SIM_NAME)[-1]).split('.')[0]                                                                                                                                                                                              # Get model name

        if (instances == 1 and not parallel):                                                                                                                                                                                                          # Check single instance
            results =   self.server.plecs.analyze(modelname,analysisName,self.OptStruct)                                                                                                                                                              # Run analysis
        else:                                                                                                                                                                                                                                          # Else case
            results =   self.server.plecs.analyze(modelname,analysisName,self.OptStruct,callback)                                                                                                                                                    # Run parallel analysis

        return results                                                                                                                                                                                                                                 # Return results

    def CloseModel(self,path):                                                                                                                                                                                                                         # Define CloseModel method
        """
        Close a PLECS model file.

        Args:
            path (str): The path to the PLECS model file that should be closed.

        Returns:
            None.

        Raises:
            None.
        """
        # modelname   =   self.MODEL_NAME
        self.server.plecs.close(path)                                                                                                                                                                                                                   # Close model

    def ClearTrace(self, modelname, scopes):                                                                                                                                                                                                            # Define ClearTrace method
        """
        Clears the traces of specified scopes in the given PLECS model.

        Args:
            modelname (str): Name of the PLECS model (without extension)
            scopes (list): List of scope paths to clear traces from
        """
        modelname = (modelname.split('.'))[0]                                                                                                                                                                                                          # Remove file extension

        try:                                                                                                                                                                                                                                            # Try block
            for scope in scopes:                                                                                                                                                                                                                        # Iterate through scopes
                self.server.plecs.scope(modelname+'/'+scope, 'ClearTraces')                                                                                                                                                                            # Clear scope traces
        except:                                                                                                                                                                                                                                        # Exception handling
            pass                                                                                                                                                                                                                                       # Pass silently

    def SaveTraces(self, modelname, scopes, path):
        """
        Saves traces from specified scopes to the given path.

        Args:
            modelname (str): Name of the PLECS model (without extension)
            scopes (list): List of scope paths to save traces from
            path (str): Directory path where traces will be saved
        """
        modelname = (modelname.split('.'))[0]                                                                                                                                                   # Remove file extension
        path = path + '/Scopes_Traces'                                                                                                                                                          # Create traces path

        try:                                                                                                                                                                                    #
            for scope in scopes:                                                                                                                                                                # Iterate through scopes
                self.server.plecs.scope(modelname+'/'+scope, 'SaveTraces', path+'/'+scope.replace("/","_"))                                                                                     # Save scope traces
        except:                                                                                                                                                                                 # Exception handling
            pass                                                                                                                                                                                # Pass silently

    def holdTrace(self, modelname, scopes):
        """
        Holds traces of specified scopes in the given PLECS model.

        Args:
            modelname (str): Name of the PLECS model (without extension)
            scopes (list): List of scope paths to hold traces for
        """
        modelname = (modelname.split('.'))[0]                                                                                                                                                   # Remove file extension

        try:                                                                                                                                                                                    #                                                                                                                         
            for scope in scopes:                                                                                                                                                                # Iterate through scopes
                self.server.plecs.scope(modelname+'/'+scope, 'HoldTrace')                                                                                                                       # Hold scope traces
        except:                                                                                                                                                                                 # Exception handling
            pass                                                                                                                                                                                # Pass silently

    def holdTraceCallback(self, scopes):
        """
        Generates a callback string for holding traces of specified scopes.

        Args:
            scopes (list): List of scope paths to generate hold commands for

        Returns:
            str: JavaScript callback string for holding traces
        """
        callback = """"""                                                                                                                                                                       # Initialize callback string

        for scope in scopes:                                                                                                                                                                    # Iterate through scopes
            callback = callback + f"plecs('scope', './{scope}', 'HoldTrace', name);"                                                                                                            # Add hold command to callback

        return callback                                                                                                                                                                         # Return callback string

    def modelInit_path(self, modelname):
        """
        Initializes the model path by opening the model and getting its absolute path.

        Args:
            modelname (str): Name of the PLECS model file (with extension)
        """
        self.Open_Model(modelname)                                                                                                                                                              # Open the Corresponding PLECS model
        self.path = self.get_Absolute_Path(modelname)                                                                                                                                           # Set The Path of the Model in each Script

    def modelinit_opts(self, maxThreads=1, iteration_range=[0], parallel=False):                                                                                                                                                                        
        """
        Initializes simulation options and connects to PLECS.

        Args:
            maxThreads (int): Maximum number of threads for parallel simulation
            iteration_range (list): Range of iterations to perform
            parallel (bool): Whether to run in parallel mode
        """
        self.optStruct(maxThreads, iteration_range, parallel)                                                                                                                                   # generate a list of simstructs for multi-threaded simulation.
        dp.time.sleep(5)                                                                                                                                                                        # Sleep for 5 seconds
        self.PlecsConnect()                                                                                                                                                                     # Connect to the plecs model
        self.LoadModel(self.path)                                                                                                                                                               # Load model

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                       _____ _ _         _              _ _                      _                                                          # ASCII art header
#?                                      |  ___(_) | ___   / \   _ __   __| | |    ___   __ _  __ _(_)_ __   __ _                                              # ASCII art header
#?                                      | |_  | | |/ _ \ / _ \ | '_ \ / _` | |   / _ \ / _` |/ _` | | '_ \ / _` |                                             # ASCII art header
#?                                      |  _| | | |  __// ___ \| | | | (_| | |__| (_) | (_| | (_| | | | | | (_| |                                             # ASCII art header
#?                                      |_|   |_|_|\___/_/   \_\_| |_|\__,_|_____\___/ \__, |\__, |_|_| |_|\__, |                                             # ASCII art header
#?                                                                                     |___/ |___/         |___/                                              # ASCII art header
#?                                                                                                                                                           # ASCII art header
#?------------------------------------------------------------------------------------------------------------------------------------------------------------- # Section separator
import os,sys                                                                                                                                                  # Import OS and system modules
sys.path.insert(1,os.getcwd() + '/Script/assets')                                                                                                              # Add assets directory to path
import Dependencies as dp                                                                                                                                      # Import Dependencies module

#?------------------------------------------------------------------------------------------------------------------------------------------------------------- # Section separator
class FileAndLogging:                                                                                                                                          # Define FileAndLogging class
    def __init__(self, suffix="", json_dir=""):                                                                                                                # Initialize class instance
        self.utc                    =   str(int(dp.time.time()*1000))                                                                                          # Get current timestamp
        dp.suffix                   =   suffix                                                                                                                 # Set suffix
        self.ResultsPath            =   ""                                                                                                                     # Initialize results path
        self.basename               =   dp.os.path.basename(dp.sys.argv[0])[:-3]                                                                              # Get script basename
        self.resultfolder           =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/" + json_dir + "_" + self.utc + suffix       # Set result folder path
        self.logfolder              =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Log/" + json_dir                                  # Set log folder path
        self.jsonfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Json/" + json_dir                                # Set JSON folder path
        self.initfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/cmd/" + json_dir                                 # Set init folder path
        self.nested_res_hier        =   ''                                                                                                                    # Initialize nested hierarchy
        self.files                  =   [1]                                                                                                                   # Initialize files list

    def natsort_files(self,ResDir):                                                                                                                            # Define natsort_files method
        """                                                                                                                                                   # Docstring start
        Sorts out a list of files in a given directory in an alphanumeric way.                                                                                # Docstring description

        Args:                                                                                                                                                 # Args section
            ResDir (string): dircetory of files.                                                                                                              # Parameter description

        Returns:                                                                                                                                              # Returns section
            list: sorted list of files.                                                                                                                      # Return value description
        """                                                                                                                                                   # Docstring end
        file_list   =   []                                                                                                                                     # Initialize file list
        # iterate over files in results directory.                                                                                                            # Comment about iteration
        for filename in dp.os.scandir(ResDir):                                                                                                                # Loop through directory
            if filename.is_file() and filename.path.endswith('.csv') and not filename.path.endswith('_Map.csv'):                                              # Check file conditions
                file_list.append(str(filename.path.replace("\\","/")))                                                                                       # Add file to list
        file_list = dp.natsorted(file_list)                                                                                                                  # Natural sort the list
        return  file_list                                                                                                                                     # Return sorted list

    def results_folder(self):                                                                                                                                 # Define results_folder method
        """                                                                                                                                                   # Docstring start
        Create a folder for storing results and return the path.                                                                                             # Docstring description

        This function creates a folder in the specified path with a name                                                                                     # Detailed description
        that includes the current UTC date and time. If the folder already                                                                                   # Continued description
        exists, the function will raise an OSError. The function returns                                                                                    # Continued description
        the path to the results folder.                                                                                                                     # Continued description

        Returns:                                                                                                                                             # Returns section
        - ResultsPath (str) : The path to the results folder.                                                                                               # Return value description
        """                                                                                                                                                  # Docstring end
        try:                                                                                                                                                  # Start try block
            dp.os.makedirs(self.resultfolder , exist_ok = False)                                                                                            # Create results folder
            dp.os.makedirs(self.resultfolder+"/HTML_REPORTS", exist_ok = False)                                                                              # Create HTML reports folder
            dp.os.makedirs(self.resultfolder+"/CSV_MAPS", exist_ok = False)                                                                                 # Create CSV maps folder
            dp.os.makedirs(self.resultfolder+"/CSV_TIME_SERIES", exist_ok = False)                                                                          # Create time series folder
            dp.os.makedirs(self.resultfolder+"/Scopes_Traces", exist_ok = False)                                                                            # Create scopes traces folder

        except OSError:                                                                                                                                       # Handle OSError
            pass                                                                                                                                             # Ignore error

        ResultsPath     =   self.resultfolder +"/CSV_TIME_SERIES/" + "results" + "_" + self.utc + "_"                                                       # Set results path
        return ResultsPath                                                                                                                                    # Return results path

    def logging_folder(self):                                                                                                                                 # Define logging_folder method
        """                                                                                                                                                   # Docstring start
        Creates a log file in a specified folder and returns the path to the file.                                                                            # Docstring description

        Args:                                                                                                                                                 # Args section
        self (object): An instance of the class that this method is a member of.                                                                             # Parameter description

        Returns:                                                                                                                                              # Returns section
        str: The full path to the log file that was created.                                                                                                 # Return value description

        Raises:                                                                                                                                               # Raises section
        OSError: If the specified log folder already exists and the `exist_ok` flag is set to False.                                                         # Exception description

        """                                                                                                                                                   # Docstring end
        try:                                                                                                                                                  # Start try block
            # Attempt to create the specified log folder.                                                                                                    # Comment about folder creation
            # If the folder already exists, an OSError will be raised (unless exist_ok is True).                                                             # Comment about error handling
            dp.os.makedirs(self.logfolder, exist_ok = False)                                                                                                # Create log folder
        except OSError:                                                                                                                                       # Handle OSError
            # If the folder already exists, ignore the error and continue.                                                                                   # Comment about error handling
            pass                                                                                                                                             # Ignore error

        # Create a unique log file name based on the current UTC time.                                                                                       # Comment about file naming
        self.LogF_name = "log" + "_" + self.utc + ".log"                                                                                                    # Set log file name

        # Build the full path to the log file using the specified log folder and file name.                                                                  # Comment about path building
        LogFile = self.logfolder +"/" + self.LogF_name                                                                                                      # Set log file path

        # Return the full path to the log file.                                                                                                              # Comment about return value
        return LogFile                                                                                                                                       # Return log file path

    def log(self,msg):                                                                                                                                        # Define log method
        """                                                                                                                                                   # Docstring start
        Redirects all printed statements from consol to a specified file.                                                                                    # Docstring description

        Args:                                                                                                                                                 # Args section
            pathf (string)  : path of the file to save to.                                                                                                   # Parameter description
            msg (string)    : message to be logged to file.                                                                                                  # Parameter description
        """                                                                                                                                                   # Docstring end
        if dp.exists(self.LogFile):                                                                                                                          # Check if log file exists
            dp.sys.stdout  =   open(self.LogFile,'a')                                                                                                       # Open in append mode
        else :                                                                                                                                                # Else clause
            dp.sys.stdout  =   open(self.LogFile,'w+')                                                                                                      # Open in write mode
        print(msg)                                                                                                                                            # Print message
        dp.sys.stdout.close()                                                                                                                                # Close file
        sys.stdout = sys.__stdout__  # Restore stdout if needed                                                                                              # Restore stdout

    def json_input_folder(self):                                                                                                                              # Define json_input_folder method
        try:                                                                                                                                                  # Start try block
            # Attempt to create the specified log folder.If the folder already exists, an OSError will be raised (unless exist_ok is True).                  # Comment about folder creation
            dp.os.makedirs(self.jsonfolder, exist_ok = True)                                                                                                # Create JSON folder
            dp.os.makedirs(self.initfolder, exist_ok = True)                                                                                                # Create init folder

        except OSError:                                                                                                                                       # Handle OSError
            # If the folder already exists, ignore the error and continue.                                                                                   # Comment about error handling
            pass                                                                                                                                             # Ignore error

    def createFolders(self):                                                                                                                                  # Define createFolders method
        """                                                                                                                                                   # Docstring start
            Create two folders for storing results and log files, respectively.                                                                              # Docstring description

            Returns:                                                                                                                                         # Returns section
            None.                                                                                                                                            # Return value description

            Side Effects:                                                                                                                                     # Side effects section
            - Creates a folder with the name returned by the results_folder() function and sets it as the                                                    # Effect description
            value of the self.ResultsPath attribute.                                                                                                         # Continued description
            - Creates a folder with the name returned by the logging_folder() function and sets it as the                                                   # Effect description
            value of the self.LogFile attribute.                                                                                                             # Continued description

            Raises:                                                                                                                                           # Raises section
            - Any exception raised by the results_folder() or logging_folder() function.                                                                     # Exception description

            Notes:                                                                                                                                            # Notes section
            - This function assumes that the self.results_folder() and self.logging_folder() functions                                                       # Note about assumptions
            have already been implemented.                                                                                                                   # Continued note
            - The self.ResultsPath and self.LogFile attributes are assumed to be instance variables.                                                         # Note about attributes
            - This function does not return anything, but it has side effects that modify the state of the                                                   # Note about side effects
            object.                                                                                                                                          # Continued note
        """                                                                                                                                                   # Docstring end
        self.ResultsPath            =   self.results_folder()                                                                                                # Set results path
        self.LogFile                =   self.logging_folder()                                                                                                # Set log file path
        self.json_input_folder()                                                                                                                                 # Call json_input_folder

    def header(self):                                                                                                                                         # Define header method
        """                                                                                                                                                   # Docstring start
            Generates a header for the log file, consisting of a horizontal line,                                                                             # Docstring description
            a stylized "SIMULATION STARTED" message, and another horizontal line.                                                                            # Continued description

            Parameters:                                                                                                                                       # Parameters section
            self (object): The instance of the class calling this method.                                                                                    # Parameter description

            Returns:                                                                                                                                          # Returns section
            None                                                                                                                                             # Return value description

            Side Effects:                                                                                                                                     # Side effects section
            Writes to the log file using the instance's `log` method.                                                                                        # Effect description
        """                                                                                                                                                   # Docstring end
        self.log("--------------------------------------------------------------------------------------------------------------------------" )              # Log separator line
        self.log(dp.figlet_format("SIMULATION  STARTED",width=100))                                                                                          # Log start message
        self.log("--------------------------------------------------------------------------------------------------------------------------" )              # Log separator line

    def footer(self,simutil):                                                                                                                                 # Define footer method
        """                                                                                                                                                   # Docstring start
            Generates the footer for the log file, including the total simulation time, a message indicating that the simulation                               # Docstring description
            has ended, and a copy of all output files.                                                                                                        # Continued description

            Parameters:                                                                                                                                       # Parameters section
            -----------                                                                                                                                      # Section separator
            self: object                                                                                                                                     # Parameter description
                The instance of the class that calls this method.                                                                                            # Continued description

            Returns:                                                                                                                                         # Returns section
            --------                                                                                                                                        # Section separator
            None                                                                                                                                             # Return value description
        """                                                                                                                                                   # Docstring end
        self.log("--------------------------------------------------------------------------------------------------------------------------"    )           # Log separator line
        tf_sim  =   dp.time.time()                                                                                                                          # Get end time
        self.log(f"Total Simulation Time    {'= '.rjust(67, ' ')}{str((tf_sim-dp.tinit_sim).__round__(3)/60)} minutes."                          )           # Log simulation time
        self.log("--------------------------------------------------------------------------------------------------------------------------\n"  )           # Log separator line
        self.log(dp.figlet_format("SIMULATION  ENDED",width=100))                                                                                           # Log end message
        self.log("--------------------------------------------------------------------------------------------------------------------------"    )           # Log separator line
        if (dp.JSON['parallel']):                                                                                                                           # Check if parallel
            self.log(dp.figlet_format("SIMULATION  ITERATIONS",width=150))                                                                                  # Log iterations header
            self.log("--------------------------------------------------------------------------------------------------------------------------")           # Log separator line
            self.log(f"Iterations    {''.rjust(59, ' ')}{dp.JSON['sweepNames']}")                                                                           # Log iterations info
            self.log(f"Sweep Names   {''.rjust(59, ' ')}{dp.JSON['Dimension_Names']}")                                                                      # Log sweep names
            for i in range(len(simutil.Map)):                                                                                                               # Loop through map
                self.log(f"Iter{' '+str(i+1)}{''.rjust(68-len(str(i+1)), ' ')}{simutil.Map[i].tolist()}")                                                  # Log iteration details
        self.copyfiles()                                                                                                                                     # Call copyfiles

    def copyfiles(self):                                                                                                                                      # Define copyfiles method
        """                                                                                                                                                   # Docstring start
            Copies relevant files to the result folder.                                                                                                       # Docstring description

            This function copies the following files to the result folder:                                                                                   # Detailed description
                1. Log file specified by self.LogFile to the path resultfolder/self.LogF_name                                                                # File 1 description
                2. PLECS model specified by dp.cp_mdl to the path resultfolder/PLECS_MODEL_<filename>                                                       # File 2 description
                3. Script file specified by dp.script_path to the path resultfolder/<basename>.py                                                            # File 3 description
                4. The directory MyLibraries located at the current working directory to the path resultfolder/Plec_Lib                                      # File 4 description
                5. The file app.js located at the path <current working directory>/Script/assets/app.js to the path resultfolder/app.js                      # File 5 description

            Parameters:                                                                                                                                       # Parameters section
            -----------                                                                                                                                      # Section separator
            self : object                                                                                                                                    # Parameter description
                An instance of the class that this method belongs to.                                                                                        # Continued description

            Returns:                                                                                                                                         # Returns section
            --------                                                                                                                                        # Section separator
            None                                                                                                                                             # Return value description
        """                                                                                                                                                   # Docstring end
        dp.shutil.copy(self.LogFile, os.path.join(self.resultfolder, self.LogF_name))                                                                         # Copy log file
        dp.shutil.copy(dp.cp_mdl, self.resultfolder+"/" +"PLECS_MODEL_"+ dp.cp_mdl.split('\\')[-1])                                                         # Copy PLECS model
        dp.shutil.copy(dp.script_path, os.path.join(self.resultfolder, self.basename+".py"))                                                                 # Copy script file
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/"+dp.Runscript_path, os.path.join(self.resultfolder+"/","Runscript.py"))             # Copy runscript
        if dp.JSON['parallel']:                                                                                                                             # Check if parallel
            dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/"+dp.ScriptBody_path, os.path.join(self.resultfolder+"/","ScriptBody.py"))       # Copy script body
        try:                                                                                                                                                  # Start try block
            dp.shutil.copytree((dp.os.getcwd()).replace("\\","/") + "/MyLibraries", self.resultfolder+"/"+"PLECS_Lib")                                      # Copy libraries
        except FileExistsError:                                                                                                                               # Handle file exists error
            pass                                                                                                                                             # Ignore error
        dp.shutil.copytree((dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES", self.resultfolder+"/"+"HEADER_FILES")                        # Copy header files
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/app.js", os.path.join(self.resultfolder+"/HTML_REPORTS/", "app.js"))         # Copy app.js
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Input_vars.json", os.path.join(self.resultfolder+"/","Input_vars.json"))      # Copy input vars
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Input_vars.json", os.path.join(self.jsonfolder+"/","Input_vars_" + self.utc + ".json")) # Copy input vars
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Param_Dicts.py", os.path.join(self.resultfolder+"/","Param_Dicts.py"))        # Copy param dicts
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/plecs_mapping.py", os.path.join(self.resultfolder+"/","plecs_mapping.py"))    # Copy plecs mapping
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/InitializationCommands.m", os.path.join(self.resultfolder+"/","InitializationCommands.m")) # Copy init commands
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/InitializationCommands.m", os.path.join(self.initfolder+"/","InitializationCommands_" + self.utc + ".m")) # Copy init commands

    def get_last_commit(self):                                                                                                                                # Define get_last_commit method
        """                                                                                                                                                   # Docstring start
        Get the last commit hash and comment.                                                                                                                 # Docstring description

        Returns:                                                                                                                                              # Returns section
            str: Commit hash , commit comment                                                                                                                 # Return value description
        """                                                                                                                                                   # Docstring end
        try:                                                                                                                                                  # Start try block
            # Run git log command to get the latest commit hash and comment                                                                                   # Comment about git command
            result = dp.subprocess.run(                                                                                                                      # Run subprocess
                                        ['git', 'log', '-1', '--pretty=format:%H%n%s']  ,                                                                    # Git command
                                        capture_output  = True                          ,                                                                    # Capture output
                                        text            = True                          ,                                                                    # Text mode
                                        check           = True                                                                                               # Check for errors
                                    )                                                                                                                                 # Close subprocess.run
            # Split the result into hash and comment                                                                                                         # Comment about processing
            commit_hash, commit_comment = result.stdout.split('\n', 1)                                                                                      # Split output
            return commit_hash, commit_comment                                                                                                               # Return values
        except dp.subprocess.CalledProcessError as e:                                                                                                         # Handle subprocess error
            print(f"Error occurred: {e}")                                                                                                                    # Print error
            return None, None                                                                                                                                # Return None values

    def param_log(self,dictt,Threads=1,iterNumber = 1 ,tot_iter=1,sim_num=1,tot_sim=1,prefix='',isFirst=True):                                              # Define param_log method
        """                                                                                                                                                   # Docstring start
        Takes a dictionry then crawls all over its parameters in a recursive way                                                                              # Docstring description
        and logs everything in a file.                                                                                                                        # Continued description

        Args:                                                                                                                                                 # Args section
            dictt (dict)                : input dictionary.                                                                                                  # Parameter description
            Threads (int)               : Number of Threads.                                                                                                 # Parameter description
            iterNumber (int)            : Current Iteration Number.                                                                                          # Parameter description
            prefix (str, optional)      : prefix for data tree in dict. Defaults to ''.                                                                      # Parameter description
            isFirst (Bool)              : helps make the recursive function run an expression only once. Defaults to True.                                   # Parameter description
        """                                                                                                                                                   # Docstring end

        if isFirst:                                                                                                                                           # Check if first call
            commit_hash, commit_comment = self.get_last_commit()                                                                                            # Get commit info
            if commit_hash and commit_comment:                                                                                                               # Check if commit info exists
                self.log("--------------------------------------------------------------------------------------------------------------------------")       # Log separator
                self.log(f"Last Full Commit Hash {'='.rjust(69, ' ')} {str(commit_hash)}"                                                        )           # Log full hash
                self.log(f"Last Commit Hash      {'='.rjust(69, ' ')} {str(commit_hash[:11])}"                                                   )           # Log short hash
                self.log(f"Last Commit Comment   {'='.rjust(69, ' ')} {str(commit_comment)}"                                                     )           # Log comment
            self.log("--------------------------------------------------------------------------------------------------------------------------")           # Log separator
            self.log(f"Date & Time             {'='.rjust(67, ' ')} {str(dp.datetime.datetime.now())}"                                           )           # Log date/time
            self.log(f"Thread Count            {'='.rjust(67, ' ')} {str(Threads)}"                                                              )           # Log thread count
            self.log(f"Iteration Number        {'='.rjust(67, ' ')} {str(iterNumber)}/{str(tot_iter)}"                                           )           # Log iteration number
            self.log(f"Simulation Number       {'='.rjust(67, ' ')} {str(sim_num)}/{str(tot_sim)}"                                               )           # Log simulation number
            self.log("--------------------------------------------------------------------------------------------------------------------------")           # Log separator
        if isinstance(dictt, dict):                                                                                                                          # Check if dictionary
            for k, v2 in dictt.items():                                                                                                                     # Iterate through items
                p2 = "{}['{}']".format(prefix, k)                                                                                                          # Create new prefix
                self.param_log(v2,Threads,iterNumber,tot_iter,sim_num,tot_sim,p2,isFirst=False)                                                           # Recursive call
        else:                                                                                                                                                # Else clause
            if dp.exists(self.LogFile):                                                                                                                      # Check if log exists
                dp.sys.stdout  =   open(self.LogFile,'a')                                                                                                   # Open in append mode
            else :                                                                                                                                            # Else clause
                dp.sys.stdout  =   open(self.LogFile,'w+')                                                                                                  # Open in write mode
            print('{}   = {}'.format(prefix.ljust(87, ' '), repr(dictt))) #replace repr w/ str for less digits.                                             # Print parameter
            dp.sys.stdout.close()                                                                                                                            # Close file
            sys.stdout = sys.__stdout__  # Restore stdout if needed                                                                                          # Restore stdout

#?------------------------------------------------------------------------------------------------------------------------------------------------------------- # Section separator





#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                       _____ _ _         _              _ _                      _
#?                                      |  ___(_) | ___   / \   _ __   __| | |    ___   __ _  __ _(_)_ __   __ _
#?                                      | |_  | | |/ _ \ / _ \ | '_ \ / _` | |   / _ \ / _` |/ _` | | '_ \ / _` |
#?                                      |  _| | | |  __// ___ \| | | | (_| | |__| (_) | (_| | (_| | | | | | (_| |
#?                                      |_|   |_|_|\___/_/   \_\_| |_|\__,_|_____\___/ \__, |\__, |_|_| |_|\__, |
#?                                                                                     |___/ |___/         |___/
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

class FileAndLogging:

    def __init__(self, suffix="", json_dir=""):

        self.utc                    =   str(int(dp.time.time()*1000))                                                                                     # current time in milliseconds
        dp.suffix                   =   suffix                                                                                                            # suffix for result folder
        self.ResultsPath            =   ""                                                                                                                # path to results folder
        self.basename               =   dp.os.path.basename(dp.sys.argv[0])[:-3]                                                                          # base name of the script without .py
        self.resultfolder           =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/" + json_dir + "_" + self.utc + suffix   # result folder path
        self.logfolder              =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Log/" + json_dir                             # log folder path
        self.jsonfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Json/" + json_dir                            # json input folder path
        self.initfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/cmd/" + json_dir                             # initialization commands folder path
        self.nested_res_hier        =   ''                                                                                                                # nested results hierarchy
        self.files                  =   [1]                                                                                                               # list of files

    def line_separator(self):
        """
        Creates and logs a visual line separator for output formatting.
        
        This method generates a horizontal line composed of dash characters
        to visually separate sections in log output. The line length is
        fixed at 105 characters for consistent formatting.
        
        Returns:
            None
        """

        # Define the length of the separator line
        # Log the separator line using the log method

        line_length = 105
        self.log("-" * line_length)

    def natsort_files(self,ResDir):
        """
        Sorts out a list of files in a given directory in an alphanumeric way.

        Args:
            ResDir (string): dircetory of files.

        Returns:
            list: sorted list of files.
        """
        # Initialize an empty list to hold file paths and sort them alphanumerically
        # then return the sorted list of file paths then return it

        file_list   =   []
        for filename in dp.os.scandir(ResDir):
            if filename.is_file() and filename.path.endswith('.csv') and not filename.path.endswith('_Map.csv') and not filename.path.endswith('_Standalone.csv'):
                file_list.append(str(filename.path.replace("\\","/")))
        file_list = dp.natsorted(file_list)
        return  file_list

    def results_folder(self):
        """
        Create a folder for storing results and return the path.

        This function creates a folder in the specified path with a name
        that includes the current UTC date and time. If the folder already
        exists, the function will raise an OSError. The function returns
        the path to the results folder.

        Returns:
        - ResultsPath (str) : The path to the results folder.
        """
        # Create the results folder and subfolders for different types of results
        # If the folder already exists, ignore the error and continue
        # Return the path to the results folder 

        try:
            dp.os.makedirs(self.resultfolder , exist_ok = False)
            dp.os.makedirs(self.resultfolder+"/HTML_REPORTS", exist_ok = False)
            dp.os.makedirs(self.resultfolder+"/CSV_MAPS", exist_ok = False)
            dp.os.makedirs(self.resultfolder+"/CSV_TIME_SERIES", exist_ok = False)
            dp.os.makedirs(self.resultfolder+"/Scopes_Traces", exist_ok = False)

        except OSError:
            pass

        ResultsPath     =   self.resultfolder +"/CSV_TIME_SERIES/" + "results" + "_" + self.utc + "_"

        return ResultsPath

    def logging_folder(self):
        """
        Creates a log file in a specified folder and returns the path to the file.

        Args:
        self (object): An instance of the class that this method is a member of.

        Returns:
        str: The full path to the log file that was created.

        Raises:
        OSError: If the specified log folder already exists and the `exist_ok` flag is set to False.

        """

        # Attempt to create the specified log folder.
        # If the folder already exists, an OSError will be raised (unless exist_ok is True).

        try:
            dp.os.makedirs(self.logfolder, exist_ok = False)
        except OSError:
            pass

        # Create a unique log file name based on the current UTC time.
        self.LogF_name = "log" + "_" + self.utc + ".log"

        # Build the full path to the log file using the specified log folder and file name.
        LogFile = self.logfolder +"/" + self.LogF_name

        # Return the full path to the log file.
        return LogFile

    def log(self,msg):
        """
        Redirects all printed statements from consol to a specified file.

        Args:
            pathf (string)  : path of the file to save to.
            msg (string)    : message to be logged to file.
        """

        # if the file exists, open it in append mode, otherwise create a new file

        if dp.exists(self.LogFile):
            dp.sys.stdout  =   open(self.LogFile,'a')
        else :
            dp.sys.stdout  =   open(self.LogFile,'w+')
        
        # log the message
        print(msg)

        # close the file and restore stdout
        dp.sys.stdout.close()
        sys.stdout = sys.__stdout__

    def json_input_folder(self):
        """
        Creates directories for JSON input and initialization files if they don't exist.
        
        This method attempts to create two directories specified by the class attributes
        `jsonfolder` and `initfolder`. If the directories already exist, the method
        silently continues without raising an error. This ensures the necessary folder
        structure is in place for storing JSON input files and initialization data.
        
        The method uses exist_ok=True parameter to prevent errors when directories
        already exist, making it safe to call multiple times.
        
        Returns:
            None
        """
        try:
            # Attempt to create the specified log folder.If the folder already exists,
            # an OSError will be raised (unless exist_ok is True).
            dp.os.makedirs(self.jsonfolder, exist_ok = True)
            dp.os.makedirs(self.initfolder, exist_ok = True)

        except OSError:
            # If the folder already exists, ignore the error and continue.
            pass

    def createFolders(self):
        """
            Create two folders for storing results and log files, respectively.

            Returns:
            None.

            Side Effects:
            - Creates a folder with the name returned by the results_folder() function and sets it as the
            value of the self.ResultsPath attribute.
            - Creates a folder with the name returned by the logging_folder() function and sets it as the
            value of the self.LogFile attribute.

            Raises:
            - Any exception raised by the results_folder() or logging_folder() function.

            Notes:
            - This function assumes that the self.results_folder() and self.logging_folder() functions
            have already been implemented.
            - The self.ResultsPath and self.LogFile attributes are assumed to be instance variables.
            - This function does not return anything, but it has side effects that modify the state of the
            object.
        """

        # Create the results folder and set the ResultsPath attribute
        # Create the logging folder and set the LogFile attribute
        # and create the JSON input folder

        self.ResultsPath            =   self.results_folder()
        self.LogFile                =   self.logging_folder()
        self.json_input_folder()

    def header(self):
        """
            Generates a header for the log file, consisting of a horizontal line,
            a stylized "SIMULATION STARTED" message, and another horizontal line.

            Parameters:
            self (object): The instance of the class calling this method.

            Returns:
            None

            Side Effects:
            Writes to the log file using the instance's `log` method.
        """
        # Generate a header for the log file
        # The header includes a horizontal line, a stylized "SIMULATION STARTED" message
        # and another horizontal line to visually separate the header from the rest of the log content

        self.log("--------------------------------------------------------------------------------------------------------------------------" )
        self.log(dp.figlet_format("SIMULATION  STARTED",width=100))
        self.log("--------------------------------------------------------------------------------------------------------------------------" )

    def footer(self,simutil):
        """
            Generates the footer for the log file, including the total simulation time, a message indicating that the simulation
            has ended, and a copy of all output files.

            Parameters:
            -----------
            self: object
                The instance of the class that calls this method.

            Returns: None
        """

        # Generate the footer for the log file
        # The footer includes the total simulation time, a message indicating that the simulation has ended,
        # and a copy of all output files to the result folder

        self.log("--------------------------------------------------------------------------------------------------------------------------"    )
        tf_sim  =   dp.time.time()
        self.log(f"Total Simulation Time    {'= '.rjust(67, ' ')}{str((tf_sim-dp.tinit_sim).__round__(3)/60)} minutes."                          )
        self.log("--------------------------------------------------------------------------------------------------------------------------\n"  )
        self.log(dp.figlet_format("SIMULATION  ENDED",width=100))
        self.log("--------------------------------------------------------------------------------------------------------------------------"    )
        if (dp.JSON['parallel']):
            self.log(dp.figlet_format("SIMULATION  ITERATIONS",width=150))
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            self.log(f"Iterations    {''.rjust(59, ' ')}{dp.JSON['sweepNames']}")
            self.log(f"Sweep Names   {''.rjust(59, ' ')}{dp.JSON['Dimension_Names']}")
            for i in range(len(simutil.Map)):
                self.log(f"Iter{' '+str(i+1)}{''.rjust(68-len(str(i+1)), ' ')}{simutil.Map[i].tolist()}")
        self.copyfiles()

    def copyfiles(self):
        """
            Copies relevant files to the result folder.

            This function copies the following files to the result folder:
                1. Log file specified by self.LogFile to the path resultfolder/self.LogF_name
                2. PLECS model specified by dp.cp_mdl to the path resultfolder/PLECS_MODEL_<filename>
                3. Script file specified by dp.script_path to the path resultfolder/<basename>.py
                4. The directory MyLibraries located at the current working directory to the path resultfolder/Plec_Lib
                5. The file app.js located at the path <current working directory>/Script/assets/app.js to the path resultfolder/app.js

            Parameters:
            -----------
            self : object
                An instance of the class that this method belongs to.

            Returns: None
        """

        # Copy the log file to the result folder with a specific name
        # Copy the PLECS model file to the result folder with a specific name
        # Copy the script file to the result folder with a specific name
        # Copy the MyLibraries directory to the result folder
        # Copy the app.js file to the HTML_REPORTS subfolder in the result folder
        # Copy the Input_vars.json file to the result folder and json folder
        # Copy the Param_Dicts.py file to the result folder
        # Copy the plecs_mapping.py file to the result folder
        # Copy the InitializationCommands.m file to the result folder and init folder
        # Copy the Input_vars.json file to the json folder with a timestamp in the filename
        # This ensures that all necessary files are available in the result folder for further analysis or reporting

        dp.shutil.copy(self.LogFile, os.path.join(self.resultfolder, self.LogF_name))
        dp.shutil.copy(dp.cp_mdl, self.resultfolder+"/" +"PLECS_MODEL_"+ dp.cp_mdl.split('\\')[-1])
        dp.shutil.copy(dp.script_path, os.path.join(self.resultfolder, self.basename+".py"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/"+dp.Runscript_path, os.path.join(self.resultfolder+"/","Runscript.py"))
        if dp.JSON['parallel']:
            dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/"+dp.ScriptBody_path, os.path.join(self.resultfolder+"/","ScriptBody.py"))
        try:
            dp.shutil.copytree((dp.os.getcwd()).replace("\\","/") + "/MyLibraries", self.resultfolder+"/"+"PLECS_Lib")
        except FileExistsError:
            pass
        dp.shutil.copytree((dp.os.getcwd()).replace("\\","/") + "/Script/assets/HEADER_FILES", self.resultfolder+"/"+"HEADER_FILES")
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/app.js", os.path.join(self.resultfolder+"/HTML_REPORTS/", "app.js"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Input_vars.json", os.path.join(self.resultfolder+"/","Input_vars.json"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Input_vars.json", os.path.join(self.jsonfolder+"/","Input_vars_" + self.utc + ".json"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/Param_Dicts.py", os.path.join(self.resultfolder+"/","Param_Dicts.py"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/plecs_mapping.py", os.path.join(self.resultfolder+"/","plecs_mapping.py"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/InitializationCommands.m", os.path.join(self.resultfolder+"/","InitializationCommands.m"))
        dp.shutil.copy((dp.os.getcwd()).replace("\\","/")   + "/Script/assets/InitializationCommands.m", os.path.join(self.initfolder+"/","InitializationCommands_" + self.utc + ".m"))

    def get_last_commit(self):
        """
        Get the last commit hash and comment.

        Returns:
            str: Commit hash , commit comment
        """

        # Retrieve the last commit hash and comment from the git repository
        # by running the git log command with specific formatting options.
        # capture the output and splits it into the hash and comment parts.
        # If an error occurs during the command execution, it prints the error message
        # and returns None for both the hash and comment.
        try:
            result = dp.subprocess.run(
                                        ['git', 'log', '-1', '--pretty=format:%H%n%s']  ,
                                        capture_output  = True                          ,
                                        text            = True                          ,
                                        check           = True
                                    )
            commit_hash, commit_comment = result.stdout.split('\n', 1)
            return commit_hash, commit_comment
        except dp.subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return None, None

    def param_log(self,dictt,Threads=1,prefix='',isFirst=True):

        """
        Takes a dictionry then crawls all over its parameters in a recursive way
        and logs everything in a file.

        Args:
            dictt (dict)                : input dictionary.
            Threads (int)               : Number of Threads.
            iterNumber (int)            : Current Iteration Number.
            prefix (str, optional)      : prefix for data tree in dict. Defaults to ''.
            isFirst (Bool)              : helps make the recursive function run an expression only once. Defaults to True.
        """

        # If this is the first call, log the last commit hash and comment
        # and the current date and time, along with the number of threads.

        if isFirst:
            commit_hash, commit_comment = self.get_last_commit()

            if commit_hash and commit_comment:
                self.log("--------------------------------------------------------------------------------------------------------------------------")
                self.log(f"Last Full Commit Hash {'='.rjust(69, ' ')} {str(commit_hash)}"                                                        )
                self.log(f"Last Commit Hash      {'='.rjust(69, ' ')} {str(commit_hash[:11])}"                                                   )
                self.log(f"Last Commit Comment   {'='.rjust(69, ' ')} {str(commit_comment)}"                                                     )

            self.log(f"Date & Time             {'='.rjust(67, ' ')} {str(dp.datetime.datetime.now())}"                                           )
            self.log(f"Thread Count            {'='.rjust(67, ' ')} {str(Threads)}"                                                              )
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            self.log(dp.figlet_format("DEFAULT PARAMETERS",width=200))
            self.log("--------------------------------------------------------------------------------------------------------------------------")

        # If the input is a dictionary, iterate through its items
        # and log each key-value pair with the specified prefix.
        # If the value is another dictionary, recursively call param_log on it
        # with an updated prefix.

        if isinstance(dictt, dict):
            for k, v2 in dictt.items():
                p2 = "{}['{}']".format(prefix, k)
                self.param_log(v2,Threads,p2,isFirst=False)
        else:
            if dp.exists(self.LogFile):
                dp.sys.stdout  =   open(self.LogFile,'a')
            else :
                dp.sys.stdout  =   open(self.LogFile,'w+')
            print('{}   = {}'.format(prefix.ljust(87, ' '), repr(dictt))) #? replace repr w/ str for less digits.
            dp.sys.stdout.close()
            sys.stdout = sys.__stdout__

    def InitializationCommands(self, input_file, output_file, flat_dict ,m_file, misc):
        """
        Replaces lines containing `search_expr` in the input file with content from `flat_dict`.
        The modified content is written to `output_file`. Specifically, if `InitializationCommands ""`
        is found, it inserts the `flat_dict` content inside the quotes.

        Args:
            input_file (str)        : Path to the input file.
            output_file (str)       : Path to the output file.
            flat_dict (list): List of strings to replace the matching line.
        """

        # Open the input file for reading and the output file for writing
        # Read each line from the input file, check for the specific line
        # If the line contains 'InitializationCommands ""', replace it with the flattened dictionary string
        # Write the modified line to the output file, otherwise write the line as is
        # Flatten the dictionary to a string using the specified separator

        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            flattened_str_dot           = misc.dict_to_string(flat_dict, sep='.')
            for line in infile:
                    if 'InitializationCommands ""' in line:
                        updated_line = line.split('""')[0] + ' "' + flattened_str_dot + "\n" +'"'
                        outfile.write(updated_line)
                    else:
                        outfile.write(line)

        # Create the directory for the .m file if it does not exist
        # and write the flattened dictionary string to the .m file
        # Ensure the directory exists before writing the file

        os.makedirs(os.path.dirname(m_file), exist_ok=True)
        with open(m_file, 'w', encoding='utf-8') as m_out:
            m_out.write(flattened_str_dot)
        m_out.close()

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

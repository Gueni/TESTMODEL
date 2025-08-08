
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
        self.utc                    =   str(int(dp.time.time()*1000))           #! define Unix Time stamp.
        dp.suffix                   =   suffix
        self.ResultsPath            =   ""                                      #! define path to dump simulation results in
        self.basename               =   dp.os.path.basename(dp.sys.argv[0])[:-3]
        self.resultfolder           =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/" + json_dir + "_" + self.utc + suffix
        self.logfolder              =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Log/" + json_dir
        self.jsonfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Json/" + json_dir
        self.initfolder             =   (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/cmd/" + json_dir
        self.nested_res_hier        =   ''
        self.files                  =   [1]

    def natsort_files(self,ResDir):
        """
        Sorts out a list of files in a given directory in an alphanumeric way.

        Args:
            ResDir (string): dircetory of files.

        Returns:
            list: sorted list of files.
        """
        file_list   =   []
        # iterate over files in results directory.
        for filename in dp.os.scandir(ResDir):
            if filename.is_file() and filename.path.endswith('.csv') and not filename.path.endswith('_Map.csv'):
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
        try:
            # Attempt to create the specified log folder.
            # If the folder already exists, an OSError will be raised (unless exist_ok is True).
            dp.os.makedirs(self.logfolder, exist_ok = False)
        except OSError:
            # If the folder already exists, ignore the error and continue.
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
        if dp.exists(self.LogFile):
            dp.sys.stdout  =   open(self.LogFile,'a')
        else :
            dp.sys.stdout  =   open(self.LogFile,'w+')
        print(msg)
        dp.sys.stdout.close()
        sys.stdout = sys.__stdout__  # Restore stdout if needed

    def json_input_folder(self):
        try:
            # Attempt to create the specified log folder.If the folder already exists, an OSError will be raised (unless exist_ok is True).
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

            Returns:
            --------
            None
        """
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

            Returns:
            --------
            None
        """
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
        try:
            # Run git log command to get the latest commit hash and comment
            result = dp.subprocess.run(
                                        ['git', 'log', '-1', '--pretty=format:%H%n%s']  ,
                                        capture_output  = True                          ,
                                        text            = True                          ,
                                        check           = True
                                    )
            # Split the result into hash and comment
            commit_hash, commit_comment = result.stdout.split('\n', 1)
            return commit_hash, commit_comment
        except dp.subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
            return None, None

    def param_log(self,dictt,Threads=1,iterNumber = 1 ,tot_iter=1,sim_num=1,tot_sim=1,prefix='',isFirst=True):
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

        if isFirst:
            commit_hash, commit_comment = self.get_last_commit()
            if commit_hash and commit_comment:
                self.log("--------------------------------------------------------------------------------------------------------------------------")
                self.log(f"Last Full Commit Hash {'='.rjust(69, ' ')} {str(commit_hash)}"                                                        )
                self.log(f"Last Commit Hash      {'='.rjust(69, ' ')} {str(commit_hash[:11])}"                                                   )
                self.log(f"Last Commit Comment   {'='.rjust(69, ' ')} {str(commit_comment)}"                                                     )
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            self.log(f"Date & Time             {'='.rjust(67, ' ')} {str(dp.datetime.datetime.now())}"                                           )
            self.log(f"Thread Count            {'='.rjust(67, ' ')} {str(Threads)}"                                                              )
            self.log(f"Iteration Number        {'='.rjust(67, ' ')} {str(iterNumber)}/{str(tot_iter)}"                                           )
            self.log(f"Simulation Number       {'='.rjust(67, ' ')} {str(sim_num)}/{str(tot_sim)}"                                               )
            self.log("--------------------------------------------------------------------------------------------------------------------------")
        if isinstance(dictt, dict):
            for k, v2 in dictt.items():
                p2 = "{}['{}']".format(prefix, k)
                self.param_log(v2,Threads,iterNumber,tot_iter,sim_num,tot_sim,p2,isFirst=False)
        else:
            if dp.exists(self.LogFile):
                dp.sys.stdout  =   open(self.LogFile,'a')
            else :
                dp.sys.stdout  =   open(self.LogFile,'w+')
            print('{}   = {}'.format(prefix.ljust(87, ' '), repr(dictt))) #replace repr w/ str for less digits.
            dp.sys.stdout.close()
            sys.stdout = sys.__stdout__  # Restore stdout if needed

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------





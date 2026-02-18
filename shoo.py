class FileAndLogging:
    def __init__(self, suffix="", json_dir=""):
        """
        Initialize the FileAndLogging class with various attributes
        """
        # Define global padding constants
        self.PADDING_WIDTH = 120  # Main padding width for parameter logging
        
        # Calculate dependent padding values
        self.COMMIT_PADDING = self.PADDING_WIDTH - 51  # For commit hash (was 69)
        self.DATE_PADDING = self.PADDING_WIDTH - 53    # For date & time (was 67)
        self.THREAD_PADDING = self.PADDING_WIDTH - 53  # For thread count (was 67)
        self.ITERATION_PADDING = self.PADDING_WIDTH - 46  # For iterations (was 74)
        self.TIME_PADDING = self.PADDING_WIDTH - 38    # For simulation time (was 67)
        
        self.utc = str(int(dp.time.time()*1000))
        # ... rest of your __init__ code ...

    def footer(self, simutil):
        """
        Generates the footer for the log file
        """
        self.log("--------------------------------------------------------------------------------------------------------------------------")
        tf_sim = dp.time.time()
        
        # Use dynamic padding for time calculation
        self.log(f"Total Simulation Time    {'= '.rjust(self.TIME_PADDING, ' ')}{str((tf_sim-dp.tinit_sim).__round__(3)/60)} minutes.")
        self.log("--------------------------------------------------------------------------------------------------------------------------\n")
        self.log(dp.figlet_format("SIMULATION  ENDED", width=100))
        self.log("--------------------------------------------------------------------------------------------------------------------------")
        
        if (dp.JSON['parallel']):
            self.log(dp.figlet_format("SIMULATION  ITERATIONS", width=150))
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            
            # Calculate iterations padding based on current width
            iter_padding = self.PADDING_WIDTH - 51
            self.log(f"Iterations    {''.rjust(iter_padding, ' ')}{self.filter_non_xi(dp.JSON['sweepNames'])}")
            
            for i in range(len(simutil.Map)):
                # Adjust iteration log padding
                self.log(f"Iter{' '+str(i+1)}{''.rjust(self.PADDING_WIDTH - 50 - len(str(i+1)), ' ')}{simutil.Map[i][:len(self.filter_non_xi(dp.JSON['sweepNames']))]}")
        
        self.copyfiles()

    def param_log(self, dictt, Threads=1, prefix='', isFirst=True):
        """
        Takes a dictionary and logs all parameters in a recursive way
        """
        if isFirst:
            commit_hash, commit_comment = self.get_last_commit()

            if commit_hash and commit_comment:
                self.log("--------------------------------------------------------------------------------------------------------------------------")
                self.log(f"Last Full Commit Hash {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_hash)}")
                self.log(f"Last Commit Hash      {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_hash[:11])}")
                self.log(f"Last Commit Comment   {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_comment)}")

            self.log(f"Date & Time             {'='.rjust(self.DATE_PADDING, ' ')} {str(dp.datetime.datetime.now())}")
            self.log(f"Thread Count            {'='.rjust(self.THREAD_PADDING, ' ')} {str(Threads)}")
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            self.log(dp.figlet_format("DEFAULT PARAMETERS", width=200))
            self.log("--------------------------------------------------------------------------------------------------------------------------")

        if isinstance(dictt, dict):
            for k, v2 in dictt.items():
                p2 = "{}['{}']".format(prefix, k)
                self.param_log(v2, Threads, p2, isFirst=False)
        else:
            if dp.exists(self.LogFile):
                dp.sys.stdout = open(self.LogFile, 'a')
            else:
                dp.sys.stdout = open(self.LogFile, 'w+')
            
            # Use the global PADDING_WIDTH for parameter logging
            print('{}   = {}'.format(prefix.ljust(self.PADDING_WIDTH, ' '), repr(dictt)))
            
            dp.sys.stdout.close()
            sys.stdout = sys.__stdout__


def param_log(self, dictt, Threads=1, prefix='', isFirst=True):
    """
    Takes a dictionary and logs all parameters in a recursive way
    """
    if isFirst:
        # Reset max prefix length for this log session
        self.max_prefix_length = 0
        
        # First, do a dry run to find the maximum prefix length
        self._find_max_prefix(dictt, '')
        
        # Add 20 to the max prefix length for padding
        self.PADDING_WIDTH = self.max_prefix_length + 20
        
        # Calculate dependent paddings based on the new PADDING_WIDTH
        self.COMMIT_PADDING = self.PADDING_WIDTH - 51
        self.DATE_PADDING = self.PADDING_WIDTH - 53
        self.THREAD_PADDING = self.PADDING_WIDTH - 53
        self.ITERATION_BASE_PADDING = self.PADDING_WIDTH - 51
        self.TIME_PADDING = self.PADDING_WIDTH - 38
        
        commit_hash, commit_comment = self.get_last_commit()

        if commit_hash and commit_comment:
            self.log("--------------------------------------------------------------------------------------------------------------------------")
            self.log(f"Last Full Commit Hash {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_hash)}")
            self.log(f"Last Commit Hash      {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_hash[:11])}")
            self.log(f"Last Commit Comment   {'='.rjust(self.COMMIT_PADDING, ' ')} {str(commit_comment)}")

        self.log(f"Date & Time             {'='.rjust(self.DATE_PADDING, ' ')} {str(dp.datetime.datetime.now())}")
        self.log(f"Thread Count            {'='.rjust(self.THREAD_PADDING, ' ')} {str(Threads)}")
        self.log("--------------------------------------------------------------------------------------------------------------------------")
        self.log(dp.figlet_format("DEFAULT PARAMETERS", width=200))
        self.log("--------------------------------------------------------------------------------------------------------------------------")

    if isinstance(dictt, dict):
        for k, v2 in dictt.items():
            p2 = "{}['{}']".format(prefix, k)
            self.param_log(v2, Threads, p2, isFirst=False)
    else:
        if dp.exists(self.LogFile):
            dp.sys.stdout = open(self.LogFile, 'a')
        else:
            dp.sys.stdout = open(self.LogFile, 'w+')
        
        # Use the dynamically calculated PADDING_WIDTH for parameter logging
        print('{}   = {}'.format(prefix.ljust(self.PADDING_WIDTH, ' '), repr(dictt)))
        
        dp.sys.stdout.close()
        sys.stdout = sys.__stdout__

def _find_max_prefix(self, dictt, prefix=''):
    """
    Helper method to find the maximum prefix length without logging
    """
    if isinstance(dictt, dict):
        for k, v in dictt.items():
            new_prefix = "{}['{}']".format(prefix, k)
            current_length = len(new_prefix)
            if current_length > self.max_prefix_length:
                self.max_prefix_length = current_length
            self._find_max_prefix(v, new_prefix)
    else:
        current_length = len(prefix)
        if current_length > self.max_prefix_length:
            self.max_prefix_length = current_length
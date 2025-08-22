
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                           ____              ____            _       _
#?                                          |  _ \ _   _ _ __ / ___|  ___ _ __(_)_ __ | |_ ___
#?                                          | |_) | | | | '_ \\___ \ / __| '__| | '_ \| __/ __|
#?                                          |  _ <| |_| | | | |___) | (__| |  | | |_) | |_\__ \
#?                                          |_| \_\\__,_|_| |_|____/ \___|_|  |_| .__/ \__|___/
#?                                                                              |_|
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class runScripts:
    
    def __init__(self,jsonInputs):

        """
        
        This function initializes the runScripts class with the provided JSON inputs.
        It sets up various class attributes and initializes necessary classes for simulation, logging, and post-processing.
        
        Args:
            jsonInputs (dict): Dictionary containing JSON inputs for the simulation.
        
        """

        self.JS                 =   jsonInputs                                                      #  declare json input file
        self.misc               =   dp.msc.Misc()                                                   #  initialize miscellaneous class
        self.fileLog            =   dp.flg.FileAndLogging(json_dir=self.JS['scriptName'])           #  initialize FileAndLogging class
        self.simutil            =   dp.sutl.SimulationUtils()                                       #  initialize SimulationUtils class
        self.plot               =   dp.plt.HTML_REPORT(self.fileLog.resultfolder,self.fileLog.utc)  #  initialize pyplot class
        self.paramProcess       =   dp.PM.ParamProcess()                                            #  initialize ParamProcess class
        self.postProcessing     =   dp.PP.Processing()                                              #  initialize Processing class

    def simInit(self):

        """
        This function initializes the simulation environment 
        from PLECS model to parameters to creation of target results folder.
        
        """
        # Initialize the simulation environment by creating necessary folders,
        # selecting the mapping for post-processing, initializing simulation variables,
        self.fileLog.createFolders()                                                                                                                            
        dp.pmap.select_mapping(dp.pmap.DCDC_pmap_Raw)        

        # initialize the simulation variables and class objects        
        self.simutil.init_sim(self.JS['maxThreads'],eval(self.JS['startPoint']),*[eval(self.JS[f"X{i}"]) for i in range(1, 11)],self.JS['permute'],self.JS['model'])

        # Add a Note to the HTML report and define the log file header.
        self.plot.note              =   self.JS['simNote']                                                                                                
        self.fileLog.header()                                                                                                                             

        # Initialize the PLECS model and set up the model variables,
        # solver options, and analysis options.
        # execute python commands from list in json var.
        for item in self.JS['ModelVars'] :                                                                                                                      
            exec(item)                                                                                    

        # Initialize Analysis options with the provided JSON input.
        dp.anlOpts                  =   self.JS['AnalysisOpts']                                                                         
        dp.mdlVars['AnalysisOpts']  =   self.JS['AnalysisOpts']     

        # Apply tolerances to the model variables if not running in parallel.
        if not dp.JSON['parallel']:
            dp.mdlVars              =   self.simutil.applyTolerances(self.JS['Comps'],eval(self.JS['Tols']),dp.mdlVars,self.JS['applyTol'],self.JS['randTol'])   

        # DCDC Average Model Calculation 
        dp.mdlVars['DCDC_Average']  =   self.paramProcess.dcdcAverageModelCalculate(dp.mdlVars)                             

        # limit precision of model parameters if specified in the JSON input.
        # This is useful for reducing the numerical precision of model parameters to a specified level.
        if self.JS['limit_precision']:                                                                                  
            dp.mdlVars              =   self.paramProcess.limit_precision(dp.mdlVars , dp.mdl_precision)
            dp.slvOpts              =   self.paramProcess.limit_precision(dp.slvOpts , dp.mdl_precision)
            dp.anlOpts              =   self.paramProcess.limit_precision(dp.anlOpts , dp.mdl_precision)

        # Initialize the solver options and analysis options with the provided JSON input.
        # Connect to the PLECS model through the RPC server.
        # Initialize the PLECS model with the specified model name.
        # Write the model variables as initialization commands in PLECS.

        self.obj                    =   dp.pc.PlecsRPC(dp.url,dp.port,dp.mdlVars,dp.slvOpts,dp.anlOpts)                  
        self.obj.PlecsConnect()                                                                                                       
        self.obj.modelInit_path(self.JS['modelname'])
        self.fileLog.InitializationCommands(self.obj.path,
                                         self.fileLog.resultfolder+"/"+"PLECS_MODEL_"+"standalone_"+self.JS['modelname'],
                                         dp.mdlVars,
                                         (dp.os.getcwd()).replace("\\","/")+"/Script/assets/InitializationCommands.m",
                                         self.misc)
        
        # Clear the traces of the desired scopes in the PLECS model.
        # This is useful for removing any previous traces or data from the specified scopes.
        self.obj.ClearTrace(self.JS['modelname'],self.JS['scopes'])

    def simLog(self,OptStruct):
        
        """ 
        This function logs the simulation parameters and updates the iteration number.
        
        Args:
            OptStruct (dict): Dictionary containing the simulation parameters.
        """

        # Increment the iteration number and log the current iteration number.
        # It also logs the updated parameters and the name of the simulation.
        
        self.simutil.iterNumber    +=  1
        self.fileLog.log(f"Iteration Number        {'='.rjust(67, ' ')} {str(self.simutil.iterNumber)}/{str(self.simutil.Iterations)}")
        
        # Log the changes made to the model parameters.
        # It iterates through the dictionary and logs the key and new value of each updated parameter.

        for path, change in dp.updated_params_dict.items():
            self.fileLog.log(f"""{path.replace("root", "").ljust(50)} = {str(change['new_value'])}\n""")
        self.fileLog.log(f"['Name']                {'='.rjust(67, ' ')} '{OptStruct['Name']}' \n")
        
        # Log the parameters of the current simulation iteration for HTML tables.
        self.plot.set_tab_dict(self.misc,OptStruct['ModelVars'])
        
        # Log the focused parameters for the current iteration.
        self.plot.iter_param_key.append(self.JS['paramKeys'])
        self.plot.iter_param_val.append(eval(self.JS['paramVals']))
        self.plot.iter_param_unt.append(self.JS['paramUnts'])

    def log_updates(self,dict):
        
        """ 
        This function logs the updates made to the model parameters.
        
        Args:
            dict (dict): Dictionary containing the updated parameters.
        """
        
        # Log the changes made to the model parameters.
        # It iterates through the dictionary and logs the key and new value of each updated parameter.

        for path, change in dict.items():
            self.fileLog.log(f"{(path.replace("root", "")).ljust(50)} = {str(change['new_value'])}\n")

    def simRun(self,threads=1,parallel=False,callback=""):

        """
        This function runs a simulation or an analysis and records the elapsed time.

        Args:
            threads   (int, optional) : number of parallel threads to simulate. Defaults to 1.
            parallel  (bool, optional): determine whether a single or parallel simulation. Defaults to False.
            callback  (str, optional) : define a callback fundtion to be executed after simulation is completed. Defaults to "".
        """
        # Selects between simulation and analysis based on the JSON input.
        # If analysis is not selected, it launches a simulation.
        # Otherwise, it launches an analysis.

        self.misc.tic()

        if (not self.JS['analysis']):

            self.obj.LaunchSim(threads,self.obj.path,parallel,callback)   
        else:

            self.obj.LaunchAnalysis(threads,self.obj.path,self.JS['analysisName'],parallel,callback)

        # It also logs the time taken for the simulation or analysis to complete.

        self.fileLog.log(f"Simualtion Time   {'= '.rjust(74, ' ')}{str(self.misc.toc())} seconds.\n")
        self.misc.tic()

    def simSave(self,Simulation=0,Crash=False):

        """
        This function saves the simulation results to disk and store them in data matrices.
        In addition, it performs post-processing on raw results.

        Args:
            Simulation  (int, optional)     : simulation package number. Defaults to 0.
            Crash       (bool, optional)    : determine if a crash happened in a previous iteration. Defaults to False.
        """
        # Hold the traces of the desired scopes
        self.obj.holdTrace(self.JS['modelname'],self.JS['scopes'])

        # Save the simulation results to CSV files and store them in data matrices too
        # then log the time taken for this operation.
        if (self.JS['saveData']):
            self.misc.tic()
            self.simutil.save_data(self.obj.OptStruct,self.simutil,self.fileLog,itr=Simulation,crash=Crash)
            self.fileLog.log(f"Saving Data   {'= '.rjust(78, ' ')}{str(self.misc.toc())} seconds.\n")

    def simEnd(self):

        """
        This function plots the processed results graphically in HTML files.
        It also creates copies of simulation files and scripts in the results folder.
        It resets the simulation iteration counter and generates an HTML report from the results and visualizations.
        Finally, it finalizes logging and saves traces of the desired scopes externally.
        """
        # Reset simulation iteration counter
        self.simutil.iterNumber = 0
        
        # Generate HTML report from results and visualizations if data saving is enabled
        if (self.JS['saveData']):
            self.plot.auto_plot(self.simutil,self.fileLog, self.misc,open=self.JS['openHTML'],iterReport=self.JS['iterReport'])  
        
        # Finalize logging and save traces
        self.fileLog.footer(self.simutil)  # Create footer for log file
        
        # Save the traces of the desired scopes externally
        self.obj.SaveTraces(self.JS['modelname'],self.JS['scopes'],self.fileLog.resultfolder)

    def simMissing(self, iter, threads_vector, Threads):

        """
        This function determines which simulation thread has crashed during 
        parallel runs to repeate it later.

        Args:
            iter (int): current iteration where a crash occured
            threads_vector (list): the used simulation threads for each simulation package
            Threads (int): number of threads used in parallel simulation

        Returns:
            MissingIter (list): list of identified simulation iterations that crashed
        """
        # Find missing iteration data file and clean up optstruct
        MissingIter         = self.postProcessing.findMissingResults(self.fileLog.resultfolder+"/CSV_TIME_SERIES",iter,threads_vector,Threads)
        
        # Reinitialize empty optstruct
        self.obj.OptStruct  = []
        
        # Convert missing iters array back to list
        MissingIter = (dp.np.array(MissingIter)-1).tolist()  
        return MissingIter

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
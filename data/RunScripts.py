
import os,sys                                                                                                            
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp                                                                                                
paramProcess            =	dp.PM.ParamProcess()                                                                         
postProcessing          =	dp.PP.Processing()                                                                           

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class runScripts:                                                                                                               # Define main simulation runner class
    def __init__(self,jsonInputs):                                                                                              # Class constructor
        self.JS                 =   jsonInputs                                                                                  # Store json input parameters
        self.misc               =   dp.msc.Misc()                                                                               # Initialize miscellaneous utilities
        self.fileLog            =   dp.flg.FileAndLogging(json_dir=self.JS['scriptName'])                                       # Initialize file logging system
        self.simutil            =   dp.sutl.SimulationUtils()                                                                   # Initialize simulation utilities
        self.plot               =   dp.plt.HTML_REPORT(self.fileLog.resultfolder,self.fileLog.utc)                              # Initialize HTML report generator

    def simInit(self):                                                                                                          # Initialize simulation environment
        self.fileLog.createFolders()                                                                                            # Create results and logging folders
        dp.pmap.select_mapping(dp.pmap.DCDC_pmap_Raw)                                                                           # Generate post-processing mapping
        self.simutil.init_sim(self.JS['maxThreads']           ,                                                                 # Initialize simulation variables
                           eval(self.JS['startPoint'])        ,                                                                 # Start point for simulation
                           eval(self.JS['X1'])                ,                                                                 # X1 parameters
                           eval(self.JS['X2'])                ,                                                                 # X2 parameters
                           eval(self.JS['X3'])                ,                                                                 # X3 parameters
                           eval(self.JS['X4'])                ,                                                                 # X4 parameters
                           eval(self.JS['X5'])                ,                                                                 # X5 parameters
                           eval(self.JS['X6'])                ,                                                                 # X6 parameters
                           eval(self.JS['X7'])                ,                                                                 # X7 parameters
                           eval(self.JS['X9'])                ,                                                                 # X9 parameters
                           eval(self.JS['X10'])               ,                                                                 # X10 parameters
                           eval(self.JS['X11'])               ,                                                                 # X11 parameters
                           self.JS['permute']                 ,                                                                 # Permute 
                           self.JS['model']                   ,                                                                 # Model                                     
                    )

        self.plot.note              =   self.JS['simNote']                                                                      # Set HTML report note
        self.fileLog.header()                                                                                                   # Write log file header

        for item in self.JS['ModelVars'] :                                                                                      # Process model variables from JSON
            exec(item)                                                                                                          # Execute Python commands from JSON
        dp.anlOpts                  =   self.JS['AnalysisOpts']                                                                 # Update analysis options
        dp.mdlVars['AnalysisOpts']  =   self.JS['AnalysisOpts']                                                                 # Update model variables dict

        if not dp.JSON['parallel']:                                                                                             # Apply tolerances if not parallel
            dp.mdlVars              =   self.simutil.applyTolerances(self.JS['Comps'],
                                        eval(self.JS['Tols']),dp.mdlVars,self.JS['applyTol'],self.JS['randTol'])                # Apply tolerances

        dp.mdlVars['DCDC_Average']  =   paramProcess.dcdcAverageModelCalculate(dp.mdlVars)                                      # Update DCDC average model

        if self.JS['limit_precision']:                                                                                          # Limit parameter precision if needed
            dp.mdlVars              =   dp.PM.ParamProcess().limit_precision(dp.mdlVars , dp.mdl_precision)                     # Limit model variables precision
            dp.slvOpts              =   dp.PM.ParamProcess().limit_precision(dp.slvOpts , dp.mdl_precision)                     # Limit solver options precision
            dp.anlOpts              =   dp.PM.ParamProcess().limit_precision(dp.anlOpts , dp.mdl_precision)                     # Limit analysis options precision

        self.obj                    =   dp.pc.PlecsRPC(dp.url,dp.port,dp.mdlVars,dp.slvOpts,dp.anlOpts)                         # Initialize PLECS RPC connection
        self.obj.PlecsConnect()                                                                                                 # Connect to PLECS RPC server
        self.obj.modelInit_path(self.JS['modelname'])                                                                           # Initialize PLECS model path
        self.misc.InitializationCommands(self.obj.path,                                                                         # Write initialization commands
                                         self.fileLog.resultfolder+"/"+"PLECS_MODEL_"+"standalone_"+self.JS['modelname'],
                                         dp.mdlVars,
                                         (dp.os.getcwd()).replace("\\","/")+"/Script/assets/InitializationCommands.m")
        self.obj.ClearTrace(self.JS['modelname'],self.JS['scopes'])                                                             # Clear PLECS traces

    def simLog(self,OptStruct,Simulation=0):                                                                                    # Create simulation log
        self.simutil.iterNumber    +=  1                                                                                        # Increment iteration counter
        itr                         =   self.simutil.iterNumber                                                                 # Get current iteration

        self.plot.set_tab_dict(self.misc,OptStruct['ModelVars'])                                                                # Add params to report table
        self.fileLog.param_log(OptStruct,self.simutil.Threads,itr,self.simutil.Iterations,Simulation+1,
                               self.simutil.Simulations)                                                                        # Log parameters

        self.plot.iter_param_key.append(self.JS['paramKeys'])                                                                   # Log focused param names
        self.plot.iter_param_val.append(eval(self.JS['paramVals']))                                                             # Log focused param values
        self.plot.iter_param_unt.append(self.JS['paramUnts'])                                                                   # Log focused param units

    def simRun(self,threads=1,parallel=False,callback=""):                                                                      # Run simulation/analysis
        self.misc.tic()                                                                                                         # Start timer
        if (not self.JS['analysis']):                                                                                           # Check if simulation or analysis
            self.obj.LaunchSim(threads,self.obj.path,parallel,callback)                                                         # Launch simulation
        else:
            self.obj.LaunchAnalysis(threads,self.obj.path,self.JS['analysisName'],parallel,callback)                            # Launch analysis

        self.fileLog.log("--------------------------------------------------------------------------------------------------------------------------")
        self.fileLog.log(f"Simualtion Time   {'= '.rjust(74, ' ')}{str(self.misc.toc())} seconds.\n")                           # Log simulation time
        self.misc.tic()                                                                                                         # Reset timer

    def simSave(self,Simulation=0,Crash=False):                                                                                 # Save simulation results
        self.obj.holdTrace(self.JS['modelname'],self.JS['scopes'])                                                              # Hold PLECS traces
        if (self.JS['saveData']):                                                                                               # Check if saving data
            self.misc.tic()                                                                                                     # Start timer
            self.simutil.save_data(self.obj.OptStruct,self.simutil,self.fileLog,itr=Simulation,crash=Crash)                     # Save data to CSV
            self.fileLog.log(f"Saving Data   {'= '.rjust(78, ' ')}{str(self.misc.toc())} seconds.\n")                           # Log save time
            self.fileLog.log("--------------------------------------------------------------------------------------------------------------------------")

    def simEnd(self):                                                                                                           # Finalize simulation
        self.simutil.iterNumber = 0                                                                                             # Reset iteration counter
        if (self.JS['saveData']):                                                                                               # Generate HTML report if needed
            self.plot.auto_plot(self.simutil,self.fileLog,self.misc,open=self.JS['openHTML'],iterReport=self.JS['iterReport'])  # Generate HTML report
        self.fileLog.footer(self.simutil)                                                                                       # Write log file footer
        self.obj.SaveTraces(self.JS['modelname'],self.JS['scopes'],self.fileLog.resultfolder)                                   # Save PLECS traces

    def simMissing(self,iter,threads_vector,Threads):                                                                           # Find crashed simulations
        MissingIter             =   postProcessing.findMissingResults(self.fileLog.resultfolder+"/CSV_TIME_SERIES",iter,
                                                                      threads_vector,Threads)                                   # Find missing results
        self.obj.OptStruct      =   []                                                                                          # Reinitialize optstruct
        self.obj.modelInit_path(self.JS['modelname'])                                                                           # Reinitialize model path
        self.obj.modelinit_opts(1,self.JS['parallel'])                                                                          # Reset to single thread

        MissingIter             =   (dp.np.array(MissingIter)-1).tolist()                                                       # Adjust iteration indices

        return MissingIter                                                                                                      # Return missing iterations

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
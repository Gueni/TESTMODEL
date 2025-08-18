
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

#?--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class runScripts:
    def __init__(self,jsonInputs):
        self.JS                 =   jsonInputs                                                                                                                      #!  declare json input file
        self.misc               =   dp.msc.Misc()                                                                                                                   #!  initialize miscellaneous class
        self.fileLog            =   dp.flg.FileAndLogging(json_dir=self.JS['scriptName'])                                                                           #!  initialize FileAndLogging class
        self.simutil            =   dp.sutl.SimulationUtils()                                                                                                       #!  initialize SimulationUtils class
        self.plot               =   dp.plt.HTML_REPORT(self.fileLog.resultfolder,self.fileLog.utc)                                                                  #!  initialize pyplot class
        self.paramProcess       =   dp.PM.ParamProcess()                                                                                                            #!  initialize ParamProcess class
        self.postProcessing     =   dp.PP.Processing()                                                                                                              #!  initialize Processing class

    def simInit(self):
        """This function initializes the simulation environment; from PLECS model to parameters to creation of target results folder.
        """
        self.fileLog.createFolders()                                                                                                                                #!  create results and logging folder
        dp.pmap.select_mapping(dp.pmap.DCDC_pmap_Raw)                                                                                                               #!  generate mapping for post-processing
        self.simutil.init_sim(self.JS['maxThreads']           ,                                                                                                     #!  initiate simulation variables and class objects
                           eval(self.JS['startPoint'])        ,
                           eval(self.JS['X1'])                ,
                           eval(self.JS['X2'])                ,
                           eval(self.JS['X3'])                ,
                           eval(self.JS['X4'])                ,
                           eval(self.JS['X5'])                ,
                           eval(self.JS['X6'])                ,
                           eval(self.JS['X7'])                ,
                           eval(self.JS['X9'])                ,
                           eval(self.JS['X9'])                ,
                           eval(self.JS['X10'])               ,
                           self.JS['permute']                 ,
                           self.JS['model']
                    )

        self.plot.note              =   self.JS['simNote']                                                                                                          #!  include a message or a note in the HTML report
        self.fileLog.header()                                                                                                                                       #!  define log file header

        for item in self.JS['ModelVars'] :                                                                                                                          #!  upadate modelVars items coming from json file
            exec(item)                                                                                                                                              #!  execute python commands from list in json var
        dp.anlOpts                  =   self.JS['AnalysisOpts']                                                                                                     #!  upadate analysis opts in PLECS
        dp.mdlVars['AnalysisOpts']  =   self.JS['AnalysisOpts']                                                                                                     #!  upadate analysis opts dictionary in mdlVars

        if not dp.JSON['parallel']:
            dp.mdlVars              =   self.simutil.applyTolerances(self.JS['Comps'],eval(self.JS['Tols']),dp.mdlVars,self.JS['applyTol'],self.JS['randTol'])      #!  apply component tolerances mapping

        dp.mdlVars['DCDC_Average']  =   self.paramProcess.dcdcAverageModelCalculate(dp.mdlVars)                                                                          #!  update DCDC average model parameters

        if self.JS['limit_precision']:                                                                                                                              #!  limit precision of all model parameters
            dp.mdlVars              =   self.paramProcess.limit_precision(dp.mdlVars , dp.mdl_precision)
            dp.slvOpts              =   self.paramProcess.limit_precision(dp.slvOpts , dp.mdl_precision)
            dp.anlOpts              =   self.paramProcess.limit_precision(dp.anlOpts , dp.mdl_precision)

        self.obj                    =   dp.pc.PlecsRPC(dp.url,dp.port,dp.mdlVars,dp.slvOpts,dp.anlOpts)                                                             #!  intialize pyplecs class
        self.obj.PlecsConnect()                                                                                                                                     #!  connect to plecs model through RPC server
        self.obj.modelInit_path(self.JS['modelname'])                                                                                                               #!  initialize and load the PLECS model
        self.fileLog.InitializationCommands(self.obj.path,                                                                                                          #!  write mdlVars as initialization commands in PLECS
                                         self.fileLog.resultfolder+"/"+"PLECS_MODEL_"+"standalone_"+self.JS['modelname'],
                                         dp.mdlVars,
                                         (dp.os.getcwd()).replace("\\","/")+"/Script/assets/InitializationCommands.m",
                                         self.misc)
        self.obj.ClearTrace(self.JS['modelname'],self.JS['scopes'])                                                                                                 #!  clear plecs scopes traces from saved data

    def simLog(self,OptStruct):

        self.simutil.iterNumber    +=  1                                                                                                                            #!  increment iteration number
        self.fileLog.log(f"Iteration Number        {'='.rjust(67, ' ')} {str(self.simutil.iterNumber)}/{str(self.simutil.Iterations)}"                                           )
        self.fileLog.param_log(dp.updated_params_dict,self.simutil.Threads,isFirst=False)
        self.fileLog.log(f"['Name']                {'='.rjust(67, ' ')} '{OptStruct['Name']}' \n")
        self.plot.set_tab_dict(self.misc,OptStruct['ModelVars'])                                                                                                    #!  add model parameters values to report table
        self.plot.iter_param_key.append(self.JS['paramKeys'])                                                                                                       #!  log focused parameters names
        self.plot.iter_param_val.append(eval(self.JS['paramVals']))                                                                                                 #!  log focused parameters values
        self.plot.iter_param_unt.append(self.JS['paramUnts'])

    def log_updates(self,dict):

        for path, change in dict.items():
            self.fileLog.log(f"{(path.replace("root", "")).ljust(50)} = {str(change['new_value'])}\n")

    def simRun(self,threads=1,parallel=False,callback=""):
        """This function runs a simulation or an analysis and records the elapsed time.

        Args:
            threads (int, optional): number of parallel threads to simulate. Defaults to 1.
            parallel (bool, optional): determine whether a single or parallel simulation. Defaults to False.
            callback (str, optional): define a callback fundtion to be executed after simulation is completed. Defaults to "".
        """
        self.misc.tic()
        if (not self.JS['analysis']):
            self.obj.LaunchSim(threads,self.obj.path,parallel,callback)                                                                                             #!  launch simulation through RPC
        else:
            self.obj.LaunchAnalysis(threads,self.obj.path,self.JS['analysisName'],parallel,callback)                                                                #!  launch analysis through RPC

        self.fileLog.log(f"Simualtion Time   {'= '.rjust(74, ' ')}{str(self.misc.toc())} seconds.\n")
        self.misc.tic()

    def simSave(self,Simulation=0,Crash=False):
        """This function saves the simulation results to disk and store them in data matrices. In addition, it performs post-processing on raw results.

        Args:
            Simulation (int, optional): simulation package number. Defaults to 0.
            Crash (bool, optional): determine if a crash happened in a previous iteration. Defaults to False.
        """
        self.obj.holdTrace(self.JS['modelname'],self.JS['scopes'])                                                                                                  #!  hold the traces of the desired scopes
        if (self.JS['saveData']):
            self.misc.tic()
            self.simutil.save_data(self.obj.OptStruct,self.simutil,self.fileLog,itr=Simulation,crash=Crash)                                                         #!  save simulation data to csv files when required
            self.fileLog.log(f"Saving Data   {'= '.rjust(78, ' ')}{str(self.misc.toc())} seconds.\n")

    def simlog_header(self,simulation=0):
            
            if not simulation:

                self.fileLog.param_log(self.obj.OptStruct[simulation],self.simutil.Threads)
                self.fileLog.log("--------------------------------------------------------------------------------------------------------------------------")
                self.fileLog.log(dp.figlet_format("ITERATIONS PARAMETERS",width=200))

            self.fileLog.log("--------------------------------------------------------------------------------------------------------------------------")
            self.fileLog.log(f"Simulation Number       {'='.rjust(67, ' ')} {str(simulation+1)}/{str(self.simutil.Simulations)}"                                               )
            self.fileLog.log("--------------------------------------------------------------------------------------------------------------------------")

    def simEnd(self):
        """This function plots the processed results graphically in HTML files. It also creates copies of simulation files and scripts in the results folder.
        """
        self.simutil.iterNumber = 0                                                                                                                                 #!  reset simulation iteration
        if (self.JS['saveData']):
            self.plot.auto_plot(self.simutil,self.fileLog,self.misc,open=self.JS['openHTML'],iterReport=self.JS['iterReport'])                                      #!  generate HTML report from results set
            # self.plot.plots_sweeps_json()                                                                                                                         #todo: function is broken, needs to be re-written in a better way  #generate 3D/2D plots after simulation sweeps
        self.fileLog.footer(self.simutil)                                                                                                                           #!  create footer for log file
        self.obj.SaveTraces(self.JS['modelname'],self.JS['scopes'],self.fileLog.resultfolder)                                                                       #!  save the traces of the desired scopes externally

    def simMissing(self,iter,threads_vector,Threads):
        """This function determines which simulation thread has crashed during parallel runs to repeate it later.

        Args:
            iter (int): current iteration where a crash occured
            threads_vector (list): the used simulation threads for each simulation package
            Threads (int): number of threads used in parallel simulation

        Returns:
            MissingIter (list): list of identified simulation iterations that crashed
        """
        MissingIter             =   self.postProcessing.findMissingResults(self.fileLog.resultfolder+"/CSV_TIME_SERIES",iter,threads_vector,Threads)                #!  find missing iteration data file
        self.obj.OptStruct      =   []                                                                                                                              #!  reintialize empty optstruct

        MissingIter             =   (dp.np.array(MissingIter)-1).tolist()                                                                                           #!  converts the missing iters array back to list
        return MissingIter

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
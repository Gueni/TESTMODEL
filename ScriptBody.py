import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
paramProcess            =	dp.PM.ParamProcess()
dataProcess             =   dp.PP.Processing()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def simScript(OptStruct,Thread,Map,iterNumber,ResultsPath,misc,crash=False):
    """
    This function is used to write scripts for automated simulations. Multiple simulations with parameters or conditions variations can be programmed here.
       Please make a copy of this file and rename it to 'ScriptBody.py' and place it in the same directory as this file.
       Please don't delete or make changes to this file.

    Args:
        OptStruct (list)        : nested list that contains simulation parameters
        Thread (int)            : current working thread number
        Map (list)              : nested list containing all simulation sweep parameters
        iterNumber (int)        : current working iteration number
        ResultsPath (string)    : current results folder location
        misc (class)            : miscellaneous class object for simulation data handling
        crash (bool)            : a boolean to determine if a simulation crash happened in the previous iteration
    """

    mdlVars                                                                        =   OptStruct[Thread]['ModelVars']
    mapVars                                                                        =   Map[iterNumber]
    X1,X2,X3,X4,X5,X6,X7,X8,X9,X10                                                 =   range(10)
    mdlVars['Common']['ToFile']['FileName']                                        =   ResultsPath + str(iterNumber+1)
    mdlVars['Common']['ToFile']['FileNameStandalone']                              =   mdlVars['Common']['ToFile']['FileName'] + '_Standalone'
    mdlVars                                                                        =   dp.TD.TrackableDict(mdlVars)

    with mdlVars.track_scope():
        pass

    #! -------------------------------------------------------------------------------------Don't change above this line---------------------------------------------------------------------------


        
        mdlVars['Common']['Thermal']['Twater']                    = mapVars[X1]
        mdlVars['DCDC_Rail1']['Control']['Inputs']['Vin']         = mapVars[X2]
        mdlVars['Common']['Control']['Targets']['Vout']           = mapVars[X3]
        mdlVars['Common']['Control']['Targets']['Pout']           = mapVars[X4]


        mdlVars['Common']['Load']['Front']['R_L']                 = mapVars[X3]**2/mapVars[X4]



        
    #! -------------------------------------------------------------------------------------Don't change under this line---------------------------------------------------------------------------

    dp.updated_params_dict                                                          =   mdlVars.assignments
    mdlVars                                                                         =   dict(mdlVars)
    OptStruct[Thread]['ModelVars']                                                  =   mdlVars

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def init_sim(self, maxThreads=1, X1=[[0]], X2=[[0]], X3=[[0]], X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]], model='DCDC', pattern=True):
    """
    Initialize simulation with parameter sweeps.
    Starting points are always the first element or first sublist of each X list.
    """

    # Store all parameters
    self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
    self.maxThreads, self.model = maxThreads, model

    # Detect mode
    self.mode = self.detect_mode(self.sweepMatrix)

    if self.mode == "WCA":
        # Reduced matrix: first sublist of each parameter
        reduced_matrix = [var if var in ([[[0]], [0]]) else [var[0]] for var in self.sweepMatrix]

        # Always use first iteration (first sublist of each parameter)
        self.idx, self.itrr = self.findIndex(self.calculate_wca_values(0, reduced_matrix), self.sweepMatrix, pattern=True)
        self.startPoint = self.calculate_wca_values(self.itrr, self.sweepMatrix)

        # Build full WCA map
        active = self.get_active_wca_params(self.sweepMatrix)
        self.Iterations = 2 ** len(active) + 1  # total WCA iterations
        self.Map = [self.calculate_wca_values(i, self.sweepMatrix) for i in range(self.Iterations)]
        self.Map = self.Map[self.itrr:]  # start from first sublist
        self.Map2D = [sum((list(p) if isinstance(p, list) else [p] for p in row), []) for row in self.Map]

    else:
        # Normal mode: first element of each list
        self.startPoint = [
            (var[0][0] if isinstance(var, list) and isinstance(var[0], list) else 0)
            if var not in ([[[0]], [0]]) else 0
            for var in self.sweepMatrix
        ]
        self.idx, self.itrr = self.findIndex(self.startPoint, self.sweepMatrix, pattern)
        self.matrix = self.findStart(self.sweepMatrix, self.idx, pattern)
        self.Map2D, self.Iterations = self.findPoint(self.matrix, self.idx, pattern)
        self.Map = self.Map2D

    # iteration counter and matrices initialization remain the same
    self.iterNumber = 0
    [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations, dp.Y_Length[i]))) for i in list(range(1, 7)) + list(range(9, 14))]
    [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations * len(dp.harmonics), dp.Y_Length[i]))) for i in range(7, 9)]

    # Threads and hierarchical simulations
    if dp.JSON['hierarchical']:
        self.threads_vector = self.postProcessing.hierarchicalSims(self.Map)
        self.Simulations = len(self.threads_vector)
    else:
        maxThreads = self.simThreads(maxThreads)
        self.Threads = self.paralellThreads(maxThreads, self.Iterations)
        self.Simulations = self.Iterations // self.Threads

    self.MAT_list = [getattr(self, f"MAT{i}") for i in range(1, 14)]

    # Set mapping parameters based on model type
    if model == 'DCDC':
        self.mode = dp.pmap.Maps_index['DCDC_data_mat'][0]
        self.map_index = dp.pmap.Maps_index['DCDC_data_mat'][1]
        self.map_names = dp.pmap.Maps_index['DCDC_map_names']
    elif model == 'OBC':
        self.mode = dp.pmap.Maps_index['OBC_data_mat'][0]
        self.map_index = dp.pmap.Maps_index['OBC_data_mat'][1]
        self.map_names = dp.pmap.Maps_index['OBC_map_names']
    else:
        raise NameError(model)

    return self
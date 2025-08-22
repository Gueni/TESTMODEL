
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                       ____  _                 _       _   _             _   _ _   _ _
#?                                      / ___|(_)_ __ ___  _   _| | __ _| |_(_) ___  _ __ | | | | |_(_) |___
#?                                      \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \| | | | __| | / __|
#?                                       ___) | | | | | | | |_| | | (_| | |_| | (_) | | | | |_| | |_| | \__ \
#?                                      |____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|\___/ \__|_|_|___/
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class SimulationUtils:

    def __init__(self):

        self.sweepMatrix,self.startPoint                = [],[]                         # Define starting point of sweep
        self.idx, self.matrix                           = '', ''                        # Define order of sweep
        self.postProcessing                             = dp.PP.Processing()            # Call the Post-Processing class and point to log data
        self.Map, self.Iterations                       = '', 1                         # Define mapping parameters Maps and Iterations
        self.iterNumber, self.Threads, self.Simulations = 1, 1, 1                       # Define Iteration Number, Threads and Simulations
        self.threads_vector                             = []                            # Define vector of threads for hierarchical simulations
        self.iter_continuous                            = 0                             # Define continuous iteration counter
        self.iter_10s                                   = 0                             # Define 10s iteration counter
        self.MAT_list                                   = ''                            # Define list of data matrices
        self.__dict__.update({f"MAT{i}": " " for i in range(1, 13)})                    # Initialize empty data matrices for MAT1-MAT12

    def simThreads(self, desired_threads=1):
        """
        Calculates the number of threads that should be used for a simulation.
        
        This function determines the optimal number of threads to use for a simulation
        by comparing the desired number of threads with the available CPU cores.
        It ensures efficient resource utilization by preventing overallocation of
        CPU resources while allowing for parallel processing when beneficial.
        
        Args:
            desired_threads (int): The number of threads requested for the simulation.
                                Defaults to 1 if not specified.
                                
        Returns:
            int: The number of threads that will be used for the simulation, which is
                the minimum between the available CPU cores and the desired threads.
                This prevents overallocation of system resources.
        """

        # Compare the desired number of threads with the available CPU cores
        return min(dp.multiprocessing.cpu_count(), desired_threads)

    def paralellThreads(self, Threads, Iterations):
        """
        Determines the optimal number of parallel threads for a given number of iterations.

        Args:
        Threads (int): The maximum number of threads that can be used simultaneously.
        Iterations (int): The total number of iterations that need to be completed.

        Returns:
        int: The optimal number of parallel threads to use.

        Raises:
        ValueError: If Threads or Iterations are not positive integers.

        Example:
        If Threads=4 and Iterations=16, the function will return 4 because it is the maximum number
        of threads that can be used to complete all iterations simultaneously.
        """

        # Validate input parameters threads should be positive integers and iterations should be positive integers
        if not isinstance(Threads, int) or not isinstance(Iterations, int) or Threads <= 0 or Iterations <= 0:
            raise ValueError("Threads and Iterations must be positive integers.")

        # Find the largest number of threads that evenly divides the total iterations
        for i in range(Threads, 0, -1):
            remainder = Iterations % i
            if remainder == 0:
                return i

        return 1

    def init_sim(self,maxThreads=1,startPoint=[0,0,0,0,0,0,0,0,0,0],X1=[0],X2=[0],X3=[0],X4=[0],X5=[0],X6=[0],X7=[0],X8=[0],X9=[0],X10=[0],pattern=True,model='DCDC'):
        """
        Initialize a simulation.

        Parameters
        ----------
        maxThreads : int, optional
            Maximum number of threads to use for parallel simulations, default is 1.
        startPoint : list of 10 floats, optional
            Starting point of the parameter sweep, default is [0,0,0,0,0,0,0,0,0,0].
        X1, X2, X3, X4, X5, X6, X7, X8, X9, X10 : list of floats, optional
            Lists of parameter values to sweep over. Each list must have at least one value.
        pattern : bool, optional
            If True, perform a patterned sweep, otherwise perform a full sweep, default is True.
        model : str, optional
            The type of model to use, either 'DCDC' or 'OBC', default is 'DCDC'.

        Returns
        -------
        None
        """
        # define starting point of sweep
        self.sweepMatrix         =   [X1,X2,X3,X4,X5,X6,X7,X8,X9,X10]
        self.startPoint          =   startPoint

        # define order of sweep
        self.idx ,itrr           =   self.postProcessing.findIndex(self.startPoint,self.sweepMatrix,pattern)
        self.matrix              =   self.postProcessing.findStart(self.sweepMatrix,self.idx,pattern)
        self.Map,self.Iterations =   self.postProcessing.findPoint(self.matrix,self.idx,pattern)
        self.iterNumber          =   0

        # initialize empty data matrices 
        # MAT1-MAT6: For Peak, RMS & AVG Currents & Voltages MAT9-MAT13: For Dissipations, Electrical Stats, Temperatures, Thermal Stats & Controls
        # MAT7-MAT8: For FFT of Currents and Voltages
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations, dp.Y_Length[i]))) for i in list(range(1, 7)) + list(range(9, 14))]
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations * len(dp.harmonics), dp.Y_Length[i]))) for i in range(7, 9)]

#!----------------------------------------------------------------------------------------------------------------------------------------------------------
        # if hierarchical simulations are enabled in JSON input file 
        # use hierarchicalSims function to determine count of paralleled simulations
        if dp.JSON['hierarchical']:
            self.threads_vector         =   self.postProcessing.hierarchicalSims(self.Map)
            self.Simulations            =   len(self.threads_vector)
            pass
        else:
            # determine count of paralleled simualtions
            maxThreads               =   self.simThreads(maxThreads)
            self.Threads             =   self.paralellThreads(maxThreads,self.Iterations)
            self.Simulations         =   self.Iterations//self.Threads

        self.MAT_list = [getattr(self, f"MAT{i}") for i in range(1, 14)]

        # initialize mapping parameters for either DCDC or OBC models
        if model == 'DCDC':
            self.mode      = dp.pmap.Maps_index['DCDC_data_mat'][0]
            self.map_index = dp.pmap.Maps_index['DCDC_data_mat'][1]
            self.map_names = dp.pmap.Maps_index['DCDC_map_names']
        elif model == 'OBC':
            self.mode      = dp.pmap.Maps_index['OBC_data_mat'][0]
            self.map_index = dp.pmap.Maps_index['OBC_data_mat'][1]
            self.map_names = dp.pmap.Maps_index['OBC_map_names']
        else:
            raise NameError(model)

    def sweepTolerances(self,misc,Comps,Tols,OptStruct,Thread,Config=0,rand=False):
            """
            Applies tolerance adjustments to specified components in an optimization structure.

            Args:
                misc (object)                           : Utility object containing helper methods like `transform_key_paths` and `update_dict_value`.
                Comps (list of str)                     : List of dot-separated key paths representing components to be adjusted.
                Tols (list of float or list of tuple)   : List of tolerance values. If `rand` is True, this should be a list of (min, max) tuples for random sampling.
                OptStruct (list of dict)                : Optimization structure containing model variables.
                Thread (int)                            : Index of the thread accessing the `OptStruct` element to modify.
                Config (int, optional)                  : If non-zero, tolerances will be applied. Defaults to 0.
                rand (bool, optional)                   : If True, applies random tolerance values from the range specified in `Tols`. Defaults to False.

                Returns:None                            : The function modifies `OptStruct` in place.
            """
            # Transform component key paths to match the structure of `OptStruct`
            # and apply tolerances if `Config` is set to a non-zero value.
            # If `rand` is True, random values within specified ranges are applied.
            # Otherwise, fixed tolerance values are used.

            Comps =misc.transform_key_paths(Comps)
            if (Config):
                for i in range(len(Comps)):
                    if (rand):
                        randMin                     =   Tols[i][0]
                        randMax                     =   Tols[i][1]
                        randError	                =	dp.random.SystemRandom().uniform(randMin,randMax)
                        misc.update_dict_value(OptStruct[Thread]['ModelVars'], Comps[i], randError)
                    else:
                        misc.update_dict_value(OptStruct[Thread]['ModelVars'], Comps[i], Tols[i])

    def applyTolerances(self,Comps,Tols,mdlVars,Config=0,rand=False):

        """
            This function allows you to apply tolerances to selected components in the model variables.
            The specified components will have their values modified based on the provided tolerances.

            Parameters  :   comps                  :  A list of component names to which tolerances will be applied.
                            Tols                   :  A list of tolerance values to apply to the corresponding components.
                            mdlVars                :  A dictionary containing the model variables.
                            Config                 :  Integer, Optional A flag indicating whether to apply tolerances (1) or not (0). Defaults to 0.
            Returns     :   Num                    :  A dictionary containing the model variables with applied tolerances, or the original model variables if Config is set to 0.
        """

        # Apply tolerances to specified components in the model variables if Config is set to a non-zero value.
        # If rand is True, random tolerance values within specified ranges are applied.
        # Otherwise, fixed tolerance values are used.
        if (Config):
            ModelVars_Flat      =   dp.flatdict.FlatDict(mdlVars, delimiter='.')

            for i in range(len(Comps)):
                if (rand):
                    randMin                     =   Tols[i][0]
                    randMax                     =   Tols[i][1]
                    randError	                =	dp.random.SystemRandom().uniform(randMin,randMax)
                    ModelVars_Flat[Comps[i]]    =   ModelVars_Flat[Comps[i]] + ModelVars_Flat[Comps[i]]*randError
                else:
                    ModelVars_Flat[Comps[i]]    =   ModelVars_Flat[Comps[i]] + ModelVars_Flat[Comps[i]]*Tols[i]

            ModelVars_Unflat    =   dp.unflatten(ModelVars_Flat)
            return ModelVars_Unflat

        else:
            return mdlVars

    def operation(self,time_values,arg,mode):
        """
        Compute an operation on the input array `arg` according to the specified `mode`.

        Args:
            time_values         : The Time Vector.
            arg (numpy.ndarray) : The input array to operate on. Must have shape (m, n).
            mode (int)          : An integer representing the mode of the operation to perform.
                - mode 1: Computes the maximum absolute value of each row in `arg`, ignoring any NaN values.
                - mode 2: Computes the mean value of each row in `arg`.
                - mode 3: Computes the maximum value of each row in `arg`, ignoring any NaN values.
                - mode 4: Returns the string "nothing".

        Returns:
            numpy.ndarray or str: The result of the operation. If `mode` is 1 or 3, returns a numpy array of shape (m,),
            containing the computed maximum value(s). If `mode` is 2, returns a numpy array of shape (m,), containing
            the computed mean value(s). If `mode` is 4, returns the string "nothing".

        Raises:
            ValueError: If `arg` is not a numpy array or does not have shape (m, n), or if `mode` is not a valid integer
                between 1 and 4 (inclusive).
        """

        # using mode to determine operation to be performed on input array arg
        # arg is expected to be a 2D numpy array with shape (m, n)
        # time_values is the Time Vector
        # mode is an integer representing the operation to perform
        # mode 1: Peak Current/Voltage (max absolute value)
        # mode 2: Average Current/Voltage (mean value)
        # mode 3: Peak Voltage (max value)
        # mode 4: RMS Current/Voltage (RMS value)
        # mode 5: AVG Current/Voltage (AVG value)
        # mode 6: nothing (no operation)
        match mode:
            case 1 :  return   dp.np.nanmax(dp.np.absolute(arg),axis=1)
            case 2 :  return   dp.np.mean(arg,axis=1)
            case 3 :  return   dp.np.nanmax(arg,axis=1)
            case 4 :  return   self.postProcessing.rms_avg('RMS',arg, time_values)
            case 5 :  return   self.postProcessing.rms_avg('AVG',arg, time_values)
            case 6 :  return   "nothing"

    def var_update(self,Threads,crash,optstruct,l):
        """
        Retrieves resistance values and auxiliary power from an optimization structure based on threading and crash conditions.

        Args:
            Threads (int): Number of threads used for parallel processing.
            crash (bool): Indicator if a crash condition has occurred.
            optstruct (list or dict): The optimization structure containing model variables.
            l (int): Index used to access a specific element in `optstruct` if threading is enabled.

        Returns:
            tuple: A tuple containing:
                - res_list (list): List of resistance values.
                - P_aux (float): Auxiliary power value from the thermal model variables.
        """

        # Retrieve resistance values and auxiliary power based on threading and crash conditions.
        # If multiple threads are used and parallel processing is enabled without a crash,
        # access the specific element in optstruct using index l.
        # If a crash has occurred, access the first element of optstruct.
        # Otherwise, access optstruct directly.
        # Return the list of resistances and auxiliary power.

        if (Threads >= 1 and dp.JSON['parallel'] and not crash):
                res_list                        = dp.pmap.return_resistances(optstruct[l])
                P_aux                           = optstruct[l]['ModelVars']['Common']['Thermal']['Paux']
        elif (crash):
                res_list                        = dp.pmap.return_resistances(optstruct[0])
                P_aux                           = optstruct[0]['ModelVars']['Common']['Thermal']['Paux']
        else:
                res_list                        = dp.pmap.return_resistances(optstruct)
                P_aux                           = optstruct['ModelVars']['Common']['Thermal']['Paux']
        return res_list,P_aux

    def save_data(self,optstruct,simutil,fileLog,itr=0,saveMode='w',crash=False):
        """
        Save the simulation results to disk and store them in data matrices.

        Parameters:
        -----------
        misc : object
            An object that contains miscellaneous data and methods.
        results : list or np.ndarray
            The simulation results to be saved.
        itr : int, optional
            The iteration index. Default is 0.
        saveMode : str, optional
            The mode of saving the data to disk. Can be 'a' for appending or 'w' for overwriting. Default is 'a'.
        """

        # Save the simulation results to disk and store them in data matrices.
        # The function processes the results for each thread, performs various operations,
        # and updates the corresponding data matrices. Finally, it appends the results to CSV files.

        iteration_range     = list(range(sum(self.threads_vector[0:itr]),sum(self.threads_vector[0:itr+1]))) if dp.JSON['hierarchical'] else list(range(itr*simutil.Threads,simutil.Threads*(itr+1)))
        for l in range(simutil.Threads):
            results_TF                          = self.postProcessing.gen_result(fileLog.resultfolder+"/CSV_TIME_SERIES",iteration_range[l],fileLog.utc)
            nestedresults                       = dp.np.array(self.postProcessing.norm_results_csv(results_TF))
            nestedresults_l                     = dp.np.array([dp.np.array(subarr,dtype=dp.np.float64)[~dp.pd.isnull(dp.np.array(subarr))] for subarr in nestedresults])
            res_list , P_aux                    = self.var_update(simutil.Threads,crash,optstruct,l)
            T_vect                              = nestedresults_l[0]

            threads_idx                         = l+sum(self.threads_vector[0:itr]) if dp.JSON['hierarchical'] else l+itr*simutil.Threads
            for mat_name, mode, sl in dp.matrix_ops:
                getattr(self, mat_name)[threads_idx, :] = self.operation(T_vect, nestedresults_l[sl, :], mode)
            self.MAT7[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect,nestedresults_l[1 : dp.Y_list[1]+1 , :])                         
            self.MAT8[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect, nestedresults_l[sum(dp.Y_list[0:2]) : sum(dp.Y_list[0:3]) , :]) 
            self.MAT9[threads_idx,:]  = self.postProcessing.dissipations(nestedresults_l,res_list,self.MAT2,threads_idx,self.MAT7)                                                                                         
            self.MAT12[threads_idx,:] = self.postProcessing.therm_stats(self.MAT_list,threads_idx,P_aux)                                                                                                                   
        self.MAT_list[6:8] = [self.MAT7[:self.Iterations * len(dp.harmonics)], self.MAT8[:self.Iterations * len(dp.harmonics)]]
        [ self.postProcessing.csv_append_rows(f"{fileLog.resultfolder}/CSV_MAPS/{name}_Map.csv", data.tolist(), save_mode=saveMode) for name, data in zip(dp.map_names, self.MAT_list) ]
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
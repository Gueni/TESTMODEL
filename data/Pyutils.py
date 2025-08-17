
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

        self.sweepMatrix,self.startPoint                = [],[]                                                                                                                                                             # Initialize sweep matrix and start point lists
        self.idx, self.matrix                           = '', ''                                                                                                                                                            # Initialize index and matrix strings
        self.postProcessing                             = dp.PP.Processing()                                                                                                                                                # Create Processing instance for post-processing
        self.Map, self.Iterations                       = '', 1                                                                                                                                                             # Initialize Map string and Iterations counter
        self.iterNumber, self.Threads, self.Simulations = 1, 1, 1                                                                                                                                                           # Initialize iteration, thread and simulation counters
        self.threads_vector                             = []                                                                                                                                                                # Initialize threads vector list
        self.iter_continuous                            = 0                                                                                                                                                                 # Initialize continuous iteration counter
        self.iter_10s                                   = 0                                                                                                                                                                 # Initialize 10s iteration counter
        self.MAT_list                                   = ''                                                                                                                                                                # Initialize MAT_list string
        self.__dict__.update({f"MAT{i}": " " for i in range(1, 13)})                                                                                                                                                        # Create MAT1-MAT12 attributes

    def simThreads(self, desired_threads=1):                                                                    
        """                                                                                                     
        Calculates the number of threads that should be used for a simulation.

        Args:
            desired_threads (int): The number of threads requested.

        Returns:
            int: The number of threads that will be used, limited by available CPU cores.
        """
        return min(dp.multiprocessing.cpu_count(), desired_threads)                                                                                                                                                         # Return minimum of available CPUs and desired threads

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
        If Threads=4 and Iterations=16, the function will return 4 because it is the maximum number of threads that can be used to complete all iterations simultaneously.
        """
        if not isinstance(Threads, int) or not isinstance(Iterations, int) or Threads <= 0 or Iterations <= 0:                                                                                                              # Validate input types and values
            raise ValueError("Threads and Iterations must be positive integers.")                                                                                                                                           # Raise error if invalid

        for i in range(Threads, 0, -1):                                                                                                                                                                                     # Iterate from Threads down to 1
            remainder = Iterations % i                                                                                                                                                                                      # Calculate remainder
            if remainder == 0:                                                                                                                                                                                              # If no remainder
                return i                                                                                                                                                                                                    # Return current thread count

        return 1                                                                                                                                                                                                            # Default return 1 thread

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
        self.sweepMatrix         =   [X1,X2,X3,X4,X5,X6,X7,X8,X9,X10]                                                                                                                                                       # Set sweep matrix with input parameter lists
        self.startPoint          =   startPoint                                                                                                                                                                             # Set start point
        self.idx ,itrr           =   self.postProcessing.findIndex(self.startPoint,self.sweepMatrix,pattern)                                                                                                                # Find sweep index
        self.matrix              =   self.postProcessing.findStart(self.sweepMatrix,pattern)                                                                                                                                # Find start matrix
        self.Map,self.Iterations =   self.postProcessing.findPoint(self.matrix,self.idx,pattern)                                                                                                                            # Find point and iterations
        self.iterNumber          =   0                                                                                                                                                                                      # Reset iteration number
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations, dp.Y_Length[i]))) for i in list(range(1, 7)) + list(range(9, 14))]                                                                                          # MAT1-MAT6: For Peak, RMS,& AVG Currents & Voltages MAT9-MAT13: For Dissipations, Electrical Stats, Temperatures, Thermal Stats,& Controls
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations * len(dp.harmonics), dp.Y_Length[i]))) for i in range(7, 9)]                                                                                                 # MAT7-MAT8: For FFT of Currents and Voltages

#!----------------------------------------------------------------------------------------------------------------------------------------------------------
        if dp.JSON['hierarchical']:                                                                                                                                                                                         # Check if hierarchical mode is enabled
            self.threads_vector         =   self.postProcessing.hierarchicalSims(self.Map)                                                                                                                                  # Get hierarchical thread vector
            self.Simulations            =   len(self.threads_vector)                                                                                                                                                        # Set simulations count
            pass                                                                                                                                                                                                            # Pass if hierarchical mode is enabled
        else:                                                                                                                                                                                                               # 
            maxThreads               =   self.simThreads(maxThreads)                                                                                                                                                        # Get maximum threads
            self.Threads             =   self.paralellThreads(maxThreads,self.Iterations)                                                                                                                                   # Get parallel threads
            self.Simulations         =   self.Iterations//self.Threads                                                                                                                                                      # Calculate simulations count

        self.MAT_list = [getattr(self, f"MAT{i}") for i in range(1, 14)]                                                                                                                                                    # Create MAT_list
        if model == 'DCDC':                                                                                                                                                                                                 # Check if model is DCDC
            self.mode      = dp.pmap.Maps_index['DCDC_data_mat'][0]                                                                                                                                                         # Set DCDC mode
            self.map_index = dp.pmap.Maps_index['DCDC_data_mat'][1]                                                                                                                                                         # Set DCDC map index
            self.map_names = dp.pmap.Maps_index['DCDC_map_names']                                                                                                                                                           # Set DCDC map names
        elif model == 'OBC':                                                                                                                                                                                                # Check if model is OBC
            self.mode      = dp.pmap.Maps_index['OBC_data_mat'][0]                                                                                                                                                          # Set OBC mode
            self.map_index = dp.pmap.Maps_index['OBC_data_mat'][1]                                                                                                                                                          # Set OBC map index
            self.map_names = dp.pmap.Maps_index['OBC_map_names']                                                                                                                                                            # Set OBC map names
        else:                                                                                                                                                                                                               # 
            raise NameError(model)                                                                                                                                                                                          # Raise model name error

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
            Comps =misc.transform_key_paths(Comps)                                                                                                                                                                          # Transform component paths
            if (Config):                                                                                                                                                                                                    # Check if config is enabled
                for i in range(len(Comps)):                                                                                                                                                                                 # Iterate through components
                    if (rand):                                                                                                                                                                                              # Check if random mode
                        randMin                     =   Tols[i][0]                                                                                                                                                          # Get random min
                        randMax                     =   Tols[i][1]                                                                                                                                                          # Get random max
                        randError	                =	dp.random.SystemRandom().uniform(randMin,randMax)                                                                                                                   # Generate random error
                        misc.update_dict_value(OptStruct[Thread]['ModelVars'], Comps[i], randError)                                                                                                                         # Update model vars with random error
                    else:                                                                                                                                                                                                   # 
                        misc.update_dict_value(OptStruct[Thread]['ModelVars'], Comps[i], Tols[i])                                                                                                                           # Update model vars with tolerance

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
        if (Config):                                                                                                                                                                                                        # Check if config is enabled
            ModelVars_Flat      =   dp.flatdict.FlatDict(mdlVars, delimiter='.')                                                                                                                                            # Flatten model vars

            for i in range(len(Comps)):                                                                                                                                                                                     # Iterate through components
                if (rand):                                                                                                                                                                                                  # Check if random mode
                    randMin                     =   Tols[i][0]                                                                                                                                                              # Get random min
                    randMax                     =   Tols[i][1]                                                                                                                                                              # Get random max
                    randError	                =	dp.random.SystemRandom().uniform(randMin,randMax)                                                                                                                       # Generate random error
                    ModelVars_Flat[Comps[i]]    =   ModelVars_Flat[Comps[i]] + ModelVars_Flat[Comps[i]]*randError                                                                                                           # Apply random error
                else:                                                                                                                                                                                                       # 
                    ModelVars_Flat[Comps[i]]    =   ModelVars_Flat[Comps[i]] + ModelVars_Flat[Comps[i]]*Tols[i]                                                                                                             # Apply tolerance

            ModelVars_Unflat    =   dp.unflatten(ModelVars_Flat)                                                                                                                                                            # Unflatten model vars
            return ModelVars_Unflat                                                                                                                                                                                         # Return modified vars

        else:                                                                                                                                                                                                               # 
            return mdlVars                                                                                                                                                                                                  # Return original vars

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
        match mode:                                                                                                                                                                                                         # Match mode
            case 1 :  return   dp.np.nanmax(dp.np.absolute(arg),axis=1)                                                                                                                                                     # Return max absolute value
            case 2 :  return   dp.np.mean(arg,axis=1)                                                                                                                                                                       # Return mean value
            case 3 :  return   dp.np.nanmax(arg,axis=1)                                                                                                                                                                     # Return max value
            case 4 :  return   self.postProcessing.rms_avg('RMS',arg, time_values)                                                                                                                                          # Return RMS value
            case 5 :  return   self.postProcessing.rms_avg('AVG',arg, time_values)                                                                                                                                          # Return AVG value
            case 6 :  return   "nothing"                                                                                                                                                                                    # Return nothing

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
        if (Threads > 1 and dp.JSON['parallel'] and not crash):                                                                                                                                                             # Check if parallel mode and no crash
                res_list                        = dp.pmap.return_resistances(optstruct[l])                                                                                                                                  # Get resistances for thread
                P_aux                           = optstruct[l]['ModelVars']['Common']['Thermal']['Paux']                                                                                                                    # Get auxiliary power for thread
        elif (crash):                                                                                                                                                                                                       # Check if crash
                res_list                        = dp.pmap.return_resistances(optstruct[0])                                                                                                                                  # Get resistances from first thread
                P_aux                           = optstruct[0]['ModelVars']['Common']['Thermal']['Paux']                                                                                                                    # Get auxiliary power from first thread
        else:                                                                                                                                                                                                               # 
                res_list                        = dp.pmap.return_resistances(optstruct)                                                                                                                                     # Get resistances
                P_aux                           = optstruct['ModelVars']['Common']['Thermal']['Paux']                                                                                                                       # Get auxiliary power
        return res_list,P_aux                                                                                                                                                                                               # Return resistances and power

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
        iteration_range     = list(range(sum(self.threads_vector[0:itr]),sum(self.threads_vector[0:itr+1]))) if dp.JSON['hierarchical'] else list(range(itr*simutil.Threads,simutil.Threads*(itr+1)))                       # Get iteration range
        for l in range(simutil.Threads):                                                                                                                                                                                    # Iterate through threads
            results_TF                          = self.postProcessing.gen_result(fileLog.resultfolder+"/CSV_TIME_SERIES",iteration_range[l],fileLog.utc)                                                                    # Generate results
            nestedresults                       = dp.np.array(self.postProcessing.norm_results_csv(results_TF))                                                                                                             # Normalize results
            nestedresults_l                     = dp.np.array([dp.np.array(subarr,dtype=dp.np.float64)[~dp.pd.isnull(dp.np.array(subarr))] for subarr in nestedresults])                                                    # Clean results
            res_list , P_aux                    = self.var_update(simutil.Threads,crash,optstruct,l)                                                                                                                        # Get resistances and power
            T_vect                              = nestedresults_l[0]                                                                                                                                                        # Get time vector
            # V_vect                              =  nestedresults_l[1:]                                                                                                                                                    #
            # for k in range(len(V_vect)):                                                                                                                                                                                  #
            #     T_resample,V_resample           =   self.postProcessing.resample(T_vect,V_vect[k])                                                                                                                        #
            #     if (dp.JSON['IIR_Filter']):                                                                                                                                                                               #
            #         V_filter                    =   self.postProcessing.IIR_Filter(T_resample,                                                                                                                            #
            #                                                                        V_resample,                                                                                                                            #
            #                                                                        dp.JSON['IIR_Freq'],                                                                                                                   #
            #                                                                        dp.JSON['IIR_Order'],                                                                                                                  #
            #                                                                        dp.JSON['IIR_Band'],                                                                                                                   #
            #                                                                        dp.JSON['IIR_Type'])                                                                                                                   #
            #     else:                                                                                                                                                                                                     #    
            #         V_filter                    =   V_resample                                                                                                                                                            #
            #     nestedresults_l[k+1]            =   V_filter                                                                                                                                                              #
            # T_vect                              =   T_resample                                                                                                                                                            # 
            threads_idx = l+sum(self.threads_vector[0:itr]) if dp.JSON['hierarchical'] else l+itr*simutil.Threads                                                                                                           # Calculate thread index
            # dp.harmonics                     = self.postProcessing.get_harmonics(T_vect,nestedresults_l[1 : dp.Y_list[1]+1 , :])                                                                                          # Get harmonics
            for mat_name, mode, sl in dp.matrix_ops:                                                                                                                                                                        # Iterate through matrix operations
                getattr(self, mat_name)[threads_idx, :] = self.operation(T_vect, nestedresults_l[sl, :], mode)                                                                                                              # Perform operation and store result
            self.MAT7[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect,nestedresults_l[1 : dp.Y_list[1]+1 , :])                          # Store FFT current
            self.MAT8[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect, nestedresults_l[sum(dp.Y_list[0:2]) : sum(dp.Y_list[0:3]) , :])  # Store FFT voltage
            self.MAT9[threads_idx,:]  = self.postProcessing.dissipations(nestedresults_l,res_list,self.MAT2,threads_idx,self.MAT7)                                                                                          # Store dissipations
            self.MAT12[threads_idx,:] = self.postProcessing.therm_stats(self.MAT_list,threads_idx,P_aux)                                                                                                                    # Store thermal stats
        self.MAT_list[6:8] = [self.MAT7[:self.Iterations * len(dp.harmonics)], self.MAT8[:self.Iterations * len(dp.harmonics)]]                                                                                             # Update MAT_list
        [ self.postProcessing.csv_append_rows(f"{fileLog.resultfolder}/CSV_MAPS/{name}_Map.csv", data.tolist(), save_mode=saveMode) for name, data in zip(dp.map_names, self.MAT_list) ]                                    # Save data to CSV
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

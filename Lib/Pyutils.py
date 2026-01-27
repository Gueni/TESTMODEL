
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
        """
        Initialize the SimulationUtils class with various attributes
        """

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

    def simThreads(self,desired_threads=1):
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

    def paralellThreads(self,Threads,Iterations):
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

    def detect_mode(self, Xs):
        
        for var in Xs:
            if var == [[0]] or var == [0]   :   continue
            for sub in var:
                if not isinstance(sub, list):   return "NORMAL"
                if len(sub) == 4            :   return "WCA"
                elif len(sub) == 1          :   return "NORMAL"

        return "NORMAL"

    def binary_index(self, iteration, index, active):
       
        # index is global parameter index 0..9
        # active is list of active WCA parameter indices
        active_index    = active.index(index)
        n_active        = len(active)

        # Reverse bit significance
        bit_position    = n_active - 1 - active_index

        return (iteration >> bit_position) & 1

    def funtol(self, Abs_rel, iteration, index, nom, tol):
        """
        Calculate tolerance-adjusted value for WCA analysis.
        
        Parameters:
            Abs_rel     (bool)  : True for absolute tolerance (tol <= 1), False for relative 
            iteration   (int)   : Current WCA iteration number
            index       (int)   : Parameter index for binary encoding
            nom         (float) : Nominal value
            tol         (float) : Tolerance value
            
        Returns   :     (float) : Tolerance-adjusted value
            
        Logic     :
            - If binary_index(iteration, index) == 1                     :   Apply upper tolerance
            - If binary_index(iteration, index) == 0                     :   Apply lower tolerance
            - For absolute tolerance (tol <= 1)                          :   Upper: nom * tol, Lower: nom / tol
            - For relative tolerance (tol > 1)                           :   Upper: nom * (1 + tol), Lower: nom * (1 - tol)
        """
        active = self.get_active_wca_params(self.sweepMatrix)

        # Check the bit for this parameter in current iteration
        if not self.binary_index(iteration, index, active):
            # Bit is 1: apply upper tolerance (increase value)
            return nom * (1 + tol) if Abs_rel else  nom * tol
        # Bit is 0: apply lower tolerance (decrease value)
        return nom * (1 - tol) if Abs_rel else nom / tol

    def calculate_wca_values(self, iteration, Xs):
        """
        Calculate WCA values for all parameters in a given iteration.
        
        Parameters:
            iteration   (int)   : Current WCA iteration number
            Xs          (list)  : List of parameter lists for X1-X10
            
        Returns   :     (list)  : 3D list of calculated WCA values for all parameters
            
        """
        results = []
        
        # Process each parameter X1 through X10
        for i, var in enumerate(Xs):
            # Handle unused parameters
            if var == [[0]] or var == [0]:
                results.append([0])
                continue
            
            # Calculate WCA values for this parameter's sublists
            wca_vals = []
            for sub in var:
                # Single value sublist (no tolerance)
                if len(sub) == 1:
                    wca_vals.append(sub[0])
                # WCA format: [nominal, tolerance, min, max]
                elif len(sub) == 4:
                    nom, tol, mn, mx = sub
                    # Determine tolerance type: True for absolute, False for relative
                    tol_type = tol <= 1
                    # Calculate tolerance-adjusted value
                    x = self.funtol(tol_type, iteration, i, nom, tol)
                    # Clamp value within min/max bounds
                    wca_vals.append(min(max(x, mn), mx))
                # Unknown format, use first element
                else:
                    wca_vals.append(sub[0])
            
            results.append(wca_vals)
        
        return results

    def get_active_wca_params(self, Xs):
        """
        Identify which parameters X lists are used.
        
        Parameters  :   Xs (list): List of parameter lists for X1-X10
            
        Returns     :      (list): Indices of parameters that have WCA format (4 elements per sublist)
            
        """
        return [i for i, var in enumerate(Xs) if var not in [[[0]], [0]] and len(var) > 0 and len(var[0]) == 4]

    def extract_values(self, Xs):
        """
        Extract simple values from parameter lists for normal mode.
        
        Args:
            Xs (list): List of parameter lists for X1-X10
            
        Returns:
            list: Simplified list of parameter values (removes nested structure)
            
        Example:
            Input: [[[10], [20]], [[100]], [[0]], ...]
            Output: [[10, 20], [100], [0], ...]
        """
        return [[sub[0] if isinstance(sub, list) and sub else sub for sub in var] if var not in [[[0]], [0]] else [0] for var in Xs]

    def findIndex(self, points, matrix, pattern=True):
        """
        Find the starting index for parameter sweeps.
        
        Parameters:
            points (list): Starting point values (format depends on mode)
            matrix (list): Parameter matrix (X1-X10 lists)
            pattern (bool, optional): True for full Cartesian product,False for sequential simple index. Defaults to True.
                                     
        Returns:
            tuple: (indices list, linear_index)
            
        Note:
            - For WCA mode: Finds which WCA iteration matches the starting point
            - For NORMAL mode with pattern=True: Computes multi-dimensional index
            - For NORMAL mode with pattern=False: Simple single index lookup
        """
        # Detect operation mode from parameters format
        if self.detect_mode(matrix) == "WCA":
            #? ============ WCA MODE LOGIC ============
            # Get active parameters that participate in WCA
            active  = self.get_active_wca_params(matrix)
            # Total WCA iterations: 2^n combinations + 1 nominal case
            total   = 2 ** len(active) + 1
            
            # Generate nominal values (no tolerance applied)
            nominal = []
            for var in matrix:
                if var in [[[0]], [0]]  : nominal.append([0])
                # Extract nominal values from each sublist
                else                    : nominal.append([sub[0] for sub in var])
            
            # Check if starting point is the nominal case
            if points == nominal:   return [total - 1], total - 1
            
            # Check all WCA iterations for match
            for iter_num in range(total - 1):
                if self.calculate_wca_values(iter_num, matrix) == points    :   return [iter_num], iter_num
            
            # Default to first iteration if no match found
            return [0], 0
        
        #? ============ NORMAL MODE LOGIC ============
        # Extract simple values from parameter matrix
        matrix_vals = self.extract_values(matrix)
        # Extract simple values from starting points
        point_vals  = [p[0] if isinstance(p, list) and p else p for p in points]
        
        if not pattern:
            # Simple index mode: only look at first parameter
            idx = matrix_vals[0].index(point_vals[0]) if matrix_vals[0] != [0] else 0
            # Return uniform indices for all parameters
            return dp.np.full(len(matrix) + 1, idx).tolist(), idx
        
        #? ============ PATTERN MODE LOGIC ============
        # Find index of each point value in its corresponding parameter list
        indices = []
        for i, (mat_vals, pt_val) in enumerate(zip(matrix_vals, point_vals)):
            if mat_vals == [0]:
                indices.append(0)  # Unused parameter
            else:
                try:
                    indices.append(mat_vals.index(pt_val))
                except ValueError:
                    indices.append(0)  # Default to first value if not found
        
        # Get dimensions of each parameter list
        lens    = [len(v) if v != [0] else 1 for v in matrix_vals]
        
        # Compute linear index from multi-dimensional indices
        itr     = sum(indices[i] * dp.np.prod(lens[i+1:]) for i in range(len(indices)-1)) + indices[-1]
        
        # Append linear index to indices list for reference
        indices.append(itr)
        
        return indices, itr

    def findPoint(self, matrix, index, pattern=True):
        """
        Generate parameter combinations starting from a given index.
        
        Args:
            matrix (list): Parameter matrix (X1-X10 lists)
            index (list): Starting index(es)
            pattern (bool, optional): True for Cartesian product,
                                     False for simple listing. Defaults to True.
                                     
        Returns:
            tuple: (parameter combinations subset, number of combinations)
            
        Note:
            - For WCA mode: Generates WCA iterations (3D structure)
            - For NORMAL mode with pattern=True: Cartesian product (2D array)
            - For NORMAL mode with pattern=False: Transposed matrix
        """
        # Detect operation mode
        if self.detect_mode(matrix) == "WCA":
            #? ============ WCA MODE LOGIC ============
            # Get active parameters and calculate total iterations
            active = self.get_active_wca_params(matrix)
            total = 2 ** len(active) + 1  # +1 for nominal case
            
            # Generate all WCA iterations
            wca_iters = []
            for iter_num in range(total):
                if iter_num == total - 1:
                    # Last iteration: nominal values only
                    wca_iters.append([sub[0] for sub in var] if var not in [[[0]], [0]] else [0] 
                                    for var in matrix)
                else:
                    # WCA iteration: apply tolerance based on binary encoding
                    wca_iters.append(self.calculate_wca_values(iter_num, matrix))
            
            # Extract subset starting from the given index
            start = index[-1] if index else 0
            subset = wca_iters[start:] if start < len(wca_iters) else []
            
            return subset, len(subset)
        
        #? ============ NORMAL MODE LOGIC ============
        # Extract simple values from parameter matrix
        matrix_vals = self.extract_values(matrix)
        
        if not pattern:
                #? ================= Sequential sweep =================
                # Pad each parameter list to max length by repeating last value
                max_len = max(len(v) if v != [0] else 1 for v in matrix_vals)
                padded = []
                for v in matrix_vals:
                    if v == [0]:
                        padded.append([0]*max_len)
                    else:
                        padded.append(v + [v[-1]]*(max_len - len(v)))
                # Transpose to iteration-wise rows
                Map2D = dp.np.array(padded).T.tolist()
                return Map2D, len(Map2D)
        
        #? ============ PATTERN MODE ============
        # Generate full Cartesian product of all parameter combinations
        
        # Get dimensions of each parameter list
        lens    = [len(v) if v != [0] else 1 for v in matrix_vals]
        
        # Total combinations = product of all dimensions
        total   = dp.np.prod(lens)
        
        if total == 0:  return dp.np.zeros((0, 10)), 0
        
        # Initialize parameter map: rows = combinations, columns = X1-X10
        map_data    = dp.np.zeros((total, 10))
        step        = total  # Start with total combinations
        
        # Generate Cartesian product efficiently using numpy operations
        for col in range(10):
            if matrix_vals[col] == [0]:
                
                # Unused parameter: fill column with zeros
                step //= 1  # Dimension is 1
                map_data[:, col] = 0
            else:
                # Active parameter: generate repeating pattern
                dim = lens[col]
                step //= dim  # Update step size for this dimension
                
                # Calculate repetition factor for this parameter's values
                repeat = total // (step * dim)
                # Fill column with repeating pattern of values
                map_data[:, col] = dp.np.tile(dp.np.repeat(matrix_vals[col], step), repeat)
        
        # Extract subset starting from the given index
        start   = index[-1] if index else 0
        subset  = map_data[start:] if start < len(map_data) else []
        
        return subset, len(subset)
    
    def findStart(self, matrix, index, pattern=True):
        """
        Get the starting portion of the parameter matrix.
        
        Args:
            matrix (list): Parameter matrix (X1-X10 lists)
            index (list): Starting index(es)
            pattern (bool, optional): True returns original structure,False returns sequential simple. Defaults to True.
                                     
        Returns:
            list: Starting portion of the matrix
            
        """
        # WCA mode or pattern mode: return original matrix structure
        if self.detect_mode(matrix) == "WCA" or pattern:
            return [row[:] for row in matrix]  # Shallow copy
        
        #? ============ NORMAL NON-PATTERN MODE ============
        # Extract simplified values and return appropriate subset
        matrix_vals = self.extract_values(matrix)
        start = index[-1] if index else 0
        
        # Return entire matrix if starting index is valid
        return matrix_vals if start < len(matrix_vals) else []
    
    def init_sim(self, maxThreads=1, X1=[[0]], X2=[[0]],X3=[[0]], X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]],X9=[[0]], X10=[[0]], model='DCDC',pattern=True):
        """
        Initialize simulation with parameter sweeps.
        
        Args:
            maxThreads (int, optional): Maximum threads for parallel execution. Defaults to 1.
            X1-X10 (list, optional): Parameter lists for each variable. Defaults to [[0]].
            model (str, optional): Simulation model type. Defaults to 'DCDC'.
            
        Returns: Processing: Self reference for method chaining ( don't have to make objects and extra calls for 
                    dependent functions such as FindPoint ... )
        """
        
        startPoint          =   None
        # Store all parameters in a single list
        self.sweepMatrix    =   [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
       
        self.maxThreads, self.model = maxThreads, model
        
        # Detect operation mode from parameter format
        self.mode = self.detect_mode(self.sweepMatrix)
        
        if self.mode == "WCA":

            # Build reduced matrix containing only FIRST WCA sublist for each Xi
            reduced_matrix = [var if var in ([[[0]], [0]]) else [var[0]] for var in self.sweepMatrix]

            # If user provided startPoint → determine its WCA iteration
            if startPoint is not None:
                self.idx, self.itrr = self.findIndex(startPoint, self.sweepMatrix, pattern=True)
            else:
                # Default: WCA iteration 0 using reduced matrix
                default_sp          = self.calculate_wca_values(0, reduced_matrix)
                self.idx, self.itrr = self.findIndex(default_sp, self.sweepMatrix, pattern=True)

            # Set startPoint to the resolved iteration
            self.startPoint = self.calculate_wca_values(self.itrr, self.sweepMatrix)

            # Build full WCA map
            active              = self.get_active_wca_params(self.sweepMatrix)
            self.wca_iterations = 2 ** len(active)
            self.Iterations     = self.wca_iterations + 1

            self.Map = []
            for iter_num in range(self.Iterations):
                if iter_num == self.Iterations - 1:
                    # Nominal values
                    self.Map.append([[sub[0] for sub in var] if var not in [[[0]], [0]] else [0]for var in self.sweepMatrix])
                else:
                    self.Map.append(self.calculate_wca_values(iter_num, self.sweepMatrix))

            # Slice WCA sequence from startPoint iteration
            self.Map = self.Map[self.itrr:]

            # Flatten for 2D representation
            self.Map2D = [
                sum((list(p) if isinstance(p, list) else [p] for p in row), [])for row in self.Map]

        else:
            #? ============ NORMAL INITIALIZATION ============
             # Set starting point or use default
            self.startPoint = [
                (var[0][0] if isinstance(var, list) and isinstance(var[0], list) else 0)
                if var not in ([[[0]], [0]]) else 0
                for var in self.sweepMatrix
            ]

            # Find starting index in parameter space
            self.idx, self.itrr = self.findIndex(self.startPoint, self.sweepMatrix, pattern)
            # Get starting matrix structure
            self.matrix = self.findStart(self.sweepMatrix, self.idx, pattern)
            # Generate parameter combinations
            self.Map2D, self.Iterations = self.findPoint(self.matrix, self.idx, pattern)
            # In normal mode, Map is same as Map2D (2D structure)
            self.Map = self.Map2D
        
        # Initialize iteration counter
        self.iterNumber = 0
        
        # initialize empty data matrices
        # MAT1-MAT6: For Peak, RMS & AVG Currents & Voltages MAT9-MAT13: For Dissipations, Electrical Stats, Temperatures, Thermal Stats & Controls
        # MAT7-MAT8: For FFT of Currents and Voltages
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations, dp.Y_Length[i]))) for i in list(range(1, 7)) + list(range(9, 14))]
        [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations * len(dp.harmonics), dp.Y_Length[i]))) for i in range(7, 9)]

        # if hierarchical simulations are enabled in JSON input file
        if dp.JSON['hierarchical']:
            # use hierarchicalSims function to determine count of paralleled simulations
            self.threads_vector         =   self.postProcessing.hierarchicalSims(self.Map)
            self.Simulations            =   len(self.threads_vector)
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
        return self  # Return self for method chaining

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
        if (Threads >= 1 and dp.JSON['parallel'] and not crash):
                res_list                        = dp.pmap.return_resistances(optstruct[l])
                P_aux                           = optstruct[l]['ModelVars']['Common']['Thermal']['Paux']

        # If a crash has occurred, access the first element of optstruct.
        elif (crash):
                res_list                        = dp.pmap.return_resistances(optstruct[0])
                P_aux                           = optstruct[0]['ModelVars']['Common']['Thermal']['Paux']

        # If single-threaded or not parallel, access the first element of optstruct.
        else:
                res_list                        = dp.pmap.return_resistances(optstruct)
                P_aux                           = optstruct['ModelVars']['Common']['Thermal']['Paux']

        # Return the list of resistances and auxiliary power.
        return res_list,P_aux
    
    def process_standalone_csvs(self, fileLog, saveMode='w'):
        """
        Post-process standalone CSV time-series simulation files.

        This function scans the CSV_TIME_SERIES folder and processes only files
        ending with `_Standalone.csv`. Each file is treated as one simulation
        iteration (ordered alphanumerically). The function computes:
            - RMS values
            - Average values
            - Minimum values
            - Maximum values
            - FFT spectra (harmonics-based)

        One row per standalone file is written to corresponding CSV MAP files:
            Standalone_RMS_Map.csv
            Standalone_AVG_Map.csv
            Standalone_MIN_Map.csv
            Standalone_MAX_Map.csv
            Standalone_FFT_Map.csv

        Headers from the time-series CSV files are preserved for all non-FFT outputs.

        Args:
            fileLog  : File logging object containing resultfolder paths.
            saveMode : File write mode ('w' = overwrite, 'a' = append). Default = 'w'.

        Returns:
            None
        """

        # ------------------------------------------------------------------
        # Directory paths
        # ------------------------------------------------------------------
        ts_dir  = f"{fileLog.resultfolder}/CSV_TIME_SERIES"
        map_dir = f"{fileLog.resultfolder}/CSV_MAPS"

        # ------------------------------------------------------------------
        # Collect standalone CSV files (sorted = iteration order)
        # ------------------------------------------------------------------
        files = sorted(
            f for f in os.listdir(ts_dir)
            if f.endswith("_Standalone.csv")
        )

        if not files:
            return

        # ------------------------------------------------------------------
        # Initialize result containers
        # ------------------------------------------------------------------
        RMS_rows, AVG_rows, MIN_rows, MAX_rows = [], [], [], []
        FFT_rows = []
        headers  = None

        # ------------------------------------------------------------------
        # Process each standalone file (1 file = 1 iteration)
        # ------------------------------------------------------------------
        for fname in files:
            path = os.path.join(ts_dir, fname)

            df = dp.pd.read_csv(path)
            if headers is None:
                headers = df.columns.tolist()

            data = df.to_numpy(dtype=dp.np.float64)

            T_vect = data[:, 0]        # time vector
            sigs   = data[:, 1:].T     # signals (shape = n_signals × time)

            # ---------------- Compute statistics ----------------
            RMS = self.postProcessing.rms_avg('RMS', sigs, T_vect)
            AVG = self.postProcessing.rms_avg('AVG', sigs, T_vect)
            MIN = dp.np.nanmin(sigs, axis=1)
            MAX = dp.np.nanmax(sigs, axis=1)

            # ---------------- FFT computation ----------------
            FFT = self.postProcessing.FFT_mat(T_vect, sigs)

            # ---------------- Store results ----------------
            RMS_rows.append(RMS.tolist())
            AVG_rows.append(AVG.tolist())
            MIN_rows.append(MIN.tolist())
            MAX_rows.append(MAX.tolist())
            FFT_rows.extend(FFT.tolist())   # FFT produces multiple harmonic rows

        # ------------------------------------------------------------------
        # Save MAP CSV outputs (compact single-line style like your framework)
        # ------------------------------------------------------------------
        sig_headers = headers[1:]  # exclude time column

        [self.postProcessing.csv_append_rows(
            f"{map_dir}/Standalone_{name}_Map.csv",
            data,
            headers=sig_headers if name != "FFT" else None,
            save_mode=saveMode
        ) for name, data in zip(
            ["RMS", "AVG", "MIN", "MAX", "FFT"],
            [RMS_rows, AVG_rows, MIN_rows, MAX_rows, FFT_rows]
        )]

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

        # iteration_range is determined based on whether hierarchical parallelization is enabled
        iteration_range     = list(range(sum(self.threads_vector[0:itr]),sum(self.threads_vector[0:itr+1]))) if dp.JSON['hierarchical'] else list(range(itr*simutil.Threads,simutil.Threads*(itr+1)))

        # Loop through each thread in the current simulation batch
        # For each thread, generate the result file and process the CSV data
        # Normalize the results and convert them to a numpy array
        # Remove NaN values from each sub-array in the nested results
        # Update the model variables and retrieve resistance values and auxiliary power
        # Perform specified operations on the time vector and normalized results
        # threads_idx is calculated based on whether hierarchical parallelization is enabled
        for l in range(simutil.Threads):
            results_TF                          = self.postProcessing.gen_result(fileLog.resultfolder+"/CSV_TIME_SERIES",iteration_range[l],fileLog.utc)
            nestedresults                       = dp.np.array(self.postProcessing.norm_results_csv(results_TF))
            nestedresults_l                     = dp.np.array([dp.np.array(subarr,dtype=dp.np.float64)[~dp.pd.isnull(dp.np.array(subarr))] for subarr in nestedresults])
            res_list,P_aux                      = self.var_update(simutil.Threads,crash,optstruct,l)
            T_vect                              = nestedresults_l[0]
            threads_idx                         = l+sum(self.threads_vector[0:itr]) if dp.JSON['hierarchical'] else l+itr*simutil.Threads

            # loop through predefined matrix operations and apply them to the corresponding data matrices
            # Mat1: Peak Currents, Mat2: RMS Currents, Mat3: AVG Currents
            # Mat4: Peak Voltages, Mat5: RMS Voltages, Mat6:
            for mat_name, mode, sl in dp.matrix_ops:
                getattr(self, mat_name)[threads_idx, :] = self.operation(T_vect, nestedresults_l[sl, :], mode)

            # Mat7: FFT of Currents, Mat8: FFT of Voltages
            # Mat9: Dissipations, Mat10: Electrical Stats, Mat11: Temperatures
            # Mat12: Thermal Stats, Mat13: Controls

            self.MAT7[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect,nestedresults_l[1 : dp.Y_list[1]+1 , :])                            # FFT_Current
            self.MAT8[threads_idx*len(dp.harmonics) : len(dp.harmonics)*(l+1)+(threads_idx-l)*len(dp.harmonics), :] =  self.postProcessing.FFT_mat(T_vect, nestedresults_l[sum(dp.Y_list[0:2]) : sum(dp.Y_list[0:3]) , :])    # FFT_Voltage
            self.MAT9[threads_idx,:]  = self.postProcessing.dissipations(nestedresults_l,res_list,self.MAT2,threads_idx,self.MAT7)                                                                                            # Dissipations
            self.MAT12[threads_idx,:] = self.postProcessing.therm_stats(self.MAT_list,threads_idx,P_aux)                                                                                                                      # thermal_stats
        self.MAT_list[6:8] = [self.MAT7[:self.Iterations * len(dp.harmonics)], self.MAT8[:self.Iterations * len(dp.harmonics)]]

        # Save the data matrices to CSV files in the specified results folder
        # Each matrix is saved with a corresponding name from map_names
        # The save_mode parameter determines whether to append or overwrite the files
        [self.postProcessing.csv_append_rows(f"{fileLog.resultfolder}/CSV_MAPS/{name}_Map.csv", data.tolist(), save_mode=saveMode) for name, data in zip(dp.map_names, self.MAT_list)]
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------



import math
import numpy as np

class Processing:
    """Class for processing parameter sweeps in both WCA (Worst Case Analysis) 
    and normal modes for simulation initialization."""
    
    def __init__(self):
        """Initialize Processing class instance."""
        pass
    
    def detect_mode(self, Xs):
        for var in Xs:
            if var == [[0]] or var == [0]:
                continue
            for sub in var:
                # Protect against flattened matrix (sub can be an int)
                if not isinstance(sub, list):
                    return "NORMAL"
                # WCA format
                if len(sub) == 4:
                    return "WCA"
                # Normal format
                elif len(sub) == 1:
                    return "NORMAL"

        return "NORMAL"

    def binary_index(self, iteration, index, active):
        """
        Extract correct bit so that X1 changes slowest and Xn fastest.
        """
        # index is global parameter index 0..9
        # active is list of active WCA parameter indices (e.g. [0,1,2])

        active_index = active.index(index)        # position inside active list
        n_active = len(active)

        # Reverse bit significance
        bit_position = n_active - 1 - active_index

        bit_value = (iteration >> bit_position) & 1
        return bit_value
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
        """
        Calculate tolerance-adjusted value for WCA analysis.
        
        Args:
            Abs_rel (bool): True for absolute tolerance (tol <= 1), False for relative (%)
            iteration (int): Current WCA iteration number
            index (int): Parameter index for binary encoding
            nom (float): Nominal value
            tol (float): Tolerance value
            
        Returns:
            float: Tolerance-adjusted value
            
        Logic:
            - If binary_index(iteration, index) == 1: Apply upper tolerance
            - If binary_index(iteration, index) == 0: Apply lower tolerance
            - For absolute tolerance (tol <= 1):
                Upper: nom * tol, Lower: nom / tol
            - For relative tolerance (tol > 1, interpreted as percentage):
                Upper: nom * (1 + tol/100), Lower: nom * (1 - tol/100)
        """
        active = self.get_active_wca_params(self.sweepMatrix)

        # Check the bit for this parameter in current iteration
        if self.binary_index(iteration, index, active):
            # Bit is 1: apply upper tolerance (increase value)
            return nom * tol if Abs_rel else nom * (1 + tol)
        # Bit is 0: apply lower tolerance (decrease value)
        return nom / tol if Abs_rel else nom * (1 - tol)
    
    def calculate_wca_values(self, iteration, Xs):
        """
        Calculate WCA values for all parameters in a given iteration.
        
        Args:
            iteration (int): Current WCA iteration number
            Xs (list): List of parameter lists for X1-X10
            
        Returns:
            list: 3D list of calculated WCA values for all parameters
            
        Structure:
            Returns a list where each element corresponds to one parameter (X1-X10),
            containing a list of calculated values for that parameter's sublists.
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
        Identify which parameters participate in WCA analysis.
        
        Args:
            Xs (list): List of parameter lists for X1-X10
            
        Returns:
            list: Indices of parameters that have WCA format (4 elements per sublist)
            
        Note:
            Only parameters with [nominal, tolerance, min, max] format participate
            in WCA binary encoding. Others are treated as fixed values.
        """
        return [i for i, var in enumerate(Xs) 
                if var not in [[[0]], [0]] and len(var) > 0 and len(var[0]) == 4]
    
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
        return [[sub[0] if isinstance(sub, list) and sub else sub for sub in var] 
                if var not in [[[0]], [0]] else [0] for var in Xs]
    
    # ================== MAIN FUNCTIONS ==================
    
    def findIndex(self, points, matrix, pattern=True):
        """
        Find the starting index for parameter sweeps.
        
        Args:
            points (list): Starting point values (format depends on mode)
            matrix (list): Parameter matrix (X1-X10 lists)
            pattern (bool, optional): True for full Cartesian product,
                                     False for simple index. Defaults to True.
                                     
        Returns:
            tuple: (indices list, linear_index)
            
        Note:
            - For WCA mode: Finds which WCA iteration matches the starting point
            - For NORMAL mode with pattern=True: Computes multi-dimensional index
            - For NORMAL mode with pattern=False: Simple single index lookup
        """
        # Detect operation mode from parameter format
        if self.detect_mode(matrix) == "WCA":
            # ============ WCA MODE LOGIC ============
            # Get active parameters that participate in WCA
            active = self.get_active_wca_params(matrix)
            # Total WCA iterations: 2^n combinations + 1 nominal case
            total = 2 ** len(active) + 1
            
            # Generate nominal values (no tolerance applied)
            nominal = []
            for var in matrix:
                if var in [[[0]], [0]]:
                    nominal.append([0])
                else:
                    # Extract nominal values from each sublist
                    nominal.append([sub[0] for sub in var])
            
            # Check if starting point is the nominal case
            if points == nominal:
                return [total - 1], total - 1
            
            # Check all WCA iterations for match
            for iter_num in range(total - 1):
                if self.calculate_wca_values(iter_num, matrix) == points:
                    return [iter_num], iter_num
            
            # Default to first iteration if no match found
            return [0], 0
        
        # ============ NORMAL MODE LOGIC ============
        # Extract simple values from parameter matrix
        matrix_vals = self.extract_values(matrix)
        # Extract simple values from starting points
        point_vals = [p[0] if isinstance(p, list) and p else p for p in points]
        
        if not pattern:
            # Simple index mode: only look at first parameter
            idx = matrix_vals[0].index(point_vals[0]) if matrix_vals[0] != [0] else 0
            # Return uniform indices for all parameters
            return np.full(len(matrix) + 1, idx).tolist(), idx
        
        # ============ PATTERN MODE LOGIC ============
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
        lens = [len(v) if v != [0] else 1 for v in matrix_vals]
        
        # Compute linear index from multi-dimensional indices
        # Formula: Σ(indices[i] * Π(dimensions of subsequent parameters))
        prod = np.prod
        itr = sum(indices[i] * prod(lens[i+1:]) for i in range(len(indices)-1)) + indices[-1]
        
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
            # ============ WCA MODE LOGIC ============
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
        
        # ============ NORMAL MODE LOGIC ============
        # Extract simple values from parameter matrix
        matrix_vals = self.extract_values(matrix)
        
        if not pattern:
                # ================= Sequential sweep =================
                # Pad each parameter list to max length by repeating last value
                max_len = max(len(v) if v != [0] else 1 for v in matrix_vals)
                padded = []
                for v in matrix_vals:
                    if v == [0]:
                        padded.append([0]*max_len)
                    else:
                        padded.append(v + [v[-1]]*(max_len - len(v)))
                # Transpose to iteration-wise rows
                Map2D = np.array(padded).T.tolist()
                return Map2D, len(Map2D)
        
        # ============ PATTERN MODE ============
        # Generate full Cartesian product of all parameter combinations
        
        # Get dimensions of each parameter list
        lens = [len(v) if v != [0] else 1 for v in matrix_vals]
        # Total combinations = product of all dimensions
        total = np.prod(lens)
        
        if total == 0:
            return np.zeros((0, 10)), 0
        
        # Initialize parameter map: rows = combinations, columns = X1-X10
        map_data = np.zeros((total, 10))
        step = total  # Start with total combinations
        
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
                map_data[:, col] = np.tile(np.repeat(matrix_vals[col], step), repeat)
        
        # Extract subset starting from the given index
        start = index[-1] if index else 0
        subset = map_data[start:] if start < len(map_data) else []
        
        return subset, len(subset)
    
    def findStart(self, matrix, index, pattern=True):
        """
        Get the starting portion of the parameter matrix.
        
        Args:
            matrix (list): Parameter matrix (X1-X10 lists)
            index (list): Starting index(es)
            pattern (bool, optional): True returns original structure,
                                     False returns simplified structure. Defaults to True.
                                     
        Returns:
            list: Starting portion of the matrix
            
        Note:
            - For WCA mode or pattern=True: Returns copy of original structure
            - For NORMAL mode with pattern=False: Returns simplified values
        """
        # WCA mode or pattern mode: return original matrix structure
        if self.detect_mode(matrix) == "WCA" or pattern:
            return [row[:] for row in matrix]  # Shallow copy
        
        # ============ NORMAL NON-PATTERN MODE ============
        # Extract simplified values and return appropriate subset
        matrix_vals = self.extract_values(matrix)
        start = index[-1] if index else 0
        
        # Return entire matrix if starting index is valid
        return matrix_vals if start < len(matrix_vals) else []
    
    def init_sim(self, maxThreads=1, startPoint=None, X1=[[0]], X2=[[0]], 
                 X3=[[0]], X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], 
                 X9=[[0]], X10=[[0]], pattern=True, model='DCDC'):
        """
        Initialize simulation with parameter sweeps.
        
        Args:
            maxThreads (int, optional): Maximum threads for parallel execution. Defaults to 1.
            startPoint (list, optional): Starting parameter values. Defaults to None.
            X1-X10 (list, optional): Parameter lists for each variable. Defaults to [[0]].
            pattern (bool, optional): True for Cartesian product, False for simple listing. Defaults to True.
            model (str, optional): Simulation model type. Defaults to 'DCDC'.
            
        Returns:
            Processing: Self reference for method chaining
            
        Note:
            Auto-detects WCA vs NORMAL mode based on parameter format.
            WCA: Parameters with [nominal, tolerance, min, max] format
            NORMAL: Parameters with single values only
        """
        # Store all parameters in a single list
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
       
        self.maxThreads, self.model = maxThreads, model
        
        # Detect operation mode from parameter format
        self.mode = self.detect_mode(self.sweepMatrix)
        
        if self.mode == "WCA":

            # Build reduced matrix containing only FIRST WCA sublist for each Xi
            reduced_matrix = [var if var in ([[[0]], [0]]) else [var[0]] for var in self.sweepMatrix]

            # If user provided startPoint → determine its WCA iteration
            if startPoint is not None:
                self.idx, self.itrr = self.findIndex(startPoint, self.sweepMatrix, pattern=True)
                print(f"WCA mode detected. Using user startPoint at WCA iteration {self.itrr}.")
            else:
                # Default: WCA iteration 0 using reduced matrix
                default_sp = self.calculate_wca_values(0, reduced_matrix)
                self.idx, self.itrr = self.findIndex(default_sp, self.sweepMatrix, pattern=True)
                print(f"WCA mode detected. Default startPoint = iteration 0 values.")

            # Set startPoint to the resolved iteration
            self.startPoint = self.calculate_wca_values(self.itrr, self.sweepMatrix)

            # Build full WCA map
            active = self.get_active_wca_params(self.sweepMatrix)
            self.wca_iterations = 2 ** len(active)
            self.Iterations = self.wca_iterations + 1

            self.Map = []
            for iter_num in range(self.Iterations):
                if iter_num == self.Iterations - 1:
                    # Nominal values
                    self.Map.append(
                        [[sub[0] for sub in var] if var not in [[[0]], [0]] else [0]
                        for var in self.sweepMatrix]
                    )
                else:
                    self.Map.append(self.calculate_wca_values(iter_num, self.sweepMatrix))

            # Slice WCA sequence from startPoint iteration
            self.Map = self.Map[self.itrr:]

            # Flatten for 2D representation
            self.Map2D = [
                sum((list(p) if isinstance(p, list) else [p] for p in row), [])
                for row in self.Map
            ]


        else:
            # ============ NORMAL INITIALIZATION ============
            self.pattern = pattern
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
        print("self.startPoint =", self.startPoint)
        
        return self  # Return self for method chaining
    

# ================== TESTING EXAMPLES ==================

if __name__ == "__main__":
    processing = Processing()
    
    # ============ NORMAL MODE EXAMPLE ============
    print("=== NORMAL MODE TEST ===")
    # Normal input: single values in sublists
    # For NORMAL mode (single values)
    X1 = [[v] for v in range(10, 41, 5)]  # [[10], [15], [20], ..., [40]]
    X2 = [[v] for v in range(100, 201, 50)]  # [[100], [150], [200]]
    X3 = [[v] for v in range(5, 26, 10)]    # [[5], [15], [25]]

    
    sim = processing.init_sim(
        maxThreads=2,
        X1=X1, X2=X2, X3=X3,
        X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]],
        pattern=True
    )
    
    print("Normal mode - All combinations:")
    for i, combo in enumerate(sim.Map):
        print(f"  Iteration {i}: {combo}")
    
    # ============ WCA MODE EXAMPLE ============
    print("\n=== WCA MODE TEST ===")
    # WCA input: [nominal, tolerance, min, max] format
    X1 = [[10, 0.1, 5, 15], [20, 0.2, 15, 25]]
    X2 = [[100, 0.5, 50, 150]]
    X3 = [[6.5, 0.1, 5, 10], [15.5, 0.2, 10, 20], [25.5, 0.3, 20, 30]]  
    
    sim = processing.init_sim(
        maxThreads=2,
        # startPoint=  [[5, 15], [150], [10, 20, 30], [0], [0], [0], [0], [0], [0], [0]],
        X1=X1, X2=X2,
        X3=X3, X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]]
    )
    
    print("WCA mode - All combinations:")
    for i, combo in enumerate(sim.Map):
        print(f"  Iteration {i}: {combo}")
    
    x1,x2,x3,x4,x5,x6,x7,x8,x9,x10 = range(10)
    print(sim.Map[0][x1][0])  # First iteration values

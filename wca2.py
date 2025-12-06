import math
import numpy as np

class Processing:
    def __init__(self):
        pass
    
    def detect_mode(self, Xs):
        """Detect if input is WCA mode or normal mode."""
        for var_data in Xs:
            if var_data == [[0]] or var_data == [0]:
                continue
            for sublist in var_data:
                if len(sublist) == 4:
                    return "WCA"
                elif len(sublist) == 1:
                    return "NORMAL"
        return "NORMAL"
    
    def binary_index(self, iteration, index):
        """Calculate binary index for WCA (0 or 1)."""
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
        """Calculate tolerance value."""
        if Abs_rel:
            if self.binary_index(iteration, index):
                return nom * tol
            else:
                return nom / tol
        else:
            if self.binary_index(iteration, index):
                return nom * (1 + tol)
            else:
                return nom * (1 - tol)
    
    def calculate_wca_values(self, iteration, Xs):
        """Calculate WCA values for a given iteration."""
        results = []
        for i, var_data in enumerate(Xs):
            if var_data == [[0]] or var_data == [0]:
                results.append([0])
                continue
            
            wca_values = []
            for sublist in var_data:
                if len(sublist) == 1:
                    wca_values.append(sublist[0])
                elif len(sublist) == 4:
                    nom, tol, min_val, max_val = sublist
                    
                    if tol <= 1:
                        x = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                    else:
                        x = self.funtol(Abs_rel=False, iteration=iteration, index=i, nom=nom, tol=tol/100.0)
                    
                    wca_value = min(max(x, min_val), max_val)
                    wca_values.append(wca_value)
                else:
                    wca_values.append(sublist[0])
            
            results.append(wca_values)
            
        return results
    
    def get_active_wca_parameters(self, Xs):
        """Get list of parameters that participate in WCA."""
        active_params = []
        for i, var_data in enumerate(Xs):
            if var_data != [[0]] and var_data != [0] and len(var_data) > 0:
                if len(var_data[0]) == 4:
                    active_params.append(i)
        return active_params
    
    def get_parameter_values(self, Xs):
        """Extract simple values from parameter lists for normal mode."""
        values = []
        for var_data in Xs:
            if var_data == [[0]] or var_data == [0]:
                values.append([0])
            else:
                # Extract single values from each sublist
                param_values = []
                for sublist in var_data:
                    if isinstance(sublist, list) and len(sublist) > 0:
                        param_values.append(sublist[0])
                    else:
                        param_values.append(sublist)
                values.append(param_values)
        return values
    
    # ================== MAIN FUNCTIONS ==================
    
    def findIndex(self, points, matrix, pattern=True):
        """
        Finds the starting index in the matrix.
        """
        mode = self.detect_mode(matrix)
        
        if mode == "WCA":
            # WCA LOGIC
            active_params = self.get_active_wca_parameters(matrix)
            num_active = len(active_params)
            total_wca_iterations = 2 ** num_active + 1
            
            # Generate nominal values
            nominal_values = []
            for var_data in matrix:
                if var_data == [[0]] or var_data == [0]:
                    nominal_values.append([0])
                else:
                    nominal_sublist = []
                    for sublist in var_data:
                        if len(sublist) == 1:
                            nominal_sublist.append(sublist[0])
                        else:
                            nominal_sublist.append(sublist[0])
                    nominal_values.append(nominal_sublist)
            
            if points == nominal_values:
                indices = [total_wca_iterations - 1]
                return indices, indices[0]
            
            for iteration in range(total_wca_iterations - 1):
                wca_values = self.calculate_wca_values(iteration, matrix)
                if wca_values == points:
                    indices = [iteration]
                    return indices, iteration
            
            indices = [0]
            return indices, 0
            
        else:
            # NORMAL LOGIC
            if pattern:
                # For normal pattern mode, extract simple values
                matrix_values = self.get_parameter_values(matrix)
                point_values = []
                
                # Convert points to simple values
                for i, point in enumerate(points):
                    if isinstance(point, list) and len(point) > 0:
                        point_values.append(point[0])
                    else:
                        point_values.append(point)
                
                indices = []
                for i in range(len(point_values)):
                    if matrix_values[i] == [0]:
                        indices.append(0)
                    else:
                        try:
                            idx = matrix_values[i].index(point_values[i])
                            indices.append(idx)
                        except ValueError:
                            indices.append(0)
                
                # Compute weighted sum for linear index
                lengths = [len(vals) if vals != [0] else 1 for vals in matrix_values]
                itr = sum(
                    indices[i] * np.prod([lengths[j] for j in range(i + 1, len(matrix_values))])
                    for i in range(len(indices) - 1)
                ) + indices[-1]
                indices.append(itr)
                
            else:
                # Simple index finding
                matrix_values = self.get_parameter_values(matrix)
                if matrix_values[0] == [0]:
                    itr = 0
                else:
                    point_val = points[0][0] if isinstance(points[0], list) else points[0]
                    itr = matrix_values[0].index(point_val)
                indices = np.full(len(matrix) + 1, itr).tolist()
            
            return indices, itr
    
    def findPoint(self, matrix, index, pattern=True):
        """
        Get parameter combinations starting from index.
        """
        mode = self.detect_mode(matrix)
        
        if mode == "WCA":
            # WCA LOGIC - returns 3D structure
            active_params = self.get_active_wca_parameters(matrix)
            num_active = len(active_params)
            total_iterations = 2 ** num_active + 1
            
            all_wca_iterations = []
            for iteration in range(total_iterations):
                if iteration == total_iterations - 1:
                    nominal_values = []
                    for var_data in matrix:
                        if var_data == [[0]] or var_data == [0]:
                            nominal_values.append([0])
                        else:
                            nominal_sublist = []
                            for sublist in var_data:
                                if len(sublist) == 1:
                                    nominal_sublist.append(sublist[0])
                                else:
                                    nominal_sublist.append(sublist[0])
                            nominal_values.append(nominal_sublist)
                    all_wca_iterations.append(nominal_values)
                else:
                    wca_values = self.calculate_wca_values(iteration, matrix)
                    all_wca_iterations.append(wca_values)
            
            start_idx = index[-1] if index else 0
            subset = all_wca_iterations[start_idx:] if start_idx < len(all_wca_iterations) else []
            
            return subset, len(subset)
            
        else:
            # NORMAL LOGIC - returns 2D structure (no nested sublists)
            if not pattern:
                # Simple case - just return matrix values
                matrix_values = self.get_parameter_values(matrix)
                
                # Find max length
                max_len = max(len(vals) for vals in matrix_values)
                
                # Pad and transpose
                padded = []
                for vals in matrix_values:
                    if vals == [0]:
                        padded.append([0] * max_len)
                    else:
                        padded_vals = vals + [0] * (max_len - len(vals))
                        padded.append(padded_vals)
                
                padded = np.array(padded).T
                return padded, len(padded)
            
            # Pattern mode - generate Cartesian product
            matrix_values = self.get_parameter_values(matrix)
            
            # Get dimensions
            dimensions = []
            for vals in matrix_values:
                if vals == [0]:
                    dimensions.append(1)
                else:
                    dimensions.append(len(vals))
            
            total_combinations = np.prod(dimensions)
            
            if total_combinations == 0:
                return np.zeros((0, 10)), 0
            
            # Generate parameter map
            ParametersMap = np.zeros((total_combinations, 10))
            
            step_size = total_combinations
            for col in range(10):
                if matrix_values[col] == [0]:
                    step_size //= 1
                    ParametersMap[:, col] = 0
                else:
                    dim = dimensions[col]
                    step_size //= dim
                    repeat_factor = total_combinations // (step_size * dim)
                    ParametersMap[:, col] = np.tile(
                        np.repeat(matrix_values[col], step_size), 
                        repeat_factor
                    )
            
            # Get subset starting from index
            start_idx = index[-1] if index else 0
            subset = ParametersMap[start_idx:] if start_idx < len(ParametersMap) else []
            
            return subset, len(subset)
    
    def findStart(self, matrix, index, pattern=True):
        """
        Get starting portion of the matrix.
        """
        mode = self.detect_mode(matrix)
        
        if mode == "WCA":
            # For WCA, return original structure
            return [row[:] for row in matrix]
            
        else:
            # NORMAL LOGIC
            if pattern:
                return [row[:] for row in matrix]
            
            # Get matrix values
            matrix_values = self.get_parameter_values(matrix)
            
            start_idx = index[-1] if index else 0
            # Create a simple list representation
            if start_idx < len(matrix_values):
                return matrix_values
            else:
                return []
    
    def init_sim(self, maxThreads=1, startPoint=None, 
                 X1=[[0]], X2=[[0]], X3=[[0]], X4=[[0]], X5=[[0]], 
                 X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]], 
                 pattern=True, model='DCDC'):
        """
        Initialize simulation for both WCA and normal modes.
        """
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
        
        # Set default start point if not provided
        if startPoint is None:
            self.startPoint = self._get_default_startpoint()
        else:
            self.startPoint = startPoint
            
        self.maxThreads = maxThreads
        self.model = model
        
        # Detect mode
        self.mode = self.detect_mode(self.sweepMatrix)
        
        if self.mode == "WCA":
            # WCA initialization
            active_params = self.get_active_wca_parameters(self.sweepMatrix)
            num_active = len(active_params)
            self.wca_iterations = 2 ** num_active
            self.Iterations = self.wca_iterations + 1
            
            # Generate WCA map (3D structure)
            self.Map = []
            for iteration in range(self.Iterations):
                if iteration == self.Iterations - 1:
                    # Nominal iteration
                    nominal_values = []
                    for var_data in self.sweepMatrix:
                        if var_data == [[0]] or var_data == [0]:
                            nominal_values.append([0])
                        else:
                            nominal_sublist = []
                            for sublist in var_data:
                                if len(sublist) == 1:
                                    nominal_sublist.append(sublist[0])
                                else:
                                    nominal_sublist.append(sublist[0])
                            nominal_values.append(nominal_sublist)
                    self.Map.append(nominal_values)
                else:
                    # WCA iteration
                    wca_values = self.calculate_wca_values(iteration, self.sweepMatrix)
                    self.Map.append(wca_values)
            
            # For compatibility, also create a 2D map
            self.Map2D = []
            for wca_iteration in self.Map:
                flat_row = []
                for param_values in wca_iteration:
                    if isinstance(param_values, list):
                        flat_row.extend(param_values)
                    else:
                        flat_row.append(param_values)
                self.Map2D.append(flat_row)
            
        else:
            # NORMAL initialization
            self.pattern = pattern
            
            # Find index
            self.idx, self.itrr = self.findIndex(self.startPoint, self.sweepMatrix, self.pattern)
            
            # Get starting matrix
            self.matrix = self.findStart(self.sweepMatrix, self.idx, self.pattern)
            
            # Get parameter combinations (2D array, no nested sublists)
            self.Map2D, self.Iterations = self.findPoint(self.matrix, self.idx, self.pattern)
            
            # For normal mode, Map is the same as Map2D (2D structure)
            self.Map = self.Map2D
            
        self.iterNumber = 0
        
        return self
    
    def _get_default_startpoint(self):
        """Get default start point."""
        default_point = []
        for var_data in self.sweepMatrix:
            if var_data == [[0]] or var_data == [0]:
                default_point.append([0])
            else:
                first_values = []
                for sublist in var_data:
                    if isinstance(sublist, list) and len(sublist) > 0:
                        first_values.append(sublist[0])
                    else:
                        first_values.append(sublist)
                default_point.append(first_values)
        return default_point
    



processing = Processing()

# Normal input (single values in sublists)
X1 = [[10], [20]]
X2 = [[100]]
X3 = [[5], [15], [25]]

sim = processing.init_sim(
    maxThreads=2,
    startPoint=[[10], [100], [5], [0], [0], [0], [0], [0], [0], [0]],
    X1=X1, X2=X2, X3=X3,
    X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]],
    pattern=True
)


# Print all iterations
print("All combinations :",sim.Map)







# WCA input
X1 = [[10, 0.1, 5, 15], [20, 0.2, 15, 25]]
X2 = [[100, 0.5, 50, 150]]

sim = processing.init_sim(
    maxThreads=2,
    startPoint=[[10, 20], [100], [0], [0], [0], [0], [0], [0], [0], [0]],
    X1=X1, X2=X2,
    X3=[[0]], X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]]
)
    
print("All combinations :",sim.Map)

import math
import numpy as np

class Processing:
    def __init__(self):
        pass
    
    def binary_index(self, iteration, index):
        """Calculate binary index for WCA (0 or 1)."""
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
        """Calculate tolerance value."""
        print("binidx = ",self.binary_index(iteration, index))
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
            # Handle unused variables
            if var_data == [[0]] or var_data == [0]:
                results.append([0])  # Single value 0
                continue
            
            wca_values = []
            # var_data is a list of sublists
            for sublist in var_data:
                if len(sublist) == 1:
                    # Single value, no WCA
                    wca_values.append(sublist[0])
                else:
                    # WCA parameters: [nom, tol, min, max]
                    nom, tol, min_val, max_val = sublist[:4]
                    
                    if tol <= 1:
                        # Absolute tolerance
                        x = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                    else:
                        # Relative tolerance (%)
                        x = self.funtol(Abs_rel=False, iteration=iteration, index=i, nom=nom, tol=tol)
                    
                    # Clamp to min/max bounds
                    wca_value = min(max(x, min_val), max_val)
                    wca_values.append(wca_value)
            
            results.append(wca_values)
            
        return results
    
    def get_active_parameters(self, Xs):
        """Get list of parameters that participate in WCA."""
        active_params = []
        for i, var_data in enumerate(Xs):
            if var_data != [[0]] and var_data != [0] and len(var_data[0]) > 1:
                active_params.append(i)
        return active_params
    
    def init_sim_wca(self, startPoint, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, 
                     maxThreads=1, model='DCDC'):
        """
        Initialize WCA simulation.
        
        Parameters:
        -----------
        startPoint: Starting parameter values (with WCA format)
        X1-X10: Parameter lists with WCA format [[nom, tol, min, max], ...]
        maxThreads: Maximum threads for parallel execution
        model: Model type
        
        Returns:
        --------
        Map: 3D array of shape (iterations, num_variables, variable_values)
        """
        # Store sweep parameters
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
        self.startPoint = startPoint
        
        # Get active parameters (those that participate in WCA)
        self.active_params = self.get_active_parameters(self.sweepMatrix)
        num_active = len(self.active_params)
        
        # Calculate number of WCA iterations (2^num_active + 1 for nominal)
        self.wca_iterations = 2 ** num_active
        self.total_iterations = self.wca_iterations + 1  # +1 for nominal case
        
        # Generate the WCA map
        self.Map = []
        
        # Generate WCA combinations
        for iteration in range(self.total_iterations):
            if iteration == self.total_iterations - 1:
                # Last iteration: nominal values only
                nominal_values = []
                for i, var_data in enumerate(self.sweepMatrix):
                    if var_data == [[0]] or var_data == [0]:
                        nominal_values.append([0])
                    else:
                        # Extract nominal values from each sublist
                        nominal_sublist = []
                        for sublist in var_data:
                            if len(sublist) == 1:
                                nominal_sublist.append(sublist[0])
                            else:
                                nominal_sublist.append(sublist[0])  # nominal value
                        nominal_values.append(nominal_sublist)
                self.Map.append(nominal_values)
            else:
                # WCA iterations
                wca_values = self.calculate_wca_values(iteration, self.sweepMatrix)
                self.Map.append(wca_values)
        
        # Set iteration tracking
        self.Iterations = self.total_iterations
        self.iterNumber = 0
        
        # Calculate Cartesian product for reference (if needed)
        # This is for the parameter space exploration aspect
        cartesian_sizes = []
        for var_data in self.sweepMatrix:
            if var_data == [[0]] or var_data == [0]:
                cartesian_sizes.append(1)
            else:
                cartesian_sizes.append(len(var_data))
        
        self.cartesian_total = np.prod(cartesian_sizes)
        print(f"Cartesian product total combinations: {self.cartesian_total}")
        return self
    
    def findIndex(self, points, matrix, pattern=True):
        """Find index for WCA start point."""
        # For WCA, we need to find which WCA iteration corresponds to startPoint
        indices = []
        
        if pattern:
            # Find matching iteration for WCA start point
            for i in range(self.total_iterations):
                current_values = self.calculate_wca_values(i, matrix)
                if current_values == points:
                    indices = [i]
                    break
            if not indices:
                # Fallback to nominal
                indices = [self.total_iterations - 1]
        else:
            # Simple index finding for non-WCA mode
            indices = [matrix[0].index(points[0])]
        
        return indices, indices[0] if indices else 0
    
    def findPoint(self, matrix, index, pattern=True):
        """Get WCA iterations starting from index."""
        if not pattern:
            # For non-WCA mode
            max_len = max(len(row) for row in matrix)
            padded_matrix = [row + [0] * (max_len - len(row)) for row in matrix]
            padded_matrix = np.array(padded_matrix).T
            return padded_matrix, len(padded_matrix)
        
        # For WCA: return subset of Map starting from index
        start_idx = index[-1] if index else 0
        subset = self.Map[start_idx:] if start_idx < len(self.Map) else []
        return subset, len(subset)
    
    def findStart(self, matrix, index, pattern=True):
        """Get starting matrix for WCA."""
        if pattern:
            # For WCA, return the WCA matrix structure
            return [row[:] for row in matrix]
        
        # For non-WCA mode
        subset = np.array(matrix[index[-1]:]) if index else np.array(matrix)
        return subset.T.tolist()
    
    
    
  
# Example usage with your WCA input
processing = Processing()

# Parse your JSON input
X1 = [[10], [20]]
X2 = [[100]]
X3 = [[5], [15], [25]]
X4 = [[0]]
X5 = [[0]]
X6 = [[0]]
X7 = [[0]]
X8 = [[0]]
X9 = [[0]]
X10 = [[0]]

startPoint = [
    [10, 20],  # X1 nominal values
    [100],     # X2 nominal
    [5, 15, 25],  # X3 nominal
    [0],      # X4 nominal
    [0],    # X5 nominal
    [0],       # X6 nominal
    [0], [0], [0], [0]  # Unused
]

# Initialize WCA simulation
sim = processing.init_sim_wca(
    startPoint=startPoint,
    X1=X1, X2=X2, X3=X3, X4=X4, X5=X5, X6=X6,
    X7=X7, X8=X8, X9=X9, X10=X10,
    maxThreads=4
)

# Access the generated Map
print(f"Total iterations: {sim.Iterations}")
print(f"Map shape: {len(sim.Map)} x {len(sim.Map[0]) if sim.Map else 0}")

# Print first WCA iteration
print("\nFirst WCA iteration:")
for i, param_values in enumerate(sim.Map[0]):
    print(f"X{i+1}: {param_values}")

# Print nominal iteration (last one)
print(f"\nNominal iteration (iteration {sim.total_iterations-1}):")
for i, param_values in enumerate(sim.Map[-1]):
    print(f"X{i+1}: {param_values}")
    
print("sim.Map = ",sim.Map)



sim.Map =  [
    
    [[15, 25], [150], [7, 20, 30], [0], [0], [0], [0], [0], [0], [0]],
    [[5, 15], [150], [7, 20, 30], [0], [0], [0], [0], [0], [0], [0]],
    [[15, 25], [50.0], [7, 20, 30], [0], [0], [0], [0], [0], [0], [0]],
    [[5, 15], [50.0], [7, 20, 30], [0], [0], [0], [0], [0], [0], [0]],
    [[15, 25], [150], [3, 10, 20], [0], [0], [0], [0], [0], [0], [0]],
    [[5, 15], [150], [3, 10, 20], [0], [0], [0], [0], [0], [0], [0]],
    [[15, 25], [50.0], [3, 10, 20], [0], [0], [0], [0], [0], [0], [0]],
    [[5, 15], [50.0], [3, 10, 20], [0], [0], [0], [0], [0], [0], [0]],
    
    [[10, 20], [100], [5, 15, 25], [0], [0], [0], [0], [0], [0], [0]]
    
    
    ]
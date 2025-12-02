import json
import math
import numpy as np

class WCAAnalyzer:
    def __init__(self):
        pass
    
    def binary_index(self, iteration, index):
        """
        Calculate the binary index for a given iteration and index.
        """
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx

    def WCA(self, iteration, Xs):
        """
        Perform Worst Case Analysis on all variables.
        """
        def funtol(Abs_rel, iteration, index, nom, tol):
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
        
        results = []
        
        for i, var_data in enumerate(Xs):
            if var_data == [[0]]:
                results.append([0, 0, 0])
                continue
                
            wca_values = []
            for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                wca_value = funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                min_value = min(wca_value, min_val)
                max_value = max(wca_value, max_val)
                wca_values.append([wca_value, min_value, max_value])
            
            results.append(wca_values)
        
        return results

    def load_variables_from_json(self, filename):
        """Load variables from JSON and return as list of lists"""
        with open(filename, 'r') as f:
            variables_data = json.load(f)
        
        variable_names = []
        Xs = []
        
        i = 1
        while f"X{i}" in variables_data:
            var_name = f"X{i}"
            value = variables_data[var_name]
            variable_names.append(var_name)
            if value != "[[0]]":
                Xs.append(eval(value))
            else:
                Xs.append([[0]])
            i += 1
        
        return variable_names, Xs

    def detect_mode(self, Xs):
        """
        Detect if we're in WCA mode or Normal mode.
        Returns "WCA" if any inner list has length > 1
        Otherwise returns "Normal" if any inner list has length 1 and value != 0
        Otherwise returns "Unknown"
        """
        # Check if any variable has inner lists with length > 1 (WCA format: [nom, tol, min, max])
        for var_data in Xs:
            if var_data != [[0]]:  # Skip unused variables
                for inner_list in var_data:
                    if len(inner_list) > 1:
                        return "WCA"
        
        # Check if any variable has single values (Normal format: [[value]])
        for var_data in Xs:
            if var_data != [[0]]:
                for inner_list in var_data:
                    if len(inner_list) == 1 and inner_list[0] != 0:
                        return "Normal"
        
        return "Unknown"

    def findIndex(self, points, matrix, pattern=True, mode="Normal"):
        """
        Finds the starting index for each row/column in a matrix based on a list of points.
        """
        indices = []
        
        if mode == "WCA":
            # For WCA mode, handle unused variables ([0]) properly
            if pattern:
                # Find the index of each point in its respective row
                indices = []
                for i in range(len(points)):
                    if i < len(matrix) and matrix[i] != [0] and points[i] in matrix[i]:
                        indices.append(matrix[i].index(points[i]))
                    else:
                        indices.append(0)  # Default for unused variables or when point not found
                
                # Compute the weighted sum dynamically, skipping unused variables
                itr = 0
                valid_indices = []
                valid_lengths = []
                
                # Collect valid indices and lengths (skip unused variables)
                for i in range(len(indices)):
                    if i < len(matrix) and matrix[i] != [0]:
                        valid_indices.append(indices[i])
                        valid_lengths.append(len(matrix[i]))
                
                # Calculate weighted sum only for valid variables
                if valid_indices:
                    itr = valid_indices[0]
                    for i in range(1, len(valid_indices)):
                        multiplier = np.prod(valid_lengths[i:])
                        itr += valid_indices[i] * multiplier
                
                indices.append(itr)
            else:
                # For non-pattern mode in WCA
                itr = 0
                # Find first valid variable
                for i in range(len(matrix)):
                    if matrix[i] != [0] and points[i] in matrix[i]:
                        itr = matrix[i].index(points[i])
                        break
                indices = np.full(len(matrix) + 1, itr).tolist()
                
        else:  # Normal mode
            if pattern:
                # Find the index of each point in its respective row
                indices = []
                for i in range(len(points)):
                    if i < len(matrix) and points[i] in matrix[i]:
                        indices.append(matrix[i].index(points[i]))
                    else:
                        indices.append(0)
                # Compute the weighted sum dynamically
                itr = sum(
                    indices[i] * np.prod([len(matrix[j]) for j in range(i + 1, len(matrix)) if j < len(matrix)])
                    for i in range(len(indices) - 1)
                ) + indices[-1]
                indices.append(itr)
            else:
                # Find the index of the first point in the first row
                itr = 0
                if matrix and points[0] in matrix[0]:
                    itr = matrix[0].index(points[0])
                indices = np.full(len(matrix) + 1, itr).tolist()
                
        return indices, itr

    def findPoint(self, matrix, index, pattern=True, mode="Normal"):
        """
        Generate parameter map based on pattern.
        """
        if mode == "WCA":
            # Filter out unused variables ([0]) for WCA mode
            filtered_matrix = [row for row in matrix if row != [0]]
            if not filtered_matrix:
                return np.array([]), 0
                
            if not pattern:
                max_len = max(len(row) for row in filtered_matrix)
                padded_matrix = [row + [0] * (max_len - len(row)) for row in filtered_matrix]
                padded_matrix = np.array(padded_matrix).T
                return padded_matrix, len(padded_matrix)

            lengths = [len(sublist) for sublist in filtered_matrix]
            totalLengths = np.prod(lengths)
            ParametersMap = np.zeros((totalLengths, len(filtered_matrix)))

            step_size = totalLengths
            for col, sublist in enumerate(filtered_matrix):
                step_size //= lengths[col]
                repeat_factor = totalLengths // (step_size * lengths[col])
                ParametersMap[:, col] = np.tile(np.repeat(sublist, step_size), repeat_factor)

            return ParametersMap, len(ParametersMap)
            
        else:  # Normal mode
            if not pattern:
                max_len = max(len(row) for row in matrix)
                padded_matrix = [row + [0] * (max_len - len(row)) for row in matrix]
                padded_matrix = np.array(padded_matrix).T
                return padded_matrix, len(padded_matrix)

            lengths = [len(sublist) for sublist in matrix]
            totalLengths = np.prod(lengths)
            ParametersMap = np.zeros((totalLengths, len(matrix)))

            step_size = totalLengths
            for col, sublist in enumerate(matrix):
                step_size //= lengths[col]
                repeat_factor = totalLengths // (step_size * lengths[col])
                ParametersMap[:, col] = np.tile(np.repeat(sublist, step_size), repeat_factor)

            return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])

    def findStart(self, matrix, index, pattern=True, mode="Normal"):
        """
        Get starting matrix based on pattern.
        """
        if mode == "WCA":
            # For WCA mode, filter out unused variables
            filtered_matrix = [row for row in matrix if row != [0]]
            if pattern:
                return [row[:] for row in filtered_matrix]
            else:
                if filtered_matrix:
                    ParametersMap = np.array(filtered_matrix).T.tolist()
                    return ParametersMap
                return []
        else:  # Normal mode
            if pattern:
                return [row[:] for row in matrix]
            else:
                ParametersMap = np.array(matrix).T.tolist()
                return ParametersMap

    def init_sim(self, maxThreads=1, startPoint=None, 
                 X1=[0], X2=[0], X3=[0], X4=[0], X5=[0], X6=[0], X7=[0], X8=[0], X9=[0], X10=[0], 
                 pattern=True, model='DCDC', mode="Normal"):
        """
        Initialize a simulation with support for both Normal and WCA modes.
        """
        # define starting point of sweep
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
        
        # Set default startPoint based on mode
        if startPoint is None:
            if mode == "WCA":
                # For WCA mode, start from first value of each non-zero variable
                self.startPoint = []
                for var in self.sweepMatrix:
                    if var != [0] and len(var) > 0:
                        self.startPoint.append(var[0])
                    else:
                        self.startPoint.append(0)
            else:
                self.startPoint = [0] * len(self.sweepMatrix)
        else:
            self.startPoint = startPoint

        # define order of sweep
        self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, pattern, mode)
        self.matrix = self.findStart(self.sweepMatrix, self.idx, pattern, mode)
        self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, pattern, mode)
        self.iterNumber = 0
        
        return self.Map, self.Iterations

# Usage example
def main():
    analyzer = WCAAnalyzer()
    
    # Load variables from JSON
    variable_names, Xs = analyzer.load_variables_from_json('Input_vars.json')
    
    print("Loaded variables:")
    for name, data in zip(variable_names, Xs):
        print(f"  {name}: {data}")
    
    # Detect mode
    mode = analyzer.detect_mode(Xs)
    print(f"\nDetected mode: {mode}")
    
    if mode == "WCA":
        # Perform WCA for a specific iteration
        iteration = 0
        results = analyzer.WCA(iteration, Xs)
        
        print(f"\nWCA Results for iteration {iteration}:")
        for name, result in zip(variable_names, results):
            print(f"  {name}: {result}")
        
        # Extract just the WCA values (first element of each triple) for simulation
        wca_values_matrix = []
        for result in results:
            if result == [0, 0, 0]:
                wca_values_matrix.append([0])
            else:
                # Extract just the wca_value (first element) from each [wca_value, min, max]
                wca_values = [item[0] for item in result]
                wca_values_matrix.append(wca_values)
        
        print(f"\nMatrix for simulation: {wca_values_matrix}")
        
        # Initialize simulation with WCA values - let startPoint be auto-generated
        simulation_map, iterations = analyzer.init_sim(
            maxThreads=1,
            startPoint=None,  # Let it auto-generate based on first values
            X1=wca_values_matrix[0] if len(wca_values_matrix) > 0 else [0],
            X2=wca_values_matrix[1] if len(wca_values_matrix) > 1 else [0],
            X3=wca_values_matrix[2] if len(wca_values_matrix) > 2 else [0],
            X4=wca_values_matrix[3] if len(wca_values_matrix) > 3 else [0],
            X5=wca_values_matrix[4] if len(wca_values_matrix) > 4 else [0],
            X6=wca_values_matrix[5] if len(wca_values_matrix) > 5 else [0],
            X7=wca_values_matrix[6] if len(wca_values_matrix) > 6 else [0],
            X8=wca_values_matrix[7] if len(wca_values_matrix) > 7 else [0],
            X9=wca_values_matrix[8] if len(wca_values_matrix) > 8 else [0],
            X10=wca_values_matrix[9] if len(wca_values_matrix) > 9 else [0],
            pattern=False,
            model='DCDC',
            mode="WCA"
        )
        
    else:  # Normal mode
        # For normal mode, use the original values directly
        normal_matrix = []
        for var_data in Xs:
            if var_data == [[0]]:
                normal_matrix.append([0])
            else:
                # Extract nominal values (first element of each sublist)
                normal_values = [item[0] for item in var_data]
                normal_matrix.append(normal_values)
        
        print(f"\nMatrix for simulation (Normal mode): {normal_matrix}")
        
        # Initialize simulation with normal values
        simulation_map, iterations = analyzer.init_sim(
            maxThreads=1,
            startPoint=None,
            X1=normal_matrix[0] if len(normal_matrix) > 0 else [0],
            X2=normal_matrix[1] if len(normal_matrix) > 1 else [0],
            X3=normal_matrix[2] if len(normal_matrix) > 2 else [0],
            X4=normal_matrix[3] if len(normal_matrix) > 3 else [0],
            X5=normal_matrix[4] if len(normal_matrix) > 4 else [0],
            X6=normal_matrix[5] if len(normal_matrix) > 5 else [0],
            X7=normal_matrix[6] if len(normal_matrix) > 6 else [0],
            X8=normal_matrix[7] if len(normal_matrix) > 7 else [0],
            X9=normal_matrix[8] if len(normal_matrix) > 8 else [0],
            X10=normal_matrix[9] if len(normal_matrix) > 9 else [0],
            pattern=True,
            model='DCDC',
            mode="Normal"
        )
    
    print(f"\nSimulation Map shape: {simulation_map.shape}")
    print(f"Total iterations: {iterations}")
    print(f"First few parameter combinations:")
    for i in range(min(5, len(simulation_map))):
        print(f"  {i}: {simulation_map[i]}")
    
    print("map =", simulation_map)

if __name__ == "__main__":
    main()
    
    
    
simulation Map = [
                    [], #iteration 0
                    [], #iteration 1
                    [], #iteration 2
                    [], #iteration 3
                    [], #iteration 4
                    [], #iteration 5
                    [], #iteration 6

    
]
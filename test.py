import json
import math
import numpy as np

class WCAAnalyzer:
    def __init__(self):
        pass
    
    def binary_index(self, iteration, index):
        """
            Calculate the binary index for a given iteration and index.
            
            This function computes a specific binary pattern at a given 
            iteration.
            
            Parameters
                        iteration   : (int) The current iteration number or step in the sequence.
                        index       : (int) The position/index in the binary pattern to compute. 
                        
            Returns     bin_idx     : (int) The binary index value at the specified position.
            
        """
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx
    
    def WCA(self, iteration, Xs):
        """
            This function calculates the worst-case values for each variable 
            based on tolerance analysis, considering both absolute and relative 
            tolerance types.
            
            Parameters
                        iteration   : (int)     The current iteration number.
                        Xs          : (list)    List of variable data given by user.
                        
            Returns     results     : (list)    List of WCA results for each variable.
                        
        """
        results = []
        for i, var_data in enumerate(Xs):
            if var_data == [[0]]:
                results.append([0, 0, 0])  # WCA unused variables become [0, 0, 0]
                continue
                
            wca_values = []
            for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                wca_value = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                min_value = min(wca_value, min_val)
                max_value = max(wca_value, max_val)
                wca_values.append([wca_value, min_value, max_value])
            
            results.append(wca_values)
            
        return results
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
        """
            This internal function calculates worst-case values based on 
            tolerance type and binary index.
            
            Parameters
                        Abs_rel     : (bool)    True for absolute tolerance, False for relative.
                        iteration   : (int)     Current iteration.
                        index       : (int)     Variable index for binary pattern lookup.
                        nom         : (float)   Nominal value of the variable.
                        tol         : (float)   Tolerance value.
                        
            Returns     wca_value   : (float)   Calculated worst-case value.
            
        """
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
    
    def load_startpoint_from_json(self, filename):
        """Load startPoint from JSON"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        if "startPoint" in data:
            startpoint_str = data["startPoint"]
            # Convert string to list
            if startpoint_str.startswith("[") and startpoint_str.endswith("]"):
                return eval(startpoint_str)
        
        # Return default: first elements of each variable
        return None

    def detect_mode(self, Xs):
        """
        Detect if we're in WCA mode or Normal mode.
        """
        # Check if any variable has inner lists with length > 1 (WCA format: [nom, tol, min, max])
        for var_data in Xs:
            if var_data != [[0]]:
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

    def is_unused(self, var_data, mode="Normal"):
        """Check if a variable is unused"""
        if mode == "WCA":
            # In WCA mode, unused is [0, 0, 0] (list of 3 zeros)
            return var_data == [0, 0, 0]
        else:
            # In Normal mode, unused is [0] (list with single zero)
            return var_data == [0]

    def _process_wca_startpoint(self, startPoint, iteration):
        """
        Process startPoint for WCA mode.
        Converts [nom, tol, min, max] to [value, min, max] using WCA calculation.
        """
        processed = []
        
        for i, sp in enumerate(startPoint):
            if sp == 0 or sp == [0]:
                processed.append(0)
            elif isinstance(sp, list):
                if len(sp) == 4:  # [nom, tol, min, max]
                    nom, tol, min_val, max_val = sp
                    wca_value = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                    min_value = min(wca_value, min_val)
                    max_value = max(wca_value, max_val)
                    processed.append([wca_value, min_value, max_value])
                elif len(sp) == 3:  # Already [value, min, max]
                    processed.append(sp)
                else:
                    processed.append(0)
            else:
                processed.append(0)
        
        return processed



    def findIndex(self, points, matrix, mode="Normal"):
        """
            Finds the starting index for each row/column in a matrix based on a list of points.
            
            Parameters
                        points      : (list) A list of points to search for in the matrix.
                        matrix      : (list[list]) A two-dimensional matrix to search for points.
                        mode        : (str) "Normal" or "WCA" - determines how points are matched.
                        
            Returns     indices     : (list) A list of indices representing the starting index 
                                    for each row/column.
                        itr         : (int) The computed iteration index for reference.
            
            For Normal mode:
                        - Matches exact values in matrix rows
                        - Computes weighted sum based on matrix lengths
                        
            For WCA mode:
                        - Matches first element of [value, min, max] triples
                        - Only considers active variables
        """
        indices = []
        
        if mode == "Normal":
            # Original pattern=True logic
            # Find the index of each point in its respective row
            indices = [matrix[i].index(points[i]) for i in range(len(points))]
            # Compute the weighted sum dynamically instead of hardcoding
            itr = sum(
                indices[i] * np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])
                for i in range(len(indices) - 1)
            ) + indices[-1]  # Last index is added directly
            indices.append(itr)  # Append computed index for reference
            return indices, itr
        
        elif mode == "WCA":
            # WCA mode logic - only for active variables
            for i in range(len(matrix)):
                if not self.is_unused(matrix[i], mode):
                    # For WCA mode, find matching [value, min, max] triple
                    found = False
                    for idx, item in enumerate(matrix[i]):
                        if isinstance(item, list) and len(item) >= 1:
                            # Compare just the value (first element)
                            if isinstance(points[i], list) and len(points[i]) >= 1:
                                if item[0] == points[i][0]:
                                    indices.append(idx)
                                    found = True
                                    break
                    if not found:
                        indices.append(0)
                else:
                    indices.append(0)  # Unused variables get index 0
            
            # Compute weighted sum for active variables only
            active_indices = []
            active_lengths = []
            for i in range(len(matrix)):
                if not self.is_unused(matrix[i], mode):
                    active_indices.append(indices[i])
                    active_lengths.append(len(matrix[i]))
            
            if active_indices:
                itr = active_indices[0]
                for i in range(1, len(active_indices)):
                    multiplier = np.prod(active_lengths[i:])
                    itr += active_indices[i] * multiplier
                indices.append(itr)
            else:
                indices.append(0)
            
            return indices, indices[-1]
        
        else:
            raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")

    def findPoint(self, matrix, index, mode="Normal", add_nominal_iteration=False, original_Xs=None):
        """
            Generate parameter map based on mode.
            
            Parameters
                        matrix              : (list[list]) A two-dimensional matrix.
                        index               : (list) Indices for slicing.
                        mode                : (str) "Normal" or "WCA" mode.
                        add_nominal_iteration : (bool) Add extra iteration with nominal values (WCA only).
                        original_Xs         : (list) Original Xs data for nominal values (WCA only).
                        
            Returns     ParametersMap       : (array) Generated parameter combinations.
                        total_iterations    : (int) Number of generated combinations.
            
            For Normal mode:
                        - Original pattern logic for permutations
                        - Returns 2D array [iterations × variables]
                        
            For WCA mode:
                        - Special handling for [value, min, max] triples
                        - Returns 3D array [iterations × variables × 3]
        """
        def get_original_nominals(Xs):
            """
            Extract nominal values and min/max bounds from variable data.
            """
            return [
                [[nom, min_val, max_val] for nom, tol, min_val, max_val in var_data] 
                if var_data != [[0]] else [[0, 0, 0]]
                for var_data in Xs
            ]
        if mode == "Normal":
            # ORIGINAL CODE - keep exactly as-is
            # Compute the product of all sublist lengths to determine total number of rows
            lengths = [len(sublist) for sublist in matrix]
            totalLengths = np.prod(lengths)
            ParametersMap = np.zeros((totalLengths, len(matrix)))  # Initialize empty matrix of correct shape

            step_size = totalLengths  # Start with total length
            for col, sublist in enumerate(matrix):
                step_size //= lengths[col]  # Reduce step size for each column
                repeat_factor = totalLengths // (step_size * lengths[col])  # Compute how often values should repeat
                ParametersMap[:, col] = np.tile(np.repeat(sublist, step_size), repeat_factor)  # Fill column efficiently

            return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])  # Slice according to index and return
        
        elif mode == "WCA":
            # NEW WCA mode logic
            # Separate active and unused variables
            active_indices = []
            active_matrix = []
            unused_positions = []
            
            for i, row in enumerate(matrix):
                if not self.is_unused(row, mode):
                    active_indices.append(i)
                    active_matrix.append(row)
                else:
                    unused_positions.append(i)
            
            if not active_matrix:
                # If no active variables, create empty array with all variables
                return np.zeros((0, len(matrix), 3)), 0
            
            # Get lengths of active variable lists
            lengths = [len(sublist) for sublist in active_matrix]
            totalLengths = np.prod(lengths)
            
            # For WCA mode: create array with all variables (including unused)
            num_all_vars = len(matrix)
            
            # Add extra iteration for nominal values if requested (only for WCA mode)
            extra_iterations = 1 if add_nominal_iteration else 0
            ParametersMap = np.zeros((totalLengths + extra_iterations, num_all_vars, 3))
            
            # Set default for unused variables in all iterations
            for i in unused_positions:
                ParametersMap[:, i, :] = [0, 0, 0]
            
            # Generate all permutations for active variables using meshgrid
            indices_list = [np.arange(length) for length in lengths]
            meshgrid_indices = np.array(np.meshgrid(*indices_list, indexing='ij'))
            meshgrid_indices = meshgrid_indices.reshape(len(active_matrix), -1).T
            
            # Fill the ParametersMap for active variables (WCA combinations)
            for i in range(totalLengths):
                for active_idx, orig_idx in enumerate(active_indices):
                    element_idx = meshgrid_indices[i, active_idx]
                    ParametersMap[i, orig_idx, :] = active_matrix[active_idx][element_idx]
            
            # Add extra iteration with original nominal values if requested (WCA mode only)
            if add_nominal_iteration and original_Xs is not None:
                nominal_iteration_idx = totalLengths
                # Get original nominal values
                original_nominals = get_original_nominals(original_Xs)
                
                for var_idx in range(num_all_vars):
                    if var_idx not in unused_positions:
                        # Find which active variable this corresponds to
                        if var_idx in active_indices:
                            active_idx = active_indices.index(var_idx)
                            # Use first element from original nominals
                            if len(original_nominals[var_idx]) > 0:
                                ParametersMap[nominal_iteration_idx, var_idx, :] = original_nominals[var_idx][0]
                    else:
                        # Unused variables remain [0, 0, 0]
                        ParametersMap[nominal_iteration_idx, var_idx, :] = [0, 0, 0]
            
            total_iterations = totalLengths + extra_iterations
            
            # Apply the slicing based on index (similar to original)
            if index and len(index) > 0:
                start_idx = index[-1] if isinstance(index, list) else index
                if start_idx < total_iterations:
                    return ParametersMap[start_idx:], len(ParametersMap[start_idx:])
            
            return ParametersMap, total_iterations
        
        else:
            raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")

    def findStart(self, matrix, index, mode="Normal"):
        """
            Get starting matrix based on mode.
            
            Parameters
                        matrix      : (list[list]) A two-dimensional matrix.
                        index       : (list) Indices for processing.
                        mode        : (str) "Normal" or "WCA" mode.
                        
            Returns     matrix_copy : (list[list]) Processed matrix based on mode.
            
            For Normal mode:
                        - Returns shallow copy of each row.
                        - Or transposed matrix based on pattern flag.
                        
            For WCA mode:
                        - Returns the matrix as-is (all variables).
        """
        
        if mode == "Normal":
            # ORIGINAL CODE - keep exactly as-is
            # This corresponds to pattern=True in original
            return [row[:] for row in matrix]  # Create a shallow copy of each row and return
        
        elif mode == "WCA":
            # For WCA mode, return matrix as-is (all variables including unused)
            return matrix
        
        else:
            raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")

    def init_sim(self, maxThreads=1, startPoint=None, 
                 X1=[0], X2=[0], X3=[0], X4=[0], X5=[0], X6=[0], X7=[0], X8=[0], X9=[0], X10=[0], 
                 model='DCDC', mode="Normal", iteration=0, add_nominal_iteration=False, original_Xs=None):
       
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
 
        # Convert startPoint to appropriate format
        if mode == "WCA":
                # Check if startPoint is already in WCA format or needs conversion
                self.startPoint = self._process_wca_startpoint(startPoint, iteration)
        else:
                self.startPoint = startPoint
        
        # Only add nominal iteration for WCA mode
        if mode == "WCA" and add_nominal_iteration:
            print(f"Adding nominal iteration for WCA mode")
        elif mode == "Normal" and add_nominal_iteration:
            print(f"Note: add_nominal_iteration ignored for Normal mode (already using nominal values)")
            add_nominal_iteration = False
        
        # Find indices and create parameter map
        self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, mode)
        self.matrix = self.findStart(self.sweepMatrix, self.idx, mode)
        self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, mode, 
                                                   add_nominal_iteration, original_Xs)
        self.iterNumber = 0
        print(f"Initialized simulation in {mode} mode with {self.Iterations} iterations.")
        print(f"Start Point: {self.startPoint}")
        print(f"Indices: {self.idx}")
        print(f"Parameter Map shape: {self.Map.shape}")
        print(f"Total Iterations: {self.Iterations}")
        print("Map: ", self.Map)
                
        return self.Map, self.Iterations

# Main function to loop through all iterations
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
    
    # Example startPoint in [nom, tol, min, max] format
    example_startpoint = [
        [10, 0.1, 5, 15],    # X1: [nom, tol, min, max]
        [100, 0.5, 50, 150], # X2
        [5, 0.2, 3, 7],      # X3
        [50, 0.1, 40, 60],   # X4
        [1, 0.5, 0.5, 2],    # X5
        [8, 0.25, 6, 10],    # X6
        [0],                  # X7: unused
        [0],                  # X8: unused
        [0],                  # X9: unused
        [0]                   # X10: unused
    ]
    
    print(f"\nExample startPoint (input format):")
    for i, sp in enumerate(example_startpoint):
        print(f"  X{i+1}: {sp}")
    
    if mode == "WCA":
     
        
        # Calculate number of iterations needed
        # For 6 variables with 2 values each: 2^6 = 64 iterations
        active_vars = sum(1 for var in Xs if var != [[0]])
        total_iterations_needed = 2 ** active_vars
        print(f"\nNumber of active variables: {active_vars}")
        print(f"Total WCA iterations needed: {total_iterations_needed}")
        
        # Store all iteration results
        all_iteration_maps = []
        
        # Loop through all iterations
        for iteration in range(total_iterations_needed):
            print(f"\n{'='*60}")
            print(f"Processing WCA iteration {iteration}/{total_iterations_needed-1}")
            print(f"{'='*60}")
            
            # Perform WCA for this iteration
            results = analyzer.WCA(iteration, Xs)
            
            print(f"\nWCA Results for iteration {iteration}:")
            for name, result in zip(variable_names, results):
                print(f"  {name}: {result}")
            
            # Convert example startPoint to WCA format for this iteration
            wca_startpoint = analyzer._process_wca_startpoint(example_startpoint, iteration)
            
            print(f"\nConverted WCA startPoint for iteration {iteration}:")
            for i, sp in enumerate(wca_startpoint):
                print(f"  X{i+1}: {sp}")
            
            # For WCA mode, use the full [value, min, max] results
            wca_matrix = results
            
            # Initialize simulation with WCA values, custom startPoint, and add nominal iteration
            simulation_map, iterations = analyzer.init_sim(
                maxThreads=1,
                startPoint=wca_startpoint,  # Use our custom startPoint
                X1=wca_matrix[0] if len(wca_matrix) > 0 else [0, 0, 0],
                X2=wca_matrix[1] if len(wca_matrix) > 1 else [0, 0, 0],
                X3=wca_matrix[2] if len(wca_matrix) > 2 else [0, 0, 0],
                X4=wca_matrix[3] if len(wca_matrix) > 3 else [0, 0, 0],
                X5=wca_matrix[4] if len(wca_matrix) > 4 else [0, 0, 0],
                X6=wca_matrix[5] if len(wca_matrix) > 5 else [0, 0, 0],
                X7=wca_matrix[6] if len(wca_matrix) > 6 else [0, 0, 0],
                X8=wca_matrix[7] if len(wca_matrix) > 7 else [0, 0, 0],
                X9=wca_matrix[8] if len(wca_matrix) > 8 else [0, 0, 0],
                X10=wca_matrix[9] if len(wca_matrix) > 9 else [0, 0, 0],
                model='DCDC',
                mode="WCA",
                iteration=iteration,
                add_nominal_iteration=True,  # Add extra iteration with nominal values (WCA mode only)
                original_Xs=Xs  # Provide original Xs for nominal values
            )
            
            # Store this iteration's map
            all_iteration_maps.append({
                'iteration': iteration,
                'map': simulation_map,
                'iterations': iterations,
                'shape': simulation_map.shape
            })
            
            print(f"\nWCA Simulation Map shape: {simulation_map.shape}")
            print(f"Total iterations in map: {iterations} ({iterations-1} WCA + 1 nominal)")
            
            if len(simulation_map) > 0:
                print(f"\nFirst iteration in map (WCA combination):")
                for var_idx in range(min(3, simulation_map.shape[1])):  # Show first 3
                    value, min_val, max_val = simulation_map[0, var_idx]
                    print(f"  X{var_idx+1}: [{value:.2f}, {min_val:.2f}, {max_val:.2f}]")
                
                print(f"\nLast iteration in map (Nominal values - iteration {len(simulation_map)-1}):")
                nominal_iteration = len(simulation_map) - 1
                for var_idx in range(min(3, simulation_map.shape[1])):  # Show first 3
                    value, min_val, max_val = simulation_map[nominal_iteration, var_idx]
                    print(f"  X{var_idx+1}: [{value:.2f}, {min_val:.2f}, {max_val:.2f}]")
        
        # Summary of all iterations
        print(f"\n{'='*60}")
        print(f"SUMMARY OF ALL {total_iterations_needed} WCA ITERATIONS")
        print(f"{'='*60}")
        
        total_simulations = 0
        for iteration_data in all_iteration_maps:
            total_simulations += iteration_data['iterations']
            print(f"Iteration {iteration_data['iteration']}: {iteration_data['shape']} shape, {iteration_data['iterations']} simulations")
        
        print(f"\nTotal simulations across all iterations: {total_simulations}")
        print(f"Average simulations per WCA iteration: {total_simulations / total_iterations_needed:.2f}")
        
        # Show first iteration's first few parameter combinations
        if all_iteration_maps:
            print(f"\nSample from iteration 0:")
            sample_map = all_iteration_maps[0]['map']
            if len(sample_map) > 0:
                print(f"First 3 parameter combinations:")
                for i in range(min(3, len(sample_map))):
                    row_str = []
                    for var_idx in range(min(3, sample_map.shape[1])):
                        value, min_val, max_val = sample_map[i, var_idx]
                        row_str.append(f"[{value:.2f}, {min_val:.2f}, {max_val:.2f}]")
                    print(f"  Combination {i}: {', '.join(row_str)}")
        
    else:  # Normal mode
        # For normal mode, extract nominal values
        normal_matrix = []
        for var_data in Xs:
            if var_data == [[0]]:
                normal_matrix.append([0])
            else:
                normal_values = [item[0] for item in var_data]
                normal_matrix.append(normal_values)
        
        print(f"\nMatrix for simulation (Normal mode): {normal_matrix}")
        
        # Create startPoint from first values
        normal_startpoint = []
        for var in normal_matrix:
            if var != [0] and len(var) > 0:
                normal_startpoint.append(var[0])
            else:
                normal_startpoint.append(0)
        
        print(f"\nNormal startPoint (first values): {normal_startpoint}")
        
        # Initialize simulation with normal values (no nominal iteration needed)
        # For Normal mode, we only need one iteration since we're using nominal values directly
        simulation_map, iterations = analyzer.init_sim(
            maxThreads=1,
            startPoint=normal_startpoint,
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
            model='DCDC',
            mode="Normal",
            add_nominal_iteration=False,  # No nominal iteration for Normal mode
            original_Xs=Xs
        )
        
        print(f"\nNormal Simulation Map shape: {simulation_map.shape}")
        print(f"Total iterations: {iterations} (all nominal combinations)")
        
        if len(simulation_map) > 0:
            print(f"\nFirst 5 iterations (all nominal values):")
            for i in range(min(5, len(simulation_map))):
                print(f"  Iteration {i}: {simulation_map[i]}")

if __name__ == "__main__":
    main()
    
    
    


can we make the following functions into one function with well commented selctions and shorter code lines so that 
at the end we have only one function that does the same as these plus the rest of the code 


load_variables_from_json ,load_startpoint_from_json ,detect_mode ,is_unused ,_process_wca_startpoint
       

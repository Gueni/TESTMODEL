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
    
    def WCA(self, Xs):
        """
            This function calculates all worst-case values for each variable 
            across all possible binary combinations, considering both absolute 
            and relative tolerance types.
            
            Parameters
                        Xs          : (list)    List of variable data given by user.
                        
            Returns     all_results : (list)    List of WCA results for each iteration.
                                                Shape: [iterations][variables][values]
                        
        """
        # Count active variables
        active_vars = sum(1 for var_data in Xs if var_data != [[0]])
        
        # Calculate number of iterations needed (2^active_vars)
        total_iterations = 2 ** active_vars if active_vars > 0 else 1
        
        all_results = []
        
        # Loop through all iterations internally
        for iteration in range(total_iterations):
            iteration_results = []
            for i, var_data in enumerate(Xs):
                if var_data == [[0]]:
                    iteration_results.append([0, 0, 0])  # WCA unused variables become [0, 0, 0]
                    continue
                    
                wca_values = []
                for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                    wca_value = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                    min_value = min(wca_value, min_val)
                    max_value = max(wca_value, max_val)
                    wca_values.append([wca_value, min_value, max_value])
                
                iteration_results.append(wca_values)
            
            all_results.append(iteration_results)
            
        return all_results
    
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
    
    def load_and_process_variables(self, json_filename, iteration=0):
        """
        Unified function to load and process variables from JSON file.
        
        This function combines:
        1. Loading variables from JSON
        2. Loading startPoint from JSON
        3. Detecting mode (Normal/WCA)
        4. Processing WCA startPoint when needed
        
        Parameters:
            json_filename: (str) Path to JSON file containing variables data
            iteration: (int) Current iteration number (for WCA processing)
            
        Returns:
            dict: Dictionary containing:
                - variable_names: List of variable names (X1, X2, etc.)
                - Xs: List of variable data
                - startPoint: Processed startPoint
                - mode: Detected mode ("Normal" or "WCA")
                - active_vars: Count of active variables
        """
        # =========================================================================
        # SECTION 1: LOAD DATA FROM JSON FILE
        # =========================================================================
        with open(json_filename, 'r') as f: 
            data = json.load(f)
        variable_names , Xs , i = [] ,[],1
        
        # Extract all X{i} variables from the JSON
        while f"X{i}" in data:
            var_name    = f"X{i}"
            value       = data[var_name]
            variable_names.append(var_name)
            Xs.append(eval(value))
            i += 1
        
        # Load startPoint
        startPoint = eval(data["startPoint"])
        
        # =========================================================================
        # SECTION 2: DETECT MODE (Normal or WCA) - Check only first active variable
        # =========================================================================
        mode = "Unknown"
        
        # Find the first non-zero variable to determine mode
        first_active_var = None
        for var_data in Xs:
            if var_data != [[0]] and var_data != [0] and len(var_data) > 0:
                first_active_var = var_data
                break
        
        if first_active_var:
            # Check the first inner list in the first active variable
            if len(first_active_var[0]) > 1:                                        mode = "WCA"    # WCA mode      : [nom, tol, min, max] format (list length > 1)
            elif len(first_active_var[0]) == 1 and first_active_var[0][0] != 0:     mode = "Normal" # Normal mode   : [[value]] format (single value)
        
        # =========================================================================
        # SECTION 3: PROCESS STARTPOINT BASED ON MODE
        # =========================================================================
        processed_startPoint = []
        
        if mode == "WCA" and startPoint:
            # Process WCA startPoint: convert [nom, tol, min, max] to [value, min, max]
            for i, sp in enumerate(startPoint):
                if sp == 0 or sp == [0]:
                    processed_startPoint.append([0, 0, 0])  # WCA unused variables become [0, 0, 0])
                elif isinstance(sp, list):
                    if len(sp) == 4:  # [nom, tol, min, max] format
                        nom, tol, min_val, max_val = sp
                        # Calculate WCA value using tolerance
                        wca_value = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                        min_value = min(wca_value, min_val)
                        max_value = max(wca_value, max_val)
                        processed_startPoint.append([wca_value, min_value, max_value])
        else:
            processed_startPoint = startPoint 
        
        # =========================================================================
        # SECTION 4: COUNT ACTIVE VARIABLES
        # =========================================================================
        if mode == "WCA":   active_vars = sum(1 for var_data in Xs if var_data != [[0]])
        else:               active_vars = sum(1 for var_data in Xs if var_data != [[0]] and var_data != [0])
        
        # =========================================================================
        return {
            'variable_names'    : variable_names,
            'Xs'                : Xs,
            'startPoint'        : processed_startPoint,
            'mode'              : mode,
            'active_vars'       : active_vars
        }
    
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
            # Find the index of each point in its respective row
            indices = [matrix[i].index(points[i]) for i in range(len(points))]
            # Compute the weighted sum dynamically
            itr = sum(
                indices[i] * np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])
                for i in range(len(indices) - 1)
            ) + indices[-1]  # Last index is added directly
            indices.append(itr)  # Append computed index for reference
            return indices, itr
        
        elif mode == "WCA":
            active_indices = []
            active_lengths = []
            # WCA mode logic - only for active variables
            for i in range(len(matrix)):
                if matrix[i] != [0, 0, 0]:  # Active variable in WCA mode
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
                if matrix[i] != [0, 0, 0]:  # Active variable in WCA mode
                    active_indices.append(indices[i])
                    active_lengths.append(len(matrix[i]))
            
            if active_indices:
                itr = int(active_indices[0])
                for i in range(1, len(active_indices)):
                    multiplier = int(np.prod(active_lengths[i:]))
                    itr += int(active_indices[i] * multiplier)
                indices.append(itr)
            else:
                indices.append(0)
            return indices, indices[-1]
        
        else:
            raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")

    def findPoint(self, matrix, index, mode="Normal", original_Xs=None):
        """
            Generate parameter map based on mode.
            
            Parameters
                        matrix              : (list[list]) A two-dimensional matrix.
                        index               : (list) Indices for slicing.
                        mode                : (str) "Normal" or "WCA" mode.
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
            # Separate active and unused variables
            active_indices,active_matrix,unused_positions = [], [], []
            
            for i, row in enumerate(matrix):
                if row != [0, 0, 0]:  # Active variable in WCA mode
                    active_indices.append(i)
                    active_matrix.append(row)
                else:
                    unused_positions.append(i)
            
            # Get lengths of active variable lists
            lengths             = [len(sublist) for sublist in active_matrix]
            totalLengths        = int(np.prod(lengths))
            
            # Add extra iteration for nominal values if requested (only for WCA mode)
            ParametersMap       = np.zeros((totalLengths + 1, len(matrix), 3))
            
            # Set default for unused variables in all iterations
            for i in unused_positions: ParametersMap[:, i, :] = [0, 0, 0]
            
            # Generate all permutations for active variables using meshgrid
            indices_list        = [np.arange(length) for length in lengths]
            meshgrid_indices    = (np.array(np.meshgrid(*indices_list, indexing='ij'))).reshape(len(active_matrix), -1).T
            
            # Fill the ParametersMap for active variables (WCA combinations)
            for i in range(totalLengths):
                for active_idx, orig_idx in enumerate(active_indices):
                    element_idx                     = meshgrid_indices[i, active_idx]
                    ParametersMap[i, orig_idx, :]   = active_matrix[active_idx][element_idx]
            
            # Add extra iteration with original nominal values (WCA mode only)
            if original_Xs is not None:
                nominal_iteration_idx = totalLengths
                # Get original nominal values
                original_nominals = get_original_nominals(original_Xs)
                
                for var_idx in range(len(matrix)):
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
            
            total_iterations = totalLengths + 1
            
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

    def init_sim(self, maxThreads=1, startPoint=None, X1=[0], X2=[0], X3=[0], X4=[0], X5=[0], X6=[0], X7=[0], X8=[0], X9=[0], X10=[0], model='DCDC', mode="Normal", iteration=0, original_Xs=None):
       
        self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
 
        # Set startPoint directly 
        self.startPoint = startPoint
                
        # Find indices and create parameter map
        self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, mode)
        self.matrix = self.findStart(self.sweepMatrix, self.idx, mode)
        self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, mode, original_Xs)
        self.iterNumber = 0
                
        return self.Map, self.Iterations

    def process_WCA_simulation(self, Xs, json_filename):
        """
        Process WCA simulation for all iterations at once.
        
        Parameters:
            Xs: Variable data
            json_filename: Path to JSON file
            
        Returns:
            dict: Contains all WCA simulation maps and summary information
        """
        # Get ALL WCA results for all iterations at once
        all_wca_results = self.WCA(Xs)
        
        all_iteration_maps = []
        all_iteration_summaries = []
        
        # Process all WCA iterations
        for iteration_idx, wca_results in enumerate(all_wca_results):
            # Process startPoint for this specific WCA iteration
            data_for_iteration = self.load_and_process_variables(
                json_filename, 
                iteration=iteration_idx  # Use iteration_idx for binary pattern
            )
            wca_startpoint = data_for_iteration['startPoint']
            
            # Initialize simulation with WCA values for this iteration
            simulation_map, iterations = self.init_sim(
                maxThreads=1,
                startPoint=wca_startpoint,
                X1=wca_results[0] if len(wca_results) > 0 else [0, 0, 0],
                X2=wca_results[1] if len(wca_results) > 1 else [0, 0, 0],
                X3=wca_results[2] if len(wca_results) > 2 else [0, 0, 0],
                X4=wca_results[3] if len(wca_results) > 3 else [0, 0, 0],
                X5=wca_results[4] if len(wca_results) > 4 else [0, 0, 0],
                X6=wca_results[5] if len(wca_results) > 5 else [0, 0, 0],
                X7=wca_results[6] if len(wca_results) > 6 else [0, 0, 0],
                X8=wca_results[7] if len(wca_results) > 7 else [0, 0, 0],
                X9=wca_results[8] if len(wca_results) > 8 else [0, 0, 0],
                X10=wca_results[9] if len(wca_results) > 9 else [0, 0, 0],
                model='DCDC',
                mode="WCA",
                iteration=iteration_idx,
                original_Xs=Xs
            )
            
            all_iteration_maps.append(simulation_map)
            all_iteration_summaries.append({
                'iteration': iteration_idx,
                'total_simulations': iterations,
                'map': simulation_map.tolist()
            })
        
        return {
            'all_maps': all_iteration_maps,
            'all_summaries': all_iteration_summaries,
            'total_iterations': len(all_wca_results),
            'binary_combinations': 2**sum(1 for var_data in Xs if var_data != [[0]])
        }

# Main function
def main():
    analyzer = WCAAnalyzer()
    
    # Use the unified function to load and process variables
    data = analyzer.load_and_process_variables('Input_vars.json')
    Xs = data['Xs']
    mode = data['mode']
    
    if mode == "WCA":
        # Process ALL WCA simulations at once
        wca_results = analyzer.process_WCA_simulation(Xs, 'Input_vars.json')
        
        print(f"\n=== WCA Simulation Results ===")
        print(f"Total WCA iterations: {wca_results['total_iterations']}")
        print(f"Total binary combinations: {wca_results['binary_combinations']}")
        
        # Print results for each iteration
        for summary in wca_results['all_summaries']:
            print(f"\n--- WCA Iteration {summary['iteration']} ---")
            print(f"Total simulations: {summary['total_simulations']}")
            for i, sublist in enumerate(summary['map']):
                print(f"Map {i}:", sublist)
        
    else:  # Normal mode
        # For normal mode, extract nominal values
        normal_matrix = []
        for var_data in Xs:
            if var_data == [[0]]:
                normal_matrix.append([0])
            else:
                normal_values = [item[0] for item in var_data]
                normal_matrix.append(normal_values)
        
        # Get the already processed startPoint from our unified function
        normal_startpoint = data['startPoint']
        
        # Initialize simulation with normal values
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
            original_Xs=Xs
        )
        
                    
if __name__ == "__main__":
    main()


# [ 
#   [[1,2] [1] [] [] [] [] [] [] [] []]
# ]
# min max
# 2**activevar 

import json
import math
import numpy as np

class WCAAnalyzer:
    def __init__(self):
        pass
    
    def binary_index(self, iteration, index):
      
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx
    
    def WCA(self, iteration, Xs):
      
        results = []
        for i, var_data in enumerate(Xs):
            if var_data == [[0]]:
                results.append([0])  # WCA unused variables become [0, 0, 0]
                continue
                
            wca_values = []
            for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                if tol <= 1:
                    # Absolute tolerance
                    x = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                else:
                    # Relative tolerance
                    x = self.funtol(Abs_rel=False, iteration=iteration, index=i, nom=nom, tol=tol)
                
                wca_value = min(max(x,min_val),max_val)
                
                wca_values.append(wca_value)
            
            results.append(wca_values)
            
        return results
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
      
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
       
        #LOAD DATA FROM JSON FILE
        # =========================================================================
        with open(json_filename, 'r') as f: data = json.load(f)
        variable_names , Xs , i = [] ,[],1
        
        # Extract all X{i} variables from the JSON and return Xs list
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
                    processed_startPoint.append([0])  # WCA unused variables become [0, 0, 0])
                elif isinstance(sp, list):
                    if len(sp) == 4:  # [nom, tol, min, max] format
                        nom, tol, min_val, max_val = sp
                        if tol < 1:
                                # Absolute tolerance
                                x = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                        else:
                                # Relative tolerance
                                x = self.funtol(Abs_rel=False, iteration=iteration, index=i, nom=nom, tol=tol)
                            
                        wca_value = min(max(x,min_val),max_val)
                        
                        # Calculate WCA value using tolerance
                        processed_startPoint.append([wca_value])
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
                if matrix[i] != [0]:  # Active variable in WCA mode
                    # For WCA mode, find matching [value] 
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
                if matrix[i] != [0]:  # Active variable in WCA mode
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
    
    def findPoint(self, matrix, index, mode="Normal", original_Xs=None):
    
        print("matrix:", matrix)
        if mode == "Normal":
            # Original Normal mode code...
            lengths = [len(sublist) for sublist in matrix]
            totalLengths = np.prod(lengths)
            
            ParametersMap = np.zeros((totalLengths, len(matrix)))
            step_size = totalLengths
            for col, sublist in enumerate(matrix):
                step_size //= lengths[col]
                repeat_factor = totalLengths // (step_size * lengths[col])
                ParametersMap[:, col] = np.tile(np.repeat(sublist, step_size), repeat_factor)

            return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])
        
        elif mode == "WCA":
            # Count active variables
            active_vars = sum(1 for row in matrix if row != [0] and row != [] and row != 0)
            
            # Use 2**active_vars + 1 for total rows
            totalLengths = 2 ** active_vars + 1
            
            # Create ParametersMap as a list of lists
            ParametersMap = []
            
            # Find active indices
            active_indices = []
            for i, row in enumerate(matrix):
                if row != [0] and row != [] and row != 0:  # Active variable
                    active_indices.append(i)
            
            # Generate WCA combinations using binary patterns (2**active_vars rows)
            for iteration in range(2 ** active_vars):
                row = []
                
                for var_idx in range(10):  # Always 10 variables
                    if var_idx in active_indices:
                        # This is an active variable
                        active_idx = active_indices.index(var_idx)
                        
                        # Get binary index for this variable at this iteration
                        bin_idx = self.binary_index(iteration, active_idx)
                        
                        # Get the value from matrix[var_idx][bin_idx]
                        if bin_idx < len(matrix[var_idx]):
                            value = matrix[var_idx][bin_idx]
                            # ALWAYS wrap in a list
                            if isinstance(value, list):
                                row.append(value.copy())
                            else:
                                row.append([value])  # Wrap single value in list
                        else:
                            # If binary index out of range, use first value
                            if matrix[var_idx] and len(matrix[var_idx]) > 0:
                                first_val = matrix[var_idx][0]
                                if isinstance(first_val, list):
                                    row.append(first_val.copy())
                                else:
                                    row.append([first_val])  # Wrap in list
                            else:
                                row.append([])
                    else:
                        # Inactive variable - add zeros
                        row.append([0.0, 0.0, 0.0])
                
                ParametersMap.append(row)
            
            # Add nominal values row (last row)
            nominal_row = []
            for var_idx in range(10):  # Always 10 variables
                if var_idx in active_indices:
                    # Use the first value from the matrix as nominal
                    if matrix[var_idx] and len(matrix[var_idx]) > 0:
                        first_val = matrix[var_idx][0]
                        if isinstance(first_val, list):
                            nominal_row.append(first_val.copy())
                        else:
                            nominal_row.append([first_val])  # Wrap in list
                    else:
                        nominal_row.append([])
                else:
                    # Inactive variable
                    nominal_row.append([0.0, 0.0, 0.0])
            
            ParametersMap.append(nominal_row)
            
            total_iterations = totalLengths
            
            # Apply slicing based on index
            if index and len(index) > 0:
                start_idx = index[-1] if isinstance(index, list) else index
                if start_idx < total_iterations:
                    return ParametersMap[start_idx:], len(ParametersMap[start_idx:])
            
            return ParametersMap, total_iterations
        
        else:
            raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")
    
    def findStart(self, matrix, index, mode="Normal"):
        """
            Get      starting matrix based on mode.
            
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
        """
        Initialize simulation setup - now includes WCA iteration generation internally.
        
        For WCA mode: Generates all WCA iterations internally
        For Normal mode: Standard parameter sweep
        """
        if mode == "WCA":
                # Calculate all WCA iterations
                active_vars = sum(1 for var_data in original_Xs if var_data != [[0]])
                total_iterations_needed = 2 ** active_vars
                
                # Generate all iteration results
                all_iteration_maps = []
                for wca_iteration in range(total_iterations_needed):
                    # Perform WCA for this iteration
                    results = self.WCA(wca_iteration, original_Xs)
                    
                    # Process startPoint for this WCA iteration
                    data_for_iteration = self.load_and_process_variables(
                        'Input_vars.json', 
                        iteration=wca_iteration
                    )
                    wca_startpoint = data_for_iteration['startPoint']
                    
                    # Use the full [value, min, max] results
                    wca_matrix = results
                    
                    # Set sweep matrix for this WCA iteration
                    self.sweepMatrix = [
                        wca_matrix[0]    if len(wca_matrix) > 0 else [0],
                        wca_matrix[1]    if len(wca_matrix) > 1 else [0],
                        wca_matrix[2]    if len(wca_matrix) > 2 else [0],
                        wca_matrix[3]    if len(wca_matrix) > 3 else [0],
                        wca_matrix[4]    if len(wca_matrix) > 4 else [0],
                        wca_matrix[5]    if len(wca_matrix) > 5 else [0],
                        wca_matrix[6]    if len(wca_matrix) > 6 else [0],
                        wca_matrix[7]    if len(wca_matrix) > 7 else [0],
                        wca_matrix[8]    if len(wca_matrix) > 8 else [0],
                        wca_matrix[9]    if len(wca_matrix) > 9 else [0]
                    ]
                    
                    # Set startPoint
                    self.startPoint = wca_startpoint
                    
                    # Find indices and create parameter map
                    self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, mode)
                    self.matrix = self.findStart(self.sweepMatrix, self.idx, mode)
                    self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, mode, original_Xs)
                    self.iterNumber = 0
                    
                    # Store this iteration's map
                    all_iteration_maps.append({
                        'iteration': wca_iteration,
                        'map': self.Map,
                        'iterations': self.Iterations,
                        'shape': self.Map
                    })
                
                # Store all iteration maps and return the last one for compatibility
                self.all_wca_maps = all_iteration_maps
                
                if all_iteration_maps:
                    # Return the last iteration map (or you could return all)
                    last_map = all_iteration_maps[-1]['map']
                    last_iterations = all_iteration_maps[-1]['iterations']
                    
                    # Store the last iteration as current state
                    self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
                    self.startPoint = startPoint
                    self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, mode)
                    self.matrix = self.findStart(self.sweepMatrix, self.idx, mode)
                    self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, mode, original_Xs)
                    self.iterNumber = 0
                    
                    return last_map, last_iterations
                else:
                    return None, 0
            
        
        
        else:  # Normal mode
            # Original Normal mode behavior
            self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
            self.startPoint = startPoint
            self.idx, itrr = self.findIndex(self.startPoint, self.sweepMatrix, mode)
            self.matrix = self.findStart(self.sweepMatrix, self.idx, mode)
            self.Map, self.Iterations = self.findPoint(self.matrix, self.idx, mode, original_Xs)
            self.iterNumber = 0
            return self.Map, self.Iterations

# Main function - simplified to one call
def main():
    analyzer = WCAAnalyzer()
    
    # Use the unified function to load and process variables
    data = analyzer.load_and_process_variables('Input_vars.json')
    Xs = data['Xs']
    mode = data['mode']
    
    # Get the already processed startPoint from our unified function
    processed_startpoint = data['startPoint']
    
    # Single call to init_sim - now handles both modes internally
    simulation_map, iterations = analyzer.init_sim(
        maxThreads=1,
        startPoint=processed_startpoint,
        X1=[0], X2=[0], X3=[0], X4=[0], X5=[0], X6=[0], X7=[0], X8=[0], X9=[0], X10=[0],  # Placeholders
        model='DCDC',
        mode=mode,
        original_Xs=Xs  # Pass original Xs for WCA mode
    )
    
    if simulation_map is not None:
        print(f"{mode} mode total iterations: {iterations}")
        
      
        print(f"Normal mode simulations: {simulation_map}")
        
if __name__ == "__main__":
    main()
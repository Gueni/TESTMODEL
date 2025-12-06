def findPoint(self, matrix, index, mode="Normal", original_Xs=None):
    """
        Generate parameter map based on mode.
        
        For WCA mode: Returns 2D array with 2**Nactive rows × 10 variables
        Each cell contains calculated WCA values for that variable based on original_Xs
    """
    def get_original_nominals(Xs):
         
            OXs = [
                [[nom] for nom, tol, min_val, max_val in var_data] 
                if var_data != [[0]] else [[0]]
                for var_data in Xs
            ]
            return OXs
    original_Xs = get_original_nominals(original_Xs)
    
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
        # Count active variables
        active_vars = sum(1 for var_data in original_Xs if var_data != [[0]])
        total_iterations = 2 ** active_vars
        
        # Create ParametersMap with 2**active_vars rows and 10 columns
        ParametersMap = []
        
        # Generate all WCA combinations
        for iteration in range(total_iterations):
            row = []
            
            # For each of the 10 variables
            for var_idx in range(10):
                if var_idx < len(original_Xs) and original_Xs[var_idx] != [[0]]:
                    # This is an active variable
                    var_data = original_Xs[var_idx]
                    var_values = []
                    
                    # Calculate WCA for each value in this variable
                    for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                        if tol <= 1:
                            # Absolute tolerance
                            x = self.funtol(Abs_rel=True, iteration=iteration, index=var_idx, nom=nom, tol=tol)
                        else:
                            # Relative tolerance
                            x = self.funtol(Abs_rel=False, iteration=iteration, index=var_idx, nom=nom, tol=tol)
                        
                        # Apply min/max bounds
                        wca_value = min(max(x, min_val), max_val)
                        var_values.append(wca_value)
                    
                    row.append(var_values)
                else:
                    # Inactive variable or beyond available Xs
                    row.append([])
            
            ParametersMap.append(row)
        
        # Convert to numpy array for consistency
        ParametersMap = np.array(ParametersMap, dtype=object)
        
        # Apply slicing based on index
        if index and len(index) > 0:
            start_idx = index[-1] if isinstance(index, list) else index
            if start_idx < total_iterations:
                return ParametersMap[start_idx:], len(ParametersMap[start_idx:])
        
        return ParametersMap, total_iterations
    
    else:
        raise ValueError(f"Unsupported mode: {mode}. Use 'Normal' or 'WCA'.")
# Import the JSON module for parsing JSON strings in the configuration
import json
# Import NumPy for numerical operations and matrix manipulations
import numpy as np

def get_active_wca_params(Xs):
    """
    Identify which parameters X lists are used in Worst-Case Analysis (WCA).
    
    This function examines a list of parameter lists (X1 through X10) and identifies
    which ones are active for WCA. Active parameters are those that are not placeholder zero values.
    
    Parameters:
        Xs (list): List of parameter lists for X1-X10, where each element is a list
                  of parameter values. Placeholder values are either [0] or [[0]].
        
    Returns:
        list: Indices of parameters that are not placeholder values.
    """
    # Use list comprehension to iterate through enumerated Xs list
    # enumerate provides both index (i) and value (var) for each parameter list
    return [i for i, var in enumerate(Xs) 
            # Check if var is NOT a placeholder zero value
            # Placeholders can be either [0] or [[0]] (nested list with zero)
            if var not in [[[0]], [0]] 
            # Ensure the list has elements (not empty)
            and len(var) > 0]

def add_perturbations(config_data, perturbation_value, perturbation_type='absolute'):
    """
    Add perturbations to active WCA parameters in the configuration.
    
    This function takes a configuration dictionary containing X1-X10 parameter lists,
    identifies active WCA parameters, and applies perturbations to create a matrix 
    of perturbed values for sensitivity analysis. The resulting structure has:
    - For each active parameter: a list of (n_vars + 1) values
    - The first n_vars positions represent sequential perturbations (one per parameter)
    - The last position is the nominal value (all parameters at nominal)
    
    The function supports three types of perturbations:
    - 'absolute': Adds the perturbation value to nominal values
    - 'relative': Multiplies nominal values by (1 + perturbation/100)
    - 'multiplicative': Multiplies nominal values by perturbation factor
    
    Args:
        config_data (dict): Configuration dictionary containing X1-X10 keys with
                           JSON string values representing parameter lists (single values)
        perturbation_value (float): The magnitude of perturbation to apply
        perturbation_type (str): Type of perturbation - 'absolute', 'relative', 
                                or 'multiplicative' (default: 'absolute')
        
    Returns:
        list: Updated X lists with perturbations applied to active parameters
        
    Raises:
        ValueError: If an unknown perturbation type is provided
    """
    # Load X1-X10 parameters from config_data by iterating through indices 1-10
    # For each X{i}, parse the JSON string to get the actual list
    # If key doesn't exist, default to "[0]" (placeholder zero)
    Xs = [json.loads(config_data.get(f"X{i}", "[0]")) for i in range(1, 11)]
    
    # Get the indices of active parameters (those that are not placeholder zeros)
    active_indices = get_active_wca_params(Xs)
    
    # Determine the number of active variables for matrix sizing
    n_vars = len(active_indices)
    
    # Extract the nominal values for active parameters (these are single values)
    nominal_values = [Xs[i][0] if isinstance(Xs[i], list) and len(Xs[i]) > 0 else Xs[i] 
                      for i in active_indices]
    
    # Create a matrix where each row corresponds to one active parameter
    # Each row will have (n_vars + 1) values:
    # - First n_vars positions: sequential perturbations
    # - Last position: nominal value (all parameters at nominal)
    result_matrix = np.zeros((n_vars, n_vars + 1))
    
    # Fill the matrix with nominal values everywhere initially
    for i in range(n_vars):
        result_matrix[i, :] = nominal_values[i]
    
    # Apply perturbations to the diagonal elements (i,i) for i from 0 to n_vars-1
    for i in range(n_vars):
        nominal = nominal_values[i]
        
        if perturbation_type == 'absolute':
            # Absolute perturbation: add perturbation value
            perturbed_value = nominal + perturbation_value
            
        elif perturbation_type == 'relative':
            # Relative perturbation: multiply by (1 + perturbation/100)
            perturbed_value = nominal * (1 + perturbation_value / 100)
            
        elif perturbation_type == 'multiplicative':
            # Multiplicative perturbation: multiply by perturbation factor
            perturbed_value = nominal * perturbation_value
            
        else:
            raise ValueError(f"Unknown perturbation type: {perturbation_type}")
        
        # Set the perturbed value at position i (sequential perturbation)
        result_matrix[i, i] = perturbed_value
    
    # Update the active X lists with the perturbed values
    # Iterate through active indices and their corresponding result rows simultaneously
    for idx, result_row in zip(active_indices, result_matrix):
        # Convert the NumPy row back to a regular Python list
        # and assign it to the corresponding position in Xs
        Xs[idx] = result_row.tolist()
    
    # Return the complete list of updated X parameters
    return Xs

# Example usage section - demonstrates how to use the add_perturbations function
# Define a sample configuration dictionary with X1-X10 parameters (single nominal values)
your_config = {
    # X1-X4 are active parameters with single nominal values
    "X1": "[35]",      # First parameter (e.g., Water Temperature)
    "X2": "[200]",     # Second parameter (e.g., Input Voltage)
    "X3": "[11.5]",    # Third parameter (e.g., Output Voltage)
    "X4": "[500]",     # Fourth parameter (e.g., Output Power)
    # X5-X10 are inactive placeholders with single zero values
    "X5": "[66]",       # Placeholder for unused parameter
    "X6": "[96369]",       # Placeholder for unused parameter
    "X7": "[0]",       # Placeholder for unused parameter
    "X8": "[0]",       # Placeholder for unused parameter
    "X9": "[0]",       # Placeholder for unused parameter
    "X10": "[0]",      # Placeholder for unused parameter
    # Names for each parameter (for display/reference purposes)
    "sweepNames": ["Water Temperature", "Input Voltage", "Output Voltage", 
                   "Output Power", "test", "cdvfgfX6", "X7", "X8", "X9", "X10"]
}


result_xlists_abs = add_perturbations(your_config, 0.1, 'absolute')
for i, xlist in enumerate(result_xlists_abs):  # Show only first 4 active parameters
    print(f"X{i+1}: {xlist}")

# Test with relative perturbation (10% perturbation)
print("\n=== RELATIVE PERTURBATION (10%) ===")
result_xlists_rel = add_perturbations(your_config, 10, 'relative')
for i, xlist in enumerate(result_xlists_rel):
    print(f"X{i+1}: {[round(val, 2) for val in xlist]}")  # Round for display

# Test with multiplicative perturbation (multiply by 1.1)
print("\n=== MULTIPLICATIVE PERTURBATION (factor=1.1) ===")
result_xlists_mul = add_perturbations(your_config, 1.1, 'multiplicative')
for i, xlist in enumerate(result_xlists_mul):
    print(f"X{i+1}: {[round(val, 2) for val in xlist]}")
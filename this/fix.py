def format_octave_struct_from_mappings(mappings, solver_opts_var='SolverOpts'):
    """
    Creates nested Octave struct based only on the paths found in ScriptBody mappings.
    
    This function takes a dictionary of variable mappings and builds an Octave structure
    string that represents the same hierarchical organization. It extracts all unique
    paths from the mappings and constructs a nested struct with placeholder values.
    
    Args:
        mappings: Dictionary of mappings from octave_sweep_mapping
                  Format: {1: 'simStruct.ModelVars.Common.Thermal.Twater = data{sim}{1}(1)', ...}
        solver_opts_var: The name of the SolverOpts variable (default: 'SolverOpts')
        
    Returns:
        A string with Octave struct syntax ready to be used in Octave scripts
    """
    # Initialize an empty set to store all unique paths extracted from mappings
    paths = set()
    
    # Iterate through each mapping expression in the mappings dictionary
    for expr in mappings.values():
        # Split the expression at the equals sign and take the left part (the path)
        # Then remove any leading/trailing whitespace
        path = expr.split('=')[0].strip()
        
        # Check if the path starts with the 'simStruct.ModelVars.' prefix
        if path.startswith('simStruct.ModelVars.'):
            # Remove the prefix by slicing from the end of the prefix string
            # This gives us just the relative path within ModelVars
            path = path[len('simStruct.ModelVars.'):]
        
        # Add the cleaned path to our set of unique paths
        # Using a set automatically eliminates duplicates
        paths.add(path)
    
    # Call helper function to build a nested structure string from the set of paths
    # This converts dot-separated paths into nested Octave struct syntax
    nested_struct = build_nested_struct_from_paths(paths)
    
    # Return the complete Octave struct assignment string
    # Format: simStruct = struct('ModelVars', <nested_struct>, 'SolverOpts', <solver_opts_var>);
    return f"simStruct = struct('ModelVars', {nested_struct}, 'SolverOpts', {solver_opts_var});"


def build_nested_struct_from_paths(paths):
    """
    Recursively builds a nested struct string from a set of dot-separated paths.
    
    This function converts a set of dot-notation paths into a nested Octave struct
    representation. It first builds a nested dictionary structure, then converts
    that dictionary to Octave struct syntax.
    
    Example paths:
        'Common.Thermal.Twater'
        'Common.Control.Targets.Vout'
        'Common.Control.Targets.Pout'
        'DCDC_Rail1.Control.Inputs.Vin'
        'DCDC_Rail1.Control.Inputs.Iin'
        'DCDC_Rail1.Control.Inputs.Vout'
        'DCDC_Rail1.Control.Inputs.Pout'
        'Common.Load.Front.R_L'
    
    Returns:
        "struct('Common', struct('Thermal', struct('Twater', 0), 'Control', struct('Targets', struct('Vout', 0, 'Pout', 0)), 'Load', struct('Front', struct('R_L', 0))), 'DCDC_Rail1', struct('Control', struct('Inputs', struct('Vin', 0, 'Iin', 0, 'Vout', 0, 'Pout', 0))))"
    """
    # Initialize an empty dictionary to serve as the root of our nested structure
    root = {}
    
    # Process each path in the set of paths
    for path in paths:
        # Split the path by dots to get individual components
        # Example: 'Common.Thermal.Twater' becomes ['Common', 'Thermal', 'Twater']
        parts = path.split('.')
        
        # Start at the root of our nested dictionary
        current = root
        
        # Iterate through each part of the path with its index
        for i, part in enumerate(parts):
            # Check if this is the last part of the path (leaf node)
            if i == len(parts) - 1:
                # Check if this leaf node doesn't already exist in the current dictionary
                if part not in current:
                    # Create leaf node with placeholder value 0
                    # This will be replaced with actual data during simulation
                    current[part] = 0
            else:
                # This is an intermediate node (not a leaf)
                # Check if this intermediate node doesn't exist in the current dictionary
                if part not in current:
                    # Create a new empty dictionary for this intermediate node
                    current[part] = {}
                
                # Move deeper into the nested structure by updating current
                # to point to the newly created or existing dictionary
                current = current[part]
    
    # Convert the nested dictionary structure to Octave struct syntax
    # Call helper function dict_to_struct to perform the recursive conversion
    return dict_to_struct(root)


def dict_to_struct(d):
    """
    Recursively converts a nested dictionary to Octave struct syntax.
    
    This function traverses a nested dictionary and generates the corresponding
    Octave struct creation code. Dictionary keys become field names, and nested
    dictionaries become nested structs.
    
    Args:
        d: A nested dictionary representing the structure to convert
        
    Returns:
        A string containing Octave struct creation code
    """
    # Initialize an empty list to store key-value pairs for struct creation
    items = []
    
    # Iterate through all key-value pairs in the dictionary
    for key, value in d.items():
        # Check if the value is another dictionary (indicating nested structure)
        if isinstance(value, dict):
            # Recursively convert the nested dictionary to struct syntax
            nested = dict_to_struct(value)
            # Add the key and nested struct to items list
            # Format: 'field_name', nested_struct
            items.append(f"'{key}', {nested}")
        else:
            # This is a leaf node - use placeholder value 0
            # Format: 'field_name', 0
            items.append(f"'{key}', 0")
    
    # Check if there are no items in the dictionary (empty dictionary case)
    if not items:
        # Return empty struct for empty dictionary
        return 'struct()'
    
    # Return complete struct creation string with all items joined by commas
    # Format: struct('field1', value1, 'field2', value2, ...)
    return f"struct({', '.join(items)})"
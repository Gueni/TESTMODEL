def format_octave_struct_from_mappings(mappings, solver_opts_var='SolverOpts'):
    """
    Creates nested Octave struct based only on the paths found in ScriptBody mappings.
    
    Args:
        mappings: Dictionary of mappings from octave_sweep_mapping
                  Format: {1: 'simStruct.ModelVars.Common.Thermal.Twater = data{sim}{1}(1)', ...}
        solver_opts_var: The name of the SolverOpts variable
        
    Returns:
        A string with Octave struct syntax
    """
    # Extract all unique paths from mappings
    paths = set()
    for expr in mappings.values():
        # Extract the left side of the assignment (the path)
        path = expr.split('=')[0].strip()
        # Remove 'simStruct.ModelVars.' prefix
        if path.startswith('simStruct.ModelVars.'):
            path = path[len('simStruct.ModelVars.'):]
        paths.add(path)
    
    # Build nested structure from paths
    nested_struct = build_nested_struct_from_paths(paths)
    
    return f"simStruct = struct('ModelVars', {nested_struct}, 'SolverOpts', {solver_opts_var});"

def build_nested_struct_from_paths(paths):
    """
    Recursively builds a nested struct string from a set of dot-separated paths.
    
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
    # Build a nested dictionary structure from paths
    root = {}
    
    for path in paths:
        parts = path.split('.')
        current = root
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                # Last part - leaf node
                if part not in current:
                    current[part] = 0  # Placeholder value
            else:
                # Intermediate node
                if part not in current:
                    current[part] = {}
                current = current[part]
    
    # Convert the nested dictionary to struct syntax
    return dict_to_struct(root)

def dict_to_struct(d):
    """
    Recursively converts a nested dictionary to Octave struct syntax.
    """
    items = []
    for key, value in d.items():
        if isinstance(value, dict):
            # If value is a dict, recursively convert it
            nested = dict_to_struct(value)
            items.append(f"'{key}', {nested}")
        else:
            # Leaf node - use placeholder value
            items.append(f"'{key}', 0")
    
    if not items:
        return 'struct()'
    
    return f"struct({', '.join(items)})"
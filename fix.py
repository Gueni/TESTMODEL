def format_octave_struct(model_vars_dict, solver_opts_var='SolverOpts'):
    """
    Formats first-order dictionary names for Octave struct syntax.
    Creates nested struct structure with placeholder values.
    """
    model_vars_names = []
    
    # For each top-level dictionary (Common, DCDC_Rail1, etc.)
    for key, value in model_vars_dict.items():
        if isinstance(value, dict):
            model_vars_names.append(key)
    
    if model_vars_names:
        # Build the nested struct structure
        # This will create something like:
        # struct('Common', struct('Thermal', struct('Twater', 0), 'Control', struct('Targets', struct('Vout', 0, 'Pout', 0))), 
        #        'DCDC_Rail1', struct('Control', struct('Inputs', struct('Vin', 0, 'Iin', 0, 'Vout', 0, 'Pout', 0))))
        
        struct_parts = []
        for name in model_vars_names:
            # Get the actual dictionary for this name
            top_dict = model_vars_dict.get(name, {})
            
            # Build the nested struct for this top-level dictionary
            nested_struct = build_nested_struct(top_dict)
            struct_parts.append(f"'{name}', {nested_struct}")
        
        model_vars_str = ', '.join(struct_parts)
        model_vars_part = f"struct({model_vars_str})"
    else:
        model_vars_part = 'struct()'
    
    return f"simStruct = struct('ModelVars', {model_vars_part}, 'SolverOpts', {solver_opts_var});"

def build_nested_struct(d, indent=0):
    """
    Recursively builds a nested struct string from a dictionary.
    """
    if not isinstance(d, dict):
        # This shouldn't happen as we only call on dicts
        return '0'
    
    items = []
    for key, value in d.items():
        if isinstance(value, dict):
            # If value is a dict, recursively build its struct
            nested = build_nested_struct(value, indent + 1)
            items.append(f"'{key}', {nested}")
        else:
            # If value is not a dict, use a placeholder (0)
            items.append(f"'{key}', 0")
    
    if not items:
        return 'struct()'
    
    return f"struct({', '.join(items)})"
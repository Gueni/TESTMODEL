
import re
from jinja2 import Environment, FileSystemLoader
import os
import numpy as np  # You may need to install numpy or implement without it

def inject_octave_simple(plecs_file_path, output_file_path, octave_code):
    Script_name = "Script"
    
    with open(plecs_file_path, 'r') as f: 
        content = f.read()
    
    escaped_code = octave_code.replace('"', '\\"')
    
    # Create the new script section
    new_script_section = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
    }}'''
    
    # CASE 1: Check for empty script section
    empty_script_pattern = r'Script\s*{\s*Name\s+"Script"\s*Script\s+""\s*}'
    if re.search(empty_script_pattern, content, re.DOTALL):
        new_content = re.sub(empty_script_pattern, new_script_section, content, flags=re.DOTALL)
    
    # CASE 2: Check for any script section (empty or not)
    elif re.search(r'Script\s*{.*?}', content, re.DOTALL):
        script_sections = list(re.finditer(r'Script\s*{.*?}', content, re.DOTALL))
        last_script = script_sections[-1]
        insert_pos = last_script.end()
        new_content = content[:insert_pos] + '\n' + new_script_section + content[insert_pos:]
    
    # CASE 3: No script section at all
    else:
        last_brace_pos = content.rfind('}')
        if last_brace_pos != -1:
            new_content = content[:last_brace_pos] + '\n' + new_script_section + content[last_brace_pos:]
        else:
            new_content = content + '\n' + new_script_section
    
    with open(output_file_path, 'w') as f: 
        f.write(new_content)

def format_octave_struct(model_vars_dict, solver_opts_var='SolverOpts'):
    """
    Formats first-order dictionary names for Octave struct syntax.
    """
    model_vars_names = []
    for key, value in model_vars_dict.items():
        if isinstance(value, dict):
            model_vars_names.append(key)
    
    if model_vars_names:
        model_vars_str = ', '.join(model_vars_names)
        model_vars_part = f'struct({model_vars_str})'
    else:
        model_vars_part = 'struct()'
    
    return f"simStruct = struct('ModelVars', {model_vars_part}, 'SolverOpts', {solver_opts_var});"

def detect_mapvars_dimensions(mapvars):
    """
    Detect if mapvars is 2D or 3D and return the appropriate indexing pattern.
    """
    # Check the first element
    first_elem = mapvars[0]
    
    if isinstance(first_elem, list):
        if first_elem and isinstance(first_elem[0], list):
            return 3  # 3D: list of lists of lists
        else:
            return 2  # 2D: list of lists

def octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict):
    template_file = 'D:\WORKSPACE\TESTMODEL\octave_sweep_template.m.j2'
    
    env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    
    filtered = [x for x in sweepnames if not (x.startswith("X") and x[1:].isdigit())]
    
    # Detect mapvars dimensions
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    
    # Generate the simStruct line
    simstruct_line = format_octave_struct(model_vars_dict)
    
    return template.render(
        mapvars=mapvars,  # Pass the original structure
        sweepnames=filtered,
        mappings=mappings,
        num_params=len(filtered),
        simstruct_line=simstruct_line,
        mapvars_dim=mapvars_dim  # Pass dimension info to template
    )

def octave_sweep_mapping(file_path, mapvars):
    """
    Extract mappings from ScriptBody.py with support for both 2D and 3D mapvars.
    """
    import re
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    print('Detected mapvars dimension:', mapvars_dim)
    mappings = {}
    pattern = r"(mdlVars.*?=\s*.+)"
    
    with open(file_path, 'r') as f:
        content = f.read()

    for match in re.finditer(pattern, content):
        line = match.group().strip()
        if '=' not in line:
            continue
        left, right = line.split('=', 1)

        path_match = re.search(r"mdlVars(.*?)$", left.strip())
        if not path_match:
            continue
        path = path_match.group(1)
        
        # Build the full path
        full_path = 'mdlVars'
        for part in re.findall(r"\[['\"](.*?)['\"]\]", path):
            full_path += f'.{part}'
        
        # Replace 'mdlVars.' with 'simStruct.ModelVars.'
        if full_path.startswith('mdlVars.'):
            octave_path = 'simStruct.ModelVars.' + full_path[8:]
        else:
            octave_path = 'simStruct.ModelVars.' + full_path

        # Find all mapVars[Xn] occurrences with possible additional indexing
        # Pattern matches mapVars[X1][0] or mapVars[X1]
        mapvar_pattern = r"mapVars\[X(\d+)\](?:\[(\d+)\])?"
        
        # First, find all matches to understand the indexing structure
        all_matches = list(re.finditer(mapvar_pattern, right))
        if not all_matches:
            continue

        expr = right.strip()

        # Replace Python operators with Octave operators
        expr = expr.replace('**', '^')

        # Process each mapVar occurrence
        x_vars = []
        for match in all_matches:
            x_num = match.group(1)      # The X number (1, 2, 3, etc.)
            idx1 = match.group(2)       # The index inside the vector if present
            
            x_vars.append(int(x_num))
            
            if mapvars_dim == 3:
                # 3D case: cell array of cell arrays of vectors
                if idx1 is not None:
                    # Has index: mapVars[X1][0] -> data{sim}{X1}(index+1)
                    element_idx = int(idx1) + 1
                    replacement = f"data{{sim}}{{{x_num}}}({element_idx})"
                else:
                    # No index: mapVars[X1] -> access first element
                    replacement = f"data{{sim}}{{{x_num}}}(1)"
            else:
                # 2D case: regular matrix
                if idx1 is not None:
                    # Has index: mapVars[X1][0] -> data(sim, column) where column = X1
                    # In 2D, each X corresponds to a column in the data matrix
                    # The index inside the vector is not needed for 2D since each column has one value
                    replacement = f"data(sim,{x_num})"
                else:
                    # No index: mapVars[X1] -> data(sim, X1)
                    replacement = f"data(sim,{x_num})"
            
            # Replace the exact match
            original = f"mapVars[X{x_num}]" + (f"[{idx1}]" if idx1 else "")
            expr = expr.replace(original, replacement)

        # Store mapping with dependency info
        mappings[octave_path] = {"expr": f"{octave_path} = {expr.strip()}", 
                                 "deps": list(set(x_vars))}

    # Dependency-aware ordering: sort by max Xi in RHS
    ordered_mappings = dict(sorted(mappings.items(), key=lambda kv: max(kv[1]["deps"])))

    # Return only the expression string for template
    return {i+1: v["expr"] for i, (k, v) in enumerate(ordered_mappings.items())}

if __name__ == "__main__":
    # Your 3D input data
    mapvars = [
        [[25, 300, 5, 180], [25, 300, 10, 280], [3, 5, 0.6, 9], [25, 300, 5, 180]],
        [[20, 200, 10, 200], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[20, 300, 5, 150], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[20, 300, 10, 250], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[25, 200, 5, 120], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[25, 200, 10, 220], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[25, 300, 5, 180], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[25, 300, 10, 280], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[30, 200, 5, 140], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[30, 200, 10, 240], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[30, 300, 5, 190], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]],
        [[30, 300, 10, 290], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200]]
    ]
    # mapvars = [
    #     [20, 200, 5, 100],
    #     [20, 200, 10, 200],
    #     [20, 300, 5, 150],
    #     [20, 300, 10, 250],
    #     [25, 200, 5, 120],
    #     [25, 200, 10, 220],
    #     [25, 300, 5, 180],
    #     [25, 300, 10, 280],
    #     [30, 200, 5, 140],
    #     [30, 200, 10, 240],
    #     [30, 300, 5, 190],
    #     [30, 300, 10, 290]
    # ]
    sweepnames = ["Water Temperature", "Input Voltage", "Output Current"]
    
    # Detect mapvars dimensions
   
    
    # Extract mappings from ScriptBody.py with dimension info
    mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\ScriptBody.py', mapvars)
    print("Extracted mappings:", mappings)
    
    model_vars_dict = { 
        'Common': {'Water_Temperature': {'value': 20}, 'Input_Voltage': {'value': 200}, 'Output_Current': {'value': 100}},
        'DCDC_Rail1': {}
    }
    
    # Generate Octave code
    octave_code = octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict)
    print(octave_code)









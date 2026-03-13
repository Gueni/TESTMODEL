
import re
from jinja2 import Environment, FileSystemLoader
import os
import numpy as np  # You may need to install numpy or implement without it

from jinja2 import Template
import re

def inject_octave_simple(plecs_file_path, output_file_path, m_file_path):
    """
    Reads Octave code from an .m file and injects it into the PLECS file.
    
    Args:
        plecs_file_path: Path to the source .plecs file
        output_file_path: Path to the output .plecs file
        m_file_path: Path to the .m file containing the Octave script
    """
    Script_name = "Script"
    
    # Read the PLECS file
    with open(plecs_file_path, 'r') as f: 
        content = f.read()
    
    # Read the Octave code from .m file
    with open(m_file_path, 'r') as f:
        octave_code = f.read()
    
    # Escape for PLECS script section
    escaped_code = octave_code.replace('\\', '\\\\').replace('"', '\\"')
    
    # Create the new script section
    new_script_section = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
  }}'''
    
    # CASE 1: Check for empty script section
    empty_script_pattern = r'Script\s*{\s*Name\s+"Script"\s*Script\s+""\s*}'
    if re.search(empty_script_pattern, content, re.DOTALL):
        new_content = re.sub(empty_script_pattern, new_script_section, content, flags=re.DOTALL)
        print("Case 1: Replaced empty script section")
    
    # CASE 2: Check for any script section (empty or not)
    elif re.search(r'Script\s*{.*?}', content, re.DOTALL):
        script_sections = list(re.finditer(r'Script\s*{.*?}', content, re.DOTALL))
        last_script = script_sections[-1]
        insert_pos = last_script.end()
        new_content = content[:insert_pos] + '\n' + new_script_section + content[insert_pos:]
        print("Case 2: Appended after existing script section")
    
    # CASE 3: No script section at all
    else:
        last_brace_pos = content.rfind('}')
        if last_brace_pos != -1:
            new_content = content[:last_brace_pos] + '\n' + new_script_section + content[last_brace_pos:]
            print("Case 3: Inserted before final brace")
        else:
            new_content = content + '\n' + new_script_section
            print("Case 3: Appended at end")
    
    # Write the modified PLECS file
    with open(output_file_path, 'w') as f: 
        f.write(new_content)
    
    print(f"✅ Injected {m_file_path} into {output_file_path}")



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

# def octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict):
#     template_file = 'octave_sweep_template.m.j2'
    
#     env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True, lstrip_blocks=True)
#     template = env.get_template(template_file)
    
#     filtered = [x for x in sweepnames if not (x.startswith("X") and x[1:].isdigit())]
    
#     # Detect mapvars dimensions
#     mapvars_dim = detect_mapvars_dimensions(mapvars)
    
#     # Generate the simStruct line
#     simstruct_line = format_octave_struct(model_vars_dict)
    
#     return template.render(
#         mapvars=mapvars,  # Pass the original structure
#         sweepnames=filtered,
#         mappings=mappings,
#         num_params=len(filtered),
#         simstruct_line=simstruct_line,
#         mapvars_dim=mapvars_dim  # Pass dimension info to template
#     )
def format_octave_struct_from_mappings(mappings, solver_opts_var='struct()'):
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

def octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict ,scopes_list):
    template_file = 'octave_sweep_template.m.j2'
    
    env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    
    filtered = [x for x in sweepnames if not (x.startswith("X") and x[1:].isdigit())]
    
    # Detect mapvars dimensions
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    # Generate the simStruct line
    simstruct_line = format_octave_struct_from_mappings(mappings)


    results_folder = os.path.join(os.getcwd(), 'simulation_results')

    # Create the directory if it doesn't exist
    os.makedirs(results_folder, exist_ok=True)

    return template.render(
        mapvars=mapvars,
        sweepnames=filtered,
        mappings=mappings,
        num_params=len(filtered),
        simstruct_line=simstruct_line,
        mapvars_dim=mapvars_dim,
        scopes=scopes_list,
        results_folder=results_folder  # Pass the results folder path
    )

def octave_sweep_mapping(file_path, mapvars):
    """
    Extract mappings from ScriptBody.py with support for both 2D and 3D mapvars.
    """
    import re
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    print('Detected mapvars dimension:', mapvars_dim)
    mappings = {}  # Will store in original order
    pattern = r"(mdlVars.*?=\s*.+)"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract only the section between the "Don't change" comments
    start_marker = "#! -------------------------------------------------------------------------------------Don't change above this line---------------------------------------------------------------------------"
    end_marker = "#! -------------------------------------------------------------------------------------Don't change under this line---------------------------------------------------------------------------"

    section_pattern = start_marker + r"\s*(.*?)\s*" + end_marker
    section_match = re.search(section_pattern, content, re.DOTALL)
    
    if not section_match:
        print("Warning: Could not find the section between comment markers")
        return {}
    
    # Use only the content between the markers
    section_content = section_match.group(1)
    
    # Process lines in order to preserve sequence
    lines = section_content.split('\n')
    mapping_counter = 1
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check if it's an assignment line
        if '=' not in line:
            continue
            
        left, right = line.split('=', 1)
        left = left.strip()
        right = right.strip()
        
        # Extract the path from left side
        path_match = re.search(r"mdlVars(.*?)$", left)
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
        
        # Check if this is a derived parameter (uses other mdlVars)
        if re.search(r"mdlVars(\[['\"].*?['\"]\])+", right):
            # This is a derived parameter
            expr = right
            
            # Replace Python operators with Octave operators
            expr = expr.replace('**', '^')
            
            # Replace all mdlVars references with simStruct.ModelVars
            dep_pattern = r"mdlVars(\[['\"].*?['\"]\])+"
            def replace_dep(match):
                dep_path = match.group(0)
                dep_parts = re.findall(r"\[['\"](.*?)['\"]\]", dep_path)
                return 'simStruct.ModelVars.' + '.'.join(dep_parts)
            
            expr = re.sub(dep_pattern, replace_dep, expr)
            
            # Store with original order
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            mapping_counter += 1
            
        else:
            # This is a direct mapVars assignment
            # Find all mapVars[Xn] occurrences with possible additional indexing
            mapvar_pattern = r"mapVars\[X(\d+)\](?:\[(\d+)\])?"
            
            all_matches = list(re.finditer(mapvar_pattern, right))
            if not all_matches:
                continue

            expr = right

            # Replace Python operators with Octave operators
            expr = expr.replace('**', '^')

            # Process each mapVar occurrence
            for match in all_matches:
                x_num = match.group(1)
                idx1 = match.group(2)
                
                if mapvars_dim == 3:
                    if idx1 is not None:
                        element_idx = int(idx1) + 1
                        replacement = f"data{{sim}}{{{x_num}}}({element_idx})"
                    else:
                        replacement = f"data{{sim}}{{{x_num}}}(1)"
                else:
                    if idx1 is not None:
                        replacement = f"data(sim,{x_num})"
                    else:
                        replacement = f"data(sim,{x_num})"
                
                original = f"mapVars[X{x_num}]" + (f"[{idx1}]" if idx1 else "")
                expr = expr.replace(original, replacement)

            # Store with original order
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            mapping_counter += 1

    return mappings



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
    scopes_list = ['Line-to-Line', 'Lines-to-Neutral', ' Lines-to-Chassis']  # Example scope names
    # Generate Octave code
    octave_code = octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict , scopes_list)
    import datetime
    folder_path =os.getcwd()  # You can change this to your desired folder path
    # One-liner to save with UTC timestamp
    with open(f'{folder_path}/ScriptBody_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.m', 'w') as f: f.write(octave_code)
    print(octave_code)




    # Example usage
    inject_octave_simple(
        plecs_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
        output_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
        m_file_path=r'D:\WORKSPACE\TESTMODEL\ScriptBody_20260312_213544.m'  # Your .m file
    )




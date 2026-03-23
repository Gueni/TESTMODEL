# Import the regular expression module for pattern matching
import re
# Import Jinja2 templating engine for generating Octave scripts from templates
from jinja2 import Environment, FileSystemLoader
# Import operating system module for file path operations
import os
# Import numpy for numerical operations (may need to install numpy or implement without it)
import numpy as np

# Re-import jinja2 Template (though already imported above)
from jinja2 import Template
# Re-import re (though already imported above)
import re
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

def inject_octave(plecs_file_path, output_file_path, m_file_path):
    """
    Reads Octave code from an .m file and injects it into the PLECS file.
    
    Parameters:
                    plecs_file_path     : Path to the source .plecs file
                    output_file_path    : Path to the output .plecs file
                    m_file_path         : Path to the .m file containing the Octave script
    """
    
    # Create the new script section in PLECS XML-like format
    new_script_section  = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
  }}'''
    
    # Define the name of the script section in PLECS
    Script_name                                     = "Script"
    
    # Read the entire content of the PLECS file into a string
    with open(plecs_file_path, 'r') as f: content   = f.read()
    
    # Read the entire Octave script code into a string
    with open(m_file_path, 'r') as f:octave_code    = f.read()
    
    # Replace backslashes with double backslashes and double quotes with escaped double quotes
    escaped_code                                    = octave_code.replace('\\', '\\\\').replace('"', '\\"')
    
    # CASE 1: Check for empty script section pattern : Script { Name "Script" Script "" }
    empty_script_pattern = r'Script\s*{\s*Name\s+"Script"\s*Script\s+""\s*}'

    # Search for empty script pattern in the content
    if re.search(empty_script_pattern, content, re.DOTALL):

        # Replace the empty script section with the new populated script section
        new_content = re.sub(empty_script_pattern, new_script_section, content, flags=re.DOTALL)
    
    # CASE 2: Check for any existing script section
    elif re.search(r'Script\s*{.*?}', content, re.DOTALL):

        # Find all script sections in the content
        script_sections = list(re.finditer(r'Script\s*{.*?}', content, re.DOTALL))

        # Get the last script section found
        last_script     = script_sections[-1]

        # Get the end position of the last script section
        insert_pos      = last_script.end()

        # Insert new script section after the last existing script section
        new_content     = content[:insert_pos] + '\n' + new_script_section + content[insert_pos:]

    # CASE 3: No script section found at all in the file
    else:

        # Find the position of the last closing brace in the file
        last_brace_pos  = content.rfind('}')

        # Check if a closing brace was found
        # Insert new script section before the final closing brace
        new_content     = content[:last_brace_pos] + '\n' + new_script_section + content[last_brace_pos:]

    # Write the modified content back to the output PLECS file
    with open(output_file_path, 'w') as f: f.write(new_content)
    
def detect_mapvars_dimensions(mapvars):
    """
    Detect if mapvars is 2D or 3D and return the appropriate indexing pattern.
    
    This function analyzes the structure of the mapvars parameter to determine
    whether it's a 2D or 3D list structure.
    
    Args:
        mapvars: A nested list structure containing parameter values for sweep
        
    Returns:
        Integer: 2 for 2D list structure, 3 for 3D list structure
    """
    # Get the first element of mapvars to analyze its structure
    first_elem = mapvars[0]
    
    # Check if the first element is a list (indicating nested structure)
    if isinstance(first_elem, list):
        # Check if the first element of the first element is also a list (3D structure)
        if first_elem and isinstance(first_elem[0], list):
            # Return 3 for 3D: list of lists of lists
            return 3
        else:
            # Return 2 for 2D: list of lists
            return 2


def format_octave_struct_from_mappings(mappings, solver_opts_var='struct()'):
    """
    Creates nested Octave struct based only on the paths found in ScriptBody mappings.
    
    This function takes the mappings dictionary and builds an Octave structure
    string that represents the same hierarchical organization.
    
    Args:
        mappings: Dictionary of mappings from octave_sweep_mapping
                  Format: {1: 'simStruct.ModelVars.Common.Thermal.Twater = data{sim}{1}(1)', ...}
        solver_opts_var: The name of the SolverOpts variable
        
    Returns:
        A string with Octave struct syntax
    """
    # Create a set to store all unique paths from mappings
    paths = set()
    # Iterate through all mapping expressions
    for expr in mappings.values():
        # Extract the left side of the assignment (the path before the equals sign)
        path = expr.split('=')[0].strip()
        # Remove the 'simStruct.ModelVars.' prefix from the path
        if path.startswith('simStruct.ModelVars.'):
            path = path[len('simStruct.ModelVars.'):]
        # Add the cleaned path to the set of paths
        paths.add(path)
    
    # Build nested structure from the collected paths
    nested_struct = build_nested_struct_from_paths(paths)
    
    # Return the complete Octave struct assignment string
    return f"simStruct = struct('ModelVars', {nested_struct}, 'SolverOpts', {solver_opts_var});"


def build_nested_struct_from_paths(paths):
    """
    Recursively builds a nested struct string from a set of dot-separated paths.
    
    This function converts a set of dot-notation paths into a nested Octave struct
    representation.
    
    Example paths:
        'Common.Thermal.Twater'
        'Common.Control.Targets.Vout'
        'Common.Control.Targets.Pout'
        
    Returns:
        "struct('Common', struct('Thermal', struct('Twater', 0), 'Control', struct('Targets', struct('Vout', 0, 'Pout', 0))))"
    """
    # Initialize an empty dictionary to build the nested structure
    root = {}
    
    # Process each path in the set
    for path in paths:
        # Split the path by dots to get individual parts
        parts = path.split('.')
        # Start at the root of our nested dictionary
        current = root
        # Iterate through each part of the path
        for i, part in enumerate(parts):
            # Check if this is the last part (leaf node)
            if i == len(parts) - 1:
                # Check if the leaf node doesn't already exist
                if part not in current:
                    # Create leaf node with placeholder value 0
                    current[part] = 0
            else:
                # Check if intermediate node doesn't exist
                if part not in current:
                    # Create intermediate node as empty dictionary
                    current[part] = {}
                # Move deeper into the nested structure
                current = current[part]
    
    # Convert the nested dictionary to Octave struct syntax and return it
    return dict_to_struct(root)


def dict_to_struct(d):
    """
    Recursively converts a nested dictionary to Octave struct syntax.
    
    This function traverses a nested dictionary and generates the corresponding
    Octave struct creation code.
    
    Args:
        d: A nested dictionary representing the structure
        
    Returns:
        A string containing Octave struct creation code
    """
    # Initialize list to store key-value pairs for struct creation
    items = []
    # Iterate through all key-value pairs in the dictionary
    for key, value in d.items():
        # Check if the value is another dictionary (nested structure)
        if isinstance(value, dict):
            # Recursively convert nested dictionary to struct syntax
            nested = dict_to_struct(value)
            # Add the nested struct to items list
            items.append(f"'{key}', {nested}")
        else:
            # Leaf node - use placeholder value 0
            items.append(f"'{key}', 0")
    
    # Check if there are no items in the dictionary
    if not items:
        # Return empty struct for empty dictionary
        return 'struct()'
    
    # Return complete struct creation string with all items
    return f"struct({', '.join(items)})"


def octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict, scopes_list):
    """
    Generate Octave script for parameter sweep simulation.
    
    This function creates an Octave script that performs multiple simulations
    sweeping through parameter combinations defined in mapvars.
    
    Args:
        mapvars: Nested list of parameter values for sweep
        sweepnames: List of names for the swept parameters
        mappings: Dictionary of variable mappings for the simulation
        model_vars_dict: Dictionary of model variables
        scopes_list: List of scope names to capture simulation results
        
    Returns:
        String containing the complete Octave script
    """
    # Define the template file name
    template_file = r'octave_sweep_template.m.j2'
    print(os.getcwd())
    # Create Jinja2 environment with current directory as template loader
    env = Environment(loader=FileSystemLoader(os.getcwd()), trim_blocks=True, lstrip_blocks=True)
    # Load the specific template file
    template = env.get_template(template_file)
    
    # Filter out sweep names that start with "X" followed by digits (internal indices)
    filtered = [x for x in sweepnames if not (x.startswith("X") and x[1:].isdigit())]
    
    # Detect whether mapvars is 2D or 3D structure
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    # Generate the simStruct line from mappings
    simstruct_line = format_octave_struct_from_mappings(mappings)

    # Create the results folder path in the current working directory
    results_folder = os.path.join(os.getcwd(), 'simulation_results')

    # Create the directory if it doesn't exist (exist_ok=True prevents error if it exists)
    os.makedirs(results_folder, exist_ok=True)

    # Render the template with all the parameters and return the result
    return template.render(
        mapvars=mapvars,  # Pass the parameter values
        sweepnames=filtered,  # Pass filtered sweep names
        mappings=mappings,  # Pass variable mappings
        num_params=len(filtered),  # Pass number of parameters
        simstruct_line=simstruct_line,  # Pass simStruct initialization line
        mapvars_dim=mapvars_dim,  # Pass dimension information
        scopes=scopes_list,  # Pass list of scopes
        results_folder=results_folder  # Pass the results folder path
    )


def octave_sweep_mapping(file_path, mapvars):
    """
    Extract mappings from ScriptBody.py with support for both 2D and 3D mapvars.
    
    This function parses a Python script file to extract variable mappings
    for Octave simulation, handling both direct and derived parameters.
    
    Args:
        file_path: Path to the Python script file containing mappings
        mapvars: The mapvars structure to determine dimensions
        
    Returns:
        Dictionary of mappings with sequential keys preserving original order
    """
    import re  # Import regular expressions for pattern matching

    # Determine if mapvars is 2D or 3D
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    print('Detected mapvars dimension:', mapvars_dim)

    mappings = {}  # Initialize empty dictionary to store mapping results
    pattern = r"(mdlVars.*?=\s*.+"  # Pattern to match assignment lines (not used below, left from old code)

    # Open the script file containing variable mappings
    with open(file_path, 'r') as f:
        content = f.read()  # Read the entire file content as a single string

    # Define the section markers that delimit the area with user-editable code
    start_marker = "#! -------------------------------------------------------------------------------------Don't change above this line---------------------------------------------------------------------------"
    end_marker   = "#! -------------------------------------------------------------------------------------Don't change under this line---------------------------------------------------------------------------"

    # Create a regex to extract the content between the start and end markers
    section_pattern = start_marker + r"\s*(.*?)\s*" + end_marker
    section_match = re.search(section_pattern, content, re.DOTALL)  # DOTALL allows '.' to match newlines

    # Warn and return empty dictionary if the section was not found
    if not section_match:
        print("Warning: Could not find the section between comment markers")
        return {}

    # Extract the content of the section
    section_content = section_match.group(1)
    # Split the section content into individual lines
    lines = section_content.split('\n')
    # Counter to create sequential dictionary keys
    mapping_counter = 1

    # Process each line in the extracted section
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if not line or line.startswith('#') or '=' not in line:
            continue  # Skip empty lines, comments, or lines without assignment

        # Split the line into left-hand side (variable) and right-hand side (value/expression)
        left, right = line.split('=', 1)
        left = left.strip()   # Trim whitespace from LHS
        right = right.strip() # Trim whitespace from RHS

        # Match the left-hand side variable path starting with 'mdlVars'
        path_match = re.search(r"mdlVars(.*?)$", left)
        if not path_match:
            continue  # Skip if LHS does not contain mdlVars

        # Extract the variable path after 'mdlVars'
        path = path_match.group(1)
        full_path = 'mdlVars'  # Initialize full path starting with 'mdlVars'

        # Convert indexing like ['Common']['Thermal'] to dot notation
        for part in re.findall(r"\[['\"](.*?)['\"]\]", path):
            full_path += f'.{part}'

        # Convert Python-style 'mdlVars' path to Octave simStruct.ModelVars path
        if full_path.startswith('mdlVars.'):
            octave_path = 'simStruct.ModelVars.' + full_path[8:]  # Remove 'mdlVars.' prefix
        else:
            octave_path = 'simStruct.ModelVars.' + full_path  # Otherwise, prepend full prefix

        # ---------- Handle derived parameters containing other mdlVars references ----------
        if re.search(r"mdlVars(\[['\"].*?['\"]\])+", right):
            expr = right  # Store the right-hand side expression
            expr = expr.replace('**', '^')  # Convert Python exponent '**' to Octave '^'

            # ---------- Handle dp.mdlVars (external module reference) ----------
            if 'dp.mdlVars' in expr:
                def repl_dp(match):
                    # Extract the keys inside brackets, e.g., ['Common']['Thermal']
                    parts = re.findall(r"\[['\"](.*?)['\"]\]", match.group(0))
                    val = dp.mdlVars  # Start from the dp.mdlVars module
                    for p in parts:
                        val = val[p]  # Traverse nested dictionaries
                    return str(val)  # Return the actual value as string
                # Replace all dp.mdlVars[...] occurrences in the expression with actual values
                expr = re.sub(r"dp\.mdlVars(\[['\"].*?['\"]\])+", repl_dp, expr)

            # ---------- Handle mapVars references inside derived expression ----------
            mapvar_pattern = r"mapVars\[X(\d+)\](?:\[(\d+)\])?"
            all_matches = list(re.finditer(mapvar_pattern, expr))
            for match in all_matches:
                x_num = match.group(1)  # Which X variable
                idx1 = match.group(2)   # Optional index inside X
                # Replace with appropriate Octave data reference depending on mapvars dimension
                if mapvars_dim == 3:
                    replacement = f"data{{sim}}{{{x_num}}}({int(idx1)+1 if idx1 else 1})"
                else:
                    replacement = f"data(sim,{x_num})"
                # Build original string to replace
                original = f"mapVars[X{x_num}]" + (f"[{idx1}]" if idx1 else "")
                expr = expr.replace(original, replacement)  # Replace in expression

            # ---------- Handle other mdlVars references in derived expression ----------
            dep_pattern = r"mdlVars(\[['\"].*?['\"]\])+"  # Regex for remaining mdlVars
            def replace_dep(match):
                dep_path = match.group(0)
                dep_parts = re.findall(r"\[['\"](.*?)['\"]\]", dep_path)
                return 'simStruct.ModelVars.' + '.'.join(dep_parts)
            expr = re.sub(dep_pattern, replace_dep, expr)

            # Save the final mapping in the dictionary with sequential key
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            mapping_counter += 1

        # ---------- Handle simple mapVars assignments ----------
        else:
            mapvar_pattern = r"mapVars\[X(\d+)\](?:\[(\d+)\])?"
            all_matches = list(re.finditer(mapvar_pattern, right))
            if not all_matches:
                continue  # Skip if no mapVars found

            expr = right  # Start with RHS
            expr = expr.replace('**', '^')  # Convert Python exponent '**' to Octave '^'

            # Replace all mapVars references with Octave data access
            for match in all_matches:
                x_num = match.group(1)
                idx1 = match.group(2)
                if mapvars_dim == 3:
                    replacement = f"data{{sim}}{{{x_num}}}({int(idx1)+1 if idx1 else 1})"
                else:
                    replacement = f"data(sim,{x_num})"
                original = f"mapVars[X{x_num}]" + (f"[{idx1}]" if idx1 else "")
                expr = expr.replace(original, replacement)

            # Save mapping to dictionary
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            mapping_counter += 1

    return mappings  # Return the dictionary of mappings


# Main execution block - runs only if this script is executed directly
if __name__ == "__main__":
    # Define 3D input data for parameter sweep
    # Each outer list element represents a simulation case
    # Each middle list element represents a parameter group
    # Each inner list contains parameter values
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
    
    # Alternative 2D data structure (commented out)
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
    
    # Define names for the sweep parameters (for readability)
    sweepnames = ["Water Temperature", "Input Voltage", "Output Current"]
    
    # Extract mappings from ScriptBody.py file with dimension info
    # Note: Update the file path to match your system
    mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\this\1inject\ScriptBody.py', mapvars)
    # Print the extracted mappings for debugging
    print("Extracted mappings:", mappings)
    
    # Define model variables dictionary with initial values
    model_vars_dict = { 
        'Common': {'Water_Temperature': {'value': 20}, 'Input_Voltage': {'value': 200}, 'Output_Current': {'value': 100}},
        'DCDC_Rail1': {}
    }
    
    # Define list of scope names for simulation results
    scopes_list = ['Line-to-Line', 'Lines-to-Neutral', ' Lines-to-Chassis']  # Example scope names
    
    # Generate Octave code using the template
    octave_code = octave_sweep_script(mapvars, sweepnames, mappings, model_vars_dict, scopes_list)
    
    # Import datetime module for timestamp generation
    import datetime
    # Get current working directory for file saving
    folder_path = os.getcwd()
    
    # Save the generated Octave code to a file with timestamp
    # Generate UTC timestamp in format: YYYYMMDD_HHMMSS
    with open(f'{folder_path}/ScriptBody_{datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.m', 'w') as f: 
        # Write the Octave code to the file
        f.write(octave_code)
    
    # Print the generated Octave code to console
    print(octave_code)

    # Example usage of inject_octave_simple function
    # Inject the generated Octave script into a PLECS file
    # inject_octave_simple(
    #     # Source PLECS file path
    #     plecs_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
    #     # Output PLECS file path (same file in this case)
    #     output_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
    #     # Path to the generated .m file (update timestamp to match)
    #     m_file_path=r'D:\WORKSPACE\TESTMODEL\ScriptBody_20260312_213544.m'
    # )
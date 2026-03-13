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

def inject_octave_simple(plecs_file_path, output_file_path, m_file_path):
    """
    Reads Octave code from an .m file and injects it into the PLECS file.
    
    This function takes a PLECS file and injects Octave script code from a .m file
    into it, handling different cases of existing script sections.
    
    Args:
        plecs_file_path: Path to the source .plecs file
        output_file_path: Path to the output .plecs file
        m_file_path: Path to the .m file containing the Octave script
    """
    # Define the name of the script section in PLECS
    Script_name = "Script"
    
    # Open and read the PLECS file in read mode
    with open(plecs_file_path, 'r') as f: 
        # Read the entire content of the PLECS file into a string
        content = f.read()
    
    # Open and read the Octave .m file in read mode
    with open(m_file_path, 'r') as f:
        # Read the entire Octave script code into a string
        octave_code = f.read()
    
    # Escape special characters for PLECS script section format
    # Replace backslashes with double backslashes and double quotes with escaped double quotes
    escaped_code = octave_code.replace('\\', '\\\\').replace('"', '\\"')
    
    # Create the new script section in PLECS XML-like format
    new_script_section = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
  }}'''
    
    # CASE 1: Check for empty script section pattern
    # Pattern matches: Script { Name "Script" Script "" }
    empty_script_pattern = r'Script\s*{\s*Name\s+"Script"\s*Script\s+""\s*}'
    # Search for empty script pattern in the content (DOTALL flag makes . match newlines)
    if re.search(empty_script_pattern, content, re.DOTALL):
        # Replace the empty script section with the new populated script section
        new_content = re.sub(empty_script_pattern, new_script_section, content, flags=re.DOTALL)
        # Print confirmation message for case 1
        print("Case 1: Replaced empty script section")
    
    # CASE 2: Check for any existing script section (whether empty or not)
    elif re.search(r'Script\s*{.*?}', content, re.DOTALL):
        # Find all script sections in the content
        script_sections = list(re.finditer(r'Script\s*{.*?}', content, re.DOTALL))
        # Get the last script section found
        last_script = script_sections[-1]
        # Get the end position of the last script section
        insert_pos = last_script.end()
        # Insert new script section after the last existing script section
        new_content = content[:insert_pos] + '\n' + new_script_section + content[insert_pos:]
        # Print confirmation message for case 2
        print("Case 2: Appended after existing script section")
    
    # CASE 3: No script section found at all in the file
    else:
        # Find the position of the last closing brace in the file
        last_brace_pos = content.rfind('}')
        # Check if a closing brace was found
        if last_brace_pos != -1:
            # Insert new script section before the final closing brace
            new_content = content[:last_brace_pos] + '\n' + new_script_section + content[last_brace_pos:]
            # Print confirmation message for case 3 (insert before brace)
            print("Case 3: Inserted before final brace")
        else:
            # If no closing brace found, simply append the new script section at the end
            new_content = content + '\n' + new_script_section
            # Print confirmation message for case 3 (append at end)
            print("Case 3: Appended at end")
    
    # Write the modified content back to the output PLECS file
    with open(output_file_path, 'w') as f: 
        # Write the new content to the file
        f.write(new_content)
    
    # Print success message indicating the injection was completed
    print(f"✅ Injected {m_file_path} into {output_file_path}")


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
    template_file = 'octave_sweep_template.m.j2'
    
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
    # Import re module locally (though already imported globally)
    import re
    # Detect the dimensions of mapvars (2D or 3D)
    mapvars_dim = detect_mapvars_dimensions(mapvars)
    # Print the detected dimension for debugging
    print('Detected mapvars dimension:', mapvars_dim)
    # Initialize empty dictionary to store mappings in original order
    mappings = {}
    # Define pattern to match variable assignments containing "mdlVars"
    pattern = r"(mdlVars.*?=\s*.+)"
    
    # Open and read the Python script file
    with open(file_path, 'r') as f:
        # Read the entire file content
        content = f.read()
    
    # Define start marker for the relevant section
    start_marker = "#! -------------------------------------------------------------------------------------Don't change above this line---------------------------------------------------------------------------"
    # Define end marker for the relevant section
    end_marker = "#! -------------------------------------------------------------------------------------Don't change under this line---------------------------------------------------------------------------"

    # Create pattern to capture content between the markers
    section_pattern = start_marker + r"\s*(.*?)\s*" + end_marker
    # Search for the section between markers
    section_match = re.search(section_pattern, content, re.DOTALL)
    
    # Check if section was found
    if not section_match:
        # Print warning if section not found
        print("Warning: Could not find the section between comment markers")
        # Return empty dictionary
        return {}
    
    # Extract the content between the markers
    section_content = section_match.group(1)
    
    # Split the section content into individual lines
    lines = section_content.split('\n')
    # Initialize counter for mapping keys
    mapping_counter = 1
    
    # Process each line in the section
    for line in lines:
        # Remove leading/trailing whitespace
        line = line.strip()
        # Skip empty lines or comment lines
        if not line or line.startswith('#'):
            continue
            
        # Skip lines that don't contain an assignment operator
        if '=' not in line:
            continue
            
        # Split the line at the first equals sign
        left, right = line.split('=', 1)
        # Clean up left and right sides
        left = left.strip()
        right = right.strip()
        
        # Extract the path part after "mdlVars" from the left side
        path_match = re.search(r"mdlVars(.*?)$", left)
        # Skip if path pattern not found
        if not path_match:
            continue
            
        # Get the matched path part
        path = path_match.group(1)
        
        # Build the full path by processing each part in brackets
        full_path = 'mdlVars'
        # Find all quoted strings inside brackets
        for part in re.findall(r"\[['\"](.*?)['\"]\]", path):
            # Append each part to the path with dot notation
            full_path += f'.{part}'
        
        # Replace 'mdlVars.' prefix with 'simStruct.ModelVars.'
        if full_path.startswith('mdlVars.'):
            octave_path = 'simStruct.ModelVars.' + full_path[8:]
        else:
            octave_path = 'simStruct.ModelVars.' + full_path
        
        # Check if this is a derived parameter (uses other mdlVars references)
        if re.search(r"mdlVars(\[['\"].*?['\"]\])+", right):
            # This is a derived parameter
            expr = right
            
            # Replace Python exponentiation operator with Octave operator
            expr = expr.replace('**', '^')
            
            # Define pattern to find mdlVars references
            dep_pattern = r"mdlVars(\[['\"].*?['\"]\])+"
            # Define replacement function for each match
            def replace_dep(match):
                # Get the full matched string
                dep_path = match.group(0)
                # Extract all quoted parts from the path
                dep_parts = re.findall(r"\[['\"](.*?)['\"]\]", dep_path)
                # Convert to Octave struct notation and return
                return 'simStruct.ModelVars.' + '.'.join(dep_parts)
            
            # Replace all mdlVars references with simStruct.ModelVars references
            expr = re.sub(dep_pattern, replace_dep, expr)
            
            # Store the mapping with current counter value
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            # Increment the counter for next mapping
            mapping_counter += 1
            
        else:
            # This is a direct mapVars assignment (not derived)
            # Find all mapVars[Xn] occurrences with possible additional indexing
            mapvar_pattern = r"mapVars\[X(\d+)\](?:\[(\d+)\])?"
            
            # Find all matches of the pattern in the right side
            all_matches = list(re.finditer(mapvar_pattern, right))
            # Skip if no matches found
            if not all_matches:
                continue

            # Start with the original expression
            expr = right

            # Replace Python operators with Octave operators
            expr = expr.replace('**', '^')

            # Process each mapVar occurrence found
            for match in all_matches:
                # Extract the X number (parameter index)
                x_num = match.group(1)
                # Extract the optional element index (for 3D case)
                idx1 = match.group(2)
                
                # Handle 3D vs 2D mapvars differently
                if mapvars_dim == 3:
                    # For 3D mapvars: data{sim}{x_num}(element_idx)
                    if idx1 is not None:
                        # If element index exists, use it (convert from 0-based to 1-based)
                        element_idx = int(idx1) + 1
                        replacement = f"data{{sim}}{{{x_num}}}({element_idx})"
                    else:
                        # Default to first element if no index specified
                        replacement = f"data{{sim}}{{{x_num}}}(1)"
                else:
                    # For 2D mapvars: data(sim, x_num)
                    if idx1 is not None:
                        # For 2D, element index might be used but we simplify to matrix indexing
                        replacement = f"data(sim,{x_num})"
                    else:
                        # Default to matrix indexing
                        replacement = f"data(sim,{x_num})"
                
                # Reconstruct the original pattern to replace
                original = f"mapVars[X{x_num}]" + (f"[{idx1}]" if idx1 else "")
                # Replace the Python-style reference with Octave-style reference
                expr = expr.replace(original, replacement)

            # Store the mapping with current counter value
            mappings[mapping_counter] = f"{octave_path} = {expr}"
            # Increment the counter for next mapping
            mapping_counter += 1

    # Return the complete dictionary of mappings
    return mappings


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
    mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\ScriptBody.py', mapvars)
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
    inject_octave_simple(
        # Source PLECS file path
        plecs_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
        # Output PLECS file path (same file in this case)
        output_file_path=r'D:\WORKSPACE\TESTMODEL\ACfilterOBC.plecs',
        # Path to the generated .m file (update timestamp to match)
        m_file_path=r'D:\WORKSPACE\TESTMODEL\ScriptBody_20260312_213544.m'
    )
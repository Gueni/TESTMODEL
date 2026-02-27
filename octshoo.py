from jinja2 import Template
import re


def octave_sweep_script(mapvars, sweepnames, mappings):
    """
    Generate an Octave script for running simulations based on the provided sweep parameters and mappings.
    
    Args:
        mapvars     (list): A list of lists containing the sweep parameters for each simulation.
        sweepnames  (list): A list of names corresponding to each sweep parameter.
        mappings    (dict): A dictionary mapping X variables to their corresponding mdlVars paths in Octave.
    
    Returns:
                    str: The generated Octave script as a string.
    """    
    template = Template("""
    % Simulation Sweep Script 
    clear; clc;

    %% Sweep data
    data = [
            {% for row in mapvars %}    [{{ row | join(', ') }}];
            {% endfor %}
        ];

    fprintf('Running %d simulations...\\n\\n', size(data, 1));

    for sim = 1:size(data, 1)
    
        fprintf('Simulation %d of %d:\\n', sim, size(data, 1));
        
        % mdlVars = struct();
        
        {% for i in range(num_params) %}
    
        {{ mappings[i+1] }} = data(sim, {{ i+1 }});
    
        fprintf('  {{ sweepnames[i] }}: %g\\n', data(sim, {{ i+1 }}));
    
        {% endfor %}
        
        fprintf('\\n');
    end

    fprintf('Complete! Ran %d simulations\\n', size(data, 1));
                        
    """)
    
    return template.render(mapvars=mapvars,sweepnames=sweepnames,mappings=mappings,num_params=len(sweepnames))

def octave_sweep_mapping(file_path):
    """
    Extract mappings using a regex pattern.
    Args:        
                file_path (str) : The path to the ScriptBody.py file to extract mappings from.
    Returns:     
                dict            : A dictionary mapping X variables to their corresponding mdlVars paths in Octave.
    """
    mappings    = {}
    pattern     =r"mdlVars.*?=\s*mapVars\[X\d+\]"
    
    with open(file_path, 'r') as f: content = f.read()
    
    # Find all assignment lines matching the pattern
    matches     = re.finditer(pattern, content, re.MULTILINE)
    
    for match in matches:
        # Extract the full line of code
        line        = match.group()
        # Parse the matched line
        left, right = line.split('=', 1)
        # Extract the path from the left side (mdlVars assignment)
        path_match  = re.search(r"mdlVars(.*?)$", left.strip())

        if path_match:
            # Extract the path and the X variable from the right side
            path    = path_match.group(1).strip()
            right   = right.strip()
            x_match = re.search(r"mapVars\[(X\d+)\](\[\d+\])?", right)
            
            if x_match:
                # Extract the X variable and any indexing
                x_var       = x_match.group(1)
                index       = x_match.group(2) or ''
                octave_path = 'mdlVars'
                
                # Convert the path to Octave syntax
                for part in re.findall(r"\[['\"](.*?)['\"]\]", path): octave_path += f'.{part}'
                
                # Handle any indexing in the X variable (e.g., X1[0] -> X1(1) in Octave)
                if index:
                    idx         = re.search(r'\[(\d+)\]', index).group(1)
                    octave_path += f'({int(idx)+1})'

                # Extract the numeric part of the X variable (e.g., X1 -> 1)
                x_num           = int(x_var[1:])
                mappings[x_num] = octave_path
    
    return mappings


# Your input
mapvars = [
    [20, 200, 5],
    [20, 200, 10],
    [20, 300, 5],
    [20, 300, 10],
    [25, 200, 5],
    [25, 200, 10],
    [25, 300, 5],
    [25, 300, 10],
    [30, 200, 5],
    [30, 200, 10],
    [30, 300, 5],
    [30, 300, 10]
]

sweepnames = ["Water Temperature", "Input Voltage", "Output Current"]
mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\ScriptBody.py')

code = octave_sweep_script(mapvars, sweepnames, mappings)
print(code)
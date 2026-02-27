from jinja2 import Template
import re



# Even simpler - just write the code directly without escaping newlines
def inject_octave_simple(plecs_file_path, output_file_path, octave_code):
    """
    Simplest version - write code directly without newline escaping.
    """
    Script_name = "Script"
    with open(plecs_file_path, 'r') as f:
        content = f.read()
    
    # Only escape quotes, keep newlines as is
    escaped_code = octave_code.replace('"', '\\"')
    
    new_script_section = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
  }}'''
    
    # Simple string replacement
    script_pattern = 'Script {\n    Name          "Script"\n    Script        ""\n  }'
    if script_pattern in content:
        new_content = content.replace(script_pattern, new_script_section)
    else:
        # Insert before end
        end_pattern = '}\nDemoSignature'
        if end_pattern in content:
            new_content = content.replace(end_pattern, new_script_section + '\n}' + '\nDemoSignature')
        else:
            new_content = content + '\n' + new_script_section
    
    with open(output_file_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Octave code injected into {output_file_path}")

# Your existing code for generating Octave script
from jinja2 import Template

def octave_sweep_script(mapvars, sweepnames, mappings):
    """
    Generate an Octave script for running simulations based on the provided sweep parameters and mappings.
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
    
    return template.render(mapvars=mapvars, sweepnames=sweepnames, 
                          mappings=mappings, num_params=len(sweepnames))

def octave_sweep_mapping(file_path):
    """
    Extract mappings using a regex pattern.
    """
    mappings = {}
    pattern = r"mdlVars.*?=\s*mapVars\[X\d+\]"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    matches = re.finditer(pattern, content, re.MULTILINE)
    
    for match in matches:
        line = match.group()
        left, right = line.split('=', 1)
        path_match = re.search(r"mdlVars(.*?)$", left.strip())
        
        if path_match:
            path = path_match.group(1).strip()
            right = right.strip()
            x_match = re.search(r"mapVars\[(X\d+)\](\[\d+\])?", right)
            
            if x_match:
                x_var = x_match.group(1)
                index = x_match.group(2) or ''
                octave_path = 'mdlVars'
                
                for part in re.findall(r"\[['\"](.*?)['\"]\]", path):
                    octave_path += f'.{part}'
                
                if index:
                    idx = re.search(r'\[(\d+)\]', index).group(1)
                    octave_path += f'({int(idx)+1})'
                
                x_num = int(x_var[1:])
                mappings[x_num] = octave_path
    
    return mappings

# Main execution
if __name__ == "__main__":
    # Your input data
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
    
    # Extract mappings from ScriptBody.py
    mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\ScriptBody.py')
    print("Extracted mappings:", mappings)
    
    # Generate Octave code
    octave_code = octave_sweep_script(mapvars, sweepnames, mappings)
    print("\nGenerated Octave code:")
    print("-" * 50)
    print(octave_code)
    
    # Inject into PLECS file
    inject_octave_simple(
        plecs_file_path=r'D:\WORKSPACE\TESTMODEL\test.plecs',  # Change this
        output_file_path=r'D:\WORKSPACE\TESTMODEL\modified_plecs_file.plecs',  # Change this
        octave_code=octave_code
    )
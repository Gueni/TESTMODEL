import re
from jinja2 import Environment, FileSystemLoader
import os

def inject_octave_simple(plecs_file_path, output_file_path, octave_code):

    Script_name         = "Script"
    
    with open(plecs_file_path, 'r') as f: content = f.read()
    
    escaped_code        = octave_code.replace('"', '\\"')
    
    # Create the new script section
    new_script_section = f'''  Script {{
    Name          "{Script_name}"
    Script        "{escaped_code}"
    }}'''
    
    # CASE 1: Check for empty script section
    empty_script_pattern = r'Script\s*{\s*Name\s+"Script"\s*Script\s+""\s*}'
    if re.search(empty_script_pattern, content, re.DOTALL):
        # Replace empty script section
        new_content = re.sub(empty_script_pattern, new_script_section, content, flags=re.DOTALL)
    
    # CASE 2: Check for any script section (empty or not)
    elif re.search(r'Script\s*{.*?}', content, re.DOTALL):
        # Find all script sections and get the last one
        script_sections = list(re.finditer(r'Script\s*{.*?}', content, re.DOTALL))
        last_script = script_sections[-1]
        
        # Insert after the last script section
        insert_pos = last_script.end()
        new_content = content[:insert_pos] + '\n' + new_script_section + content[insert_pos:]
    
    # CASE 3: No script section at all
    else:
        # Find the last closing brace before DemoSignature
        # The file typically ends with "}\nDemoSignature"
        last_brace_pos = content.rfind('}')
        
        if last_brace_pos != -1:
            # Insert before the last closing brace
            new_content = content[:last_brace_pos] + '\n' + new_script_section + content[last_brace_pos:]
        else:
            # Fallback: if no brace found, just append
            new_content = content + '\n' + new_script_section
    
    # Write the modified content
    with open(output_file_path, 'w') as f: f.write(new_content)

def octave_sweep_script(mapvars, sweepnames, mappings):


    template_file='octave_sweep_template.m.j2'
    # Create Jinja2 environment
    env = Environment(loader=FileSystemLoader(os.getcwd()),trim_blocks=True,lstrip_blocks=True)
    
    # Load template
    template = env.get_template(template_file)
    
    # Render template
    return template.render(mapvars=mapvars,sweepnames=sweepnames,mappings=mappings,num_params=len(sweepnames))

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
    print(octave_code)
    
    # Inject into PLECS file
    inject_octave_simple(
        plecs_file_path=r'D:\WORKSPACE\TESTMODEL\test.plecs',  # Change this
        output_file_path=r'D:\WORKSPACE\TESTMODEL\modified_plecs_file.plecs',  # Change this
        octave_code=octave_code
    )
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
    import re

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
        octave_path = 'mdlVars'
        for part in re.findall(r"\[['\"](.*?)['\"]\]", path):
            octave_path += f'.{part}'

        # Find all mapVars[Xn] occurrences
        x_vars = re.findall(r"mapVars\[X(\d+)\]", right)
        if not x_vars:
            continue

        expr = right.strip()

        # Replace Python operators with Octave operators
        expr = expr.replace('**', '^')   # exponentiation
        # You can also handle element-wise if needed:
        # expr = expr.replace('*', '.*').replace('/', './') 

        # Replace mapVars[Xn] with data(sim,n)
        for x in x_vars:
            expr = expr.replace(f"mapVars[X{x}]", f"data(sim,{x})")

        # Store mapping with dependency info
        mappings[octave_path] = {"expr": f"{octave_path} = {expr.strip()}", 
                                 "deps": [int(x) for x in x_vars]}

    # Dependency-aware ordering: sort by max Xi in RHS
    ordered_mappings = dict(sorted(mappings.items(), key=lambda kv: max(kv[1]["deps"])))

    # Return only the expression string for template
    return {i+1: v["expr"] for i,(k,v) in enumerate(ordered_mappings.items())}

# Main execution
if __name__ == "__main__":
    # Your input data
    mapvars = [
        [20, 200, 5, 100],
        [20, 200, 10, 200],
        [20, 300, 5, 150],
        [20, 300, 10, 250],
        [25, 200, 5, 120],
        [25, 200, 10, 220],
        [25, 300, 5, 180],
        [25, 300, 10, 280],
        [30, 200, 5, 140],
        [30, 200, 10, 240],
        [30, 300, 5, 190],
        [30, 300, 10, 290]
    ]
    
    sweepnames = ["Water Temperature", "Input Voltage", "Output Current"]
    
    # Extract mappings from ScriptBody.py
    mappings = octave_sweep_mapping(r'D:\WORKSPACE\TESTMODEL\ScriptBody.py')
    print("Extracted mappings:", mappings)
    
    # Generate Octave code
    octave_code = octave_sweep_script(mapvars, sweepnames, mappings)
    print(octave_code)
    
    # # Inject into PLECS file
    # inject_octave_simple(
    #     plecs_file_path=r'D:\WORKSPACE\TESTMODEL\test.plecs',  # Change this
    #     output_file_path=r'D:\WORKSPACE\TESTMODEL\modified_plecs_file.plecs',  # Change this
    #     octave_code=octave_code
    # )
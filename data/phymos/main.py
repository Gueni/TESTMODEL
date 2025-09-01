import plotly.graph_objects as go
from plotly.offline import plot
from collections import OrderedDict
import json

class YourClass:
    def __init__(self):
        self.image = ""
    
    def base64_img(self):
        """
        Read a text file containing a base64 encoded image and store it as a string in the `image` attribute of the object.
        """
        # Read base64 image from text file and store in self.image
        with open(r"D:\WORKSPACE\BJT-MODEL\data\assets\BMW_Base64_Logo.txt", 'r') as fin:
            lines = fin.readlines()
        
        # Reset image and concatenate all lines
        self.image = ""
        for line in lines:
            self.image += line.strip()  # Remove any extra whitespace/newlines










def generate_complete_html(nested_dict, base64_image="", output_file='parameter_table.html', 
                         simulation_id="SIM_001", utc_time="2024-01-15 14:30:45", simulation_name="Default_Simulation"):
    """
    Generate a complete standalone HTML file with global header and BMW-style design
    """
    # Convert the nested dict to JSON for JavaScript usage
    dict_json = json.dumps(nested_dict)
    
    # Create initial table (showing all)
    parameters, values = [], []
    for category, subdict in nested_dict.items():
        parameters.append(f"<b>{category.upper()}</b>")
        values.append("")  # Empty value for category header
        
        for param, value in subdict.items():
            parameters.append(f"&nbsp;&nbsp;{param}")
            values.append(str(value))
    
    # Create global header with text on left and image on right (white background with border)
    global_header = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 25px; background: white; border: 2px solid #e0e0e0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="text-align: left; flex: 1;">
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>Simulation ID:</strong> {simulation_id}</div>
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>UTC:</strong> {utc_time}</div>
        </div>
        
        <div style="text-align: center; flex: 1;">
            <h1 style="margin: 0; font-size: 28px; color: #2c3e50; font-weight: bold;">{simulation_name}</h1>
        </div>
        
        <div style="text-align: right; flex: 1;">
            <img src="data:image/png;base64,{base64_image}" alt="Logo" style="max-width: 500px; height: auto; margin-left: 20px;">
        </div>
    </div>
    """ if base64_image else f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 25px; background: white; border: 2px solid #e0e0e0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="text-align: left; flex: 1;">
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>Simulation ID:</strong> {simulation_id}</div>
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>UTC:</strong> {utc_time}</div>
            <div style="font-size: 16px; color: #2c3e50;"><strong>Simulation Name:</strong> {simulation_name}</div>
        </div>
        
        <div style="text-align: center; flex: 1;">
            <h1 style="margin: 0; font-size: 28px; color: #2c3e50; font-weight: bold;">Configuration Parameters Dashboard</h1>
        </div>
        
        <div style="text-align: right; flex: 1;">
            <!-- Empty space for alignment when no image -->
        </div>
    </div>
    """
    
    # Create the HTML content
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Configuration Parameters Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .table-section {{
            margin-top: 40px;
            padding: 25px;
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
        }}
        .controls {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 25px;
            padding: 12px;
            background: #0066b3; /* BMW Blue */
            border-radius: 8px;
            color: white;
        }}
        .dropdown {{
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            background: white;
            color: #333;
            font-size: 13px;
            min-width: 180px;
            cursor: pointer;
            height: 35px;
        }}
        .dropdown-label {{
            font-size: 14px;
            font-weight: normal;
        }}
        .table-container {{
            margin-top: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .instructions {{
            text-align: center;
            color: #7f8c8d;
            margin-top: 15px;
            font-style: italic;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {global_header}
        
        <div class="table-section">
            <div class="controls">
                <label for="categorySelect" class="dropdown-label"><strong>Select Category:</strong></label>
                <select id="categorySelect" class="dropdown" onchange="updateTable()">
                    <option value="all">All Categories</option>
                    <option value="system">System</option>
                    <option value="network">Network</option>
                    <option value="database">Database</option>
                    <option value="logging">Logging</option>
                    <option value="security">Security</option>
                </select>
            </div>

            <div id="tableContainer" class="table-container">
                <div id="parameterTable"></div>
            </div>
            
            <div class="instructions">
                <p>Select a category from the dropdown to filter the parameters</p>
            </div>
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #7f8c8d; font-style: italic;">
            <p>Additional tables and sections can be added here...</p>
        </div>
    </div>

    <script>
        // Store the data
        const parameterData = {dict_json};
        
        // Function to update the table based on selected category
        function updateTable() {{
            const select = document.getElementById('categorySelect');
            const selectedCategory = select.value;
            
            let parameters = [];
            let values = [];
            
            if (selectedCategory === 'all') {{
                // Show all categories
                for (const [category, subdict] of Object.entries(parameterData)) {{
                    parameters.push(`<b>${{category.toUpperCase()}}</b>`);
                    values.push("");
                    
                    for (const [param, value] of Object.entries(subdict)) {{
                        parameters.push(`&nbsp;&nbsp;${{param}}`);
                        values.push(String(value));
                    }}
                }}
            }} else {{
                // Show specific category
                const subdict = parameterData[selectedCategory];
                for (const [param, value] of Object.entries(subdict)) {{
                    parameters.push(param);
                    values.push(String(value));
                }}
            }}
            
            // Create or update the table
            const tableData = [{{
                type: 'table',
                header: {{
                    values: ['<b>Parameter</b>', '<b>Value</b>'],
                    align: 'left',
                    fill: {{color: '#0066b3'}}, /* BMW Blue for header */
                    font: {{color: 'white', size: 14, family: 'Arial'}},
                    height: 40
                }},
                cells: {{
                    values: [parameters, values],
                    align: 'left',
                    fill: {{color: ['#f8f9fa', 'white']}},
                    font: {{size: 13, family: 'Arial'}},
                    height: 30
                }}
            }}];
            
            const layout = {{
                margin: {{l: 20, r: 20, t: 10, b: 20}},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            }};
            
            Plotly.newPlot('parameterTable', tableData, layout, {{displayModeBar: false}});
        }}
        
        // Initialize the table on page load
        document.addEventListener('DOMContentLoaded', function() {{
            updateTable();
        }});
    </script>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

def create_nested_ordered_dict():
    return OrderedDict([
        ('system', OrderedDict([
            ('version', '1.2.3'),
            ('build_date', '2023-12-01'),
            ('status', 'active'),
            ('mode', 'production')
        ])),
        ('network', OrderedDict([
            ('ip_address', '192.168.1.100'),
            ('subnet_mask', '255.255.255.0'),
            ('gateway', '192.168.1.1'),
            ('dns', '8.8.8.8'),
            ('port', '8080')
        ])),
        ('database', OrderedDict([
            ('host', 'localhost'),
            ('port', '5432'),
            ('user', 'admin'),
            ('password', 'encrypted123'),
            ('max_connections', '100'),
            ('timeout', '30s')
        ])),
        ('logging', OrderedDict([
            ('level', 'INFO'),
            ('file_path', '/var/log/app.log'),
            ('max_size', '10MB'),
            ('retention_days', '30')
        ])),
        ('security', OrderedDict([
            ('ssl_enabled', 'true'),
            ('certificate_path', '/etc/ssl/cert.pem'),
            ('key_path', '/etc/ssl/key.pem'),
            ('auth_timeout', '300s')
        ]))
    ])

if __name__ == "__main__":
    # Create instance and load base64 image
    obj = YourClass()
    obj.base64_img()
    
    nested_odict = create_nested_ordered_dict()
    generate_complete_html(nested_odict, obj.image, 'interactive_parameter_table.html')
    
    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5],
        y=[10, 11, 12, 13, 14],
        mode='lines+markers',
        name='Sample Data'
    ))
    fig.update_layout(
        title='Sample Plotly Chart',
        xaxis_title='X Axis',
        yaxis_title='Y Axis'
    )
    
    # Convert the figure to HTML div
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    
    # Read the existing HTML file
    with open('interactive_parameter_table.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find where to insert the plot (before the closing body tag)
    insert_position = html_content.find('</body>')
    
    # Create the plot section HTML
    plot_section = f"""
    <div style="margin: 40px auto; padding: 25px; background: white; border: 2px solid #e0e0e0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #2c3e50;">Simulation Results</h2>
        {plot_div}
    </div>
    """
    
    # Insert the plot section
    updated_html = html_content[:insert_position] + plot_section + html_content[insert_position:]
    
    # Write the updated HTML back to the file
    with open('interactive_parameter_table.html', 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"Plot added to interactive_parameter_table.html")
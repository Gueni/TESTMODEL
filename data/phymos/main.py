import plotly.graph_objects as go
from plotly.offline import plot
from collections import OrderedDict
import json

def append_to_html(nested_dict, output_file='parameter_table.html'):
    """
    Append an interactive parameter table to an existing HTML file
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
    
    # Create the HTML content to append
    html_content = f"""
<!-- BEGIN APPENDED PARAMETER TABLE -->
<div class="container">
    <div class="header">
        <h1>🔧 Configuration Parameters Dashboard</h1>
        <p>Interactive table with category filtering</p>
    </div>
    
    <div class="controls">
        <label for="categorySelect"><strong>Select Category:</strong></label>
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
                fill: {{color: '#2c3e50'}},
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
<!-- END APPENDED PARAMETER TABLE -->
"""
    
    # Check if file exists and read current content
    existing_content = ""
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    except FileNotFoundError:
        # If file doesn't exist, we'll create it with the full HTML structure
        pass 
    else:
        # If file exists, append our content before the closing body tag
        if '</body>' in existing_content:
            html_content = existing_content.replace('</body>', html_content + '\n</body>')
        else:
            # If no body tag found, just append to the end
            html_content = existing_content + html_content
    
    # Write to HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Parameter table appended to: {output_file}")
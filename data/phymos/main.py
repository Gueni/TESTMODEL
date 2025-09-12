from matplotlib.pyplot import margins
import plotly.graph_objects as go
from plotly.offline import plot
from collections import OrderedDict
import json

class YourClass:
    def __init__(self):
        self.image = ""

    def base64_img(self):
        """
        Read a text file containing a base64 encoded image and store it as a string in the `image` attribute.
        """
        with open(r"D:\WORKSPACE\BJT-MODEL\data\assets\BMW_Base64_Logo.txt", 'r') as fin:
            self.image = "".join(line.strip() for line in fin.readlines())


def flatten_dict(d, parent_key="", sep="."):
    """
    Recursively flatten a nested dictionary.

    Example:
        {"a": {"b": 1, "c": {"d": 2}}}
        -> {"a.b": 1, "a.c.d": 2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def generate_complete_html(nested_dict, base64_image="", output_file='parameter_table.html',
                         simulation_id="SIM_001", utc_time="2024-01-15 14:30:45", simulation_name="Default_Simulation"):
    """
    Generate a complete standalone HTML file with global header and BMW-style design.
    Works for arbitrarily nested dictionaries.
    """
    dict_json = json.dumps(nested_dict)  # Full nested dict
    top_categories = list(nested_dict.keys())  # Only top-level keys for dropdown

    dropdown_options = "\n".join([f'<option value="{cat}">{cat}</option>' for cat in top_categories])

    # Header section
    global_header = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; padding: 25px; background: white; border: 2px solid #e0e0e0; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <div style="text-align: left; flex: 1;">
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>Simulation   :</strong> {simulation_name}</div>
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>Date & Time  :</strong> {utc_time}</div>
            <div style="font-size: 16px; margin-bottom: 8px; color: #2c3e50;"><strong>Simulation ID:</strong> {simulation_id}</div>
        </div>
        <div style="text-align: right; flex: 1;">
            <img src="data:image/png;base64,{base64_image}" alt="Logo" style="max-width: 700px; height: auto; margin-left: 20px;">
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
        <div style="text-align: right; flex: 1;"></div>
    </div>
    """

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
        .controls {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 0px;
            padding: 12px;
            background: #0066b3;
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

    </style>
</head>
<body>
    <div class="container">
        {global_header}

        <div class="controls">
            <label for="categorySelect"><strong>Simulation Model Configuration & Parameters:</strong></label>
            <select id="categorySelect" class="dropdown" onchange="updateTable()">
                <option value="all">All Categories</option>
                {dropdown_options}
            </select>
        </div>

        <div id="parameterTable"></div>
    </div>

    <script>
        const parameterData = {dict_json};

        function flatten(obj, parentKey = '') {{
            let items = {{}};
            for (let [k, v] of Object.entries(obj)) {{
                const newKey = parentKey ? parentKey + '.' + k : k;
                if (typeof v === 'object' && v !== null) {{
                    Object.assign(items, flatten(v, newKey));
                }} else {{
                    items[newKey] = v;
                }}
            }}
            return items;
        }}

        function updateTable() {{
            const select = document.getElementById('categorySelect');
            const selectedCategory = select.value;
     


            let parameters = [];
            let values = [];

            if (selectedCategory === 'all') {{
                for (const [category, subdict] of Object.entries(parameterData)) {{
                    const flat = flatten(subdict, category);
                    for (const [param, value] of Object.entries(flat)) {{
                        parameters.push(param);
                        values.push(String(value));
                    }}
                }}
            }} else {{
                const subdict = parameterData[selectedCategory];
                const flat = flatten(subdict, selectedCategory);
                for (const [param, value] of Object.entries(flat)) {{
                    parameters.push(param);
                    values.push(String(value));
                }}
            }}

            const tableData = [{{
                type: 'table',
                header: {{
                    values: ['<b>Parameter</b>', '<b>Value</b>'],
                    align: 'left',
                    fill: {{color: '#0066b3'}},
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


            Plotly.newPlot('parameterTable', tableData, {{displayModeBar: false}});
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            updateTable();
        }});
    </script>
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)


def example_nested_dict():
    return OrderedDict([
        ('system', OrderedDict([
            ('version', '1.2.3'),
            ('build_date', '2023-12-01'),
            ('nested', OrderedDict([
                ('subkey1', 'value1'),
                ('subkey2', OrderedDict([
                    ('deep_param', '42'),
                    ('another', 'test')
                ]))
            ]))
        ])),
        ('network', OrderedDict([
            ('ip_address', '192.168.1.100'),
            ('advanced', OrderedDict([
                ('routes', ['route1', 'route2']),
                ('dns_servers', ['8.8.8.8', '1.1.1.1'])
            ]))
        ]))
    ])


if __name__ == "__main__":
    obj = YourClass()
    obj.base64_img()

    nested_odict = example_nested_dict()
    generate_complete_html(nested_odict, obj.image, 'interactive_parameter_table.html')

    print("✅ HTML file created: interactive_parameter_table.html")

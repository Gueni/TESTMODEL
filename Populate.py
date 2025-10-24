import plotly.graph_objects as go
from datetime import datetime

def create_parameter_table(data_dict, title=""):
    
    def flatten_dict_with_brackets(d, parent_keys=None):
        """Flatten a nested dictionary using bracket notation"""
        if parent_keys is None:
            parent_keys = []
        
        items = []
        for k, v in d.items():
            current_keys = parent_keys + [k]
            if isinstance(v, dict):
                items.extend(flatten_dict_with_brackets(v, current_keys))
            else:
                # Create bracket notation: ["key1"]["key2"]["key3"]
                bracket_path = ''.join([f'["{key}"]' for key in current_keys])
                items.append((bracket_path, v))
        return items
    
    def get_level_one_paths(d):
        """Get only the top-level dictionary paths"""
        paths = ["all"]
        for key, value in d.items():
            if isinstance(value, dict):
                paths.append(key)
        return paths
    
    # Get only level-one dictionary paths for dropdown
    available_paths = get_level_one_paths(data_dict)
    # Create initial table data (show all by default)
    flattened_items = flatten_dict_with_brackets(data_dict)
    parameters = [item[0] for item in flattened_items]
    values = [str(item[1]) for item in flattened_items]
    
    # Create the table with clear separation
    table = go.Table(
        header=dict(
            values=['<b>Parameters</b>', '<b>Values</b>'],
            fill_color="#0066b1",
            align='center',
            font=dict(size=14, color='white'),
            height=28
        ),
        cells=dict(
            values=[parameters, values],
            fill=dict(color=['#F7F7F7', 'white']),
            align='center',
            font=dict(size=12),
            height=28
        ),
        domain=dict(x=[0, 1], y=[0, 0.9])  # Table occupies bottom 80%
    )
    
    # Create dropdown buttons
    dropdown_buttons = []
    
    for path in available_paths:
        if path == "all":
            # Show all parameters
            flattened_items = flatten_dict_with_brackets(data_dict)
            params = [item[0] for item in flattened_items]
            vals = [str(item[1]) for item in flattened_items]
        else:
            # Get specific level-one sub-dictionary
            sub_dict = data_dict.get(path, {})
            if isinstance(sub_dict, dict):
                flattened_items = flatten_dict_with_brackets(sub_dict, [path])
                params = [item[0] for item in flattened_items]
                vals = [str(item[1]) for item in flattened_items]
            else:
                # If it's not a dict, show it as a single parameter
                params = [f'["{path}"]']
                vals = [str(sub_dict)]
        
        dropdown_buttons.append(
            dict(
                label=path,
                method="update",
                args=[
                    {
                        "cells": {
                            "values": [params, vals]
                        }
                    }
                ]
            )
        )
    
    fig = go.Figure(data=[table])
    
    # Layout with clear section separation
    fig.update_layout(
        height=500,
        margin=dict(t=0, l=10, r=10, b=30),
        plot_bgcolor='white',
        paper_bgcolor='white',
   
        annotations=[
            # Main title
            dict(
                text=f"{title}",
                x=0.0,
                y=0.95,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="middle",
                showarrow=False,
                font=dict(size=20, color="darkslategray"),
                align="left"
            ),
           
        ],
        updatemenus=[
            dict(
                buttons=dropdown_buttons,
                direction="down",
                showactive=True,
                x=0.75,
                xanchor="left",
                y=0.95,
                yanchor="middle",
                bgcolor="white",
                bordercolor="#2E86AB",
                borderwidth=1,
                font=dict(size=12),
                active=0
            )
        ]
    )
    
    return fig

# Updated populate_html_template function
def populate_html_template(template_path, output_path, script_name, date_time, simulation_id, 
                         logo_file_path=None, plot_items="", parameters_dict=None):
    
    with open(template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Replace the variables
    html_content = html_content.replace("{{TITLE}}", ":  "+"Simulation Report")
    html_content = html_content.replace("{{SCRIPT_NAME}}", ":  "+script_name)
    html_content = html_content.replace("{{DATE_TIME}}", ":  "+date_time)
    html_content = html_content.replace("{{SIMULATION_ID}}", ":  "+simulation_id)
    
    # Handle logo from file
    if logo_file_path:
        with open(logo_file_path, 'r', encoding='utf-8') as logo_file:
            logo_base64 = logo_file.read().strip()
        html_content = html_content.replace("{{LOGO_BASE64}}", logo_base64)
    
    # Add parameters table if provided
    if parameters_dict:
        # Use the first version with level-one dropdown only
        param_table = create_parameter_table(parameters_dict, "Simulation Model Configurations & Parameters:")
        # Convert Plotly figure to HTML
        param_table_html = param_table.to_html(include_plotlyjs='cdn', div_id="parameters-table")
        plot_items = param_table_html + param_table_html + plot_items
    
    # Replace plot items
    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
    
    # Write the populated HTML
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Example usage
if __name__ == "__main__":
    # Your variables
    script_name = "standalone_cs555555555555555555555555555555555555v.py"
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    simulation_id = "1759764207"
    
    # Sample parameters dictionary
    sample_parameters = {
        "performance": {
            "metrics": {
                "accuracy": {
                    "value": 0.95,
                    "threshold": 0.85
                },
                "precision": {
                    "value": 0.92,
                    "threshold": 0.80
                }
            },
            "training": {
                "epochs": 100,
                "batch_size": 32
            }
        },
        "model": {
            "architecture": "CNN",
            "layers": 5,
            "parameters": 1000000
        },
        "data": {
            "samples": 50000,
            "features": 784,
            "split": {
                "train": 0.7,
                "validation": 0.2,
                "test": 0.1
            }
        },"datddd": {
            "samples": 50000,
            "features": 784,
            "split": {
                "train": 0.7,
                "validation": 0.2,
                "test": 0.1
            },
            "extra": {
                "info1": "value1",
                "info2": "value2"
            },
            "more_data": {
                "sub_data1": {
                    "detailA": 123,
                    "detailB": 456
                },
                "sub_data2": {
                    "detailC": 789,
                    "detailD": 101
                }
            },
            "additional": {
                "part1": {
                    "segmentA": {
                        "itemX": "foo",
                        "itemY": "bar"
                    },
                    "segmentB": {
                        "itemZ": "baz"
                    }
                },
                "part2": {
                    "segmentC": {
                        "itemW": "qux"
                    }
                }   
            },
            "final_section": {
                "element1": {
                    "sub_elementA": {
                        "detailX": 111,
                        "detailY": 222
                    }
                },
                "element2": {
                    "sub_elementB": {
                        "detailZ": 333
                    }
                }
            }   ,
            "ultimate": {
                "layer1": {
                    "componentA": {
                        "feature1": "alpha",
                        "feature2": "beta"
                    }
                },
                "layer2": {
                    "componentB": {
                        "feature3": "gamma"
                    }
                }
            }
        }
    }
    
    # Path to your logo file
    logo_file_path = r"D:\WORKSPACE\TESTMODEL\BMW_Base64_Logo.txt"
    
    # Populate the template with parameters table
    populate_html_template(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path="simulation_report.html",
        script_name=script_name,
        date_time=date_time,
        simulation_id=simulation_id,
        logo_file_path=logo_file_path,
        parameters_dict=sample_parameters
    )
    
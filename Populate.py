import re
import plotly.graph_objects as go
from datetime import datetime


def remove_div(html_content):
    """
    Remove specific sections from HTML content
    
    Args:
        html_content (str): The HTML content
    
    Returns:
        str: HTML content with sections removed
    """
    # Remove table container, note section, multiplot container, constants container, and download section
    html_content = re.sub(r'<div class="table-container">\s*</div>', '', html_content)
    html_content = re.sub(r'<!-- Note Section -->\s*<div class="note-section">[\s\S]*?{{NOTE_TEXT}}[\s\S]*?</div>', '', html_content)
    html_content = re.sub(r'<!-- multiplot Container -->\s*<div class="multiplot-container">[\s\S]*?{{multiplot_ITEMS_TABLE}}[\s\S]*?</div>', '', html_content)
    html_content = re.sub(r'<!-- constants Container -->\s*<div class="constants-container">[\s\S]*?{{constants_ITEMS_TABLE}}[\s\S]*?</div>', '', html_content)
    html_content = re.sub(r'<div class="download_section">[\s\S]*?</div>\s*<script src="scripts.js"></script>', '', html_content)
    
    return html_content



def create_parameter_table(data_dict, title="", dropdown_level=1):
    """
    Create a parameter table with dropdown menu at specified level
    
    Args:
        data_dict: Nested dictionary of parameters
        title: Table title
        dropdown_level: Level at which to create dropdown options (1 = top level, 2 = second level, etc.)
    """
    
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
    
    def get_paths_at_level(d, current_level=1, target_level=1, current_path=None):
        """Get dictionary paths at specified level"""
        if current_path is None:
            current_path = []
            
        paths = []
        
        # If we've reached the target level, return current path as an option
        if current_level == target_level:
            if current_path:  # Only add if we have a path
                path_str = "->".join(current_path)
                paths.append(("->".join(current_path), current_path.copy()))
        else:
            # If we haven't reached target level yet, continue traversing
            for key, value in d.items():
                if isinstance(value, dict):
                    new_path = current_path + [key]
                    paths.extend(get_paths_at_level(value, current_level + 1, target_level, new_path))
        
        # Always include "all" option at any level
        if current_level == 1:
            paths.insert(0, ("all", []))
            
        return paths
    
    def get_subdict_by_path(d, path_keys):
        """Get sub-dictionary by path keys"""
        if not path_keys:
            return d
            
        current = d
        for key in path_keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return {}
        return current if isinstance(current, dict) else {path_keys[-1]: current}
    
    # Get paths at specified level for dropdown
    available_paths = get_paths_at_level(data_dict, target_level=dropdown_level)
    
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
    
    for path_label, path_keys in available_paths:
        if path_label == "all":
            # Show all parameters
            flattened_items = flatten_dict_with_brackets(data_dict)
            params = [item[0] for item in flattened_items]
            vals = [str(item[1]) for item in flattened_items]
        else:
            # Get specific sub-dictionary at the chosen level
            sub_dict = get_subdict_by_path(data_dict, path_keys)
            if isinstance(sub_dict, dict) and sub_dict:
                flattened_items = flatten_dict_with_brackets(sub_dict, path_keys)
                params = [item[0] for item in flattened_items]
                vals = [str(item[1]) for item in flattened_items]
            else:
                # If it's not a dict or empty, show it as a single parameter
                if path_keys:
                    bracket_path = ''.join([f'["{key}"]' for key in path_keys])
                    params = [bracket_path]
                    vals = [str(sub_dict)]
                else:
                    params = []
                    vals = []
        
        dropdown_buttons.append(
            dict(
                label=path_label,
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
                x=0,
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
                         logo_file_path=None, plot_items="", parameters_dict=None, dropdown_level=1):
    
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
    
    if parameters_dict:
        # Use the version with configurable dropdown level
        param_table = create_parameter_table(parameters_dict, "", dropdown_level)
        # Convert Plotly figure to HTML
        param_table_html = param_table.to_html(include_plotlyjs='cdn', div_id="parameters-table")
        plot_items = param_table_html + plot_items
    
    # Replace plot items
    html_content = html_content.replace("{{PLOT_ITEMS_TABLE}}", plot_items)
    html_content = remove_div(html_content)
    # Write the populated HTML
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Example usage with different levels
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
        },
        "datddd": {
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
            }
        }
    }
    
    # Path to your logo file
    logo_file_path = r"D:\WORKSPACE\TESTMODEL\BMW_Base64_Logo.txt"
    
    # Example 1: Level 1 dropdown (original behavior)
    print("Creating report with level 1 dropdown...")
    populate_html_template(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path="simulation_report_level1.html",
        script_name=script_name,
        date_time=date_time,
        simulation_id=simulation_id,
        logo_file_path=logo_file_path,
        parameters_dict=sample_parameters,
        dropdown_level=1
    )
    
    # Example 2: Level 2 dropdown
    print("Creating report with level 2 dropdown...")
    populate_html_template(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path="simulation_report_level2.html",
        script_name=script_name,
        date_time=date_time,
        simulation_id=simulation_id,
        logo_file_path=logo_file_path,
        parameters_dict=sample_parameters,
        dropdown_level=2
    )
    
    # Example 3: Level 3 dropdown
    print("Creating report with level 3 dropdown...")
    populate_html_template(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path="simulation_report_level3.html",
        script_name=script_name,
        date_time=date_time,
        simulation_id=simulation_id,
        logo_file_path=logo_file_path,
        parameters_dict=sample_parameters,
        dropdown_level=3
    )
    
    print("Reports created with different dropdown levels!")
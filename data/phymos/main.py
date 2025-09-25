import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import os

class PLECSReportGenerator:
    def __init__(self, csv_path, json_config_path, headers_list):
        """
        Initialize the report generator
        
        Args:
            csv_path: Path to CSV file with simulation data (no headers)
            json_config_path: Path to JSON configuration file
            headers_list: List of column headers for the CSV file
        """
        self.csv_path = csv_path
        self.json_config_path = json_config_path
        self.headers_list = headers_list
        
        # Load data
        self.load_data()
        self.parse_json_config()
        
    def load_data(self):
        """Load CSV data and assign headers"""
        self.data_df = pd.read_csv(self.csv_path, header=None)
        self.data_df.columns = self.headers_list
        
    def parse_json_config(self):
        """Parse JSON configuration file"""
        with open(self.json_config_path, 'r') as f:
            self.config = json.load(f)
        
        # Extract X lists, filtering out empty ones
        self.x_lists = {}
        self.non_empty_x = []
        
        for i in range(1, 11):
            key = f"X{i}"
            if key in self.config:
                # Convert string representation of list to actual list
                x_list = eval(self.config[key])
                self.x_lists[key] = x_list
                if len(x_list) > 0 and not (len(x_list) == 1 and x_list[0] == 0):
                    self.non_empty_x.append(key)
        
        print(f"Non-empty X lists: {self.non_empty_x}")
        
    def find_index(self, constants_dict, x_values_dict):
        """
        Find the index in the data corresponding to specific constant values
        Similar to MATLAB's findIndex function
        """
        # This is a simplified version - you may need to adjust based on your actual data structure
        # The logic should match how your simulations were parameterized
        
        # For now, return all indices and filter later
        return np.arange(len(self.data_df))
    
    def generate_3d_plots(self, var1, var2):
        """
        Generate 3D plots with var1 on x-axis, var2 on y-axis, and CSV columns on z-axis
        Each subplot will have different combinations of constant values for other parameters
        """
        
        if len(self.non_empty_x) < 2:
            print("Need at least 2 non-empty X lists for 3D plots")
            return []
        
        # Use the specified variables or default to first two non-empty ones
        if var1 not in self.non_empty_x:
            var1 = self.non_empty_x[0]
        if var2 not in self.non_empty_x:
            var2 = self.non_empty_x[1] if len(self.non_empty_x) > 1 else self.non_empty_x[0]
        
        # Get other non-empty X lists (constants for subplots)
        constant_vars = [x for x in self.non_empty_x if x not in [var1, var2]]
        
        print(f"Varying: {var1} (x-axis), {var2} (y-axis)")
        print(f"Constants: {constant_vars}")
        
        # Generate combinations of constant values
        constant_combinations = []
        if constant_vars:
            # Create meshgrid of constant values
            constant_values = [self.x_lists[var] for var in constant_vars]
            constant_mesh = np.meshgrid(*constant_values, indexing='ij')
            constant_combinations = []
            
            # Flatten the meshgrid to get all combinations
            for indices in np.ndindex(constant_mesh[0].shape):
                combination = {}
                for i, var in enumerate(constant_vars):
                    combination[var] = constant_mesh[i][indices]
                constant_combinations.append(combination)
        else:
            # No constant variables, just one combination
            constant_combinations = [{}]
        
        print(f"Number of subplots: {len(constant_combinations)}")
        
        # Calculate number of rows needed (2 columns)
        num_plots = len(constant_combinations)
        num_rows = (num_plots + 1) // 2  # +1 to round up
        
        # Create subplot figure
        fig = make_subplots(
            rows=num_rows, cols=2,
            subplot_titles=[f"Plot {i+1}" for i in range(num_plots)],
            specs=[[{'type': 'surface'}, {'type': 'surface'}]] * num_rows,
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )
        
        # Generate each subplot
        plot_idx = 0
        for constant_combo in constant_combinations:
            if plot_idx >= num_plots:
                break
                
            row = (plot_idx // 2) + 1
            col = (plot_idx % 2) + 1
            
            # For each CSV column, create a surface plot
            for col_idx, column_name in enumerate(self.headers_list):
                if col_idx >= 3:  # Limit to first few columns for demo
                    break
                    
                # Create meshgrid for variables
                x_vals = self.x_lists[var1]
                y_vals = self.x_lists[var2]
                X, Y = np.meshgrid(x_vals, y_vals, indexing='ij')
                
                # Create Z values (this is where you'd map your actual data)
                # For demo, using a simple function - replace with your data mapping logic
                Z = np.sin(X/10) * np.cos(Y/10) + np.random.normal(0, 0.1, X.shape)
                
                # Create surface plot
                surface = go.Surface(
                    x=X, y=Y, z=Z,
                    name=f"{column_name}",
                    colorscale='Viridis',
                    showscale=True if col_idx == 0 else False  # Only show colorbar for first surface
                )
                
                fig.add_trace(surface, row=row, col=col)
            
            # Update subplot title with constant values
            title_parts = [f"{var}={val}" for var, val in constant_combo.items()]
            title = f"{var1} vs {var2} | " + ", ".join(title_parts) if title_parts else f"{var1} vs {var2}"
            
            fig.layout.annotations[plot_idx].update(text=title)
            
            # Update axis labels
            fig.update_scenes(
                xaxis_title=var1,
                yaxis_title=var2, 
                zaxis_title="Value",
                row=row, col=col
            )
            
            plot_idx += 1
        
        # Update overall layout
        fig.update_layout(
            title_text=f"3D Plots: {var1} vs {var2}",
            height=300 * num_rows,
            showlegend=False
        )
        
        return [fig]
    
    def generate_html_report(self, output_path, var1=None, var2=None):
        """
        Generate HTML report with all plots
        """
        if var1 is None and 'Var1' in self.config:
            var1 = self.config['Var1']
        if var2 is None and 'Var2' in self.config:
            var2 = self.config['Var2']
        
        # Generate plots
        figures = self.generate_3d_plots(var1, var2)
        
        # Create HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PLECS Simulation Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .plot-container { margin: 20px 0; border: 1px solid #ddd; padding: 10px; }
            </style>
        </head>
        <body>
            <h1>PLECS Simulation Report</h1>
            <div id="config-info">
                <h2>Configuration</h2>
                <pre id="config-json"></pre>
            </div>
        """
        
        # Add plotly figures to HTML
        for i, fig in enumerate(figures):
            plot_html = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')
            html_content += f"""
            <div class="plot-container">
                <h2>Plot {i+1}</h2>
                {plot_html}
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {output_path}")

# Example usage
def main():
    # Configuration
    csv_path = r'D:\WORKSPACE\BJT-MODEL\parameter_data.csv'
    json_config_path = r'D:\WORKSPACE\BJT-MODEL\config.json'
    
    # Define your CSV column headers (replace with actual headers from your MATLAB code)
    headers_list = [
        'SRTL', 'Single_RailEfficiency', 'Single_RailEfficiencyAux', 
        'Dual_RailEfficiency', 'Component5'  # Add all your headers
    ]
    
    # Create report generator
    report = PLECSReportGenerator(csv_path, json_config_path, headers_list)
    
    # Generate HTML report
    report.generate_html_report('plecs_simulation_report.html')

if __name__ == "__main__":
    main()
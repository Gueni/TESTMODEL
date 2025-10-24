import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def add_plotly_figures():
    # Example 1: Line plot
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 11, 12, 13, 14]
    })
    line_fig = px.line(df, x='x', y='y', title='Sample Line Plot')
    
    # Example 2: Bar chart
    bar_fig = px.bar(df, x='x', y='y', title='Sample Bar Chart')
    
    # Example 3: Custom table
    table_fig = go.Figure(data=[go.Table(
        header=dict(values=['A', 'B', 'C']),
        cells=dict(values=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )])
    
    # Convert all to HTML
    plots_html = (
        line_fig.to_html(include_plotlyjs=False, div_id="line-plot") +
        bar_fig.to_html(include_plotlyjs=False, div_id="bar-chart") +
        table_fig.to_html(include_plotlyjs=False, div_id="data-table")
    )
    
    return plots_html

# Usage in your function:
def populate_html_template(..., plot_items="", parameters_dict=None):
    # ... existing code ...
    
    # Add your plots
    additional_plots = add_plotly_figures()
    plot_items = additional_plots + plot_items  # Add before parameters table
    
    # ... rest of the code ...





















    def populate_html_template(template_path, output_path, script_name, date_time, simulation_id, 
                         logo_file_path=None, plot_items="", parameters_dict=None, 
                         additional_plots=None, additional_tables=None):
    
    with open(template_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Replace the variables
    html_content = html_content.replace("{{TITLE}}", "Simulation Report")
    html_content = html_content.replace("{{SCRIPT_NAME}}", ":  "+script_name)
    html_content = html_content.replace("{{DATE_TIME}}", ":  "+date_time)
    html_content = html_content.replace("{{SIMULATION_ID}}", ":  "+simulation_id)
    
    # Handle logo
    if logo_file_path:
        with open(logo_file_path, 'r', encoding='utf-8') as logo_file:
            logo_base64 = logo_file.read().strip()
        html_content = html_content.replace("{{LOGO_BASE64}}", logo_base64)
    
    all_plot_items = ""
    
    # Add parameters table if provided
    if parameters_dict:
        param_table = create_parameter_table(parameters_dict, "Simulation Parameters")
        param_table_html = param_table.to_html(include_plotlyjs='cdn', div_id="parameters-table")
        all_plot_items += param_table_html
    
    # Add additional plots
    if additional_plots:
        for i, plot in enumerate(additional_plots):
            plot_html = plot.to_html(include_plotlyjs=False, div_id=f"plot-{i}")
            all_plot_items += plot_html
    
    # Add additional tables
    if additional_tables:
        for i, table in enumerate(additional_tables):
            table_html = table.to_html(include_plotlyjs=False, div_id=f"table-{i}")
            all_plot_items += table_html
    
    # Add any existing plot items
    all_plot_items += plot_items
    
    # Replace plot items
    html_content = html_content.replace("{{PLOT_ITEMS}}", all_plot_items)
    
    # Write the populated HTML
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
















        # Example usage with multiple plots and tables
if __name__ == "__main__":
    # Your existing variables
    script_name = "standalone_cs555555555555555555555555555555555555v.py"
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    simulation_id = "1759764207"
    
    # Create additional plots
    additional_plots = []
    additional_tables = []
    
    # 1. Create a scatter plot
    scatter_fig = px.scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], 
                           title="Performance Scatter Plot")
    additional_plots.append(scatter_fig)
    
    # 2. Create a histogram
    hist_fig = px.histogram(x=[1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4], 
                          title="Distribution Histogram")
    additional_plots.append(hist_fig)
    
    # 3. Create a data table
    data_table = go.Figure(data=[go.Table(
        header=dict(values=['Metric', 'Value', 'Threshold']),
        cells=dict(values=[
            ['Accuracy', 'Precision', 'Recall'],
            [0.95, 0.92, 0.88],
            [0.85, 0.80, 0.75]
        ])
    )])
    data_table.update_layout(title="Model Metrics")
    additional_tables.append(data_table)
    
    # 4. Create a heatmap
    import numpy as np
    heatmap_data = np.random.rand(5, 5)
    heatmap_fig = px.imshow(heatmap_data, title="Correlation Heatmap")
    additional_plots.append(heatmap_fig)
    
    # Populate template with everything
    populate_html_template(
        template_path="HTML_REPORT_TEMPLATE.html",
        output_path="simulation_report.html",
        script_name=script_name,
        date_time=date_time,
        simulation_id=simulation_id,
        logo_file_path=logo_file_path,
        parameters_dict=sample_parameters,
        additional_plots=additional_plots,
        additional_tables=additional_tables
    )


















    class ReportPlotManager:
    def __init__(self):
        self.plots = []
        self.tables = []
    
    def add_plot(self, plot, title=None):
        if title:
            plot.update_layout(title=title)
        self.plots.append(plot)
    
    def add_table(self, data, columns, title=None):
        table_fig = go.Figure(data=[go.Table(
            header=dict(values=columns),
            cells=dict(values=data)
        )])
        if title:
            table_fig.update_layout(title=title)
        self.tables.append(table_fig)
    
    def generate_html(self):
        html_content = ""
        for i, plot in enumerate(self.plots):
            html_content += plot.to_html(include_plotlyjs=False, div_id=f"plot-{i}")
        for i, table in enumerate(self.tables):
            html_content += table.to_html(include_plotlyjs=False, div_id=f"table-{i}")
        return html_content

# Usage:
plot_manager = ReportPlotManager()
plot_manager.add_plot(scatter_fig, "Scatter Analysis")
plot_manager.add_table(
    data=[[1, 2, 3], [4, 5, 6]], 
    columns=['Col A', 'Col B', 'Col C'],
    title="Sample Data Table"
)

# Then use in your main function:
plot_items = plot_manager.generate_html()
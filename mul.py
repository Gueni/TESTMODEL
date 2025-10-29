import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_signal_figures(csv_file, units):
    """
    Create Plotly figures from CSV data with Time as x-axis and signals as y-axis.
    
    Parameters:
    csv_file (str): Path to the CSV file
    units (list): List of units for each signal (excluding Time column)
    
    Returns:
    list: List of Plotly figure objects
    """
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Get signal names (all columns except first)
    time_col = df.columns[0]
    signal_names = df.columns[1:]
    
    # Validate units list length
    if len(units) != len(signal_names):
        raise ValueError(f"Number of units ({len(units)}) must match number of signals ({len(signal_names)})")
    
    figures = []
    
    # Create individual figure for each signal
    for i, (signal_name, unit) in enumerate(zip(signal_names, units)):
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[time_col],
            y=df[signal_name],
            mode='lines',
            showlegend=False,  # No legend
            line=dict(color='blue')
        ))
        
        # Set layout
        fig.update_layout(
            title=signal_name,  # Title is the signal name from header
            xaxis_title=time_col,
            yaxis_title=f"{signal_name} ({unit})",
            template="plotly_white"
        )
        
        figures.append(fig)
    
    return figures

# Example usage:
# figures = create_signal_figures("data.csv", ["V", "A", "Pa", "°C"])
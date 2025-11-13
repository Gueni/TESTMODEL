import plotly.graph_objects as go
import numpy as np

# Sample FFT data
freqs = np.fft.fftfreq(100)
amplitudes = np.abs(np.fft.fft(np.random.randn(100)))
phases = np.angle(np.fft.fft(np.random.randn(100)))

# Create 3D bar coordinates
x_positions = []
y_positions = [] 
z_positions = []
custom_data = []

for i, (freq, amp, phase) in enumerate(zip(freqs, amplitudes, phases)):
    if freq >= 0:  # Only positive frequencies
        # Create bar vertices
        bar_width = 0.1
        x = [freq, freq+bar_width, freq+bar_width, freq] * 2
        y = [0, 0, bar_width, bar_width] * 2  
        z = [0, 0, 0, 0, amp, amp, amp, amp]
        
        x_positions.extend(x)
        y_positions.extend(y)
        z_positions.extend(z)
        
        # Add custom data for each vertex
        for _ in range(8):  # 8 vertices per bar
            custom_data.append([freq, amp, phase])

# Define mesh indices (simplified - you'll need proper triangulation)
i_indices = [0, 0, 4, 4, 0, 1, 5, 5, 1, 2, 6, 6, 2, 3, 7, 7, 3, 0, 4, 4]
j_indices = [1, 4, 5, 0, 2, 5, 6, 1, 3, 6, 7, 2, 0, 7, 4, 3, 4, 5, 6, 7]  
k_indices = [4, 5, 6, 7, 5, 6, 7, 4, 6, 7, 4, 5, 7, 4, 5, 6, 1, 2, 3, 0]

fig = go.Figure()

fig.add_trace(go.Mesh3d(
    x=x_positions,
    y=y_positions,
    z=z_positions,
    i=i_indices,
    j=j_indices,
    k=k_indices,
    intensity=amplitudes,
    colorscale='Viridis',
    hoverinfo='none',  # Disable default hover
    customdata=custom_data,
    hovertemplate=(
        'Frequency: %{customdata[0]:.3f} Hz<br>'
        'Amplitude: %{customdata[1]:.4f}<br>'
        'Phase: %{customdata[2]:.2f}°<br>'
        '<extra></extra>'
    ),
    showscale=True  # Keep colorbar if needed
))

fig.update_layout(
    scene=dict(
        xaxis_title='Frequency (Hz)',
        yaxis_title='',
        zaxis_title='Amplitude',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
    ),
    title='3D FFT Visualization'
)

fig.show()
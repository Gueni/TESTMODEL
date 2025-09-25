import os
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ============================
# USER INPUT SECTION
# ============================

# Path to CSV folder (where your simulation CSVs are stored)
csv_folder = r"D:\WORKSPACE\BJT-MODEL\source"

# Path to JSON file (input configuration)
json_file = r"D:\WORKSPACE\BJT-MODEL\config.json"

# List of CSV files to load (order matters!)
csv_names_order = [0,1]

# Pick component of interest (e.g., "SRTL")
component_name = "SRTL"

# Constant values for fixed operating points
Constant_1 = 0
Constant_2 = 35
Constant_3 = 13.5

# ============================
# LOAD JSON INPUTS
# ============================

with open(json_file, "r") as f:
    json_data = json.load(f)

inputs = json_data   # instead of json_data
for key in inputs["sweepNames"]:
    inputs[key] = np.array(eval(inputs[key]))


# Operating points
X1, X2, X3, X4, X5, X6, X7, X8, X9, X10 = [inputs[f"X{i}"] for i in range(1, 11)]

# Variables for plotting
Var1 = inputs["Var1"]   # e.g. "X3"
Var2 = inputs["Var2"]   # e.g. "X5"

Variable_1 = inputs[Var1]
Variable_2 = inputs[Var2]

Case = "Typical" if Constant_1 == 0 else "Worst-Case"

# ============================
# LOAD CSV DATA
# ============================

csv_files = sorted(os.listdir(csv_folder))
print(csv_files)
print(f"Found {len(csv_files)} CSV files in {csv_folder}")
selected_csvs = [csv_files[i] for i in csv_names_order]

# Stack all CSVs into one matrix (like combinedMap in MATLAB)
combined_map = []
for fname in selected_csvs:
    data = np.loadtxt(os.path.join(csv_folder, fname), delimiter=",")
    combined_map.append(data)

combined_map = np.vstack(combined_map)  # rows = components, cols = data points

# Make dictionary of probed params
component_names = [f"Comp_{i}" for i in range(combined_map.shape[0])]
probed_params = {name: idx for idx, name in enumerate(component_names)}

# Overwrite one with actual name you care about
probed_params[component_name] = probed_params[component_names[0]]

# ============================
# BUILD MAP FOR 3D PLOT
# ============================

def find_index(c1, c2, v1, c3, v2,
               x6, x7, x8, x9, x10,
               X1, X2, X3, X4, X5, X6, X7, X8, X9, X10):
    """
    Mimics MATLAB findIndex (maps operating points into a flat index).
    For simplicity, we assume row-major ordering across sweep dimensions.
    """
    grid = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
    values = [c1, c2, v1, c3, v2, x6, x7, x8, x9, x10]

    # find indices for each variable
    idxs = [np.where(np.isclose(g, val))[0][0] for g, val in zip(grid, values)]
    # convert multi-index into flat index
    strides = np.cumprod([1] + [len(g) for g in grid[::-1]])[::-1][1:]
    flat_idx = sum(i * s for i, s in zip(idxs, strides))
    return flat_idx


component_idx = probed_params[component_name]
z_values = []

for v1 in Variable_1:
    row = []
    for v2 in Variable_2:
        idx = find_index(Constant_1, Constant_2, v1, Constant_3, v2,
                         0, 0, 0, 0, 0,
                         X1, X2, X3, X4, X5, X6, X7, X8, X9, X10)
        row.append(combined_map[component_idx, idx])
    z_values.append(row)

Z = np.array(z_values) / 8.0

# ============================
# PLOT 3D SURFACE
# ============================

X, Y = np.meshgrid(Variable_2, Variable_1)

fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis")])
fig.update_layout(
    scene=dict(
        xaxis_title="Target Load Power [W]",
        yaxis_title="Input Voltage [V]",
        zaxis_title=component_name
    ),
    title=f"{component_name} Map in {Case} conditions "
          f"with respect to Input Voltage & Output Power "
          f"at {Constant_2}°C Water Temperature & {Constant_3}V Output"
)

fig.show()

# ============================
# EXPORT FLATTENED MATRIX
# ============================

# Example: reshape as in MATLAB
component_map = combined_map[component_idx, :] * 1.4444
component_map_reshaped = component_map.reshape(len(X5), len(X4), len(X3), len(X2))

# Take slice at X4 index = 4
component_map_135 = component_map_reshaped[:, 1, :, :]  # Python uses 0-based index

# Reshape
component_map_135_reshaped = component_map_135.reshape(len(X5), len(X3), len(X2))

# Permute axes (swap to desired orientation)
C = np.transpose(component_map_135_reshaped, (0, 2, 1))

# Flatten
component_map_135_flat = C.reshape(-1, C.shape[-1])

# Add X5 as first column
X5_repeated = np.tile(X5, len(component_map_135_flat) // len(X5))
component_map_135_flat_new = np.column_stack([X5_repeated, component_map_135_flat])

# Save to CSV
df = pd.DataFrame(component_map_135_flat_new)
df.to_csv("LuT_3D.csv", index=False, header=False)

import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

# -------------------------------
# Paths
# -------------------------------
csv_file = r'D:\WORKSPACE\BJT-MODEL\parameter_data.csv'
json_file = r'D:\WORKSPACE\BJT-MODEL\config.json'

# -------------------------------
# Load CSV data
# -------------------------------
combined_map = pd.read_csv(csv_file, header=None).values

# -------------------------------
# Load JSON input file
# -------------------------------
with open(json_file, 'r') as f:
    json_data = json.load(f)
inputs = json_data['inputs']

# Extract operating points
X1 = np.array(eval(inputs['X1']))
X2 = np.array(eval(inputs['X2']))
X3 = np.array(eval(inputs['X3']))
X4 = np.array(eval(inputs['X4']))
X5 = np.array(eval(inputs['X5']))
X6 = np.array(eval(inputs['X6']))
X7 = np.array(eval(inputs['X7']))
X8 = np.array(eval(inputs['X8']))
X9 = np.array(eval(inputs['X9']))
X10 = np.array(eval(inputs['X10']))

# -------------------------------
# Component names
# -------------------------------
component_names = ['SRTL'] + [f'Comp{i}' for i in range(2, combined_map.shape[0]+1)]
probed_params = {name: idx for idx, name in enumerate(component_names)}
params_names = list(probed_params.keys())
Component = probed_params['SRTL']

# -------------------------------
# Fully vectorized 3D map (X3 vs X5)
# -------------------------------
Variable_1 = X3  # X3 varies
Variable_2 = X5  # X5 varies

# Create meshgrid of variable combinations
V1_grid, V2_grid = np.meshgrid(Variable_1, Variable_2, indexing='ij')  # shape: len(X3), len(X5)
V1_flat = V1_grid.ravel()
V2_flat = V2_grid.ravel()

# Vectorized distance calculation to find closest indices
X3_grid_2D, X5_grid_2D = np.meshgrid(X3, X5, indexing='ij')
flat_grid_2D = np.vstack([X3_grid_2D.ravel(), X5_grid_2D.ravel()]).T
target_points = np.vstack([V1_flat, V2_flat]).T

# Broadcasting distances for all points
dist_matrix = np.linalg.norm(flat_grid_2D[None, :, :] - target_points[:, None, :], axis=2)
indices = np.argmin(dist_matrix, axis=1)

# Map to component values
x_list = combined_map[Component, indices]
Z = x_list.reshape(len(Variable_1), len(Variable_2)) / 8
X, Y = np.meshgrid(Variable_2, Variable_1)

# -------------------------------
# Plot 3D surface
# -------------------------------
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', alpha=1.0)
cbar = fig.colorbar(surf)
cbar.set_label(params_names[Component], fontsize=14)
ax.set_xlabel('Target Load Power [W]', fontsize=14)
ax.set_ylabel('Input Voltage [V]', fontsize=14)
ax.set_zlabel(params_names[Component], fontsize=14)
ax.set_title(f"{params_names[Component]} Map in Typical conditions\n"
             f"with Respect to Input Voltage & Output Power at 35°C Water Temperature & 13.5V Output.", fontsize=14)
plt.show()

# -------------------------------
# Fully vectorized 4D component map flattening (X5, X4, X3, X2)
# -------------------------------
X5_grid, X4_grid, X3_grid, X2_grid = np.meshgrid(X5, X4, X3, X2, indexing='ij')
X5_flat = X5_grid.ravel()
X4_flat = X4_grid.ravel()
X3_flat = X3_grid.ravel()
X2_flat = X2_grid.ravel()

# Vectorized mapping for 4D grid
X3_grid_2D, X5_grid_2D = np.meshgrid(X3, X5, indexing='ij')
flat_grid_2D = np.vstack([X3_grid_2D.ravel(), X5_grid_2D.ravel()]).T
target_points_2D = np.vstack([X3_flat, X5_flat]).T

dist_matrix = np.linalg.norm(flat_grid_2D[None, :, :] - target_points_2D[:, None, :], axis=2)
indices_2D = np.argmin(dist_matrix, axis=1)

# Map values and scale
component_map_flat = combined_map[Component, indices_2D] * 1.4444
component_map_reshaped = component_map_flat.reshape(len(X5), len(X4), len(X3), len(X2))

# Slice X4 index=3 (MATLAB index 4)
component_map_slice = component_map_reshaped[:, 2, :, :]
component_map_slice_reshaped = component_map_slice.reshape(len(X5), len(X3), len(X2))

# Permute and flatten (vectorized)
C = np.transpose(component_map_slice_reshaped, (0, 2, 1))
component_map_flat_new = np.zeros((C.shape[0]*C.shape[1], C.shape[2]+1))
component_map_flat_new[:, 1:] = C.reshape(-1, C.shape[2])
component_map_flat_new[:, 0] = np.tile(X5, C.shape[1])

# Export CSV
pd.DataFrame(component_map_flat_new).to_csv('LuT_3D.csv', header=False, index=False)

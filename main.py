

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# findIndex (adapted)
# -------------------------------
def findIndex(points, matrix, pattern=True):
    """
    Finds the starting index for each row/column in a matrix based on a list of points.

    Args:
        points (list)       : A list of points to search for in the matrix.
        matrix (list[list]) : A two-dimensional matrix to search for the points in.
        pattern (bool)      : Return a pattern index if True; else uniform index.

    Returns:
        indices (list) : List of indices representing the position of each point.
        itr (int)      : The combined iteration index.
    """
    indices = []

    if pattern:
        # Compute index of each point in its corresponding row
        indices = [matrix[i].index(points[i]) if points[i] in matrix[i] else 0 for i in range(len(points))]
        # Weighted sum of indices
        itr = sum(
            indices[i] * np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])
            for i in range(len(indices) - 1)
        ) + indices[-1]
        indices.append(itr)
    else:
        # If pattern=False, uniform index for all rows
        itr = matrix[0].index(points[0]) if points[0] in matrix[0] else 0
        indices = np.full(len(matrix) + 1, itr).tolist()

    return indices, itr

# -------------------------------
# Paths
# -------------------------------
csv_folder = r"D:\WORKSPACE\BJT-MODEL\csvMaps"
json_file = r"D:\WORKSPACE\BJT-MODEL\Input_vars.json"
header_folder = r"D:\WORKSPACE\BJT-MODEL\HEADER_FILES"

headers = ["CT Trafo Primary Current AVG", "CT Trafo Secondary Current AVG", 
           "Choke RC Snubber Capacitor Current AVG", 
           "CT Trafo Primary voltage AVG", "CT Trafo Secondary voltage AVG"]

componentNames = [str(h) for h in headers]

# -------------------------------
# Load CSVs and split into columns
# -------------------------------
combinedMap = []

for f in sorted(os.listdir(csv_folder)):
    csv_path = os.path.join(csv_folder, f)
    data = np.loadtxt(csv_path, delimiter=',')  # shape: (n_rows, n_cols)
    
    # Ensure 2D even if CSV has only one column
    if data.ndim == 1:
        data = data[:, np.newaxis]
    
    # Append each column separately
    for col in range(data.shape[1]):
        combinedMap.append(data[:, col])

# Now combinedMap[i] = 1D array for a single column (component)
print(f"Total components loaded: {len(combinedMap)}")


# -------------------------------
# Load JSON
# -------------------------------
with open(json_file, 'r') as f: data = json.load(f)
X = [eval(data[f"X{i}"]) for i in range(1, 11)]

# Use sweepNames and Var1/Var2
sweepNames = data["sweepNames"]
Var1_name  = data["Var1"]
Var2_name  = data["Var2"]

# Select variables to sweep by indexing into X
Variable_1 = X[int(Var1_name[1:])-1]  # X3 → X[2]
Variable_2 = X[int(Var2_name[1:])-1]  # X5 → X[4]

# -------------------------------
# Operating points constants
# -------------------------------
Constant_1 = 75
Constant_2 = 200
Constant_3 = 10.5

# -------------------------------
# Choose component to plot
# -------------------------------
# Component = componentNames.index("CT Trafo Secondary Current AVG")
# Component = componentNames.index("CT Trafo Primary Current AVG")
# Component = componentNames.index("Choke RC Snubber Capacitor Current AVG")
Component = componentNames.index("CT Trafo Primary voltage AVG")

# -------------------------------
# Build data for surface
# -------------------------------
x_vals = []
for v1 in Variable_1:
    for v2 in Variable_2:
        indices, idx = findIndex(
            [Constant_1, Constant_2, v1, Constant_3, v2, 0, 0, 0, 0, 0],
            X,
            pattern=False
        )
        x_vals.append(combinedMap[Component][idx])


x_vals = np.array(x_vals)
# -------------------------------
# Meshgrid & plot
# -------------------------------
X_mesh, Y_mesh = np.meshgrid(Variable_2, Variable_1)
Z = x_vals.reshape(len(Variable_1), len(Variable_2)) / 8.0

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X_mesh, Y_mesh, Z, alpha=1.0, cmap="viridis")

cbar = fig.colorbar(surf, ax=ax)
cbar.ax.tick_params(labelsize=12)

ax.set_xlabel(sweepNames[int(Var2_name[1:])-1], fontsize=14)
ax.set_ylabel(sweepNames[int(Var1_name[1:])-1], fontsize=14)
ax.set_zlabel(componentNames[Component], fontsize=14)

ax.set_title(f"{componentNames[Component]} \n  Temperature: {Constant_1} & Input Voltage: {Constant_2} & Output Power: {Constant_3}",
             fontsize=12)

plt.show()


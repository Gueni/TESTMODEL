# Import the JSON module for parsing JSON strings in the configuration
import json
# Import NumPy for numerical operations and matrix manipulations
import numpy as np

def get_active_wca_params(Xs):
    """
    Identify which parameters X lists are used in Worst-Case Analysis (WCA).
    
    This function examines a list of parameter lists (X1 through X10) and identifies
    which ones are active for WCA. Active parameters are those that are not placeholder zero values.
    
    Parameters:
        Xs (list): List of parameter lists for X1-X10, where each element is a list
                  of parameter values. Placeholder values are either [0] or [[0]].
        
    Returns:
        list: Indices of parameters that are not placeholder values.
    """
    # Use list comprehension to iterate through enumerated Xs list
    # enumerate provides both index (i) and value (var) for each parameter list
    return [i for i, var in enumerate(Xs) 
            # Check if var is NOT a placeholder zero value
            # Placeholders can be either [0] or [[0]] (nested list with zero)
            if var not in [[[0]], [0]] 
            # Ensure the list has elements (not empty)
            and len(var) > 0]

def apply_sensitivity(config_data, perturbation_value,perturbation_type='relative',include_nominals=True):
    """
    The function reads parameter vectors X1..X10 from a configuration dictionary,
    identifies which parameters are active,and builds a matrix where each parameter is perturbed individually while
    all other parameters remain at their nominal values.

    The resulting matrices for each operating point are stitched horizontally
    to form a complete sensitivity matrix.

    Args    :
                config_data         : dict   Dictionary containing JSON encoded lists for parameters X1..X10.
                perturbation_value  : float  Value used to perturb the nominal parameter.
                perturbation_type   : str    Type of perturbation to apply:
                                                - 'absolute'        : nominal + perturbation_value
                                                - 'relative'        : nominal * (1 + perturbation_value / 100)
                                                - 'multiplicative'  : nominal * perturbation_value
                include_nominals    : bool, optional   If True, the nominal parameter matrix is appended to the final result.

    Returns :
                list    Updated list of parameter vectors X1..X10 containing the sensitivity matrix.
    """

    # Extract parameter lists X1..X10 from the configuration dictionary
    # Each parameter is stored as a JSON string, so we parse it into Python lists
    Xs              = [json.loads(config_data.get(f"X{i}", "[0]")) for i in range(1, 11)]

    # Determine which parameters are active for Worst Case Analysis (WCA)
    active_indices  = get_active_wca_params(Xs)

    # Number of active variables participating in the sensitivity analysis
    n_vars          = len(active_indices)

    # Number of operating points (length of each parameter vector)
    m               = len(Xs[active_indices[0]])

    # List that will store each sensitivity block before stitching
    stitched_blocks = []

    # Loop over each operating point
    for k in range(m):

        # Extract nominal values for all active parameters at operating point k
        nominal_values  = [Xs[i][k] for i in active_indices]

        # Initialize a square matrix for the sensitivity block
        result_matrix   = np.zeros((n_vars, n_vars))

        # Fill each row with the corresponding nominal value
        for i in range(n_vars):
            
            result_matrix[i, :] = nominal_values[i]

        # Apply perturbation to each variable independently (diagonal perturbation)
        for i in range(n_vars):

            # Nominal value of the current variable
            nominal             = nominal_values[i]

            # Compute perturbed value depending on perturbation type
            if      perturbation_type == 'absolute'         :   perturbed = nominal + perturbation_value
            elif    perturbation_type == 'relative'         :   perturbed = np.abs(nominal * (1 + perturbation_value / 100))
            elif    perturbation_type == 'multiplicative'   :   perturbed = nominal * perturbation_value
            else                                            :   raise ValueError("Unknown perturbation type")

            # Replace the diagonal element with the perturbed value
            # result_matrix[i, i] = perturbed
            np.fill_diagonal(result_matrix, perturbed)


        # Append the generated block for this operating point
        stitched_blocks.append(result_matrix)

    # Horizontally concatenate all sensitivity blocks
    stitched        = np.hstack(stitched_blocks)

    # Optionally append the nominal parameter matrix
    if include_nominals:

        # Construct matrix containing nominal parameter values
        nominal_matrix  = np.array([[Xs[i][k] for k in range(m)] for i in active_indices])

        # Append nominal values to the right of the stitched sensitivity matrix
        final_matrix    = np.hstack((stitched, nominal_matrix))
    else:

        # If nominal values are not requested, keep only the sensitivity matrix
        final_matrix    = stitched

    # Write the resulting rows back into the original parameter structure
    for idx, row in zip(active_indices, final_matrix)   :   Xs[idx] = row.tolist()

    # Return the updated parameter lists
    return Xs

# Example usage with multiple data points
your_config = {
    # X1-X6 are active parameters with multiple data points
    "X1": "[35, 40,55]",      # First parameter with 2 points
    "X2": "[200, 250,300]",    # Second parameter with 2 points
    "X3": "[11.5, 12.0,13.0]",  # Third parameter with 2 points
    "X4": "[500, 550,600]",    # Fourth parameter with 2 points
    "X5": "[66, 70,75]",      # Fifth parameter with 2 points
    "X6": "[96369, 96370,96375]", # Sixth parameter with 2 points
    "X7": "[0]",          # Inactive
    "X8": "[0]",          # Inactive
    "X9": "[0]",          # Inactive
    "X10": "[0]",         # Inactive
    "sweepNames": ["Water Temperature", "Input Voltage", "Output Voltage", 
                   "Output Power", "Test1", "Test2", "X7", "X8", "X9", "X10"]
}





result_xlists_abs = apply_sensitivity(your_config, 0.1, 'absolute')

for i, xlist in enumerate(result_xlists_abs, start=1):
    print(f"X{i}: {xlist}")





# Below is a **clean, professional Confluence documentation** for the **Sensitivity Matrix Generator for Worst-Case Analysis (WCA)**, formatted similarly to the previous documentation (architecture, diagrams, workflow, API documentation, etc.).

# You can **paste this directly into Confluence**.

# ---

# # Sensitivity Matrix Generator for Worst-Case Analysis (WCA)

# ## 1. Overview

# This module generates **sensitivity analysis matrices** used for **Worst-Case Analysis (WCA)** in engineering simulations.

# The algorithm perturbs **one parameter at a time** while keeping all others at their **nominal values**. This allows engineers to evaluate the **impact of each parameter independently** on system behavior.

# The implementation supports:

# * Multiple **operating points**
# * Multiple **perturbation types**
# * Automatic **active parameter detection**
# * Automatic **sensitivity matrix generation**
# * Optional **nominal simulation cases**

# ---

# ## Typical Applications

# | Domain                  | Example                                |
# | ----------------------- | -------------------------------------- |
# | Power Electronics       | Converter parameter tolerance analysis |
# | Control Systems         | Controller robustness testing          |
# | Circuit Design          | Component tolerance studies            |
# | Thermal Modeling        | Temperature sensitivity analysis       |
# | Reliability Engineering | Worst-case operating evaluation        |

# ---

# # System Architecture

# The sensitivity generator integrates into the simulation pipeline as follows.

# ```mermaid
# flowchart LR

# A[Configuration JSON] --> B[Parameter Parsing]
# B --> C[Active Parameter Detection]
# C --> D[Sensitivity Matrix Builder]
# D --> E[Simulation Parameter Vectors]

# E --> F[Simulation Engine]
# F --> G[Simulation Results]
# ```

# ---

# # Data Flow

# The full algorithm pipeline is illustrated below.

# ```mermaid
# flowchart TD

# A[Load Configuration] --> B[Parse JSON Parameter Lists]
# B --> C[Detect Active Parameters]
# C --> D[Loop Over Operating Points]
# D --> E[Extract Nominal Values]
# E --> F[Build Nominal Matrix]
# F --> G[Apply Perturbations]
# G --> H[Create Sensitivity Block]
# H --> I[Concatenate Blocks]
# I --> J[Append Nominal Matrix]
# J --> K[Update Parameter Lists]
# ```

# ---

# # Project Structure

# Example project organization:

# ```
# project_root
# │
# ├── sensitivity.py
# ├── config.json
# │
# ├── simulation_inputs
# │
# └── simulation_results
# ```

# ---

# # Input Configuration

# Parameters are provided through a **configuration dictionary**.

# Each parameter list is stored as a **JSON encoded list**.

# ### Example

# ```python
# config = {

# "X1": "[35,40,55]",
# "X2": "[200,250,300]",
# "X3": "[11.5,12.0,13.0]",
# "X4": "[500,550,600]",
# "X5": "[66,70,75]",
# "X6": "[96369,96370,96375]",

# "X7": "[0]",
# "X8": "[0]",
# "X9": "[0]",
# "X10": "[0]"
# }
# ```

# Inactive parameters are represented by:

# ```
# [0]
# ```

# or

# ```
# [[0]]
# ```

# ---

# # Parameter Structure

# Parameters follow the naming convention:

# ```
# X1
# X2
# ...
# X10
# ```

# Each parameter contains **values across operating points**.

# Example:

# ```
# X1 = [35,40,55]
# X2 = [200,250,300]
# ```

# Interpretation:

# ```
# Operating Point 1 → X1=35 , X2=200
# Operating Point 2 → X1=40 , X2=250
# Operating Point 3 → X1=55 , X2=300
# ```

# ---

# # Core Functions

# ## 1. `get_active_wca_params()`

# ### Purpose

# Detects which parameter vectors are **active** in the analysis.

# Inactive parameters are ignored during sensitivity matrix construction.

# ---

# ### Function Signature

# ```python
# get_active_wca_params(Xs)
# ```

# ---

# ### Parameters

# | Parameter | Description                             |
# | --------- | --------------------------------------- |
# | `Xs`      | List containing parameter lists X1..X10 |

# ---

# ### Return Value

# ```
# list
# ```

# Indices of active parameters.

# ---

# ### Example

# Input:

# ```
# X1 = [35,40]
# X2 = [200,250]
# X3 = [0]
# ```

# Output:

# ```
# [0,1]
# ```

# Meaning:

# ```
# X1 and X2 are active
# ```

# ---

# # 2. `apply_sensitivity()`

# ### Purpose

# Builds the **complete sensitivity simulation matrix**.

# Each simulation case perturbs **one variable only**.

# ---

# ### Function Signature

# ```python
# apply_sensitivity(
#     config_data,
#     perturbation_value,
#     perturbation_type='absolute',
#     include_nominals=True
# )
# ```

# ---

# ### Parameters

# | Parameter            | Description                                |
# | -------------------- | ------------------------------------------ |
# | `config_data`        | Dictionary containing JSON parameter lists |
# | `perturbation_value` | Value used for perturbation                |
# | `perturbation_type`  | Type of perturbation                       |
# | `include_nominals`   | Include nominal simulations                |

# ---

# ### Supported Perturbation Types

# #### Absolute

# ```
# perturbed = nominal + perturbation
# ```

# Example:

# ```
# 35 + 0.1 = 35.1
# ```

# ---

# #### Relative

# ```
# perturbed = nominal * (1 + percentage / 100)
# ```

# Example:

# ```
# 35 * (1 + 5/100) = 36.75
# ```

# ---

# #### Multiplicative

# ```
# perturbed = nominal * factor
# ```

# Example:

# ```
# 35 * 1.1 = 38.5
# ```

# ---

# # Sensitivity Matrix Concept

# For **N active parameters**, the algorithm generates **N simulations per operating point**.

# Each simulation perturbs **one parameter**.

# ---

# ## Example

# Nominal values:

# ```
# X1 = 35
# X2 = 200
# X3 = 11.5
# ```

# Absolute perturbation:

# ```
# +0.1
# ```

# Generated matrix:

# ```
# [35.1 35   35  ]
# [200  200.1 200]
# [11.5 11.5 11.6]
# ```

# Columns represent **simulation cases**.

# ---

# # Algorithm Details

# ## Step 1 — Load Parameter Lists

# Parameters are parsed from JSON strings.

# Example:

# ```
# "[35,40,55]" → [35,40,55]
# ```

# ---

# ## Step 2 — Detect Active Parameters

# Inactive parameters are filtered.

# Example:

# ```
# active_indices = [0,1,2,3,4,5]
# ```

# ---

# ## Step 3 — Determine Dimensions

# ```
# n_vars = number of active parameters
# m      = number of operating points
# ```

# Example:

# ```
# n_vars = 6
# m = 3
# ```

# ---

# ## Step 4 — Iterate Over Operating Points

# ```
# for k in range(m)
# ```

# Example:

# ```
# k=0
# k=1
# k=2
# ```

# ---

# ## Step 5 — Extract Nominal Values

# Example:

# ```
# nominal_values =
# [35,200,11.5,500,66,96369]
# ```

# ---

# ## Step 6 — Build Base Matrix

# Matrix size:

# ```
# n_vars × n_vars
# ```

# Example:

# ```
# 6 × 6
# ```

# Initial matrix:

# ```
# [35 35 35 35 35 35]
# [200 200 200 200 200 200]
# ...
# ```

# ---

# ## Step 7 — Apply Perturbation

# Only **diagonal elements** are perturbed.

# Example:

# ```
# [35.1 35 35 35 35 35]
# [200 200.1 200 200 200 200]
# ...
# ```

# Meaning:

# ```
# simulation 1 → perturb X1
# simulation 2 → perturb X2
# simulation 3 → perturb X3
# ```

# ---

# ## Step 8 — Store Block

# Each operating point produces a **sensitivity block**.

# ```
# Block1
# Block2
# Block3
# ```

# ---

# ## Step 9 — Stitch Blocks

# Blocks are concatenated horizontally.

# ```
# np.hstack()
# ```

# Example:

# ```
# [Block1 | Block2 | Block3]
# ```

# ---

# ## Step 10 — Append Nominal Matrix (Optional)

# If enabled:

# ```
# [sensitivity_matrix | nominal_matrix]
# ```

# ---

# ## Step 11 — Update Parameter Lists

# Each row replaces the original parameter vector.

# Example:

# ```
# X1 → sensitivity vector
# X2 → sensitivity vector
# ```

# Inactive parameters remain unchanged.

# ---

# # Example Usage

# ## Configuration

# ```python
# your_config = {

# "X1": "[35,40,55]",
# "X2": "[200,250,300]",
# "X3": "[11.5,12.0,13.0]",
# "X4": "[500,550,600]",
# "X5": "[66,70,75]",
# "X6": "[96369,96370,96375]",

# "X7": "[0]",
# "X8": "[0]",
# "X9": "[0]",
# "X10": "[0]"
# }
# ```

# ---

# ## Run Sensitivity

# ```python
# result = apply_sensitivity(
#     your_config,
#     0.1,
#     'absolute'
# )
# ```

# Meaning:

# ```
# Perturb each variable by +0.1
# ```

# ---

# ## Display Results

# ```python
# for i, xlist in enumerate(result, start=1):
#     print(f"X{i}: {xlist}")
# ```

# ---

# # Output Structure

# Each parameter becomes a **long vector of simulation cases**.

# Example:

# ```
# X1 = [
# 35.1,35,35,35,35,35,
# 40.1,40,40,40,40,40,
# 55.1,55,55,55,55,55,
# 35,40,55
# ]
# ```

# Interpretation:

# ```
# 6 simulations per operating point
# +
# nominal simulations
# ```

# ---

# # Simulation Count

# If:

# ```
# n_vars = 6
# m = 3
# ```

# Sensitivity cases:

# ```
# 6 × 3 = 18
# ```

# Nominal cases:

# ```
# +3
# ```

# Total simulations:

# ```
# 21
# ```

# ---

# # Computational Complexity

# Time complexity:

# ```
# O(n_vars² × m)
# ```

# Memory complexity:

# ```
# O(n_vars² × m)
# ```

# For typical WCA problems:

# ```
# n_vars ≤ 10
# ```

# Execution is very efficient.

# ---

# # Advantages

# ✔ Automatic detection of active variables
# ✔ Supports multiple operating points
# ✔ Multiple perturbation types
# ✔ Optional nominal simulations
# ✔ Simple integration with simulation pipelines
# ✔ Efficient matrix construction

# ---

# # Typical Integration

# This module is typically used before **simulation sweep generation**.

# ```mermaid
# flowchart LR

# A[Parameter Configuration] --> B[Sensitivity Matrix Generator]
# B --> C[Simulation Sweep Engine]
# C --> D[PLECS / SPICE Simulation]
# D --> E[Results Analysis]
# ```

# ---

# If you'd like, I can also generate a **combined documentation page** for your whole workflow:

# **Sensitivity → Sweep Generator → PLECS Injection → Simulation Results**

# with **full system architecture diagrams (like internal Bosch / BMW simulation frameworks)**.

# Import the JSON module for parsing JSON strings in the configuration
import json
# Import NumPy for numerical operations and matrix manipulations
import numpy as np

import json
import numpy as np

import numpy as np

import numpy as np

import numpy as np
import json

import numpy as np
import json

def generate_sensitivity_masks(nvars, perturbation_value, config_data):
    """
    Generate diagonal perturbation masks and append nominal values as last column.

    Args:
        nvars              : int    Number of active variables (X1..Xnvars)
        perturbation_value : float  Value placed on diagonal
        config_data        : dict   Original config with X1..X10

    Returns:
        list: X1..X10 lists (active = masks + nominal, inactive = unchanged)
    """

    # Step 1: Generate diagonal matrix
    matrix              = np.zeros((nvars, nvars))
    np.fill_diagonal(matrix, perturbation_value)

    # Step 2: Load original Xs (nominals)
    original_Xs         = [json.loads(config_data.get(f"X{i}", "[0]")) for i in range(1, 11)]

    # Extract nominal values for active variables (take first value)
    nominals            = [original_Xs[i][0] for i in range(nvars)]

    # Step 3: Append nominal column
    nominal_column      = np.array(nominals).reshape(-1, 1)
    matrix_with_nominal = np.hstack((matrix, nominal_column))

    # Step 4: Convert to X list format
    active_Xs   = [row.tolist() for row in matrix_with_nominal]

    # Step 5: Merge with inactive
    final_Xs    = []

    for i in range(10):
    
        if i < nvars    :   final_Xs.append(active_Xs[i])
        else            :   final_Xs.append(original_Xs[i])

    return final_Xs

# Example usage with multiple data points
your_config = {
    # X1-X6 are active parameters with multiple data points
    "X1": "[0]",      # First parameter with 2 points
    "X2": "[0]",    # Second parameter with 2 points
    "X3": "[0]",  # Third parameter with 2 points
    "X4": "[0]",    # Fourth parameter with 2 points
    "X5": "[0]",      # Fifth parameter with 2 points
    "X6": "[0]", # Sixth parameter with 2 points
    "X7": "[0]",          # Inactive
    "X8": "[0]",          # Inactive
    "X9": "[0]",          # Inactive
    "X10": "[0]",         # Inactive
    "sweepNames": ["Water Temperature", "Input Voltage", "Output Voltage", 
                   "Output Power", "Test1", "Test2", "X7", "X8", "X9", "X10"]
}




result = generate_sensitivity_masks(6, 0.1, your_config)

for i, xlist in enumerate(result, start=1):
    print(f"X{i}    : {xlist}")




# Here’s a **clean, Confluence-ready documentation page** for your function, including a **Mermaid diagram**, clear structure, and user-facing explanations.

# ---

# # 📊 Sensitivity Mask Generator (Diagonal Perturbation + Nominals)

# ---

# ## 🧭 Overview

# The `generate_sensitivity_masks` function creates a **structured sensitivity input matrix** used for numerical sensitivity analysis and simulation-based Jacobian extraction.

# It generates:

# * A **diagonal perturbation matrix** (ΔX)
# * Appends **nominal values** as the final column
# * Preserves **inactive parameters** unchanged

# This enables workflows such as:

# * Finite-difference sensitivity analysis
# * Automated simulation sweeps
# * Jacobian matrix computation

# ---

# ## 🎯 Purpose

# The function prepares input data in the form:

# ```
# [ ΔX1  ΔX2  ...  ΔXn  |  X_nominal ]
# ```

# Where:

# * Each column represents a **simulation case**
# * First `n` columns → **perturbed variables**
# * Last column → **nominal case**

# ---

# ## ⚙️ Function Definition

# ```python
# def generate_sensitivity_masks(nvars, perturbation_value, config_data):
# ```

# ### Parameters

# | Name                 | Type  | Description                                      |
# | -------------------- | ----- | ------------------------------------------------ |
# | `nvars`              | int   | Number of active variables (X1 → Xnvars)         |
# | `perturbation_value` | float | Value applied to diagonal (ΔX)                   |
# | `config_data`        | dict  | Configuration containing X1..X10 as JSON strings |

# ---

# ## 🔍 How It Works

# ### Step-by-step process

# 1. **Generate diagonal perturbation matrix**

#    * Size: `nvars × nvars`
#    * Diagonal = `perturbation_value`
#    * Off-diagonal = `0`

# 2. **Load nominal values**

#    * Extracted from `config_data`
#    * Uses the **first element** of each Xi list

# 3. **Filter active parameters**

#    * Only parameters ≠ `[0]` are considered active

# 4. **Append nominal column**

#    * Adds nominal values as the **last column**

# 5. **Merge with inactive parameters**

#    * X(nvars+1) → X10 remain unchanged

# ---

# ## 🔄 Workflow Diagram

# ```mermaid
# flowchart TD

# A[Start] --> B[Read config_data X1..X10]
# B --> C[Create zero matrix nvars x nvars]
# C --> D[Fill diagonal with perturbation_value]

# D --> E[Extract nominal values from config]
# E --> F{Any active nominals?}

# F -->|Yes| G[Append nominal column]
# F -->|No| H[Skip append]

# G --> I[Convert matrix to X lists]
# H --> I

# I --> J[Merge with inactive Xs]
# J --> K[Return final X1..X10]

# K --> L[End]
# ```

# ---

# ## 📐 Output Structure

# For `nvars = 3`, output becomes:

# ```
# X1: [Δ, 0, 0, X1_nom]
# X2: [0, Δ, 0, X2_nom]
# X3: [0, 0, Δ, X3_nom]
# ```

# Inactive parameters:

# ```
# X7: [0]
# X8: [0]
# ...
# ```

# ---

# ## 🧪 Example Usage

# ### Input Configuration

# ```python
# your_config = {
#     "X1": "[35]",
#     "X2": "[200]",
#     "X3": "[11.5]",
#     "X4": "[500]",
#     "X5": "[66]",
#     "X6": "[96369]",
#     "X7": "[0]",
#     "X8": "[0]",
#     "X9": "[0]",
#     "X10": "[0]"
# }
# ```

# ---

# ### Function Call

# ```python
# result = generate_sensitivity_masks(6, 0.1, your_config)

# for i, xlist in enumerate(result, start=1):
#     print(f"X{i}: {xlist}")
# ```

# ---

# ### Output

# ```
# X1: [0.1, 0,   0,   0,   0,   0,   35]
# X2: [0,   0.1, 0,   0,   0,   0,   200]
# X3: [0,   0,   0.1, 0,   0,   0,   11.5]
# X4: [0,   0,   0,   0.1, 0,   0,   500]
# X5: [0,   0,   0,   0,   0.1, 0,   66]
# X6: [0,   0,   0,   0,   0,   0.1, 96369]

# X7: [0]
# X8: [0]
# X9: [0]
# X10: [0]
# ```

# ---

# ## 🧠 Interpretation

# | Column      | Meaning                              |
# | ----------- | ------------------------------------ |
# | 1 → nvars   | Each variable perturbed individually |
# | Last column | Nominal (baseline simulation)        |

# ---

# ## 🚀 Typical Use Case

# ### Sensitivity Calculation

# After running simulations:

# ```
# S ≈ (Y_perturbed - Y_nominal) / ΔX
# ```

# ---

# ## ⚡ Notes & Best Practices

# * Ensure all active X lists contain **at least one value**
# * `[0]` is treated as **inactive parameter**
# * Nominal extraction uses **first element only**
# * Matrix size grows as:

#   ```
#   nvars × (nvars + 1)
#   ```

# ---

# ## 🔮 Next Steps

# This function is typically followed by:

# 1. Simulation execution (PLECS / Octave / Python)
# 2. Output collection (Y matrix)
# 3. Sensitivity computation (Jacobian matrix)

# ---

# If you want, I can next generate a **matching Confluence page for the Jacobian computation step** to complete your workflow.

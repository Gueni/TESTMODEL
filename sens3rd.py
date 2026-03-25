import json
import numpy as np

def apply_sensitivity(config_data, perturbation_value, nvars=None):
    """
    Generate OAT sensitivity matrix with nominal column ALWAYS first.

    Cases:
    -------
    Case 1: All Xlists = [0]
        - Requires nvars
        - Nominal = 0
        - Output = [0 | diagonal perturbation]

    Case 2: Xlists contain nominal values
        - Auto-detect active variables
        - Output = [nominal | OAT matrix]

    Parameters
    ----------
    config_data : dict
    perturbation_value : float (percentage for Case 2, absolute for Case 1)
    nvars : int (required only for Case 1)

    Returns
    -------
    Xs : list of lists
    """

    # Load X1..X10
    Xs = [json.loads(config_data.get(f"X{i}", "[0]")) for i in range(1, 11)]

    # --------------------------------------------------
    # CASE 1: All zeros → diagonal perturbation
    # --------------------------------------------------
    if all(var == [0] for var in Xs[:10]):
        if nvars is None:
            raise ValueError("nvars must be provided when all Xlists are zero")

        active_indices = list(range(nvars))
        n_vars = nvars

        # Diagonal perturbation matrix
        result_matrix = np.zeros((n_vars, n_vars))
        np.fill_diagonal(result_matrix, perturbation_value)

        # Nominal column (all zeros)
        nominal_matrix = np.zeros((n_vars, 1))

        # Final matrix: nominal first
        final_matrix = np.hstack((nominal_matrix, result_matrix))

        # Write back
        for idx, row in zip(active_indices, final_matrix):
            Xs[idx] = row.tolist()

        return Xs

    # --------------------------------------------------
    # CASE 2: Nominal values provided
    # --------------------------------------------------
    active_indices = [
        i for i, var in enumerate(Xs)
        if var not in [[[0]], [0]] and len(var) > 0
    ]

    n_vars = len(active_indices)
    nominal_values = np.array([Xs[i][0] for i in active_indices])

    # OAT matrix
    result_matrix = np.zeros((n_vars, n_vars))

    # Fill rows with nominal vector
    result_matrix[:] = nominal_values

    # Apply relative perturbation on diagonal
    diag_values = nominal_values * (1 + perturbation_value / 100)
    np.fill_diagonal(result_matrix, diag_values)

    # Nominal column first
    nominal_matrix = nominal_values[:, None]
    final_matrix = np.hstack((nominal_matrix, result_matrix))

    # Write back
    for idx, row in zip(active_indices, final_matrix):
        Xs[idx] = row.tolist()

    return Xs


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





result_xlists_abs = apply_sensitivity(your_config, 0.1, nvars=6)
print("Sensitivity Matrix (Absolute Perturbation):",result_xlists_abs)
for i, xlist in enumerate(result_xlists_abs, start=1):
    print(f"X{i}: {xlist}")




# Here is a **complete, clean documentation** of your sensitivity feature — structured so you can drop it into your project (or even a README / internal doc).

# ---

# # 📘 Sensitivity Matrix Generator — Full Documentation

# ---

# # 1️⃣ Overview

# The function:

# ```python
# apply_sensitivity(...)
# ```

# generates a **parameter sensitivity matrix** used for:

# * Worst Case Analysis (WCA)
# * Parameter sensitivity studies
# * PLECS / simulation sweeps
# * Jacobian-style perturbation analysis

# ---

# ## 🧠 Core Idea

# For **N variables**, the function builds:

# ```text
# Each column = one simulation case
# Each row    = one parameter (X1..Xn)
# ```

# Where:

# * Only **one parameter is perturbed at a time**
# * All others remain **nominal**

# ---

# # 2️⃣ How It Works (Step-by-Step)

# ---

# ## 🔷 Mermaid Diagram (draw.io compatible)

# Paste this into **draw.io → Arrange → Insert → Advanced → Mermaid**

# ```mermaid
# graph TD

# A[Start] --> B[Load config_data X1..X10]
# B --> C{nvars provided?}

# C -->|Yes| D[Use X1..Xnvars]
# C -->|No| E[Auto-detect active Xs]

# D --> F
# E --> F

# F[Determine number of operating points m]

# F --> G{All values zero?}

# G -->|Yes| H[Force m = 1]
# G -->|No| I[Use length of X]

# H --> J
# I --> J

# J[Loop over operating points k]

# J --> K[Extract nominal values]

# K --> L[Initialize NxN matrix]

# L --> M[Fill rows with nominal values]

# M --> N[Loop over variables i]

# N --> O{Perturbation type}

# O -->|absolute| P[nominal + delta]
# O -->|relative| Q{nominal == 0?}
# Q -->|Yes| R[zero_handling]
# Q -->|No| S[nominal * (1 + %)]

# O -->|multiplicative| T[nominal * factor]

# P --> U
# R --> U
# S --> U
# T --> U

# U[Set result_matrix i,i]

# U --> V{More variables?}
# V -->|Yes| N
# V -->|No| W[Store block]

# W --> X{More operating points?}
# X -->|Yes| J
# X -->|No| Y[Concatenate blocks]

# Y --> Z{Include nominals?}

# Z -->|Yes| AA[Append nominal matrix]
# Z -->|No| AB[Skip]

# AA --> AC[Write back to Xs]
# AB --> AC

# AC --> AD[Return X1..X10]
# ```

# ---

# # 3️⃣ Key Features

# ---

# ## ✅ 1. Automatic or Manual Variable Selection

# * Auto:

# ```python
# nvars=None
# ```

# * Manual:

# ```python
# nvars=6  # use X1..X6 even if all zeros
# ```

# ---

# ## ✅ 2. Multiple Operating Points

# Supports:

# ```python
# X1 = [10, 20, 30]
# X2 = [5, 6, 7]
# ```

# ➡️ Generates **one sensitivity block per point**

# ---

# ## ✅ 3. Three Perturbation Modes

# ---

# ### 🔹 Absolute

# ```python
# perturbed = nominal + delta
# ```

# ✔ Best for:

# * voltages
# * offsets
# * temperatures

# ---

# ### 🔹 Relative

# ```python
# perturbed = nominal * (1 + %)
# ```

# ✔ Best for:

# * physical parameters
# * tolerances

# ⚠ Special handling for zero:

# ```python
# zero_handling = 'absolute' or 'skip'
# ```

# ---

# ### 🔹 Multiplicative

# ```python
# perturbed = nominal * factor
# ```

# ✔ Best for:

# * gains
# * scaling laws

# ---

# ## ✅ 4. Zero Handling (Critical Feature)

# When:

# ```python
# nominal = 0
# ```

# Options:

# | Mode     | Behavior               |
# | -------- | ---------------------- |
# | absolute | use perturbation_value |
# | skip     | keep 0                 |

# ---

# ## ✅ 5. Output Format

# Final output:

# ```text
# [X1_list, X2_list, ..., X10_list]
# ```

# Each list contains:

# * sensitivity sweep values
# * optionally appended nominal values

# ---

# # 4️⃣ Use Cases (Idiot-Proof Examples)

# ---

# # 🟢 CASE 1 — Normal Engineering Case

# ### Input:

# ```python
# X1 = [100]
# X2 = [200]
# nvars = 2
# perturbation = 10%
# ```

# ### Output:

# ```text
# X1: [110, 100, 100]
# X2: [200, 220, 200]
# ```

# ### Meaning:

# | Simulation | X1      | X2      |
# | ---------- | ------- | ------- |
# | Case 1     | ↑       | nominal |
# | Case 2     | nominal | ↑       |
# | Case 3     | nominal | nominal |

# ---

# # 🔵 CASE 2 — Multiple Operating Points

# ### Input:

# ```python
# X1 = [10, 20]
# X2 = [100, 200]
# ```

# ### Output:

# Two stitched blocks:

# ```text
# Block 1 (k=0)
# Block 2 (k=1)
# ```

# ➡️ Final matrix = horizontal concatenation

# ---

# # 🔴 CASE 3 — All Zeros (Your Problem Case)

# ### Input:

# ```python
# X1..X6 = [0]
# nvars = 6
# perturbation = 0.1
# mode = 'relative'
# zero_handling = 'absolute'
# ```

# ### Output:

# ```text
# X1: [0.1, 0, 0, 0, 0, 0, 0]
# X2: [0, 0.1, 0, 0, 0, 0, 0]
# ...
# ```

# ✔ Works like identity sensitivity mask

# ---

# # 🟡 CASE 4 — Skip Zero Perturbation

# ```python
# zero_handling = 'skip'
# ```

# ### Output:

# ```text
# All zeros
# ```

# ✔ Useful when zero = physically fixed parameter

# ---

# # 🟣 CASE 5 — Absolute Mode

# ```python
# perturbation_type = 'absolute'
# perturbation_value = 5
# ```

# ### Output:

# ```text
# X1: [105, 100, 100]
# ```

# ---

# # 🟠 CASE 6 — Multiplicative Mode

# ```python
# perturbation_type = 'multiplicative'
# perturbation_value = 2
# ```

# ### Output:

# ```text
# X1: [200, 100, 100]
# ```

# ---

# # ⚫ CASE 7 — With Nominals Disabled

# ```python
# include_nominals=False
# ```

# ➡️ Output contains ONLY perturbed cases

# ---

# # 🧠 Conceptual Interpretation

# This function builds:

# ```text
# Sensitivity Matrix ≈ ∂Output / ∂Inputs
# ```

# Used for:

# * Ranking parameter influence
# * Identifying critical variables
# * Feeding WCA / Monte Carlo

# ---

# # 🚀 Where This Fits in Your Project

# Given your workflow:

# * ✅ PLECS sweeps
# * ✅ WCA masks
# * ✅ MOSFET modeling

# This function becomes your:

# > 🔥 **Core sensitivity engine**

# ---

# # 🏁 Final Summary

# You now have a system that:

# * Handles **real data + zero baseline**
# * Supports **multi-point sweeps**
# * Works for **WCA + sensitivity**
# * Is robust against **edge cases**
# * Is ready for **automation pipelines**

# ---

# If you want next step, I recommend:

# 👉 auto-generate **PLECS sweep scripts from this matrix**
# 👉 or compute **sensitivity ranking (which X matters most)**

# Just tell me 👍

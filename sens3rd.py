


import json
import numpy as np


def apply_sensitivity(config_data,perturbation_value,perturbation_type='relative',include_nominals=True,nvars=None,zero_handling='absolute'):
    """
    Generate a sensitivity matrix by perturbing each parameter independently.

    This function constructs a matrix where each column represents a simulation case
    in which only one parameter is perturbed while all others remain at their nominal values.
    The matrices for all operating points are horizontally concatenated.

    Parameters
    ----------
    config_data : dict
        Dictionary containing parameters X1..X10 stored as JSON strings.

    perturbation_value : float perturbation magnitude.

    perturbation_type : str, optional
        Type of perturbation:
            - 'absolute'        : nominal + perturbation_value
            - 'relative'        : nominal * (1 + perturbation_value / 100)
            - 'multiplicative'  : nominal * perturbation_value
        Default is 'relative'.

    include_nominals : bool, optional
        If True, append nominal values as additional columns at the end.
        Default is True.

    nvars : int, optional
        Number of active variables (X1..Xnvars).
        If provided, overrides automatic detection.

    zero_handling : str, optional
        Behavior when nominal value is zero in 'relative' mode:
            - 'absolute' → use perturbation_value
            - 'skip'     → keep zero
        Default is 'absolute'.

    Returns
    -------
    list
        Updated list of X1..X10 where active variables contain the sensitivity matrix.
    """

    # --------------------------------------------------
    # Load parameter lists X1..X10 from config (JSON → Python)
    # --------------------------------------------------
    Xs = [json.loads(config_data.get(f"X{i}", "[0]")) for i in range(1, 11)]

    # --------------------------------------------------
    # Determine which variables are active
    # - If nvars is provided → use X1..Xnvars
    # - Otherwise → auto-detect non-zero placeholders
    # --------------------------------------------------
    if nvars is not None:
        active_indices = list(range(nvars))
    else:
        active_indices = [
            i for i, var in enumerate(Xs)
            if var not in [[[0]], [0]] and len(var) > 0
        ]

    # Number of active variables
    n_vars = len(active_indices)

    # First active variable index (used to infer operating points)
    first_active = active_indices[0]

    # --------------------------------------------------
    # Determine number of operating points (m)
    # - If all zeros → force single operating point
    # - Else → use length of parameter vector
    # --------------------------------------------------
    if Xs[first_active] == [0]:
        m = 1
        # Ensure all active variables have consistent length
        for i in active_indices:
            Xs[i] = [0] * m
    else:
        m = len(Xs[first_active])

    # List to store sensitivity blocks for each operating point
    stitched_blocks = []

    # --------------------------------------------------
    # Loop over each operating point
    # --------------------------------------------------
    for k in range(m):

        # Extract nominal values at operating point k
        nominal_values = [Xs[i][k] for i in active_indices]

        # Initialize sensitivity matrix (n_vars × n_vars)
        result_matrix = np.zeros((n_vars, n_vars))

        # --------------------------------------------------
        # Fill each row with nominal values
        # (baseline: all parameters at nominal)
        # --------------------------------------------------
        for i in range(n_vars):
            result_matrix[i, :] = nominal_values[i]

        # --------------------------------------------------
        # Apply perturbation on diagonal (one variable at a time)
        # --------------------------------------------------
        for i in range(n_vars):

            # Current nominal value
            nominal = nominal_values[i]

            # --- Compute perturbed value based on type ---
            if perturbation_type == 'absolute':
                perturbed = nominal + perturbation_value

            elif perturbation_type == 'relative':
                # Special handling for zero nominal
                if nominal == 0:
                    if zero_handling == 'absolute':
                        perturbed = perturbation_value
                    elif zero_handling == 'skip':
                        perturbed = 0
                    else:
                        raise ValueError("Unknown zero_handling mode")
                else:
                    perturbed = nominal * (1 + perturbation_value / 100)

            elif perturbation_type == 'multiplicative':
                perturbed = nominal * perturbation_value

            else:
                raise ValueError("Unknown perturbation type")

            # --------------------------------------------------
            # Update ONLY the diagonal element (critical fix)
            # --------------------------------------------------
            result_matrix[i, i] = perturbed

        # Store this operating point block
        stitched_blocks.append(result_matrix)

    # --------------------------------------------------
    # Concatenate all operating point blocks horizontally
    # --------------------------------------------------
    stitched = np.hstack(stitched_blocks)

    # --------------------------------------------------
    # Optionally append nominal values as final columns
    # --------------------------------------------------
    if include_nominals:
        nominal_matrix = np.array([
            [Xs[i][k] for k in range(m)]
            for i in active_indices
        ])
        final_matrix = np.hstack((stitched, nominal_matrix))
    else:
        final_matrix = stitched

    # --------------------------------------------------
    # Write computed rows back into X1..X10 structure
    # --------------------------------------------------
    for idx, row in zip(active_indices, final_matrix):
        Xs[idx] = row.tolist()

    # Return updated parameter lists
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

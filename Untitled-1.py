# Alright — I’ll give you a **clean, structured documentation pack** exactly like a professional feature doc, with:

# 1. **Overview page**
# 2. **Workflow diagram (Mermaid – Graph TD, draw.io compatible)**
# 3. **Deep technical explanation**
# 4. **Step-by-step execution flow**
# 5. **Full idiot-proof example (input → output)**

# ---

# # 📘 Sensitivity Analysis Feature Documentation

# ---

# # 🧾 1. Overview

# ## What is this feature?

# The **Sensitivity Analysis module** evaluates how much each input parameter affects output signals (RMS, AVG, MAX, MIN, FFT).

# It computes a **normalized sensitivity (%)**:

# * Independent of units
# * Comparable across variables
# * Robust to scaling

# ---

# ## 🎯 Purpose

# * Identify **dominant parameters**
# * Rank variable importance
# * Detect **critical design sensitivities**
# * Support optimization & robustness studies

# ---

# ## 📊 Output

# The system generates:

# * CSV Maps:

#   * `Standalone_RMS_Map.csv`
#   * `Standalone_AVG_Map.csv`
#   * `Standalone_MAX_Map.csv`
#   * `Standalone_MIN_Map.csv`
#   * `Standalone_FFT_Map.csv`

# * Sensitivity Maps:

#   * `*_Sensitivity.csv`

# ---

# ## 📐 Sensitivity Definition

# [
# S = \frac{\Delta Y / Y_0}{\Delta X / X_0} \times 100
# ]

# Where:

# * (Y_0): nominal output
# * (\Delta Y): output variation
# * (\Delta X): input perturbation

# ---

# # 🔷 2. Workflow Diagram (Mermaid - Graph TD)

# Paste this directly into **draw.io (Mermaid import)**:

# ```
# graph TD

# A[Start Simulation] --> B[Load X1..X10 from JSON]

# B --> C{Are all X = 0?}

# C -->|Yes| D[Generate diagonal perturbation matrix]
# C -->|No| E[Extract nominal values]

# D --> F[Build sweep matrix]
# E --> F

# F --> G[Run simulations for each perturbation]

# G --> H[Generate CSV_TIME_SERIES files]

# H --> I[Read CSV files]

# I --> J[Compute RMS, AVG, MAX, MIN]
# I --> K[Compute FFT]

# J --> L[Append results to maps]
# K --> L

# L --> M{Perturbation != 0?}

# M -->|No| N[End]

# M -->|Yes| O[Compute Sensitivity]

# O --> P{FFT Mode?}

# P -->|Yes| Q[Compute harmonic sensitivity]
# P -->|No| R[Compute standard sensitivity]

# Q --> S[Save FFT sensitivity CSV]
# R --> T[Save standard sensitivity CSV]

# S --> U[End]
# T --> U
# ```

# ---

# # ⚙️ 3. How It Works (Deep Explanation)

# ---

# ## 🔹 3.1 Input Parameters

# From JSON:

# * `X1 ... X10` → Parameter sweeps
# * `perturbation` → % variation (e.g. 5%)
# * `FFT` → enable harmonic analysis

# ---

# ## 🔹 3.2 Perturbation Logic

# ### Case 1: No user-defined values

# If all X = `[0]`:

# * System builds:

# ```
# [Nominal | Perturbed Matrix]
# ```

# Example (nvars=3, perturb=5%):

# ```
# [0  5  0  0]
# [0  0  5  0]
# [0  0  0  5]
# ```

# ---

# ### Case 2: Nominal values provided

# Example:

# ```
# X1 = [10]
# X2 = [20]
# ```

# System generates:

# ```
# Nominal column + diagonal perturbation
# ```

# ```
# [10 10.5 10]
# [20 20 21]
# ```

# ---

# ## 🔹 3.3 Simulation Execution

# Each column = **one simulation run**

# * Column 0 → Nominal
# * Column i → Parameter i perturbed

# ---

# ## 🔹 3.4 Signal Processing

# From time-series CSV:

# * RMS
# * AVG
# * MAX
# * MIN
# * FFT (optional)

# ---

# ## 🔹 3.5 Sensitivity Computation

# ### Standard Case

# ```python
# S = ((Y - Y0) / Y0) / perturbation * 100
# ```

# ---

# ### FFT Case

# Computed per harmonic:

# ```python
# S[h] = ((Yh - Y0h) / Y0h) / perturbation * 100
# ```

# ---

# ## ⚠️ Edge Case Handling

# Handled via:

# ```python
# np.errstate(divide='ignore', invalid='ignore')
# np.nan_to_num(..., nan=1e9)
# ```

# Meaning:

# * Division by zero → replaced by `1e9`
# * Infinite sensitivity → capped

# ---

# # 🔁 4. Step-by-Step Execution Flow

# ---

# ## Step 1 — User Input

# User defines:

# * Parameters (`X1..X10`)
# * Perturbation %

# ---

# ## Step 2 — Perturbation Matrix

# Function:

# ```python
# apply_perturbation()
# ```

# Output:

# * Matrix of simulation cases

# ---

# ## Step 3 — Run Simulations

# Each column = one simulation

# Outputs:

# ```
# CSV_TIME_SERIES/*.csv
# ```

# ---

# ## Step 4 — Extract Signals

# Function:

# ```python
# save_csv_maps_standalone()
# ```

# Extract:

# * RMS
# * AVG
# * MAX
# * MIN
# * FFT

# ---

# ## Step 5 — Build Maps

# Saved as:

# ```
# CSV_MAPS/Standalone_*_Map.csv
# ```

# ---

# ## Step 6 — Compute Sensitivity

# Function:

# ```python
# compute_sensitivity()
# ```

# ---

# ## Step 7 — Save Sensitivity Maps

# ```
# Standalone_*_Map_Sensitivity.csv
# ```

# ---

# # 🧪 5. Full Example (Idiot-Proof)

# ---

# ## 🟢 User Input (JSON)

# ```json
# {
#   "X1": "[100]",
#   "X2": "[200]",
#   "X3": "[0]",
#   "perturbation": 5,
#   "FFT": false
# }
# ```

# ---

# ## 🟡 Step 1: Perturbation Matrix

# Generated:

# ```
# X1 → [100, 105, 100]
# X2 → [200, 200, 210]
# ```

# ---

# ## 🔵 Step 2: Simulations

# | Run | X1  | X2  |
# | --- | --- | --- |
# | 0   | 100 | 200 |
# | 1   | 105 | 200 |
# | 2   | 100 | 210 |

# ---

# ## 🟣 Step 3: Results (RMS Example)

# ```
# Y =
# [
#  [10, 20],   ← nominal
#  [11, 21],   ← X1 perturbed
#  [10.5, 23]  ← X2 perturbed
# ]
# ```

# ---

# ## 🔴 Step 4: Sensitivity Calculation

# For X1:

# [
# S = \frac{(11 - 10)/10}{0.05} \times 100 = 20%
# ]

# For X2:

# [
# S = \frac{(23 - 20)/20}{0.05} \times 100 = 30%
# ]

# ---

# ## ⚫ Final Sensitivity Map

# ```
# [20, 5]
# [5, 30]
# ```

# ---

# ## 📁 Generated Files

# ```
# CSV_MAPS/
#  ├── Standalone_RMS_Map.csv
#  ├── Standalone_RMS_Map_Sensitivity.csv
#  ├── Standalone_AVG_Map.csv
#  ├── Standalone_MAX_Map.csv
#  ├── Standalone_MIN_Map.csv
# ```

# ---

# # ✅ Key Takeaways

# * ✔ Fully automated pipeline
# * ✔ Works with time-domain & FFT
# * ✔ Handles numerical issues safely
# * ✔ Scales to multiple parameters
# * ✔ Outputs directly usable in MATLAB / Python

# ---

# # 🚀 If You Want Next

# I can:

# * Turn this into a **PDF doc**
# * Add **formulas + LaTeX derivation page**
# * Add **ranking / dominant variable detection**
# * Clean your code into a **production-ready module**
# * Or build a **visual dashboard for sensitivity**

# Just tell me 👍

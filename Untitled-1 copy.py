Here is a comprehensive documentation page for the sensitivity feature, structured as requested.

---

# Sensitivity Analysis Feature Documentation

## 1. Overview

The Sensitivity Analysis feature quantifies how variations in input parameters affect the simulation outputs. By applying small perturbations to the nominal parameter values and comparing the resulting output changes, the feature generates a **sensitivity matrix**. This matrix indicates the percentage change in each output signal for a 1% change in each input parameter, enabling engineers to identify which parameters have the most significant impact on system performance.

The feature is integrated into the simulation workflow, automatically computing sensitivity matrices for both time-domain metrics (RMS, AVG, MIN, MAX) and frequency-domain (FFT) outputs. The results are saved as CSV files for further analysis and visualization.

---

## 2. Workflow

The diagram below illustrates the complete sensitivity analysis workflow, from simulation setup to the final CSV outputs.

```mermaid
graph TD
    A[Start: Simulation Initialization] --> B{Is Perturbation Enabled?}
    B -- No (Perturbation = 0) --> C[Skip Sensitivity Analysis]
    B -- Yes (Perturbation > 0) --> D[Setup Parameter Sweep]

    subgraph "Iteration Loop"
        D --> E[Iteration 0: Run Nominal Simulation]
        E --> F{More Iterations?}
        F -- Yes --> G[Iteration i: Apply Perturbation to Parameter i-1]
        G --> H[Run Perturbed Simulation]
        H --> I[Collect Output Metrics: RMS, AVG, MIN, MAX, FFT]
        I --> F
        F -- No --> J[All Simulations Complete]
    end

    J --> K{Process Each Output Type}
    
    subgraph "Sensitivity Computation"
        K --> L[Compute ΔY = Y_perturbed - Y_nominal]
        L --> M[Compute Relative Change: ΔY / Y_nominal]
        M --> N[Divide by Perturbation Value]
        N --> O[Multiply by 100 for Percentage]
        O --> P[Handle Edge Cases: NaN, Inf → 1e9]
    end

    P --> Q[Save Sensitivity Matrix to CSV]
    Q --> R[End: Sensitivity Analysis Complete]
```

---

## 3. How It Works: Detailed Explanation

This section breaks down the sensitivity computation into its core components and steps.

### 3.1. Parameter Sweep Setup

The simulation is executed multiple times (iterations) to generate data for sensitivity calculation. The number of iterations equals the number of parameters being analyzed.

- **Iteration 0 (Nominal Run):** The simulation runs with the nominal (baseline) values for all parameters. This serves as the reference point (`Y0`).
- **Iteration i (Perturbed Runs):** For each subsequent iteration `i`, the `i-th` parameter is perturbed by a small, user-defined percentage (e.g., 1%). All other parameters remain at their nominal values. The simulation runs again, producing outputs under this perturbed condition.

This "one-at-a-time" (OAT) approach isolates the effect of each individual parameter.

### 3.2. Output Metric Collection

For each simulation run (nominal and perturbed), the system calculates key output metrics from the time-domain simulation data. The metrics are defined as:

| Metric | Description | Mathematical Definition |
| :--- | :--- | :--- |
| **RMS** | Root Mean Square | $\sqrt{\frac{1}{N}\sum_{n=1}^{N} y_n^2}$ |
| **AVG** | Arithmetic Mean | $\frac{1}{N}\sum_{n=1}^{N} y_n$ |
| **MAX** | Maximum Value | $\max(y_1, y_2, ..., y_N)$ |
| **MIN** | Minimum Value | $\min(y_1, y_2, ..., y_N)$ |
| **FFT** | Fast Fourier Transform Harmonics | Amplitude of the selected harmonic frequencies. |

### 3.3. Sensitivity Matrix Calculation

The `compute_sensitivity` method is the core engine for this feature. It calculates the sensitivity matrix `S` based on the collected outputs `Y`. The computation differs slightly for time-domain metrics (RMS, AVG, etc.) and frequency-domain FFT results.

#### Standard Case (Time-Domain Metrics)

This case applies to `RMS`, `AVG`, `MIN`, and `MAX`.

1.  **Extract Reference:** `Y0` is the output from the nominal simulation (iteration 0).
2.  **Calculate Output Variation:** `dY = Y[iter] - Y0`. This is the absolute change in the output for the perturbed run.
3.  **Compute Relative Sensitivity:** The formula is applied element-wise:
    $$S = \left( \frac{dY}{Y0} \right) / \text{perturbation} \times 100$$
    - `dY / Y0` gives the relative change in the output.
    - Dividing by `perturbation` normalizes the result to a 1% change in the input.
    - Multiplying by 100 converts it to a percentage.
4.  **Error Handling:** The calculation can produce `NaN` (if `Y0` is 0) or `inf` (if `dY` is infinite). These are replaced with a large number (`1e9`) to indicate a near-infinite sensitivity, which is a clear warning for the user.

#### FFT Case (Frequency-Domain)

FFT outputs are multi-dimensional: each harmonic for each output signal.

1.  **Reshape Data:** `Y` is structured with shape `(n_harmonics * n_iterations, n_signals)`. The first `n_harmonics` rows represent the nominal FFT data.
2.  **Iterate per Harmonic:** The calculation loops through each harmonic `h`:
    - `Y0` = `Y[h, :]` (nominal amplitude for harmonic `h`).
    - `dY` = `Y[iter * n_harmonics + h, :] - Y0` (amplitude change for harmonic `h` in the perturbed run).
    - The sensitivity for that harmonic is then computed using the same core formula as above.
3.  **Output Structure:** The final sensitivity matrix `S` has the shape `(n_harmonics, n_signals)`, where each row corresponds to a harmonic, and each column to an output signal.

### 3.4. CSV Output Generation

After the sensitivity matrix `S` is computed, it is saved to a CSV file. The file naming convention depends on the output type:

- `Standalone_RMS_Map_Sensitivity.csv`
- `Standalone_AVG_Map_Sensitivity.csv`
- `Standalone_MAX_Map_Sensitivity.csv`
- `Standalone_MIN_Map_Sensitivity.csv`
- `Standalone_FFT_Map_Sensitivity.csv`

The CSV file is structured as follows:

- **Rows:** Correspond to the perturbed parameters (one row per parameter). For FFT, rows are grouped by parameter and then by harmonic.
- **Columns:** Correspond to the simulation output signals.

This format allows for easy import into spreadsheet software or data analysis tools for further processing and visualization.

---

## 4. Example Usage: A Step-by-Step Guide

This section provides a complete, step-by-step example of how a user would set up and run a simulation to leverage the sensitivity analysis feature.

### Scenario
We are analyzing a simple DC-DC converter model with **2 input parameters** (`R_load` and `L`) and we are interested in how changes to these parameters affect **1 output signal** (the output voltage). We will use the **RMS** output metric.

### Step 1: User Input (Configuration)

The user defines the simulation and sensitivity analysis parameters. This is typically done through a configuration file (e.g., JSON) or a user interface.

```json
{
  "model": "DCDC",
  "perturbation": 1.0,
  "FFT": false,
  "X1": [100],   // Nominal value for R_load (Ohms)
  "X2": [1e-3],  // Nominal value for L (Henries)
  "X3": [0],
  "X4": [0],
  "X5": [0],
  "X6": [0],
  "X7": [0],
  "X8": [0],
  "X9": [0],
  "X10": [0]
}
```

**Key Inputs Explained:**
- **`model`:** Specifies the simulation model to run.
- **`perturbation`:** The perturbation size (1.0 means a 1% change).
- **`FFT`:** Set to `false` to only compute RMS, AVG, MIN, MAX.
- **`X1`, `X2`:** The nominal values for the parameters. Only `X1` and `X2` are non-zero, so they will be the only ones perturbed.
- `X3` through `X10` are set to `[0]`, indicating they are not part of this analysis.

### Step 2: Simulation Execution (Automatic)

The simulation engine processes the user's input and executes the following iterations:

- **Iteration 0 (Nominal):**
    - `R_load` = 100 Ω, `L` = 1 mH
    - Simulation runs → Output RMS Voltage = `Y0` = 5.0 V

- **Iteration 1 (Perturb `R_load`):**
    - `R_load` = 100 Ω * (1 + 1.0/100) = 101 Ω, `L` = 1 mH
    - Simulation runs → Output RMS Voltage = `Y_pert1` = 4.95 V

- **Iteration 2 (Perturb `L`):**
    - `R_load` = 100 Ω, `L` = 1 mH * (1 + 1.0/100) = 1.01 mH
    - Simulation runs → Output RMS Voltage = `Y_pert2` = 5.02 V

### Step 3: Sensitivity Computation (Automatic)

The `compute_sensitivity` method is called by `save_csv_maps_standalone` for the RMS results (`k = "RMS"`, `nharmonics=None`).

The collected outputs `Y` would look like:
`Y = [ [5.0], [4.95], [5.02] ]`

For iteration 1 (perturbing `R_load`):
- `Y0 = 5.0`
- `dY = 4.95 - 5.0 = -0.05`
- `(dY / Y0) = -0.05 / 5.0 = -0.01`
- `S = (-0.01 / 1.0) * 100 = -1.0`

For iteration 2 (perturbing `L`):
- `Y0 = 5.0`
- `dY = 5.02 - 5.0 = 0.02`
- `(dY / Y0) = 0.02 / 5.0 = 0.004`
- `S = (0.004 / 1.0) * 100 = 0.4`

### Step 4: Results Output

The final sensitivity matrix `S` is saved to a CSV file.

**File:** `CSV_MAPS/Standalone_RMS_Map_Sensitivity.csv`

**Content:**
```csv
-1.0
0.4
```

### Step 5: Interpreting the Results

The user opens the CSV file. The results are easy to interpret:

- **Row 1:** The output RMS voltage changes by **-1.0%** for a 1% increase in `R_load`. This indicates a negative sensitivity; increasing the load resistance decreases the RMS voltage.
- **Row 2:** The output RMS voltage changes by **+0.4%** for a 1% increase in `L`. This indicates a positive, but less significant, sensitivity.

Based on this analysis, the user can conclude that the output voltage is more sensitive to changes in the load resistance than to changes in the inductance. This insight is invaluable for design optimization, component selection, and identifying potential stability issues.
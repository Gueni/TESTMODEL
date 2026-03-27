### 🧠 Compute Sensitivity — Short Explanation

The `compute_sensitivity` function evaluates how strongly each output changes relative to a small perturbation applied to inputs. It first extracts the **nominal output** (Y_0) (iteration 0), then computes the variation (\Delta Y = Y - Y_0) for a given iteration. The sensitivity is calculated as a normalized percentage:

[
S = \left(\frac{\Delta Y}{Y_0}\right) \div \text{perturbation} \times 100
]

This effectively approximates the derivative (\frac{\partial Y}{\partial X}) in a dimensionless way. In FFT mode, the same computation is applied **per harmonic**. Numerical issues like division by zero or invalid values are handled using NumPy safeguards, replacing them with large sentinel values (e.g., (1e9)) to keep the matrix usable. Finally, the sensitivity matrix is appended to a CSV file.



graph TD

A[Start compute_sensitivity] --> B[Convert Y to numpy array]

B --> C{iter equals 0}

C -->|Yes| D[Return]
C -->|No| E{nharmonics is None}

E -->|Yes| F[Set Y0 as first row]
F --> G[Compute dY equals Y at iter minus Y0]
G --> H[Compute S equals dY divided by Y0 divided by perturbation times 100]

E -->|No| I[Extract Y0 for each harmonic]
I --> J[Loop over harmonics]
J --> K[Compute dY for each harmonic]
K --> L[Compute S for each harmonic]

H --> M[Replace NaN and Inf values]
L --> M

M --> N[Append S to CSV file]

N --> O[End]

S = \left(\frac{Y - Y_0}{Y_0}\right) \cdot \frac{100}{\text{perturbation}}
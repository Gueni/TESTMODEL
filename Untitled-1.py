### 🧠 Compute Sensitivity — Short Explanation

The `compute_sensitivity` function evaluates how strongly each output changes relative to a small perturbation applied to inputs. It first extracts the **nominal output** (Y_0) (iteration 0), then computes the variation (\Delta Y = Y - Y_0) for a given iteration. The sensitivity is calculated as a normalized percentage:

[
S = \left(\frac{\Delta Y}{Y_0}\right) \div \text{perturbation} \times 100
]

This effectively approximates the derivative (\frac{\partial Y}{\partial X}) in a dimensionless way. In FFT mode, the same computation is applied **per harmonic**. Numerical issues like division by zero or invalid values are handled using NumPy safeguards, replacing them with large sentinel values (e.g., (1e9)) to keep the matrix usable. Finally, the sensitivity matrix is appended to a CSV file.

---

### 🔷 Graph TD Flowchart (Diagram.io / Mermaid Compatible)

```mermaid
graph TD

A[Start compute_sensitivity] --> B[Convert Y to numpy array]

B --> C{iter == 0?}
C -->|Yes| D[Return without computation]
C -->|No| E{FFT mode?}

E -->|No| F[Extract nominal Y0 = Y[0]]
F --> G[Compute dY = Y[iter] - Y0]
G --> H[Compute S = ((dY / Y0) / perturbation) * 100]

E -->|Yes| I[Extract Y0 per harmonic]
I --> J[Loop over harmonics]

J --> K[Compute dY per harmonic]
K --> L[Compute S[h] = ((dY / Y0) / perturbation) * 100]

H --> M[Handle NaN / Inf using nan_to_num]
L --> M

M --> N[Append S to CSV file]

N --> O[End]
```

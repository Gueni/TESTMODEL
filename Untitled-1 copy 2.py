### 🧠 `save_csv_maps_standalone` — Short Explanation

The `save_csv_maps_standalone` function processes all `_Standalone.csv` time-series files, extracts key signal metrics (RMS, AVG, MAX, MIN, and optionally FFT), and builds structured result maps. For each file, signals are read and transformed into scalar outputs (or harmonic vectors for FFT). These results are accumulated and saved into CSV map files. If a nonzero perturbation is defined, the function then calls the sensitivity computation, which evaluates:

[
S = \left(\frac{Y - Y_0}{Y_0}\right) \div \text{perturbation} \times 100
]

(or per harmonic in FFT mode). This creates corresponding sensitivity maps aligned with each metric.

---

### 🔷 Graph TD Flowchart — draw.io Compatible

```mermaid id="7k2d9p"
graph TD

A[Start save_csv_maps_standalone] --> B[Set CSV_TIME_SERIES and CSV_MAPS paths]

B --> C[Get standalone CSV files]

C --> D{Files exist}

D -->|No| E[Return]
D -->|Yes| F[Initialize results structure]

F --> G[Loop over each file]

G --> H[Read CSV file]
H --> I[Extract time vector and signals]

I --> J[Compute RMS AVG MAX MIN]
I --> K[Compute FFT]

J --> L[Append results]
K --> L

L --> M[End loop]

M --> N[Save results to CSV_MAPS]

N --> O{Perturbation not zero}

O -->|No| P[End]
O -->|Yes| Q{FFT enabled and key is FFT}

Q -->|Yes| R[Call compute_sensitivity with harmonics]
Q -->|No| S[Call compute_sensitivity standard]

R --> T[End]
S --> T
```

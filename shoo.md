# WCA (Worst Case Analysis) Feature Documentation

## Overview

The Worst Case Analysis (WCA) feature allows you to analyze how component tolerances affect your circuit's performance by simulating extreme combinations of parameter variations. 

## How it Works


The WCA algorithm is based on binary encoding of parameter states:

1. **Binary Representation**: Each parameter's state is represented by a single bit
   - Bit = 0 → Parameter at lower tolerance limit (minimum value)
   - Bit = 1 → Parameter at upper tolerance limit (maximum value)

2. **Combination Generation**: For n parameters with tolerances, we generate:
   - **2ⁿ worst-case combinations**: All possible permutations of min/max values
   - **1 nominal combination**: All parameters at their nominal values
   - **Total simulations**: 2ⁿ + 1

3. **Example with 3 parameters**:
```
Binary    Parameter States
000  →  [min, min, min]
001  →  [min, min, max]
010  →  [min, max, min]
011  →  [min, max, max]
100  →  [max, min, min]
101  →  [max, min, max]
110  →  [max, max, min]
111  →  [max, max, max]
---  →  [nom, nom, nom]  (nominal case)
```

### Tolerance Types

The WCA feature supports two types of tolerances:

#### 1. Absolute Tolerance (tol ≤ 1)
When tolerance value is less than or equal to 1, it's treated as an absolute multiplier:
- **Upper limit (max)**: nominal × tol
- **Lower limit (min)**: nominal / tol

**Example**: nominal = 100, tol = 0.1 (10% absolute)
- Upper value = 100 × 0.1 = 110
- Lower value = 100 / 0.1 = 90

#### 2. Relative Tolerance (tol > 1)
When tolerance value is greater than 1, it's treated as a relative percentage:
- **Upper limit (max)**: nominal × (1 + tol)
- **Lower limit (min)**: nominal × (1 - tol)

**Example**: nominal = 100, tol = 0.2 (20% relative)
- Upper value = 100 × (1 + 0.2) = 120
- Lower value = 100 × (1 - 0.2) = 80

### Parameter Format Options

The WCA feature provides two ways to specify parameters:

#### Option 1: Bounded WCA (with min/max limits)
```
[nominal, tolerance, min_value, max_value]
```
The calculated tolerance value is clamped within the specified bounds:
- If calculated value < min_value → use min_value
- If calculated value > max_value → use max_value
- Otherwise → use calculated value

**Use case**: When you have physical constraints (e.g., resistance can't be negative, voltage can't exceed breakdown limits)

#### Option 2: Unbounded WCA (no limits)
```
[nominal, tolerance]
```
The calculated value can extend to any value based on the tolerance formula.

**Use case**: When you want to see the theoretical extremes without artificial constraints

## Step 1: Configure Your JSON Input File

The JSON input file is where you define all your WCA parameters. Here's an extremely detailed explanation of each field and how to configure it properly.

### Complete JSON Structure

```json
{

  "X1"                : "[[1.0    , 0.3    , 1.0    , 1.3    ] , [1.0    , 0.2    , 1.0    , 1.2    ] , [1.0    , 0.2    , 1.0    , 1.2    ] , [1.0    , 0.3    , 1.0    , 1.3    ] ]",
  "X2"                : "[[1.7    , 0.3529 , 1.7    , 2.3    ] , [1.8    , 0.1111 , 1.8    , 2.0    ] , [1.8    , 0.1111 , 1.8    , 2.0    ] , [1.7    , 0.3529 , 1.7    , 2.3    ] ]",
  "X3"                : "[[58.6   , 0.7065 , 58.6   , 100    ] , [21.6   , 0.3889 , 21.6   , 30     ] , [21.6   , 0.3889 , 21.6   , 30     ] , [58.6   , 0.7065 , 58.6   , 100    ] ]",
  "X4"                : "[[3.0    , 0.2667 , 3.0    , 3.8    ] , [4.3    , 0.3023 , 4.3    , 5.6    ] , [4.3    , 0.3023 , 4.3    , 5.6    ] , [1.5    , 1.0    , 1.5    , 3.0    ] ]",
  "X5"                : "[[16.6   , 0.3    , 11.62  , 21.58  ] , [1.10   , 0.3    , 0.77   , 1.43   ] , [1.10   , 0.3    , 0.77   , 1.43   ] , [24.0   , 0.3    , 16.8   , 31.2   ] ]",
  "X6"                : "[[1.0    , 0.06   , 0.94   , 1.06   ] , [10.0   , 0.06   , 9.4    , 10.6   ] , [10.0   , 0.06   , 9.4    , 10.6   ] , [1.0    , 0.06   , 0.94   , 1.06   ] ]",
  "X7"                : "[[3.9    , 0.06   , 3.666  , 4.134  ] , [10.0   , 0.06   , 9.4    , 10.6   ] , [10.0   , 0.06   , 9.4    , 10.6   ] , [1.0    , 0.06   , 0.94   , 1.06   ] ]",
  "X8"                : "[[1.5    , 3.3333 , 1.5    , 5.0    ] , [0.55   , 0.3    , 0.385  , 0.715  ] , [0.55   , 0.3    , 0.385  , 0.715  ] , [1.5    , 3.3333 , 1.5    , 5.0    ] ]",
  "X9"                : "[[2.5    , 2.8    , 2.5    , 7.0    ] , [1.13   , 0.3    , 0.791  , 1.469  ] , [1.13   , 0.3    , 0.791  , 1.469  ] , [2.5    , 2.8    , 2.5    , 7.0    ] ]",
  "X10"               : "[[0]]",
  
  "sweepNames"        : ["Vth_l", "Vth_h", "Td", "Vth", "Cg", "Rg_OFF", "Rg_ON", "Rg_l", "Rg_h", "X10"]
}
```


### Understanding WCA Iterations

For our example with 8 active parameters (X1, X2, X3, X4, X6, X7, X8, X9):

- Number of active parameters (n) = 8
- Total WCA iterations = 2ⁿ + 1 = 2⁸ + 1 = 256 + 1 = 257 simulations

The iterations are organized as:

```
Iteration 0:   [min, min, min, min, min, min, min, min]  (binary 00000000)
Iteration 1:   [min, min, min, min, min, min, min, max]  (binary 00000001)
Iteration 2:   [min, min, min, min, min, min, max, min]  (binary 00000010)
Iteration 3:   [min, min, min, min, min, min, max, max]  (binary 00000011)
...
Iteration 254: [max, max, max, max, max, max, max, min]  (binary 11111110)
Iteration 255: [max, max, max, max, max, max, max, max]  (binary 11111111)
Iteration 256: [nom, nom, nom, nom, nom, nom, nom, nom]  (nominal case)
```















# WCA Code Architecture and Function Flow Diagram

Here's a comprehensive diagram showing how the WCA functions work together in the code:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          WCA CODE ARCHITECTURE FLOW                         │
└─────────────────────────────────────────────────────────────────────────────┘

USER INPUT (JSON)
{
  "X1": "[[1.0,0.3,1.0,1.3], [1.0,0.2,1.0,1.2], ...]",
  "X2": "[[1.7,0.3529,1.7,2.3], [1.8,0.1111,1.8,2.0], ...]",
  ...
  "sweepNames": ["Vth_l", "Vth_h", "Td", "Vth", ...]
}
                │
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INITIALIZATION PHASE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  sim_utils.init_sim(X1, X2, ..., X10, model='DCDC')                        │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────┐                                                       │
│  │ detect_mode()   │◄──────────────────┐                                   │
│  │                 │                    │                                   │
│  │ Checks each Xi  │                    │                                   │
│  │ for WCA format: │                    │                                   │
│  │ • If sub list   │                    │                                   │
│  │   length = 4 → WCA                    │                                   │
│  │ • If length = 1 → NORMAL              │                                   │
│  │ • Returns "WCA" or "NORMAL"           │                                   │
│  └────────┬────────┘                    │                                   │
│           │                              │                                   │
│           ▼ (mode = "WCA")                │                                   │
│  ┌─────────────────┐                    │                                   │
│  │ get_active_wca_ │                    │                                   │
│  │   params()      │                    │                                   │
│  │                 │                    │                                   │
│  │ Returns list of │                    │                                   │
│  │ indices where   │                    │                                   │
│  │ len(sub[0]) = 4 │                    │                                   │
│  │ e.g., [0,1,2,3,4,5,6,7,8] for 9 active│                                   │
│  └────────┬────────┘                    │                                   │
│           │                              │                                   │
│           ▼                              │                                   │
│  ┌─────────────────┐                    │                                   │
│  │ findIndex()     │                    │                                   │
│  │                 │                    │                                   │
│  │ If startPoint   │                    │                                   │
│  │ provided:       │                    │                                   │
│  │ • Compare with  │                    │                                   │
│  │   nominal values│                    │                                   │
│  │ • Loop through  │                    │                                   │
│  │   WCA iterations│                    │                                   │
│  │   using         │                    │                                   │
│  │   calculate_wca_│                    │                                   │
│  │   values()      │                    │                                   │
│  │ • Return [iter],│                    │                                   │
│  │   linear_index  │                    │                                   │
│  └────────┬────────┘                    │                                   │
│           │                              │                                   │
│           ▼                              │                                   │
│  ┌─────────────────┐                    │                                   │
│  │ findPoint()     │                    │                                   │
│  │                 │                    │                                   │
│  │ Generates all   │                    │                                   │
│  │ WCA iterations: │                    │                                   │
│  │ • For iter_num  │                    │                                   │
│  │   in range(total)│                   │                                   │
│  │   └─► calculate_│                   │                                   │
│  │       wca_values│                   │                                   │
│  │       (iter_num)│                   │                                   │
│  │                 │                    │                                   │
│  │ Returns: Map,   │                    │                                   │
│  │ Iterations      │                    │                                   │
│  └────────┬────────┘                    │                                   │
│           │                              │                                   │
│           ▼                              │                                   │
│  ┌─────────────────────────────────────┐│                                   │
│  │      WCA CORE FUNCTIONS LOOP        ││                                   │
│  └─────────────────────────────────────┘│                                   │
└──────────────────────────────────────────┴──────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WCA CORE FUNCTIONS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    calculate_wca_values()                            │   │
│  │                                                                       │   │
│  │  Input: iteration (int), Xs (list of 10 parameters)                  │   │
│  │  Output: 3D list of calculated WCA values                             │   │
│  │                                                                       │   │
│  │  For each Xi in Xs:                                                   │   │
│  │      For each sublist in Xi:                                          │   │
│  │          CASE len(sub) == 1:                                          │   │
│  │              result = sub[0]  # Fixed value                           │   │
│  │                                                                       │   │
│  │          CASE len(sub) == 2:  # NEW: Unbounded WCA                    │   │
│  │              nom, tol = sub                                           │   │
│  │              tol_type = (tol <= 1)  # True=Absolute, False=Relative  │   │
│  │              result = funtol(tol_type, iteration, i, nom, tol)       │   │
│  │              # No clamping (unbounded)                                │   │
│  │                                                                       │   │
│  │          CASE len(sub) == 4:  # Bounded WCA                           │   │
│  │              nom, tol, mn, mx = sub                                   │   │
│  │              tol_type = (tol <= 1)                                    │   │
│  │              x = funtol(tol_type, iteration, i, nom, tol)            │   │
│  │              result = min(max(x, mn), mx)  # Clamp within bounds     │   │
│  │                                                                       │   │
│  │      Append result to wca_vals                                        │   │
│  │      Append wca_vals to results                                       │   │
│  │                                                                       │   │
│  │  return results                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      funtol()                                        │   │
│  │                                                                       │   │
│  │  Input: Abs_rel (bool), iteration (int), index (int),               │   │
│  │         nom (float), tol (float)                                     │   │
│  │  Output: Tolerance-adjusted value                                    │   │
│  │                                                                       │   │
│  │  active = get_active_wca_params()  # Get active indices              │   │
│  │  bit = binary_index(iteration, index, active)                        │   │
│  │                                                                       │   │
│  │  if bit == 1:  # Upper tolerance                                     │   │
│  │      if Abs_rel:  # Absolute                                         │   │
│  │          return nom * tol                                            │   │
│  │      else:  # Relative                                               │   │
│  │          return nom * (1 + tol)                                      │   │
│  │  else:  # bit == 0, Lower tolerance                                  │   │
│  │      if Abs_rel:  # Absolute                                         │   │
│  │          return nom / tol                                            │   │
│  │      else:  # Relative                                               │   │
│  │          return nom * (1 - tol)                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    binary_index()                                    │   │
│  │                                                                       │   │
│  │  Input: iteration (int), index (int), active (list)                 │   │
│  │  Output: bit value (0 or 1)                                          │   │
│  │                                                                       │   │
│  │  # Find position of this index in active list                        │   │
│  │  active_index = active.index(index)                                  │   │
│  │  n_active = len(active)                                              │   │
│  │                                                                       │   │
│  │  # Reverse bit significance (MSB = first parameter)                  │   │
│  │  bit_position = n_active - 1 - active_index                          │   │
│  │                                                                       │   │
│  │  # Extract the bit                                                    │   │
│  │  return (iteration >> bit_position) & 1                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     WCA ITERATION GENERATION EXAMPLE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Active Parameters: [X1, X2, X3, X4, X6, X7, X8, X9] (8 parameters)        │
│  Total Iterations: 2^8 + 1 = 257                                           │
│                                                                             │
│  ┌───────────┬───────────┬───────────┬───────────┬───────────┬─────────┐  │
│  │ Iteration │ Binary    │ X1  │ X2  │ X3  │ X4  │ ... │ X9  │ Type    │  │
│  ├───────────┼───────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────────┤  │
│  │ 0         │ 00000000  │ min │ min │ min │ min │ ... │ min │ Worst   │  │
│  │ 1         │ 00000001  │ min │ min │ min │ min │ ... │ max │ Worst   │  │
│  │ 2         │ 00000010  │ min │ min │ min │ min │ ... │ min │ Worst   │  │
│  │ 3         │ 00000011  │ min │ min │ min │ min │ ... │ max │ Worst   │  │
│  │ ...       │ ...       │ ... │ ... │ ... │ ... │ ... │ ... │ ...     │  │
│  │ 254       │ 11111110  │ max │ max │ max │ max │ ... │ min │ Worst   │  │
│  │ 255       │ 11111111  │ max │ max │ max │ max │ ... │ max │ Worst   │  │
│  │ 256       │ Nominal   │ nom │ nom │ nom │ nom │ ... │ nom │ Nominal │  │
│  └───────────┴───────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SIMULATION EXECUTION PHASE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  simScript(OptStruct, Thread, Map, iterNumber, ResultsPath, misc)         │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  # Extract values for current iteration                               │   │
│  │  mapVars = Map[iterNumber]                                           │   │
│  │                                                                       │   │
│  │  # Define indices                                                     │   │
│  │  X1, X2, X3, X4, X5, X6, X7, X8, X9, X10 = range(10)                 │   │
│  │                                                                       │   │
│  │  # Assign values (handling nested lists)                              │   │
│  │  if isinstance(mapVars[X1], list):                                    │   │
│  │      mdlVars['Common']['Thermal']['Twater'] = mapVars[X1][0]         │   │
│  │  else:                                                                │   │
│  │      mdlVars['Common']['Thermal']['Twater'] = mapVars[X1]            │   │
│  │                                                                       │   │
│  │  # Similar for other parameters...                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      POST-PROCESSING PHASE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  save_data(optstruct, simutil, fileLog, itr, saveMode, crash)             │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  for l in range(simutil.Threads):                                   │   │
│  │      # Load results                                                   │   │
│  │      results = postProcessing.gen_result(...)                        │   │
│  │                                                                       │   │
│  │      # Calculate metrics using operation()                           │   │
│  │      # MAT1: Peak Currents (mode=1)                                  │   │
│  │      # MAT2: RMS Currents (mode=4)                                   │   │
│  │      # MAT3: AVG Currents (mode=5)                                   │   │
│  │      # MAT4: Peak Voltages (mode=3)                                  │   │
│  │      # MAT5: RMS Voltages (mode=4)                                   │   │
│  │      # MAT6: AVG Voltages (mode=5)                                   │   │
│  │                                                                       │   │
│  │      # FFT calculations (MAT7, MAT8)                                 │   │
│  │      # Dissipations (MAT9)                                           │   │
│  │      # Thermal stats (MAT12)                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Function Call Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     CALL HIERARCHY                               │
├─────────────────────────────────────────────────────────────────┤

MAIN SCRIPT
    │
    ├──► sim_utils.init_sim()
    │       │
    │       ├──► detect_mode() ──► Returns "WCA" or "NORMAL"
    │       │
    │       ├──► get_active_wca_params() ──► [indices of WCA params]
    │       │
    │       ├──► findIndex()  (if startPoint provided)
    │       │       │
    │       │       └──► calculate_wca_values()
    │       │               │
    │       │               └──► funtol()
    │       │                       │
    │       │                       └──► binary_index()
    │       │
    │       └──► findPoint()
    │               │
    │               └──► calculate_wca_values() (for each iteration)
    │                       │
    │                       └──► funtol()
    │                               │
    │                               └──► binary_index()
    │
    │
SIMULATION LOOP (for each iteration)
    │
    ├──► simScript()
    │       │
    │       └──► Extract values from Map[iterNumber]
    │            and assign to model variables
    │
    │
POST-PROCESSING
    │
    └──► sim_utils.save_data()
            │
            ├──► postProcessing.gen_result()
            │
            ├──► sim_utils.operation()  (for MAT1-MAT6)
            │       │
            │       └──► postProcessing.rms_avg() (for modes 4,5)
            │
            ├──► postProcessing.FFT_mat()  (for MAT7, MAT8)
            │
            ├──► postProcessing.dissipations()  (MAT9)
            │
            └──► postProcessing.therm_stats()  (MAT12)

└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   JSON   │────►│   X_vars  │────►│   init_  │────►│   WCA    │
│   File   │     │  (lists)  │     │   sim()  │     │   Map    │
└──────────┘     └──────────┘     └──────────┘     └────┬─────┘
                                                         │
                                                         ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Results │◄────│   save_   │◄────│   sim_   │◄────│  Map[iter]│
│  Files   │     │   data()  │     │  Script()│     │          │
└──────────┘     └────┬─────┘     └──────────┘     └──────────┘
                      │
                      ▼
              ┌──────────────┐
              │ MAT1-MAT13   │
              │ Data Matrices│
              └──────────────┘
```

## Key Function Descriptions

| Function | Purpose | Key Logic |
|----------|---------|-----------|
| `detect_mode()` | Determines if WCA or normal mode | Checks if any sublist has length 4 |
| `get_active_wca_params()` | Identifies which parameters are active | Returns indices where len(sub[0]) == 4 |
| `binary_index()` | Extracts bit for a parameter at given iteration | `(iteration >> (n_active-1-index)) & 1` |
| `funtol()` | Calculates tolerance value | Uses bit to decide min/max, applies absolute/relative |
| `calculate_wca_values()` | Generates all values for one iteration | Loops through all parameters and sublists |
| `findIndex()` | Finds starting index in parameter space | Compares with nominal or iterates through WCA combos |
| `findPoint()` | Generates all parameter combinations | Creates 2ⁿ + 1 WCA combinations |
| `operation()` | Calculates metrics from time-series data | Mode-based: peak, RMS, average, etc. |

This architecture allows the WCA feature to efficiently generate and simulate all worst-case combinations while handling both bounded and unbounded tolerance specifications.

























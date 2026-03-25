import numpy as np

def compute_sensitivity(Y, X):
    """
    Compute normalized OAT (One-At-a-Time) sensitivity matrix.

    This function assumes:
    - Each iteration perturbs ONLY one variable
    - The LAST row in Y and X is the nominal (reference) case

    Sensitivity formula used:
        S = (dY / dX) * (X0 / Y0)

    Where:
        dY = Y_iter - Y_nominal
        dX = X_iter - X_nominal
        X0 = nominal value of perturbed variable
        Y0 = nominal output

    Parameters:
    -----------
    Y : ndarray of shape (n_iter+1, n_signals)
        Output matrix (e.g., RMS values)
        Last row = nominal values

    X : ndarray of shape (n_iter+1, n_vars)
        Input variables matrix
        Last row = nominal values

    Returns:
    --------
    S : ndarray of shape (n_iter, n_signals)
        Sensitivity matrix:
        - Each row = one perturbation (one variable)
        - Each column = one signal
    """

    # --- Nominal ---
    Y0 = Y[-1]   # (n_signals,)
    X0 = X[-1]   # (n_vars,)

    # --- Iterations ---
    Y_iter = Y[:-1]
    X_iter = X[:-1]

    # --- Output variation ---
    dY = Y_iter - Y0   # (n_iter, n_signals)

    # --- Compute perturbation per iteration ---
    # perturb = (X_iter - X0) / X0
    dX = X_iter - X0
    perturb = np.sum(dX / X0, axis=1)   # (n_iter,)

    # --- Sensitivity (% form) ---
    S = (dY / Y0[None, :]) / perturb[:, None] * 100

    # --- Save (pandas) ---
    import pandas as pd
    import os

    save_path = os.path.join(r'D:\WORKSPACE\TESTMODEL\CSVMAPS', 'curr_S_MAP.csv')
    pd.DataFrame(S).to_csv(save_path, index=False, header=False)

    return S


# --- Example RMS data (6 perturbations + 1 nominal) ---
Y = np.array([
    [1.9120, 1.9530, 1.9230],
    [1.9125, 1.9500, 1.9220],
    [1.9130, 1.9550, 1.9250],
    [1.9128, 1.9540, 1.9240],
    [1.9127, 1.9535, 1.9235],
    [1.9126, 1.9532, 1.9233],
    [1.9124, 1.9528, 1.9229]  # Nominal row
])

# --- Input matrix: each row perturbs one variable ---
Xlists = [
    [9.0,     100e-6, 220e-6, 100e3, 400.0, 0.05, 25.0],   # R_load ↓
    [10.0,     90e-6, 220e-6, 100e3, 400.0, 0.05, 25.0],   # L ↓
    [10.0,    100e-6, 198e-6, 100e3, 400.0, 0.05, 25.0],   # C ↓
    [10.0,    100e-6, 220e-6,  90e3, 400.0, 0.05, 25.0],   # fsw ↓
    [10.0,    100e-6, 220e-6, 100e3, 360.0, 0.05, 25.0],   # Vin ↓
    [10.0,    100e-6, 220e-6, 100e3, 400.0, 0.045,25.0],   # Rds_on ↓

    [10.0,    100e-6, 220e-6, 100e3, 400.0, 0.05, 25.0]    # Nominal
]

# Convert to NumPy array
X = np.array(Xlists)

# --- Compute sensitivity ---
S = compute_sensitivity(Y, X)

# --- Display results ---
print("Sensitivity matrix shape:", S.shape)
print(S)
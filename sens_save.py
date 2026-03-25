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

    # --- Extract nominal values (last row) ---
    Y0 = Y[-1]   # Nominal outputs → shape (n_signals,)
    X0 = X[-1]   # Nominal inputs  → shape (n_vars,)

    # --- Remove nominal row → keep only perturbation runs ---
    Y_iter = Y[:-1]   # Shape: (n_iter, n_signals)
    X_iter = X[:-1]   # Shape: (n_iter, n_vars)

    # --- Compute differences relative to nominal ---
    dY = Y_iter - Y0   # Change in outputs → (n_iter, n_signals)
    dX = X_iter - X0   # Change in inputs  → (n_iter, n_vars)

    # --- Each row has only ONE perturbed variable ---
    # Sum across variables → gives the scalar perturbation per iteration
    dX_scalar = np.sum(dX, axis=1)   # Shape: (n_iter,)

    # --- Identify which variable was perturbed using a mask ---
    # (dX != 0) → True only for the perturbed variable
    # Multiply by X0 to extract the nominal value of that variable
    X0_scalar = np.sum((dX != 0) * X0, axis=1)   # Shape: (n_iter,)

    # --- Compute normalized sensitivity ---
    # dY / dX → slope (finite difference)
    # X0 / Y0 → normalization factor
    #
    # Broadcasting:
    # dX_scalar[:, None] → (n_iter, 1)
    # Y0[None, :]        → (1, n_signals)
    S = (dY / dX_scalar[:, None]) * (X0_scalar[:, None] / Y0[None, :])

    # --- Save result using pandas ---
    import pandas as pd
    import os

    # Define output file path
    save_path = os.path.join(r'D:\WORKSPACE\TESTMODEL\CSVMAPS', 'curr_S_MAP.csv')

    # Convert to DataFrame (optional but cleaner for CSV handling)
    df = pd.DataFrame(S)

    # Save without index and header (pure numeric matrix)
    df.to_csv(save_path, index=False, header=False)

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
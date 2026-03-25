import numpy as np

import numpy as np
import pandas as pd
import os

def compute_sensitivity(Y, X, perturb=0.1):
    """
    Compute normalized OAT (One-At-a-Time) sensitivity matrix.

    Assumes:
    - The FIRST row in Y and X is the nominal (reference) case
    - Each subsequent row perturbs ONE variable

    Sensitivity formula (percentage form):
        S = ((Y_iter - Y_nom) / Y_nom) / perturb * 100

    Parameters:
    -----------
    Y : ndarray (n_iter+1, n_signals)
        Output matrix (RMS, etc.)
        First row = nominal

    X : ndarray (n_iter+1, n_vars)
        Input variables matrix
        First row = nominal

    perturb : float
        Relative perturbation applied to each variable (fraction, e.g. 0.1 = 10%)

    Returns:
    --------
    S : ndarray (n_iter, n_signals)
        Sensitivity matrix
        Each row = one perturbed iteration
        Each column = one signal
    """

    # --- Nominal values (first row) ---
    Y0 = Y[0]   # (n_signals,)

    # --- Iterations (exclude nominal) ---
    Y_iter = Y[1:]   # (n_iter, n_signals)

    # --- Output difference ---
    dY = Y_iter - Y0  # (n_iter, n_signals)

    # --- Sensitivity (% form) ---
    S = (dY / Y0[None, :]) / perturb * 100

    # --- Save CSV ---
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

]

# Convert to NumPy array
X = np.array(Xlists)

# --- Compute sensitivity ---
S = compute_sensitivity(Y, X)

# --- Display results ---
print("Sensitivity matrix shape:", S.shape)
print(S)


import numpy as np
import pandas as pd
import os

def compute_sensitivity(Y, X, perturb=0.1, nharmonics=None):
    """
    Compute normalized OAT (One-At-a-Time) sensitivity matrix.

    Parameters
    ----------
    Y : ndarray
        Output matrix (RMS, FFT, etc.).
        First row(s) = nominal (for RMS) or first nharmonics rows = nominal for FFT.
    X : ndarray
        Input variables matrix.
        First row = nominal.
    perturb : float
        Relative perturbation applied to each variable (fraction, e.g., 0.1 = 10%)
    nharmonics : int or None
        Number of harmonics if Y is FFT. If None, RMS logic is used.

    Returns
    -------
    S : ndarray
        Sensitivity matrix (% form)
    """
    if nharmonics is None:
        # --- RMS case ---
        Y0 = Y[0]
        Y_iter = Y[1:]
        dY = Y_iter - Y0
        S = (dY / Y0[None, :]) / perturb * 100
    else:
        # --- FFT case ---
        n_iter = (Y.shape[0] - nharmonics) // nharmonics
        n_signals = Y.shape[1]
        S = np.zeros((n_iter * nharmonics, n_signals))

        # Nominal rows for each harmonic
        Y0 = Y[:nharmonics, :]

        for i in range(n_iter):
            for h in range(nharmonics):
                idx = nharmonics + i * nharmonics + h  # current perturbed row
                S[i * nharmonics + h, :] = ((Y[idx, :] - Y0[h, :]) / Y0[h, :]) / perturb * 100

    # --- Save CSV ---
    save_path = os.path.join(r'D:\WORKSPACE\TESTMODEL\CSVMAPS', 'curr_S_MAP.csv')
    pd.DataFrame(S).to_csv(save_path, index=False, header=False)

    return S
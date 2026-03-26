import numpy as np
import pandas as pd
import os

def compute_sensitivity(Y, X, perturb=0.1, nharmonics=None, save_path=None):
    """
    Compute normalized OAT (One-At-a-Time) sensitivity matrix, with shape checks.

    Parameters
    ----------
    Y : ndarray (n_rows, n_signals)
        Output matrix (RMS, FFT, etc.)
        - RMS: first row = nominal, remaining rows = perturbed iterations
        - FFT: first nharmonics rows = nominal harmonics, then nharmonics rows per iteration

    X : ndarray (n_rows, n_vars)
        Input matrix
        - First row = nominal
        - Must have exactly the same number of iterations as Y

    perturb : float
        Relative perturbation fraction (e.g., 0.1 = 10%)

    nharmonics : int or None
        If None → RMS mode
        If int → FFT mode with this many harmonics per iteration

    save_path : str or None
        CSV path to save sensitivity matrix

    Returns
    -------
    S : ndarray
        Sensitivity matrix
        - RMS: shape = (n_iter, n_signals)
        - FFT: shape = (n_iter * nharmonics, n_signals)
    """

    Y = np.array(Y)
    X = np.array(X)
    
    # ----------------------------
    # RMS / Standard case
    # ----------------------------
    if nharmonics is None:
        n_iter = Y.shape[0] - 1  # exclude nominal
        if X.shape[0] != n_iter + 1:
            raise ValueError(f"X rows ({X.shape[0]}) do not match Y rows ({Y.shape[0]}) for RMS mode")
        
        Y_nom = Y[0, :]
        Y_iter = Y[1:, :]
        dY = Y_iter - Y_nom[None, :]
        with np.errstate(divide='ignore', invalid='ignore'):
            S = (dY / Y_nom[None, :]) / perturb * 100
            S = np.nan_to_num(S, nan=0.0, posinf=0.0, neginf=0.0)

    # ----------------------------
    # FFT case
    # ----------------------------
    else:
        nh = nharmonics
        n_total_rows = Y.shape[0]
        n_signals = Y.shape[1]
        n_iter = (n_total_rows - nh) // nh
        expected_Y_rows = nh + n_iter * nh
        if n_total_rows != expected_Y_rows:
            raise ValueError(f"Y rows ({n_total_rows}) inconsistent with nharmonics={nh} and iterations={n_iter}")
        if X.shape[0] != n_iter + 1:
            raise ValueError(f"X rows ({X.shape[0]}) inconsistent with number of FFT iterations ({n_iter})")

        # Initialize sensitivity
        S = np.zeros((n_iter * nh, n_signals))
        Y_nom = Y[:nh, :]  # first nh rows = nominal harmonics

        # Compute sensitivity per harmonic per iteration
        for i in range(n_iter):
            for h in range(nh):
                idx_Y = nh + i*nh + h
                idx_S = i*nh + h
                dY = Y[idx_Y, :] - Y_nom[h, :]
                with np.errstate(divide='ignore', invalid='ignore'):
                    S[idx_S, :] = (dY / Y_nom[h, :]) / perturb * 100
                    S[idx_S, :] = np.nan_to_num(S[idx_S, :], nan=0.0, posinf=0.0, neginf=0.0)

    # ----------------------------
    # Save CSV
    # ----------------------------
    if save_path is None:
        save_path = os.path.join(r'D:\WORKSPACE\TESTMODEL', 'curr_S_MAP.csv')
    pd.DataFrame(S).to_csv(save_path, index=False, header=False)

    return S


# RMS example
Y_rms = np.random.rand(3, 6)  # 1 nominal + 6 perturb
X_rms = np.random.rand(3, 3)
S_rms = compute_sensitivity(Y_rms, X_rms, perturb=0.1)

# FFT example


print(S_rms)  # (6, 3)
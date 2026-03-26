from blinker import signal
import numpy as np
import pandas as pd
import os

from scipy.fftpack import fft

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







# example fft file structure: for harmonic = 2 and 1 nominal + 7 iterations, Y shape = (2 + 6*2, n_signals) = (14, n_signals)
#                 signal 1  signal 2  signal 3
# iteration 0     value1    value2    value3
#                 value4    value5    value6

# iteration 1     value7    value8    value9
#                 value10   value11   value12

# iteration 2     value13   value14   value15
#                 value16   value17   value18

# iteration 3     value19   value20   value21
#                 value22   value23   value24

# iteration 4     value25   value26   value27 
#                 value28   value29   value30

# iteration 5     value31   value32   value33
#                 value34   value35   value36

# iteration 6     value37   value38   value39
#                 value40   value41   value42

# iteration 7     value43   value44   value45
#                 value46   value47   value48 



# the resulting sensitivity matrix S would have shape (6*2, n_signals) = (12, n_signals), where each row corresponds to the sensitivity of a specific harmonic for a specific iteration.

# iteration 1     value7    value8    value9
#                 value10   value11   value12

# iteration 2     value13   value14   value15
#                 value16   value17   value18

# iteration 3     value19   value20   value21
#                 value22   value23   value24

# iteration 4     value25   value26   value27 
#                 value28   value29   value30

# iteration 5     value31   value32   value33
#                 value34   value35   value36

# iteration 6     value37   value38   value39
#                 value40   value41   value42

# iteration 7     value43   value44   value45
#                 value46   value47   value48



import numpy as np
import pandas as pd
import os

def compute_sensitivity(Y, X, current_iter, perturb=0.1, nharmonics=None, save_path=None):
    """
    Compute sensitivity incrementally during simulation loop.

    Rules:
    - iter == 0 → nominal → do nothing
    - iter > 0 → compute sensitivity using available data

    Parameters
    ----------
    Y : ndarray
        Accumulated outputs up to current iteration

    X : ndarray
        Input matrix (not used here but kept for consistency)

    current_iter : int
        Current iteration index in the loop

    perturb : float
        Relative perturbation (e.g. 0.1 = 10%)

    nharmonics : int or None
        None → RMS
        int → FFT mode

    save_path : str
        Where to save CSV
    """

    # -----------------------------------
    # Skip nominal iteration
    # -----------------------------------
    if current_iter == 0:
        return  # nothing to compute

    Y = np.array(Y)

    # -----------------------------------
    # RMS CASE
    # -----------------------------------
    if nharmonics is None:

        Y_nom = Y[0, :]           # first row = nominal
        Y_iter = Y[1:, :]         # all computed iterations so far

        dY = Y_iter - Y_nom[None, :]

        with np.errstate(divide='ignore', invalid='ignore'):
            S = (dY / Y_nom[None, :]) / perturb * 100
            S = np.nan_to_num(S, nan=0.0, posinf=0.0, neginf=0.0)

    # -----------------------------------
    # FFT CASE
    # -----------------------------------
    else:
        nh = nharmonics
        n_rows, n_signals = Y.shape

        # Number of completed iterations so far
        n_iterations_total = n_rows // nh

        if n_iterations_total <= 1:
            return  # still only nominal

        n_iter = n_iterations_total - 1

        Y_nom = Y[0:nh, :]  # first block

        S = np.zeros((n_iter * nh, n_signals))

        for i in range(1, n_iterations_total):  # skip iteration 0
            for h in range(nh):
                idx_Y = i * nh + h
                idx_S = (i - 1) * nh + h

                dY = Y[idx_Y, :] - Y_nom[h, :]

                with np.errstate(divide='ignore', invalid='ignore'):
                    S[idx_S, :] = (dY / Y_nom[h, :]) / perturb * 100
                    S[idx_S, :] = np.nan_to_num(S[idx_S, :], nan=0.0, posinf=0.0, neginf=0.0)

    # -----------------------------------
    # Save
    # -----------------------------------
    if save_path is None:
        save_path = os.path.join(r'D:\WORKSPACE\TESTMODEL', 'curr_S_MAP.csv')

    pd.DataFrame(S).to_csv(save_path, index=False, header=False)
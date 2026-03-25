import os
import numpy as np


def compute_sensitivity_from_csvmaps(csv_folder, Xlists, output_folder=None):
   

    if output_folder is None:
        output_folder = os.path.join(csv_folder, "SENSITIVITY")
    os.makedirs(output_folder, exist_ok=True)

    # Convert Xlists → (n_iter, n_vars)
    X = np.array(Xlists).T

    results = {}

    for file in os.listdir(csv_folder):

        # Only RMS files
        if "RMS" not in file or not file.endswith(".csv"):
            continue

        filepath = os.path.join(csv_folder, file)

        # Load Y
        Y = np.loadtxt(filepath, delimiter=",")

        # --- Sanity check ---
        if Y.shape[0] != X.shape[0]:
            raise ValueError(f"{file}: mismatch (Y rows != X rows)")

        # --- Nominal (last row) ---
        Y0 = Y[-1]   # (n_signals,)
        X0 = X[-1]   # (n_vars,)

        # --- Differences ---
        dY = Y[:-1] - Y0   # (runs, signals)
        dX = X[:-1] - X0   # (runs, vars)

        eps = 1e-12

        # Expand dims
        dY_exp = dY[:, :, None]   # (runs, signals, 1)
        dX_exp = dX[:, None, :]   # (runs, 1, vars)

        # --- Sensitivity (finite difference, NOT gradient) ---
        S = np.where(
            np.abs(dX_exp) > eps,
            dY_exp / dX_exp * (X0[None, None, :] / (Y0[None, :, None] + eps)),
            0.0
        )
        
        # --- Collapse runs ---
        S_mean = np.mean(S, axis=0)   # (signals × variables)

        # --- Save ---
        base = file.replace(".csv", "")

        np.savetxt(os.path.join(output_folder, base + "_S_Y_by_X.csv"),
                   S_mean, delimiter=",")

        results[file] = {
            "S_yx": S_mean,  # (signals × variables)
        }

    for name, data in results.items():
        S = data["S_yx"]
        importance = np.sum(np.abs(S), axis=0)

        print("\nRanking for", name)
        print(np.argsort(-importance))
        dominant = np.argmax(np.abs(S), axis=1)
        print("Dominant variable per signal:", dominant)

    return results





Xlists  =   [[0.1,1.0,1.0,1.0,1.0,1.0 ,1], 
             [1.0, 0.1,1.0,1.0,1.0,1.0,1], 
             [1.0,1.0, 0.1,1.0,1.0,1.0,1], 
             [1.0,1.0,1.0, 0.1,1.0,1.0,1], 
             [1.0,1.0,1.0,1.0, 0.1,1.0,1], 
             [1.0,1.0,1.0,1.0,1.0, 0.1,1]]

# -----------------------------------
# Step 2 — Run PLECS manually / script
# → generates CSVs in "CSVMAPS"
# -----------------------------------

# -----------------------------------
# Step 3 — Compute sensitivity matrices
# -----------------------------------
results = compute_sensitivity_from_csvmaps(
    csv_folder=r"D:\WORKSPACE\TESTMODEL\this\2sensitivity\CSVMAPS",
    Xlists=Xlists
)

# -----------------------------------
# Step 4 — Access results
# -----------------------------------
for name, data in results.items():
    print("\nFile:", name)
    print("S_yx shape:", data["S_yx"].shape)
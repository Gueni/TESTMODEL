

# lambda for normal sweepmatrix and for sensitivity sweepmatrix with nominals
from collections import OrderedDict

to_dict = lambda Xs: OrderedDict((f"X{i+1}", v) for i, v in enumerate(Xs))

Xs = [[35,2,3,6,5],[45,50],[55,60],[65,70],[75,80],[85],[95],[0],[0],[0]]

result = to_dict(Xs)
print(result)

#-----------------------------------------------------------------------------
import numpy as np
def pad_all_top_with_nan(matrices, N=1):
    padded_matrices = []
    max_rows = max(np.atleast_2d(mat).shape[0] for mat in matrices)
    
    for mat in matrices:
        mat = np.atleast_2d(mat)  # convert 1D to 2D row
        rows, cols = mat.shape
        pad_rows = N * (max_rows - rows)
        if pad_rows > 0:
            pad = np.full((pad_rows, cols), np.nan)
            mat_padded = np.vstack([pad, mat])
        else:
            mat_padded = mat
        padded_matrices.append(mat_padded)
        
    return padded_matrices
A = np.array([[1, 2],
              [3, 4],
              [5, 6]])

B = np.array([[10, 20]])

C = np.array([[100,200],
              [300,400]])

matrices = [A, B, C]

padded = pad_all_top_with_nan(matrices, N=1)
result = np.hstack(padded)
print(result)
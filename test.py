

# lambda for normal sweepmatrix and for sensitivity sweepmatrix with nominals
from collections import OrderedDict

to_dict = lambda Xs: OrderedDict((f"X{i+1}", v) for i, v in enumerate(Xs))

Xs = [[35,2,3,6,5],[45,50],[55,60],[65,70],[75,80],[85],[95],[0],[0],[0]]

result = to_dict(Xs)
print(result)

#-----------------------------------------------------------------------------
import numpy as np
import numpy as np

pad_top = lambda X, target_rows: np.vstack([np.full((target_rows - X.shape[0], X.shape[1]), np.nan), X])
A = np.array([[1, 2], [3, 4], [5, 6]])
B = np.array([[10, 20]])  # fewer rows

B_padded = pad_top(B, target_rows=A.shape[0])
print(B_padded)
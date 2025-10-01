import numpy as np

# Suppose MAT1 ... MAT10 already exist
combined = np.hstack([globals()[f"MAT{i}"] for i in range(1, 11)])

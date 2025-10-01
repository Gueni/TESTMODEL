


# --- Example usage ---
# Mock matrices
mat_dict = {f"MAT{i}": np.random.rand(5, i) for i in range(1, 14)}  # rows=5, cols=i


import numpy as np

# Example: all MAT1-MAT13 stored in a dictionary
mat_dict = {f"MAT{i}": getattr(simutils, f"MAT{i}") for i in range(1, 14)}

# Custom order for non-FFT matrices
custom_order = ['MAT6', 'MAT3', 'MAT1', 'MAT12']

# Separate FFT and non-FFT names
fft_names = ['MAT7', 'MAT8']
nonfft_names = [name for name in custom_order if name not in fft_names]

# Combine matrices
combined_nonfft = np.hstack([mat_dict[name] for name in nonfft_names])
combined_fft    = np.hstack([mat_dict[name] for name in fft_names])

# Optional: combine both into one final matrix (FFT first, then others)
combined_final  = np.hstack([combined_fft, combined_nonfft])




import numpy as np

# Dictionary of MAT1–MAT13
mat_dict = {f"MAT{i}": np.array(getattr(simutils, f"MAT{i}")).T for i in range(1, 14)}

# Custom order for non-FFT
custom_order = ['MAT6', 'MAT3', 'MAT1', 'MAT12']

# Separate FFT and non-FFT
fft_names = ['MAT7', 'MAT8']
nonfft_names = [name for name in custom_order if name not in fft_names]

# Combine
combined_nonfft = np.hstack([mat_dict[name] for name in nonfft_names])
combined_fft    = np.hstack([mat_dict[name] for name in fft_names])

# Final (FFT first, then others)
combined_final  = np.hstack([combined_fft, combined_nonfft])

print(combined_nonfft.shape, combined_fft.shape, combined_final.shape)

# Non-FFT matrices
excluded = [6, 7]  # zero-based indices for MAT7, MAT8
combined_matrix = np.hstack([simutil.MAT_list[i] for i in range(13) if i not in excluded])

# FFT matrices
fft_indices = [6, 7]  # MAT7, MAT8
combined_fft_matrix = np.hstack([simutil.MAT_list[i] for i in fft_indices])

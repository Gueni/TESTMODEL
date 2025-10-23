# Adjust the raw mapping by removing specific ranges
arr = dp.np.array(DCDC_pmap_Raw)

# --- Delete 62 elements starting at Ycumsum[2] (original first delete)
start_1 = Ycumsum[2]
end_1   = start_1 + dp.Y_Length[9]
arr = dp.np.delete(arr, dp.np.r_[start_1:end_1])

# --- Delete 8 elements counting from the end (original second delete)
start_2 = len(arr) - (dp.Y_list[-1] + 1)
end_2   = start_2 + dp.Y_Length[12]
arr = dp.np.delete(arr, dp.np.r_[start_2:end_2])

# Convert back to list for compatibility
DCDC_pmap_Raw = arr.tolist()

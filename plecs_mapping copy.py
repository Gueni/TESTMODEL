arr = dp.np.array(DCDC_pmap_Raw)
n = len(arr)
start = n - (dp.Y_list[-1] + 1)
end = start + dp.Y_Length[12]
DCDC_pmap_Raw = dp.np.delete(arr, dp.np.r_[start:end]).tolist()

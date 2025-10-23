delete_segments = lambda arr, seglen, segdel: np.delete(
    np.array(arr),
    np.hstack([np.r_[np.cumsum([0]+seglen[:-1])[i] : np.cumsum([0]+seglen[:-1])[i] + seglen[i]] for i in segdel])
).tolist()

segments = [1, 77, 69, 62, 15, 18, 8, 148]
DCDC_pmap_Raw = list(range(sum(segments)))  # [0..397]

DCDC_pmap_Raw = delete_segments(DCDC_pmap_Raw, segments, [3, 6])
print(len(DCDC_pmap_Raw))  # → 328 ✅

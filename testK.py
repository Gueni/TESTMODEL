def parse_indices(indices_str):
    cleaned = indices_str.strip("[]").replace(",", " ")
    tokens = cleaned.split()
    indices = []
    for token in tokens:
        if ":" in token:
            start, end = token.split(":")
            indices.extend(range(int(start), int(end) + 1))
        else:
            indices.append(int(token))
    return indices

def update_signal_selector(indices_str, rail, n_signals=36, exclude=[]):
    indices = parse_indices(indices_str)
    
    new_indices = []
    for i in indices:
        if i in exclude:
            continue  # common signal, skip for Rail 2
        # how many excluded signals are before i → shifts position in Rail 2
        shift = sum(1 for e in exclude if e < i)
        new_indices.append(n_signals + (i - shift) + (rail - 2) * (n_signals - len(exclude)))
    
    combined = indices + new_indices
    print("[" + " ".join(str(i) for i in combined) + "]")

# Example: signal 7 is common
update_signal_selector("[5 7 10]", rail=2, n_signals=36, exclude=[7])
# [5 7 10 41 45]
# 5 → 36 + (5-0) = 41
# 7 → skipped (common)
# 10 → 36 + (10-1) = 45
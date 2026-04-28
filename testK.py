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

def update_selector(indices_str, n_signals=3, exclude=[]):
    indices = parse_indices(indices_str)
    
    new_indices = []
    for i in indices:
        if i in exclude:
            continue  # common signal, no Rail 2 copy
        shift = sum(1 for e in exclude if e < i)
        new_indices.append(n_signals + i - shift)
    
    combined = indices + new_indices
    print("[" + " ".join(str(i) for i in combined) + "]")

# Usage - just paste your selector output each time
update_selector("[1 2 3]")
# [1 2 3 7 8 9]
update_selector("[1 2 3]", exclude=[2])
# [1 2 3 7 8]
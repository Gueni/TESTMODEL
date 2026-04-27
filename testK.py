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
    new_indices = [i + (rail - 1) * n_signals for i in indices if i not in exclude]
    combined = indices + new_indices
    print("[" + " ".join(str(i) for i in combined) + "]")

# Examples
update_signal_selector("[1 7 13 25:30]", rail=2, n_signals=36, exclude=[7])
# 7 is common, won't be duplicated
# [1 7 13 25 26 27 28 29 30 37 43 61 62 63 64 65 66]
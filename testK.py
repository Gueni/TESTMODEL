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

def update_signal_selector(indices_str, rail, n_signals=36):
    indices = parse_indices(indices_str)
    new_indices = [i + (rail - 1) * n_signals for i in indices]
    combined = indices + new_indices
    print("[" + " ".join(str(i) for i in combined) + "]")

# Examples
update_signal_selector("[1 7 13]", rail=2, n_signals=36)
# [1 7 13 37 43 49]

update_signal_selector("[25:36]", rail=2, n_signals=36)
# [25 26 27 28 29 30 31 32 33 34 35 36 61 62 63 64 65 66 67 68 69 70 71 72]

update_signal_selector("[1 7 25:30 36]", rail=2, n_signals=36)
# [1 7 25 26 27 28 29 30 36 37 43 61 62 63 64 65 66 67 72]
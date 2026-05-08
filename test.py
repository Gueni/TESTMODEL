Here's a function that scans the folder and builds both lists dynamically while preserving your order:

```python
import os

def get_mat_lists_from_folder(folder_path):
    """
    Scans folder for Standalone_* files and builds mat_names + mat_suffix
    in the canonical order, skipping any that don't exist.
    """
    # Define canonical order (base suffixes first, then _Sens variants)
    canonical_order = ['RMS', 'AVG', 'MAX', 'MIN', 'FFT',
                       'RMS_Sens', 'AVG_Sens', 'MAX_Sens', 'MIN_Sens', 'FFT_Sens']

    # Collect all Standalone_* filenames (strip extensions)
    existing = set()
    for f in os.listdir(folder_path):
        name, _ = os.path.splitext(f)          # e.g. "Standalone_FFT"
        if name.startswith("Standalone_"):
            suffix = name[len("Standalone_"):]  # e.g. "FFT"
            existing.add(suffix)

    # Build lists in canonical order, only for what exists
    mat_suffix = [s for s in canonical_order if s in existing]
    mat_names  = [f"Standalone_{s}" for s in mat_suffix]

    return mat_names, mat_suffix
```

Then replace your hardcoded blocks with:

```python
mat_names, mat_suffix = get_mat_lists_from_folder(your_folder_path)

# d and N can still be derived if you need them
has_sens = any("Sens" in s for s in mat_suffix)
d = 8 if has_sens else 4
N = 2 if has_sens else 1
```

**How it works:**
- Lists all files in the folder, strips extensions, and checks if the name starts with `Standalone_`
- Extracts the suffix part (e.g. `FFT`, `RMS_Sens`) and adds it to a set
- Rebuilds both lists by filtering the canonical order against that set — so the order is always guaranteed regardless of filesystem ordering
- FFT (or any other variant) is simply skipped if absent
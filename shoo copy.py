import os
import glob

def Open_Model(self, modelname):
    """
    Searches recursively for a .plecs model file and opens it.
    Skips excluded top-level folders for speed.
    """

    root_dir = os.getcwd()

    # 🔹 Top-level folders to exclude
    excluded_folders = [
        "build",
        "archive",
        "old_versions",
        "__pycache__"
    ]

    # Normalize model name
    if not modelname.lower().endswith(".plecs"):
        modelname += ".plecs"
    modelname = modelname.lower()

    # 🔹 Build allowed top-level paths (root included)
    allowed_dirs = [
        os.path.join(root_dir, d)
        for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d)) and d not in excluded_folders
    ] + [root_dir]  # include root itself

    # 🔹 Build glob patterns for all allowed folders
    patterns = [os.path.join(d, "**", "*.plecs") for d in allowed_dirs]

    # 🔹 Flatten all matches into one list without loops
    all_matches = sum((glob.glob(p, recursive=True) for p in patterns), [])

    # 🔹 Case-insensitive filter
    model_path = next(
        (p for p in all_matches if os.path.basename(p).lower() == modelname),
        None
    )

    if model_path:
        dp.cp_mdl = model_path
        os.startfile(model_path)
        print(f"Opened model: {model_path}")
    else:
        print("Check the model name please.")
        os._exit(0)
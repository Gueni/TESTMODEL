import os
import glob

def Open_Model(self, modelname):
    """
    Searches recursively for a .plecs model file and opens it.

    Args:
        modelname (str): Name of the PLECS model file (with or without .plecs)
    """

    root_dir = os.getcwd()

    # 🔹 Folders to exclude (populate as needed)
    excluded_folders = [
        "build",
        "archive",
        "old_versions",
        "__pycache__"
    ]

    # Normalize model name (case-insensitive)
    if not modelname.lower().endswith(".plecs"):
        modelname += ".plecs"

    modelname = modelname.lower()

    # 🔹 Single-pass search + filter + match
    model_path = next(
        (
            path for path in glob.iglob(os.path.join(root_dir, "**", "*.plecs"), recursive=True)
            if os.path.basename(path).lower() == modelname
            and not any(f"{os.sep}{excluded}{os.sep}" in path for excluded in excluded_folders)
        ),
        None
    )

    if model_path:
        dp.cp_mdl = model_path
        os.startfile(model_path)
        print(f"Opened model: {model_path}")
    else:
        print("Check the model name please.")
        os._exit(0)
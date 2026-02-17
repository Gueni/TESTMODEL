def copyfiles(self):
    """Copy all required files to the result folder."""
    cwd = dp.os.getcwd().replace("\\", "/")
    
    # Base files to copy: (source, destination)
    files_to_copy = [
        (dp.cp_mdl, f"PLECS_MODEL_{dp.cp_mdl.split('\\')[-1]}"),
        (dp.script_path, f"{self.basename}.py"),
        (f"{cwd}/Script/{dp.Runscript_path}", "Runscript.py"),
        (self.LogFile, self.LogF_name),
        (f"{cwd}/Script/assets/scripts.js", "HTML_REPORTS/scripts.js"),
        (f"{cwd}/Script/assets/Input_vars.json", "Input_vars.json"),
        (f"{cwd}/Script/assets/Param_Dicts.py", "Param_Dicts.py"),
        (f"{cwd}/Script/assets/plecs_mapping.py", "plecs_mapping.py"),
        (f"{cwd}/Script/assets/InitializationCommands.m", "InitializationCommands.m"),
    ]
    
    # Add ScriptBody.py if in parallel mode
    if dp.JSON.get('parallel'):
        files_to_copy.append((f"{cwd}/Script/{dp.ScriptBody_path}", "ScriptBody.py"))
    
    # Directories to copy: (source, destination)
    dirs_to_copy = [
        (f"{cwd}/MyLibraries", "PLECS_Lib"),
        (f"{cwd}/Script/assets/HEADER_FILES", "HEADER_FILES"),
    ]
    
    # Copy all files
    for src, dst in files_to_copy:
        dp.shutil.copy(src, os.path.join(self.resultfolder, dst))
    
    # Copy all directories
    for src, dst in dirs_to_copy:
        try:
            dp.shutil.copytree(src, os.path.join(self.resultfolder, dst))
        except FileExistsError:
            pass
    
    # Copy signal mapping based on config
    config = dp.JSON.get('TF_Config')
    if config:
        try:
            src = f"{cwd}/Script/assets/SIGNAL_MAPPING/{config}"
            dp.shutil.copytree(src, os.path.join(self.resultfolder, f"SIGNAL_MAPPING/{config}"))
        except FileNotFoundError:
            pass
    
    # Copy timestamped files
    dp.shutil.copy(f"{cwd}/Script/assets/Input_vars.json", 
                  os.path.join(self.jsonfolder, f"Input_vars_{self.utc}.json"))
    dp.shutil.copy(f"{cwd}/Script/assets/InitializationCommands.m", 
                  os.path.join(self.initfolder, f"InitializationCommands_{self.utc}.m"))
    
    # Fix headers
    self.fix_json_strings(os.path.join(self.resultfolder, "HEADER_FILES"))
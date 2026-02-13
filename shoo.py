def create_folders(self):
    """Create all necessary folders and return paths."""
    try:
        # Create results folder structure
        dp.os.makedirs(self.resultfolder, exist_ok=False)

        [dp.os.makedirs(self.resultfolder + sf, exist_ok=False) for sf in ["/HTML_REPORTS", "/HTML_GRAPHS", "/CSV_MAPS", "/CSV_TIME_SERIES", "/Scopes_Traces"]]
        
        # Create other folders
        [dp.os.makedirs(f, exist_ok=True) for f in [self.logfolder, self.jsonfolder, self.initfolder]]  
   
    except OSError:
        pass
    
    # Set paths
    self.ResultsPath = f"{self.resultfolder}/CSV_TIME_SERIES/results_{self.utc}_"
    self.LogFile = f"{self.logfolder}/log_{self.utc}.log"
    
    return self.ResultsPath, self.LogFile
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    """
    Main simulation controller that manages parallel or serial execution of simulation runs.
    
    Handles:
    - Initialization of simulation environment and callback setup
    - Parallel execution with thread management (if enabled in config)
    - Error recovery and retry logic for failed simulations
    - Serial execution fallback mode
    - Results logging and final cleanup
    
    The execution flow is controlled by JSON configuration which determines:
    - Parallel/hierarchical mode settings
    - Number of threads/iterations
    - Error handling behavior and max retries
    
    Dependencies:
    - Requires properly configured Dependencies (dp) and ScriptBody modules
    - Relies on JSON configuration for runtime parameters
    """
  

if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
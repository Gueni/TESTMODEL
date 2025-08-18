import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
import ScriptBody
dp.script_path  =   os.path.abspath(__file__)

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
    # Create script runner instance and initialize simulation
    RunScript       =       dp.run.runScripts(dp.JSON)
    RunScript.simInit()
    
    # Setup callback function for trace holding based on JSON configuration
    Callback        =       RunScript.obj.holdTraceCallback(dp.JSON['scopes'])
    
    # Initialize counters for iterations and retries
    i               =       0
    tries           =       0
    
    # Parallel Execution Section
    if dp.JSON['parallel']:

        # Main parallel simulation loop
        while i < RunScript.simutil.Simulations:

            # Determine iteration range based on hierarchical or flat parallelization
            if dp.JSON['hierarchical']:
                iteration_range             =   list(range(sum(RunScript.simutil.threads_vector[0:i]),sum(RunScript.simutil.threads_vector[0:i+1])))
                RunScript.simutil.Threads   =   RunScript.simutil.threads_vector[i]
            else:
                iteration_range             =   list(range(i*RunScript.simutil.Threads,RunScript.simutil.Threads*(i+1)))
            
            # Initialize model options for current parallel batch
            RunScript.obj.modelinit_opts(RunScript.simutil.Threads,iteration_range,RunScript.JS['parallel'])
            
            # Simulation Iterations Header logging 
            j = 0
            RunScript.iterations_header(i)

            while j < RunScript.simutil.Threads:

                # Execute simulation script and log updated values for each thread
                ScriptBody.simScript(RunScript,RunScript.obj.OptStruct,j,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)
                RunScript.simLog(RunScript.obj.OptStruct[j])
                j+=1
            
            # Simulation Run and Error Handling Section
            try:
                # Normal execution parameter setting
                crash                           =   False
                RunScript.simRun(RunScript.simutil.Threads,True,Callback)
                RunScript.simSave(i,crash)
                tries                           =   0
                i+=1
            except:
                # Error recovery parameter setting
                crash                           =   True
                iterNumber                      =   RunScript.simutil.iterNumber
                
                # Handle missing iterations after crash
                MissingIter                     =   RunScript.simMissing(i,RunScript.simutil.threads_vector,RunScript.simutil.Threads)
                k = 0
                while k < len(MissingIter):
                    RunScript.simutil.iterNumber   =   MissingIter[k]
                    RunScript.obj.modelinit_opts(1,[RunScript.simutil.iterNumber],True)

                    # Re-run failed simulations
                    ScriptBody.simScript(RunScript.obj.OptStruct,0,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)
                    RunScript.simRun(parallel=True,callback=Callback)
                    k+=1

                # Save results after recovery
                RunScript.simSave(i,crash)
                RunScript.simutil.iterNumber       =   iterNumber

                i+=1
                tries+=1
                # Exit if max retries reached
                if (tries >= dp.JSON['tries']):
                    break
                else:
                    continue
    
    # Serial Execution Section
    else:
        # Non-parallel execution path
        RunScript.obj.modelinit_opts(RunScript.simutil.Threads,RunScript.JS['parallel'])
        RunScript.simLog(RunScript.obj.OptStruct)
        RunScript.simRun(threads=1,parallel=False)
        RunScript.simSave()

    # Cleanup and footer logging Section
    RunScript.simEnd()

if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
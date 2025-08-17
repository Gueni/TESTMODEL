
import os,sys                                                                                                                                                  # Import os and sys modules
sys.path.insert(1,os.getcwd() + '/Script/assets')                                                                                                               # Insert assets directory to system path
import Dependencies as dp                                                                                                                                       # Import Dependencies module as dp
import ScriptBody                                                                                                                                               # Import ScriptBody module
dp.script_path  =   os.path.abspath(__file__)                                                                                                                   # Set script path to absolute path of current file

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():                                                                                                                                                     # Define main function
    RunScript       =       dp.run.runScripts(dp.JSON)                                                                                                          # Initialize RunScript with JSON configuration
    RunScript.simInit()                                                                                                                                         # Initialize simulation
    Callback        =       RunScript.obj.holdTraceCallback(dp.JSON['scopes'])                                                                                  # Set up trace callback for scopes

    i               =       0                                                                                                                                   # Initialize counter i to 0
    tries           =       0                                                                                                                                   # Initialize tries counter to 0
    if dp.JSON['parallel']:                                                                                                                                     # Check if parallel execution is enabled
        while i < RunScript.simutil.Simulations:                                                                                                                # Loop while i is less than total simulations
            if dp.JSON['hierarchical']:                                                                                                                         # Check if hierarchical mode is enabled
                iteration_range             = list(range(sum(RunScript.simutil.threads_vector[0:i]),sum(RunScript.simutil.threads_vector[0:i+1])))             # Calculate iteration range for hierarchical mode
                RunScript.simutil.Threads   = RunScript.simutil.threads_vector[i]                                                                              # Set threads from threads_vector

            iteration_range                 = list(range(i*RunScript.simutil.Threads,RunScript.simutil.Threads*(i+1)))                                          # Calculate iteration range for parallel mode
            RunScript.obj.modelinit_opts(RunScript.simutil.Threads,iteration_range,RunScript.JS['parallel'])                                                    # Initialize model options

            j = 0                                                                                                                                              # Initialize counter j to 0
            while j < RunScript.simutil.Threads:                                                                                                                # Loop through each thread
                ScriptBody.simScript(RunScript.obj.OptStruct,j,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)  # Execute simulation script
                RunScript.simLog(RunScript.obj.OptStruct[j],i)                                                                                                 # Log simulation results
                j+=1                                                                                                                                           # Increment j

            try:                                                                                                                                               # Begin try block for error handling
                crash                           =   False                                                                                                       # Set crash flag to False
                RunScript.simRun(RunScript.simutil.Threads,True,Callback)                                                                                      # Run simulation
                RunScript.simSave(i,crash)                                                                                                                     # Save simulation results
                tries                           =   0                                                                                                           # Reset tries counter
                i+=1                                                                                                                                           # Increment i

            except:                                                                                                                                             # Handle exceptions
                crash                           =   True                                                                                                        # Set crash flag to True
                iterNumber                      =   RunScript.simutil.iterNumber                                                                                # Store current iteration number
                MissingIter                     =   RunScript.simMissing(i,RunScript.simutil.threads_vector,RunScript.simutil.Threads)                         # Find missing iterations

                k = 0                                                                                                                                          # Initialize counter k to 0
                while k < len(MissingIter):                                                                                                                    # Loop through missing iterations
                    RunScript.simutil.iterNumber   =   MissingIter[k]                                                                                         # Set current iteration number
                    # RunScript.obj.OptStruct[RunScript.simutil.iterNumber]['Name']   =   'Iter_' + str(RunScript.simutil.iterNumber+1)                        # (Commented out) Set iteration name
                    ScriptBody.simScript(RunScript.obj.OptStruct,0,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)  # Execute simulation script
                    RunScript.simRun(parallel=True,callback=Callback)                                                                                          # Run simulation in parallel
                    k+=1                                                                                                                                       # Increment k

                RunScript.simSave(i,crash)                                                                                                                     # Save simulation results
                RunScript.simutil.iterNumber       =   iterNumber                                                                                              # Restore original iteration number
                RunScript.obj.modelInit_path(RunScript.JS['modelname'])                                                                                        # Initialize model path
                RunScript.obj.modelinit_opts(RunScript.simutil.Threads,RunScript.JS['parallel'])                                                               # Initialize model options

                i+=1                                                                                                                                           # Increment i

                tries+=1                                                                                                                                        # Increment tries counter
                if (tries >= dp.JSON['tries']):                                                                                                                 # Check if max tries reached
                    break                                                                                                                                       # Break loop if max tries reached
                else:                                                                                                                                          # Else
                    continue                                                                                                                                    # Continue loop

    else:                                                                                                                                                      # If not parallel execution
        RunScript.obj.modelinit_opts(RunScript.simutil.Threads,RunScript.JS['parallel'])                                                                        # Initialize model options
        RunScript.simLog(RunScript.obj.OptStruct)                                                                                                              # Log simulation results
        RunScript.simRun(threads=1,parallel=False)                                                                                                             # Run simulation in single thread
        RunScript.simSave()                                                                                                                                     # Save simulation results

    RunScript.simEnd()                                                                                                                                          # End simulation

if __name__ == "__main__":                                                                                                                                      # Check if script is run directly
    main()                                                                                                                                                      # Call main function
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
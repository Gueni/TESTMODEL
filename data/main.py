import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
import ScriptBody
dp.script_path  =   os.path.abspath(__file__)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    RunScript       =       dp.run.runScripts(dp.JSON)
    RunScript.simInit()
    Callback        =       RunScript.obj.holdTraceCallback(dp.JSON['scopes'])

    i               =       0
    tries           =       0
    if dp.JSON['parallel']:
        while i < RunScript.simutil.Simulations:
            if dp.JSON['hierarchical']:
                iteration_range             = list(range(sum(RunScript.simutil.threads_vector[0:i]),sum(RunScript.simutil.threads_vector[0:i+1])))
                RunScript.simutil.Threads   = RunScript.simutil.threads_vector[i]

            iteration_range                 = list(range(i*RunScript.simutil.Threads,RunScript.simutil.Threads*(i+1)))
            RunScript.obj.modelinit_opts(RunScript.simutil.Threads,iteration_range,RunScript.JS['parallel'])

            j = 0
            while j < RunScript.simutil.Threads:
                ScriptBody.simScript(RunScript.obj.OptStruct,j,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)
                RunScript.simLog(RunScript.obj.OptStruct[j],i)
                j+=1
            try:
                crash                           =   False
                RunScript.simRun(RunScript.simutil.Threads,True,Callback)
                RunScript.simSave(i,crash)
                tries                           =   0
                i+=1

            except:
                crash                           =   True
                iterNumber                      =   RunScript.simutil.iterNumber
                MissingIter                     =   RunScript.simMissing(i,RunScript.simutil.threads_vector,RunScript.simutil.Threads)

                k = 0
                while k < len(MissingIter):
                    RunScript.simutil.iterNumber   =   MissingIter[k]
                    # RunScript.obj.OptStruct[RunScript.simutil.iterNumber]['Name']   =   'Iter_' + str(RunScript.simutil.iterNumber+1)
                    ScriptBody.simScript(RunScript.obj.OptStruct,0,RunScript.simutil.Map,RunScript.simutil.iterNumber,RunScript.fileLog.ResultsPath,RunScript.simutil)
                    RunScript.simRun(parallel=True,callback=Callback)
                    k+=1

                RunScript.simSave(i,crash)
                RunScript.simutil.iterNumber       =   iterNumber
                RunScript.obj.modelInit_path(RunScript.JS['modelname'])
                RunScript.obj.modelinit_opts(RunScript.simutil.Threads,RunScript.JS['parallel'])

                i+=1

                tries+=1
                if (tries >= dp.JSON['tries']):
                    break
                else:
                    continue
    else:
        RunScript.obj.modelinit_opts(RunScript.simutil.Threads,RunScript.JS['parallel'])
        RunScript.simLog(RunScript.obj.OptStruct)
        RunScript.simRun(threads=1,parallel=False)
        RunScript.simSave()

    RunScript.simEnd()

if __name__ == "__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

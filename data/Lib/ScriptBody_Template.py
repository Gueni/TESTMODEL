import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
paramProcess            =	dp.PM.ParamProcess()
dataProcess             =   dp.PP.Processing()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def simScript(RunScript,OptStruct,Thread,Map,iterNumber,ResultsPath,misc,crash=False):
    """This function is used to write scripts for automated simulations. Multiple simulations with parameters or conditions variations can be programmed here.
       Please make a copy of this file and rename it to 'ScriptBody.py' and place it in the same directory as this file.
       Please don't delete or make changes to this file.

    Args:
        OptStruct (list)        : nested list that contains simulation parameters
        Thread (int)            : current working thread number
        Map (list)              : nested list containing all simulation sweep parameters
        iterNumber (int)        : current working iteration number
        ResultsPath (string)    : current results folder location
        misc (class)            : miscellaneous class object for simulation data handling
        crash (bool)            : a boolean to determine if a simulation crash happened in the previous iteration
    """

    mdlVars                                                                        =   OptStruct[Thread]['ModelVars']
    mapVars                                                                        =   Map[iterNumber]
    mdlVars['Common']['ToFile']['FileName']                                        =   ResultsPath + str(iterNumber+1)

    #! -------------------------------------------------------------------------------------Don't change above this line-------------------------------------------------------------------------------------

    #?  to change a simulation parameter use the following command:
        #*  mdlVars['Common']['DesiredParameter']           =   DesiredValue
        #*  mdlVars['DCDC_Rail1']['DesiredParameter']       =   DesiredValue
        #*  mdlVars['DCDC_Rail2']['DesiredParameter']       =   DesiredValue
            #   DesiredParameter can be a variable, list or dictionary

    #?  to assign a sweep parameter to a simulation parameter use the following command:
        #*  mdlVars['DesiredParameter']                     =   mapVars[x]
            #   x is the parameter index as created in the 'Input_vars.json' file, ranging from 0 to 9.

    #! -------------------------------------------------------------------------------------Don't change under this line-------------------------------------------------------------------------------------

    diff = dp.DeepDiff(OptStruct[Thread-1]['ModelVars'], OptStruct[Thread]['ModelVars'], verbose_level=2).get("values_changed", {})
    RunScript.log_updates(diff)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
paramProcess            =	dp.PM.ParamProcess()
dataProcess             =   dp.PP.Processing()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def simScript(OptStruct,Thread,Map,iterNumber,ResultsPath,misc,crash=False):
    """
    This function is used to write scripts for automated simulations. Multiple simulations with parameters or conditions variations can be programmed here.
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
    X1,X2,X3,X4,X5,X6,X7,X8,X9,X10                                                 =   range(10)
    mdlVars['Common']['ToFile']['FileName']                                        =   ResultsPath + str(iterNumber+1)
    mdlVars['Common']['ToFile']['FileNameStandalone']                              =   mdlVars['Common']['ToFile']['FileName'] + '_Standalone'
    mdlVars                                                                        =   dp.TD.TrackableDict(mdlVars)

    with mdlVars.track_scope():
        pass

    #! -------------------------------------------------------------------------------------Don't change above this line---------------------------------------------------------------------------
        mdlVars['Rectifier']['Gate_Driver']['Ron']                                  =   mapVars[X1][0]
        mdlVars['Rectifier']['Gate_Driver']['Roff']                                 =   mapVars[X2][0]
        mdlVars['Rectifier']['GateNetwork']['ON_Path']['Rg']                        =   mapVars[X3][0]
        mdlVars['Rectifier']['GateNetwork']['OFF_Path']['Rg']                       =   mapVars[X4][0]
        mdlVars['Rectifier']['Transistor']['Cg_tot']                                =   mapVars[X5][0] * 1e-9
        mdlVars['Rectifier']['Vth']                                                 =   mapVars[X6][0]
        mdlVars['Rectifier']['Gate_Driver']['Delay']                                =   mapVars[X7][0] * 1e-9
        mdlVars['Rectifier']['Gate_Driver']['Vth_h']                                =   mapVars[X8][0]
        mdlVars['Rectifier']['Gate_Driver']['Vth_l']                                =   mapVars[X9][0]

        mdlVars['PS_LS']['Gate_Driver']['Ron']                                      =   mapVars[X1][0]
        mdlVars['PS_LS']['Gate_Driver']['Roff']                                     =   mapVars[X2][0]
        mdlVars['PS_LS']['GateNetwork']['ON_Path']['Rg']                            =   mapVars[X3][0]
        mdlVars['PS_LS']['GateNetwork']['OFF_Path']['Rg']                           =   mapVars[X4][0]
        mdlVars['PS_LS']['Transistor']['Cg_tot']                                    =   mapVars[X5][0] * 1e-9
        mdlVars['PS_LS']['Vth']                                                     =   mapVars[X6][0]
        mdlVars['PS_LS']['Gate_Driver']['Delay']                                    =   mapVars[X7][0] * 1e-9
        mdlVars['PS_LS']['Gate_Driver']['Vth_h']                                    =   mapVars[X8][0]
        mdlVars['PS_LS']['Gate_Driver']['Vth_l']                                    =   mapVars[X9][0]

        mdlVars['PS_HS']['Gate_Driver']['Ron']                                      =   mapVars[X1][0]
        mdlVars['PS_HS']['Gate_Driver']['Roff']                                     =   mapVars[X2][0]
        mdlVars['PS_HS']['GateNetwork']['ON_Path']['Rg']                            =   mapVars[X3][0]
        mdlVars['PS_HS']['GateNetwork']['OFF_Path']['Rg']                           =   mapVars[X4][0]
        mdlVars['PS_HS']['Transistor']['Cg_tot']                                    =   mapVars[X5][0] * 1e-9
        mdlVars['PS_HS']['Vth']                                                     =   mapVars[X6][0]
        mdlVars['PS_HS']['Gate_Driver']['Delay']                                    =   mapVars[X7][0] * 1e-9
        mdlVars['PS_HS']['Gate_Driver']['Vth_h']                                    =   mapVars[X8][0]
        mdlVars['PS_HS']['Gate_Driver']['Vth_l']                                    =   mapVars[X9][0]

        mdlVars['AC']['Gate_Driver']['Ron']                                         =   mapVars[X1][0]
        mdlVars['AC']['Gate_Driver']['Roff']                                        =   mapVars[X2][0]
        mdlVars['AC']['GateNetwork']['ON_Path']['Rg']                               =   mapVars[X3][0]
        mdlVars['AC']['GateNetwork']['OFF_Path']['Rg']                              =   mapVars[X4][0]
        mdlVars['AC']['Transistor']['Cg_tot']                                       =   mapVars[X5][0] * 1e-9
        mdlVars['AC']['Vth']                                                        =   mapVars[X6][0]
        mdlVars['AC']['Gate_Driver']['Delay']                                       =   mapVars[X7][0] * 1e-9
        mdlVars['AC']['Gate_Driver']['Vth_h']                                       =   mapVars[X8][0]
        mdlVars['AC']['Gate_Driver']['Vth_l']                                       =   mapVars[X9][0]

        # mdlVars['Rectifier']['Gate_Driver']['Ron']                                  =   mapVars[X9][0]
        # mdlVars['Rectifier']['Gate_Driver']['Roff']                                 =   mapVars[X8][0]
        # mdlVars['Rectifier']['GateNetwork']['ON_Path']['Rg']                        =   mapVars[X7][0]
        # mdlVars['Rectifier']['GateNetwork']['OFF_Path']['Rg']                       =   mapVars[X6][0]
        # mdlVars['Rectifier']['Transistor']['Cg_tot']                                =   mapVars[X5][0] * 1e-9
        # mdlVars['Rectifier']['Vth']                                                 =   mapVars[X4][0]
        # mdlVars['Rectifier']['Gate_Driver']['Delay']                                =   mapVars[X3][0] * 1e-9
        # mdlVars['Rectifier']['Gate_Driver']['Vth_h']                                =   mapVars[X2][0]
        # mdlVars['Rectifier']['Gate_Driver']['Vth_l']                                =   mapVars[X1][0]

        # mdlVars['PS_LS']['Gate_Driver']['Ron']                                      =   mapVars[X9][0]
        # mdlVars['PS_LS']['Gate_Driver']['Roff']                                     =   mapVars[X8][0]
        # mdlVars['PS_LS']['GateNetwork']['ON_Path']['Rg']                            =   mapVars[X7][0]
        # mdlVars['PS_LS']['GateNetwork']['OFF_Path']['Rg']                           =   mapVars[X6][0]
        # mdlVars['PS_LS']['Transistor']['Cg_tot']                                    =   mapVars[X5][0] * 1e-9
        # mdlVars['PS_LS']['Vth']                                                     =   mapVars[X4][0]
        # mdlVars['PS_LS']['Gate_Driver']['Delay']                                    =   mapVars[X3][0] * 1e-9
        # mdlVars['PS_LS']['Gate_Driver']['Vth_h']                                    =   mapVars[X2][0]
        # mdlVars['PS_LS']['Gate_Driver']['Vth_l']                                    =   mapVars[X1][0]

        # mdlVars['PS_HS']['Gate_Driver']['Ron']                                      =   mapVars[X9][0]
        # mdlVars['PS_HS']['Gate_Driver']['Roff']                                     =   mapVars[X8][0]
        # mdlVars['PS_HS']['GateNetwork']['ON_Path']['Rg']                            =   mapVars[X7][0]
        # mdlVars['PS_HS']['GateNetwork']['OFF_Path']['Rg']                           =   mapVars[X6][0]
        # mdlVars['PS_HS']['Transistor']['Cg_tot']                                    =   mapVars[X5][0] * 1e-9
        # mdlVars['PS_HS']['Vth']                                                     =   mapVars[X4][0]
        # mdlVars['PS_HS']['Gate_Driver']['Delay']                                    =   mapVars[X3][0] * 1e-9
        # mdlVars['PS_HS']['Gate_Driver']['Vth_h']                                    =   mapVars[X2][0]
        # mdlVars['PS_HS']['Gate_Driver']['Vth_l']                                    =   mapVars[X1][0]

        # mdlVars['AC']['Gate_Driver']['Ron']                                         =   mapVars[X9][0]
        # mdlVars['AC']['Gate_Driver']['Roff']                                        =   mapVars[X8][0]
        # mdlVars['AC']['GateNetwork']['ON_Path']['Rg']                               =   mapVars[X7][0]
        # mdlVars['AC']['GateNetwork']['OFF_Path']['Rg']                              =   mapVars[X6][0]
        # mdlVars['AC']['Transistor']['Cg_tot']                                       =   mapVars[X5][0] * 1e-9
        # mdlVars['AC']['Vth']                                                        =   mapVars[X4][0]
        # mdlVars['AC']['Gate_Driver']['Delay']                                       =   mapVars[X3][0] * 1e-9
        # mdlVars['AC']['Gate_Driver']['Vth_h']                                       =   mapVars[X2][0]
        # mdlVars['AC']['Gate_Driver']['Vth_l']                                       =   mapVars[X1][0]

    #! -------------------------------------------------------------------------------------Don't change under this line---------------------------------------------------------------------------

    dp.updated_params_dict                                                          =   mdlVars.assignments
    mdlVars                                                                         =   dict(mdlVars)
    OptStruct[Thread]['ModelVars']                                                  =   mdlVars

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   Extract parameters from Param_Dicts to be transferred to Dymola DC/DC converter model.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------import dependencies

import numpy as np
import os, sys
sys.path.append(os.path.abspath('Script/assets'))
sys.path.append(os.path.abspath('Script/Lib'))
sys.path.append(os.path.abspath('Script/DCDC'))
sys.path.append(os.path.abspath('../../Packages/termcolor/Lib/site-packages'))
import termcolor

import Dependencies
import Param_Dicts as pd

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

print("//primary stage")
print("parameter Real Cp =",pd.Cin['Csingle']*pd.Cin['nPar']/pd.Cin['nSer']+pd.Cpi['Csingle']*pd.Cpi['nPar']/pd.Cpi['nSer']+2*pd.Cc['Csingle']*pd.Cc['nPar']/pd.Cc['nSer'],";")  	                                                                        #Cin.Csingle * Cin.nPar/Cin.nSer
print("parameter Real Rcp =",(pd.Cpi['Rsingle']*pd.Cpi['nSer']/pd.Cpi['nPar'])*(0.5*pd.Cc['Rsingle']*pd.Cc['nSer']/pd.Cc['nPar'])/((pd.Cpi['Rsingle']*pd.Cpi['nSer']/pd.Cpi['nPar'])+(0.5*pd.Cc['Rsingle']*pd.Cc['nSer']/pd.Cc['nPar'])),";")    	                                                                    # Cin.Rsingle * Cin.nSer/Cin.nPar
print("//converter")
print("parameter Real Rdsp =",pd.LeftLeg_1['Transistor']['Rds_on'],";") 	                                                                                    #AIMDQ75R063M1H LeftLeg.Transistor.Rds_on
print("parameter Real Rdss =",pd.Rectifier_1['Transistor']['Rds_on'],";")	                                                                                    #IAUT300N1055015 LeftLeg.Transistor.Rds_on
print("parameter Real L_k =",pd.Trafo['Lkp']+pd.Trafo['Lks']*(pd.Trafo['Np']/pd.Trafo['Ns'])**2,";")	                                                    #Trafo.Lkp+Trafo.Lks*(Trafo.Np/Trafo.Ns)^2
print("parameter Real R_ss =",pd.Trafo['Rpri']+pd.Cb['Rsingle']*pd.Cb['nSer']/pd.Cb['nPar']+ pd.CT['Trafo']['Rpri'] + pd.CT['Trafo']['Rsec']*(pd.CT['Trafo']['Np']/pd.CT['Trafo']['Ns'])**2,";")#Trafo.Rpri + Cb.Rsingle*Cb.nSer/Cb.nPar + CT.Rpri + CT.Rsec*(CT.Np/CT.Ns)^2
print("parameter Real n =",pd.Trafo['Np']/pd.Trafo['Ns'],";")		                                                                                        #(Trafo.Np/Trafo.Ns)
print("parameter Real Vdp =",pd.LeftLeg_1['BodyDiode']['Vf'],";") 		                                                                                        #AIMDQ75R063M1H BodyDiode.Vf, IAUT300N1055015 BodyDiode.Vf
print("parameter Real Vds =",pd.Rectifier_1['BodyDiode']['Vf'],";")
print("parameter Real Vd =",pd.Rectifier_1['BodyDiode']['Vf'],";")
print("//output stage")
print("parameter Real Coe =",pd.Coe1['Csingle']*pd.Coe1['nPar']/pd.Coe1['nSer'],";")	                    # electrolytic capacitor:  Co.Csingle * Co.nPar/Co.nSer  ||  Coe.Csingle * Coe.nPar/Coe.nSer
print("parameter Real Rd =",pd.Coe1['Rsingle'] * pd.Coe1['nSer']/pd.Coe1['nPar'] + pd.Coe1['Rd'],";")	    # electrolytic capacitor: Co.Rsingle * Co.nSer/Co.nPar || Coe.Rsingle * Coe.nSer/Coe.nPar + Coe.Rd
print("parameter Real Cs =",pd.Co['Csingle']*pd.Co['nPar']/pd.Co['nSer'],";")	                        # ceramic capacitor:
print("parameter Real Rcs =",pd.Co['Rsingle']*pd.Co['nSer']/pd.Co['nPar'],";")	    # ceramic capacitor: Co.Rsingle * Co.nSer/Co.nPar || Coe.Rsingle * Coe.nSer/Coe.nPar + Coe.Rd
print("parameter Real Ls =",pd.Lf['L'],";")		                                                                                                            # Lf.L
print("parameter Real DCR =",pd.Trafo['Rsec']+pd.Lf['R']+pd.LV_currentSense['R'],";")	                                                                    # Trafo.Rsec + Lf.R + LV_currentSense.R
print("//snubbers")
print("parameter Real Rscp=1;"); 		#* optional:
print("parameter Real Csp=",pd.LeftLeg_1['Coss']['C'],";")	                                                                                                #	* AIMDQ75R063M1H Coss.C: more accurate -> C= AIMDQ75R063M1H Coss.Qoss/Vds (lookup)
print("parameter Real Rscs=",pd.RCsnubber['SR_MOSFET']['Rs']['R']/pd.RCsnubber['SR_MOSFET']['Rs']['nPar'],";")	                                        #	* optional: RCsnubber.SR_MOSFET.Rs.R/RCsnubber.SR_MOSFET.Rs.nPar +
print("parameter Real Css=", pd.RCsnubber['SR_MOSFET']['Cs']['Csingle']*pd.RCsnubber['SR_MOSFET']['Cs']['nPar']/pd.RCsnubber['SR_MOSFET']['Cs']['nSer']+pd.Rectifier_1['Coss']['C'],";") # RCsnubber.SR_MOSFET.Cs.Csingle* RCsnubber.SR_MOSFET.Cs.nPar/RCsnubber.SR_MOSFET.Cs.nSer                                                                                                #		* IAUT300N1055015 Coss.C: more accurate ->  C= IAUT300N1055015 Coss.Qoss/(Vds/n) (lookup)
print("//measurment current")
print("parameter Real Nct =",(pd.CT['Trafo']['Np']/pd.CT['Trafo']['Ns'])**(-1),";")	                                                                                        #	* (CT.Np/CT.Ns)^(-1)
print("parameter Real Rt =",pd.CT['Rt'],";")		                                                                                                        #* (CT.Rt)
print("//measurment voltage")
print("parameter Real voltageDivider =",pd.LV_voltageSense['Misc']['Gain'],";")                                   # * LV_voltageSense.R2/(LV_voltageSense.R1+ LV_voltageSense.R2)
print("//voltage control")
print("parameter Real ADCrange =",pd.ADCgains['ADCrange'],";")                                                                                              #* ADCgains.ADCrange
print("parameter Real Kc =",pd.PCMCbuck['outputScale'],";")
print("parameter Real Kpc =",pd.PCMCbuck['Kp'],";")		                                                                                                    #* PCMCbuck.Kp
print("parameter Real Kic =",pd.PCMCbuck['Ki'],";") 	                                                                                                    #* PCMCbuck.Ki
print("parameter Real Icmax =",pd.Control['Targets']['Icmax'],";")                                                                                          # in ampere Control.Targets.Icmax
print("parameter Real UpLim =",pd.PCMCbuck['UpLim'],";")
print("//peak current control")
print("parameter Real SLP =",pd.PCMCbuck['SLP'],";")                                                                                                        #		* PCMCbuck.SLP
print("parameter Real DACrange =",pd.ADCgains['DACrange'],";")                                                                                              # * ADCgains.DACrange
print("parameter Real Dmax =",pd.PWM['Dmax'],";")                                                                                                           # 	* PWM.Dmax
print("parameter Real Dmin =",pd.PWM['Dmin'],";")                                                                                                           #		* PWM.Dmin
print("parameter Real LV_current_Gain =",pd.LV_currentSense['R'],";")                                                                                                           #		* PWM.Dmin
print("parameter Real LV_current_SlewRate =",pd.softStart['BuckRamp'],";")
#print("parameter Real LV_current_Offset =",pd.LV_currentSense['Misc']['Voffset'],";")                                                                                                           #		* PWM.Dmin
print("//measurements")
print("parameter Real LV_current_G1 =",pd.LV_currentSense['FirstComponent']['Gain'],";")
print("parameter Real LV_current_G2 =",pd.LV_currentSense['SecondComponent']['Gain'],";")
print("parameter Real LV_current_B1_1 =",   pd.LV_currentSense['FirstComponent']['C1_2'] * \
                                            pd.LV_currentSense['FirstComponent']['C2_2'] * \
                                            pd.LV_currentSense['FirstComponent']['R1_2'] * \
                                            pd.LV_currentSense['FirstComponent']['R2_2'],";")
print("parameter Real LV_current_B2_1 =",   (pd.LV_currentSense['FirstComponent']['R1_2'] + \
                                            pd.LV_currentSense['FirstComponent']['R2_2']) * \
                                            pd.LV_currentSense['FirstComponent']['C2_2'],";")
print("parameter Real LV_current_B1_2 =",   pd.LV_currentSense['SecondComponent']['C1_2'] * \
                                            pd.LV_currentSense['SecondComponent']['C2_2'] * \
                                            pd.LV_currentSense['SecondComponent']['R1_2'] * \
                                            pd.LV_currentSense['SecondComponent']['R2_2'],";")
print("parameter Real LV_current_B2_2 =",   (pd.LV_currentSense['SecondComponent']['R1_2'] + \
                                            pd.LV_currentSense['SecondComponent']['R2_2']) * \
                                            pd.LV_currentSense['SecondComponent']['C1_2']  + \
                                            pd.LV_currentSense['SecondComponent']['C2_2']  * \
                                            pd.LV_currentSense['SecondComponent']['R1_2']  * \
                                            (1 - pd.LV_currentSense['SecondComponent']['Gain']),";")
#LP filter of LV_currentSense, LV_voltageSense, CT
#print("parameter Real LV_current_R =",pd.LV_currentSense['LP_Filter']['R'],";")
#print("parameter Real LV_current_C =",pd.LV_currentSense['LP_Filter']['C'],";")
#print("parameter Real LV_CT_R =",pd.CT['Rf'],";")
#print("parameter Real LV_CT_C =",pd.CT['Cf'],";")
print("parameter Real LV_voltageSense_R =",pd.ADCmodel['InputFilters']['LV_voltageSense']['Rfil'],";")
print("parameter Real LV_voltageSense_C =",pd.ADCmodel['InputFilters']['LV_voltageSense']['Cfil'],";")
print("//modulator")
print("parameter Real f_s=",pd.MCU['f_s'],";")                                                                                                              #		* MCU.f_s
print("parameter Real T_s =",pd.MCU['T_s'],";")	                                                                                                        #MCU.T_s = 1/ MCU.f_s
print("parameter Real Td=",pd.PWM['Deadtimes_Rail_1']['S1'],";")
print("parameter Real Tdp=",pd.PWM['Deadtimes_Rail_1']['S1'],";")	                                                                                                            # *  PWM.Tdead
print("parameter Real Tds=",pd.PWM['Deadtimes_Rail_1']['S1'],";")	                                                                                                            # *  PWM.Tdead
print("parameter Real Trise=",pd.PWM['RecShift_Rail_1']['CCM']['S5']['Tr'],";")
print("parameter Real Tfall=",pd.PWM['RecShift_Rail_1']['CCM']['S5']['Tf'],";")
print("parameter Real Toffset=",pd.ADCmodel['Tacq'],";")
print("parameter Real Invlp=",pd.PCMCbuck['CCMcurrent'],";")
print("//ripple current approximation")
print("parameter Real Ir=20;")
print("")
print("//output filter")
#print("Coe, Rc3, Rd eliminated// Rbb busbar resistance (after p_s added)")
print("//differential mode choke");
print("parameter Real Lout1=",pd.LVdmc['Lself'],";")
print("parameter Real Kcm1=",pd.LVdmc['Km'],";")
#print("//common mode choke"); #eliminated in B-Sample
#print("parameter Real Lout2=",pd.LVcmc['Lself'],";")#eliminated in B-Sample
#print("parameter Real Kcm2=",pd.LVcmc['Km'],";")#eliminated in B-Sample
print("//ceramic capacitors");
print("parameter Real Coc=",pd.Coc1['Csingle']*pd.Coc1['nPar']/pd.Coc1['nSer']+pd.Coc2['Csingle']*pd.Coc2['nPar']/pd.Coc2['nSer'],";")
print("parameter Real Rc2=",(pd.Coc1['Rsingle']*pd.Coc1['nSer']/pd.Coc1['nPar'])*(pd.Coc2['Rsingle']*pd.Coc2['nSer']/pd.Coc2['nPar'])/((pd.Coc1['Rsingle']*pd.Coc1['nSer']/pd.Coc1['nPar'])+(pd.Coc2['Rsingle']*pd.Coc2['nSer']/pd.Coc2['nPar'])),";")
print("parameter Real Rbb=",pd.Busbars_PCB['LV_Filter']['PlusResistance']+pd.Busbars_PCB['LV_Filter']['MinusResistance'],";")
print("//y capacitors");
print("parameter Real Cy=",pd.Cyo['Csingle']*pd.Cyo['nPar']/pd.Cyo['nSer'],";")
print("parameter Real Ry=",pd.Cyo['Rsingle']*pd.Cyo['nSer']/pd.Cyo['nPar']+1,";")
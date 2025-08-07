
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 __  __  ___  ____  _____ _       ____   _    ____      _    __  __ _____ _____ _____ ____  ____
#?						|  \/  |/ _ \|  _ \| ____| |     |  _ \ / \  |  _ \    / \  |  \/  | ____|_   _| ____|  _ \/ ___|
#?						| |\/| | | | | | | |  _| | |     | |_) / _ \ | |_) |  / _ \ | |\/| |  _|   | | |  _| | |_) \___ \
#?						| |  | | |_| | |_| | |___| |___  |  __/ ___ \|  _ <  / ___ \| |  | | |___  | | | |___|  _ < ___) |
#?						|_|  |_|\___/|____/|_____|_____| |_| /_/   \_\_| \_\/_/   \_\_|  |_|_____| |_| |_____|_| \_\____/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------

#------------------import dependencies

import Dependencies as dp
Fuses 		= 	dp.copy.deepcopy(dp.Fuses_Dicts.AllFuses)
Mags 		=	dp.copy.deepcopy(dp.Mags_Dicts.AllMagnetics)
Sensors 	=	dp.copy.deepcopy(dp.Sensor_Dicts.AllSensors)
Switches 	=	dp.copy.deepcopy(dp.Switches_Dicts.AllSwitches)
Relay		= 	dp.copy.deepcopy(dp.Relay_Dicts.AllRelays)
Battery		= 	dp.copy.deepcopy(dp.Battery_Dicts.AllBatteries)

#------------------

#! All DCDC simulation parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Simulation Parameters

simParams			= 	{																																	#*	simulation run parameters
							'tSim'      		  	: 24e-3			  																					,  	#?	total simulation time
                            'tStart'    		 	: 0.0e-3		  																					,  	#?	converter start time
                            'Maxstep'   		  	: 1e-3			  																					,  	#?	maximum simulation step size
                            'Fixedstep' 		  	: 2e-10			  																					,  	#?	fixed simulation step size
                            'tBegin'    		  	: 0e-3			  																					,   #?	start time of probing
                            'tSave'					: 0e-3																								,	#?	start time of data saving
                            'tEnd'      		  	: 23e-3			  																					,  	#?	end time of probing
                            'RelTol'    		  	: 1e-3 			  																					,  	#?	relative tolerance of solvers
                            'ZeroCross' 		  	: 1000          																					,	#?	max number of consecutive zero-crossings
                            'Refine'				: 1																										#?	data refining factor to get more data points
                        }

OutputTimes			=	{																																	#*	configuration for RPC-based OutputTimes vector
    						'tEnd'					: 0.50e-4																							,	#?	last element of Time vector in OutputTimes
       						'tStart'				: 0.30e-4																							,	#?	first element of Time vector in OuutputTimes
       						'Npoints'				: 350																									#?	number of sample points of the simulation results through RPC
      					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Models Selection

Probes				= 	{																																	#*	probes statuses
                            'Electric_Probes'     	: 1 			  																					,	#?	1->Enable | 2->Disable
                            'Control_Probes'      	: 5       		  																						#? 	1->Peak Buck | 2->Duty Precharge | 3->Duty Boost | 4->Duty Buck | 5->Disable
                        }

ToFile				=	dp.OrderedDict({																													#*	PLECS built-in data output configuration
							'OutputTimes'			:			  2																						,	#?	1->Enable | 2->Disable
							'CurrentExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'VoltageExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'ThermalExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'StatsExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'ControlExport'			:			  2																						,	#?	1->Enable | 2->Disable
       						'FileName'				:		      ''																					,	#?	name of the exported data file
                            'Tau_deg'				:			  1e-9																					,	#?	deglitch filter time-constant to remove simulation artifacts
                            'Ts'					:			  0																						,	#?	sample time for the data export, 0 for continuous sampling
							'Y1'					:	{																									#!	data set 1
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 77																						#?	length of export data
							},
							'Y2'					:	{																									#!	data set 2
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 77																						#?	length of export data
							},
							'Y3'					:	{																									#!	data set 3
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 77																						#?	length of export data
							},
							'Y4'					:	{																									#!	data set 4
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 69																						#?	length of export data
							},
							'Y5'					:	{																									#!	data set 5
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 69																						#?	length of export data
							},
							'Y6'					:	{																									#!	data set 6
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 69																						#?	length of export data
							},
							'Y7'					:	{																									#!	data set 7
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 77																						#?	length of export data
							},
							'Y8'					:	{																									#!	data set 8
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 69																						#?	length of export data
							},
							'Y9'					:	{																									#!	data set 9
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 25																						#?	length of export data
							},
							'Y10'					:	{																									#!	data set 10
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 15																						#?	length of export data
							},
							'Y11'					:	{																									#!	data set 11
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 18																						#?	length of export data
							},
           					'Y12'					:	{																									#!	data set 11
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 8																							#?	length of export data
							},
                  			'Y13'					:	{																									#!	data set 11
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 148																						#?	length of export data
							}


           })

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Model Configurations

PSFBconfigs			= 	{																																	#*	PSFB components model configuration
						'ModelConfig'				: 1																									,	#?	1->Switched model | 2->Substep model | 3->Averaged model
                        'ControlConfig'    	  		: 1				  																					,   #? 	1->Peak Buck | 2->Duty Precharge | 3->Duty Boost | 4->Duty Buck | 5->Open-Loop Buck | 6->Average Peak Buck
                        'Dual_Enable'   	  		: 2				  																					,   #? 	1->Enable | 2->Disable
                        'Single_Enable' 	  		: 1				  																					,   #?  1->Enable | 2->Disable
                        'CISPR25'					: 2																									,	#?  1->Enable | 2->Disable
                        'HV_Filter'   		  		: 2				  																					,   #? 	1->With Y-Caps | 2->No Y-Caps | 3->Pass
                        'LV_Filter' 		  		: 2				  																					,   #?	1->With Y-Caps | 2->No Y-Caps | 3->Pass
                        'ShortCircuit'    	    	: 2       																							,	#?	1->MOSFET | 2->Resistive | 3->Pass
						'LV_BuffDiv'				: 1																									,	#?	1->buffered divider | 2->unbuffered divider
                        'LV_MeasLoc'				: 2																									,	#?	LV Vo measurement location, 1->before filter | 2->after filter
                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Rbox Model Configurations

RboxConfigs			=	{																																	#*	Rbox components configuartions
							'Rbox'      		  	: 3																									,	#? 	1->real | 2->complex | 3->simple | 4->ideal
                            'MainPlus' 			  	: 5																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'MainMinus' 		  	: 5																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'USMplus'   		  	: 4																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'USMminus'  		  	: 4																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'USMmid'    		  	: 5																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'DCDC'      		  	: 5                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
                            'DCplus'      		  	: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'DCminus'      		  	: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'preCharge'      		: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'OBCplus'      		  	: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'OBCminus'      		: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'ISO_en'      			: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'ISO_sw'      			: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'PyroPlus'      		: 5                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'PyroMinus'      		: 5                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'PyroAux'      			: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'DCplus_sw'      		: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'DCminus_sw'      		: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
							'USM_diag'      		: 4                         																		,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
      }

Relays				=	{																																	#*	relays configurations
							'MainPlus' 						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
							'MainMinus'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
							'USMplus'						:	dp.copy.deepcopy(Relay['PierburgHVC'])													,	#?	Relay parameters
							'USMminus'						:	dp.copy.deepcopy(Relay['PierburgHVC'])													,	#?	Relay parameters
							'USMmid'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
       						'DCDC'							:	dp.copy.deepcopy(Relay['EVRBE10UG'])													,	#?	Relay parameters
       						'DCplus'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
       						'DCminus'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
                            'preCharge'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
       						'OBCplus'						:	dp.copy.deepcopy(Relay['EVRBA50CI'])													,	#?	Relay parameters
       						'OBCminus'						:	dp.copy.deepcopy(Relay['EVRBA50CI'])													,	#?	Relay parameters
       						'ISO_en'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
       						'ISO_sw'						:	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,	#?	Relay parameters
							'PyroPlus' 						:  	dp.copy.deepcopy(Fuses['SFH400C'])														,   #? 	Relay parameters
							'PyroMinus' 					:  	dp.copy.deepcopy(Fuses['SFH400C'])														,   #? 	Relay parameters
							'PyroAux'   					:  	dp.copy.deepcopy(Fuses['SCH4KAA'])														,   #? 	Relay parameters
							'DCplus_sw'   					:  	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,   #? 	Relay parameters
							'DCminus_sw'   					:  	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,   #? 	Relay parameters
							'USM_diag'   					:  	dp.copy.deepcopy(Relay['EVRBE400CIS5'])													,   #? 	Relay parameters
      					}

DCDC_AUX			=	{																																	#*	DCDC aux supply configuration
							'Config'						:	2																						,	#?	1->enable | 2->disable
                            'Vext'							: 	0																						,	#?	external supply voltage
                            'Inductance'					:	20e-9																					,	#?	path inductance of the Aux power
							'CTRL'	:	{																													#!	CTRL board AUX parameters
                                'Lboost'					:	22e-6																					,	#?	LV boost inductance
                                'Vf_Boost'					:	1																						,	#?	LV boost diode forward voltage
                                'Rdon_Boost'				:	1e-3																					,	#?	LV boost diode ON-state resistance
								'Cx'	:	{																												#	DC link caps configuration
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	277.36e-6																				,   #?	single capacitor value
									'Rsingle'   			:	1e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	1e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'Cx_boost':	{																												#	LV boost DC link caps configuration
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	171e-6																					,   #?	single capacitor value
									'Rsingle'   			:	1e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	1e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                            	'Load'	:	{																												#	loading configuration
                                  	'Config'    			: 3																							,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
                                    'Type'	   				: 3																							,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
									'R_L'       			: 0																							,	#?	resistive-load model
									'I_L'       			: 0.85																						,	#?	current-load model
                            		'L_L'					: 0.0																						,	#?	inductive load model
                                    'Vvec'					: [6,16]																					,	#?	power load voltage vector
									'Rvec'      			: [0,0]																						,	#?	resistive-load vector
									'Ivec'     				: [1.91,0.7125]																				,	#?	constant power-load vector
                                    'Pload'					: 11.44																						,	#?	constant power load
									'OutLen'				: [1,1]																						,	#?	number of repetition of each load point
									'slpPos'				: 0																							,	#?	positive current change slope
									'slpNeg'				: 0																							,	#?	negative current change slope
                                    'Td'					: 0																							,	#?	load time delay
									'Tau'					: 0																							,	#?	time-constant of the dynamic load changes
									'Tsim'      			: simParams['tSim']						 														#?  simulation time that the load vectors is calculated with
								},
							},
                            'PeCU'	:	{																													#!	PeCU board AUX parameters
                                'Lboost'					:	22e-6																					,	#?	LV boost inductance
                                'Vf_Boost'					:	1																						,	#?	LV boost diode forward voltage
                                'Rdon_Boost'				:	1e-3																					,	#?	LV boost diode ON-state resistance
								'Cx'	:	{																												#	DC link caps configuration
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	4.7e-6																					,   #?	single capacitor value
									'Rsingle'   			:	10e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'Cx_boost':	{																												#	LV boost DC link caps configuration
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	30.7e-6																					,   #?	single capacitor value
									'Rsingle'   			:	1e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	1e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
								'C_L1'	:	{																												#	PeCU board first load caps
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	203e-6																					,   #?	single capacitor value
									'Rsingle'   			:	2e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'C_L2'	:	{																												#	PeCU board second load caps
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	10.1e-6																					,   #?	single capacitor value
									'Rsingle'   			:	2e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
								'Cy'	:	{																												#	Y-caps configuraton
                                    'Config'    			:	1																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	4.7e-9																					,   #?	single capacitor value
									'Rsingle'   			:	1+5e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	5e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'CMC'	:	{																												#	common-mode choke configuration
                                  	'Lself'     			:	1.5e-6																					,   #?	windings self inductance
									'Cwind'					:	0.0																						,	#?	intrawinding capacitance
									'Rwind'     			:	3.0e-3																					,   #?	windings resistance
									'Km'        			:	0.9841																					,   #?	coupling factor
									'Cm'					:	0.0																						,	#?	interwinding capacitance
									'Rm'	    			:	0			 																			,	#?	mutual resistance
									'N'						:	1																							#?	number of turns
								},
                            	'Load'	:	{																												#	loading configuration
                                  	'Config'    			: 3																							,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
                                    'Type'	   				: 3																							,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
									'R_L'       			: 0																							,	#?	resistive-load model
									'I_L'       			: 0.5																						,	#?	current-load model
                            		'L_L'					: 0.0																						,	#?	inductive load model
                                    'Vvec'					: [6,16]																					,	#?	power load voltage vector
									'Rvec'      			: [0,0]																						,	#?	resistive-load vector
									'Ivec'     				: [0.83,0.31]																				,	#?	constant power-load vector
                                    'Pload'					: 5.0																						,	#?	constant power load
									'OutLen'				: [1,1]																						,	#?	number of repetition of each load point
									'slpPos'				: 0																							,	#?	positive current change slope
									'slpNeg'				: 0																							,	#?	negative current change slope
                                    'Td'					: 0																							,	#?	load time delay
									'Tau'					: 0																							,	#?	time-constant of the dynamic load changes
									'Tsim'      			: simParams['tSim']						 														#?  simulation time that the load vectors is calculated with
								},
								'Lpar1'						:	27.5e-9																					,	#	PeCU board first load inductance
                                'Lpar2'						:	14e-9																					,	#	PeCU board second load inductance
							},
                            'Rbox'	:	{																													#!	Rbox AUX parameters
                                'Cx'	:	{																												#	DC link caps configuration
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	4.7e-6																					,   #?	single capacitor value
									'Rsingle'   			:	10e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'C_L1'	:	{																												#	PeSU board first load caps
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	60.2e-6																					,   #?	single capacitor value
									'Rsingle'   			:	2e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'C_L2'	:	{																												#	PeSU board second load caps
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	110.2e-6																				,   #?	single capacitor value
									'Rsingle'   			:	2e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'C_L3'	:	{																												#	PeSU board third load caps
                                    'Config'    			:	2																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	40.6e-6 																				,   #?	single capacitor value
									'Rsingle'   			:	2e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	0.6e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'Cy'	:	{																												#	Y-caps configuraton
                                    'Config'    			:	1																						,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
									'Csingle'   			:	4.7e-9																					,   #?	single capacitor value
									'Rsingle'   			:	1+5e-3																					,   #?	ESR of single capacitor
									'Lsingle'   			:	5e-9																					,   #?	ESL of single capacitor
									'nPar' 	   				:	1																						,   #?	number of parallel connections
									'nSer' 	  		 		:	1																						,   #?	number of series connections
									'Vinit'     			:	0        																					#?	capacitor initial voltage
								},
                                'CMC'	:	{																												#	common-mode choke configuration
                                  	'Lself'     			:	1.5e-6																					,   #?	windings self inductance
									'Cwind'					:	0.0																						,	#?	intrawinding capacitance
									'Rwind'     			:	3.0e-3																					,   #?	windings resistance
									'Km'        			:	0.9841																					,   #?	coupling factor
									'Cm'					:	0.0																						,	#?	interwinding capacitance
									'Rm'	    			:	0			 																			,	#?	mutual resistance
									'N'						:	1																							#?	number of turns
								},
                            	'Load'	:	{																												#	loading configuration
                                  	'Config'    			: 3																							,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
                                    'Type'	   				: 3																							,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
									'R_L'       			: 0																							,	#?	resistive-load model
									'I_L'       			: 2.60																						,	#?	current-load model
                            		'L_L'					: 0.0																						,	#?	inductive load model
                                    'Vvec'					: [6,8,10.5,13.5,17,19]																		,	#?	power load voltage vector
									'Rvec'      			: [0,0]																						,	#?	resistive-load vector
									'Ivec'     				: [11.77,8.83,6.73,5.23,4.15]																,	#?	constant power-load vector
                                    'Pload'					: 70.60																						,	#?	constant power load
									'OutLen'				: [1,1]																						,	#?	number of repetition of each load point
									'slpPos'				: 0																							,	#?	positive current change slope
									'slpNeg'				: 0																							,	#?	negative current change slope
                                    'Td'					: 0																							,	#?	load time delay
									'Tau'					: 0																							,	#?	time-constant of the dynamic load changes
									'Tsim'      			: simParams['tSim']						 														#?  simulation time that the load vectors is calculated with
								},
								'Lpar1'						:	30.75e-9																				,	#	PeSU board first load inductance
                                'Lpar2'						:	285e-9																					,	#	PeSU board second load inductance
                                'Lpar3'						:	240e-9																						#	PeSU board second load inductance
							},
                            'RPP'	:	{																													#!	reverse polarity protection switch parameters
                                'Config'					: 	2																						,	#?	1->active switch | 2->diode emulation
                                'Switch'					: 	dp.copy.deepcopy(Switches['BUK9Y6R540H'])												,	#?	active switch parameters
                                'GateDelay'					: 	750e-9																					,	#?	active switch gate-source response time
								'Vf'						: 	0.0																						,	#?	emulated diode forward voltage drop
                                'Rdon'						: 	12.35e-3																					#?	emulated diode on-state resistance
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Operation Parameters

Control				=	{																																	#*	reference and control targets
 						'LoopType'  :{																														#!	selection between closed-loop or open loop
							'TimeVec'				: [0, 1]																							,	#?	loop type time vector
							'OutVec'				: [0, 0]																								#?	loop type output vector
									},
						'Targets'	:{																														#!	control loop target values
							'Pout'     	  			: 100.0																								,	#?	Full-load power
							'Vout'        			: 10.5																								,	#?	Output reference voltage
							'Vinref'      			: 425																								,	#?	Boost reference voltage
							'Iosat1'      			: 100																								,	#?	Max inductor current at first precharge period
							'Iosat2'	  			: 150																								,	#?	Max inductor current at second precharge period
							'Iosat3'	  			: 100																								,	#?	Max inductor current during packs balancing
							'Pcmax'					: 2600																								,	#?	Maximum saturated buck output power
							'Icmax'       			: 200      																								#?	Maximum saturated buck inductor current
									},
						'Inputs'   :{																														#!	input referece values
							'Vin'        			: 400																								,	#?	constant rail input voltage
							'Vinvec'	  			: [225, 345, 355, 415]																				,	#?	variable rail input voltage
							'OutLen'				: [1, 1, 1, 1]																						,	#?	number of repetition of each Vin point
							'Vinslct'    			: 1																									,	#?	rail input voltage behavior, 1->constant Vin | 2->variable Vin
					    },
						'Modes'						: [1, 2, 2, 2]																						,	#?	Peak Buck | Duty Precharge | Duty Boost | Duty Buck | Duty Buck
						'Tsim'	      				: simParams['tSim']					 	  																#?	Simulation time that the load vectors is calculated with
						}

RailsOperation  	=	{																																	#*	rails operating modes configuration
						'Rail_1'  :	{																														#! rail 1 (lower rail) configuration
							'Trigger1_TimeVec'	  	:	[0, 1]																							,	#? mode 1 selection time vector
							'Trigger1_OutVec'	  	:	[1, 1]																							,	#? mode 1 selection status vector, 0->inactive | 1->active
							'Trigger2_TimeVec'	  	:	[0, 1]																							,	#? mode 2 selection time vector
							'Trigger2_OutVec'	  	:	[0, 0]																							,	#? mode 2 selection status vector, 0->inactive | 1->active
							'Trigger3_TimeVec'	  	:	[0, 1]																							,	#? mode 3 selection time vector
							'Trigger3_OutVec'	  	:	[0, 0]																							,	#? mode 3 selection status vector, 0->inactive | 1->active
							'Trigger4_TimeVec'	  	:	[0, 1]																							,	#? mode 4 selection time vector
							'Trigger4_OutVec'	  	:	[0, 0]																								#? mode 4 selection status vector, 0->inactive | 1->active
									},

						'Rail_2'  :	{																														#! rail 2 (upper rail) configuration
							'Trigger1_TimeVec'	  	:	[0, 1]																							,	#? mode 1 selection time vector
							'Trigger1_OutVec'	  	:	[1, 1]																							,	#? mode 1 selection status vector, 0->inactive | 1->active
							'Trigger2_TimeVec'	  	:	[0, 1]																							,	#? mode 2 selection time vector
							'Trigger2_OutVec'	  	:	[0, 0]																							,	#? mode 2 selection status vector, 0->inactive | 1->active
							'Trigger3_TimeVec'	  	:	[0, 1]																							,	#? mode 3 selection time vector
							'Trigger3_OutVec'	  	:	[0, 0]																							,	#? mode 3 selection status vector, 0->inactive | 1->active
							'Trigger4_TimeVec'	  	:	[0, 1]																							,	#? mode 4 selection time vector
							'Trigger4_OutVec'	  	:	[0, 0]																								#? mode 4 selection status vector, 0->inactive | 1->active
									}
						}

Initials			=	{																																	#*	input/output initial voltages
							'Vout'     				: 0.0			   																					,	#?	Initial LV capacitors voltages
							'Vin'      				: Control['Inputs']['Vin'] 																				#?	Initial HV capacitors voltages
						}

Protection  		=	{																																	#*	HW protection thresholds
							'VinMin'    			: 150			        																			,	#?	Min input voltage before UVLO
							'VinMax'    			: 470			        																			,	#?	Max input voltage before OVLO
							'VoMax'     			: 35																								,	#?	Max output voltage before OVLO
							'IoMax'     			: 450	    		    																			,	#?	Max inductor current before OC protection
							'IoMin'     			: -450	    		    																			,	#?	Min inductor current before OC protection
							'IinMax'    			: 25		    		   																			,	#?	Max HV current before OC protection
							'IinMin'    			: -25		    		   																				#?	Min HV current before OC protection
						}

Load 				=	{																																	#*	loading behavior
							'Front'		:	{																												#!	vehicle front load parameters
								'Config'    			: 2																								,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
								'Type'	   				: 1																								,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
								'R_L'       			: 2.0*Control['Targets']['Vout']**2/Control['Targets']['Pout']									,	#?	resistive-load model
								'I_L'       			: 0.5*Control['Targets']['Pout']/Control['Targets']['Vout']										,	#?	current-load model
                            	'L_L'					: 1.0e-9																						,	#?	inductive load model
                                'Vvec'					: [0,0]																							,	#?	power load voltage vector
								'Rvec'      			: [0,0]																							,	#?	resistive-load vector
								'Ivec'     				: [0,0]																							,	#?	current-load vector
                                'Pload'					: 0.5*Control['Targets']['Pout']																,	#?	constant power load
								'OutLen'				: [1,1]																							,	#?	number of repetition of each load point
								'slpPos'				: 500e3																							,	#?	positive current change slope
								'slpNeg'				: -500e3																						,	#?	negative current change slope
                                'Td'					: 0																								,	#?	load time delay
								'Tau'					: 75e-6																							,	#?	time-constant of the dynamic load changes
								'Tsim'      			: simParams['tSim']						 															#?  simulation time that the load vectors is calculated with
							},
                            'Back'		:	{																												#!	vehicle back load parameters
								'Config'    			: 2																								,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
								'Type'	   				: 1																								,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
								'R_L'       			: 2.0*Control['Targets']['Vout']**2/Control['Targets']['Pout']									,	#?	resistive-load model
								'I_L'       			: 0.5*Control['Targets']['Pout']/Control['Targets']['Vout']										,	#?	current-load model
                            	'L_L'					: 1.0e-9																						,	#?	inductive load model
								'Vvec'					: [0,0]																							,	#?	power load voltage vector
								'Rvec'      			: [0,0]																							,	#?	resistive-load vector
								'Ivec'     				: [0,0]																							,	#?	current-load vector
                                'Pload'					: 0.5*Control['Targets']['Pout']																,	#?	constant power load
								'OutLen'				: [1,1]																							,	#?	number of repetition of each load point
								'slpPos'				: 500e3																							,	#?	positive current change slope
								'slpNeg'				: -500e3																						,	#?	negative current change slope
                                'Td'					: 0																								,	#?	load time delay
								'Tau'					: 75e-6																							,	#?	time-constant of the dynamic load changes
								'Tsim'      			: simParams['tSim']						 															#?  simulation time that the load vectors is calculated with
							}
						}

RailsEnable 		=	{																																	#*	rails enabling configurations
							'Rail_1'  :	{																													#!	rail 1 (lower rail) configuration
								'TimeVec_Buck'					:	[0, simParams['tStart'], 1]															,	#?	buck mode activation time vector
								'OutVec_Buck'					:	[0, 1, 1]																			,	#? 	buck mode status 0->disabled | 1->enabled
								'TimeVec_Precharge'				:	[0, 1]																				,	#?	precharge mode activation time vector
								'OutVec_Precharge'				:	[0, 0]																				,	#?	precharge mode status 0->disabled | 1->enabled
								'TimeVec_Boost'					:	[0, 1]																				,	#?	boost mode activation time vector
								'OutVec_Boost'					:	[0, 0]																					#?	boost mode status 0->disabled | 1->enabled
										},
							'Rail_2'  :	{																													#!	rail 2 (upper rail) configuration
								'TimeVec_Buck'					:	[0, simParams['tStart'], 1]															,	#?	buck mode activation time vector
								'OutVec_Buck'					:	[0, 1, 1]																			,	#? 	buck mode status 0->disabled | 1->enabled
								'TimeVec_Precharge'				:	[0, 1]																				,	#?	precharge mode activation time vector
								'OutVec_Precharge'				:	[0, 0]																				,	#?	precharge mode status 0->disabled | 1->enabled
								'TimeVec_Boost'					:	[0, 1]																				,	#?	boost mode activation time vector
								'OutVec_Boost'					:	[0, 0]																					#?	boost mode status 0->disabled | 1->enabled
												}
						}

DualSingleOperation	=	{
							'Slope'								:	0.05																				,
							'Ramping'	:	{
								'TimeVec'						:	[0, 1]																				,
								'OutVec'						:	[0, 0]
											},
							'Thresholds':	{
								'Upper'							:	70.0																				,
								'Lower'							:	40.0
											}
						}

shortCircuit		=	{																																	#*	short-circuit events behavior
							'HV'		:	{																												#!	HV side short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
								'Ron'							:	1e-3																				,	#?	short-circuit impedance
								'Roff'							:	1e9																					,	#?	open-circuit impedance
								'L'								:	1e-9																				,	#?	short-circuit inductance
								'tau'							:	40e-9																				,	#?	short-circuit event time constant
								'TimeVec'						:	[0, 1]																				,	#?	time vector for activation of short-circuit event
								'OutVec'						:	[0, 0]																					#?	enable vector for activation of short-circuit event
								},
							'LV'		:	{																												#!	LV side short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
								'Ron'							:	1e-3																				,	#?	short-circuit impedance
								'Roff'							:	1e-3																				,	#?	open-circuit impedance
								'L'								:	1e-9																				,	#?	short-circuit inductance
								'tau'							:	40e-9																				,	#?	short-circuit event time constant
								'TimeVec'						:	[0, 1]																				,	#?	time vector for activation of short-circuit event
								'OutVec'						:	[0, 0]																					#?	enable vector for activation of short-circuit event
								},
							'Trafo'		:	{																												#!	Transformer primary short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->Short
								'Ron'							:	1e-3																				,	#?	short-circuit impedance
								'Roff'							:	1e-3																				,	#?	open-circuit impedance
								'L'								:	1e-9																				,	#?	short-circuit inductance
								'tau'							:	40e-9																				,	#?	short-circuit event time constant
								'TimeVec'						:	[0, 1]																				,	#?	time vector for activation of short-circuit event
								'OutVec'						:	[0, 0]																					#?	enable vector for activation of short-circuit event
								},
						}

SC_Switch_Control	=	{																																	#*	short-circuit eFuse (switch) control
							'TimeVec'							:	[0, 1]																				,	#? 	time vector for activation of short-circuit switch
							'OutVec'							:	[1, 1]																					#? 	enable vector for activation of short-circuit switch
						}

loadShifting		=	{																																	#*	load shifting hysteresis behavior
							'Slope'								:	0.05																				,	#?	rate of change of load-shifting factor per switching period
							'Mode'								:	1																					,	#?	1->manual shift | 2->DualSingle operation | 3->EIS
							'Direction'	:	{																												#!	load shifting direction parameters
								'TimeVec'						:	[0, 1]																				,	#?	load shifting direction time vector
								'OutVec'						:	[0, 0]																					#?	load shifting direction, 0->shift to rail 2 | 1->shift to rail 1
											},
							'Shift'		:	{																												#!	load shifting activation parameters
								'TimeVec'						:	[0, 1]																				,	#?	load shifting activation time vector
								'OutVec'						:	[0, 0]																					#?	load shifting activation, 0->disabled | 1->enabled
											},
							'Factor'							:	[0, 0]																				,	#?	load-shifting percentage factor
							'OutLen'							:	[1, 1]																				,	#?	number of repetition of each shift point
							'Tprd'								:	simParams['tSim']																		#?	simulation time that the shift vectors is calculated with
						}

EIS 				=	{																																	#*	EIS control law
							'SetRest'	:	{																												#!	search process control
												'TimeVec'		:	[0, 1]																				,	#?	search process enable time vector
												'OutVec'		:	[0, 0]																					#?	search process status vector, 0->Disable | 1->Enable
											},
							'Amplitude'	:	{																												#!	excitation amplitide control
												'Amp'			:	[5, 5]																				,	#?	current amplitude
												'OutLen'		:	[1, 1]																					#?	number of repetition of each amplitude point
											},
							'Frequency'	:	{																												#!	excitation frerquency control
												'Freq'			:	[1e3, 1e3]																			,	#?	current frerquency
												'OutLen'		:	[1, 1]																					#?	number of repetition of each frerquency point
											},
							'Slope'								:	0.001																				,	#?	duty cycle ramp per 10us during the searching process
							'Direction'							:	2																					,	#?	select which rail is the master, 1->Rail 1 | 2->Rail 2
							'Tprd'								:	simParams['tSim']																		#?	simulation time that the EIS vectors is calculated with
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Parameters

HVfuse				= 	dp.copy.deepcopy(Fuses['MEV55C'])																									#*	HV input fuse
PyroFuse			=	dp.copy.deepcopy(Fuses['SFH400C'])																									#*	Rbox pyro fuse

HVcmc				=	{																																	#*	HV CMC choke parameters
							'Config'				:	1																								,	#?	1->positively coupled | 2->negatively coupled | 3->pass
							'Lself'     			:	0.47e-3																							,   #?	windings self inductance
							'Cwind'					:	0.0																								,	#?	intrawinding capacitance
							'Rwind'     			:	8.0e-3																							,   #?	windings resistance
							'Km'        			:	0.99436																							,   #?	coupling factor
							'Cm'					:	0.0																								,	#?	interwinding capacitance
							'Rm'	    			:	0			 																					,	#?	mutual resistance
							'N'						:	1																									#?	number of turns
						}

Cin 				=	{																																	#*	HV input capacitor parameters
							'Config'    			:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	0																								,   #?	single capacitor value
							'Rsingle'   			:	0																								,   #?	ESR of single capacitor
							'Lsingle'   			:	0																								,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	  		 		:	1																								,   #?	number of series connections
							'Vinit'     			:	Initials['Vin']        																			,	#?	capacitor initial voltage
                            'Rd'					:	"inf"																							,	#?	parallel discharge resistor
						}

Cpi 				=	{																																	#*	HV Pi capacitor parameters
							'Config'    			:	2																								, 	#?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	5e-6																							,	#?	single capacitor value
							'Rsingle'   			:	24.5e-3																							,	#?	ESR of single capacitor
							'Lsingle'   			:	27.5e-9																							,	#?	ESL of single capacitor
							'nPar' 	   				:	2						 																		,  	#?	number of parallel connections
							'nSer' 	  		 		:	1																								, 	#?	number of series connections
							'Vinit'     			:	Initials['Vin']        																			,	#?	capacitor initial voltage
                            'Rd'					:	"inf"																							,	#?	parallel discharge resistor
						}

Cyi					= 	{																																	#*	HV Y-capacitors parameters
							'Config'    			:	2																								,	#?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	3.3e-9																							,	#?	single capacitor value
							'Rsingle'   			:	2.8  																							,	#?	ESR of single capacitor
							'Lsingle'   			:	15e-9																							,	#?	ESL of single capacitor
							'nPar' 	  	 			:	1																								,	#?	number of parallel connections
							'nSer' 	   				:	1																								,	#?	number of series connections
							'Vinit'     			:	Initials['Vin']	       																				#?	capacitor initial voltage
						}

Cc					= 	{																																	#*	HV snubber capacitors parameters
							'Config'    			:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	4e-6																							,   #?	single capacitor value
							'Rsingle'   			:	23.0e-3																							,   #?	ESR of single capacitor
							'Lsingle'   			:	16.2e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	  		 		:	1																								,   #?	number of series connections
							'Vinit'     			:	Initials['Vin']		       																			#?	capacitor initial voltage
						}

Trafo				=	dp.copy.deepcopy(Mags['Cyntec_C20_Trafo'])																							#*	main transformer parameters

Cb					= 	{																																	#*	transformer blocking capacitor parameters
							'Config'    			:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	10e-6																							,   #?	single capacitor value
							'Rsingle'   			:	6.2e-3																							,   #?	ESR of single capacitor
							'Lsingle'   			:	1e-9																							,   #?	ESL of single capacitor
							'nPar' 	    			:	6																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0				                																    #?	capacitor initial voltage
						}

RCsnubber		=		{																																	#*	RC snubbers parameters
						'SR_MOSFET'	:	{																													#!	SR MOSFETs RC snubbers parameters
							'Config'				:	2																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	0																								,	#?	resistance value
								'nPar'				:	1																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	0																								,   #?	single capacitor value
								'Rsingle'   		:	0																								,   #?	ESR of single capacitor
								'Lsingle'   		:	0																								,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							}
						},
                        'PS_MOSFET'	:	{																													#!	SR MOSFETs RC snubbers parameters
							'Config'				:	2																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	0																								,	#?	resistance value
								'nPar'				:	1																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	0																								,   #?	single capacitor value
								'Rsingle'   		:	0																								,   #?	ESR of single capacitor
								'Lsingle'   		:	0																								,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							}
						},
                        'LV_FB'		:	{																													#!	LV full-bridge RC snubbers parameters
							'Config'				:	1																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	10																								,	#?	resistance value
								'nPar'				:	2																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	1.0e-9																							,   #?	single capacitor value
								'Rsingle'   		:	10e-3																							,   #?	ESR of single capacitor
								'Lsingle'   		:	0.0																								,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							}
						},
						'HV_FB'		:	{																													#!	HV full-bridge RC snubbers parameters
							'Config'				:	2																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	2.2																								,	#?	resistance value
								'nPar'				:	1																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	5.0e-9																							,   #?	single capacitor value
								'Rsingle'   		:	200e-3																							,   #?	ESR of single capacitor
								'Lsingle'   		:	1.5e-9																							,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							}
						},
						'Choke'		:	{																													#!	choke RC snubbers parameters
							'Config'				:	2																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	0																								,	#?	resistance value
								'nPar'				:	1																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	4																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	0																								,   #?	single capacitor value
								'Rsingle'   		:	0																								,   #?	ESR of single capacitor
								'Lsingle'   		:	0																								,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							},
							'Rpar'					:	0																									#?	snubber capacitor parallel resistance
						},
						'Trafo'		:	{																													#!	trafo RC snubbers parameters
							'Config'				:	2																								,	#	1->Enable | 2->Disable
							'Rs'		:	{																												#	snubber resistors
								'R'					:	0																								,	#?	resistance value
								'nPar'				:	1																									#?	number of parallel resistors
							},
							'Cs'		:	{																												#	snubber capacitors
								'Config'    		:	4																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
								'Csingle'   		:	0																								,   #?	single capacitor value
								'Rsingle'   		:	0																								,   #?	ESR of single capacitor
								'Lsingle'   		:	0																								,   #?	ESL of single capacitor
								'nPar' 	    		:	1																								,   #?	number of parallel connections
								'nSer' 	    		:	1																								,   #?	number of series connections
								'Vinit'     		:	0																									#?	capacitor initial voltage
							}
						}
					}

RCDclamp		= 	{																																		#*	RCD clamp parameters
						'Config'					:	1																								,	#!	1->Enable | 2->Disable
                        'Rs'		:	{																											        #!	snubber resistors
							'R'						:	'1.5e3'																							,	#?	resistance value
						},
						'Cs'		:	{																										            #!	snubber capacitors
							'Config'    			:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	1.41e-6																							,   #?	single capacitor value
							'Rsingle'   			:	8.046e-3																						,   #?	ESR of single capacitor
							'Lsingle'   			:	15e-9																							,   #?	ESL of single capacitor
							'nPar' 	    			:	6																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0																									#?	capacitor initial voltage
						},
                        'Switch'     				:	dp.copy.deepcopy(Switches['NVMFS3D6N10MCL'])													,	#?	clamp switch
					}

ERCclamp 		=	{																																		#*	energy recovery clamp parameters
                        'Config'					:	2																								,	#!	1->Enable | 2->Disable
						'Diode'     :  {																													#! diode parameters
							'Vf'       				:	0.58																							,   #?	diode forward voltage
							'Rdon'     				:	100e-3																							   	#?	diode on-state resistance
						},
						'Cs'		:	{																										            #!	snubber capacitors
							'Config'    			:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	1e-6																					    	,   #?	single capacitor value
							'Rsingle'   			:	10e-3																							,   #?	ESR of single capacitor
							'Lsingle'   			:	0.0																								,   #?	ESL of single capacitor
							'nPar' 	    			:	1																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0																									#?	capacitor initial voltage
						},
                      }

FRW				=		{																																	#*	freewheeler parameters
						'Config'					:	2																								,	#?	1->enable | 2->disable
						'Switch'					: 	dp.copy.deepcopy(Switches['NVMFS3D6N10MCL'])													,	#?	freewheeling switch parameters
						'BlockingCap'	:	{																												#!	blocking capacitor parameters
							'Config'    			:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	0																								,   #?	single capacitor value
							'Rsingle'   			:	0																								,   #?	ESR of single capacitor
							'Lsingle'   			:	0																								,   #?	ESL of single capacitor
							'nPar' 	    			:	1																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0				                																    #?	capacitor initial voltage
						},
						'ImpedanceCap'	:	{																												#!	impedance-matching capacitor parameters
							'Config'    			:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	0																								,   #?	single capacitor value
							'Rsingle'   			:	0																								,   #?	ESR of single capacitor
							'Lsingle'   			:	0																								,   #?	ESL of single capacitor
							'nPar' 	    			:	1																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0				                																    #?	capacitor initial voltage
						},
						'Resistor'		:	{																												#!	freewheeling resistor paramters
							'R'						:	0																								,	#?	freewheeling resistance value
							'L'						:	0.0																									#?	parasitic inductance
						}
					}

Lf					= 	dp.copy.deepcopy(Mags['Cyntec_C20_Choke'])																							#*	LC filter output choke parameters

RCDsnubber			= 	{																																	#*	RCD snubber configuration
							'Vf'       				:	0.58																							,   #?	diode forward voltage
							'Rdon'     				:	250e-3																							,   #?	diode on-state resistance
							'Cs'       				:	10e-9																							,   #?	snubber capacitance
							'Rs'       				:	1.1e3																							    #?	snubber resistance
						}

Co					=	{																																	#*	LC filter cermaic capacitors parameters
							'Config'   				:	2				   																				,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	5.5e-6   																						,   #?	single capacitor value
							'Rsingle'  				:	4e-3  																							,   #?	ESR of single capacitor
							'Lsingle'  				:	1.11e-9			   																				,   #?	ESL of single capacitor
							'nPar' 	   				:	12																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Coe1				= 	{																																	#*	LC filter electrolytic capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	270e-6																							,   #?	single capacitor value
							'Rsingle'  				:	20e-3																							,   #?	ESR of single capacitor
							'Lsingle'  				:	10e-9																							,   #?	ESL of single capacitor
							'nPar' 	  				:	1																								,   #?	number of parallel connections
							'nSer' 	  				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']																				,   #?	capacitor initial voltage
							'Rd'	   				:	50e-3			                																    #?	damping resistor
						}

InductancesPCB		=	{																																	#*	PCB parasitic inductances
							'HV_Bridge'		:	{																											#!	parasitic inductances related to HV bridge
                                'LeftLeg'			:	0																								,	#	inductances between HS and LS of left leg
                                'RightLeg'			:	0																								,	#	inductances between HS and LS of right leg
								'Drain'	:	{																												#!	parasitic inductance in series to half-bridge drain
                                    'RL'			:	0																								,	#?	right leg drain parasitic inductance
                                    'LL'			:	0																									#?	left leg drain parasitic inductance
								},
                                'Source':	{																												#!	parasitic inductance in series to half-bridge source
                                    'RL'			:	0																								,	#?	right leg drain parasitic inductance
                                    'LL'			:	0																									#?	left leg drain parasitic inductance
								},
							},
                            'LV_Bridge'		:	{																											#!	parasitic inductances related to LV bridge
                                'LeftLeg'			:	0																								,	#	inductances between HS and LS of left leg
                                'RightLeg'			:	0																								,	#	inductances between HS and LS of right leg
								'Drain'	:	{																												#!	parasitic inductance in series to half-bridge drain
                                    'RL'			:	0																								,	#?	right leg drain parasitic inductance
                                    'LL'			:	0																									#?	left leg drain parasitic inductance
								},
                                'Source':	{																												#!	parasitic inductance in series to half-bridge source
                                    'RL'			:	0																								,	#?	right leg drain parasitic inductance
                                    'LL'			:	0																									#?	left leg drain parasitic inductance
								},
							},
                            'B_plus'		:	{																											#!	B plus inline parasitic inductance
                                'Rail_1'			:	0																								,	#?	rail 1 inline resistance
                                'Rail_2'			:	0																								,	#?	rail 2 inline resistance
                                'Common'			:	0																									#?	shared resistance between two rails
							},
                            'B_minus'		:	{																											#!	B minus inline parasitic inductance
                                'Rail_1'			:	0																								,	#?	rail 1 inline resistance
                                'Rail_2'			:	0																								,	#?	rail 2 inline resistance
                                'Common'			:	0																									#?	shared resistance between two rails
							},
                            'LV_Filter'		:	{																											#!	LV filter terminal connections parasitic inductance
                                'Plus_Terminal_1'	:	0																								,	#?	first filter plus terminal
                                'Plus_Terminal_2'	:	0																								,	#?	second filter plus terminal
                                'Plus_Terminal_3'	:	0																								,	#?	Third filter plus terminal
                                'Minus_Terminal_1'	:	0																								,	#?	first filter negative terminal
                                'Minus_Terminal_2'	:	0																								,	#?	second filter negative terminal
                                'Minus_Terminal_3'	:	0																								,	#?	Third filter negative terminal
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------LV Filter Parameters

LVdmc				= 	{																																	#*	LV DMC choke parameters
							'Config'				:	1																								,	#?	1->positively coupled | 2->negatively coupled | 3->pass
							'Lself' 				:	1.08e-6																							,   #?	windings self inductance
							'Cwind'					:	0.0																								,	#?	intrawinding capacitance
							'Rwind'					:	0.0																								,   #?	windings resistance
							'Km'    				:	0.92592																							,  	#?	coupling factor
							'Cm'					:	0.0																								,	#?	interwinding capacitance
							'Rm'					:	0			 		            																,   #?	mutual resistance
							'N'						:	1																									#?	number of turns
						}

LVcmc				= 	{																																	#*	LV CMC choke parameters
							'Config'				:	1																								,	#?	1->positively coupled | 2->negatively coupled | 3->pass
							'Lself' 				:	10e-6																							,   #?	windings self inductance
							'Cwind'					:	0.0																								,	#?	intrawinding capacitance
							'Rwind' 				:	0.0			  																					,   #?	windings resistance
							'Km'    				:	0.999																							,   #?	coupling factor
							'Cm'					:	0.0																								,	#?	interwinding capacitance
							'Rm'					:	0			 		            																,   #?	mutual resistance
							'N'						:	1																									#?	number of turns
						}

Coc1				=	{																																	#*	LV filter first ceramic capacitors parameters
							'Config'   				:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	0																								,   #?	single capacitor value
							'Rsingle'  				:	0																								,   #?	ESR of single capacitor
							'Lsingle'  				:	0																								,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	0	            																    				#?	capacitor initial voltage
						}

Coc2				=	{																																	#*	LV filter second ceramic capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	7.5e-6																							,   #?	single capacitor value
							'Rsingle'  				:	4e-3																							,   #?	ESR of single capacitor
							'Lsingle'  				:	1.1e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	10																								,   #?	number of parallel connections
							'nSer' 	   				:	2																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Coc3				=	{																																	#*	LV filter third ceramic capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	7.5e-6																							,   #?	single capacitor value
							'Rsingle'  				:	4e-3																							,   #?	ESR of single capacitor
							'Lsingle'  				:	1.1e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	10																								,   #?	number of parallel connections
							'nSer' 	   				:	2																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Coec1				= 	{																																	#*	LV filter first electrolytic capacitors parameters
							'Config'   				:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	0																								,   #?	single capacitor value
							'Rsingle'  				:	0																								,   #?	ESR of single capacitor
							'Lsingle'  				:	0																								,   #?	ESL of single capacitor
							'nPar' 	  				:	1																								,   #?	number of parallel connections
							'nSer' 	  				:	1																								,   #?	number of series connections
							'Vinit'    				:	0																								,   #?	capacitor initial voltage
							'Rd'	   				:	0				                																    #?	damping resistor
						}

Coec2				= 	{																																	#*	LV filter second electrolytic capacitors parameters
							'Config'   				:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	0																								,   #?	single capacitor value
							'Rsingle'  				:	0																								,   #?	ESR of single capacitor
							'Lsingle'  				:	0																								,   #?	ESL of single capacitor
							'nPar' 	  				:	1																								,   #?	number of parallel connections
							'nSer' 	  				:	1																								,   #?	number of series connections
							'Vinit'    				:	0																								,   #?	capacitor initial voltage
							'Rd'	   				:	0				                																    #?	damping resistor
						}

Coec3				= 	{																																	#*	LV filter third electrolytic capacitors parameters
							'Config'   				:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	0																								,   #?	single capacitor value
							'Rsingle'  				:	0																								,   #?	ESR of single capacitor
							'Lsingle'  				:	0																								,   #?	ESL of single capacitor
							'nPar' 	  				:	1																								,   #?	number of parallel connections
							'nSer' 	  				:	1																								,   #?	number of series connections
							'Vinit'    				:	0																								,   #?	capacitor initial voltage
							'Rd'	   				:	0				                																    #?	damping resistor
						}

Cyo					=	{																																	#*	LC filter Y-capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	10e-6																							,   #?	single capacitor value
							'Rsingle'  				:	4.0e-3+1																						,   #?	ESR of single capacitor
							'Lsingle'  				:	1e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Cyoc				=	{																																	#*	LV filter Y-capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	10.0e-9																							,   #?	single capacitor value
							'Rsingle'  				:	4.0e-3+1																						,   #?	ESR of single capacitor
							'Lsingle'  				:	1e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Busbars_PCB			=	{																																	#*	PCB traces and/or busbars resistances
							'LV_Filter'		:	{																											#!	LV filter inline resistances
                                'PlusResistance'		:	96.00e-6 + 167e-6 + 60e-6																	,	#?	positive line resistance
								'MinusResistance'		:	132.4e-6 + 148e-6 + 60e-6																	,	#?	negative line resistance
                                'Plus_Terminal_1'		:	0																							,	#?	first filter plus terminal
								'Plus_Terminal_2'		:	12.7e-3																						,	#?	second filter plus terminal
								'Plus_Terminal_3'		:	13.0e-3																						,	#?	Third filter plus terminal
								'Minus_Terminal_1'		:	0																							,	#?	first filter negative terminal
								'Minus_Terminal_2'		:	13.0e-3																						,	#?	second filter negative terminal
								'Minus_Terminal_3'		:	13.0e-3																							#?	Third filter negative terminal
							},
                            'B_plus'		:	{																											#!	B plus inline resistances
                                'Rail_1'				:	300e-6																						,	#?	rail 1 inline resistance
                                'Rail_2'				:	100e-6																						,	#?	rail 2 inline resistance
                                'Common'				:	0																								#?	shared resistance between two rails
							},
                            'B_minus'		:	{																											#!	B minus inline resistances
                                'Rail_1'				:	200e-6																						,	#?	rail 1 inline resistance
                                'Rail_2'				:	500e-6																						,	#?	rail 2 inline resistance
                                'Common'				:	0																								#?	shared resistance between two rails
							},
                            'SR_LC'			:	{																											#!	rectifier bridge to LC filter inline resistance
                                'PlusResistance'		:	1.031e-3																					,	#?	positive line resistance
                                'MinusResistance'		:	0																								#?	negative line resistance
							},
                            'Trafo_SR'		:	{																											#!	trafo to rectifier bridge inline resistance
                                'PlusResistance'		:	0.104e-3																					,	#?	positive line resistance
                                'MinusResistance'		:	0.18e-3																							#?	negative line resistance
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------EnBn Parameters

LVS					=	{																																	#*	LV battery parameters
							'Config'   				:	2																								,   #? 	1->complex | 2>-simple | 3->disable
							'V'        				:	Control['Targets']['Vout'] - 50e-3																,   #?	battery voltage
							'R'        				:	5e-3			     		 	 																,	#?	internal battery resistance
                            'Ext'	:	{																													#!	external supply profile
                                'Config'			:	1																								,	#?	1->constant voltage | 2->external pulse
                                'Prd'				:	0																								,	#?	period length of external pulse
                                'Filename'			:	''																								,	#?	external pulse filename
							},
                            'Cell'	:	{																													#!	battery cell parameters
								'Model'				:	dp.copy.deepcopy(Battery['CAMEL_230906_new_BOL'])												,	#?	cell electrical parameters
								'InitSoC'			:	0.85																							,	#?	initial state of charge of cells
                                'RsConfig'			:	1																								,	#?	variable resistor config, 1->VS model | 2->IS Model
								'Cnom'				:	22																								,	#?	nominal cell capacity in Ah
                                'nParallel'			:	1																								,	#?	number of parallel cells
                                'nSeries'			:	4																								,	#?	number of series cells
								'Temp'				:	25																									#?	initial battery temperature
							}
						}

EnBn				= 	{																																	#*	LV Bordnetz parameters
							'Config'   				:	2																								,   #?	1->complex model | 2->simple model | 3->pass
                            'Vinit'					:	0																								,	#?	initial voltage
							'R'        				:	5e-3																							,   #?	lumped resistance
							'L'        				:	2.5e-6																							,   #?	lumped inductance
							'C'       			:	{																										#*	lumped capacitance
								'Config'   			:	1																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
								'Csingle'  			:	10e-3																							,   #?	single capacitor value
								'Rsingle'  			:	0																								,   #?	ESR of single capacitor
								'Lsingle'  			:	0																								,   #?	ESL of single capacitor
								'nPar' 	  			:	1																								,   #?	number of parallel connections
								'nSer' 	  			:	1																								,   #?	number of series connections
								'Vinit'    			:	0																								   	#?	capacitor initial voltage
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Rbox Parameters

HVS					= 	{																																	#*	LV Bordnetz parameters
							'Config'        		: 	2               																				,   #?	1->Inductive Model | 2->Resistive Model
							'Rcell'         		:	0.6e-3			  		 																		,   #? 	single-cell resistance
							'Lcell'         		:	80e-9																							,   #? 	single-cell inductance
							'SeriesCells'   		:	100																								,   #? 	number of series battery cells
							'ParallelCells'	 		:	1					 	        																 	#? 	number of parallel battery cells
						}

Cdc					=	{																																	#*	vehicle DC link parameters
							'Config'    			: 2				  																					,   #? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'   			: 430e-6		  																					,   #? 	Single Capacitor Size
							'Rsingle'   			: 50e-6			  																					,   #? 	Single Capacitor ESR
							'Lsingle'   			: 1e-9			  																					,   #?	Single Capacitor ESL
							'nPar' 	    			: 1				  																					,   #?	Parallel Branches
							'nSer' 	    			: 1				  																					,   #?	Series Branches
							'Vinit'     			: 0				  																					,   #?	Initial Voltage
							'Load'	:	{
                                'Config'    			: 6																								,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
								'Type'	   				: 4																								,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
								'R_L'       			: 250e3																							,	#?	resistive-load model
								'I_L'       			: 0.13																							,	#?	current-load model
                            	'L_L'					: 0																								,	#?	inductive load model
                                'Vvec'					: [20,850]																						,	#?	power load voltage vector
								'Rvec'      			: [0,0]																							,	#?	resistive-load vector
								'Ivec'     				: [0,0]																							,	#?	current-load vector
                                'Pload'					: 50																							,	#?	constant power load
								'OutLen'				: [1,1]																							,	#?	number of repetition of each load point
								'slpPos'				: 0																								,	#?	positive current change slope
								'slpNeg'				: 0																								,	#?	negative current change slope
                                'Td'					: 0																								,	#?	load time delay
								'Tau'					: 0																								,	#?	time-constant of the dynamic load changes
								'Tsim'      			: 1										 															#?  simulation time that the load vectors is calculated with
							}
						}

Cobc					=	{																																#*	OBC DC link parameters
							'Config'    			: 2				  																					,   #? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->Pass
							'Csingle'   			: 100e-6		  																					,   #? 	Single Capacitor Size
							'Rsingle'   			: 50e-6			  																					,   #? 	Single Capacitor ESR
							'Lsingle'   			: 1e-9			  																					,   #?	Single Capacitor ESL
							'nPar' 	    			: 1				  																					,   #?	Parallel Branches
							'nSer' 	    			: 1				  																					,   #?	Series Branches
							'Vinit'     			: 0				  																					,   #?	Initial Voltage
							'Load'	:	{
                                'Config'    			: 6																								,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
								'Type'	   				: 4																								,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
								'R_L'       			: 250e3																							,	#?	resistive-load model
								'I_L'       			: 0.13																							,	#?	current-load model
                            	'L_L'					: 0																								,	#?	inductive load model
                                'Vvec'					: [20,850]																						,	#?	power load voltage vector
								'Rvec'      			: [0,0]																							,	#?	resistive-load vector
								'Ivec'     				: [0,0]																							,	#?	current-load vector
                                'Pload'					: 50																							,	#?	constant power load
								'OutLen'				: [1,1]																							,	#?	number of repetition of each load point
								'slpPos'				: 0																								,	#?	positive current change slope
								'slpNeg'				: 0																								,	#?	negative current change slope
                                'Td'					: 0																								,	#?	load time delay
								'Tau'					: 0																								,	#?	time-constant of the dynamic load changes
								'Tsim'      			: 1										 															#?  simulation time that the load vectors is calculated with
							}
						}

Ccharge					=	{																																#*	DC charging DC link parameters
							'Config'    			: 2				  																					,   #? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->Pass
							'Csingle'   			: 100e-6		  																					,   #? 	Single Capacitor Size
							'Rsingle'   			: 50e-6			  																					,   #? 	Single Capacitor ESR
							'Lsingle'   			: 1e-9			  																					,   #?	Single Capacitor ESL
							'nPar' 	    			: 1				  																					,   #?	Parallel Branches
							'nSer' 	    			: 1				  																					,   #?	Series Branches
							'Vinit'     			: 0				  																					,   #?	Initial Voltage
							'Load'	:	{
                                'Config'    			: 6																								,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
								'Type'	   				: 4																								,	#?	1->ohmic load | 2->current load | 3->power load | 4->pass
								'R_L'       			: 250e3																							,	#?	resistive-load model
								'I_L'       			: 0.13																							,	#?	current-load model
                            	'L_L'					: 0																								,	#?	inductive load model
                                'Vvec'					: [20,850]																						,	#?	power load voltage vector
								'Rvec'      			: [0,0]																							,	#?	resistive-load vector
								'Ivec'     				: [0,0]																							,	#?	current-load vector
                                'Pload'					: 50																							,	#?	constant power load
								'OutLen'				: [1,1]																							,	#?	number of repetition of each load point
								'slpPos'				: 0																								,	#?	positive current change slope
								'slpNeg'				: 0																								,	#?	negative current change slope
                                'Td'					: 0																								,	#?	load time delay
								'Tau'					: 0																								,	#?	time-constant of the dynamic load changes
								'Tsim'      			: 1										 															#?  simulation time that the load vectors is calculated with
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PWM Parameters

MCU					= 	{																																	#*	microcontroller timings parameters
							'f_pwm'         		:	200e6																							,   #? 	PWM module frequency
							'f_s'           		:	100e3																							,   #? 	switching frequency
							'T_s'           		:	10e-6																							,   #? 	switching period
							'Tpecu' 	    		:	1.0e-3		                    																    #? 	cycle time of PeCU/PeSU
						}

PWM					= 	{																																	#*	microcontroller PWM parameters
							'Fs'					:	MCU['f_s']																						,	#?	switching frequency
                            'Ts'					:	MCU['T_s']																						,	#?	switching period
                            'PSFB_Ts'				:	0																								,	#?	substep PSFB model sampling time
							'M'             		:	MCU['f_pwm']/MCU['f_s']																			,   #? 	gain stage of PWM module MCU.f_pwm/MCU.f_s
							'Dmax' 	       			:	0.99			    																			,   #? 	maximum duty cycle
							'Dmin'          		:	0.02																							,   #? 	minimum duty cycle
							'PCMCconfig'			:	2																								,	#?	1->Variable PWM generation | 2->Static PWM generation
                            'PCMCinterleave'		:	0																								,	#?	rail interleaving in buck, 0-> non-interleaved rails | 1->interleaved rails
                            'PCMCblanking'			:	{																									#!	blanking time parameters for PCMC mode
                                'Rail_1'		:	{																										#	rail 1 parameters
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Time'			:	350e-9																								#?	blanking time duration
								},
                                'Rail_2'		:	{																										#	rail 2 parameters
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Time'			:	350e-9																								#?	blanking time duration
								}
							},
							'RecScheme'      		: 	2                               																,   #?	0->passive modulation | 1->disable CCM modulation | 2->enable CCM modulation | 3->disable DCM modulation
                            'RecShift_Rail_1'		:	{																									#!	positive SR shift with respect to primary full-bridge in rail 1
                                'DCM'			:	{																										#	SR shift in DCM mode
                                    'S5'	:	{																											#!	rectifier switch S5 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S6'	:	{																											#!	rectifier switch S6 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S7'	:	{																											#!	rectifier switch S7 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S8'	:	{																											#!	rectifier switch S8 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									}
								},
                                'CCM'			:	{																										#	SR shift in CCM mode
                                    'S5'	:	{																											#!	rectifier switch S5 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S6'	:	{																											#!	rectifier switch S6 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S7'	:	{																											#!	rectifier switch S7 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S8'	:	{																											#!	rectifier switch S8 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									}
								},
							},
                            'RecShift_Rail_2'		:	{																									#!	positive SR shift with respect to primary full-bridge in rail 2
                                'DCM'			:	{																										#	SR shift in DCM mode
                                    'S5'	:	{																											#!	rectifier switch S5 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S6'	:	{																											#!	rectifier switch S6 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S7'	:	{																											#!	rectifier switch S7 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									},
                                    'S8'	:	{																											#!	rectifier switch S8 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	0																									#?	falling edge shift
									}
								},
                                'CCM'			:	{																										#	SR shift in CCM mode
                                    'S5'	:	{																											#!	rectifier switch S5 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S6'	:	{																											#!	rectifier switch S6 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S7'	:	{																											#!	rectifier switch S7 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									},
                                    'S8'	:	{																											#!	rectifier switch S8 parameters
                                        'Tr'		:	50e-9																							,	#?	rising edge shift
                                        'Tf'		:	50e-9																								#?	falling edge shift
									}
								},
							},
							'Masking_Rail_1'		: 	{																									#!	Rail 1 PWM masking configurations
								'S1'			:	{																										#	PWM S1 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S2'			:	{																										#	PWM S2 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S3'			:	{																										#	PWM S3 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S4'			:	{																										#	PWM S4 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S5'			:	{																										#	PWM S5 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S6'			:	{																										#	PWM S6 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
                                'S7'			:	{																										#	PWM S7 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S8'			:	{																										#	PWM S8 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sac'			:	{																										#	PWM Sac configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sfw'			:	{																										#	PWM Sfw configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Ssc'			:	{																										#	PWM Ssc configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sdis'			:	{																										#	PWM Sdis configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Rec_Scheme'	:	{																										#	Rectifiction configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
							},
							'Masking_Rail_2'		: 	{																									#!	Rail 2 PWM masking configurations
								'S1'			:	{																										#	PWM S1 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S2'			:	{																										#	PWM S2 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S3'			:	{																										#	PWM S3 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S4'			:	{																										#	PWM S4 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S5'			:	{																										#	PWM S5 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S6'			:	{																										#	PWM S6 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
                                'S7'			:	{																										#	PWM S7 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'S8'			:	{																										#	PWM S8 configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sac'			:	{																										#	PWM Sac configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sfw'			:	{																										#	PWM Sfw configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Ssc'			:	{																										#	PWM Ssc configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Sdis'			:	{																										#	PWM Sdis configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
								'Rec_Scheme'	:	{																										#	Rectifiction configuration
									'Config'		:	2																								,	#?	1->Enable | 2-Disable
									'HIGH'	:	{																											#!	HIGH mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[0, 0]																								#?	mask output
									},
									'LOW'	:	{																											#!	LOW mask configuation
										'TimeVec'	:	[0, 1]																							,	#?	activation time vector
										'OutVec'	:	[1, 1]																								#?	mask output
									},
								},
							},
							'Propagation_Rail_1'	:	{																									#!	parasitic propagation delay of switching PWMs in rail 1
                                'Config'			:	3																								,	#?	1->variable delay | 2->constant delay | 3->disable
                                'Delay'	:	{																												#	parasitic delay values
                                    'S1'	:	{																											#*	S1 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S2'	:	{																											#*	S2 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S3'	:	{																											#*	S3 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S4'	:	{																											#*	S4 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S5'	:	{																											#*	S5 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S6'	:	{																											#*	S6 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
									'S7'	:	{																											#*	S7 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S8'	:	{																											#*	S8 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'Sac'	:	{																											#*	Sac switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
								},
							},
                            'Propagation_Rail_2'	:	{																									#!	parasitic propagation delay of switching PWMs in rail 2
                                'Config'			:	3																								,	#?	1->variable delay | 2->constant delay | 3->disable
                                'Delay'	:	{																												#	parasitic delay values
                                    'S1'	:	{																											#*	S1 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S2'	:	{																											#*	S2 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S3'	:	{																											#*	S3 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S4'	:	{																											#*	S4 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S5'	:	{																											#*	S5 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S6'	:	{																											#*	S6 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
									'S7'	:	{																											#*	S7 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'S8'	:	{																											#*	S8 switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
                                    'Sac'	:	{																											#*	Sac switch
                                        'Rising'	:	0																								,	#?	rising edge
                                        'Falling'	:	0																								,	#?	falling edge
										'Shift'		:	0																									#?	rising & falling edge shift
									},
								},
							},
							'Limit_Duty_Rail_1'		:	{																									#!	switching PWMs duty cycle limit for rail 1
                                'S1'	:	{																												#	S1 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S2'	:	{																												#	S2 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S3'	:	{																												#	S3 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S4'	:	{																												#	S4 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S5'	:	{																												#	S5 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S6'	:	{																												#	S6 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S7'	:	{																												#	S7 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S8'	:	{																												#	S8 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
							},
                            'Limit_Duty_Rail_2'		:	{																									#!	switching PWMs duty cycle limit for rail 2
                                'S1'	:	{																												#	S1 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S2'	:	{																												#	S2 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S3'	:	{																												#	S3 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S4'	:	{																												#	S4 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.5																								,	#?	maximum duty limit
                                    'Dmin'			:	0.5																									#?	minimum duty limit
								},
                                'S5'	:	{																												#	S5 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S6'	:	{																												#	S6 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S7'	:	{																												#	S7 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
                                'S8'	:	{																												#	S8 switch limits
                                    'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'Dmax'			:	0.95																							,	#?	maximum duty limit
                                    'Dmin'			:	0.2																									#?	minimum duty limit
								},
							},
							'Deadtimes_Rail_1'		:	{																									#!	primary full-bridge deadtime parameters for rail 1
                                'S1'				:	50e-9																							,	#?	S1 switch deadtime
                                'S2'				:	50e-9																							,	#?	S2 switch deadtime
                                'S3'				:	50e-9																							,	#?	S3 switch deadtime
                                'S4'				:	50e-9																								#?	S4 switch deadtime
							},
                            'Deadtimes_Rail_2'		:	{																									#!	primary full-bridge deadtime parameters for rail 2
                                'S1'				:	50e-9																							,	#?	S1 switch deadtime
                                'S2'				:	50e-9																							,	#?	S2 switch deadtime
                                'S3'				:	50e-9																							,	#?	S3 switch deadtime
                                'S4'				:	50e-9																								#?	S4 switch deadtime
							},
							'Short_Circuit'			:	{																									#!	short-circuit switch control signals
                                'Rail_1'	:	{																											#!	rail 1 switch
                                	'TimeVec'		:	[0, 1]																							,	#?	activation time vector
                                	'OutVec'		:	[1, 1]																								#?	activation signal vector
								},
                                'Rail_2'	:	{																											#!	rail 2 switch
                                	'TimeVec'		:	[0, 1]																							,	#?	activation time vector
                                	'OutVec'		:	[1, 1]																								#?	activation signal vector
								},
							},
                            'Active_Discharge'		:	{																									#!	active discharge switch control signals
                                'Rail_1'	:	{																											#!	rail 1 switch
                                	'TimeVec'		:	[0, 1]																							,	#?	activation time vector
                                	'OutVec'		:	[0, 0]																								#?	activation signal vector
								},
                                'Rail_2'	:	{																											#!	rail 1 switch
                                	'TimeVec'		:	[0, 1]																							,	#?	activation time vector
                                	'OutVec'		:	[0, 0]																								#?	activation signal vector
								},
							},
							'ActiveClamp'			:	{																									#!	active clamp PWM control
                                'Rail_1'	: {																												#	rail 1 parameters
                                    'FreqScale'		:	2																								,	#?	clamp switching frequency scaled to switching frequency
                                    'ON_Time'		:	200e-9																							,	#?	clamp on time
									'LeftRight'		:	0																									#?	0-> synced to right leg | 1-> synced to left leg
								},
                                'Rail_2'	: {																												#	rail 1 parameters
                                    'FreqScale'		:	2																								,	#?	clamp switching frequency scaled to switching frequency
                                    'ON_Time'		:	200e-9																							,	#?	clamp on time
									'LeftRight'		:	0																									#?	0-> synced to right leg | 1-> synced to left leg
								},
							},
                            'Resolution'			:	{																									#!	PWM resolution scale limited by HW
                                'Rail_1'	: {																												#	rail 1 parameters
									'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'HV_PWM'		:	1																								,	#?	HV PWM resolution scale
                                    'LV_PWM'		:	1																									#?	LV PWM resolution scale
								},
                                'Rail_2'	: {																												#	rail 2 parameters
									'Config'		:	2																								,	#?	1->enable | 2->disable
                                    'HV_PWM'		:	1																								,	#?	HV PWM resolution scale
                                    'LV_PWM'		:	1																									#?	LV PWM resolution scale
								}
							}
						}

burstPWM			= 	{																																	#*	burst PWM signal parameters
							'BurstFreq'   			:	MCU['f_s']/10    																				,   #? 	burst-mode PWM frequency
							'BurstDuty' 	    	:	[1.0, 1.0]	    																				,   #? 	burst-mode PWM duty cycle
							'BurstEnable'       	:	1				 	            																    #? 	1->enable burst PWM | 2->disable burst PWM
						}

burstControl		= 	{																																	#*	burst operation control parameters
							'BurstDuty_OutVec'		: 	burstPWM['BurstDuty']               															,	#? 	duty cycle vector for activation of burst-mode PWM
							'BurstDuty_Time'  		: 	simParams['tSim']*(1 - 1/len(burstPWM['BurstDuty']))											,	#? 	simulation time that the burst-duty will be calculated with [s]
							'BurstDutySlope'  		: 	(1 - burstPWM['BurstDuty'][1])/5e-3                  												#? 	slope of transition to burst-mode [1/s]
						}

activeDischarge		= 	{																																	#*	active discharge control
							'Config'					:	2																							,	#?	1->Enable | 2->Disable
							'Rdis' 						:	10.0																						,	#?	discharging resistance
							'Switch'					:	dp.copy.deepcopy(Switches['PMT200EPE'])														,	#?	active discharge switch
                            'BlockingDiode'	:	{																											#!	blocking diode parameters
                              'Vf'  					:	1																							,	#?	forward voltage
                              'Rd_on'					:	1e-3																							#?	diode on-resistance
							}
						}

CPH					=	{																																	#*	software component protection handler
							'Freq'			 	 		:	10e3																						,	#?	runtime PWM frequency
							'd'				    		:	0.5																							,	#?	runtime PWM duty cylce
							'Enable'			 		:	1																							,	#?	0->disable CPH | 1->enable CPH
        					'OutputVoltage'	:	{																											#!	output voltage CPH parameters
								'UpThresh'				:	Protection['VoMax']																			,	#?	upper threshold
								'LoThresh'				:	0																							,	#?	lower threshold
								'CNTINC'				:	1																							,	#?	debounce increment
								'CNTDEC'				:	1																							,	#?	debounce decrement
								'CNTMAX'				:	100																							,	#?	max debounce counter
								'RSTRT'					:	10						 	 																	#?	restart period counter
												},
							'OutputCurrent'	:	{																											#!	output current CPH parameters
								'UpThresh'				:	Protection['IoMax']																			,	#?	upper threshold
								'LoThresh'				:	-Protection['IoMax']																		,	#?	lower threshold
								'CNTINC'				:	1																							,	#?	debounce increment
								'CNTDEC'				:	1																							,	#?	debounce decrement
								'CNTMAX'				:	100																							,	#?	max debounce counter
								'RSTRT'					:	10						 																		#?	restart period counter
												},
							'InputVoltage'	:	{																											#!	input voltage CPH parameters
								'UpThresh'				:	Protection['VinMax']																		,	#?	upper threshold
								'LoThresh'				:	Protection['VinMin']																		,	#?	lower threshold
								'CNTINC'				:	1																							,	#?	debounce increment
								'CNTDEC'				:	1																							,	#?	debounce decrement
								'CNTMAX'				:	100																							,	#?	max debounce counter
								'RSTRT'					:	1000						 																	#?	restart period counter
												},
							'InputCurrent'	:	{ 																											#!	input current CPH parameters
								'UpThresh'				:	Protection['IinMax']																		,	#?	upper threshold
								'LoThresh'				:	-Protection['IinMax']																		,	#?	lower threshold
								'CNTINC'				:	1																							,	#?	debounce increment
								'CNTDEC'				:	1																							,	#?	debounce decrement
								'CNTMAX'				:	100																							,	#?	max debounce counter
								'RSTRT'					:	10						 	 																	#?	restart period counter
												}
						}

FaultLogic			=	{																																	#* hardware fault logic (safe-state aggregator) parameters
							'Reset'			 			:	0																							,	#?	0->no reset | 1->reset
							'Config'			 		:	2																							,	#?	1->Enable | 2->Disable
							'Type'						:	2																							,	#?	1->Physical Model | 2->Small-Signal Model
							'Delay'						:	49.2e-9																						,	#?	total prpagation delay of the SSA
        					'OutputVoltage'	:	{																											#!	output voltage fault logic parameters
								'R1'					:	1.2987e3																					,	#?	reference voltage divider supply resistance
								'Rfil'					:	1e3																							,	#?	input signal filter resistance
								'Cfil'					:	10e-9																						,	#?	input signal filter capacitance
								'UpBand'				:	17.18																						,	#?	upper heysteresis band
								'LoBand'				:	16.53																						,	#?	lower heysteresis band
								'Delay'					:	614e-9																						,	#? 	overall propagation delay
								'Vcc'					:	3.3																							,	#?	upper rail supply voltage
								'Vee'					:	0.04																						,	#?	lower rail supply voltage
								'Vin'					:	3.0																								#?	input reference voltage
												},
							'OutputCurrentPos':	{																											#!	output voltage fault logic parameters
								'R1'					:	1.96993e3																					,	#?	reference voltage divider supply resistance
								'Rfil'					:	10e3																						,	#?	input signal filter resistance
								'Cfil'					:	100e-12																						,	#?	input signal filter capacitance
								'UpBand'				:	220.0																						,	#?	upper heysteresis band for positive currents
								'LoBand'				:	200.0																						,	#?	lower heysteresis band for positive currents
								'Delay'					:	52e-9																						,	#? 	overall propagation delay
								'Vcc'					:	3.3																							,	#?	upper rail supply voltage
								'Vee'					:	0.1																						,	#?	lower rail supply voltage
								'Vin'					:	3.0																								#?	input reference voltage
												},
							'OutputCurrentNeg':	{																											#!	output voltage fault logic parameters
								'R1'					:	1.96993e3																					,	#?	reference voltage divider supply resistance
								'Rfil'					:	10e3																						,	#?	input signal filter resistance
								'Cfil'					:	100e-12																						,	#?	input signal filter capacitance
								'UpBand'				:	-158.0																						,	#?	upper heysteresis band for negative currents
								'LoBand'				:	-168.0																						,	#?	lower heysteresis band for negative currents
								'Delay'					:	52e-9																						,	#? 	overall propagation delay
								'Vcc'					:	3.3																							,	#?	upper rail supply voltage
								'Vee'					:	0.04																						,	#?	lower rail supply voltage
								'Vin'					:	3.0																								#?	input reference voltage
												},
							'InputVoltage'	:	{																											#!	input voltage fault logic parameters
								'R1'					:	2.1573e3																					,	#?	reference voltage divider supply resistance
								'Rfil'					:	5.1e3																						,	#?	input signal filter resistance
								'Cfil'					:	470e-12																						,	#?	input signal filter capacitance
								'UpBand'				:	478.8152																					,	#?	upper heysteresis band
								'LoBand'				:	435.7601																					,	#?	lower heysteresis band
								'Delay'					:	614e-9																						,	#? 	overall propagation delay
								'Vcc'					:	3.3																							,	#?	upper rail supply voltage
								'Vee'					:	0.04																						,	#?	lower rail supply voltage
								'Vin'					:	3.0																								#?	input reference voltage
												}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ADC Parameters

ADCres				= 	{																																	#*	microcontroller analog resulution
							'Nadc'           		:	12			        																			,   #?	ADC resolution bits
							'Ndac'           		:	12			        																			,   #?	DAC resolution bits
							'Vadc'           		:	3.0			     																				,   #?	ADC reference voltage
							'Vdac'           		:	3.3			                    																    #?	DAC reference voltage
						}

ADCgains			= 	{																																	#*	microcontroller analog parameters
							'ADCrange'       		:	(2**ADCres['Nadc'] - 1)/ADCres['Vadc']   														,   #?	ADC resolution bits
							'DACrange'       		:	(2**ADCres['Nadc'] - 1)/ADCres['Vdac']   														,   #?	DAC resolution bits
							'VopAmp'         		:	ADCres['Vadc']/2			             														,   #?	ADC offset voltage
							'Dvopamp'        		:	(2**ADCres['Nadc'] - 1)/2			         														#?	digital value of Vopamp
						}

ADCmodel			=	{
							'RailsConfig'			:   1																								,	#?	1->enable | 2->disable
							'Config'				:	2																								,	#?	1->physical model | 2->small-signal model | 3->ideal model
                            'Avg'					:	1																								,	#?	1-> enable average | 2->disable average
							'Cpar'					:	13e-12																							,	#?	channel parasitic capacitance
							'Ileak'					:	300e-9																							,	#?	channel leakage current
							'Radc'					:	425																								,	#?	sample-and-hold resistance
							'Csh'					:	14.5e-12																						,	#?	sample-and-hold capacitance
							'Rdis'					:	100.0																							,	#?	sample-and-hold discharge resistance
							'Fs'					:	100e3																							,	#?	sampling frequency
							'Ts'					:	10e-6																							,	#?	sampling period
                            'Td'					:	10e-6																							,	#?	measurement delay time
							'Tacq'					:	75e-9																							,	#?	acquisition time window
                            'Tconv'					:	55e-9																							,	#?	conversion time window
                            'Tavg'					:	10e-6																							,	#?	moving average time window
							'Tdead'					:	0.0																								,	#?	deadtime between acquisition & discharge
							'Quantize'				:	1																								,	#?	1->floor | 2->ceil | 3->round | 4->fix
                            'InputFilters'	:	{																											#*	ADC input filters parameters
								'LV_voltageSense'	:	{																									#!	LV voltage sensor filter parameters
									'Rfil'			:	499																								,	#?	filter resistance
                                    'Cfil'			:	10e-9																								#?	filter capacitance
								},
                                'HV_voltageSense'	:	{																									#!	HV voltage sensor filter parameters
									'Rfil'			:	200																								,	#?	filter resistance
                                    'Cfil'			:	10e-9																								#?	filter capacitance
								},
                                'LV_currentSense'	:	{																									#!	LV current sensor filter parameters
									'Rfil'			:	200.0																							,	#?	filter resistance
                                    'Cfil'			:	100e-9																								#?	filter capacitance
								},
                                'HV_currentSense'	:	{																									#!	HV current sensor filter parameters
									'Rfil'			:	100																								,	#?	filter resistance
                                    'Cfil'			:	330e-12																								#?	filter capacitance
								},
                                'CT'				:	{																									#!	CT current sensor filter parameters
									'Rfil'			:	100																								,	#?	filter resistance
                                    'Cfil'			:	330e-12																								#?	filter capacitance
								}
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Sensor Parameters

LV_voltageSense		=	dp.copy.deepcopy(Sensors['BuffDivider_3'])																							#*	LV voltage sensor
HV_voltageSense		=	dp.copy.deepcopy(Sensors['SI8932D'])																								#*	HV voltage sensor
LV_currentSense 	= 	dp.copy.deepcopy(Sensors['INA240A2'])																								#*	LV current sensor
HV_currentSense		=	dp.copy.deepcopy(Sensors['ACS724'])																									#*	HV current sensor
CT					=	dp.copy.deepcopy(Sensors['DS_P100076'])																								#*	current transformer sensor

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Controllers

#Digital PCMC controller-------------------------------------------------------
PCMCbuck 			=	{																																	#*	peak buck mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain | 3->disable
                            'Type'					:	1																								,	#?	1->PI controller | 2->Type II compensator
                            'openLoop'		:	{																											#*	open-loop configuration parameters
								'Config'			:	2																								,	#?	1->enable | 2->disable
								'Duty'				:	1																								,	#?	open-loop duty cycle value
                                'Dinit'				:	0.1																								,	#?	open-loop duty cycle value
                                'Dselect'			:	0																								,	#?	0->custom open-loop transformer reference voltage | 1->controller reference voltage value
                                'Dscale'			:	1																								,	#?	duty cycle scaling option
								'Dconfig'			:	1																								,	#?	1->floor duty cycle | 2->pass duty cycle
                                'Ramp'	:	{																												#!	open-loop configuration parameters
                                    'Config'		:	3																								,	#?	1->discrete | 2->continuous | 3->pass
                                    'Slope'			:	0																								,	#?	ramp slope value
                                    'Scale'			:	1																								,	#?	ramp output scaling
                                    'sampleTime'	:	MCU['T_s']																							#?	ramp computation sample tine
								}
							},
							'Kp'             		:	0.84              																				,	#?	proportional gain for PI
							'Ki'             		:	85800*MCU['T_s']    																			,   #?	integral gain for PI
                            'K_c'					:	1.5e4*2*dp.np.pi*30e3/8e3																		,	#?	proportional gain for Type II
                            'f_p'					:	30e3																							,	#?	pole frequency for Type II
                            'f_z'					:	8e3																								,	#?	zero frequency for Type II
                            'Td'					:	0																								,	#?	controller delay
							'UpLim'			 		:	2*2**ADCres['Ndac'] - 1																			,	#?	upper saturation limit
							'LoLim'			 		:	0.0	     		  																				,	#?	lower saturation limit
							'CCMcurrent'			:	25																								,	#?	current threshold to switch to CCM mode
							'outputScale'	 		:	0.5				  																				,	#?	controller output scaling
							'ohmicOffset'			:	0																								,	#?	add ohmich offset to the reference voltage
							'enableOffset'			:	0																								,	#?	0->disable | 1->enable
							'SLP'            		:	0.5                	            																    #?	slope compensation
						}

# Digital ACMC precharge controller--------------------------------------------
ACMCprecharge		= 	{																																	#*	precharge mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain
							'Kp'              		:	0.0075            																				,	#?	proportional gain
							'Ki'              		:	0.001             																				,   #?	integral gain
                            'Td'					:	0																								,	#?	controller delay
							'UpLim'			  		:	PWM['Dmax']*PWM['M']	  																		,	#?	upper saturation limit
							'MdLim'			  		:	PWM['M']/2	     																				,	#?	middle saturation limit
							'MdLimOffset'			:	0																								,	#?	middle saturation limit offset
							'LoLim'			  		:	PWM['Dmin']*PWM['M']/2 		 																	,	#?	lower saturation limit
							'CCMcurrent'	  		:	25				  																				,	#?	current threshold to switch to CCM mode
                            'CurrentConfig'			:	2																								,	#?	precharge current configurations, 1->online calculation | 2->fixed lookup | 3->constant currents
                            'ConfigLuT'				:	0																								,	#?	precharge current LuT config, 0->interpolated | 1->discrete
							'outputScale'	  		:	2.0			  																					,	#?	controller output scaling
							'RateSlope'		  		:	0.2				  																				,	#?	rate limiter current slope per 10us
							'Vdelta'         		:	5                	            																,   #?	undervoltage difference where slope starts
                            'Icmax'					:	40																								,	#?	maximum capacitor current allowed during precharge of the precharge
                            'ILVmax'				:	100																								,	#?	maximum DC current allowed during precharge of the precharge
                            'Vsnub'					:	60																								,	#?	maximum allowed active snubber voltage during precharge of the precharge
                            'tonsnub_min'			:	250e-9																							,	#?	minimum on-time for the active snubber during precharge of the precharge
                            'tonsnub_final'			:   250e-9																							,	#?
                            'Points'				:   20																								,	#?	number of points for the current-voltage precharge lookup
							'ohmicOffset'			:	0																								,	#?	add ohmich offset to the reference voltage
							'enableOffset'			:	0																									#?	0->disable | 1->enable
						}

# Digital ACMC boost controller------------------------------------------------
ACMCboost			= 	{																																	#*	boost mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain
                            'openLoop'		:	{																											#*	open-loop configuration parameters
								'Config'			:	2																								,	#?	1->enable | 2->disable
								'Duty'				:	1																								,	#?	open-loop duty cycle value
                                'Dinit'				:	PWM['Dmin']																						,	#?	open-loop duty cycle value
                                'Dselect'			:	0																								,	#?	0->custom open-loop transformer reference voltage | 1->controller reference voltage value
                                'Dscale'			:	1																								,	#?	duty cycle scaling option
								'Dconfig'			:	1																								,	#?	1->floor duty cycle | 2->pass duty cycle
                                'Ramp'	:	{																												#!	open-loop configuration parameters
                                    'Config'		:	3																								,	#?	1->discrete | 2->continuous | 3->pass
                                    'Slope'			:	0																								,	#?	ramp slope value
                                    'Scale'			:	1																								,	#?	ramp output scaling
                                    'sampleTime'	:	MCU['T_s']																							#?	ramp computation sample tine
								}
							},
							'Kp'              		:  	0.165              																				,	#?	proportional gain
							'Ki'              		:	0.0040             																				,   #?	integral gain
                            'Td'					:	0																								,	#?	controller delay
							'UpLim'			  		:	PWM['Dmax']*PWM['M']/2																			,	#?	upper saturation limit
							'LoLim'			  		:	PWM['Dmin']*PWM['M']/2   																		,	#?	lower saturation limit
							'CCMcurrent'	  		:	25																								,	#?	current threshold to switch to CCM mode
                            'ACcurrent'	  			:	15																								,	#?	current threshold to switch ON active clamp
                            'ACprecharge'			:	2e-3																							,	#?	delays the controller operation until is AC is precharged
							'outputScale'	  		:	1.0			    																				,	#?	controller output scaling
							'ohmicOffset'			:	0																								,	#?	add ohmich offset to the reference voltage
							'enableOffset'			:	0																								,	#?	0->disable | 1->enable
							'Shutdown'		:	{																											#!	soft shuntdown triggers
								'Rail_1'		:	{																										#	rail 1 (lower rail) shuntdown trigger
									'TimeVec'		:	[0, 1]																							,	#?	shutdown time trigger
									'OutVec'		:	[0, 0]																								#?	shutdown output trigger
								},
								'Rail_2'		:	{																										#	rail 2 (upper rail) shuntdown trigger
									'TimeVec'		:	[0, 1]																							,	#?	shutdown time trigger
									'OutVec'		:	[0, 0]																								#?	shutdown output trigger
								}
							}
						}

# Digital ACMC buck controller-------------------------------------------------
ACMCbuck			= 	{																																	#*	duty cycle buck mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain
                            'openLoop'		:	{																											#*	open-loop configuration parameters
								'Config'			:	2																								,	#?	1->enable | 2->disable
								'Duty'				:	1																								,	#?	open-loop duty cycle value
                                'Dinit'				:	PWM['Dmin']																						,	#?	open-loop duty cycle value
                                'Dselect'			:	0																								,	#?	0->custom open-loop transformer reference voltage | 1->controller reference voltage value
                                'Dscale'			:	1																								,	#?	duty cycle scaling option
								'Dconfig'			:	1																								,	#?	1->floor duty cycle | 2->pass duty cycle
                                'Ramp'	:	{																												#!	open-loop configuration parameters
                                    'Config'		:	3																								,	#?	1->discrete | 2->continuous | 3->pass
                                    'Slope'			:	0																								,	#?	ramp slope value
                                    'Scale'			:	1																								,	#?	ramp output scaling
                                    'sampleTime'	:	MCU['T_s']																							#?	ramp computation sample tine
								}
							},
							'Kp'              		:	0.2                																				,	#?	proportional gain
							'Ki'              		:	0.0095             																				,   #?	integral gain
                            'Td'					:	0																								,	#?	controller delay
							'UpLim'			  		:	PWM['Dmax']*PWM['M']/2																			,	#?	upper saturation limit
							'LoLim'			  		:	PWM['Dmin']*PWM['M']/2																			,	#?	lower saturation limit
							'CCMcurrent'	  		:	25																								,	#?	current threshold to switch to CCM mode
                            'ACcurrent'	  			:	15																								,	#?	current threshold to switch ON active clamp
							'outputScale'	  		:	1.0			    																				,	#?	controller output scaling
							'RateSlope'		  		:	2.0					 	 	 																	,	#?	rate limiter current slope per 10us
							'ohmicOffset'			:	0																								,	#?	add ohmich offset to the reference voltage
							'enableOffset'			:	0																								,	#?	0->disable | 1->enable
							'Shutdown'		:	{																											#!	soft shuntdown triggers
								'Rail_1'		:	{																										#	rail 1 (lower rail) shuntdown trigger
									'TimeVec'		:	[0, 1]																							,	#?	shutdown time trigger
									'OutVec'		:	[0, 0]																								#?	shutdown output trigger
								},
								'Rail_2'		:	{																										#	rail 2 (upper rail) shuntdown trigger
									'TimeVec'		:	[0, 1]																							,	#?	shutdown time trigger
									'OutVec'		:	[0, 0]																								#?	shutdown output trigger
								}
							}
						}

# Balancing Hysteresis controller----------------------------------------------
BalHys				=	{																																	#*	balancing hysteresis controller
							'PackDiff'          	:   5.0              																				,	#?	voltage value where difference in pack voltages is detected
							'PackEq'            	:	2.0              																				,   #?	voltage value where equalized pack voltages is detected
							'UpperThd'          	:	50.0            																				,   #?	upper LV current threshold where two rails will operate
							'LowerThd'          	:	20.0            																				,   #?	lower LV current threshold where one rail will operate
							'LoadShiftFactor'   	:	0.2                             																    #?	percentage of the load-shift between the two rails
						}

# Rectifier Rising Edge calculation--------------------------------------------
Trise				=	{																																	#*	boost mode rectifier rising edge early turn-ON calculator
							'Config'				:	0																								,	#?	selector between constant and dynamic Trise, 0->constant | 1->dynamic
							'TdeadFactor'       	:   6               																				,	#?	maximum allowed deadtime for earlier turn-on
							'LeakageFactor'     	:	2.6      	                       																,   #?	correction factor for the leakage inductance
						}

# Soft-start ramps-------------------------------------------------------------
softStart			=	{																																	#*	buck/boost soft-start paramters
							'BuckRamp'          	:   1.0             																				,   #?	Buck voltage/current ramp per 10us
                            'BuckConfig'			:	1																								,	#?	1->current ramp | 2->voltage ramp
							'BoostRamp'         	:   1.0                             																    #?	Boost current ramp per 10us
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Active Switches

LeftLeg_1			=	dp.copy.deepcopy(Switches['AIMDQ75R060M1H'])																						#*	HV left leg switches parameters
LeftLeg_2			=	dp.copy.deepcopy(Switches['AIMDQ75R060M1H'])																						#*	HV left leg switches parameters
RightLeg_1			=	dp.copy.deepcopy(Switches['AIMDQ75R060M1H'])																						#*	HV right leg switches parameters
RightLeg_2			=	dp.copy.deepcopy(Switches['AIMDQ75R060M1H'])																						#*	HV right leg switches parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Rectifier Switches

Rectifier_1			=	dp.copy.deepcopy(Switches['IAUT300N10S5N015'])																						#*	LV rectifier switches parameters
Rectifier_2			=	dp.copy.deepcopy(Switches['IAUT300N10S5N015'])																						#*	LV rectifier switches parameters
Rectifier_3			=	dp.copy.deepcopy(Switches['IAUT300N10S5N015'])																						#*	LV rectifier switches parameters
Rectifier_4			=	dp.copy.deepcopy(Switches['IAUT300N10S5N015'])																						#*	LV rectifier switches parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Short-Circuit Switch

SC_Switch			=	dp.copy.deepcopy(Switches['NVMTS0D6N04C'])																							#*	short-circuit switch parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Thermal Parameters

Thermal 			=   {																																	#* 	thermal conditions
							'Tinit'             	:   35           		 																			,	#? 	initial temperature of semiconductors and heatsinks
							'Tjmax'					:	175																								,	#?	maximum junction temperature for semiconductor switches
							'Tjmin'					:	-55																								,	#?	minimum junction temperature for semiconductor switches
							'Twater'            	:	35                                          													,	#? 	coolant water temperature
                            'IMS_Rth'				:	1.0																								,	#?	IMS board thermal resistance with respect to hottest component
							'BuckBoost'				:	0																								,	#?	0->buck operation | 1->boost operation
                            'TempSelect_IMS'		:	1																								,	#?	0->no coupling | 1->IMS coupling
                            'R_IMS'					:	2.883e-3																						,	#?	IMS board equivalent resistance
                            'Paux'					:	30																								,	#?	DCDC aux consumption
                            'PCB_IMS_SS':	{																												#*	temperature coupling on Basis DCDC IMS board and its components
                                'Config'			:	1																								,	#?	1->enable | 2->disable
                                'Scale'				:	[1,1,1,1,1]																						,	#?	loss scaling for transient operations
                                'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-38.70575646,-0.91590339,-0.84725137,1.12472138,-0.24846279]									,	#?	first row
                                    'A2'			:	[-1.29695581,0.02069626,-0.07205622,-0.05668288,-0.15819592]									,	#?	second row
									'A3'			:	[-18.40080818,-0.35784609,-0.32788111,1.09294221,0.63545890]									,	#?	third row
									'A4'			:	[-4.68688077,0.14098871,-0.40970239,-0.85094779,-1.48558837]									,	#?	fourth row
									'A5'			:	[-49.97349560,-0.25217364,-1.86533686,-0.58425075,-3.48880019]									,	#?	fifth row
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[2.585102597,0.225430753,0.225430753,0.245033424,6.248352291]									,	#?	first row
                                    'B2'			:	[0.092023489,0.008024847,0.008024847,0.008722622,0.22242676]									,	#?	second row
									'B3'			:	[1.205285427,0.105105462,0.105105462,0.114245066,2.913249167]									,	#?	third row
									'B4'			:	[0.362684729,0.031627469,0.031627469,0.034377691,0.876631146]									,	#?	fourth row
									'B5'			:	[3.448509465,0.300723103,0.300723103,0.326872936,8.335259867]									,	#?	fifth row
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[20.20618513,189.2177136,-13.42389823,3.621548276,-14.99528173]									,	#?	first row
                                    'C2'			:	[17.55370886,246.6851124,-25.22868559,-19.85621542,-8.739564788]								,	#?	second row
									'C3'			:	[20.9613834,275.4200667,-22.64536171,-9.915021348,-14.04941664]									,	#?	third row
									'C4'			:	[18.81757498,201.1703046,-15.03689437,1.257979944,-14.13951791]									,	#?	fourth row
									'C5'			:	[19.84895797,195.4996438,-14.11212592,2.807097902,-14.92257608]									,	#?	fifth row
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[0.41382775,0.03739708,0.03739709,0.03966523,1.00887729]										,	#?	first row
                                    'D2'			:	[0.22988932,0.02240205,0.02240206,0.02258795,0.57136651]										,	#?	second row
									'D3'			:	[0.28037978,0.02679386,0.02679387,0.02736749,0.69325791]										,	#?	third row
									'D4'			:	[0.31468971,0.02891530,0.02891531,0.03032394,0.77035460]										,	#?	fourth row
									'D5'			:	[0.37608849,0.03417790,0.03417791,0.03611244,0.91814041]										,	#?	fifth row
								},
                                'Temps_Init'		:	[35,35,35,35,35]																				,	#?	components initial temperatures
                                'Losses_Init'		:	[0,0,0,0,0]																							#?	components initial losses
							}
						}

#!	simulation, analysis and solver settings & parameterizations
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SolverOpts			= 	{																																	#*	solver settings parameters for simulations
							'Solver'					: 	'auto'					,																		#?	solver to use for the simulation. Possible values are auto, dopri, radau and discrete
							'StartTime'					:	0.0						,																		#?	start time specifies the initial value of the simulation time at the beginning of a simulation, in seconds
							'TimeSpan'					:	simParams['tSim']		,																		#?	simulation ends when the simulation time has advancedby the specified time span, in seconds
							'stopTime'					: 	simParams['tSim']		,																		#?	this parameter is obsolete. It is provided to keep old scripts working. Aadvise against using it in new code
							'Timeout'					:	0						,																		#?	maximum number of seconds that a simulation or analysis is allowed to run. After this period the simulation or analysis is stopped with a timeout error. A value of 0 disables the imeout.
							'MaxStep'					:	simParams['Maxstep']	,																		#?	maximum step size taken by the variable-step solvers
							'FixedStep'					:	simParams['Fixedstep']	,																		#?	simulation step size taken by the fixed-step solvers
							'RelTol'					:	simParams['RelTol']		, 																		#?	relative tolerance of solvers
                            'Refine'					:	simParams['Refine']																				#?	data points refine factor
						}

AnalysisOpts		= 	{																																	#*	parameters for analyses
							'TimeSpan'					: 	MCU['T_s']				,																		#?	system period length
							'StartTime'					: 	0						,																		#?	simulation start time
							'Tolerance'					: 	1e-4					,																		#?	relative error tolerance used in the convergence criterion of a steady-state analysis
							'MaxIter'					: 	20						,																		#?	maximum number of iterations allowed in a steady-state analysis
							'JacobianPerturbation'		: 	1e-4					,																		#?	relative perturbation of the state variables used to calculate the approximate Jacobian matrix
							'JacobianCalculation'		: 	'fast'					,																		#?	controls the way the Jacobian matrix is calculated. Options are full and fast
							'InitCycles'				: 	0						,																		#?	number of cycle-by-cycle simulations that should be performed before the actual analysis
							'ShowCycles'				: 	2						,																		#?	number of steady-state cycles of the time span that should be simulated at the end of an analysis
							'FrequencyRange'			: 	[1, 1e12]				,																		#?	range of the perturbation frequencies for small-signal anaylsis
							'FrequencyScale'			: 	'logarithmic'			,																		#?	specifies whether the sweep frequencies should be distributed on a linear or logarithmic
							'AdditionalFreqs'			: 	[]						,																		#?	vector specifying frequencies to be swept in addition to the automatically distributed frequencies
							'NumPoints'					: 	5000					,																		#?	The number of automatically distributed perturbation frequencies
							'Perturbation'				: 	''						,																		#?	full block path (excluding the model name) of the Small Signal Perturbation block that will be active during an analysis
							'Response'					: 	''						,																		#?	full block path (excluding the model name) of the Small Signal Response block that will record the system response during an analysis
							'AmplitudeRange'			: 	1e-3					, 																		#?	amplitude of the sinusoidal pulse perturbation for an ac sweep analysis
							'Amplitude'					: 	1e-3					, 																		#?	amplitude of the discrete pulse perturbation for an impulse response analysis
                            'ShowResults'				:	1																								#?	specifies whether to show a Bode plot after a small-signal analysis.
						}

#!	assemble all parameters to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Common 				= 	{
							'simParams' 				: 	simParams 								,
							'Probes'  					: 	Probes 									,
							'ToFile'					:	ToFile									,
							'PSFBconfigs'  				: 	PSFBconfigs 							,
							'RboxConfigs'  				: 	RboxConfigs 							,
							'Relays'  					: 	Relays 									,
                            'PyroFuse'					:	PyroFuse								,
                            'DCDC_AUX'					:	DCDC_AUX								,
							'Control'  					: 	dp.copy.deepcopy(Control) 				,
							'RailsOperation'  			: 	RailsOperation							,
							'Initials'  				: 	Initials 								,
							'Protection'  				: 	Protection 								,
							'Load'  					: 	Load			 						,
							'RailsEnable'  				: 	RailsEnable 							,
							'DualSingleOperation'		:	DualSingleOperation						,
							'loadShifting'				:	loadShifting							,
							'EIS'						:	EIS										,
							'InductancesPCB'			: 	InductancesPCB							,
							'LVdmc'  					: 	LVdmc 									,
							'LVcmc'  					: 	LVcmc 									,
							'Coc1'  					: 	Coc1 									,
                            'Coc2'						:	Coc2									,
                            'Coc3'						:	Coc3									,
                            'Coec1' 					: 	Coec1 									,
                            'Coec2' 					: 	Coec2 									,
                            'Coec3' 					: 	Coec3 									,
                            'Cyoc'						:	Cyoc									,
							'Busbars_PCB'				:	Busbars_PCB								,
							'LVS'  						: 	LVS 									,
							'EnBn'  					: 	EnBn 									,
							'HVS'  						: 	HVS 									,
							'Cdc'						: 	Cdc										,
                            'Cobc'						: 	Cobc									,
							'Ccharge'					: 	Ccharge									,
							'MCU'  						: 	MCU 									,
							'PWM'  						: 	PWM 									,
							'burstPWM'  				: 	burstPWM 								,
							'burstControl'  			: 	burstControl 							,
							'CPH'  						: 	CPH 									,
							'FaultLogic'				:	FaultLogic								,
							'ADCres'  					: 	ADCres 									,
							'ADCgains'  				: 	ADCgains 								,
							'PCMCbuck'  				: 	dp.copy.deepcopy(PCMCbuck) 				,
							'BalHys'  					: 	BalHys 									,
							'softStart'  				: 	softStart 								,
							'Thermal'  					: 	Thermal
                        }

DCDC_Rail1 			= 	{
							'Control'  					: 	dp.copy.deepcopy(Control) 				,
							'shortCircuit'				:	shortCircuit							,
							'SC_Switch_Control'			: 	SC_Switch_Control 						,
							'HVfuse'					:	HVfuse									,
							'HVcmc'  					: 	HVcmc 									,
							'Cin'  						: 	Cin 									,
							'Cpi'  						: 	Cpi 									,
							'Cyi'  						: 	Cyi 									,
							'Cc'  						: 	Cc										,
							'Trafo'  					: 	Trafo 									,
							'Cb'  						: 	Cb 										,
							'RCsnubber'  				: 	RCsnubber 								,
							'RCDclamp1'					:	dp.copy.deepcopy(RCDclamp)				,
							'RCDclamp2'					:	dp.copy.deepcopy(RCDclamp)				,
							'ERCclamp'					:	ERCclamp								,
							'FRW' 						: 	FRW 									,
							'Lf'  						: 	Lf 										,
							'RCDsnubber'  				: 	RCDsnubber 								,
							'Co'  						: 	Co 										,
							'Coe1' 						: 	Coe1 									,
                            'Cyo'  						: 	Cyo 									,
							'InductancesPCB'			: 	InductancesPCB							,
							'Busbars_PCB'				:	Busbars_PCB								,
							'activeDischarge'  			: 	activeDischarge 						,
							'ADCmodel'					:	ADCmodel								,
							'LV_voltageSense'			:	LV_voltageSense							,
							'HV_voltageSense'			:	HV_voltageSense							,
							'LV_currentSense'			:	LV_currentSense							,
							'HV_currentSense'			:	HV_currentSense							,
							'CT'  						: 	CT 										,
							'PCMCbuck'  				: 	dp.copy.deepcopy(PCMCbuck) 				,
							'ACMCprecharge' 			: 	ACMCprecharge 							,
							'ACMCboost'  				: 	ACMCboost 								,
							'ACMCbuck'  				: 	ACMCbuck 								,
							'Trise'  					: 	Trise 									,
							'LeftLeg_1'  				: 	LeftLeg_1 								,
                            'LeftLeg_2'  				: 	LeftLeg_2 								,
							'RightLeg_1'  				: 	RightLeg_1 								,
                            'RightLeg_2'  				: 	RightLeg_2 								,
							'Rectifier_1'  				: 	Rectifier_1 							,
                            'Rectifier_2'  				: 	Rectifier_2 							,
                            'Rectifier_3'  				: 	Rectifier_3 							,
                            'Rectifier_4'  				: 	Rectifier_4 							,
							'SC_Switch'  				: 	SC_Switch 								,
						}

DCDC_Rail2 			= 	{
							'Control'  					: 	dp.copy.deepcopy(Control) 				,
							'shortCircuit'				:	shortCircuit							,
							'SC_Switch_Control'			: 	SC_Switch_Control 						,
							'HVfuse'					:	HVfuse									,
							'HVcmc'  					: 	HVcmc 									,
							'Cin'  						: 	Cin 									,
							'Cpi'  						: 	Cpi 									,
							'Cyi'  						: 	Cyi 									,
							'Cc'  						: 	Cc										,
							'Trafo'  					: 	Trafo 									,
							'Cb'  						: 	Cb 										,
							'RCsnubber'  				: 	RCsnubber 								,
							'RCDclamp1'					:	dp.copy.deepcopy(RCDclamp)				,
							'RCDclamp2'					:	dp.copy.deepcopy(RCDclamp)				,
							'ERCclamp'					:	ERCclamp								,
							'FRW' 						: 	FRW 									,
							'Lf'  						: 	Lf 										,
							'RCDsnubber'  				: 	RCDsnubber 								,
							'Co'  						: 	Co 										,
							'Coe1' 						: 	Coe1 									,
                            'Cyo'  						: 	Cyo 									,
							'InductancesPCB'			: 	InductancesPCB							,
							'Busbars_PCB'				:	Busbars_PCB								,
							'activeDischarge'  			: 	activeDischarge 						,
							'ADCmodel'					:	ADCmodel								,
							'LV_voltageSense'			:	LV_voltageSense							,
							'HV_voltageSense'			:	HV_voltageSense							,
							'LV_currentSense'			:	LV_currentSense							,
							'HV_currentSense'			:	HV_currentSense							,
							'CT'  						: 	CT 										,
							'PCMCbuck'  				: 	dp.copy.deepcopy(PCMCbuck) 				,
							'ACMCprecharge' 			: 	ACMCprecharge 							,
							'ACMCboost'  				: 	ACMCboost 								,
							'ACMCbuck'  				: 	ACMCbuck 								,
							'Trise'  					: 	Trise 									,
							'LeftLeg_1'  				: 	LeftLeg_1 								,
                            'LeftLeg_2'  				: 	LeftLeg_2 								,
							'RightLeg_1'  				: 	RightLeg_1 								,
                            'RightLeg_2'  				: 	RightLeg_2 								,
							'Rectifier_1'  				: 	Rectifier_1 							,
                            'Rectifier_2'  				: 	Rectifier_2 							,
                            'Rectifier_3'  				: 	Rectifier_3 							,
                            'Rectifier_4'  				: 	Rectifier_4 							,
							'SC_Switch'  				: 	SC_Switch 								,
						}

ModelVars 			= 	{
							'Common' 					: 	Common 									,
							'DCDC_Rail1'  				: 	DCDC_Rail1 								,
							'DCDC_Rail2'				:	DCDC_Rail2								,
                            'AnalysisOpts'				:	AnalysisOpts
						}
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

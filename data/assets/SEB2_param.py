
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 _____ ____ ____    ___    ____   _    ____      _    __  __ _____ _____ _____ ____  ____
#?						| ____| __ )___ \  / _ \  |  _ \ / \  |  _ \    / \  |  \/  | ____|_   _| ____|  _ \/ ___|
#?						|  _| |  _ \ __) || | | | | |_) / _ \ | |_) |  / _ \ | |\/| |  _|   | | |  _| | |_) \___ \
#?						| |___| |_) / __/ | |_| | |  __/ ___ \|  _ <  / ___ \| |  | | |___  | | | |___|  _ < ___) |
#?						|_____|____/_____(_)___/  |_| /_/   \_\_| \_\/_/   \_\_|  |_|_____| |_| |_____|_| \_\____/
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

#------------------

#! All DCDC simulation parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Simulation Parameters

simParams			= 	{																																	#*	simulation run parameters
							'tSim'      		  	: 24e-3			  																					,  	#?	total simulation time
                            'tStart'    		 	: 0.0e-3		  																					,  	#?	converter start time
                            'Maxstep'   		  	: 1e-3			  																					,  	#?	maximum simulation step size
                            'Fixedstep' 		  	: 2e-10			  																					,  	#?	fixed simulation step size
                            'tBegin'    		  	: 0e-3			  																					,   #?	start time of probing
                            'tEnd'      		  	: 23e-3			  																					,  	#?	end time of probing
                            'RelTol'    		  	: 1e-3 			  																					,  	#?	relative tolerance of solvers
                            'ZeroCross' 		  	: 0000          																						#?	max number of consecutive zero-crossings
                        }

OutputTimes			=	{
    						'tEnd'					: 0.50e-4	,
       						'tStart'				: 0.30e-4	,
       						'Npoints'				: 350
      					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Models Selection

Probes				= 	{																																	#*	probes statuses
                            'Electric_Probes'     	: 1 			  																					,	#?	1->Enable | 2->Disable
                            'Thermal_Probes'     	: 2 			  																					,	#?	1->Enable | 2->Disable
                            'Control_Probes'      	: 6       		  																						#? 	1->Peak Buck | 2->Duty Precharge | 3->Duty Boost | 4->Duty Buck | 5->Open-Loop Buck | 6->Disable
                        }

ToFile				=	dp.OrderedDict({																													#*	PLECS built-in data output configuration
							'Config'				:			  'DCDC_S'																				,	#?	select submodel simulation
							'OutputTimes'			:			  3																						,	#?	1->Enable-RPC 2->Enable-ToFile | 3->Disable
							'CurrentExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'VoltageExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'ThermalExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'StatsExport'			:			  2																						,	#?	1->Enable | 2->Disable
							'ControlExport'			:			  2																						,	#?	1->Enable | 2->Disable
       						'FileName'				:		      ''																					,	#?	name of the exported data file
							'Ts'					:			  0																						,	#?	sample time for the data export, 0 for continuous sampling
							'Y1'					:	{																									#!	data set 1
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 66																						#?	length of export data
							},
							'Y2'					:	{																									#!	data set 2
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 66																						#?	length of export data
							},
							'Y3'					:	{																									#!	data set 3
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 66																						#?	length of export data
							},
							'Y4'					:	{																									#!	data set 4
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 57																						#?	length of export data
							},
							'Y5'					:	{																									#!	data set 5
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 57																						#?	length of export data
							},
							'Y6'					:	{																									#!	data set 6
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 57																						#?	length of export data
							},
							'Y7'					:	{																									#!	data set 7
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 22																						#?	length of export data
							},
							'Y8'					:	{																									#!	data set 8
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 11																							#?	length of export data
							},
							'Y9'					:	{																									#!	data set 9
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 5																							#?	length of export data
							},
							'Y10'					:	{																									#!	data set 10
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 4																							#?	length of export data
							},
							'Y11'					:	{																									#!	data set 11
								'Config'						: 2																						,	#?	1->Enable | 2->Disable
								'Length'						: 134																						#?	length of export data
								}
           })
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Model Configurations

PSFBconfigs			= 	{																																	#*	PSFB components model configuration
						'Config'      		  		: 3				  																					,   #? 	1->Complex | 2->Simple | 3->Ideal
                        'ControlConfig'    	  		: 1				  																					,   #? 	1->Peak Buck | 2->Duty Precharge | 3->Duty Boost | 4->Duty Buck | 5->Open-Loop Buck
                        'Dual_Enable'   	  		: 2				  																					,   #? 	1->Enable | 2->Disable
                        'Single_Enable' 	  		: 1				  																					,   #?  1->Enable | 2->Disable
                        # 'HB1'    			  		: 5				  																					,   #?  1->real MOSFET & real Bdiode  | 2->real MOSFET & ideal Bdiode
                        # 'HB2'      			  	: 5				  																					,   #? 	3->ideal MOSFET & real Bdiode | 4->real diodes | 5->integrated Bdiode
                        # 'HB3'    			  		: 6 			  																					,   #? 	6->separate Bdiode | 7->diodes | 8->no Bdiode - thermal
                        # 'HB4' 				  	: 6				  																					,   #? 	9->integrated Bdiode - thermal | 10->separate Bdiode - thermal | 11->diodes - thermal
                        'HV_Filter'   		  		: 2				  																					,   #? 	1->With Y-Caps | 2->No Y-Caps | 3->Pass
                        'LV_Filter' 		  		: 1				  																					,   #?	1->With Y-Caps | 2->No Y-Caps | 3->Pass
                        'ShortCircuit'    	    	: 2       																							,	#?	1->MOSFET | 2->Resistive | 3->Pass
						'LV_BuffDiv'				: 1																										#?	1->buffered divider | 2->unbuffered divider
                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Rbox Model Configurations

RboxConfigs			=	{																																	#*	Rbox components configuartions
							'Rbox'      		  	: 2																									,	#? 	1->Complex | 2->Ideal
                            'DC_Link'    		  	: 2																									,   #? 	1->Complex | 2->Simple
                            'Cdc_Switch'   		  	: 0																									,   #? 	0->Disconnected DC Link | 1->Connected DC Link
                            'MainPlus' 			  	: 2																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
							'MainMinus' 		  	: 2																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
							'USMplus'   		  	: 2																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
							'USMminus'  		  	: 2																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
							'USMmid'    		  	: 2																									,   #?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
							'DCDC'      		  	: 2                         																			#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
						}

Relays				=	{																																	#*	relays configurations
							'MainPlus' 			:	{																										#!	Main plus relay configuration
														'Ron' 	  				: 150e-6																, 	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	, 	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]	  															, 	#?	relay time control vector
														'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
													},
							'MainMinus'			:	{		 																								#!	Main minus relay configuration
														'Ron' 	  				: 150e-6																, 	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	, 	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]																, 	#?	relay time control vector
														'OutVec'  				: [1, 1]      																#?	relay status vector, 0->open | 1->closed
													},
							'USMplus'				:	{																									#!	USM plus relay configuration
														'Ron' 	  				: 150e-6																,  	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	, 	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]																,  	#?	relay time control vector
														'OutVec'  				: [0, 0]        														 	#?	relay status vector, 0->open | 1->closed
													},
							'USMminus'			:	{																										#!	USM minus relay configuration
														'Ron' 	  				: 150e-6																,  	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	,  	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]																,  	#?	relay time control vector
														'OutVec'  				: [0, 0]        														    #?	relay status vector, 0->open | 1->closed
													},
							'USMmid'				:	{																									#!	USM mid relay configuration
														'Ron' 	  				: 150e-6																,  	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	,  	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]																,  	#?	relay time control vector
														'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
													},
       						'DCDC'				:	{																										#!	DCDC relays configuration
														'Ron' 	  				: 150e-6																,  	#?	relay closed-state resistance
														'Roff'					: 1e9																	,	#?	relay open-state resistance
														'L'   	  				: 10e-9																	,  	#?	relay inductance
														'tau'					: 40e-9																	,	#?	relay switching time constant
														'TimeVec' 				: [0, 1]																,  	#?	relay time control vector
														'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
													}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Operation Parameters

Control				=	{																																	#*	reference and control targets
 						'LoopType'  :{																														#!	selection between closed-loop or open loop
							'TimeVec'				: [0, 1]																							,	#?	loop type time vector
							'OutVec'				: [0, 0]																								#?	loop type output vector
									},
						'Targets'	:{																														#!	control loop target values
							'Pout'     	  			: 2.6e3																								,	#?	Full-load power
							'Vout'        			: 13.5																								,	#?	Output reference voltage
							'Vinref'      			: 425																								,	#?	Boost reference voltage
							'Iosat1'      			: 100																								,	#?	Max inductor current at first precharge period
							'Iosat2'	  			: 150																								,	#?	Max inductor current at second precharge period
							'Iosat3'	  			: 100																								,	#?	Max inductor current during packs balancing
							'Pcmax'					: 2600																								,	#?	Maximum saturated buck output power
							'Icmax'       			: 200      																								#?	Maximum saturated buck inductor current
									},
						'Inputs'   :{																														#!	input referece values
							'Vin1'        			: 400																								,	#?	constant rail 1 input voltage
							'Vin2'        			: 400																								,	#?	constant rail 2 input voltage
							'Vinvec1'	  			: [225, 345, 355, 415]																				,	#?	variable rail 1 input voltage
							'Vinvec2'	  			: [215, 355, 345, 425]																				,	#?	1->constant Vin | 2->variable Vin
							'OutLen1'				: [1, 1, 1, 1]																						,	#?	number of repetition of each Vin1 point
							'OutLen2'				: [1, 1, 1, 1]																						,	#?	number of repetition of each Vin2 point
							'Vinslct1'    			: 1																									,	#?	rail 1 input voltage behavior, 1->constant Vin | 2->variable Vin
							'Vinslct2'    			: 1	                    																			   	#?	rail 2 input voltage behavior, 1->constant Vin | 2->variable Vin
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
							'Vin'      				: Control['Inputs']['Vin1'] 																			#?	Initial HV capacitors voltages
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
							'Config'    			: 2																									,	#?	1->variable ohmic-inductive | 2->variable ohmic | 3->variable current | 4->constant resistance | 5->constant current | 6->Pass
							'Type'	   				: 1																									,	#?	1->ohmic load | 2->current load
							'Select'				: 2																									,	#?	1->constant load | 2->variable load
							'R_L'       			: Control['Targets']['Vout']**2/Control['Targets']['Pout']											,	#?	resistive-load model
							'I_L'       			: Control['Targets']['Pout']/Control['Targets']['Vout']												,	#?	current-load model
							'Rvec'      			: (dp.np.array([2, 10, 1, 4, 1])*Control['Targets']['Vout']**2/Control['Targets']['Pout']).tolist()	,	#?	resistive-load vector
							'Pvec'     				: (dp.np.array([0.1, 1, 0.2, 0.5, 1])*Control['Targets']['Pout']).tolist()							,	#?	constant power-load vector
							'OutLen'				: [1, 1, 1, 1, 1]																					,	#?	number of repetition of each load point
							'slpPos'				: 500e3																								,	#?	positive current change slope
							'slpNeg'				: -500e3																							,	#?	negative current change slope
							'Tau'					: 75e-6																								,	#?	time-constant of the dynamic load changes
							'Tsim'      			: simParams['tSim']						 																#?  simulation time that the load vectors is calculated with
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
								'Upper'							:	50.0																				,
								'Lower'							:	20.0
											}
						}

shortCircuit		=	{																																	#*	short-circuit events behavior
							'HV'		:	{																												#!	HV side short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
								'Ron'							:	1e-3																				,	#?	short-circuit impedance
								'Roff'							:	1e9																					,	#?	open-circuit impedance
								'L'								:	1e-9																				,	#?	short-circuit inductance
								'tau'							:	40e-9																				,	#?	short-circuit event time constant
								'TimeVec'						:	[0, 1]																				,	#?	time vector for activation of short-circuit event
								'OutVec'						:	[0, 0]																					#?	enable vector for activation of short-circuit event
								},
							'LV'		:	{																												#!	LV side short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
								'Ron'							:	1e-3																				,	#?	short-circuit impedance
								'Roff'							:	1e-3																				,	#?	open-circuit impedance
								'L'								:	1e-9																				,	#?	short-circuit inductance
								'tau'							:	40e-9																				,	#?	short-circuit event time constant
								'TimeVec'						:	[0, 1]																				,	#?	time vector for activation of short-circuit event
								'OutVec'						:	[0, 0]																					#?	enable vector for activation of short-circuit event
								},
							'Trafo'		:	{																												#!	Transformer primary short-circuit
								'Config'						:	4																					,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass
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

HVfuse				= Fuses['MEV55C']																														#*	HV input fuse

HVcmc				=	{																																	#*	HV CMC choke parameters
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
							'Vinit'     			:	Initials['Vin']        																			#?	capacitor initial voltage
						}

Cpi 				=	{																																	#*	HV Pi capacitor parameters
							'Config'    			:	2																								, 	#?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	5e-6																							,	#?	single capacitor value
							'Rsingle'   			:	24.5e-3																							,	#?	ESR of single capacitor
							'Lsingle'   			:	27.5e-9																							,	#?	ESL of single capacitor
							'nPar' 	   				:	2						 																		,  	#?	number of parallel connections
							'nSer' 	  		 		:	1																								, 	#?	number of series connections
							'Vinit'     			:	Initials['Vin']        																				#?	capacitor initial voltage
						}

Cyi					= 	{																																	#*	HV Y-capacitors parameters
							'Config'    			:	2																								,	#?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	3.3e-9																							,	#?	single capacitor value
							'Rsingle'   			:	4.0  																							,	#?	ESR of single capacitor
							'Lsingle'   			:	1e-9																							,	#?	ESL of single capacitor
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

Trafo				=	Mags['Cyntec_EB2_Trafo']																											#*	main transformer parameters

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
                        'LV_FB'	:	{																														#!	LV full-bridge RC snubbers parameters
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
							'R'						:	3.0e3																							,	#?	resistance value
							'nPar'					:	2																									#?	number of parallel resistors
						},
						'Cs'		:	{																										            #!	snubber capacitors
							'Config'    			:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	1.41e-6																							,   #?	single capacitor value
							'Rsingle'   			:	8.046e-3																						,   #?	ESR of single capacitor
							'Lsingle'   			:	0.0																								,   #?	ESL of single capacitor
							'nPar' 	    			:	12																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0																									#?	capacitor initial voltage
						},
                        'Switch'     				:	Switches['SQJQ186ER_2']																			,	#?	clamp switch
					}
RCDclamp['Switch']['nParallel'] 	=	2

ERCclamp 		=	{																																		#*	energy recovery clamp parameters
                        'Config'					:	2																								,	#!	1->Enable | 2->Disable
						'Diode'     :  {																													#! diode parameters
							'Vf'       				:	0.0																								,   #?	diode forward voltage
							'Rdon'     				:	0																								   	#?	diode on-state resistance
						},
						'Cs'		:	{																										            #!	snubber capacitors
							'Config'    			:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass
							'Csingle'   			:	0																						    	,   #?	single capacitor value
							'Rsingle'   			:	0																								,   #?	ESR of single capacitor
							'Lsingle'   			:	0.0																								,   #?	ESL of single capacitor
							'nPar' 	    			:	1																								,   #?	number of parallel connections
							'nSer' 	    			:	1																								,   #?	number of series connections
							'Vinit'     			:	0																									#?	capacitor initial voltage
						},
                      }

FRW				=		{																																	#*	freewheeler parameters
						'Config'					:	3																								,	#?	1->ideal | 2->nonideal | 3->pass
                        'clampConfig'				:	1																								,	#?	0->freewheeler | 1->active clamp
						'Switch'     				:	Switches['SQJQ186ER_2']																			,	#?	freewheeling switch parameters
                        'Duty'						:	0.05 																							,	#?	clamp turn on time
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

Lf					= 	Mags['Cyntec_EB2_Choke']																											#*	LC filter output choke parameters

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
							'Lsingle'  				:	5e-9			   																				,   #?	ESL of single capacitor
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
							'Lpri'					:	0																								,	#?	parasitic inductance between HV legs
							'Lsec'					:	0																									#?	parasitic inductance between LV legs
}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------LV Filter Parameters

LVdmc				= 	{																																	#*	LV DMC choke parameters
							'Lself' 				:	3.52e-6																							,   #?	windings self inductance
							'Cwind'					:	0.0																								,	#?	intrawinding capacitance
							'Rwind'					:	0.0																								,   #?	windings resistance
							'Km'    				:	0.9490																							,  	#?	coupling factor
							'Cm'					:	0.0																								,	#?	interwinding capacitance
							'Rm'					:	0			 		            																,   #?	mutual resistance
							'N'						:	1																									#?	number of turns
						}

LVcmc				= 	{																																	#*	LV CMC choke parameters
							'Lself' 				:	3.2e-6																							,   #?	windings self inductance
							'Cwind'					:	0.0																								,	#?	intrawinding capacitance
							'Rwind' 				:	0.0			  																					,   #?	windings resistance
							'Km'    				:	0.9400																							,   #?	coupling factor
							'Cm'					:	0.0																								,	#?	interwinding capacitance
							'Rm'					:	0			 		            																,   #?	mutual resistance
							'N'						:	1																									#?	number of turns
						}

Coc					=	{																																	#*	LV filter ceramic capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	2.35e-6																							,   #?	single capacitor value
							'Rsingle'  				:	5e-3																							,   #?	ESR of single capacitor
							'Lsingle'  				:	862e-12																							,   #?	ESL of single capacitor
							'nPar' 	   				:	4																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Coe2				= 	{																																	#*	LV filter electrolytic capacitors parameters
							'Config'   				:	5																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	0																								,   #?	single capacitor value
							'Rsingle'  				:	0																								,   #?	ESR of single capacitor
							'Lsingle'  				:	0																								,   #?	ESL of single capacitor
							'nPar' 	  				:	1																								,   #?	number of parallel connections
							'nSer' 	  				:	1																								,   #?	number of series connections
							'Vinit'    				:	0																								,   #?	capacitor initial voltage
							'Rd'	   				:	0				                																    #?	damping resistor
						}

Cyo					=	{																																	#*	LV Y-capacitors parameters
							'Config'   				:	2																								,   #?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor
							'Csingle'  				:	5.5e-6																							,   #?	single capacitor value
							'Rsingle'  				:	4.0e-3																							,   #?	ESR of single capacitor
							'Lsingle'  				:	5e-9																							,   #?	ESL of single capacitor
							'nPar' 	   				:	1																								,   #?	number of parallel connections
							'nSer' 	   				:	1																								,   #?	number of series connections
							'Vinit'    				:	Initials['Vout']	            																    #?	capacitor initial voltage
						}

Busbars_PCB			=	{																																	#*	PCB traces and/or busbars resistances
							'LV_Filter'		:	{																											#!	LV filter inline resistances
                                'PlusResistance'		:	96.00e-6 + 167e-6 + 60e-6																	,	#?	positive line resistance
								'MinusResistance'		:	132.4e-6 + 148e-6 + 60e-6																		#?	negative line resistance
							},
                            'B_plus'		:	{																											#!	B plus inline resistances
                                'Rail_1'				:	0																							,	#?	rail 1 inline resistance
                                'Rail_2'				:	0																							,	#?	rail 2 inline resistance
                                'Common'				:	0																								#?	shared resistance between two rails
							},
                            'B_minus'		:	{																											#!	B minus inline resistances
                                'Rail_1'				:	0																							,	#?	rail 1 inline resistance
                                'Rail_2'				:	0																							,	#?	rail 2 inline resistance
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
							'Config'   				:	3																								,   #? 	1->Complex Model | 2->Simple Model | 3->Pass
							'V'        				:	Control['Targets']['Vout'] - 50e-3																,   #?	battery voltage
							'R'        				:	5e-3			     		 	 																	#?	internal battery resistance
						}

EnBn				= 	{																																	#*	LV Bordnetz parameters
							'Config'   				:	2																								,   #?	1->enable | 2->disable
							'R'        				:	5e-3																							,   #?	lumped resistance
							'L'        				:	2.5e-6																							,   #?	lumped inductance
							'C'       				:	10e-3			            																		#?	lumped capacitance
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
							'Rpass'     			: 250e3           																					,  	#? 	Vehicle DC link passive discharge
							'Pdc'       			: 0.0             							     														#? 	Vehicle DC link constant load
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PWM Parameters

MCU					= 	{																																	#*	microcontroller timings parameters
							'f_pwm'         		:	100e6																							,   #? 	PWM module frequency
							'f_s'           		:	100e3																							,   #? 	switching frequency
							'T_s'           		:	10e-6																							,   #? 	switching period
							'Tpecu' 	    		:	1.0e-3		                    																    #? 	cycle time of PeCU/PeSU
						}

PWM					= 	{																																	#*	microcontroller PWM parameters
							'M'             		:	MCU['f_pwm']/MCU['f_s']																			,   #? 	gain stage of PWM module MCU.f_pwm/MCU.f_s
							'Dmax' 	       			:	0.99			    																			,   #? 	maximum duty cycle
							'Dmin'          		:	0.01																							,   #? 	minimum duty cycle
							'Tdead'         		: 	50e-9               																			,   #? 	full-bridge deadtime [s]
							'Trise'    				: 	50e-9               																			,   #? 	synchronous rectifiers rising edge delay
							'Tfall'					:	50e-9																							,	#? 	synchronous rectifiers falling edge delay
							'PCMCconfig'			:	1																								,	#?	1->Variable PWM generation | 2->Static PWM generation
                            'PCMCinterleave'		:	1																								,	#?	rail interleaving in buck, 0-> non-interleaved rails | 1->interleaved rails
							'CCM'           		: 	1                               																,   #?	0->Disable CCM Modulation | 1->Enable CCM Modulation | 2->Disable DCM Modulation
							'ActiveSR'				:	1																								,	#? 	1->active rectification | 0->passive rectification
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
								'S58'			:	{																										#	PWM S58 configuration
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
								'S67'			:	{																										#	PWM S67 configuration
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
								'S58'			:	{																										#	PWM S58 configuration
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
								'S67'			:	{																										#	PWM S67 configuration
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

dischargePWM		= 	{																																	#*	active discharge control
							'Config'					:	1																							,	#?	1->Enable | 2->Disable
							'Rdis' 						:	10.0																						,	#?	discharging resistance
							'Discharge_TimeVec' 		:	[1.0, 1.0]	   																				,   #?	active discharge activation time vector
							'Discharge_OutVec'  		:	[0, 0]																						,   #?	active discharge activation status vector, 0->inactive | 1->active
							'Rail_1'  :	{																													#!	rail 1 (lower rail) active discharge parameters
								'Slope'   				:	1/3      																					,   #?	duty cycle slope
								'Slope_TimeVec'			:	[1.0, 1.0]	   																				,	#?	slope activation time vector
								'Slope_OutVec'  		:	[0, 0]				            															    #?	slope activation status vector, 0->inactive | 1->active
										},
							'Rail_2'  :	{																													#!	rail 2 (upper rail) active discharge parameters
								'Slope'   				:	1/3      																					,   #?	duty cycle slope
								'Slope_TimeVec' 		:	[1.0, 1.0]	   																				,  	#?	slope activation time vector
								'Slope_OutVec'  		:	[0, 0]			                																#?	slope activation status vector, 0->inactive | 1->active
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
								'Rfil'					:	1e3																							,	#?	input signal filter resistance
								'Cfil'					:	100e-12																						,	#?	input signal filter capacitance
								'UpBand'				:	250.0																						,	#?	upper heysteresis band for positive currents
								'LoBand'				:	230.0																						,	#?	lower heysteresis band for positive currents
								'Delay'					:	52e-9																						,	#? 	overall propagation delay
								'Vcc'					:	3.3																							,	#?	upper rail supply voltage
								'Vee'					:	0.04																						,	#?	lower rail supply voltage
								'Vin'					:	3.0																								#?	input reference voltage
												},
							'OutputCurrentNeg':	{																											#!	output voltage fault logic parameters
								'R1'					:	1.96993e3																					,	#?	reference voltage divider supply resistance
								'Rfil'					:	1e3																							,	#?	input signal filter resistance
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
								'Cfil'					:	100e-12																						,	#?	input signal filter capacitance
								'UpBand'				:	469.2																						,	#?	upper heysteresis band
								'LoBand'				:	435.0																						,	#?	lower heysteresis band
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

ADCmodel			=	{																																	#*	microcontroller ADC model parameter
							'RailsConfig'			:   1																								,	#?	1->enable | 2->disable
							'Config'				:	2																								,	#?	1->physical model | 2->small-signal model | 3->ideal model
							'Cpar'					:	13e-12																							,	#?	channel parasitic capacitance
							'Ileak'					:	300e-9																							,	#?	channel leakage current
							'Radc'					:	425																								,	#?	sample-and-hold resistance
							'Csh'					:	14.5e-12																						,	#?	sample-and-hold capacitance
							'Rdis'					:	100.0																							,	#?	sample-and-hold discharge resistance
							'Fs'					:	100e3																							,	#?	sampling frequency
							'Ts'					:	10e-6																							,	#?	sampling period
							'Tacq'					:	1.0e-6																							,	#?	acquisition time window
                            'Tconv'					:	200e-9																							,	#?	conversion time window
							'Tdead'					:	0.0																								,	#?	deadtime between acquisition & discharge
							'Quantize'				:	1																								,	#?	1->floor | 2->ceil | 3->round | 4->fix
                            'InputFilters'	:	{																											#*	ADC input filters parameters
								'LV_voltageSense'	:	{																									#!	LV voltage sensor filter parameters
									'Rfil'			:	499																								,	#?	filter resistance
                                    'Cfil'			:	10e-9																								#?	filter capacitance
								},
                                'HV_voltageSense'	:	{																									#!	HV voltage sensor filter parameters
									'Rfil'			:	100																								,	#?	filter resistance
                                    'Cfil'			:	10e-9																								#?	filter capacitance
								},
                                'LV_currentSense'	:	{																									#!	LV current sensor filter parameters
									'Rfil'			:	200.0																							,	#?	filter resistance
                                    'Cfil'			:	330e-12																								#?	filter capacitance
								},
                                'HV_currentSense'	:	{																									#!	HV current sensor filter parameters
									'Rfil'			:	100																								,	#?	filter resistance
                                    'Cfil'			:	330e-12																								#?	filter capacitance
								},
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Sensor Parameters

LV_voltageSense		=	Sensors['BuffDivider_3']																											#*	LV voltage sensor
HV_voltageSense		=	Sensors['SI8932D']																													#*	HV voltage sensor
LV_currentSense 	= 	Sensors['INA240A2']																													#*	LV current sensor
HV_currentSense		=	Sensors['ACS724']																													#*	HV current sensor
CT					=	Sensors['DS_P100076']																												#*	current transformer sensor

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------PSFB Controllers

#Digital PCMC controller-------------------------------------------------------
PCMCbuck 			=	{																																	#*	peak buck mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain | 3->disable
							'Vct'					:	ADCres['Vdac']																					,	#?	open-loop transformer reference voltage
							'VctSelect'				: 	0																								,	#?	0->custom open-loop transformer reference voltage | 1->controller reference voltage value
							'Kp'             		:	0.84              																				,	#?	proportional gain
							'Ki'             		:	85800*MCU['T_s']    																			,   #?	integral gain
							'UpLim'			 		:	2**ADCres['Ndac'] - 1																			,	#?	upper saturation limit
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
							'UpLim'			  		:	PWM['Dmax']*PWM['M']	  																		,	#?	upper saturation limit
							'MdLim'			  		:	PWM['M']/2	     																				,	#?	middle saturation limit
							'MdLimOffset'			:	0																								,	#?	middle saturation limit offset
							'LoLim'			  		:	0       		  																				,	#?	lower saturation limit
							'CCMcurrent'	  		:	25				  																				,	#?	current threshold to switch to CCM mode
                            'CurrentConfig'			:	1																								,	#?	precharge current configurations, 1->online calculation | 2->fixed lookup | 3->constant currents
							'outputScale'	  		:	2.0			  																					,	#?	controller output scaling
							'RateSlope'		  		:	0.05			  																				,	#?	rate limiter current slope per 10us
							'Vdelta'         		:	35                	            																,   #?	undervoltage difference where slope starts
                            'Icmax'					:	40																								,	#?	maximum capacitor current allowed during precharge of the precharge
                            'ILVmax'				:	100																								,	#?	maximum DC current allowed during precharge of the precharge
                            'Vsnub'					:	60																								,	#?	maximum allowed active snubber voltage during precharge of the precharge
                            'tonsnub_min'			:	400e-9																							,	#?	minimum on-time for the active snubber during precharge of the precharge
                            'tonsnub_final'			:   200e-9																							,	#?
							'ohmicOffset'			:	0																								,	#?	add ohmich offset to the reference voltage
							'enableOffset'			:	0																									#?	0->disable | 1->enable
						}

# Digital ACMC boost controller------------------------------------------------
ACMCboost			= 	{																																	#*	boost mode controller
							'Config'				:	1																								,	#?	1->discrete-time domain | 2->continuous-time domain
							'Kp'              		:  	0.165              																				,	#?	proportional gain
							'Ki'              		:	0.0040             																				,   #?	integral gain
							'UpLim'			  		:	PWM['Dmax']*PWM['M']/2																			,	#?	upper saturation limit
							'LoLim'			  		:	PWM['Dmin']*PWM['M']/2   																		,	#?	lower saturation limit
							'CCMcurrent'	  		:	25																								,	#?	current threshold to switch to CCM mode
							'outputScale'	  		:	1.0			    																				,	#?	controller output scaling
							'RateSlope'		  		:	2.0				 	 																			,	#?	rate limiter current slope per 10us
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
							'Kp'              		:	0.2                																				,	#?	proportional gain
							'Ki'              		:	0.0095             																				,   #?	integral gain
							'UpLim'			  		:	PWM['Dmax']*PWM['M']/2																			,	#?	upper saturation limit
							'LoLim'			  		:	PWM['Dmin']*PWM['M']/2																			,	#?	lower saturation limit
							'CCMcurrent'	  		:	40																								,	#?	current threshold to switch to CCM mode
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
Trise				=	{																																	#*	boost mode rectifier rising edge calculator
							'TdeadFactor'       	:   6               																				,	#?	maximum allowed deadtime for earlier turn-on
							'LeakageFactor'     	:	2.6                             																    #?	correction factor for the leakage inductance
						}

# Soft-start ramps-------------------------------------------------------------
softStart			=	{																																	#*	buck/boost soft-start paramters
							'BuckRamp'          	:   1.0             																				,   #?	Buck current ramp per 10us
							'BoostRamp'         	:   1.0                             																    #?	Boost current ramp per 10us
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Active Switches

LeftLeg_1			=	Switches['AIMDQ75R060M1H']																											#*	HV left leg switches parameters
LeftLeg_2			=	Switches['AIMDQ75R060M1H']																											#*	HV left leg switches parameters
RightLeg_1			=	Switches['AIMDQ75R060M1H']																											#*	HV right leg switches parameters
RightLeg_2			=	Switches['AIMDQ75R060M1H']																											#*	HV right leg switches parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Rectifier Switches

Rectifier_1			=	Switches['SQJQ186ER_1']																												#*	LV rectifier switches parameters
Rectifier_2			=	Switches['SQJQ186ER_1']																												#*	LV rectifier switches parameters
Rectifier_3			=	Switches['SQJQ186ER_1']																												#*	LV rectifier switches parameters
Rectifier_4			=	Switches['SQJQ186ER_1']																												#*	LV rectifier switches parameters
Rectifier_1['nParallel'] 		=	2
Rectifier_2['nParallel'] 		=	2
Rectifier_3['nParallel'] 		=	2
Rectifier_4['nParallel'] 		=	2

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Short-Circuit Switch

SC_Switch			=	Switches['SQJQ144AER']																												#*	short-circuit switch parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Thermal Parameters

Thermal 			=   {																																	#* 	thermal conditions
							'Tinit'             	:   35           		 																			,	#? 	initial temperature of semiconductors and heatsinks
							'Tjmax'					:	175																								,	#?	maximum junction temperature for semiconductor switches
							'Tjmin'					:	-55																								,	#?	minimum junction temperature for semiconductor switches
							'Twater'            	:	35                                          													,	#? 	coolant temperature
							'BuckBoost'				:	0																									#?	1->buck operation | 2->boost operation
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#! All ThermalChains simulation parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Junction 			=   {																																	#* 	junction thermal chain parameters
							'Rth_vector'          	:   [0, 0]          		 																		,	#? 	thermal resistance vector
							'Cth_vector'		    :	[0, 0] 																							,	#?	thermal capacitance vector
							'Tinit'					:	0																									#?	initial temperature
						}

Heatsink 			=   {																																	#* 	heatsink thermal chain parameters
							'Rth_vector'          	:   [0, 0]          		 																		,	#? 	thermal resistance vector
							'Cth_vector'		    :	[0, 0] 																							,	#?	thermal capacitance vector
							'Tinit'					:	0																									#?	initial temperature
						}

Switch				=	{																																	#*	switch parameters
							'Transistor'  			: 	{																									#!	transistors parameters
									'TCR'           		:   Switches['AIMDQ75R063M1H']['Transistor']['Rvec']                						,   #? 	Rdson temperature coefficient
									'LossSW'                :   0                                       												, 	#? 	switching losses
									'Irms_Vector'			:	[0,0]																						#?	rms current profile
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Vf'           			:   Switches['AIMDQ75R063M1H']['BodyDiode']['Vf']                   						,   #? 	diode forward voltage
									'Rd_on'               	:   Switches['AIMDQ75R063M1H']['BodyDiode']['Rd_on']		        						,  	#? 	body diode reverse recovery charge
									'Irms_Vector'			:	[0,0]																					,	#?	rms current profile
									'Iavg_Vector'			:	[0,0]																						#?	average current profile
						},
							'Diode'					: 	{																									#!	passive diodes parameters
									'Vf'           			:   Switches['AIMDQ75R063M1H']['BodyDiode']['Vf']                   						,   #? 	diode forward voltage
									'Rd_on'               	:   Switches['AIMDQ75R063M1H']['BodyDiode']['Rd_on']		        						,  	#? 	body diode reverse recovery charge
									'Irms_Vector'			:	[0,0]																					,	#?	rms current profile
									'Iavg_Vector'			:	[0,0]																						#?	average current profile
						},
						}

Profile 			=	{																																	#*	main profile parameters
							'Vector'						:	[0, 0]																					,	#?	profile vector
							'Period'						:	[1]																						,	#?	profile period
							'Lengths'						:	[1, 1]																					,	#?	number of repetition of each point
							'Scale'							:	1																						,	#?	profile output scale
							'Delay'							:	[0]																						,	#?	delay of the profile start in seconds
							'SamplingOffset'				:	0																							#?	profile sampling offset
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
							'RelTol'					:	simParams['RelTol']		 																		#?	relative tolerance of solvers
						}

AnalysisOpts		= 	{																																	#*	parameters for analyses
							'TimeSpan'					: 	MCU['T_s']				,																		#?	system period length
							'StartTime'					: 	100e-6					,																		#?	simulation start time
							'Tolerance'					: 	1e-4					,																		#?	relative error tolerance used in the convergence criterion of a steady-state analysis
							'MaxIter'					: 	20						,																		#?	maximum number of iterations allowed in a steady-state analysis
							'JacobianPerturbation'		: 	1e-4					,																		#?	relative perturbation of the state variables used to calculate the approximate Jacobian matrix
							'JacobianCalculation'		: 	'fast'					,																		#?	controls the way the Jacobian matrix is calculated. Options are full and fast
							'InitCycles'				: 	100						,																		#?	number of cycle-by-cycle simulations that should be performed before the actual analysis
							'ShowCycles'				: 	2						,																		#?	number of steady-state cycles of the time span that should be simulated at the end of an analysis
							'FrequencyRange'			: 	[1, 1e9]				,																		#?	range of the perturbation frequencies for small-signal anaylsis
							'FrequencyScale'			: 	'logarithmic'			,																		#?	specifies whether the sweep frequencies should be distributed on a linear or logarithmic
							'AdditionalFreqs'			: 	[]						,																		#?	vector specifying frequencies to be swept in addition to the automatically distributed frequencies
							'NumPoints'					: 	100						,																		#?	The number of automatically distributed perturbation frequencies
							'Perturbation'				: 	''						,																		#?	full block path (excluding the model name) of the Small Signal Perturbation block that will be active during an analysis
							'Response'					: 	''						,																		#?	full block path (excluding the model name) of the Small Signal Response block that will record the system response during an analysis
							'AmplitudeRange'			: 	1e-3					, 																		#?	amplitude of the sinusoidal pulse perturbation for an ac sweep analysis
							'Amplitude'					: 	1e-3					 																		#?	amplitude of the discrete pulse perturbation for an impulse response analysis
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!	assemble all parameters to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ModelVars 			= 	{
							'simParams' 				: 	simParams 				,

							'Probes'  					: 	Probes 					,
							'ToFile'					:	ToFile					,

							'PSFBconfigs'  				: 	PSFBconfigs 			,

							'RboxConfigs'  				: 	RboxConfigs 			,
							'Relays'  					: 	Relays 					,

							'Control'  					: 	Control 				,
							'RailsOperation'  			: 	RailsOperation			,
							'Initials'  				: 	Initials 				,
							'Protection'  				: 	Protection 				,
							'Load'  					: 	Load			 		,
							'RailsEnable'  				: 	RailsEnable 			,
							'DualSingleOperation'		:	DualSingleOperation		,
							'shortCircuit'				:	shortCircuit			,
							'SC_Switch_Control'			: 	SC_Switch_Control 		,
							'loadShifting'				:	loadShifting			,
							'EIS'						:	EIS						,

							'HVfuse'					:	HVfuse					,
							'HVcmc'  					: 	HVcmc 					,
							'Cin'  						: 	Cin 					,
							'Cpi'  						: 	Cpi 					,
							'Cyi'  						: 	Cyi 					,
							'Cc'  						: 	Cc						,
							'Trafo'  					: 	Trafo 					,
							'Cb'  						: 	Cb 						,
							'RCsnubber'  				: 	RCsnubber 				,
							'RCDclamp'					:	RCDclamp				,
							'ERCclamp'					:	ERCclamp				,
							'FRW' 						: 	FRW 					,
							'Lf'  						: 	Lf 						,
							'RCDsnubber'  				: 	RCDsnubber 				,
							'Co'  						: 	Co 						,
							'Coe1' 						: 	Coe1 					,
							'InductancesPCB'			: 	InductancesPCB			,

							'LVdmc'  					: 	LVdmc 					,
							'LVcmc'  					: 	LVcmc 					,
							'Coc'  						: 	Coc 					,
                            'Coe2' 						: 	Coe2 					,
							'Cyo'  						: 	Cyo 					,
							'Busbars_PCB'				:	Busbars_PCB				,

							'LVS'  						: 	LVS 					,
							'EnBn'  					: 	EnBn 					,

							'HVS'  						: 	HVS 					,
							'Cdc'						: 	Cdc						,

							'MCU'  						: 	MCU 					,
							'PWM'  						: 	PWM 					,
							'burstPWM'  				: 	burstPWM 				,
							'burstControl'  			: 	burstControl 			,
							'dischargePWM'  			: 	dischargePWM 			,
							'CPH'  						: 	CPH 					,
							'FaultLogic'				:	FaultLogic				,

							'ADCres'  					: 	ADCres 					,
							'ADCgains'  				: 	ADCgains 				,
							'ADCmodel'					:	ADCmodel				,

							'LV_voltageSense'			:	LV_voltageSense			,
							'HV_voltageSense'			:	HV_voltageSense			,
							'LV_currentSense'			:	LV_currentSense			,
							'HV_currentSense'			:	HV_currentSense			,
							'CT'  						: 	CT 						,

							'PCMCbuck'  				: 	PCMCbuck 				,
							'ACMCprecharge' 			: 	ACMCprecharge 			,
							'ACMCboost'  				: 	ACMCboost 				,
							'ACMCbuck'  				: 	ACMCbuck 				,
							'BalHys'  					: 	BalHys 					,
							'Trise'  					: 	Trise 					,
							'softStart'  				: 	softStart 				,

							'LeftLeg_1'  				: 	LeftLeg_1 				,
                            'LeftLeg_2'  				: 	LeftLeg_2 				,
							'RightLeg_1'  				: 	RightLeg_1 				,
                            'RightLeg_2'  				: 	RightLeg_2 				,
							'Rectifier_1'  				: 	Rectifier_1 			,
                            'Rectifier_2'  				: 	Rectifier_2 			,
                            'Rectifier_3'  				: 	Rectifier_3 			,
                            'Rectifier_4'  				: 	Rectifier_4 			,
							'SC_Switch'  				: 	SC_Switch 				,

							'Thermal'  					: 	Thermal 				,

							'Junction'					:	Junction				,
							'Heatsink'					:	Heatsink				,
							'Switch'					:	Switch					,
							'Profile'					:	Profile					,

							'AnalysisOpts'				:	AnalysisOpts
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

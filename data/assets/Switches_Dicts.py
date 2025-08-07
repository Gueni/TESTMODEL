
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 ____          _ _       _                 ____                                _
#?						/ ___|_      _(_) |_ ___| |__   ___  ___  |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___
#?						\___ \ \ /\ / / | __/ __| '_ \ / _ \/ __| | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?						 ___) \ V  V /| | || (__| | | |  __/\__ \ |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?						|____/ \_/\_/ |_|\__\___|_| |_|\___||___/ |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs switches models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Dependencies as dp

#----------------------------------------------------------------------

#! 	call the Params-Processing class and point to the location of csv data
paramProcess		=	dp.PM.ParamProcess()

switchesCossPath	=	'Script/Data/Switches_Coss/'
switchesCrssPath	=	'Script/Data/Switches_Crss/'
switchesRdsonPath	= 	'Script/Data/Switches_Rdson/'
switchesIdsonPath	= 	'Script/Data/Switches_Rdson_Ids/'
switchesEoffPath    =   'Script/Data/Switches_Eoff/'
switchesEonPath    	=   'Script/Data/Switches_Eon/'
bodyDiodeVIPath 	=	'Script/Data/Diodes_VI/'

#! 	switches models parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------GaN Switches
Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'GS66508T',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'GS66508T',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'GS66508T',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'GS66508T',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'GS66508T',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'GS66508T',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'GS66508T')

GS66508T			=	{																																	#*	GS66508T parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real with limited di/dt | 2->ideal switch
									'Thermal'           	:   'GaN_Systems/GS66508_v3'                                  								,   #? 	selected transistor
									'Custom'            	:   ['Rgon','1','Rgoff','1','vgsoff','1','g','m:g']                 						,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   30	                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650 																						#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   2.6                                 													,   #? 	body diode forward voltage
									'If'                	:   30	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0	                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0			                              												,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.529																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.015,0.23,0.24,0.015]																	,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[8e-5,7.4e-4,6.5e-3,2e-3]																,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   3.50            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	160e-12						 															,	#?	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
							'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   0              																		    ,	#? 	body diode reference current
							'Vs'							:	0																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------SiC Switches

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'AIMDQ75R063M1H',1.0,0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'AIMDQ75R063M1H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'AIMDQ75R063M1H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'AIMDQ75R063M1H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'AIMDQ75R063M1H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'AIMDQ75R063M1H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'AIMDQ75R063M1H')

AIMDQ75R063M1H		=	{																																	#*	AIMDQ75R063M1H parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   'Infineon/CoolSiC/AIMDQ75R063M1H'                                  						,   #? 	selected transistor
									'Custom'            	:   ['TCR','1']                 															,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	2																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   750                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   32	                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	750 																						#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   4.0                                 													,   #? 	body diode forward voltage
									'If'                	:   32	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0	                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   93e-9			                              											,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.359																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.0																						,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [1.0682,1.2039,0.7389,0.427] 															,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [12.8939,1.6758,0.0755,169.4661]            											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	139.1e-12						 														,	#?	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	25.0e-12																				,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#?	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[1.82,3.3,5.15,6.83,10.18]																,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	10.0																						#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[1.82,3.3,5.15,6.83,10.18]																,	#?	ON path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	10.0																						#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   11.3              																		, 	#? 	body diode reference current
							'Vs'							:	500																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'AIMDQ75R060M1H',1.0,0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'AIMDQ75R060M1H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'AIMDQ75R060M1H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'AIMDQ75R060M1H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'AIMDQ75R060M1H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'AIMDQ75R060M1H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'AIMDQ75R060M1H')

AIMDQ75R060M1H		=	{																																	#*	AIMDQ75R060M1H parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	2																						,	#?	choose which NI vector to be used (Vgs=15,18,20)
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   750                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   32	                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	750 																						#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   3.9                                 													,   #? 	body diode forward voltage
									'If'                	:   32	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   16e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   57e-9			                              											,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.359																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.90																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [1.0682,1.2039,0.7389,0.427] 															,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [12.8939,1.6758,0.0755,169.4661]            											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	106e-12							 														,	#?	device parasitic output capacitance
									'R'						:	0																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	0																						,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	25.0e-12																				,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#?	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[1.82,3.3,5.15,6.83,10.18]																,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	10.0																						#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[1.82,3.3,5.15,6.83,10.18]																,	#?	ON path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	10.0																						#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   11.1              																		, 	#? 	body diode reference current
							'Vs'							:	500																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'AIMDQ75R042M1H',1.0,0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'AIMDQ75R042M1H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'AIMDQ75R042M1H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'AIMDQ75R042M1H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'AIMDQ75R042M1H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'AIMDQ75R042M1H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'AIMDQ75R042M1H')

AIMDQ75R042M1H		=	{																																	#*	AIMDQ75R042M1H parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   'Infineon/CoolSiC/AIMDQ75R042M1H'                                  						,   #? 	selected transistor
									'Custom'            	:   ['TCR','1']                 															,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   750                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   42.2                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	750 																						#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   4.0                                 													,   #? 	body diode forward voltage
									'If'                	:   42	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0	                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   144e-9			                              											,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.359																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.82																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [1.399,1.017,0.638,0.453,0.564]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [2.028,16.857,0.757,210.682,0.149]            											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	332.3e-12						 														,	#?	device parasitic output capacitance
									'R'						:	0																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	0																						,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[1.8,5.3,10.2,22.9]																		,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	10.0																						#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[1.82,3.3,5.15,6.83,10.18]																,	#?	ON path gate resistances vector
                                    'Vvec'					:	[200,400]																				,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	10.0																						#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   16.6              																		, 	#? 	body diode reference current
							'Vs'							:	500																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SCTH35N65G2V',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SCTH35N65G2V',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SCTH35N65G2V',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SCTH35N65G2V',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SCTH35N65G2V',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SCTH35N65G2V',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SCTH35N65G2V')

SCTH35N65G2V		=	{																																	#*	SCTH35N65G2V parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   45                                 														,   #? 	transistor drain current
									'Tr'                	:   30e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   44e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650 																						#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   3.3                                 													,   #? 	body diode forward voltage
									'If'                	:   45                                 														,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   18e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   7                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   85e-9	                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.0																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.72																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   4.80            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	125e-12						 															,	#?	device parasitic output capacitance
									'R'						:	0																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	0																						,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   20	              																		, 	#? 	body diode reference current
							'Vs'							:	400																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SCT055HU65G3AG',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SCT055HU65G3AG',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SCT055HU65G3AG',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SCT055HU65G3AG',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SCT055HU65G3AG',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SCT055HU65G3AG',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SCT055HU65G3AG')

SCT055HU65G3AG		=	{																																	#*	SCT055HU65G3AG parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   40                                 														,   #? 	transistor drain current
									'Tr'                	:   27e-9                                													,   #? 	transistor rise time
									'Tf'                	:   19.4e-9                                    												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   3.0                                 													,   #? 	body diode forward voltage
									'If'                	:   40                                 														,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   51e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   6.3                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   71e-9	                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.0																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.85																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   4.80            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	139.08e-12					 															,	#?	device parasitic output capacitance
									'R'						:	0																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	0																						,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss		           																	,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   15	              																		, 	#? 	body diode reference current
							'Vs'							:	400																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Si Switches

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'IAUT300N10S5N015',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'IAUT300N10S5N015',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'IAUT300N10S5N015',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'IAUT300N10S5N015',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'IAUT300N10S5N015',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N10S5N015',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'IAUT300N10S5N015')

IAUT300N10S5N015	=	{																																	#*	IAUT300N10S5N015 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   55e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   118e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   90e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   220e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.444																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[2.202e-4,3e-2,7.642e-2,3.729e-5,2.401e-1,5.318e-2]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[4.541e-2,3.333e-3,1.309e-2,2.682e2,4.164e-1,1.880e1]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.8]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1920e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,1000]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	1																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	50																							#?	body diode reference voltage
						}
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMJST3D3N08X',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMJST3D3N08X',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMJST3D3N08X',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMJST3D3N08X',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMJST3D3N08X',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST3D3N08X',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMJST3D3N08X')

NVMJST3D3N08X		=	{																																	#*	NVMJST3D3N08X parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.183																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   194                                 													,   #? 	transistor drain current
									'Tr'                	:   31e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   39e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   194                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   22.6e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   151e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.445																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.003073492,0.0145417,0.0365529,0.142744,0.378208]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000035866,0.00009899,0.00071709,0.0019792,0.0214]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	798e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,1000]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	1																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   31              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVBYST0D6N08X',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVBYST0D6N08X',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVBYST0D6N08X',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVBYST0D6N08X',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVBYST0D6N08X',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBYST0D6N08X',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVBYST0D6N08X')

NVBYST0D6N08X		=	{																																	#*	NVBYST0D6N08X parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.167																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   856                                 													,   #? 	transistor drain current
									'Tr'                	:   77e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   114e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   856                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   42e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   513e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.558																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.000898284,0.00345812,0.0102355,0.0174793,0.141617]									,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.00034051,0.00093982,0.0040849,0.011274,0.0214]										,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	4665e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,1000]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	1																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMJST004N08X',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMJST004N08X',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMJST004N08X',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMJST004N08X',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMJST004N08X',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST004N08X',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMJST004N08X')

NVMJST004N08X		=	{																																	#*	NVMJST004N08X parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.156																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   409                                 													,   #? 	transistor drain current
									'Tr'                	:   29e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   37e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   409                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   21e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   138e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.463																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00352257,0.016627,0.0383147,0.160293,0.427985]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000031294,0.000086371,0.00062568,0.0017269,0.0214]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	699e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
                                    'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,1000]																				,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	1																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   27              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVBLS1D5N10MC',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVBLS1D5N10MC',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVBLS1D5N10MC',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVBLS1D5N10MC',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVBLS1D5N10MC',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D5N10MC',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVBLS1D5N10MC')

NVBLS1D5N10MC		=	{																																	#*	NVBLS1D5N10MC parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   110e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   143e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.625																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.45																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	5100e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	          																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   71              																		, 	#? 	body diode reference current
							'Vs'							:	50																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVBLS1D7N10MC',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVBLS1D7N10MC',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVBLS1D7N10MC',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVBLS1D7N10MC',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVBLS1D7N10MC',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D7N10MC',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVBLS1D7N10MC')

NVBLS1D7N10MC		=	{																																	#*	NVBLS1D7N10MC parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   110e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   143e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.585																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.49																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	5100e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	          																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   62              																		, 	#? 	body diode reference current
							'Vs'							:	50																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'IAUT300N08S5N014',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'IAUT300N08S5N014',1.27)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'IAUT300N08S5N014',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'IAUT300N08S5N014',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'IAUT300N08S5N014',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N08S5N014',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'IAUT300N08S5N014')

IAUT300N08S5N014	=	{																																	#*	IAUT300N08S5N014 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   83e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   156e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.33																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.5																						,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1625e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	           																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	40																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'IAUT300N08S5N012',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'IAUT300N08S5N012',1.2)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'IAUT300N08S5N012',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'IAUT300N08S5N012',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'IAUT300N08S5N012',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N08S5N012',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'IAUT300N08S5N012')

IAUT300N08S5N012	=	{																																	#*	IAUT300N08S5N012 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   86e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   177e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.33																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.4																						,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	2000e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	           																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	40																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVBLS1D1N08H',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVBLS1D1N08H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVBLS1D1N08H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVBLS1D1N08H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVBLS1D1N08H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D1N08H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVBLS1D1N08H')

NVBLS1D1N08H		=	{																																	#*	NVBLS1D1N08H parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   351                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   351                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   92e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   234e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.578																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.48																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1600e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'FDBL86361',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'FDBL86361',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'FDBL86361',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'FDBL86361',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'FDBL86361',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'FDBL86361',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'FDBL86361')

FDBL86361			=	{																																	#*	FDBL86361 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.25                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   136e-9                                 													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   269e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.563																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.35																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1925e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	           																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   80              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVBLS1D7N08H',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVBLS1D7N08H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVBLS1D7N08H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVBLS1D7N08H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVBLS1D7N08H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D7N08H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVBLS1D7N08H')

NVBLS1D7N08H		=	{																																	#*	FDBL86361 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   241                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   241                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   73e-9                                 													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   138e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.5																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.63																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1059e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss	           																		,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   43              																		, 	#? 	body diode reference current
							'Vs'							:	40																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMTS0D6N04CL',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMTS0D6N04CL',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMTS0D6N04CL',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMTS0D6N04CL',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMTS0D6N04CL',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMTS0D6N04CL',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMTS0D6N04CL')

NVMTS0D6N04CL		=	{																																	#*	NVMTS0D6N04CL parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   554.5                                 													,   #? 	transistor drain current
									'Tr'                	:   100e-9                                 													,   #? 	transistor rise time
									'Tf'                	:   100e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   99.3e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   228e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.6																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.002103,0.00875,0.025951,0.093755,0.642636]											,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000701,0.001817,0.009225,0.023893,0.0833]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.830418054,46.83713327,10.8124087,1.682365674,-41.85694941]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.163263676,1.272174175,15.0646712,336.385802,-1.581288262]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	6801e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	20																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMTS0D6N04C',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMTS0D6N04C',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMTS0D6N04C',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMTS0D6N04C',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMTS0D6N04C',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMTS0D6N04C',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMTS0D6N04C')

NVMTS0D6N04C		=	{																																	#*	NVMTS0D6N04C parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   533                                 													,   #? 	transistor drain current
									'Tr'                	:   100e-9                                 													,   #? 	transistor rise time
									'Tf'                	:   100e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   105e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   274e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.6																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.002103,0.00875,0.025951,0.093755,0.642636]											,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000701,0.001817,0.009225,0.023893,0.0833]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.830418054,46.83713327,10.8124087,1.682365674,-41.85694941]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.163263676,1.272174175,15.0646712,336.385802,-1.581288262]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	6801e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	20																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'IPT007N06N',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'IPT007N06N',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'IPT007N06N',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'IPT007N06N',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'IPT007N06N',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IPT007N06N',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'IPT007N06N')

IPT007N06N			=	{																																	#*	IPT007N06N parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   60                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   486                                 													,   #? 	transistor drain current
									'Tr'                	:   56e-9                                 													,   #? 	transistor rise time
									'Tf'                	:   98e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	60																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.0                                 													,   #? 	body diode forward voltage
									'If'                	:   323                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   87e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   144e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.149																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.40																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   5.38            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	4522e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   100              																		, 	#? 	body diode reference current
							'Vs'							:	30																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMFS3D6N10MCL',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMFS3D6N10MCL',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMFS3D6N10MCL',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMFS3D6N10MCL',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMFS3D6N10MCL',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMFS3D6N10MCL',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMFS3D6N10MCL')

NVMFS3D6N10MCL		=	{																																	#*	NVMFS3D6N10MCL parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   132.0                                 													,   #? 	transistor drain current
									'Tr'                	:   10e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   10e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   132.0                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   28.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   183e-9                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.566																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.015264,0.131852,0.687605,0.265279]													,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.001045,0.000791,0.009862,0.091526]													,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [15.21677265,3.550500602,7.988490088,1.96139986,2.312302281]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [1.734533318,1.345923536,18.43461362,242.1156251,0.159741955]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1808e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   24              																		, 	#? 	body diode reference current
							'Vs'							:	50																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQM70060EL',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQM70060EL',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQM70060EL',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQM70060EL',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQM70060EL',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQM70060EL',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQM70060EL')

SQM70060EL			=	{																																	#*	SQM70060EL parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   75.0                                 													,   #? 	transistor drain current
									'Tr'                	:   60e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   85e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.5                                 													,   #? 	body diode forward voltage
									'If'                	:   75.0                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   28.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   183e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.667																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.90																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	2600e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50             																		   	, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'TK55S10N1',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'TK55S10N1',1.182)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'TK55S10N1',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'TK55S10N1',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'TK55S10N1',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'TK55S10N1',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'TK55S10N1')

TK55S10N1			=	{																																	#*	TK55S10N1 parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   55.0                                 													,   #? 	transistor drain current
									'Tr'                	:   39e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   70e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   55.0                                 													,   #? 	body diode forward current
									'dIr'               	:   50e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   75.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   73.0e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[0,175]																					,	#?	temperature vector
                                        'Vfscale'			:	1.341																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.95																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1520e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   55              																		, 	#? 	body diode reference current
							'Vs'							:	80																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'TK33S10N1L',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'TK33S10N1L',1.182)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'TK33S10N1L',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'TK33S10N1L',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'TK33S10N1L',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'TK33S10N1L',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'TK33S10N1L')

TK33S10N1L			=	{																																	#*	TK33S10N1L parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   33.0                                 													,   #? 	transistor drain current
									'Tr'                	:   27e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   70e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   55.0                                 													,   #? 	body diode forward current
									'dIr'               	:   50e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   66.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   60.0e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[0,175]																					,	#?	temperature vector
                                        'Vfscale'			:	1.394																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.20																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1010e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   33              																		, 	#? 	body diode reference current
							'Vs'							:	80																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQR70090ELR',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQR70090ELR',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQR70090ELR',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQR70090ELR',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQR70090ELR',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQR70090ELR',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQR70090ELR')

SQR70090ELR			=	{																																	#*	SQR70090ELR parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   50.0                                 													,   #? 	transistor drain current
									'Tr'                	:   30e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   75e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.5                                 													,   #? 	body diode forward voltage
									'If'                	:   55.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0		                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.705																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.10																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1900e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   50              																		, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'XPH4R10ANB',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'XPH4R10ANB',1.21)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'XPH4R10ANB',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'XPH4R10ANB',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'XPH4R10ANB',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'XPH4R10ANB',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'XPH4R10ANB')

XPH4R10ANB			=	{																																	#*	XPH4R10ANB parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   70.0                                 													,   #? 	transistor drain current
									'Tr'                	:   73e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   111e-9                                      											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   70.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0		                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[0,175]																					,	#?	temperature vector
                                        'Vfscale'			:	1.382																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.88																					,	#?	junction-to-case thermal resistancee
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1940e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   70              																		, 	#? 	body diode reference current
							'Vs'							:	80																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQJ418EP',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQJ418EP',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQJ418EP',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQJ418EP',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQJ418EP',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJ418EP',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQJ418EP')

SQJ418EP			=	{																																	#*	SQJ418EP parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   30.0                                 													,   #? 	transistor drain current
									'Tr'                	:   50e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   50e-9 	                                     											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   30.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0		                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.411																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	2.20																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1200e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   20              																		, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQD70140EL',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQD70140EL',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQD70140EL',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQD70140EL',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQD70140EL',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQD70140EL',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQD70140EL')

SQD70140EL			=	{																																	#*	SQD70140EL parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   30.0                                 													,   #? 	transistor drain current
									'Tr'                	:   45e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   125e-9 	                                     											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.5                                 													,   #? 	body diode forward voltage
									'If'                	:   30.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0		                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.6																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	2.10																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1100e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   30              																		, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQJ402EP',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQJ402EP',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQJ402EP',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQJ402EP',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQJ402EP',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJ402EP',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQJ402EP')

SQJ402EP			=	{																																	#*	SQJ402EP parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   30.0                                 													,   #? 	transistor drain current
									'Tr'                	:   30e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   51e-9 	                                     											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   32.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0		                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.558																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.80																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	903e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   10              																		, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'DMTH10H010SPSQ',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'DMTH10H010SPSQ',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'DMTH10H010SPSQ',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'DMTH10H010SPSQ',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'DMTH10H010SPSQ',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'DMTH10H010SPSQ',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'DMTH10H010SPSQ')

DMTH10H010SPSQ		=	{																																	#*	DMTH10H010SPSQ parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   100.0                                 													,   #? 	transistor drain current
									'Tr'                	:   41.1e-9                                													,   #? 	transistor rise time
									'Tf'                	:   74.3e-9                                      											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   100.0                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   54.5e-9	                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   106.4e-9                                 												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.625																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.20																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	903e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   13              																		, 	#? 	body diode reference current
							'Vs'							:	50																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQD50N108M9L',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQD50N108M9L',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQD50N108M9L',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQD50N108M9L',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQD50N108M9L',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQD50N108M9L',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQD50N108M9L')

SQD50N108M9L		=	{																																	#*	SQD50N108M9L parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   49.0                                 													,   #? 	transistor drain current
									'Tr'                	:   36.0e-9                                													,   #? 	transistor rise time
									'Tf'                	:   325e-9                                      											,	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.5                                 													,   #? 	body diode forward voltage
									'If'                	:   49.0                                 													,   #? 	body diode forward current
									'dIr'               	:   0.0		                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0.0		                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0.0		                               													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0.0     	                            												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.875																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	1.10																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.22            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1810e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   49              																		, 	#? 	body diode reference current
							'Vs'							:	25																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQJQ186ER',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQJQ186ER',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQJQ186ER',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQJQ186ER',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQJQ186ER',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJQ186ER',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQJQ186ER')

SQJQ186ER_1			=	{																																	#*	SQJQ186ER parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   329.0                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.1                                 													,   #? 	body diode forward voltage
									'If'                	:   329.0                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   126e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   210e-9                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.375																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.25																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.803,2.119,0.791,0.225,0.962]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [2.441,0.281,12.082,140.360,40.968]             										,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	1655e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   40              																		, 	#? 	body diode reference current
							'Vs'							:	64																							#?	body diode reference voltage
						}
SQJQ186ER_2 			=	dp.copy.deepcopy(SQJQ186ER_1)
SQJQ186ER_2['Rth_ca']	=	[1.558,1.022,1.820,0.621]
SQJQ186ER_2['Cth_ca']	=	[5.024,0.342,28.706,114.962]
SQJQ186ER_2['nParallel']=	1

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'SQJQ144AER',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'SQJQ144AER',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'SQJQ144AER',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'SQJQ144AER',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'SQJQ144AER',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJQ144AER',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'SQJQ144AER')

SQJQ144AER			=	{																																	#*	SQJQ144AER parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   575                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.1                                 													,   #? 	body diode forward voltage
									'If'                	:   545                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   66.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   94e-9	                                  												 ,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.375																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.25																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [2.251,4.171,1.986,2.052,5.029]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [1.877,0.351,18.314,133.837,43.720]             										,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	2860e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   15              																		, 	#? 	body diode reference current
							'Vs'							:	32																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMJST0D7N04XM',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMJST0D7N04XM',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMJST0D7N04XM',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMJST0D7N04XM',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMJST0D7N04XM',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST0D7N04XM',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMJST0D7N04XM')

NVMJST0D7N04XM		=	{																																	#*	NVMJST0D7N04XM parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.164																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   553                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])                             	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   0.77                                 													,   #? 	body diode forward voltage
									'If'                	:   553                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   69.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   132e-9	                                  												,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.00																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00129071,0.0068152,0.0254695,0.0909854,0.241406]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[2.78E-05,7.68E-05,0.00083487,0.0023042,0.0214]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   0.0            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	2966e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   17.8              																		, 	#? 	body diode reference current
							'Vs'							:	32																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'NVMJST0D5N04XM',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'NVMJST0D5N04XM',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'NVMJST0D5N04XM',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'NVMJST0D5N04XM',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'NVMJST0D5N04XM',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST0D5N04XM',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'NVMJST0D5N04XM')

NVMJST0D5N04XM		=	{																																	#*	NVMJST0D5N04XM parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.174																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   906                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])                             	,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   0.77                                 													,   #? 	body diode forward voltage
									'If'                	:   906                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:  	93.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   282e-9	                                  												,	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.00																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00067201,0.00355133,0.0168122,0.0515319,0.141005]									,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[4.76E-05,0.00013147,0.0014285,0.0039428,0.0214]										,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   0.0            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	5136e-12																				,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	1																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   31.2              																		, 	#? 	body diode reference current
							'Vs'							:	32																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'PMT200EPE',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'PMT200EPE',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'PMT200EPE',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'PMT200EPE',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'PMT200EPE',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'PMT200EPE',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'PMT200EPE')

PMT200EPE			=	{																																	#*	PMT200EPE parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.5																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   2.4                                 													,   #? 	transistor drain current
									'Tr'                	:   14e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   44e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	70																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   1.8                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   1e-9	                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   1e-9	                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.5																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	15.0																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   15.0            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	47e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	5																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   1              																		   	, 	#? 	body diode reference current
							'Vs'							:	0																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss		=	paramProcess.Coss_data(switchesCossPath,'BUK9Y6R540H',1.0)
Rvec,Tvec			=	paramProcess.Rdson_data(switchesRdsonPath,'BUK9Y6R540H',1.0)
Nvec,Ivec 			=	paramProcess.Idson_data(switchesIdsonPath,'BUK9Y6R540H',1.0)
Ioff,catOFF,Eoff	=	paramProcess.Eoff_data(switchesEoffPath,'BUK9Y6R540H',1.0)
Ion,catON,Eon 		=	paramProcess.Eon_data(switchesEonPath,'BUK9Y6R540H',1.0)
Vfvec,Ifvec 		=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'BUK9Y6R540H',1.0)
Crss,Crss_avg 		=	paramProcess.Crss_data(switchesCrssPath, 'BUK9Y6R540H')

BUK9Y6R540H			=	{																																	#*	BUK9Y6R540H parameters
							'Config'						:	2																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rds_on'            	:   Rvec[-1][-1]																			,   #? 	transistor ON resistance
									'Rds_off'				:	200e3																					,	#?	transistor OFF resistance
									'Rvec'					:	Rvec																					,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.607																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used (Vgs=4.5,10)
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling
									'Lsig'					:	1e-9																					,	#?	transistor die source inductance
									'Ls'					:	0																						,	#?	device package source inductance
                                    'Ld'					:	0																						,	#?	device package drain inductance
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   70	                                 													,   #? 	transistor drain current
									'Tr'                	:   22e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   17e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	70																							#?	avalanche voltage
									}
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	200e3																					,	#?	body diode OFF resistance
									'Vf'                	:   1.0                                 													,   #? 	body diode forward voltage
									'If'                	:   70	                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   19e-9	                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   9.9e-9	                                  												, 	#? 	body diode reverse recovery charge
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.205																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	2.35																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.35            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	transistor/diode Coss parameters
									'C'						:	536e-12																					,	#? 	device parasitic output capacitance
									'R'						:	1																						,	#?	Coss resistance to emulate limited dV/dt
									'L'						:	100e-9																					,	#?	Coss inductance to reduce current slope
									'Vvec'					:	Coss[0]																					,	#? 	device Coss voltage vector
									'Cvec'					:	Coss[1]																					,	#?	device Coss capacity vector
									'Offset'				:	0																						,	#?	parasitic offset to Coss
                                    'Factor'				:	1.0																						,	#?	parasitic tolerance to Coss
									'Config'				:	5																							#? 	1->constant | 2->constant with damping R | 4->variable
						},
                        	'Crss'					:	{																									#!	transistor/diode Crss parameters
                                'Crss_avg'					:	Crss_avg																				,	#?	voltage-average Crss value
                                'Crss'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Eoff'					:	{																									#!	transistor turn-OFF energy losses
									'Ivec'					:	Ioff																					,	#?	turn-OFF energy current vector
									'Rgvec'					:	[0,100]																					,	#?	OFF path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-OFF voltage vector
                                    'Evec'					:	Eoff																					,	#?	turn-OFF energy vectors
                                    'CAT'					:	catOFF																					,	#?	octave Eoff energy syntax
									'Rg'					:	0																							#?	used OFF path gate resistance
						},
							'Eon'					:	{																									#!	transistor turn-ON energy losses
									'Ivec'					:	Ion																						,	#?	turn-ON energy current vector
									'Rgvec'					:	[0,100]																					,	#?	ON path gate resistances vector
                                    'Vvec'					:	[0,500]																					,	#?	turn-ON voltage vector
                                    'Evec'					:	Eon																						,	#?	turn-ON energy vectors
                                    'CAT'					:	catON																					,	#?	octave Eon energy syntax
									'Rg'					:	0																							#?	used ON path gate resistance
						},
							'Tau_deg'						:	0																						,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
							'Qoss'                			:  	Qoss           																			,   #? 	device output charge
							'Eoss'                			:  	Eoss		           																	,   #? 	device output energy
							'Is'                  			:   20              																		, 	#? 	body diode reference current
							'Vs'							:	20																							#?	body diode reference voltage
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!	assemble all switches to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

LVswitchVars 			= 	{
								'IAUT300N10S5N015' 		: 	IAUT300N10S5N015 		,
								'NVBLS1D5N10MC' 		: 	NVBLS1D5N10MC 			,
								'NVBLS1D7N10MC' 		: 	NVBLS1D7N10MC 			,
								'IAUT300N08S5N014' 		: 	IAUT300N08S5N014 		,
								'IAUT300N08S5N012' 		: 	IAUT300N08S5N012 		,
								'NVBLS1D1N08H' 			: 	NVBLS1D1N08H 			,
								'FDBL86361' 			: 	FDBL86361 				,
								'NVBLS1D7N08H'			:	NVBLS1D7N08H			,
                                'SQJQ186ER_1'			:	SQJQ186ER_1				,
                                'NVBYST0D6N08X'			:	NVBYST0D6N08X
							}

HVswitchVars 			= 	{
								'GS66508T'				:	GS66508T				,
								'AIMDQ75R063M1H' 		: 	AIMDQ75R063M1H			,
                                'AIMDQ75R060M1H'		:	AIMDQ75R060M1H			,
                                'AIMDQ75R042M1H'		:	AIMDQ75R042M1H			,
                                'SCT055HU65G3AG'		:	SCT055HU65G3AG			,
								'SCTH35N65G2V'			:	SCTH35N65G2V
							}

shortCircuitSwitchVars	= 	{
								'NVMTS0D6N04CL' 		: 	NVMTS0D6N04CL 			,
                                'NVMTS0D6N04C'			:	NVMTS0D6N04C			,
                                'IPT007N06N'			:	IPT007N06N				,
                                'SQJQ144AER'			:	SQJQ144AER				,
                                'NVMJST0D7N04XM'		:	NVMJST0D7N04XM			,
                                'NVMJST0D5N04XM'		:	NVMJST0D5N04XM
							}

FreewheelingSwitchVars	=	{
								'NVMFS3D6N10MCL'		:	NVMFS3D6N10MCL			,
								'SQM70060EL'			:	SQM70060EL				,
								'TK55S10N1'				:	TK55S10N1				,
								'TK33S10N1L'			:	TK33S10N1L				,
								'SQR70090ELR'			:	SQR70090ELR				,
								'XPH4R10ANB'			:	XPH4R10ANB				,
								'SQJ418EP'				:	SQJ418EP				,
								'SQD70140EL'			:	SQD70140EL				,
								'SQJ402EP'				:	SQJ402EP				,
								'DMTH10H010SPSQ'		:	DMTH10H010SPSQ			,
								'SQD50N108M9L'			:	SQD50N108M9L			,
                                'SQJQ186ER_2'			:	SQJQ186ER_2				,
                                'NVMJST3D3N08X'			:	NVMJST3D3N08X			,
                                'NVMJST004N08X'			:	NVMJST004N08X
							}

AllSwitches 			=	{
								'IAUT300N10S5N015' 		: 	IAUT300N10S5N015 		,
								'NVBLS1D5N10MC' 		: 	NVBLS1D5N10MC 			,
								'NVBLS1D7N10MC' 		: 	NVBLS1D7N10MC 			,
								'IAUT300N08S5N014' 		: 	IAUT300N08S5N014 		,
								'IAUT300N08S5N012' 		: 	IAUT300N08S5N012 		,
								'NVBLS1D1N08H' 			: 	NVBLS1D1N08H 			,
								'FDBL86361' 			: 	FDBL86361 				,
								'NVBLS1D7N08H'			:	NVBLS1D7N08H			,
								'SQJQ186ER_1'			:	SQJQ186ER_1				,
								'SQJQ186ER_2'			:	SQJQ186ER_2				,
                                'GS66508T'				:	GS66508T				,
								'AIMDQ75R063M1H' 		: 	AIMDQ75R063M1H			,
                                'AIMDQ75R060M1H'		:	AIMDQ75R060M1H			,
                                'AIMDQ75R042M1H'		:	AIMDQ75R042M1H			,
                                'SCT055HU65G3AG'		:	SCT055HU65G3AG			,
								'SCTH35N65G2V'			:	SCTH35N65G2V			,
                                'NVMTS0D6N04CL' 		: 	NVMTS0D6N04CL 			,
                                'NVMTS0D6N04C'			:	NVMTS0D6N04C			,
                                'IPT007N06N'			:	IPT007N06N				,
                                'SQJQ144AER'			:	SQJQ144AER				,
                                'NVMFS3D6N10MCL'		:	NVMFS3D6N10MCL			,
								'SQM70060EL'			:	SQM70060EL				,
								'TK55S10N1'				:	TK55S10N1				,
								'TK33S10N1L'			:	TK33S10N1L				,
								'SQR70090ELR'			:	SQR70090ELR				,
								'XPH4R10ANB'			:	XPH4R10ANB				,
								'SQJ418EP'				:	SQJ418EP				,
								'SQD70140EL'			:	SQD70140EL				,
								'SQJ402EP'				:	SQJ402EP				,
								'DMTH10H010SPSQ'		:	DMTH10H010SPSQ			,
								'SQD50N108M9L'			:	SQD50N108M9L			,
                                'PMT200EPE'				:	PMT200EPE				,
                                'BUK9Y6R540H'			:	BUK9Y6R540H				,
                                'NVMJST3D3N08X'			:	NVMJST3D3N08X			,
                                'NVBYST0D6N08X'			:	NVBYST0D6N08X			,
                                'NVMJST004N08X'			:	NVMJST004N08X			,
                                'NVMJST0D7N04XM'		:	NVMJST0D7N04XM			,
                                'NVMJST0D5N04XM'		:	NVMJST0D5N04XM
							}
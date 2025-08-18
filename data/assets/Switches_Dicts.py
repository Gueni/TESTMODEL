
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
paramProcess			=	dp.PM.ParamProcess()

switchesTransferPath	=	'Script/Data/Switches_Forward_Transfer/'
switchesCossPath		=	'Script/Data/Switches_Coss/'
switchesCrssPath		=	'Script/Data/Switches_Crss/'
switchesCissPath		=	'Script/Data/Switches_Ciss/'
switchesRdsonPath		= 	'Script/Data/Switches_Rdson/'
switchesIdsonPath		= 	'Script/Data/Switches_Rdson_Ids/'
switchesEoffPath    	=   'Script/Data/Switches_Eoff/'
switchesEonPath    		=   'Script/Data/Switches_Eon/'
bodyDiodeVIPath 		=	'Script/Data/Diodes_VI/'

#! 	switches models parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------GaN Switches
Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'GS66508T','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'GS66508T','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'GS66508T','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'GS66508T','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'GS66508T','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'GS66508T','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'GS66508T','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'GS66508T')
Vds_vec,Ids_vec 					=	paramProcess.Forward_Transfer_data(switchesTransferPath,'NVMTS0D6N04C')

GS66508T			=	{																																	#*	GS66508T parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real with limited di/dt | 2->ideal switch | 3->behavioral model
									'Thermal'           	:   'GaN_Systems/GS66508_v3'                                  								,   #? 	selected transistor
									'Custom'            	:   ['Rgon','1','Rgoff','1','vgsoff','1','g','m:g']                 						,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	1																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   30	                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650 																					,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   2.6                                 													,   #? 	body diode forward voltage
									'If'                	:   30	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0	                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   0			                              												,	#? 	body diode reverse recovery charge
									'Is'                  	:   0              																		   	,	#? 	body diode reference current
									'Vs'					:	0																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.529																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.015,0.23,0.24,0.015]																	,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[8e-5,7.4e-4,6.5e-3,2e-3]																,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   3.50            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	160e-12						 															,	#?	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
							'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'AIMDQ75R060M1H','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'AIMDQ75R060M1H','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'AIMDQ75R060M1H','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'AIMDQ75R060M1H','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'AIMDQ75R060M1H','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'AIMDQ75R060M1H','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'AIMDQ75R060M1H','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'AIMDQ75R060M1H')
Vds_vec,Ids_vec 					=	paramProcess.Forward_Transfer_data(switchesTransferPath,'AIMDQ75R060M1H')

AIMDQ75R060M1H		=	{																																	#*	AIMDQ75R060M1H parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rg'					:	6.752																					,	#?	internal gate resistance
									'Lg'					:	9.52e-9*0																				,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	2																						,	#?	choose which NI vector to be used (Vgs=15,18,20)
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	10																						,	#?	gate ON path resistance
									'Rgoff'					:	10																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	47.2e-3*0																				,	#?	kelvin source pin resistance
									'Lsrc'					:	5.57e-9*0																				,	#?	kelvin source pin inductance
									'Ls'					:	4.62e-9*0																				,	#?	package source inductance
                                    'Ld'					:	2.19e-9*0																				,	#?	package drain inductance
									'Rs'					:	993e-6*0																				,	#?	package source resistance
									'Rd'					:	46.3e-6*0																				,	#?	package drain inductance
									'Ksrc'					:	1																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   750                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   32	                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	750 																					,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	list(dp.np.arange(0.0,21.0,0.35))														,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   3.9                                 													,   #? 	body diode forward voltage
									'If'                	:   32	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   16e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   57e-9			                              											,	#? 	body diode reverse recovery charge
									'Is'                  	:   11.1              																		, 	#? 	body diode reference current
									'Vs'					:	500																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.359																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	18																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	0.55																					,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.90																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [1.0682,1.2039,0.7389,0.427] 															,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [12.8939,1.6758,0.0755,169.4661]            											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	106e-12							 														,	#?	device parasitic output capacitance
								'R'							:	0																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	0																						,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0*25.0e-12																				,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#?	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'AIMDQ75R040M1H','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'AIMDQ75R040M1H','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'AIMDQ75R040M1H','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'AIMDQ75R040M1H','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'AIMDQ75R040M1H','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'AIMDQ75R040M1H','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'AIMDQ75R040M1H','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'AIMDQ75R040M1H')

AIMDQ75R040M1H		=	{																																	#*	AIMDQ75R040M1H parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   'Infineon/CoolSiC/AIMDQ75R040M1H'                                  						,   #? 	selected transistor
									'Custom'            	:   ['TCR','1']                 															,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   750                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   42.2                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	750 																					,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   4.0                                 													,   #? 	body diode forward voltage
									'If'                	:   42	                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   0	                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                      													,   #? 	body diode reverse recovery current
									'Qrr'               	:   144e-9			                              											,	#? 	body diode reverse recovery charge
									'Is'                  	:   16.6              																		, 	#? 	body diode reference current
									'Vs'					:	500																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.359																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.82																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [1.399,1.017,0.638,0.453,0.564]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [2.028,16.857,0.757,210.682,0.149]            											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	332.3e-12						 														,	#?	device parasitic output capacitance
								'R'							:	0																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	0																						,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'SCTH35N65G2V','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'SCTH35N65G2V','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'SCTH35N65G2V','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'SCTH35N65G2V','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'SCTH35N65G2V','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'SCTH35N65G2V','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'SCTH35N65G2V','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SCTH35N65G2V')

SCTH35N65G2V		=	{																																	#*	SCTH35N65G2V parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	1																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   45                                 														,   #? 	transistor drain current
									'Tr'                	:   30e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   44e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650 																					,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   3.3                                 													,   #? 	body diode forward voltage
									'If'                	:   45                                 														,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   18e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   7                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   85e-9	                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   20	              																		, 	#? 	body diode reference current
									'Vs'					:	400																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.0																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.72																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   4.80            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	125e-12						 															,	#?	device parasitic output capacitance
								'R'							:	0																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	0																						,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'SCT055HU65G3AG','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'SCT055HU65G3AG','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'SCT055HU65G3AG','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'SCT055HU65G3AG','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'SCT055HU65G3AG','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'SCT055HU65G3AG','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'SCT055HU65G3AG','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SCT055HU65G3AG')

SCT055HU65G3AG		=	{																																	#*	SCT055HU65G3AG parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []                 																		,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	1																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   650                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   40                                 														,   #? 	transistor drain current
									'Tr'                	:   27e-9                                													,   #? 	transistor rise time
									'Tf'                	:   19.4e-9                                    												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	650																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   3.0                                 													,   #? 	body diode forward voltage
									'If'                	:   40                                 														,   #? 	body diode forward current
									'dIr'               	:   1000e6                                 													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   51e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   6.3                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   71e-9	                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   15	              																		, 	#? 	body diode reference current
									'Vs'					:	400																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.0																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.85																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   4.80            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	139.08e-12					 															,	#?	device parasitic output capacitance
								'R'							:	0																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	0																						,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Si Switches

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'IAUT300N10S5N015','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'IAUT300N10S5N015','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'IAUT300N10S5N015','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'IAUT300N10S5N015','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'IAUT300N10S5N015','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'IAUT300N10S5N015','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'IAUT300N10S5N015','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N10S5N015')
Vds_vec,Ids_vec 					=	paramProcess.Forward_Transfer_data(switchesTransferPath,'IAUT300N10S5N015')

IAUT300N10S5N015	=	{																																	#*	IAUT300N10S5N015 parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1.5																						,	#?	internal gate resistance
									'Lg'					:	3e-9*0																					,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	3.9																						,	#?	gate ON path resistance
									'Rgoff'					:	1																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	208e-6*0																				,	#?	kelvin source pin resistance
									'Lsrc'					:	1.5e-9*0																				,	#?	kelvin source pin inductance
									'Ls'					:	1.5e-9*0																				,	#?	package source inductance
                                    'Ld'					:	1e-9*0																					,	#?	package drain inductance
									'Rs'					:	208e-6*0																				,	#?	package source resistance
									'Rd'					:	20e-6*0																					,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   55e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   118e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	list(dp.np.arange(0.0,12.0+0.2,0.2))													,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.01																					,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   90e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   220e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	50																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.444																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	2.5																						,	#?	sourcing output resistance
									'Roff'					:	1.5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	50e-9																					,	#?	input-to-output total deadtime
									'Trise'					:	9e-9																					,	#?	output rising time
									'Tfall'					:	7e-9																					,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[2.202e-4,3e-2,7.642e-2,3.729e-5,2.401e-1,5.318e-2]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[4.541e-2,3.333e-3,1.309e-2,2.682e2,4.164e-1,1.880e1]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.8]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1920e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	0.98																					,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	1																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	2.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	380e-12																					,	#?	tuning offset for turn ON
								'Offset_OFF'				:	700e-12																					,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.05																					,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	350e-12																				,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	0.97																					,	#?	tuning factor for turn ON
								'Factor_OFF'				:	0.95																						#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMJST3D3N08X','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMJST3D3N08X','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMJST3D3N08X','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMJST3D3N08X','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMJST3D3N08X','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMJST3D3N08X','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMJST3D3N08X','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST3D3N08X')

NVMJST3D3N08X		=	{																																	#*	NVMJST3D3N08X parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.183																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   194                                 													,   #? 	transistor drain current
									'Tr'                	:   31e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   39e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   194                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   22.6e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   151e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   31              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.445																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.003073492,0.0145417,0.0365529,0.142744,0.378208]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000035866,0.00009899,0.00071709,0.0019792,0.0214]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	798e-12																					,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVBYST0D6N08X','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVBYST0D6N08X','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVBYST0D6N08X','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVBYST0D6N08X','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVBYST0D6N08X','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVBYST0D6N08X','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVBYST0D6N08X','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBYST0D6N08X')

NVBYST0D6N08X		=	{																																	#*	NVBYST0D6N08X parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.167																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   856                                 													,   #? 	transistor drain current
									'Tr'                	:   77e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   114e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   856                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   42e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   513e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.558																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.000898284,0.00345812,0.0102355,0.0174793,0.141617]									,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.00034051,0.00093982,0.0040849,0.011274,0.0214]										,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	4665e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMJST004N08X','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMJST004N08X','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMJST004N08X','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMJST004N08X','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMJST004N08X','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMJST004N08X','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMJST004N08X','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST004N08X')

NVMJST004N08X		=	{																																	#*	NVMJST004N08X parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.156																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                               	 													,   #? 	transistor blocking voltage
									'Id'                	:   409                                 													,   #? 	transistor drain current
									'Tr'                	:   29e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   37e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   409                                 													,   #? 	body diode forward current
									'dIr'               	:   1e9		                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   21e-9                                													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   138e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   27              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.463																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00352257,0.016627,0.0383147,0.160293,0.427985]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000031294,0.000086371,0.00062568,0.0017269,0.0214]									,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0]            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0]             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	699e-12																					,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVBLS1D5N10MC','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVBLS1D5N10MC','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVBLS1D5N10MC','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVBLS1D5N10MC','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVBLS1D5N10MC','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVBLS1D5N10MC','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVBLS1D5N10MC','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D5N10MC')

NVBLS1D5N10MC		=	{																																	#*	NVBLS1D5N10MC parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   110e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   143e-9                                  											,	#? 	body diode reverse recovery charge
									'Is'                  	:   71              																		, 	#? 	body diode reference current
									'Vs'					:	50																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.625																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.45																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	5100e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVBLS1D7N10MC','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVBLS1D7N10MC','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVBLS1D7N10MC','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVBLS1D7N10MC','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVBLS1D7N10MC','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVBLS1D7N10MC','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVBLS1D7N10MC','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D7N10MC')

NVBLS1D7N10MC		=	{																																	#*	NVBLS1D7N10MC parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                   												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   110e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   143e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   62              																		, 	#? 	body diode reference current
									'Vs'					:	50																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.585																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.49																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	5100e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'IAUT300N08S5N014','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'IAUT300N08S5N014','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'IAUT300N08S5N014','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'IAUT300N08S5N014','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'IAUT300N08S5N014','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'IAUT300N08S5N014','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'IAUT300N08S5N014','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N08S5N014')

IAUT300N08S5N014	=	{																																	#*	IAUT300N08S5N014 parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   83e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   156e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	40																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.33																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.5																						,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1625e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'IAUT300N08S5N012','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'IAUT300N08S5N012','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'IAUT300N08S5N012','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'IAUT300N08S5N012','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'IAUT300N08S5N012','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'IAUT300N08S5N012','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'IAUT300N08S5N012','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'IAUT300N08S5N012')

IAUT300N08S5N012	=	{																																	#*	IAUT300N08S5N012 parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   86e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   177e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	40																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.33																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.4																						,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	2000e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVBLS1D1N08H','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVBLS1D1N08H','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVBLS1D1N08H','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVBLS1D1N08H','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVBLS1D1N08H','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVBLS1D1N08H','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVBLS1D1N08H','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D1N08H')

NVBLS1D1N08H		=	{																																	#*	NVBLS1D1N08H parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   351                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   351                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   92e-9                                  													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   234e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.578																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.48																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1600e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'FDBL86361','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'FDBL86361','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'FDBL86361','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'FDBL86361','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'FDBL86361','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'FDBL86361','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'FDBL86361','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'FDBL86361')

FDBL86361			=	{																																	#*	FDBL86361 parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   300                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.25                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   136e-9                                 													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   269e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   80              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.563																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.35																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1925e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVBLS1D7N08H','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVBLS1D7N08H','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVBLS1D7N08H','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVBLS1D7N08H','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVBLS1D7N08H','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVBLS1D7N08H','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVBLS1D7N08H','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVBLS1D7N08H')

NVBLS1D7N08H		=	{																																	#*	FDBL86361 parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   241                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   241                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   73e-9                                 													,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   138e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   43              																		, 	#? 	body diode reference current
									'Vs'					:	40																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.5																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.63																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.292,0.258,0.856,0.228,0.3]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.788,0.205,15.91,3.716,0.015]             											,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1059e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMTS0D6N04CL','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMTS0D6N04CL','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMTS0D6N04CL','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMTS0D6N04CL','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMTS0D6N04CL','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMTS0D6N04CL','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMTS0D6N04CL','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMTS0D6N04CL')
Vds_vec,Ids_vec 					=	paramProcess.Forward_Transfer_data(switchesTransferPath,'NVMTS0D6N04C')

NVMTS0D6N04CL		=	{																																	#*	NVMTS0D6N04CL parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1.077																					,	#?	internal gate resistance
									'Lg'					:	6.23e-9*0																				,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	1.95																					,	#?	gate ON path resistance
									'Rgoff'					:	1.95																					,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	54.37e-6*0																				,	#?	kelvin source pin resistance
									'Lsrc'					:	0.99e-9*0																				,	#?	kelvin source pin inductance
									'Ls'					:	0.99e-9*0																				,	#?	package source inductance
                                    'Ld'					:	0.3377e-9*0																				,	#?	package drain inductance
									'Rs'					:	54.37e-6*0																				,	#?	package source resistance
									'Rd'					:	149.74e-9*0																				,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   533                                 													,   #? 	transistor drain current
									'Tr'                	:   100e-9                                 													,   #? 	transistor rise time
									'Tf'                	:   100e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	list(dp.np.arange(0.0,12.0+0.2,0.2))													,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   105e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   274e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	20																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.6																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	10																						,	#?	sourcing output resistance
									'Roff'					:	12																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	40e-6																					,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.002103,0.00875,0.025951,0.093755,0.642636]											,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000701,0.001817,0.009225,0.023893,0.0833]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.830418054,46.83713327,10.8124087,1.682365674,-41.85694941]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.163263676,1.272174175,15.0646712,336.385802,-1.581288262]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	6801e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMTS0D6N04C','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMTS0D6N04C','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMTS0D6N04C','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMTS0D6N04C','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMTS0D6N04C','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMTS0D6N04C','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMTS0D6N04C','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMTS0D6N04C')
Vds_vec,Ids_vec 					=	paramProcess.Forward_Transfer_data(switchesTransferPath,'NVMTS0D6N04C')

NVMTS0D6N04C		=	{																																	#*	NVMTS0D6N04C parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	0.6																						,	#?	internal gate resistance
									'Lg'					:	6.2322e-9*0																				,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	1.95																					,	#?	gate ON path resistance
									'Rgoff'					:	1.95																					,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0.9922e-9*0																				,	#?	package source inductance
                                    'Ld'					:	0.3377e-9*0																				,	#?	package drain inductance
									'Rs'					:	54.3723e-6*0																			,	#?	package source resistance
									'Rd'					:	149.735e-9*0																			,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   533                                 													,   #? 	transistor drain current
									'Tr'                	:   100e-9                                 													,   #? 	transistor rise time
									'Tf'                	:   100e-9                                     												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	list(dp.np.arange(0.0,12.0+0.2,0.2))													,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   300                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   105e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   274e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   50              																		, 	#? 	body diode reference current
									'Vs'					:	20																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.6																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	10																						,	#?	sourcing output resistance
									'Roff'					:	12																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	0																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	0																						,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	40e-6																					,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.002103,0.00875,0.025951,0.093755,0.642636]											,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.000701,0.001817,0.009225,0.023893,0.0833]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.830418054,46.83713327,10.8124087,1.682365674,-41.85694941]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [0.163263676,1.272174175,15.0646712,336.385802,-1.581288262]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	6801e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMFS3D6N10MCL','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMFS3D6N10MCL','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMFS3D6N10MCL','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMFS3D6N10MCL','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMFS3D6N10MCL','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMFS3D6N10MCL','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMFS3D6N10MCL','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMFS3D6N10MCL')

NVMFS3D6N10MCL		=	{																																	#*	NVMFS3D6N10MCL parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   100                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   132.0                                 													,   #? 	transistor drain current
									'Tr'                	:   10e-9                                   												,   #? 	transistor rise time
									'Tf'                	:   10e-9                                       											, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	100																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.3                                 													,   #? 	body diode forward voltage
									'If'                	:   132.0                                 													,   #? 	body diode forward current
									'dIr'               	:   1000e6                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   28.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   183e-9                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   24              																		, 	#? 	body diode reference current
									'Vs'					:	50																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.566																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	2																						,	#?	sourcing output resistance
									'Roff'					:	2																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	50e-9																					,	#?	input-to-output total deadtime
									'Trise'					:	9e-9																					,	#?	output rising time
									'Tfall'					:	7e-9																					,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.015264,0.131852,0.687605,0.265279]													,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[0.001045,0.000791,0.009862,0.091526]													,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [15.21677265,3.550500602,7.988490088,1.96139986,2.312302281]            				,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [1.734533318,1.345923536,18.43461362,242.1156251,0.159741955]             				,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1808e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'SQJQ186ER','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'SQJQ186ER','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'SQJQ186ER','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'SQJQ186ER','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'SQJQ186ER','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'SQJQ186ER','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'SQJQ186ER','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJQ186ER')

SQJQ186ER_1			=	{																																	#*	SQJQ186ER parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   80                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   329.0                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	80																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.1                                 													,   #? 	body diode forward voltage
									'If'                	:   329.0                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6                                  													,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   126e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   210e-9                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   40              																		, 	#? 	body diode reference current
									'Vs'					:	64																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.375																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.25																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [0.803,2.119,0.791,0.225,0.962]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [2.441,0.281,12.082,140.360,40.968]             										,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	1655e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}
SQJQ186ER_2 			=	dp.copy.deepcopy(SQJQ186ER_1)
SQJQ186ER_2['Rth_ca']	=	[1.558,1.022,1.820,0.621]
SQJQ186ER_2['Cth_ca']	=	[5.024,0.342,28.706,114.962]
SQJQ186ER_2['nParallel']=	1

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'SQJQ144AER','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'SQJQ144AER','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'SQJQ144AER','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'SQJQ144AER','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'SQJQ144AER','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'SQJQ144AER','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'SQJQ144AER','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'SQJQ144AER')

SQJQ144AER			=	{																																	#*	SQJQ144AER parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.0																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   575                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-5][-1] - Vfvec[-1][-1])/(Ifvec[-5] - Ifvec[-1])                              	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.1                                 													,   #? 	body diode forward voltage
									'If'                	:   545                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   66.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   94e-9	                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   15              																		, 	#? 	body diode reference current
									'Vs'					:	32																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.375																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	0.25																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   [2.251,4.171,1.986,2.052,5.029]            												,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   [1.877,0.351,18.314,133.837,43.720]             										,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	2860e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMJST0D7N04XM','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMJST0D7N04XM','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMJST0D7N04XM','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMJST0D7N04XM','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMJST0D7N04XM','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMJST0D7N04XM','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMJST0D7N04XM','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST0D7N04XM')

NVMJST0D7N04XM		=	{																																	#*	NVMJST0D7N04XM parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.164																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   553                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])                             	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   0.77                                 													,   #? 	body diode forward voltage
									'If'                	:   553                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   69.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   132e-9	                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   17.8              																		, 	#? 	body diode reference current
									'Vs'					:	32																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.00																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00129071,0.0068152,0.0254695,0.0909854,0.241406]										,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[2.78E-05,7.68E-05,0.00083487,0.0023042,0.0214]											,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   0.0            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	2966e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'NVMJST0D5N04XM','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'NVMJST0D5N04XM','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'NVMJST0D5N04XM','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'NVMJST0D5N04XM','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'NVMJST0D5N04XM','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'NVMJST0D5N04XM','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'NVMJST0D5N04XM','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'NVMJST0D5N04XM')

NVMJST0D5N04XM		=	{																																	#*	NVMJST0D5N04XM parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.174																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   906                                 													,   #? 	transistor drain current
									'Tr'                	:   0                                   													,   #? 	transistor rise time
									'Tf'                	:   0                                       												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	40																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])                             	,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   0.77                                 													,   #? 	body diode forward voltage
									'If'                	:   906                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:  	93.0e-9                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   282e-9	                                  												,	#? 	body diode reverse recovery charge
									'Is'                  	:   31.2              																		, 	#? 	body diode reference current
									'Vs'					:	32																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[-55,25,175]																			,	#?	temperature vector
                                        'Vfscale'			:	1.00																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	2                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	[0.00067201,0.00355133,0.0168122,0.0515319,0.141005]									,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	[4.76E-05,0.00013147,0.0014285,0.0039428,0.0214]										,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   0.0            																			,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	5136e-12																				,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'PMT200EPE','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'PMT200EPE','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'PMT200EPE','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'PMT200EPE','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'PMT200EPE','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'PMT200EPE','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'PMT200EPE','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'PMT200EPE')

PMT200EPE			=	{																																	#*	PMT200EPE parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.5																						,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   2.4                                 													,   #? 	transistor drain current
									'Tr'                	:   14e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   44e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	70																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.2                                 													,   #? 	body diode forward voltage
									'If'                	:   1.8                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   1e-9	                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   1e-9	                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   1              																		   	, 	#? 	body diode reference current
									'Vs'					:	0																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,150]																				,	#?	temperature vector
                                        'Vfscale'			:	1.5																							#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	15.0																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   15.0            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	47e-12																					,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Coss,Qoss,Eoss,Coss_tr,Coss_er		=	paramProcess.MOSFETcaps(switchesCossPath,'BUK9Y6R540H','_Coss')
Crss,Qrss,Erss,Crss_tr,Crss_er 		=	paramProcess.MOSFETcaps(switchesCrssPath,'BUK9Y6R540H','_Crss')
Ciss,Qiss,Eiss,Ciss_tr,Ciss_er 		=	paramProcess.MOSFETcaps(switchesCissPath,'BUK9Y6R540H','_Ciss')
Rvec,Tvec							=	paramProcess.MOSFETrdson(switchesRdsonPath,'BUK9Y6R540H','_Rdson')
Nvec,Ivec 							=	paramProcess.MOSFETrdson(switchesIdsonPath,'BUK9Y6R540H','_Rdson')
Ioff,catOFF,Eoff					=	paramProcess.MOSFETenergies(switchesEoffPath,'BUK9Y6R540H','_Eoff')
Ion,catON,Eon 						=	paramProcess.MOSFETenergies(switchesEonPath,'BUK9Y6R540H','_Eon')
Vfvec,Ifvec 						=	paramProcess.DiodeVI_data(bodyDiodeVIPath,'BUK9Y6R540H')

BUK9Y6R540H			=	{																																	#*	BUK9Y6R540H parameters
							'Config'						:	1																						,	#!	1->electric integrated | 2->electric separate | 3->thermal integrated | 4->thermal separate
							'Transistor'  			: 	{																									#!	transistors parameters
									'Config'				:	2																						,	#?	1->real model | 2->ideal model | 3->behavioral model
									'Thermal'           	:   ''                                  													,   #? 	selected transistor
									'Custom'            	:   []						               													,   #? 	transistor provided custom variables
									'Rg'					:	1																						,	#?	internal gate resistance
									'Lg'					:	0																						,	#?	gate pin inductance
									'Rds_on'            	:   Rvec[-1][-1]*1e-3																		,   #? 	transistor ON resistance
									'Rds_off'				:	'inf'																					,	#?	transistor OFF resistance
									'Rvec'					:	(dp.np.array(Rvec)*1e-3).tolist()														,	#?	absolute Rdson vector corresponding to junction temperature
									'Tvec'					:	Tvec 																					,	#?	junction temperature vector for Rdson
									'RTconfig'				:	1																						,	#?	choose which RT vector to be used, 1->typ | 2->max
									'RdsonScale'			:	1.607																					,	#?	Rdson scaling to account for min, typ and max deviations
									'Nvec'					:	Nvec 																					,	#?	normalized Rdson vector corresponding to current
									'Ivec'					:	Ivec																					,	#?	current vector for normalized Rdson
									'NIconfig'				:	1																						,	#?	choose which NI vector to be used (Vgs=4.5,10)
									'IdsonScale'			:	1.0																						,	#?	Idson resistance scaling to account for min, typ and max deviations
									'Rgon'					:	5																						,	#?	gate ON path resistance
									'Rgoff'					:	5																						,	#?	gate OFF path resistance
									'Lgon'					:	0																						,	#?	gate ON path inductance
									'Lgoff'					:	0																						,	#?	gate OFF path inductance
									'Rsrc'					:	0																						,	#?	kelvin source pin resistance
									'Lsrc'					:	0																						,	#?	kelvin source pin inductance
									'Ls'					:	0																						,	#?	package source inductance
                                    'Ld'					:	0																						,	#?	package drain inductance
									'Rs'					:	0																						,	#?	package source resistance
									'Rd'					:	0																						,	#?	package drain inductance
									'Ksrc'					:	0																						,	#?	kelvin source option, 0->no kelvin | 1->kelvin
									'Vblock'            	:   40                                	 													,   #? 	transistor blocking voltage
									'Id'                	:   70	                                 													,   #? 	transistor drain current
									'Tr'                	:   22e-9                                  													,   #? 	transistor rise time
									'Tf'                	:   17e-9                                      												, 	#? 	transistor fall time
									'Avalanche'		:	{																									#!	transistor avalanche parameters
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Voltage'			:	70																						,	#?	avalanche voltage
										'Resistance'		:	1e-3																						#?	avalanche resistance to break voltage state-dependency
									},
									'Transfer'		:	{																									#!	transistor forward transfer parameters
										'Vds'				:	Vds_vec																					,	#?	drain-source voltage vector
										'Vgs'				:	[0,20]																					,	#?	gate-source voltage vector
										'Ids'				:	Ids_vec																					,	#?	drain current vector
										'Factor_ON'			:	1.0																						,	#?	scaling factor for Ids at turn ON
										'Factor_OFF'		:	1.0																						,	#?	scaling factor for Ids at turn OFF
										'Factor_Vgs_ON'		:	1.0																						,	#?	scaling factor for Vgs at turn ON
										'Factor_Vgs_OFF'	:	1.0																						,	#?	scaling factor for Vgs at turn OFF
										'Vcoss'				:	0																						,	#?	initial voltage of the Coss
									},
						},
							'BodyDiode'  			:	{																									#!	body diodes paramteters
									'Config'				:	4																						,	#?	1->non-ideal RR | 2->non-ideal | 3->ideal RR | 4->ideal
									'Thermal'           	:   ''                                  													,   #? 	separate body diode
									'Custom'            	:   []					                 													,   #? 	body diode provided custrom variables
									'Rd_on'             	:   (Vfvec[-10][-1] - Vfvec[-1][-1])/(Ifvec[-10] - Ifvec[-1])								,  	#? 	body diode ON resistance
									'Rd_off'				:	'inf'																					,	#?	body diode OFF resistance
									'Vf'                	:   1.0                                 													,   #? 	body diode forward voltage
									'If'                	:   70	                                 													,   #? 	body diode forward current
									'dIr'               	:   100e6	                                  												,   #? 	body diode current slope
									'Lrr'					:	1e-9																					,	#?	body diode reverse recovery inductance
									'Trr'               	:   19e-9	                                  												,   #? 	body diode reverse recovery time
									'Irr'               	:   0                                   													,   #? 	body diode reverse recovery current
									'Qrr'               	:   9.9e-9	                                  												, 	#? 	body diode reverse recovery charge
									'Is'                  	:   20              																		, 	#? 	body diode reference current
									'Vs'					:	20																						,	#?	body diode reference voltage
                                    'VIcurve'		:	{																									#!	body diode VI characteristics
                                        'Vfvec'				:	Vfvec																					,	#?	forward voltage vector
                                        'Ifvec'				:	Ifvec																					,	#?	forward current vector
                                        'Temps'				:	[25,175]																				,	#?	temperature vector
                                        'Vfscale'			:	1.205																						#?	Vf scaling to account for min, typ and max deviations
									},
						},
							'GateDriver'			:	{																									#!	gate driver parameters
									'Config'				:	3																						,	#?	1->high-side | 2->low-side | 3->disable
									'Von'					:	12																						,	#?	ON driving voltage
									'Voff'					:	0																						,	#?	OFF driving voltage
									'Ron'					:	5																						,	#?	sourcing output resistance
									'Roff'					:	5																						,	#?	sinking output resistance
									'Lon'					:	0																						,	#?	sourcing output inductance
									'Loff'					:	0																						,	#?	sinking output inductance
									'Delay'					:	0																						,	#?	input-to-output total deadtime
									'Trise'					:	0																						,	#?	output rising time
									'Tfall'					:	0																						,	#?	output falling time
									'UVLO_Start'			:	7.0																						,	#?	UVLO startup voltage threshold
									'UVLO_Stop'				:	6.5																						,	#?	UVLO shutdown voltage threshold
									'UVLO_Delay'			:	100e-9																					,	#?	delay between UVLO startup and shutdown
									'CurrentLimit'	:	{																									#*	current limit of driver stage
										'Config'			:	2																						,	#?	1->enable | 2->disable
										'Ts'				: 	0 																						,	#?	sampling time between inductive & capacitive links
										'tau'				: 	0																						,	#?	first-order delay between inductive & capacitive links
                                    	'Rs'				: 	0																						,	#?	source impedance of inductive link
										'Cs'				:	1e-12																					,	#?	source capacitance of capacitive link
                                        'UpLim'				: 	10																						,	#?	max current limit on capacitive link
                                        'LoLim'				: 	-10																						,	#?	min current limit on capacitive link
                                        'Voffset'			: 	0																							#?	voltage offset between inductive & capacitive links
									},
									'Masking'		:	{																									#*	switching stages masking
										'ON'	:	{																										#	ON path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										},
										'OFF'	:	{																										#	OFF path masking
											'Config'		:	2																						,	#?	1->enable | 2->disable
											'HIGH'	:	{																									#!	HIGH mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[0, 0]																						#?	mask output
											},
											'LOW'	:	{																									#!	LOW mask configuration
												'TimeVec'	:	[0, 1]																					,	#?	activation time vector
												'OutVec'	:	[1, 1]																						#?	mask output
											}
										}
									},
									'Boot'			:	{																									#*	bootstrap/charge pump parameters
										'Config'			:	1																						,	#?	1->bootstrap | 2->charge pump
										'Von'				:	14																						,	#?	boostrap driving voltage
										'Cboot'				:	4.7e-6																					,	#?	bootstrap capacitance
										'Vinit'				:	0																						,	#?	bootstrap capacitance initial voltage
										'Rboot'				:	10																						,	#?	bootstrap resistance
										'Vfboot'			:	0.87																					,	#?	bootstrap diode forward voltage
										'Rdboot'			:	1e-3																					,	#?	bootstrap diode ON-state resistance
										'Ichrg'				:	300e-6																					,	#?	charge pump supply current
										'Idis'				:	5e-6																					,	#?	charge pump loading or leakage current
										'Cpar'				:	0																						,	#?	charge pump parallel cap to break state/source dependency
									    'UVLO_Start'		:	11.6																					,	#?	threshold value to start the charge pump
										'UVLO_Stop'			:	12.4																						#?	threshold value to stop the charge pump
									},
							},
							'nParallel'   					:	1                                       												,   #? 	number of parallel devices
							'Rth_jc'						:	2.35																					,	#?	junction-to-case thermal resistance
							'Cth_jc'						:	0.00																					,	#?	junction-to-case thermal capacitance
							'Rth_ca'              			:   2.35            																		,   #? 	case-to-ambient thermal resistance
							'Cth_ca'              			:   0.0             																		,   #? 	case-to-ambient thermal capacitance
							'Tinit'							:	0.0																						,	#?	initial juntion temperature
							'Pinit'							:	0.0																						,	#?	initial power dissipation
							'Coss'					: 	{																									#!	device Coss parameters
								'C'							:	536e-12																					,	#? 	device parasitic output capacitance
								'R'							:	1																						,	#?	Coss resistance to emulate limited dV/dt
								'L'							:	100e-9																					,	#?	Coss inductance to reduce current slope
								'Vvec'						:	Coss[0]																					,	#? 	device Coss voltage vector
								'Cvec'						:	Coss[1]																					,	#?	device Coss capacity vector
								'Offset'					:	0																						,	#?	parasitic offset to Coss
                                'Factor'					:	1.0																						,	#?	parasitic tolerance to Coss
								'Qoss'						:	Qoss																					,	#?	equivalent charge of Coss
								'Eoss'						:	Eoss																					,	#?	equivalent energy of Coss
								'Config'					:	5																							#? 	1->capacitor only | 2->include ESR | 3->include ESR & ESL | 4->variable capacitor | 5->pass | 6->short
						},
                        	'Crss'					:	{																									#!	device Crss parameters
                                'Crss_er'					:	Crss_er																					,	#?	energy-related Crss
                                'Cvec'						:	Crss[1]																					,	#?	device Crss capacity vector
                                'Vvec'						:	Crss[0]																					,	#?	device Crss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Crss
								'Factor'					:	1.0																							#?	parasitic tolerance to Crss
						},
							'Ciss'					:	{																									#!	device Ciss parameters
								'Cvec'						:	Ciss[1]																					,	#?	device Ciss capacity vector
								'Vvec'						:	Crss[0]																					,	#?	device Ciss voltage vector
								'Offset'					:	0																						,	#?	parasitic offset to Ciss
								'Factor'					:	1.0																							#?	parasitic tolerance to Ciss
							},
							'Cds'					:	{																									#!	device Cds parameters
								'Cvec'						:	(dp.np.array(Coss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cds capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cds voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgd'					:	{																									#!	device Cgd parameters
								'Cvec'						:	Crss[1]																					,	#?	device Cgd capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgd voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
							},
							'Cgs'					:	{																									#!	device Cgs parameters
								'Cvec'						:	(dp.np.array(Ciss[1]) - dp.np.array(Crss[1])).tolist()									,	#?	device Cgs capacity vector
								'Vvec'						:	Coss[0]																					,	#?	device Cgs voltage vector
								'Offset_ON'					:	0																						,	#?	tuning offset for turn ON
								'Offset_OFF'				:	0																						,	#?	tuning offset for turn OFF
								'Factor_ON'					:	1.0																						,	#?	tuning factor for turn ON
								'Factor_OFF'				:	1.0																							#?	tuning factor for turn OFF
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
							'Tau_deg'						:	100e-9																					,	#?	deglitch filter for currents and voltages
							'RCsnubber'						:	2																						,	#?	1->enable | 2->disable
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
                                'AIMDQ75R060M1H'		:	AIMDQ75R060M1H			,
                                'AIMDQ75R040M1H'		:	AIMDQ75R040M1H			,
                                'SCT055HU65G3AG'		:	SCT055HU65G3AG			,
								'SCTH35N65G2V'			:	SCTH35N65G2V
							}

shortCircuitSwitchVars	= 	{
								'NVMTS0D6N04CL' 		: 	NVMTS0D6N04CL 			,
                                'NVMTS0D6N04C'			:	NVMTS0D6N04C			,
                                'SQJQ144AER'			:	SQJQ144AER				,
                                'NVMJST0D7N04XM'		:	NVMJST0D7N04XM			,
                                'NVMJST0D5N04XM'		:	NVMJST0D5N04XM
							}

FreewheelingSwitchVars	=	{
								'NVMFS3D6N10MCL'		:	NVMFS3D6N10MCL			,
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
                                'AIMDQ75R060M1H'		:	AIMDQ75R060M1H			,
                                'AIMDQ75R040M1H'		:	AIMDQ75R040M1H			,
                                'SCT055HU65G3AG'		:	SCT055HU65G3AG			,
								'SCTH35N65G2V'			:	SCTH35N65G2V			,
                                'NVMTS0D6N04CL' 		: 	NVMTS0D6N04CL 			,
                                'NVMTS0D6N04C'			:	NVMTS0D6N04C			,
                                'SQJQ144AER'			:	SQJQ144AER				,
                                'NVMFS3D6N10MCL'		:	NVMFS3D6N10MCL			,
                                'PMT200EPE'				:	PMT200EPE				,
                                'BUK9Y6R540H'			:	BUK9Y6R540H				,
                                'NVMJST3D3N08X'			:	NVMJST3D3N08X			,
                                'NVBYST0D6N08X'			:	NVBYST0D6N08X			,
                                'NVMJST004N08X'			:	NVMJST004N08X			,
                                'NVMJST0D7N04XM'		:	NVMJST0D7N04XM			,
                                'NVMJST0D5N04XM'		:	NVMJST0D5N04XM
							}
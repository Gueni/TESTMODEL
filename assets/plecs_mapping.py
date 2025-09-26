
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?												  ____  _     _____ ____ ____    __  __                   _
#?												 |  _ \| |   | ____/ ___/ ___|  |  \/  | __ _ _ __  _ __ (_)_ __   __ _
#?												 | |_) | |   |  _|| |   \___ \  | |\/| |/ _` | '_ \| '_ \| | '_ \ / _` |
#?												 |  __/| |___| |__| |___ ___) | | |  | | (_| | |_) | |_) | | | | | (_| |
#?												 |_|   |_____|_____\____|____/  |_|  |_|\__,_| .__/| .__/|_|_| |_|\__, |
#?												                                             |_|   |_|            |___/
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import Dependencies as dp
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
input_dict						=	dp.Param_Dicts.ModelVars								# Dictionary of Current Simulation Parameters.
source_mdlvar					=	dp.copy.deepcopy(input_dict)							# Sub dictionaries for config_dict : by default is Param_Dicts.
config_dicts					= 	{ 														# Simulation Configurations Dictionary.
										'Probes'  			: 	source_mdlvar['Common']['Probes']			,
										'ToFile'			:	source_mdlvar['Common']['ToFile']			,
										'PSFBconfigs'  		: 	source_mdlvar['Common']['PSFBconfigs'] 	,
										'RboxConfigs'  		: 	source_mdlvar['Common']['RboxConfigs']
       								}
values_dicts 					= 	dp.msc.Misc().keys_exists(config_dicts,source_mdlvar)	# Loop over dict and only pop out config_dicts& leave values.
Maps_index 						= 	{														# Mode of operation (nanmax , absolute , mean ...)
    																						# used in miscellaneous lib to define the mode of operation (nanmax , absolute , mean ...)
                          																	# & the names of the corresponding matrices
                            			'DCDC_data_mat' 	: [[1,4,5,1,4,5,1,1,1,5,5,1,1],[-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600]] ,
										'OBC_data_mat' 		: [[],[]],
										'DCDC_map_names'	: [	"Peak_Currents"		,
                              									"RMS_Currents"		,
                              									"AVG_Currents"		,
                              									"Peak_Voltages"		,
                              									"RMS_Voltages"		,
                              									"AVG_Voltages"		,
																"FFT_Current"		,
                                       							"FFT_Voltage"		,
                              									"Dissipations"		,
                                       							"Elec_Stats"		,
                                       							"Temps"				,
																"Thermal_Stats"		,
                                       							"Controls"
                                       						  ],
       									'OBC_map_names'		: []
									}

DCDC_pmap_Raw	 				=	[														# DCDC Raw mapping
									'Time'												,
									#? PEAK CURRENTS RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
         							# Resistive-----------------------------------------
									'CT Trafo Primary Current' 							,'CT Trafo Secondary Current'						,
									'Choke RC Snubber Capacitor Current' 				,'Choke RC Snubber Resistance Current'  			,'Choke RC Snubber Par Res Current'					,
									'RCD Clamp Capacitor Current'  						,'RCD Clamp Resistance Current'  					,
         							'Freewheeler Blocking Cap Current'  				,'Freewheeler Resistor Current'  					,'Freewheeler Impedance Cap Current' 				,
                					'Damping Resistor Current'  						,
                     				'LV Current Sensor Current'							,
									'HV X-Caps 1 Current'								,'HV X-Caps 2 Current'  							,
         							'HV Current Sensor Current'  						,
         							'Blocking Capacitor Current' 						,
                					'Transformer Snubber Cap Current'					,'Transformer Snubber Res Current'					,
                					'MOSFET RC Snubber Cap Current'						,'MOSFET RC Snubber Res Current'					,
                     				'HV Y-Caps Current'  								,
                     				'LV FullBridge Snubber Cap Current'					,'LV FullBridge Snubber Res Current'				,
                         			'HV Snubber Caps Current'  							,
                         			'Output Ceramic Capacitors Current'  				,'Output Electrolytic Capacitors Current'  			,'Output Y-Cap Current'				  		        ,
                            		'HV Voltage Sensor Current'  						,
                              		'HV CMC Choke Current'  							,
									#*---------------
                              		'LV Filter X-Cap 1 Current'	  						,'LV Filter X-Cap 2 Current'						,'LV Filter Elko-Cap Current'						,
                            		'LV Filter Y-Cap Current'							,
                            		'LV Filter DMC Current'  							,
                              		'LV Filter CMC Current'  							,
         							'LV Filter Output Current RbPlus'					,
         							'LV Filter Output Current RbMinus'					,
									# Non Resistive-------------------------------------
         							'RCD Clamp Transistor Current' 						,'RCD Clamp Bodydiode Current'  					,
           							'LV Rectifiers Current 1'							,'LV Rectifiers Current 2'							,
           							'DC Choke Current'  								,
                  					'Freewheeler Switch Current 1'						,'Freewheeler Switch Current 2'						,
									'Short Circuit Current 1'							,'Short Circuit Current 2'							,
         							'HV Left-Leg HS Current 1'  						,'HV Left-Leg HS Current 2'  						,
                					'HV Right-Leg HS Current 1'  						,'HV Right-Leg HS Current 2' 						,
                					'Transformer Primary Current'	  					,'Transformer Secondary Current'					,'Transformer Magnetizing Current'					,
                     				'HV Left-Leg ON Current'							,'HV Left-Leg OFF Current'							,'HV Left-Leg Max Current1'							,
									'HV Left-Leg Max Current2'							,
									'HV Right-Leg ON Current'							,'HV Right-Leg OFF Current'							,'HV Right-Leg Max Current1'						,
									'HV Right-Leg Max Current2'							,
         							'Pack Current'										,
                					'Relay Current Main' 								,'Relay Current DCDC' 								,
									'DC Link Current'									,
					                'KL30 Current'										,
									'ENBN DCDC Current'									,'ENBN Battery Current'								,
									'LV Filter Input Current'							,'LV Filter Output Current'							,
									'CISPR Input Current'								,'CISPR Output Current'								,
									'Load L_F Current'									,'Load L_B Current'									,
									'CTRL Current'										,'PECU Current'										,'Rbox Current'										,
									#? PEAK VOLTAGES RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
         							'CT Trafo Primary Voltage'  				,
									'CT Trafo Secondary Voltage'  				,
									'Choke RC Snubber Voltage 1'  			    ,
									'Choke RC Snubber Voltage 2'  			    ,
									'Choke RC Snubber Voltage 3'  			    ,
									'RCD Clamp Capacitor Voltage'  		    	,
									'RCD Clamp Resistance Voltage'  		    ,
									'Freewheeler Blocking Cap Voltage'  	    ,
									'Freewheeler Resistor Voltage'  		    ,
									'Freewheeler Impedance Cap Voltage'  	    ,
									'Damping Resistor Voltage'  			    ,
									'LV Current Sensor Voltage'  			    ,
									'HV X-Caps 1 Voltage'  				    	,
									'HV X-Caps 2 Voltage'  				    	,
									'HV Current Sensor Voltage'  			    ,
									'Blocking Capacitor Voltage'  			    ,
									'Transformer Snubber Voltage 1'		    	,
									'Transformer Snubber Voltage 2'		    	,
									'MOSFET RC Snubber Voltage 1'			    ,
									'MOSFET RC Snubber Voltage 2'			    ,
									'HV Y-Caps Voltage'  					    ,
									'LV FullBridge Snubber Voltage 1'		    ,
									'LV FullBridge Snubber Voltage 2'		    ,
									'HV Snubber Caps Voltage'  			    	,
									'Output Ceramic Capacitors Voltage'  	    ,
									'Output Electrolytic Capacitors Voltage'   	,
									'Output Y-Cap Voltage'				  	    ,
									'HV Voltage Sensor Voltage'  			    ,
									'HV CMC Choke Voltage'  				    ,
                              		'LV Filter X-Cap 1 Voltage'	  				,
                                	'LV Filter X-Cap 2 Voltage'					,
                                 	'LV Filter Elko-Cap Voltage'				,
									'LV Filter Y-Cap Voltage'  			   		,
									'LV Filter DMC Voltage'  				    ,
									'LV Filter CMC Voltage'  				    ,
									'LV Filter Output Voltage 1'               	,
									'LV Filter Output Voltage 2'               	,
									'RCD Clamp Transistor Voltage'  		    ,
									'RCD Clamp Bodydiode Voltage'  		    	,
									'LV Rectifiers Voltage 1'	  			    ,
									'LV Rectifiers Voltage 2'	  			    ,
									'DC Choke Voltage'  					    ,
									'Freewheeler Switch Voltage 1'  		    ,
									'Freewheeler Switch Voltage 2'  		    ,
									'Short Circuit Voltage 1'				    ,
									'Short Circuit Voltage 2'				    ,
									'HV Left-Leg HS Voltage 1'  			    ,
									'HV Left-Leg HS Voltage 2'  			    ,
									'HV Right-Leg HS Voltage 1'  			    ,
									'HV Right-Leg HS Voltage 2'  			    ,
									'Transformer Primary Voltage'  		    	,
									'Transformer Secondary Voltage'  		    ,
									'Transformer Flux'  					    ,
									'Pack Voltage'							    ,
									'Relay Voltage Main' 					    ,
									'Relay Voltage DCDC' 					    ,
									'DC Link Voltage'						    ,
									'KL30 Voltage'  						    ,
									'ENBN DCDC Voltage'					    	,
									'ENBN Battery Voltage'					    ,
									'LV Filter Input Voltage'  			    	,
									'LV Filter Output Voltage 3'  			    ,
									'CISPR Input Voltage'					    ,
									'CISPR Output Voltage'					    ,
									'Load L_F Voltage'						    ,
									'Load L_B Voltage'						    ,
									'CTRL Voltage'							    ,
									'PECU Voltage'							    ,
									'Rbox Voltage'							    ,
									#? DISSIPATION RAW MAPPING-----------------------------------------------------------------------------------------------------------------------------------
         							# exported from plecs--------------------------------
									'LL_HS_LS Dissipation 1'							,'LL_HS_LS Dissipation 2'							,'RL_HS_LS Dissipation 1'							,
									'RL_HS_LS Dissipation 2'							,'SR Dissipation 1' 								,'SR Dissipation 2'									,
									'SC Switch Dissipation 1' 							,'SC Switch Dissipation 2'							,'RCD Clamp Transistor Dissipation'					,
									'RCD Clamp Bodydiode Dissipation'  					,'Transformer Rpri Copper Dissipation' 				,'Transformer Rsec Copper Dissipation'  			,
									'Transformer Core Dissipation'  					,'Freewheeler Switch Dissipation 1' 				,'Freewheeler Switch Dissipation 2'					,
									'LL TL'												,'RL TL'											,'SR TL'											,
									'SC TL'												,'RCD_TL'											,'Trafo TL'											,
									'DC Choke Dissipation'								,'IMS TL'											,'CT Sensor diode Dissipation'						,
									'FRW_TL'											,
									# calculated from resistances -----------------------
									'CT Trafo Primary Dissipation' 						,'CT Trafo Secondary Dissipation'					,
									'Choke RC Snubber Capacitor Dissipation' 			,'Choke RC Snubber Resistance Dissipation'  		,'Choke RC Snubber Rpar Dissipation'				,
									'RCD Clamp Capacitor Dissipation'  					,'RCD Clamp Resistance Dissipation'  				,
         							'Freewheeler Blocking Cap Dissipation'  			,'Freewheeler Resistor Dissipation'  				,'Freewheeler Impedance Cap Dissipation' 			,
                					'Damping Resistor Dissipation'  					,
                     				'LV Current Sensor Dissipation'						,
									'HV X-Caps 1 Dissipation'							,'HV X-Caps 2 Dissipation'  						,
         							'HV Current Sensor Dissipation'  					,
         							'Blocking Capacitor Dissipation' 					,
                					'Transformer Snubber Cap Dissipation'				,'Transformer Snubber Res Dissipation'				,
                					'MOSFET RC Snubber Cap Dissipation'					,'MOSFET RC Snubber Res Dissipation'				,
                     				'HV Y-Caps Dissipation'  							,
                     				'LV FullBridge Snubber Cap Dissipation'				,'LV FullBridge Snubber Res Dissipation'			,
                         			'HV Snubber Caps Dissipation'  						,
                         			'Output Ceramic Capacitors Dissipation'  			,'Output Electrolytic Capacitors Dissipation'  		,'Output Y-Cap Dissipation'				  			,
                            		'HV Voltage Sensor Dissipation'  					,
                              		'HV CMC Choke Dissipation'  						,

                              		'LV Filter X-Cap 1 Dissipation'	  					,
									'LV Filter X-Cap 2 Dissipation'	  					,
									'LV Filter Elko-Cap Dissipation'	  				,
                            		'LV Filter Y-Cap Dissipation'						,
                            		'LV Filter DMC Dissipation'  						,
                              		'LV Filter CMC Dissipation'  						,
         							'LV Filter Single Busbar Rb_Plus Dissipation'  		,
                					'LV Filter Single Busbar Rb_Minus Dissipation'  	,

         							#? ELECTRIC STATS RAW MAPPING--------------------------------------------------------------------------------------------------------------------------------
									'Target LV Voltage'  								,
         							'Target Load Power'  								,
                					'Target HV Voltage'  								,
                     				'Measured Load Voltage L_F' 						,
                     				'Measured Load Power L_F' 							,
                          			'Measured Load Voltage L_B' 						,
                     				'Measured Load Power L_B' 							,
									'Measured HV Voltage'   							,
                                	'Measured Load Current L_F' 						,
                          			'Measured Load Current L_B' 						,
                                 	'Measured LV Output Voltage' 						,
                                	'Measured LV Output Current' 						,
         							'Measured HV Current'								,
									'Measured Output Power'								,
         							'Measured Input Power'	  							,
									#? TEMPERATURES RAW MAPPING----------------------------------------------------------------------------------------------------------------------------------
									'HV FB Right Leg Temperature'  						,'HV FB Left Leg Temperature'  						,'Rectifier Temperature'  							,
									'Short-Circuit Switch Temperature'  				,'Active Clamp Switch Temperature'					,'Trafo Pri Winding Temperature' 				    ,
									'Trafo Sec Winding Temperature'						,'Trafo Core Temperature'							,'Shunt Temperature' 								,
									'Choke Winding Temperature'							,'Choke Core Temperature'							,'IMS Board Temperature'							,
									'Water Temperature'									,'HV FB Left Leg Rth'								,'HV FB Right Leg Rth'								,
									'Rectifier Rth'										,'Short-Circuit Switch Rth'							,'Active Clamp Switch Rth'							,
         							#? THERMAL STATS RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
									'Single-Rail Total Dissipation'  					,'Dual-Rail Total Dissipation'  					,
									'Single-Rail Efficiency'  							,'Dual-Rail Efficiency'  							,
									'Single-Rail Efficiency Aux'  						,'Dual-Rail Efficiency Aux'  						,
         							'Single-Rail Input Power'  							,'Dual-Rail Input Power'  							,
									#? CONTROLLER RAW MAPPING------------------------------------------------------------------------------------------------------------------------------------
									#Carrier Signals---------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Carrier Waveforms 1'					,'PWM Modulator Carrier Waveforms 2'  				,
									#Duty Cycle--------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary Modulator Duty Cycle'  		,'PWM Modulator Secondary Modulator Duty Cycle'  	,
									#PWM Signals-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs S1'  			,'PWM Modulator Primary PWM Outputs S2'  			,'PWM Modulator Primary PWM Outputs S3'  			,
									'PWM Modulator Primary PWM Outputs S4'  			,'PWM Modulator Secondary PWM Outputs S5'  			,'PWM Modulator Secondary PWM Outputs S6'  			,
									'PWM Modulator Secondary PWM Outputs S7'  			,'PWM Modulator Secondary PWM Outputs S8'  			,'PWM Modulator Auxiliary PWM Outputs Sac'  		,
									'PWM Modulator Auxiliary PWM Outputs Sfw'  			,'PWM Modulator Auxiliary PWM Outputs Ssc'  		,'PWM Modulator Auxiliary PWM Outputs Sdis'  		,
									#LV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured Output Ceramic Capacitors Voltage'  		,'Measured LV Filter Output Voltage'  				,'Measured ADCs Sampled Signals 1'  				,
									'Measured ADCs Analog Signals 1'  					,'Measured ADCs ADC Signals 1'  					,'Measured HW Protection Comparator Signals 1'  	,
									#LV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured PSFB LV Current Sensor Current'  			,'Measured ADCs Sampled Signals 2'  				,'Measured ADCs Analog Signals 2'  					,
									'Measured ADCs ADC Signals 2'  						,'Measured HW Protection Comparator Signals 2'  	,
									#HV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Filter Voltages 1'  					,'Measured HV Filter Voltages 2'  					,'Measured ADCs Sampled Signals 3'  				,
									'Measured ADCs Analog Signals 3'  					,'Measured ADCs ADC Signals 3'  					,'Measured HW Protection Comparator Signals 3'  	,
									#HV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Current Sensor Current'  				,'Measured ADCs Sampled Signals 4'  				,'Measured ADCs ADC Signals 4'  					,
									#CT Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured CT Current Sensor Current'  				,'Measured ADCs Sampled Signals 5' 					, 'Measured ADCs ADC Signals 5'  					,
									#Digital Raw Values------------------------------------------------------------------------------------------------------------------------------------------
									'Measured ADCs Sensors Digital Values Vo'			,'Measured ADCs Sensors Digital Values Io'  		,'Measured ADCs Sensors Digital Values Vin'  		,
									'Measured ADCs Sensors Digital Values Iin'  		,'Measured ADCs Sensors Digital Values CT' 			,'Measured ADCs Digital Reference'  				,
									#LV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 1'  							,'ADCs S-and-H Voltages 1'  						,'ADCs Sampled Voltages 1'  						,
									#LV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 2'  							,'ADCs S-and-H Voltages 2'  						,'ADCs Sampled Voltages 2'  						,
									#HV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 3'  							,'ADCs S-and-H Voltages 3'  						,'ADCs Sampled Voltages 3'  						,
									#HV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 4'  							,'ADCs S-and-H Voltages 4'  						,'ADCs Sampled Voltages 4'  						,
									#CT Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 5'  							,'ADCs S-and-H Voltages 5'  						,'ADCs Sampled Voltages 5'  						,
									#Charging Currents-------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Charging Currents 1'  						,'ADCs Charging Currents 2'  						,'ADCs Charging Currents 3'  						,
									'ADCs Charging Currents 4'  						,'ADCs Charging Currents 5'  						,'ADCs Charging Currents 6'  						,
									'ADCs Charging Currents 7'  						,'ADCs Charging Currents 8'  						,'ADCs Charging Currents 9'							,
									'ADCs Charging Currents 10'							,
									#Sample Triggers---------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Sampling Triggers 1'  						,'ADCs Sampling Triggers 2'  						,'ADCs Sampling Triggers 3'  						,
									'ADCs Sampling Triggers 4'  						,'ADCs Sampling Triggers 5'							,
									#LV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'PSFB Output Ceramic Capacitors Voltage'  			,'LV Filter Input Voltage Sampling'  				,'LV Filter Output Voltage Sampling'  				,
									#LV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'LV Current Sensor Current Sampling'	  			,
									#HV Voltage--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Filter X-Caps Voltages 1 Sampling'  			,'HV Filter X-Caps Voltages 2 Sampling'  			,
									#HV Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Current Sensor Current Sampling'	  			,
									#CT Current--------------------------------------------------------------------------------------------------------------------------------------------------
									'CT Current Sensor Current Sampling'	  			,
									#PWM Signals-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs 1'  				,'PWM Modulator Primary PWM Outputs 2'  			,'PWM Modulator Primary PWM Outputs 3'  			,
									'PWM Modulator Primary PWM Outputs 4'  				,'PWM Modulator Secondary PWM Outputs 1'  			,'PWM Modulator Secondary PWM Outputs 2'  			,
									'PWM Modulator Secondary PWM Outputs 3'  			,'PWM Modulator Secondary PWM Outputs 4'  			,
									#Sample Triggers---------------------------------------------------------------------------------------------------------------------------------------------
									'Sample Trigger 1'  								,'Sample Trigger 2'  								,'Sample Trigger 3'  								,
									'Sample Trigger 4'  								,'Sample Trigger 5'									,
									#Controller Update-------------------------------------------------------------------------------------------------------------------------------------------
									'Controller Update'  								,
									#Measured Signals--------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Measured Signals Vo'					,'SW Protection Measured Signals Io'				,'SW Protection Measured Signals Vin'				,
									'SW Protection Measured Signals Iin'				,'SW Protection Upper Thresholds Vo'				,'SW Protection Upper Thresholds Io'				,
									'SW Protection Upper Thresholds Vin'				,'SW Protection Upper Thresholds Iin'				,'SW Protection Lower Thresholds Vo'				,
									'SW Protection Lower Thresholds Io'					,'SW Protection Lower Thresholds Vin'				,'SW Protection Lower Thresholds Iin'				,
									#Fault Counters----------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Fault Counters Vo'					,'SW Protection Fault Counters Io'					,'SW Protection Fault Counters Vin'					,
									'SW Protection Fault Counters Iin'					,
									#Comparators Triggers----------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Fault Comparators VoH'				,'SW Protection Fault Comparators VoL'				,'SW Protection Fault Comparators IoH'				,
									'SW Protection Fault Comparators IoL'				,'SW Protection Fault Comparators VinH'				,'SW Protection Fault Comparators VinL'				,
									'SW Protection Fault Comparators IinH'				,'SW Protection Fault Comparators IinL'				,
									#Disable Latches---------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Disable Latches Vo'					,'SW Protection Disable Latches Io'					,'SW Protection Disable Latches Vin'				,
									'SW Protection Disable Latches Iin'					,
									#Enable------------------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Enable Signal'						,
									#Output Voltage----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage Ref'					,'HW Protection Output Voltage In'					,'HW Protection Output Voltage VH'					,
									'HW Protection Output Voltage VL'					,
									#Positive Output Current-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Positive Output Current Ref'			,'HW Protection Positive Output Current In'			,'HW Protection Positive Output Current VH'			,
									'HW Protection Positive Output Current VL'			,
									#Negative Output Current-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Negative Output Current Ref'			,'HW Protection Negative Output Current In'			,'HW Protection Negative Output Current VH'			,
									'HW Protection Negative Output Current VL'			,
									#Input Voltage-----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Input Voltage Ref'					,'HW Protection Input Voltage In'					,'HW Protection Input Voltage VH'					,
									'HW Protection Input Voltage VL'					,
									#Triggers----------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage 3'					,'HW Protection Positive Output Current 3'			,'HW Protection Negative Output Current 3'			,
									'HW Protection Input Voltage 3'						,
									#States------------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Latch State'							,'HW Protection Reset State'
                     				]
DCDC_pmap_plt					=	[														# DCDC plots mapping
    							#?	['TITLE OF FIGURE'					,'CURRENT IN RAW MAPPING'					,'VOLTAGE IN RAW MAPPING'					]
								#                   	-----------------------------------------------------------------------------------------------------------------------------
								['CT Trafo Primary' 						,   'CT Trafo Primary Current' 							,   'CT Trafo Primary Voltage'  			],
								['CT Trafo Secondary'						,   'CT Trafo Secondary Current'						,   'CT Trafo Secondary Voltage'  			],
								['Choke RC Snubber Capacitor' 				,   'Choke RC Snubber Capacitor Current' 				,   'Choke RC Snubber Voltage 1'  			],
								['Choke RC Snubber Resistance'  			,   'Choke RC Snubber Resistance Current'  				,   'Choke RC Snubber Voltage 2'  			],
								['Choke RC Snubber Par Res'					,   'Choke RC Snubber Par Res Current'					,   'Choke RC Snubber Voltage 3'  	    	],
								['RCD Clamp Capacitor'  					,   'RCD Clamp Capacitor Current'  						,   'RCD Clamp Capacitor Voltage'  			],
								['RCD Clamp Resistance'  					,   'RCD Clamp Resistance Current'  					,   'RCD Clamp Resistance Voltage'  		],
								['Freewheeler Blocking Cap'  				,   'Freewheeler Blocking Cap Current'  				,   'Freewheeler Blocking Cap Voltage'  	],
								['Freewheeler Resistor'  					,   'Freewheeler Resistor Current'  					,   'Freewheeler Resistor Voltage'  		],
								['Freewheeler Impedance Cap' 				,   'Freewheeler Impedance Cap Current' 				,   'Freewheeler Impedance Cap Voltage'  	],
								['Damping Resistor'  						,   'Damping Resistor Current'  						,   'Damping Resistor Voltage'  			],
								['LV Current Sensor'						,   'LV Current Sensor Current'							,   'LV Current Sensor Voltage'  			],
								['HV X-Caps 1'								,   'HV X-Caps 1 Current'								,   'HV X-Caps 1 Voltage'  					],
								['HV X-Caps 2'  							,   'HV X-Caps 2 Current'  								,   'HV X-Caps 2 Voltage'  					],
								['HV Current Sensor'  						,   'HV Current Sensor Current'  						,   'HV Current Sensor Voltage'  			],
								['Blocking Capacitor' 						,   'Blocking Capacitor Current' 						,   'Blocking Capacitor Voltage'  			],
								['Transformer Snubber Cap'					,   'Transformer Snubber Cap Current'					,   'Transformer Snubber Voltage 1'			],
								['Transformer Snubber Res'					,   'Transformer Snubber Res Current'					,   'Transformer Snubber Voltage 2'			],
								['MOSFET RC Snubber Cap'					,   'MOSFET RC Snubber Cap Current'						,   'MOSFET RC Snubber Voltage 1'			],
								['MOSFET RC Snubber Res'					,   'MOSFET RC Snubber Res Current'						,   'MOSFET RC Snubber Voltage 2'			],
								['HV Y-Caps'  								,   'HV Y-Caps Current'  								,   'HV Y-Caps Voltage'  					],
								['LV FullBridge Snubber Cap'				,   'LV FullBridge Snubber Cap Current'					,   'LV FullBridge Snubber Voltage 1'		],
								['LV FullBridge Snubber Res'				,   'LV FullBridge Snubber Res Current'					,   'LV FullBridge Snubber Voltage 2'		],
								['HV Snubber Caps'  						,   'HV Snubber Caps Current'  							,   'HV Snubber Caps Voltage'  				],
								['Output Ceramic Capacitors'  				,   'Output Ceramic Capacitors Current'  				,   'Output Ceramic Capacitors Voltage'  	],
								['Output Electrolytic Capacitors'  			,   'Output Electrolytic Capacitors Current'  			,   'Output Electrolytic Capacitors Voltage'],
								['Output Y-Cap'				  		        ,   'Output Y-Cap Current'				  		        ,   'Output Y-Cap Voltage'				  	],
								['LV Filter X-Cap 1'	  					,   'LV Filter X-Cap 1 Current'	  						,   'LV Filter X-Cap 1 Voltage'  			],
								['LV Filter X-Cap 2'	  					,   'LV Filter X-Cap 2 Current'	  						,   'LV Filter X-Cap 2 Voltage'  			],
								['LV Filter Elko-Cap'	  					,   'LV Filter Elko-Cap Current'	  					,   'LV Filter Elko-Cap Voltage'  			],
								['LV Filter Y-Cap'							,   'LV Filter Y-Cap Current'							,   'LV Filter Y-Cap Voltage'  				],
								['HV Voltage Sensor'  						,   'HV Voltage Sensor Current'  						,   'HV Voltage Sensor Voltage'  			],
								['LV Filter DMC'  							,   'LV Filter DMC Current'  							,   'LV Filter DMC Voltage'  				],
								['LV Filter CMC'  							,   'LV Filter CMC Current'  							,   'LV Filter CMC Voltage'  				],
								['HV CMC Choke'  							,   'HV CMC Choke Current'  							,   'HV CMC Choke Voltage'  		        ],
								['LV Filter Output RbPlus'					,   'LV Filter Output Current RbPlus'					,   'LV Filter Output Voltage 1'  			],
								['LV Filter Output RbMinus'					,   'LV Filter Output Current RbMinus'					,   'LV Filter Output Voltage 2'  			],
								['RCD Clamp Transistor' 					,   'RCD Clamp Transistor Current' 						,   'RCD Clamp Transistor Voltage'  		],
								['RCD Clamp Bodydiode'  					,   'RCD Clamp Bodydiode Current'  						,   'RCD Clamp Bodydiode Voltage'  			],
								['LV Rectifiers 1'							,   'LV Rectifiers Current 1'							,   'LV Rectifiers Voltage 1'	  			],
								['LV Rectifiers 2'							,   'LV Rectifiers Current 2'							,   'LV Rectifiers Voltage 2'	  			],
								['DC Choke'  								,   'DC Choke Current'  								,   'DC Choke Voltage'  					],
								['Freewheeler Switch 1'						,   'Freewheeler Switch Current 1'						,   'Freewheeler Switch Voltage 1'  		],
								['Freewheeler Switch 2'						,   'Freewheeler Switch Current 2'						,   'Freewheeler Switch Voltage 2'  		],
								['Short Circuit 1'							,   'Short Circuit Current 1'							,   'Short Circuit Voltage 1'				],
								['Short Circuit 2'							,   'Short Circuit Current 2'							,   'Short Circuit Voltage 2'				],
								['HV Left-Leg HS 1'  						,   'HV Left-Leg HS Current 1'  						,   'HV Left-Leg HS Voltage 1'  			],
								['HV Left-Leg HS 2'  						,   'HV Left-Leg HS Current 2'  						,   'HV Left-Leg HS Voltage 2'  			],
								['HV Right-Leg HS 1'  						,   'HV Right-Leg HS Current 1'  						,   'HV Right-Leg HS Voltage 1'  			],
								['HV Right-Leg HS 2' 						,   'HV Right-Leg HS Current 2' 						,   'HV Right-Leg HS Voltage 2'  			],
								['Transformer Primary'	  					,   'Transformer Primary Current'	  					,   'Transformer Primary Voltage'  		    ],
								['Transformer Secondary'					,   'Transformer Secondary Current'						,   'Transformer Secondary Voltage'  		],
								['Transformer Magnetizing'					,   'Transformer Magnetizing Current'					,   'Transformer Flux'  					],
								['Pack'										,   'Pack Current'										,   'Pack Voltage'							],
								['Relay Main' 								,   'Relay Current Main' 								,   'Relay Voltage Main' 					],
								['Relay DCDC' 								,   'Relay Current DCDC' 								,   'Relay Voltage DCDC' 					],
								['DC Link'									,   'DC Link Current'									,   'DC Link Voltage'	                    ],
								['KL30'										,   'KL30 Current'										,   'KL30 Voltage'  						],
								['ENBN DCDC'								,   'ENBN DCDC Current'									,   'ENBN DCDC Voltage'						],
								['ENBN Battery'								,   'ENBN Battery Current'								,   'ENBN Battery Voltage'					],
 								['LV Filter Input'							,   'LV Filter Input Current'							,   'LV Filter Input Voltage'  			    ],
								['LV Filter Output'							,   'LV Filter Output Current'							,   'LV Filter Output Voltage 3'  			],
								['CISPR Input '								,   'CISPR Input Current'								,   'CISPR Input Voltage'  			    	],
								['CISPR Output '							,   'CISPR Output Current'								,   'CISPR Output Voltage'  			    ],
								['Load L_F'									,   'Load L_F Current'									,   'Load L_F Voltage'  			   		],
								['Load L_B'									,   'Load L_B Current'									,   'Load L_B Voltage'  			   		],
								['CTRL'										,   'CTRL Current'										,   'CTRL Voltage'  			   		 	],
								['PECU'										,   'PECU Current'										,   'PECU Voltage'  			   		 	],
								['Rbox'										,   'Rbox Current'										,   'Rbox Voltage'  			   		 	]
									]
DCDC_Constants					=	[														# DCDC Constants

                             			['Measured Load Voltage L_F' 		, '[ V ]'	],
							 			['Measured Load Power L_F' 			, '[ W ]'	],
							 			['Measured Load Voltage L_B' 		, '[ V ]'	],
							 			['Measured Load Power L_B' 			, '[ W ]'	],
							 			['Measured Load Current L_F' 		, '[ A ]'	],
							 			['Measured Load Current L_B' 		, '[ A ]'	],
										['Target LV Voltage'				, '[ V ]'	],
          								['Measured LV Output Voltage'		, '[ V ]'	],
                  						['Target HV Voltage'				, '[ V ]'	],
          								['Measured LV Output Current'		, '[ A ]'	],
                  						['Target Load Power'				, '[ W ]'	],
                  						['Measured Output Power'			, '[ W ]'	],
                        				['Measured Input Power'				, '[ W ]'	],
                        				['Measured HV Voltage'				, '[ V ]'	],
                            			['Measured HV Current'				, '[ A ]'	],
                            			['HV FB Right Leg Temperature'		, '[ °C ]'	],
                            			['HV FB Left Leg Temperature'		, '[ °C ]'	],
                               			['Rectifier Temperature'			, '[ °C ]'	],
                               			['Short-Circuit Switch Temperature'	, '[ °C ]'	],
										['Trafo Pri Winding Temperature'	, '[ °C ]'	],
          								['Trafo Sec Winding Temperature'	, '[ °C ]'	],
          								['Trafo Core Temperature'	    	, '[ °C ]'	],
										['Choke Winding Temperature'		, '[ °C ]'	],
          								['Choke Core Temperature'	    	, '[ °C ]'	],
          								['Shunt Temperature'	    		, '[ °C ]'	],
										['IMS Board Temperature'			, '[ °C ]'	],
          								['Water Temperature'				, '[ °C ]'	],
          								['HV FB Left Leg Rth'				, '[ K/W ]' ],
										['HV FB Right Leg Rth'				, '[ K/W ]' ],
          								['Rectifier Rth'					, '[ K/W ]' ],
          								['Short-Circuit Switch Rth'			, '[ K/W ]' ],
										['Active Clamp Switch Rth'			, '[ K/W ]' ]
									]
DCDC_Ctrl_plt					=	[														# DCDC Controls plots mapping.
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									['PWM' ,'Measurments','ADC','Sampling','SW Protection','HW Protection'],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#PWM
										['Carrier Signals' 				,['PWM Modulator Carrier Waveforms 1'				,'PWM Modulator Carrier Waveforms 2'															]	,['[ - ]']],
										['PWM Modulator Duty Cycle' 	,['PWM Modulator Primary Modulator Duty Cycle'		,'PWM Modulator Secondary Modulator Duty Cycle'													]	,['[ - ]']],
										['PWM Signal'					,['PWM Modulator Primary PWM Outputs S1'			,'PWM Modulator Primary PWM Outputs S2'			,'PWM Modulator Primary PWM Outputs S3'
									                     				, 'PWM Modulator Primary PWM Outputs S4'			,'PWM Modulator Secondary PWM Outputs S5'		,'PWM Modulator Secondary PWM Outputs S6'
																		, 'PWM Modulator Secondary PWM Outputs S7'			,'PWM Modulator Secondary PWM Outputs S8'		,'PWM Modulator Auxiliary PWM Outputs Sac'
									                         			, 'PWM Modulator Auxiliary PWM Outputs Sfw'			,'PWM Modulator Auxiliary PWM Outputs Ssc'		,'PWM Modulator Auxiliary PWM Outputs Sdis'		]	,['[ - ]']],
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#Measurments
										['LV Voltage'					,['Measured Output Ceramic Capacitors Voltage'		,'Measured LV Filter Output Voltage'			,'Measured ADCs Sampled Signals 1'
									                     				,'Measured ADCs Analog Signals 1'					,'Measured ADCs ADC Signals 1'					,'Measured HW Protection Comparator Signals 1'	]	,['[ V ]']],
										['LV Current'					,['Measured PSFB LV Current Sensor Current'			,'Measured ADCs Sampled Signals 2'				,'Measured ADCs Analog Signals 2'
									                     				, 'Measured ADCs ADC Signals 2'						,'Measured HW Protection Comparator Signals 2'													]	,['[ A ]']],
									 	['HV Voltage'					,['Measured HV Filter Voltages 1'					,'Measured HV Filter Voltages 2'				,'Measured ADCs Sampled Signals 3'
									                      				, 'Measured ADCs Analog Signals 3'					,'Measured ADCs ADC Signals 3'					,'Measured HW Protection Comparator Signals 3'	]	,['[ V ]']],
										['HV Current'					,['Measured HV Current Sensor Current'				,'Measured ADCs Sampled Signals 4'				,'Measured ADCs ADC Signals 4'					]	,['[ A ]']],

										['CT Current'					,['Measured CT Current Sensor Current'				,'Measured ADCs Sampled Signals 5'				,'Measured ADCs ADC Signals 5'					]	,['[ A ]']],

										['Digital Raw Values'			,['Measured ADCs Sensors Digital Values Vo'			,'Measured ADCs Sensors Digital Values Io'		,'Measured ADCs Sensors Digital Values Vin'
									                           			, 'Measured ADCs Sensors Digital Values Iin'		,'Measured ADCs Sensors Digital Values CT'      ,'Measured ADCs Digital Reference'				]	,['[ V ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#ADC
										['LV Voltage'					,['ADCs ADC Pin Voltages 1'							,'ADCs S-and-H Voltages 1'						,'ADCs Sampled Voltages 1'						]	,['[ V ]']],
										['LV Current'					,['ADCs ADC Pin Voltages 2'							,'ADCs S-and-H Voltages 2'						,'ADCs Sampled Voltages 2'						]	,['[ V ]']],
										['HV Voltage'					,['ADCs ADC Pin Voltages 3'							,'ADCs S-and-H Voltages 3'						,'ADCs Sampled Voltages 3'						]	,['[ V ]']],
										['HV Current'					,['ADCs ADC Pin Voltages 4'							,'ADCs S-and-H Voltages 4'						,'ADCs Sampled Voltages 4'						]	,['[ V ]']],
										['CT Current'					,['ADCs ADC Pin Voltages 5'							,'ADCs S-and-H Voltages 5'						,'ADCs Sampled Voltages 5'						]	,['[ V ]']],
										['Charging Currents'			,['ADCs Charging Currents 1'						,'ADCs Charging Currents 2'						,'ADCs Charging Currents 3'
									                          			, 'ADCs Charging Currents 4'						,'ADCs Charging Currents 5'						,'ADCs Charging Currents 6'
									                             		, 'ADCs Charging Currents 7'						,'ADCs Charging Currents 8'						,'ADCs Charging Currents 9'
																		, 'ADCs Charging Currents 10'																														]	,['[ A ]']],
										['Sample Triggers'				,['ADCs Sampling Triggers 1'						,'ADCs Sampling Triggers 2'						,'ADCs Sampling Triggers 3'
									                         			, 'ADCs Sampling Triggers 4'						,'ADCs Sampling Triggers 5'																		]	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#Sampling
										['LV Voltage'					,['PSFB Output Ceramic Capacitors Voltage'			,'LV Filter Input Voltage Sampling'				,'LV Filter Output Voltage Sampling'			]	,['[ V ]']],
										['LV Current'					,['LV Current Sensor Current Sampling'																												]	,['[ V ]']],
										['HV Voltage'					,['HV Filter X-Caps Voltages 1 Sampling'			,'HV Filter X-Caps Voltages 2 Sampling'															]	,['[ V ]']],
										['HV Current'					,['HV Current Sensor Current Sampling'																												]	,['[ A ]']],
										['CT Current'					,['CT Current Sensor Current Sampling'																												]	,['[ A ]']],
										['PWM Signals'					,['PWM Modulator Primary PWM Outputs 1'				,'PWM Modulator Primary PWM Outputs 2'			,'PWM Modulator Primary PWM Outputs 3'
									                      				, 'PWM Modulator Primary PWM Outputs 4'				,'PWM Modulator Secondary PWM Outputs 1'		,'PWM Modulator Secondary PWM Outputs 2'
																		, 'PWM Modulator Secondary PWM Outputs 3'           ,'PWM Modulator Secondary PWM Outputs 4'														]	,['[ V ]']],
										['Sample Triggers'				,['Sample Trigger 1'								,'Sample Trigger 2'								,'Sample Trigger 3'
									                         			, 'Sample Trigger 4'								,'Sample Trigger 5'																				]	,['[ - ]']],
										['Controller Update'			,['Controller Update'																																]	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#SW Protection
										['Measured Signals'				,['SW Protection Measured Signals Vo'				,'SW Protection Measured Signals Io'			,'SW Protection Measured Signals Vin'
									                          			, 'SW Protection Measured Signals Iin'				,'SW Protection Upper Thresholds Vo'			,'SW Protection Upper Thresholds Io'
									                             		, 'SW Protection Upper Thresholds Vin'				,'SW Protection Upper Thresholds Iin'			,'SW Protection Lower Thresholds Vo'
									                               		, 'SW Protection Lower Thresholds Io'				,'SW Protection Lower Thresholds Vin'			,'SW Protection Lower Thresholds Iin'			]	,['[ V ]','[ A ]']],
										['Fault Counters'				,['SW Protection Fault Counters Vo'					,'SW Protection Fault Counters Io'				,'SW Protection Fault Counters Vin'
									                        			, 'SW Protection Fault Counters Iin'																												]	,['[ V ]','[ A ]']],
										['Comparators Triggers'			,['SW Protection Fault Comparators VoH'				,'SW Protection Fault Comparators VoL'			,'SW Protection Fault Comparators IoH'
									                             		, 'SW Protection Fault Comparators IoL'				,'SW Protection Fault Comparators VinH'			,'SW Protection Fault Comparators VinL'
									                               		, 'SW Protection Fault Comparators IinH'			,'SW Protection Fault Comparators IinL'															]	,['[ V ]','[ A ]']],
										['Disable Latches'				,['SW Protection Disable Latches Vo'				,'SW Protection Disable Latches Io'				,'SW Protection Disable Latches Vin'
									                         			, 'SW Protection Disable Latches Iin'																												]	,['[ V ]','[ A ]']],
										['Enable'						,['SW Protection Enable Signal'																														]	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#HW Protection
										['Output Voltage'				,['HW Protection Output Voltage Ref'				,'HW Protection Output Voltage In'				,'HW Protection Output Voltage VH'
									                        			, 'HW Protection Output Voltage VL'																													]	,['[ V ]']],
										['Positive Output Current'		,['HW Protection Positive Output Current Ref'		,'HW Protection Positive Output Current In'		,'HW Protection Positive Output Current VH'
									                               		, 'HW Protection Positive Output Current VL'																										]	,['[ A ]']],
										['Negative Output Current'		,['HW Protection Negative Output Current Ref'		,'HW Protection Negative Output Current In'		,'HW Protection Negative Output Current VH'
									                               		, 'HW Protection Negative Output Current VL'																										]	,['[ A ]']],
										['Input Voltage'				,['HW Protection Input Voltage Ref'					,'HW Protection Input Voltage In'				,'HW Protection Input Voltage VH'
									                       				, 'HW Protection Input Voltage VL'																													]	,['[ V ]']],
										['Triggers'						,['HW Protection Output Voltage 3'					,'HW Protection Positive Output Current 3'		,'HW Protection Negative Output Current 3'
									                    				, 'HW Protection Input Voltage 3'																													]	,['[ V ]']],
										['States'						,['HW Protection Latch State'						,'HW Protection Reset State'																	]	,['[ - ]']]
									]
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									]
DCDC_DUAL_pmap_Raw				=	[														# DCDC Dual Rail Raw Mapping
									"Time"													,
									#? PEAK CURRENTS RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
									"CT Trafo Primary Current Rail 1",
									"CT Trafo Secondary Current Rail 1",
									"CT Trafo Primary Current Rail 2",
									"CT Trafo Secondary Current Rail 2",

         							"Choke RC Snubber Capacitor Current Rail 1",
									"Choke RC Snubber Resistance Current Rail 1",
									"Choke RC Snubber Par Res Current Rail 1",
									"Choke RC Snubber Capacitor Current Rail 2",
									"Choke RC Snubber Resistance Current Rail 2",
									"Choke RC Snubber Par Res Current Rail 2",

									"RCD Clamp Capacitor Current Rail 1",
									"RCD Clamp Resistance Current Rail 1",
									"RCD Clamp Capacitor Current Rail 2",
									"RCD Clamp Resistance Current Rail 2",

									"Freewheeler Blocking Cap Current Rail 1",
									"Freewheeler Resistor Current Rail 1",
									"Freewheeler Impedance Cap Current Rail 1",
									"Freewheeler Blocking Cap Current Rail 2",
									"Freewheeler Resistor Current Rail 2",
									"Freewheeler Impedance Cap Current Rail 2",

									"Damping Resistor Current Rail 1",
									"Damping Resistor Current Rail 2",

									"LV Current Sensor Current Rail 1",
									"LV Current Sensor Current Rail 2",

									"HV X-Caps 1 Current Rail 1",
									"HV X-Caps 2 Current Rail 1",
									"HV X-Caps 1 Current Rail 2",
									"HV X-Caps 2 Current Rail 2",

									"HV Current Sensor Current Rail 1",
									"HV Current Sensor Current Rail 2",

									"Blocking Capacitor Current Rail 1",
									"Blocking Capacitor Current Rail 2",

									"Transformer Snubber Cap Current Rail 1",
									"Transformer Snubber Res Current Rail 1",
									"Transformer Snubber Cap Current Rail 2",
									"Transformer Snubber Res Current Rail 2",

									"MOSFET RC Snubber Cap Current Rail 1",
									"MOSFET RC Snubber Res Current Rail 1",
									"MOSFET RC Snubber Cap Current Rail 2",
									"MOSFET RC Snubber Res Current Rail 2",

									"HV Y-Caps Current Rail 1",
									"HV Y-Caps Current Rail 2",

									"LV FullBridge Snubber Cap Current Rail 1",
									"LV FullBridge Snubber Res Current Rail 1",
									"LV FullBridge Snubber Cap Current Rail 2",
									"LV FullBridge Snubber Res Current Rail 2",

									"HV Snubber Caps Current Rail 1",
									"HV Snubber Caps Current Rail 2",

									"Output Ceramic Capacitors Current Rail 1",
									"Output Electrolytic Capacitors Current Rail 1",
									"Output Y-Cap Current Rail 1",
									"Output Ceramic Capacitors Current Rail 2",
									"Output Electrolytic Capacitors Current Rail 2",
									"Output Y-Cap Current Rail 2",

									"HV Voltage Sensor Current Rail 1",
									"HV Voltage Sensor Current Rail 2",

									"HV CMC Choke Current Rail 1",
									"HV CMC Choke Current Rail 2",

									'LV Filter X-Cap 1 Current'	  						,
         							'LV Filter X-Cap 2 Current'						,
                					'LV Filter Elko-Cap Current'						,
                            		'LV Filter Y-Cap Current'							,

									"LV Filter DMC Current",

									"LV Filter CMC Current",

									"LV Filter Output Current RbPlus",

									"LV Filter Output Current RbMinus",

         							"RCD Clamp Transistor Current Rail 1",
									"RCD Clamp Bodydiode Current Rail 1",
									"RCD Clamp Transistor Current Rail 2",
									"RCD Clamp Bodydiode Current Rail 2",
									"LV Rectifiers Current 1 Rail 1",
									"LV Rectifiers Current 2 Rail 1",
									"LV Rectifiers Current 1 Rail 2",
									"LV Rectifiers Current 2 Rail 2",
									"DC Choke Current Rail 1",
									"DC Choke Current Rail 2",
									"Freewheeler Switch Current 1 Rail 1",
									"Freewheeler Switch Current 2 Rail 1",
									"Freewheeler Switch Current 1 Rail 2",
									"Freewheeler Switch Current 2 Rail 2",
									"Short Circuit Current 1 Rail 1",
									"Short Circuit Current 2 Rail 1",
									"Short Circuit Current 1 Rail 2",
									"Short Circuit Current 2 Rail 2",
									"HV Left-Leg HS Current 1 Rail 1",
									"HV Left-Leg HS Current 2 Rail 1",
									"HV Left-Leg HS Current 1 Rail 2",
									"HV Left-Leg HS Current 2 Rail 2",
									"HV Right-Leg HS Current 1 Rail 1",
									"HV Right-Leg HS Current 2 Rail 1",
									"HV Right-Leg HS Current 1 Rail 2",
									"HV Right-Leg HS Current 2 Rail 2",
									"Transformer Primary Current Rail 1",
									"Transformer Secondary Current Rail 1",
									"Transformer Magnetizing Current Rail 1",
									"Transformer Primary Current Rail 2",
									"Transformer Secondary Current Rail 2",
									"Transformer Magnetizing Current Rail 2",

									'HV Left-Leg ON Current Rail 1'							,
         							'HV Left-Leg ON Current Rail 2'							,
         							'HV Left-Leg OFF Current Rail 1'							,
                					'HV Left-Leg OFF Current Rail 2'							,
                					'HV Left-Leg Max Current1 Rail 1'							,
                     				'HV Left-Leg Max Current1 Rail 2'							,
									'HV Left-Leg Max Current2 Rail 1'							,
         							'HV Left-Leg Max Current2 Rail 2'							,
									'HV Right-Leg ON Current Rail 1'							,
         							'HV Right-Leg ON Current Rail 2'							,
         							'HV Right-Leg OFF Current Rail 1'							,
                					'HV Right-Leg OFF Current Rail 2'							,
                					'HV Right-Leg Max Current1 Rail 1'						,
                     				'HV Right-Leg Max Current1 Rail 2'						,
									'HV Right-Leg Max Current2 Rail 1'							,
         							'HV Right-Leg Max Current2 Rail 2'							,
									"Pack 1 Current",
									"Pack 2 Current",
									"Relay Main + Current",
									"Relay Main - Current",
									"Relay USMmid Current",
									"Relay USM + Current",
									"Relay USM - Current",
									"Relay DCDC 1 Current",
									"Relay DCDC 2 Current",
									"DC Link Current",
									"KL30 Current",
									"ENBN DCDC Current",
									"ENBN Battery Current",
									"LV Filter Input Current",
									"LV Filter Output Current",
									"CISPR Input Current",
									"CISPR Output Current",
									"Load L_F Current",
									"Load L_B Current",
									"CTRL Current",
									"PECU Current",
									"Rbox Current",
									#? PEAK Voltages RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
									"CT Trafo Primary Voltage Rail 1"  ,
									"CT Trafo Secondary Voltage Rail 1"  ,
									"CT Trafo Primary Voltage Rail 2"  ,
									"CT Trafo Secondary Voltage Rail 2"  ,

									"Choke RC Snubber Voltage 1 Rail 1"  ,
									"Choke RC Snubber Voltage 2 Rail 1"  ,
									"Choke RC Snubber Voltage 3 Rail 1"  ,
									"Choke RC Snubber Voltage 1 Rail 2"  ,
									"Choke RC Snubber Voltage 2 Rail 2"  ,
									"Choke RC Snubber Voltage 3 Rail 2"  ,

									"RCD Clamp Capacitor Voltage Rail 1"  ,
									"RCD Clamp Resistance Voltage Rail 1"  ,

									"RCD Clamp Capacitor Voltage Rail 2"  ,
									"RCD Clamp Resistance Voltage Rail 2"  ,

									"Freewheeler Blocking Cap Voltage Rail 1"  ,
									"Freewheeler Resistor Voltage Rail 1"  ,
									"Freewheeler Impedance Cap Voltage Rail 1"  ,
									"Freewheeler Blocking Cap Voltage Rail 2"  ,
									"Freewheeler Resistor Voltage Rail 2"  ,
									"Freewheeler Impedance Cap Voltage Rail 2"  ,

									"Damping Resistor Voltage Rail 1"  ,
									"Damping Resistor Voltage Rail 2"  ,

									"LV Current Sensor Voltage Rail 1"  ,
									"LV Current Sensor Voltage Rail 2"  ,

									"HV X-Caps 1 Voltage Rail 1"  ,
									"HV X-Caps 2 Voltage Rail 1"  ,
									"HV X-Caps 1 Voltage Rail 2"  ,
									"HV X-Caps 2 Voltage Rail 2"  ,

									"HV Current Sensor Voltage Rail 1"  ,
									"HV Current Sensor Voltage Rail 2"  ,

									"Blocking Capacitor Voltage Rail 1"  ,
									"Blocking Capacitor Voltage Rail 2"  ,

									"Transformer Snubber Voltage 1 Rail 1"  ,
									"Transformer Snubber Voltage 2 Rail 1"  ,
									"Transformer Snubber Voltage 1 Rail 2"  ,
									"Transformer Snubber Voltage 2 Rail 2"  ,

									"MOSFET RC Snubber Voltage 1 Rail 1"  ,
									"MOSFET RC Snubber Voltage 2 Rail 1"  ,

									"MOSFET RC Snubber Voltage 1 Rail 2"  ,
									"MOSFET RC Snubber Voltage 2 Rail 2"  ,

									"HV Y-Caps Voltage Rail 1"  ,
									"HV Y-Caps Voltage Rail 2"  ,

									"LV FullBridge Snubber Voltage 1 Rail 1"  ,
									"LV FullBridge Snubber Voltage 2 Rail 1"  ,
									"LV FullBridge Snubber Voltage 1 Rail 2"  ,
									"LV FullBridge Snubber Voltage 2 Rail 2"  ,

									"HV Snubber Caps Voltage Rail 1"  ,

									"HV Snubber Caps Voltage Rail 2"  ,

									"Output Ceramic Capacitors Voltage Rail 1"  ,
									"Output Electrolytic Capacitors Voltage Rail 1"  ,
									"Output Y-Cap Voltage Rail 1"  ,

									"Output Ceramic Capacitors Voltage Rail 2"  ,
									"Output Electrolytic Capacitors Voltage Rail 2"  ,
									"Output Y-Cap Voltage Rail 2"  ,

									"HV Voltage Sensor Voltage Rail 1"  ,
									"HV Voltage Sensor Voltage Rail 2"  ,

									"HV CMC Choke Voltage Rail 1"  ,

									"HV CMC Choke Voltage Rail 2"  ,

									'LV Filter X-Cap 1 Voltage'	  				,
                                	'LV Filter X-Cap 2 Voltage'					,
                                 	'LV Filter Elko-Cap Voltage'				,
									'LV Filter Y-Cap Voltage'  			   		,
									"LV Filter DMC Voltage"  ,
									"LV Filter CMC Voltage"  ,
									"LV Filter Output Voltage 1"  ,
									"LV Filter Output Voltage 2"  ,
									"RCD Clamp Transistor Voltage Rail 1"  ,
									"RCD Clamp Bodydiode Voltage Rail 1"  ,
									"RCD Clamp Transistor Voltage Rail 2"  ,
									"RCD Clamp Bodydiode Voltage Rail 2"  ,
									"LV Rectifiers Voltage 1 Rail 1"  ,
									"LV Rectifiers Voltage 2 Rail 1"  ,
									"LV Rectifiers Voltage 1 Rail 2"  ,
									"LV Rectifiers Voltage 2 Rail 2"  ,
									"DC Choke Voltage Rail 1"  ,
									"DC Choke Voltage Rail 2"  ,
									"Freewheeler Switch Voltage 1 Rail 1"  ,
									"Freewheeler Switch Voltage 2 Rail 1"  ,
									"Freewheeler Switch Voltage 1 Rail 2"  ,
									"Freewheeler Switch Voltage 2 Rail 2"  ,
									"Short Circuit Voltage 1 Rail 1"  ,
									"Short Circuit Voltage 2 Rail 1"  ,
									"Short Circuit Voltage 1 Rail 2"  ,
									"Short Circuit Voltage 2 Rail 2"  ,
									"HV Left-Leg HS Voltage 1 Rail 1"  ,
									"HV Left-Leg HS Voltage 2 Rail 1"  ,
									"HV Left-Leg HS Voltage 1 Rail 2"  ,
									"HV Left-Leg HS Voltage 2 Rail 2"  ,
									"HV Right-Leg HS Voltage 1 Rail 1"  ,
									"HV Right-Leg HS Voltage 2 Rail 1"  ,
									"HV Right-Leg HS Voltage 1 Rail 2"  ,
									"HV Right-Leg HS Voltage 2 Rail 2"  ,
									"Transformer Primary Voltage Rail 1"  ,
									"Transformer Secondary Voltage Rail 1"  ,
									"Transformer Flux Rail 1"  ,
									"Transformer Primary Voltage Rail 2"  ,
									"Transformer Secondary Voltage Rail 2"  ,
									"Transformer Flux Rail 2"  ,
									"Pack 1 Voltage"  ,
									"Pack 2 Voltage"  ,
									"Relay Main + Voltage"  ,
									"Relay Main - Voltage"  ,
									"Relay USMmid Voltage"  ,
									"Relay USM + Voltage"  ,
									"Relay USM - Voltage"  ,
									"Relay DCDC 1 Voltage"  ,
									"Relay DCDC 2 Voltage"  ,
									"DC Link Voltage"  ,
									"KL30 Voltage"  ,
									"ENBN DCDC Voltage"  ,
									"ENBN Battery Voltage"  ,
									"LV Filter Input Voltage"  ,
									"LV Filter Output Voltage 3"  ,
									"CISPR Input Voltage"  ,
									"CISPR Output Voltage"  ,
									"Load L_F Voltage"  ,
									"Load L_B Voltage"  ,
									"CTRL Voltage"  ,
									"PECU Voltage"  ,
									"Rbox Voltage"  ,
									#? DISSIPATION RAW MAPPING------------------------------------------------------------------------------------------------------------------------------------
									'Dissipation placeholder'								,
									#? ELECTRIC STATS RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
									'Target LV Voltage'  									,'Target Load Power'  										,
									'Target HV Voltage'  									,'Measured Load Voltage L_F' 								,
									'Measured Load Power L_F' 								,'Measured Load Voltage L_B' 								,
									'Measured Load Power L_B' 								,'Measured HV Voltage Rail 1'								,
									'Measured HV Voltage Rail 2'							,'Measured Load Current L_F' 								,
									'Measured Load Current L_B' 							,'Measured LV Output Voltage' 								,
									'Measured LV Output Current' 							,'Measured HV Current Rail 1'								,
									'Measured HV Current Rail 2'							,'Measured Output Power'  									,
									'Measured Input Power'  								,
									#? TEMP RAW MAPPING----------------------------------------------------------------------------------------------------------------------------------------
									'TEMP placeholder'										,
									#? THERM STATS RAW MAPPING---------------------------------------------------------------------------------------------------------------------------------
									'THERM placeholder'										,
									#? CONTROLLER RAW MAPPING------------------------------------------------------------------------------------------------------------------------------------
									#*Carrier Signals Rail 1---------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Carrier Waveforms 1 Rail 1'					,'PWM Modulator Carrier Waveforms 2 Rail 1'  				,
									#*Duty Cycle Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary Modulator Duty Cycle Rail 1'  		,'PWM Modulator Secondary Modulator Duty Cycle Rail 1'  	,
									#*PWM Signals Rail 1-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs S1 Rail 1'  				,'PWM Modulator Primary PWM Outputs S2 Rail 1'  			,'PWM Modulator Primary PWM Outputs S3 Rail 1'  		,
									'PWM Modulator Primary PWM Outputs S4 Rail 1'  				,'PWM Modulator Secondary PWM Outputs S5 Rail 1'  			,'PWM Modulator Secondary PWM Outputs S6 Rail 1'  		,
									'PWM Modulator Secondary PWM Outputs S7 Rail 1'  			,'PWM Modulator Secondary PWM Outputs S8 Rail 1'  			,'PWM Modulator Auxiliary PWM Outputs Sac Rail 1'  		,
									'PWM Modulator Auxiliary PWM Outputs Sfw Rail 1'  			,'PWM Modulator Auxiliary PWM Outputs Ssc Rail 1'  			,'PWM Modulator Auxiliary PWM Outputs Sdis Rail 1'  	,

         							#Carrier Signals Rail 2---------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Carrier Waveforms 1 Rail 2'					,'PWM Modulator Carrier Waveforms 2 Rail 2'  				,
									#Duty Cycle--------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary Modulator Duty Cycle Rail 2'  		,'PWM Modulator Secondary Modulator Duty Cycle Rail 2'  	,
									#PWM Signals Rail 2-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs S1 Rail 2'  				,'PWM Modulator Primary PWM Outputs S2 Rail 2'  			,'PWM Modulator Primary PWM Outputs S3 Rail 2'  		,
									'PWM Modulator Primary PWM Outputs S4 Rail 2'  				,'PWM Modulator Secondary PWM Outputs S5 Rail 2'  			,'PWM Modulator Secondary PWM Outputs S6 Rail 2'  		,
									'PWM Modulator Secondary PWM Outputs S7 Rail 2'  			,'PWM Modulator Secondary PWM Outputs S8 Rail 2'  			,'PWM Modulator Auxiliary PWM Outputs Sac Rail 2'  		,
									'PWM Modulator Auxiliary PWM Outputs Sfw Rail 2'  			,'PWM Modulator Auxiliary PWM Outputs Ssc Rail 2'  			,'PWM Modulator Auxiliary PWM Outputs Sdis Rail 2'  	,
									#!--------------------------------------------------
									#*LV Voltage  Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured Output Ceramic Capacitors Voltage Rail 1'  		,
         							'Measured LV Filter Output Voltage Rail 1'  				,
                					'Measured ADCs Sampled Signals 1 Rail 1'  					,
									'Measured ADCs Analog Signals 1 Rail 1'  					,'Measured ADCs ADC Signals 1 Rail 1'  					,'Measured HW Protection Comparator Signals 1 Rail 1'  	,
									#*LV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured PSFB LV Current Sensor Current Rail 1'  			,
         							'Measured ADCs Sampled Signals 2 Rail 1'  				,'Measured ADCs Analog Signals 2 Rail 1'  					,
									'Measured ADCs ADC Signals 2 Rail 1'  						,'Measured HW Protection Comparator Signals 2 Rail 1'  	,
									#*HV Voltage Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Filter Voltages 1 Rail 1'  					,'Measured HV Filter Voltages 2 Rail 1'  					,'Measured ADCs Sampled Signals 3 Rail 1'  				,
									'Measured ADCs Analog Signals 3 Rail 1'  					,'Measured ADCs ADC Signals 3 Rail 1'  					,'Measured HW Protection Comparator Signals 3 Rail 1'  	,
									#*HV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Current Sensor Current Rail 1'  				,'Measured ADCs Sampled Signals 4 Rail 1'  				,'Measured ADCs ADC Signals 4 Rail 1'  					,
									#*CT Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured CT Current Sensor Current Rail 1'  				,'Measured ADCs Sampled Signals 5 Rail 1' 					, 'Measured ADCs ADC Signals 5 Rail 1'  					,
									#*Digital Raw Values Rail 1------------------------------------------------------------------------------------------------------------------------------------------
									'Measured ADCs Sensors Digital Values Vo Rail 1'			,'Measured ADCs Sensors Digital Values Io Rail 1'  		,'Measured ADCs Sensors Digital Values Vin Rail 1'  		,
									'Measured ADCs Sensors Digital Values Iin Rail 1'  		,'Measured ADCs Sensors Digital Values CT Rail 1' 			,'Measured ADCs Digital Reference Rail 1'  				,

         							#LV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured Output Ceramic Capacitors Voltage Rail 2'  		,'Measured LV Filter Output Voltage Rail 2'  				,'Measured ADCs Sampled Signals 1 Rail 2'  				,
									'Measured ADCs Analog Signals 1 Rail 2'  					,'Measured ADCs ADC Signals 1 Rail 2'  					,'Measured HW Protection Comparator Signals 1 Rail 2'  	,
									#LV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured PSFB LV Current Sensor Current Rail 2'  			,'Measured ADCs Sampled Signals 2 Rail 2'  				,'Measured ADCs Analog Signals 2 Rail 2'  					,
									'Measured ADCs ADC Signals 2 Rail 2'  						,'Measured HW Protection Comparator Signals 2 Rail 2'  	,
									#HV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Filter Voltages 1 Rail 2'  					,'Measured HV Filter Voltages 2 Rail 2'  					,'Measured ADCs Sampled Signals 3 Rail 2'  				,
									'Measured ADCs Analog Signals 3 Rail 2'  					,'Measured ADCs ADC Signals 3 Rail 2'  					,'Measured HW Protection Comparator Signals 3 Rail 2'  	,
									#HV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured HV Current Sensor Current Rail 2'  				,'Measured ADCs Sampled Signals 4 Rail 2'  				,'Measured ADCs ADC Signals 4 Rail 2'  					,
									#CT Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'Measured CT Current Sensor Current Rail 2'  				,'Measured ADCs Sampled Signals 5 Rail 2' 					, 'Measured ADCs ADC Signals 5 Rail 2'  					,
									#Digital Raw Values Rail 2------------------------------------------------------------------------------------------------------------------------------------------
									'Measured ADCs Sensors Digital Values Vo Rail 2'			,'Measured ADCs Sensors Digital Values Io Rail 2'  		,'Measured ADCs Sensors Digital Values Vin Rail 2'  		,
									'Measured ADCs Sensors Digital Values Iin Rail 2'  		,'Measured ADCs Sensors Digital Values CT Rail 2' 			,'Measured ADCs Digital Reference Rail 2'  				,
									#!--------------------------------------------------
         							#*LV Voltage Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 1 Rail 1'  							,'ADCs S-and-H Voltages 1 Rail 1'  						,'ADCs Sampled Voltages 1 Rail 1'  						,
									#*LV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 2 Rail 1'  							,'ADCs S-and-H Voltages 2 Rail 1'  						,'ADCs Sampled Voltages 2 Rail 1'  						,
									#*HV Voltage Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 3 Rail 1'  							,'ADCs S-and-H Voltages 3 Rail 1'  						,'ADCs Sampled Voltages 3 Rail 1'  						,
									#*HV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 4 Rail 1'  							,'ADCs S-and-H Voltages 4 Rail 1'  						,'ADCs Sampled Voltages 4 Rail 1'  						,
									#*CT Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 5 Rail 1'  							,'ADCs S-and-H Voltages 5 Rail 1'  						,'ADCs Sampled Voltages 5 Rail 1'  						,
									#*Charging Currents Rail 1-------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Charging Currents 1 Rail 1'  						,'ADCs Charging Currents 2 Rail 1'  						,'ADCs Charging Currents 3 Rail 1'  						,
									'ADCs Charging Currents 4 Rail 1'  						,'ADCs Charging Currents 5 Rail 1'  						,'ADCs Charging Currents 6 Rail 1'  						,
									'ADCs Charging Currents 7 Rail 1'  						,'ADCs Charging Currents 8 Rail 1'  						,'ADCs Charging Currents 9 Rail 1'							,
									'ADCs Charging Currents 10 Rail 1'							,
									#*Sample Triggers Rail 1---------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Sampling Triggers 1 Rail 1'  						,'ADCs Sampling Triggers 2 Rail 1'  						,'ADCs Sampling Triggers 3 Rail 1'  						,
									'ADCs Sampling Triggers 4 Rail 1'  						,'ADCs Sampling Triggers 5 Rail 1'							,

									#LV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 1 Rail 2'  							,'ADCs S-and-H Voltages 1 Rail 2'  						,'ADCs Sampled Voltages 1 Rail 2'  						,
									#LV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 2 Rail 2'  							,'ADCs S-and-H Voltages 2 Rail 2'  						,'ADCs Sampled Voltages 2 Rail 2'  						,
									#HV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 3 Rail 2'  							,'ADCs S-and-H Voltages 3 Rail 2'  						,'ADCs Sampled Voltages 3 Rail 2'  						,
									#HV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 4 Rail 2'  							,'ADCs S-and-H Voltages 4 Rail 2'  						,'ADCs Sampled Voltages 4 Rail 2'  						,
									#CT Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs ADC Pin Voltages 5 Rail 2'  							,'ADCs S-and-H Voltages 5 Rail 2'  						,'ADCs Sampled Voltages 5 Rail 2'  						,
									#Charging Currents Rail 2-------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Charging Currents 1 Rail 2'  						,'ADCs Charging Currents 2 Rail 2'  						,'ADCs Charging Currents 3 Rail 2'  						,
									'ADCs Charging Currents 4 Rail 2'  						,'ADCs Charging Currents 5 Rail 2'  						,'ADCs Charging Currents 6 Rail 2'  						,
									'ADCs Charging Currents 7 Rail 2'  						,'ADCs Charging Currents 8 Rail 2'  						,'ADCs Charging Currents 9 Rail 2'							,
									'ADCs Charging Currents 10 Rail 2'							,
									#Sample Triggers Rail 2---------------------------------------------------------------------------------------------------------------------------------------------
									'ADCs Sampling Triggers 1 Rail 2'  						,'ADCs Sampling Triggers 2 Rail 2'  						,'ADCs Sampling Triggers 3 Rail 2'  						,
									'ADCs Sampling Triggers 4 Rail 2'  						,'ADCs Sampling Triggers 5 Rail 2'							,
									#!--------------------------------------------------
         							#*LV Voltage Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'PSFB Output Ceramic Capacitors Voltage Rail 1'  			,
         							'LV Filter Input Voltage Sampling Rail 1'  				,'LV Filter Output Voltage Sampling Rail 1'  				,
									#*LV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'LV Current Sensor Current Sampling Rail 1'	  			,
									#*HV Voltage Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Filter X-Caps Voltages 1 Sampling Rail 1'  			,'HV Filter X-Caps Voltages 2 Sampling Rail 1'  			,
									#*HV Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Current Sensor Current Sampling Rail 1'	  			,
									#*CT Current Rail 1--------------------------------------------------------------------------------------------------------------------------------------------------
									'CT Current Sensor Current Sampling Rail 1'	  			,
									#*PWM Signals Rail 1-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs 1 Rail 1'  				,'PWM Modulator Primary PWM Outputs 2 Rail 1'  			,'PWM Modulator Primary PWM Outputs 3 Rail 1'  			,
									'PWM Modulator Primary PWM Outputs 4 Rail 1'  				,'PWM Modulator Secondary PWM Outputs 1 Rail 1'  			,'PWM Modulator Secondary PWM Outputs 2 Rail 1'  			,
									'PWM Modulator Secondary PWM Outputs 3 Rail 1'  			,'PWM Modulator Secondary PWM Outputs 4 Rail 1'  			,
									#*Sample Triggers Rail 1---------------------------------------------------------------------------------------------------------------------------------------------
									'Sample Trigger 1 Rail 1'  								,'Sample Trigger 2 Rail 1'  								,'Sample Trigger 3 Rail 1'  								,
									'Sample Trigger 4 Rail 1'  								,'Sample Trigger 5 Rail 1'									,
									#*Controller Update Rail 1-------------------------------------------------------------------------------------------------------------------------------------------
									'Controller Update Rail 1'  								,

									#LV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'PSFB Output Ceramic Capacitors Voltage Rail 2'  			,'LV Filter Input Voltage Sampling Rail 2'  				,'LV Filter Output Voltage Sampling Rail 2'  				,
									#LV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'LV Current Sensor Current Sampling Rail 2'	  			,
									#HV Voltage Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Filter X-Caps Voltages 1 Sampling Rail 2'  			,'HV Filter X-Caps Voltages 2 Sampling Rail 2'  			,
									#HV Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'HV Current Sensor Current Sampling Rail 2'	  			,
									#CT Current Rail 2--------------------------------------------------------------------------------------------------------------------------------------------------
									'CT Current Sensor Current Sampling Rail 2'	  			,
									#PWM Signals Rail 2-------------------------------------------------------------------------------------------------------------------------------------------------
									'PWM Modulator Primary PWM Outputs 1 Rail 2'  				,'PWM Modulator Primary PWM Outputs 2 Rail 2'  			,'PWM Modulator Primary PWM Outputs 3 Rail 2'  			,
									'PWM Modulator Primary PWM Outputs 4 Rail 2'  				,'PWM Modulator Secondary PWM Outputs 1 Rail 2'  			,'PWM Modulator Secondary PWM Outputs 2 Rail 2'  			,
									'PWM Modulator Secondary PWM Outputs 3 Rail 2'  			,'PWM Modulator Secondary PWM Outputs 4 Rail 2'  			,
									#Sample Triggers Rail 2---------------------------------------------------------------------------------------------------------------------------------------------
									'Sample Trigger 1 Rail 2'  								,'Sample Trigger 2 Rail 2'  								,'Sample Trigger 3 Rail 2'  								,
									'Sample Trigger 4 Rail 2'  								,'Sample Trigger 5 Rail 2'									,
									#Controller Update Rail 2-------------------------------------------------------------------------------------------------------------------------------------------
									'Controller Update Rail 2'  								,
									#!--------------------------------------------------
         							#*Measured Signals Rail 1--------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Measured Signals Vo Rail 1'					,
         							'SW Protection Measured Signals Io Rail 1'					,
                					'SW Protection Measured Signals Vin Rail 1'					,
									'SW Protection Measured Signals Iin Rail 1'					,
         							'SW Protection Measured Signals Io Rail 2'					,
         							'SW Protection Measured Signals Vin Rail 2'					,
         							'SW Protection Measured Signals Iin Rail 2'					,
         							'SW Protection Measured Signals Vo Rail 2'					,

         							'SW Protection Upper Thresholds X1'							,
         							'SW Protection Upper Thresholds X2'							,
         							'SW Protection Upper Thresholds Vo Rail 1'					,
                					'SW Protection Upper Thresholds Io Rail 1'					,
									'SW Protection Upper Thresholds Vin Rail 1'					,
         							'SW Protection Upper Thresholds Iin Rail 1'					,

                     				'SW Protection Lower Thresholds Vo X1'						,
                     				'SW Protection Lower Thresholds Vo X2'						,
                     				'SW Protection Lower Thresholds Vo Rail 1'					,
									'SW Protection Lower Thresholds Io Rail 1'					,
         							'SW Protection Lower Thresholds Vin Rail 1'					,
                					'SW Protection Lower Thresholds Iin Rail 1'					,

									#*Fault Counters Rail 1----------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Fault Counters Vo Rail 1'					,
         							'SW Protection Fault Counters Io Rail 1'					,
                					'SW Protection Fault Counters Vin Rail 1'					,
									'SW Protection Fault Counters Iin Rail 1'					,
									'SW Protection Fault Counters Io Rail 2'					,
									'SW Protection Fault Counters Vin Rail 2'					,
									'SW Protection Fault Counters Iin Rail 2'					,
									'SW Protection Fault Counters Vo Rail 2'					,

									#*Comparators Triggers Rail 1----------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Fault Comparators VoH Rail 1'				,
         							'SW Protection Fault Comparators VoL Rail 1'				,
                					'SW Protection Fault Comparators IoH Rail 1'				,
									'SW Protection Fault Comparators IoL Rail 1'				,
         							'SW Protection Fault Comparators VinH Rail 1'				,
                					'SW Protection Fault Comparators VinL Rail 1'				,
									'SW Protection Fault Comparators IinH Rail 1'				,
         							'SW Protection Fault Comparators IinL Rail 1'				,
									#Comparators Triggers Rail 2----------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Fault Comparators VoH Rail 2'				,
         							'SW Protection Fault Comparators VoL Rail 2'				,
                					'SW Protection Fault Comparators IoH Rail 2'				,
									'SW Protection Fault Comparators IoL Rail 2'				,
         							'SW Protection Fault Comparators VinH Rail 2'				,
                					'SW Protection Fault Comparators VinL Rail 2'				,
									'SW Protection Fault Comparators IinH Rail 2'				,
         							'SW Protection Fault Comparators IinL Rail 2'				,
									#*Disable Latches Rail 1---------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Disable Latches Vo Rail 1'					,
         							'SW Protection Disable Latches Io Rail 1'					,
                					'SW Protection Disable Latches Vin Rail 1'					,
									'SW Protection Disable Latches Iin Rail 1'					,
									#Disable Latches Rail 2---------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Disable Latches Vo Rail 2'					,
         							'SW Protection Disable Latches Io Rail 2'					,
                					'SW Protection Disable Latches Vin Rail 2'					,
									'SW Protection Disable Latches Iin Rail 2'					,
									#*Enable Rail 1------------------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Enable Signal Rail 1'						,
									#Enable Rail 2------------------------------------------------------------------------------------------------------------------------------------------------------
									'SW Protection Enable Signal Rail 2'						,
									#!--------------------------------------------------
         							#*Output Voltage Rail 1----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage Ref Rail 1'					,'HW Protection Output Voltage In Rail 1'					,'HW Protection Output Voltage VH Rail 1'					,
									'HW Protection Output Voltage VL Rail 1'					,
									#*Positive Output Current Rail 1-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Positive Output Current Ref Rail 1'			,'HW Protection Positive Output Current In Rail 1'			,'HW Protection Positive Output Current VH Rail 1'			,
									'HW Protection Positive Output Current VL Rail 1'			,
									#*Negative Output Current Rail 1-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Negative Output Current Ref Rail 1'			,'HW Protection Negative Output Current In Rail 1'			,'HW Protection Negative Output Current VH Rail 1'			,
									'HW Protection Negative Output Current VL Rail 1'			,
									#*Input Voltage Rail 1-----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Input Voltage Ref Rail 1'					,'HW Protection Input Voltage In Rail 1'					,'HW Protection Input Voltage VH Rail 1'					,
									'HW Protection Input Voltage VL Rail 1'					,
									#*Triggers Rail 1----------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage 3 Rail 1'					,'HW Protection Positive Output Current 3 Rail 1'			,'HW Protection Negative Output Current 3 Rail 1'			,
									'HW Protection Input Voltage 3 Rail 1'						,
									#*States Rail 1------------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Latch State Rail 1'							,'HW Protection Reset State Rail 1',

									#Output Voltage Rail 2----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage Ref Rail 2'					,'HW Protection Output Voltage In Rail 2'					,'HW Protection Output Voltage VH Rail 2'					,
									'HW Protection Output Voltage VL Rail 2'					,
									#Positive Output Current Rail 2-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Positive Output Current Ref Rail 2'			,'HW Protection Positive Output Current In Rail 2'			,'HW Protection Positive Output Current VH Rail 2'			,
									'HW Protection Positive Output Current VL Rail 2'			,
									#Negative Output Current Rail 2-------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Negative Output Current Ref Rail 2'			,'HW Protection Negative Output Current In Rail 2'			,'HW Protection Negative Output Current VH Rail 2'			,
									'HW Protection Negative Output Current VL Rail 2'			,
									#Input Voltage Rail 2-----------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Input Voltage Ref Rail 2'					,'HW Protection Input Voltage In Rail 2'					,'HW Protection Input Voltage VH Rail 2'					,
									'HW Protection Input Voltage VL Rail 2'					,
									#Triggers Rail 2----------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Output Voltage 3 Rail 2'					,'HW Protection Positive Output Current 3 Rail 2'			,'HW Protection Negative Output Current 3 Rail 2'			,
									'HW Protection Input Voltage 3 Rail 2'						,
									#States Rail 2------------------------------------------------------------------------------------------------------------------------------------------------------
									'HW Protection Latch State Rail 2'							,'HW Protection Reset State Rail 2'

									]
DCDC_DUAL_pmap_plt				=	[														# Dual Rails DCDC plots mapping
										#?	['TITLE OF FIGURE'			                      ,'CURRENT 1 IN RAW MAPPING'	                     ,'CURRENT 2 IN RAW MAPPING'			          ,'VOLTAGE 1 IN RAW MAPPING'		                 ,'VOLTAGE 2 IN RAW MAPPING'			          ]
										#-----------------------------------------------------------------------------------------------------------------------------
										["CT Trafo Primary"                                   ,"CT Trafo Primary Current Rail 1"                 ,"CT Trafo Primary Current Rail 2"               ,"CT Trafo Primary Voltage Rail 1"                 ,"CT Trafo Primary Voltage Rail 2"               ],
										["CT Trafo Secondary"                                 ,"CT Trafo Secondary Current Rail 1"               ,"CT Trafo Secondary Current Rail 2"             ,"CT Trafo Secondary Voltage Rail 1"               ,"CT Trafo Secondary Voltage Rail 2"             ],
										["Choke RC Snubber Capacitor"                         ,"Choke RC Snubber Capacitor Current Rail 1"       ,"Choke RC Snubber Capacitor Current Rail 2"     ,"Choke RC Snubber Voltage 1 Rail 1"               ,"Choke RC Snubber Voltage 1 Rail 2"             ],
										["Choke RC Snubber Resistance"                        ,"Choke RC Snubber Resistance Current Rail 1"      ,"Choke RC Snubber Resistance Current Rail 2"    ,"Choke RC Snubber Voltage 2 Rail 1"               ,"Choke RC Snubber Voltage 2 Rail 2"             ],
										["Choke RC Snubber Parallel Resistance"               ,"Choke RC Snubber Par Res Current Rail 1"         ,"Choke RC Snubber Par Res Current Rail 2"       ,"Choke RC Snubber Voltage 3 Rail 1"               ,"Choke RC Snubber Voltage 3 Rail 2"             ],
										["RCD Clamp Capacitor"                                ,"RCD Clamp Capacitor Current Rail 1"              ,"RCD Clamp Capacitor Current Rail 2"            ,"RCD Clamp Capacitor Voltage Rail 1"              ,"RCD Clamp Capacitor Voltage Rail 2"            ],
										["RCD Clamp Resistance"                               ,"RCD Clamp Resistance Current Rail 1"             ,"RCD Clamp Resistance Current Rail 2"           ,"RCD Clamp Resistance Voltage Rail 1"             ,"RCD Clamp Resistance Voltage Rail 2"           ],
										["Freewheeler Blocking Cap"                           ,"Freewheeler Blocking Cap Current Rail 1"         ,"Freewheeler Blocking Cap Current Rail 2"       ,"Freewheeler Blocking Cap Voltage Rail 1"         ,"Freewheeler Blocking Cap Voltage Rail 2"       ],
										["Freewheeler Resistor"                               ,"Freewheeler Resistor Current Rail 1"             ,"Freewheeler Resistor Current Rail 2"           ,"Freewheeler Resistor Voltage Rail 1"             ,"Freewheeler Resistor Voltage Rail 2"           ],
										["Freewheeler Impedance Cap"                          ,"Freewheeler Impedance Cap Current Rail 1"        ,"Freewheeler Impedance Cap Current Rail 2"      ,"Freewheeler Impedance Cap Voltage Rail 1"        ,"Freewheeler Impedance Cap Voltage Rail 2"      ],
										["Damping Resistor"                                   ,"Damping Resistor Current Rail 1"                 ,"Damping Resistor Current Rail 2"               ,"Damping Resistor Voltage Rail 1"                 ,"Damping Resistor Voltage Rail 2"               ],
										["LV Current Sensor"                                  ,"LV Current Sensor Current Rail 1"                ,"LV Current Sensor Current Rail 2"              ,"LV Current Sensor Voltage Rail 1"                ,"LV Current Sensor Voltage Rail 2"              ],
										["HV X-Caps 1"                                        ,"HV X-Caps 1 Current Rail 1"                      ,"HV X-Caps 1 Current Rail 2"                    ,"HV X-Caps 1 Voltage Rail 1"                      ,"HV X-Caps 1 Voltage Rail 2"                    ],
										["HV X-Caps 2"                                        ,"HV X-Caps 2 Current Rail 1"                      ,"HV X-Caps 2 Current Rail 2"                    ,"HV X-Caps 2 Voltage Rail 1"                      ,"HV X-Caps 2 Voltage Rail 2"                    ],
										["HV Current Sensor"                                  ,"HV Current Sensor Current Rail 1"                ,"HV Current Sensor Current Rail 2"              ,"HV Current Sensor Voltage Rail 1"                ,"HV Current Sensor Voltage Rail 2"              ],
										["Blocking Capacitor"                                 ,"Blocking Capacitor Current Rail 1"               ,"Blocking Capacitor Current Rail 2"             ,"Blocking Capacitor Voltage Rail 1"               ,"Blocking Capacitor Voltage Rail 2"             ],
										["Transformer Snubber Cap"                            ,"Transformer Snubber Cap Current Rail 1"          ,"Transformer Snubber Cap Current Rail 2"        ,"Transformer Snubber Voltage 1 Rail 1"            ,"Transformer Snubber Voltage 1 Rail 2"          ],
										["Transformer Snubber Res"                            ,"Transformer Snubber Res Current Rail 1"          ,"Transformer Snubber Res Current Rail 2"        ,"Transformer Snubber Voltage 2 Rail 1"            ,"Transformer Snubber Voltage 2 Rail 2"          ],
										["MOSFET RC Snubber Cap"                              ,"MOSFET RC Snubber Cap Current Rail 1"            ,"MOSFET RC Snubber Cap Current Rail 2"          ,"MOSFET RC Snubber Voltage 1 Rail 1"              ,"MOSFET RC Snubber Voltage 1 Rail 2"            ],
										["MOSFET RC Snubber Res"                              ,"MOSFET RC Snubber Res Current Rail 1"            ,"MOSFET RC Snubber Res Current Rail 2"          ,"MOSFET RC Snubber Voltage 2 Rail 1"              ,"MOSFET RC Snubber Voltage 2 Rail 2"            ],
										["HV Y-Caps"                                          ,"HV Y-Caps Current Rail 1"                        ,"HV Y-Caps Current Rail 2"                      ,"HV Y-Caps Voltage Rail 1"                        ,"HV Y-Caps Voltage Rail 2"                      ],
										["LV FullBridge Snubber Cap"                          ,"LV FullBridge Snubber Cap Current Rail 1"        ,"LV FullBridge Snubber Cap Current Rail 2"      ,"LV FullBridge Snubber Voltage 1 Rail 1"          ,"LV FullBridge Snubber Voltage 1 Rail 2"        ],
										["LV FullBridge Snubber Res"                          ,"LV FullBridge Snubber Res Current Rail 1"        ,"LV FullBridge Snubber Res Current Rail 2"      ,"LV FullBridge Snubber Voltage 2 Rail 1"          ,"LV FullBridge Snubber Voltage 2 Rail 2"        ],
										["HV Snubber Caps"                                    ,"HV Snubber Caps Current Rail 1"                  ,"HV Snubber Caps Current Rail 2"                ,"HV Snubber Caps Voltage Rail 1"                  ,"HV Snubber Caps Voltage Rail 2"                ],
										["Output Ceramic Capacitors"                          ,"Output Ceramic Capacitors Current Rail 1"        ,"Output Ceramic Capacitors Current Rail 2"      ,"Output Ceramic Capacitors Voltage Rail 1"        ,"Output Ceramic Capacitors Voltage Rail 2"      ],
										["Output Electrolytic Capacitors"                     ,"Output Electrolytic Capacitors Current Rail 1"   ,"Output Electrolytic Capacitors Current Rail 2" ,"Output Electrolytic Capacitors Voltage Rail 1"   ,"Output Electrolytic Capacitors Voltage Rail 2" ],
										["Output Y-Cap"                                       ,"Output Y-Cap Current Rail 1"                     ,"Output Y-Cap Current Rail 2"                   ,"Output Y-Cap Voltage Rail 1"                     ,"Output Y-Cap Voltage Rail 2"                   ],
										["HV Voltage Sensor"                                  ,"HV Voltage Sensor Current Rail 1"                ,"HV Voltage Sensor Current Rail 2"              ,"HV Voltage Sensor Voltage Rail 1"                ,"HV Voltage Sensor Voltage Rail 2"              ],
										["HV CMC Choke Current"                               ,"HV CMC Choke Current Rail 1"                     ,"HV CMC Choke Current Rail 2"                   ,"HV CMC Choke Voltage Rail 1"                     ,"HV CMC Choke Voltage Rail 2"                   ],
										["LV Filter X-Cap"                                    ,'LV Filter X-Cap 1 Current'                       ,'LV Filter X-Cap 2 Current'                     ,'LV Filter X-Cap 1 Voltage'                       ,'LV Filter X-Cap 2 Voltage'                     ],
										["RCD Clamp Transistor"                               ,"RCD Clamp Transistor Current Rail 1"             ,"RCD Clamp Transistor Current Rail 2"           ,"RCD Clamp Transistor Voltage Rail 1"             ,"RCD Clamp Transistor Voltage Rail 2"           ],
										["RCD Clamp Bodydiode"                                ,"RCD Clamp Bodydiode Current Rail 1"              ,"RCD Clamp Bodydiode Current Rail 2"            ,"RCD Clamp Bodydiode Voltage Rail 1"              ,"RCD Clamp Bodydiode Voltage Rail 2"            ],
										["LV Rectifiers 1"                                    ,"LV Rectifiers Current 1 Rail 1"                  ,"LV Rectifiers Current 1 Rail 2"                ,"LV Rectifiers Voltage 1 Rail 1"                  ,"LV Rectifiers Voltage 1 Rail 2"                ],
										["LV Rectifiers 2"                                    ,"LV Rectifiers Current 2 Rail 1"                  ,"LV Rectifiers Current 2 Rail 2"                ,"LV Rectifiers Voltage 2 Rail 1"                  ,"LV Rectifiers Voltage 2 Rail 2"                ],
										["DC Choke"                                           ,"DC Choke Current Rail 1"                         ,"DC Choke Current Rail 2"                       ,"DC Choke Voltage Rail 1"                         ,"DC Choke Voltage Rail 2"                       ],
										["Freewheeler Switch 1"                               ,"Freewheeler Switch Current 1 Rail 1"             ,"Freewheeler Switch Current 1 Rail 2"           ,"Freewheeler Switch Voltage 1 Rail 1"             ,"Freewheeler Switch Voltage 1 Rail 2"           ],
										["Freewheeler Switch 2"                               ,"Freewheeler Switch Current 2 Rail 1"             ,"Freewheeler Switch Current 2 Rail 2"           ,"Freewheeler Switch Voltage 2 Rail 1"             ,"Freewheeler Switch Voltage 2 Rail 2"           ],
										["Short Circuit 1"                                    ,"Short Circuit Current 1 Rail 1"                  ,"Short Circuit Current 1 Rail 2"                ,"Short Circuit Voltage 1 Rail 1"                  ,"Short Circuit Voltage 1 Rail 2"                ],
										["Short Circuit 2"                                    ,"Short Circuit Current 2 Rail 1"                  ,"Short Circuit Current 2 Rail 2"                ,"Short Circuit Voltage 2 Rail 1"                  ,"Short Circuit Voltage 2 Rail 2"                ],
										["HV Left-Leg HS 1"                                   ,"HV Left-Leg HS Current 1 Rail 1"                 ,"HV Left-Leg HS Current 1 Rail 2"               ,"HV Left-Leg HS Voltage 1 Rail 1"                 ,"HV Left-Leg HS Voltage 1 Rail 2"               ],
										["HV Left-Leg HS 2"                                   ,"HV Left-Leg HS Current 2 Rail 1"                 ,"HV Left-Leg HS Current 2 Rail 2"               ,"HV Left-Leg HS Voltage 2 Rail 1"                 ,"HV Left-Leg HS Voltage 2 Rail 2"               ],
										["HV Right-Leg HS 1"                                  ,"HV Right-Leg HS Current 1 Rail 1"                ,"HV Right-Leg HS Current 1 Rail 2"              ,"HV Right-Leg HS Voltage 1 Rail 1"                ,"HV Right-Leg HS Voltage 1 Rail 2"              ],
										["HV Right-Leg HS 2"                                  ,"HV Right-Leg HS Current 2 Rail 1"                ,"HV Right-Leg HS Current 2 Rail 2"              ,"HV Right-Leg HS Voltage 2 Rail 1"                ,"HV Right-Leg HS Voltage 2 Rail 2"              ],
										["Transformer Primary"                                ,"Transformer Primary Current Rail 1"              ,"Transformer Primary Current Rail 2"            ,"Transformer Primary Voltage Rail 1"              ,"Transformer Primary Voltage Rail 2"            ],
										["Transformer Secondary"                              ,"Transformer Secondary Current Rail 1"            ,"Transformer Secondary Current Rail 2"          ,"Transformer Secondary Voltage Rail 1"            ,"Transformer Secondary Voltage Rail 2"          ],
										["Transformer Magnetizing"                            ,"Transformer Magnetizing Current Rail 1"          ,"Transformer Magnetizing Current Rail 2"        ,"Transformer Flux Rail 1"                         ,"Transformer Flux Rail 2"                       ],
          								["Pack"                           					  ,"Pack 1 Current"         						 ,"Pack 2 Current"       						  ,"Pack 1 Voltage"                         		 ,"Pack 2 Voltage"                      		  ],
										["Relay Main"                           			  ,"Relay Main + Current"          					 ,"Relay Main - Current"       				      ,"Relay Main + Voltage"                            ,"Relay Main - Voltage"                          ],
										["Relay USM"                           				  ,"Relay USM + Current"         					 ,"Relay USM - Current"        				      ,"Relay USM + Voltage"                             ,"Relay USM - Voltage"                           ],
										["Relay DCDC"                           			  ,"Relay DCDC 1 Current"          					 ,"Relay DCDC 2 Current"        				  ,"Relay DCDC 1 Voltage"                            ,"Relay DCDC 2 Voltage"                          ],
										["ENBN DCDC"                           				  ,"ENBN DCDC Current"          					 ,"ENBN DCDC Voltage"                                                       																		  ],
										["ENBN Battery"                           		      ,"ENBN Battery Current"        				     ,"ENBN Battery Voltage"                          																									  ],
										["LV Filter"                           				  ,"LV Filter Input Current"          				 ,"LV Filter Output Current"         			  ,"LV Filter Input Voltage"                         ,"LV Filter Output Voltage 3"                    ],
										["CISPR"                           					  ,"CISPR Input Current"          					 ,"CISPR Output Current"        				  ,"CISPR Input Voltage"                             ,"CISPR Output Voltage"                          ],
										["Load"                           					  ,"Load L_F Current"          						 ,"Load L_B Current"        					  ,"Load L_F Voltage"                                ,"Load L_B Voltage"                              ],
										["LV Filter Rbus"                           		  ,"LV Filter Output Current RbPlus"          		 ,"LV Filter Output Current RbMinus"        	  ,"LV Filter Output Voltage 1"                      ,"LV Filter Output Voltage 2"                    ],
										["Relay USMmid"                                       ,"Relay USMmid Current"                            ,"Relay USMmid Voltage"                          																									  ],
										["DC Link"                                            ,"DC Link Current"                                 ,"DC Link Voltage"                               																									  ],
										["KL30"                                               ,"KL30 Current"                                    ,"KL30 Voltage"                                  																									  ],
										["CTRL"                                               ,"CTRL Current"                                    ,"CTRL Voltage"                                  																									  ],
										["PECU"                                               ,"PECU Current"                                    ,"PECU Voltage"                                  																									  ],
										["Rbox"                                               ,"Rbox Current"                                    ,"Rbox Voltage"                                  																									  ],
										["LV Filter Elko-Cap"                                 ,"LV Filter Elko-Cap Current"                      ,"LV Filter Elko-Cap Voltage"					  																									  ],
          								["LV Filter Y-Cap"                                    ,"LV Filter Y-Cap Current"                         ,"LV Filter Y-Cap Voltage"        			      																									  ],
										["LV Filter DMC"                                      ,"LV Filter DMC Current"                           ,"LV Filter DMC Voltage"          			      																									  ],
										["LV Filter CMC"                                      ,"LV Filter CMC Current"                           ,"LV Filter CMC Voltage"          			      																									  ]

													]
DCDC_DUAL_Constants				=	[														# DCDC Constants

                             			['Measured Load Voltage L_F' 		, '[ V ]'	],
							 			['Measured Load Power L_F' 			, '[ W ]'	],
							 			['Measured Load Voltage L_B' 		, '[ V ]'	],
							 			['Measured Load Power L_B' 			, '[ W ]'	],
							 			['Measured Load Current L_F' 		, '[ A ]'	],
							 			['Measured Load Current L_B' 		, '[ A ]'	],
										['Target LV Voltage'				, '[ V ]'	],
          								['Measured LV Output Voltage'		, '[ V ]'	],
                  						['Target HV Voltage'				, '[ V ]'	],
          								['Measured LV Output Current'		, '[ A ]'	],
                  						['Target Load Power'				, '[ W ]'	],
                  						['Measured Output Power'			, '[ W ]'	],
                        				['Measured Input Power'    			, '[ W ]'	],
                        				['Measured HV Voltage Rail 1'		, '[ V ]'	],
                        				['Measured HV Voltage Rail 2'		, '[ V ]'	],
                            			['Measured HV Current Rail 1'		, '[ A ]'	],
										['Measured HV Current Rail 2'		, '[ A ]'	]

									]
DCDC_DUAL_Ctrl_plt				=	[
    								#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									['PWM' ,'Measurments','ADC','Sampling','SW Protection','HW Protection'],#
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#PWM
										['Carrier Signals' 				,['PWM Modulator Carrier Waveforms 1 Rail 1'				,'PWM Modulator Carrier Waveforms 2 Rail 1'
                                   										, 'PWM Modulator Carrier Waveforms 1 Rail 2'				,'PWM Modulator Carrier Waveforms 2 Rail 2'		]	,['[ - ]']],

          								['PWM Modulator Duty Cycle' 	,['PWM Modulator Primary Modulator Duty Cycle Rail 1'		,'PWM Modulator Secondary Modulator Duty Cycle Rail 1'
                                                 						, 'PWM Modulator Primary Modulator Duty Cycle Rail 2'		,'PWM Modulator Secondary Modulator Duty Cycle Rail 2'			]	,['[ - ]']],

          								['PWM Signal'					,['PWM Modulator Primary PWM Outputs S1 Rail 1'				,'PWM Modulator Primary PWM Outputs S2 Rail 1'			,'PWM Modulator Primary PWM Outputs S3 Rail 1'
									                     				, 'PWM Modulator Primary PWM Outputs S4 Rail 1'				,'PWM Modulator Secondary PWM Outputs S5 Rail 1'		,'PWM Modulator Secondary PWM Outputs S6 Rail 1'
																		, 'PWM Modulator Secondary PWM Outputs S7 Rail 1'			,'PWM Modulator Secondary PWM Outputs S8 Rail 1'		,'PWM Modulator Auxiliary PWM Outputs Sac Rail 1'
									                         			, 'PWM Modulator Auxiliary PWM Outputs Sfw Rail 1'			,'PWM Modulator Auxiliary PWM Outputs Ssc Rail 1'		,'PWM Modulator Auxiliary PWM Outputs Sdis Rail 1'

                  														, 'PWM Modulator Primary PWM Outputs S1 Rail 2'			    ,'PWM Modulator Primary PWM Outputs S2 Rail 2'			,'PWM Modulator Primary PWM Outputs S3 Rail 2'
									                     				, 'PWM Modulator Primary PWM Outputs S4 Rail 2'				,'PWM Modulator Secondary PWM Outputs S5 Rail 2'		,'PWM Modulator Secondary PWM Outputs S6 Rail 2'
																		, 'PWM Modulator Secondary PWM Outputs S7 Rail 2'			,'PWM Modulator Secondary PWM Outputs S8 Rail 2'		,'PWM Modulator Auxiliary PWM Outputs Sac Rail 2'
									                         			, 'PWM Modulator Auxiliary PWM Outputs Sfw Rail 2'			,'PWM Modulator Auxiliary PWM Outputs Ssc Rail 2'		,'PWM Modulator Auxiliary PWM Outputs Sdis Rail 2'	]	,['[ - ]']],
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#Measurments
										['LV Voltage'					,['Measured Output Ceramic Capacitors Voltage Rail 1'		,'Measured LV Filter Output Voltage Rail 1'			,'Measured ADCs Sampled Signals 1 Rail 1'
									                     				,'Measured ADCs Analog Signals 1 Rail 1'					,'Measured ADCs ADC Signals 1 Rail 1'					,'Measured HW Protection Comparator Signals 1 Rail 1'

                 														,'Measured Output Ceramic Capacitors Voltage Rail 2'		,'Measured LV Filter Output Voltage Rail 2'			,'Measured ADCs Sampled Signals 1 Rail 2'
									                     				,'Measured ADCs Analog Signals 1 Rail 2'					,'Measured ADCs ADC Signals 1 Rail 2'					,'Measured HW Protection Comparator Signals 1 Rail 2']	,['[ V ]']],

										['LV Current'					,['Measured PSFB LV Current Sensor Current Rail 1'			,'Measured ADCs Sampled Signals 2 Rail 1'				,'Measured ADCs Analog Signals 2 Rail 1'
									                     				, 'Measured ADCs ADC Signals 2 Rail 1'						,'Measured HW Protection Comparator Signals 2 Rail 1'

                                  										, 'Measured PSFB LV Current Sensor Current Rail 2'			,'Measured ADCs Sampled Signals 2 Rail 2'				,'Measured ADCs Analog Signals 2 Rail 2'
									                     				, 'Measured ADCs ADC Signals 2 Rail 2'						,'Measured HW Protection Comparator Signals 2 Rail 2']	,['[ A ]']],

									 	['HV Voltage'					,['Measured HV Filter Voltages 1 Rail 1'					,'Measured HV Filter Voltages 2 Rail 1'					,'Measured ADCs Sampled Signals 3 Rail 1'
									                      				, 'Measured ADCs Analog Signals 3 Rail 1'					,'Measured ADCs ADC Signals 3 Rail 1'					,'Measured HW Protection Comparator Signals 3 Rail 1'

                                   										, 'Measured HV Filter Voltages 1 Rail 2'					,'Measured HV Filter Voltages 2 Rail 2'					,'Measured ADCs Sampled Signals 3 Rail 2'
									                      				, 'Measured ADCs Analog Signals 3 Rail 2'					,'Measured ADCs ADC Signals 3 Rail 2'					,'Measured HW Protection Comparator Signals 3 Rail 2' ]	,['[ V ]']],

          								['HV Current'					,['Measured HV Current Sensor Current Rail 1'				,'Measured ADCs Sampled Signals 4 Rail 1'				,'Measured ADCs ADC Signals 4 Rail 1'
                              											, 'Measured HV Current Sensor Current Rail 2'				,'Measured ADCs Sampled Signals 4 Rail 2'				,'Measured ADCs ADC Signals 4 Rail 2']	,['[ A ]']],

										['CT Current'					,['Measured CT Current Sensor Current Rail 1'				,'Measured ADCs Sampled Signals 5 Rail 1'				,'Measured ADCs ADC Signals 5 Rail 1'

											                            , 'Measured CT Current Sensor Current Rail 2'				,'Measured ADCs Sampled Signals 5 Rail 2'				,'Measured ADCs ADC Signals 5 Rail 2']	,['[ A ]']],

										['Digital Raw Values'			,['Measured ADCs Sensors Digital Values Vo Rail 1'			,'Measured ADCs Sensors Digital Values Io Rail 1'		,'Measured ADCs Sensors Digital Values Vin Rail 1'
									                           			, 'Measured ADCs Sensors Digital Values Iin Rail 1'			,'Measured ADCs Sensors Digital Values CT Rail 1'      	,'Measured ADCs Digital Reference Rail 1'

                                       									, 'Measured ADCs Sensors Digital Values Vo Rail 2'			,'Measured ADCs Sensors Digital Values Io Rail 2'		,'Measured ADCs Sensors Digital Values Vin Rail 2'
									                           			, 'Measured ADCs Sensors Digital Values Iin Rail 2'		    ,'Measured ADCs Sensors Digital Values CT Rail 2'       ,'Measured ADCs Digital Reference Rail 2']	,['[ V ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#ADC
										['LV Voltage'					,['ADCs ADC Pin Voltages 1 Rail 1'							,'ADCs S-and-H Voltages 1 Rail 1'						,'ADCs Sampled Voltages 1 Rail 1'
                              											,'ADCs ADC Pin Voltages 1 Rail 2'							,'ADCs S-and-H Voltages 1 Rail 2'						,'ADCs Sampled Voltages 1 Rail 2'						]	,['[ V ]']],

										['LV Current'					,['ADCs ADC Pin Voltages 2 Rail 1'							,'ADCs S-and-H Voltages 2 Rail 1'						,'ADCs Sampled Voltages 2 Rail 1'
                              											,  'ADCs ADC Pin Voltages 2 Rail 2'							,'ADCs S-and-H Voltages 2 Rail 2'						,'ADCs Sampled Voltages 2 Rail 2'					]	,['[ V ]']],

										['HV Voltage'					,['ADCs ADC Pin Voltages 3 Rail 1'							,'ADCs S-and-H Voltages 3 Rail 1'						,'ADCs Sampled Voltages 3 Rail 1'
                              											,  'ADCs ADC Pin Voltages 3 Rail 2'							,'ADCs S-and-H Voltages 3 Rail 2'						,'ADCs Sampled Voltages 3 Rail 2'					]	,['[ V ]']],

										['HV Current'					,['ADCs ADC Pin Voltages 4 Rail 1'							,'ADCs S-and-H Voltages 4 Rail 1'						,'ADCs Sampled Voltages 4 Rail 1'
                              											,  'ADCs ADC Pin Voltages 4 Rail 2'							,'ADCs S-and-H Voltages 4 Rail 2'						,'ADCs Sampled Voltages 4 Rail 2'					]	,['[ V ]']],

          								['CT Current'					,['ADCs ADC Pin Voltages 5 Rail 1'							,'ADCs S-and-H Voltages 5 Rail 1'						,'ADCs Sampled Voltages 5 Rail 1'
                                      									,  'ADCs ADC Pin Voltages 5 Rail 2'							,'ADCs S-and-H Voltages 5 Rail 2'						,'ADCs Sampled Voltages 5 Rail 2'					]	,['[ V ]']],

          								['Charging Currents'			,['ADCs Charging Currents 1 Rail 1'						    ,'ADCs Charging Currents 2 Rail 1'						,'ADCs Charging Currents 3 Rail 1'
									                          			, 'ADCs Charging Currents 4 Rail 1'						    ,'ADCs Charging Currents 5 Rail 1'						,'ADCs Charging Currents 6 Rail 1'
									                             		, 'ADCs Charging Currents 7 Rail 1'						    ,'ADCs Charging Currents 8 Rail 1'						,'ADCs Charging Currents 9 Rail 1'
																		, 'ADCs Charging Currents 10 Rail 1'

                  														,  'ADCs Charging Currents 1 Rail 2'						,'ADCs Charging Currents 2 Rail 2'						,'ADCs Charging Currents 3 Rail 2'
									                          			, 'ADCs Charging Currents 4 Rail 2'						    ,'ADCs Charging Currents 5 Rail 2'						,'ADCs Charging Currents 6 Rail 2'
									                             		, 'ADCs Charging Currents 7 Rail 2'						    ,'ADCs Charging Currents 8 Rail 2'						,'ADCs Charging Currents 9 Rail 2'
																		, 'ADCs Charging Currents 10 Rail 2'                             ]	,['[ A ]']],

										['Sample Triggers'				,['ADCs Sampling Triggers 1 Rail 1'						,'ADCs Sampling Triggers 2 Rail 1'						,'ADCs Sampling Triggers 3 Rail 1'
									                         			, 'ADCs Sampling Triggers 4 Rail 1'						,'ADCs Sampling Triggers 5 Rail 1'

                                     									, 'ADCs Sampling Triggers 1 Rail 2'						,'ADCs Sampling Triggers 2 Rail 2'						,'ADCs Sampling Triggers 3 Rail 2'
									                         			, 'ADCs Sampling Triggers 4 Rail 2'						,'ADCs Sampling Triggers 5 Rail 2' ]	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#Sampling
										['LV Voltage'					,['PSFB Output Ceramic Capacitors Voltage Rail 1'			,'LV Filter Input Voltage Sampling Rail 1'				,'LV Filter Output Voltage Sampling Rail 1'
                              											, 'PSFB Output Ceramic Capacitors Voltage Rail 2'			,'LV Filter Input Voltage Sampling Rail 2'				,'LV Filter Output Voltage Sampling Rail 2'			]	,['[ V ]']],

          								['LV Current'					,['LV Current Sensor Current Sampling Rail 1' 				,'LV Current Sensor Current Sampling Rail 2']	,['[ V ]']],

          								['HV Voltage'					,['HV Filter X-Caps Voltages 1 Sampling Rail 1'			,'HV Filter X-Caps Voltages 2 Sampling Rail 1'
                                      									, 'HV Filter X-Caps Voltages 1 Sampling Rail 2'			,'HV Filter X-Caps Voltages 2 Sampling Rail 2'														]	,['[ V ]']],

          								['HV Current'					,['HV Current Sensor Current Sampling Rail 1','HV Current Sensor Current Sampling Rail 2']	,['[ A ]']],

          								['CT Current'					,['CT Current Sensor Current Sampling Rail 1','CT Current Sensor Current Sampling Rail 2']	,['[ A ]']],

          								['PWM Signals'					,['PWM Modulator Primary PWM Outputs 1 Rail 1'				,'PWM Modulator Primary PWM Outputs 2 Rail 1'			,'PWM Modulator Primary PWM Outputs 3 Rail 1'
									                      				, 'PWM Modulator Primary PWM Outputs 4 Rail 1'				,'PWM Modulator Secondary PWM Outputs 1 Rail 1'		    ,'PWM Modulator Secondary PWM Outputs 2 Rail 1'
																		, 'PWM Modulator Secondary PWM Outputs 3 Rail 1'            ,'PWM Modulator Secondary PWM Outputs 4 Rail 1'

                  														, 'PWM Modulator Primary PWM Outputs 1 Rail 2'				,'PWM Modulator Primary PWM Outputs 2 Rail 2'			,'PWM Modulator Primary PWM Outputs 3 Rail 2'
									                      				, 'PWM Modulator Primary PWM Outputs 4 Rail 2'				,'PWM Modulator Secondary PWM Outputs 1 Rail 2'		    ,'PWM Modulator Secondary PWM Outputs 2 Rail 2'
																		, 'PWM Modulator Secondary PWM Outputs 3 Rail 2'            ,'PWM Modulator Secondary PWM Outputs 4 Rail 2']	,['[ V ]']],

										['Sample Triggers'				,['Sample Trigger 1 Rail 1'								,'Sample Trigger 2 Rail 1'								,'Sample Trigger 3 Rail 1'
									                         			, 'Sample Trigger 4 Rail 1'								,'Sample Trigger 5 Rail 1'

                                              							, 'Sample Trigger 1 Rail 2'								,'Sample Trigger 2 Rail 2'								,'Sample Trigger 3 Rail 2'
									                         			, 'Sample Trigger 4 Rail 2'								,'Sample Trigger 5 Rail 2']	,['[ - ]']],

										['Controller Update'			,['Controller Update Rail 1'			,'Controller Update Rail 2']	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#SW Protection
										['Measured Signals'				,['SW Protection Measured Signals Vo Rail 1'				,'SW Protection Measured Signals Io Rail 1'			,'SW Protection Measured Signals Vin Rail 1'
									                          			, 'SW Protection Measured Signals Iin Rail 1'				,'SW Protection Upper Thresholds Vo Rail 1'			,'SW Protection Upper Thresholds Io Rail 1'
									                             		, 'SW Protection Upper Thresholds Vin Rail 1'				,'SW Protection Upper Thresholds Iin Rail 1'			,'SW Protection Lower Thresholds Vo Rail 1'
									                               		, 'SW Protection Lower Thresholds Io Rail 1'				,'SW Protection Lower Thresholds Vin Rail 1'			,'SW Protection Lower Thresholds Iin Rail 1'

                                          								, 'SW Protection Measured Signals Vo Rail 2'				,'SW Protection Measured Signals Io Rail 2'			,'SW Protection Measured Signals Vin Rail 2'
									                          			, 'SW Protection Measured Signals Iin Rail 2']	,['[ V ]','[ A ]']],

										['Fault Counters'				,['SW Protection Fault Counters Vo Rail 1'					,'SW Protection Fault Counters Io Rail 1'				,'SW Protection Fault Counters Vin Rail 1'
									                        			, 'SW Protection Fault Counters Iin Rail 1'

                                             							, 'SW Protection Fault Counters Vo Rail 2'					,'SW Protection Fault Counters Io Rail 2'				,'SW Protection Fault Counters Vin Rail 2'
									                        			, 'SW Protection Fault Counters Iin Rail 2']	,['[ V ]','[ A ]']],

										['Comparators Triggers'			,['SW Protection Fault Comparators VoH Rail 1'				,'SW Protection Fault Comparators VoL Rail 1'			,'SW Protection Fault Comparators IoH Rail 1'
									                             		, 'SW Protection Fault Comparators IoL Rail 1'				,'SW Protection Fault Comparators VinH Rail 1'			,'SW Protection Fault Comparators VinL Rail 1'
									                               		, 'SW Protection Fault Comparators IinH Rail 1'	     		,'SW Protection Fault Comparators IinL Rail 1'

                                          							    , 'SW Protection Fault Comparators VoH Rail 2'				,'SW Protection Fault Comparators VoL Rail 2'			,'SW Protection Fault Comparators IoH Rail 2'
									                             		, 'SW Protection Fault Comparators IoL Rail 2'				,'SW Protection Fault Comparators VinH Rail 2'			,'SW Protection Fault Comparators VinL Rail 2'
									                               		, 'SW Protection Fault Comparators IinH Rail 2'			,'SW Protection Fault Comparators IinL Rail 2']	,['[ V ]','[ A ]']],

										['Disable Latches'				,['SW Protection Disable Latches Vo Rail 1'				,'SW Protection Disable Latches Io Rail 1'				,'SW Protection Disable Latches Vin Rail 1'
									                         			, 'SW Protection Disable Latches Iin Rail 1'

                                     									,'SW Protection Disable Latches Vo Rail 2'				,'SW Protection Disable Latches Io Rail 2'				,'SW Protection Disable Latches Vin Rail 2'
									                         			, 'SW Protection Disable Latches Iin Rail 2']	,['[ V ]','[ A ]']],

										['Enable'						,['SW Protection Enable Signal Rail 1'					,'SW Protection Enable Signal Rail 2']	,['[ - ]']]
									],
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									[	#HW Protection
										['Output Voltage'				,[	'HW Protection Output Voltage Ref Rail 1'				,
                                 											'HW Protection Output Voltage In Rail 1'				,
                                            								'HW Protection Output Voltage VH Rail 1'			    ,
                                                    						'HW Protection Output Voltage VL Rail 1'				,
                                                          					'HW Protection Output Voltage Ref Rail 2'				,
                                                               				'HW Protection Output Voltage In Rail 2'				,
                                                                   			'HW Protection Output Voltage VH Rail 2'				,
                                                                      		'HW Protection Output Voltage VL Rail 2'
                                                                        ]	,['[ V ]']
           								],

										['Positive Output Current'		,[	'HW Protection Positive Output Current Ref Rail 1'		,
                                        									'HW Protection Positive Output Current In Rail 1'		,
                                                 							'HW Protection Positive Output Current VH Rail 1'		,
                                                        					'HW Protection Positive Output Current VL Rail 1'		,
                                                             				'HW Protection Positive Output Current Ref Rail 2'		,
                                                                 			'HW Protection Positive Output Current In Rail 2'		,
                                                                    		'HW Protection Positive Output Current VH Rail 2'		,
                                                                      		'HW Protection Positive Output Current VL Rail 2'
                                                                        ]	,['[ A ]']
           								],

										['Negative Output Current'		,[	'HW Protection Negative Output Current Ref Rail 1'		,
                                        									'HW Protection Negative Output Current In Rail 1'		,
                                                 							'HW Protection Negative Output Current VH Rail 1'		,
                                                        					'HW Protection Negative Output Current VL Rail 1'		,
                                                             				'HW Protection Negative Output Current Ref Rail 2'		,
                                                                 			'HW Protection Negative Output Current In Rail 2'		,
                                                                    		'HW Protection Negative Output Current VH Rail 2'		,
                                                                      		'HW Protection Negative Output Current VL Rail 2'
                                                                        ]	,['[ A ]']
           								],

										['Input Voltage'				,[	'HW Protection Input Voltage Ref Rail 1'				,
                                											'HW Protection Input Voltage In Rail 1'					,
                                           									'HW Protection Input Voltage VH Rail 1'					,
                                                    						'HW Protection Input Voltage VL Rail 1'					,
																			'HW Protection Input Voltage Ref Rail 2'				,
                   															'HW Protection Input Voltage In Rail 2' 				,
                                  											'HW Protection Input Voltage VH Rail 2'					,
                                             								'HW Protection Input Voltage VL Rail 2'
                                                     					]	,['[ V ]']
           								],

										['Triggers'						,[	'HW Protection Output Voltage 3 Rail 1'					,
                             												'HW Protection Positive Output Current 3 Rail 1'		,
                                         									'HW Protection Negative Output Current 3 Rail 1'		,
                                                  							'HW Protection Input Voltage 3 Rail 1'					,
                                                         					'HW Protection Output Voltage 3 Rail 2'					,
                                                              				'HW Protection Positive Output Current 3 Rail 2'		,
                                                                  			'HW Protection Negative Output Current 3 Rail 2'		,
                                                                     		'HW Protection Input Voltage 3 Rail 2'
                                                                       	]	,['[ V ]']
           								]

										# ['States'						,[	'HW Protection Latch State Rail 1'						,
                           				# 									'HW Protection Reset State Rail 1'						,
                                        # 									'HW Protection Latch State Rail 2'						,
                                        #          							'HW Protection Reset State Rail 2'
                                        #                 				]	,['[ - ]']
           								# ]
									]
									#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
									]

OBC_pmap_Raw					=	[]														# OBC Raw PLECS Mapping
OBC_pmap_plt					=	[]														# OBC Plotting  Mapping
OBC_Constants					=	[]														# OBC Constants Mapping
OBC_Ctrl_plt					=	[]														# OBC Controls plots mapping.

PFC_pmap_Raw					=	[]														# PFC Raw PLECS Mapping
PFC_pmap_plt					=	[]														# PFC Plotting  Mapping
PFC_Constants					=	[]														# PFC Constants Mapping
PFC_Ctrl_plt					=	[]														# PFC Controls plots mapping.

LLC_pmap_Raw					=	[]														# LLC Raw PLECS Mapping
LLC_pmap_plt					=	[]														# LLC Plotting  Mapping
LLC_Constants					=	[]														# LLC Constants Mapping
LLC_Ctrl_plt					=	[]														# LLC Controls plots mapping.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def return_mags(op_dict):
	"""
	Extracts parameters for transformers and chokes based on the given operational dictionary.
	Args:
	    op_dict (dict): Operational dictionary containing model variables.
	Returns:
	    tuple: Tuple containing lists of parameters for transformers and chokes.
	"""
	mdlvdict 		=   op_dict['ModelVars']
	match dp.JSON['TF_Config']:
		case 'DCDC_S'	:
			dp.trafo_inputs = [ #!
								#? Parameters for the Trafo
								[   #! core losses data-------------------------------------------------------
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Temperatures']        ,  # 0  mag_core_temp
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Flux']                ,  # 1  mag_core_flux
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Voltage']             ,  # 2  mag_core_volt
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Loss']                ,  # 3  mag_core_loss
									dp.pmapping['Transformer Flux']                     					 ,  # 4  flux index
									dp.pmapping['Measured HV Voltage']+dp.Y_list[3]                  		 ,  # 5  Volt index
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Temp']                ,  # 6  Core temp
									mdlvdict['DCDC_Rail1']['Trafo']['Core']['Factor']              ,  # 7  Gain
									#! primary losses data----------------------------------------------------
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Fvec']     ,  # 8  Pri Fvec
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Temperatures']     ,  # 9  Pri Temp vec
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Rvec']     ,  # 10 Pri Rvec
									# [mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Temp']]   ,  # 11 Pri Temp
                					[mdlvdict['Thermal']['Twater']] ,
									#! secondary losses data--------------------------------------------------
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Fvec']     ,  # 12 Pri Fvec
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Temperatures']     ,  # 13 Pri Temp vec
									mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Rvec']     ,  # 14 Pri Rvec
									# [mdlvdict['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Temp']]   ,  # 15 Pri Temp
         							[mdlvdict['Thermal']['Twater']],
        							dp.pmapping['Transformer Primary Current']								 ,
                 					dp.pmapping['Transformer Secondary Current']
						        ]
							  ]

			dp.choke_inputs = [
								#? Parameters for the  dc choke
								[   #! core losses data
									mdlvdict['DCDC_Rail1']['Lf']['Core']['Temperatures']        ,  # 0  mag_core_temp
									mdlvdict['DCDC_Rail1']['Lf']['Core']['Flux']                ,  # 1  mag_core_flux
									mdlvdict['DCDC_Rail1']['Lf']['Core']['Voltage']             ,  # 2  mag_core_volt
									mdlvdict['DCDC_Rail1']['Lf']['Core']['Loss']                ,  # 3  mag_core_loss
									0                                       ,  #!  flux for the choke
									0                                       ,  #!  voltage for the choke
									mdlvdict['DCDC_Rail1']['Lf']['Core']['Temp']                ,  # 6  Core temp
									0 ,#mdlvdict['DCDC_Rail1']['Lf']['Core']['Factor']              ,  # 7  Gain is set to 0 to not get core loss here
									#! Copper losses data
									mdlvdict['DCDC_Rail1']['Lf']['Winding']['Rwind']['Fvec']    ,  # 8  Pri Fvec
									mdlvdict['DCDC_Rail1']['Lf']['Winding']['Temperatures']     ,  # 9  Pri Temp vec
									mdlvdict['DCDC_Rail1']['Lf']['Winding']['Rwind']['Rvec']    ,  # 10 Pri Rvec
									[mdlvdict['DCDC_Rail1']['Lf']['Winding']['Rwind']['Temp']]  ,  # 11 Pri Temp
								    dp.pmapping['DC Choke Current']										  ,  # 12
									mdlvdict['DCDC_Rail1']['Lf']['Winding']['Harmonics']
								]
							]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D' 	:
			dp.trafo_inputs     =   []
			dp.choke_inputs     =   []
  		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'PFC' 		:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_S'	:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_D'	:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'OBC'		:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _			:
			dp.tkinter.messagebox.showerror(' Value Error', ' Value Error ! ')
			dp.sys.exit()

	return  dp.trafo_inputs  , dp.choke_inputs

def return_resistances(op_dict):
	"""
	Return a list of resistances based on the configuration specified in op_dict.
	Args:
	    op_dict (dict): Dictionary containing model variables and configuration.
	Returns:
	    np.ndarray: Array of resistances.

	"""
	mdlvdict 		=   op_dict['ModelVars']
	match dp.JSON['TF_Config']:
		case 'DCDC_S'	:
			dp.Resistances     =   [
				#?'CT Trafo Primary Dissipation'
				mdlvdict['DCDC_Rail1']['CT']['Trafo']['Rpri'],
				#?'CT Trafo Secondary Dissipation'
				mdlvdict['DCDC_Rail1']['CT']['Trafo']['Rsec'],
				#?'Choke RC Snubber Capacitor Dissipation'
				(mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Cs']['Rsingle']*(mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Cs']['nSer']/mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Cs']['nPar'])),
				#?'Choke RC Snubber Resistance Dissipation'
				(mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Rs']['R']/mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Rs']['nPar']),
				#?'Choke RC Snubber Parallel Resistance Dissipation'
				(mdlvdict['DCDC_Rail1']['RCsnubber']['Choke']['Rpar']),
				#?'RCD Clamp Capacitor Dissipation'
				(mdlvdict['DCDC_Rail1']['RCDclamp1']['Cs']['Rsingle']*(mdlvdict['DCDC_Rail1']['RCDclamp1']['Cs']['nSer']/mdlvdict['DCDC_Rail1']['RCDclamp1']['Cs']['nPar'])),
				#?'RCD Clamp Resistance Dissipation'
				float(mdlvdict['DCDC_Rail1']['RCDclamp1']['Rs']['R']),
				#?'Freewheeler Blocking Cap Dissipation'
				mdlvdict['DCDC_Rail1']['FRW']['BlockingCap']['Rsingle']*(mdlvdict['DCDC_Rail1']['FRW']['BlockingCap']['nSer']/mdlvdict['DCDC_Rail1']['FRW']['BlockingCap']['nPar']),
				#?'Freewheeler Resistor Dissipation'
				mdlvdict['DCDC_Rail1']['FRW']['Resistor']['R'],
				#?'Freewheeler Impedance Cap Dissipation'
				mdlvdict['DCDC_Rail1']['FRW']['ImpedanceCap']['Rsingle']*(mdlvdict['DCDC_Rail1']['FRW']['ImpedanceCap']['nSer']/mdlvdict['DCDC_Rail1']['FRW']['ImpedanceCap']['nPar']),
				#?'Damping Resistor Dissipation'
				mdlvdict['DCDC_Rail1']['Coe1']['Rd'],
				#?'LV Current Sensor Dissipation'
				mdlvdict['DCDC_Rail1']['LV_currentSense']['R'],
				#?'HV X-Caps 1 Dissipation'
				mdlvdict['DCDC_Rail1']['Cpi']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cpi']['nSer']/mdlvdict['DCDC_Rail1']['Cpi']['nPar']),
				#?'HV X-Caps 2 Dissipation'
				mdlvdict['DCDC_Rail1']['Cin']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cin']['nSer']/mdlvdict['DCDC_Rail1']['Cin']['nPar']),
				#?'HV Current Sensor Dissipation'
				mdlvdict['DCDC_Rail1']['HV_currentSense']['R'],
				#?'Blocking Capacitor Dissipation'
				mdlvdict['DCDC_Rail1']['Cb']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cb']['nSer']/mdlvdict['DCDC_Rail1']['Cb']['nPar']),
				#?'Transformer Snubber Cap Dissipation'
				mdlvdict['DCDC_Rail1']['RCsnubber']['Trafo']['Cs']['Rsingle']*(mdlvdict['DCDC_Rail1']['RCsnubber']['Trafo']['Cs']['nSer']/mdlvdict['DCDC_Rail1']['RCsnubber']['Trafo']['Cs']['nPar']),
				#?'Transformer Snubber Res Dissipation'
				(mdlvdict['DCDC_Rail1']['RCsnubber']['Trafo']['Rs']['R']/mdlvdict['DCDC_Rail1']['RCsnubber']['Trafo']['Rs']['nPar']),
				#?'MOSFET RC Snubber Cap Dissipation'
				4*mdlvdict['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Cs']['Rsingle']*(mdlvdict['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Cs']['nSer']/mdlvdict['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Cs']['nPar']),
				#?'MOSFET RC Snubber Res Dissipation'
				4*(mdlvdict['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Rs']['R']/mdlvdict['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Rs']['nPar']),
				#?'HV Y-Caps Dissipation'
				4*mdlvdict['DCDC_Rail1']['Cyi']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cyi']['nSer']/mdlvdict['DCDC_Rail1']['Cyi']['nPar']),
				#?'LV FullBridge Snubber Cap Dissipation'
				2*mdlvdict['DCDC_Rail1']['RCsnubber']['LV_FB']['Cs']['Rsingle']*(mdlvdict['DCDC_Rail1']['RCsnubber']['LV_FB']['Cs']['nSer']/mdlvdict['DCDC_Rail1']['RCsnubber']['LV_FB']['Cs']['nPar']),
				#?'LV FullBridge Snubber Res Dissipation'
				2*(mdlvdict['DCDC_Rail1']['RCsnubber']['LV_FB']['Rs']['R']/mdlvdict['DCDC_Rail1']['RCsnubber']['LV_FB']['Rs']['nPar']),
				#?'HV Snubber Caps Dissipation'
				2*mdlvdict['DCDC_Rail1']['Cc']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cc']['nSer']/mdlvdict['DCDC_Rail1']['Cc']['nPar']),
				#?'Output Ceramic Capacitors Dissipation'
				mdlvdict['DCDC_Rail1']['Co']['Rsingle']*(mdlvdict['DCDC_Rail1']['Co']['nSer']/mdlvdict['DCDC_Rail1']['Co']['nPar']),
				#?'Output Electrolytic Capacitors Dissipation'
				mdlvdict['DCDC_Rail1']['Coe1']['Rsingle']*(mdlvdict['DCDC_Rail1']['Coe1']['nSer']/mdlvdict['DCDC_Rail1']['Coe1']['nPar']),
				#?'Output Y-Cap Dissipation'
				4*mdlvdict['DCDC_Rail1']['Cyo']['Rsingle']*(mdlvdict['DCDC_Rail1']['Cyo']['nSer']/mdlvdict['DCDC_Rail1']['Cyo']['nPar']),
				#?'HV Voltage Sensor Dissipation'
				mdlvdict['DCDC_Rail1']['HV_voltageSense']['Divider']['R1'] + mdlvdict['DCDC_Rail1']['HV_voltageSense']['Divider']['R2'],
				#?'HV CMC Choke Dissipation'
				2*mdlvdict['DCDC_Rail1']['HVcmc']['Rwind'],
				#----------------------------------------------------------------------------------------------------------------------------------------------------------------
				#?'LV Filter X-Cap Dissipation'
				mdlvdict['Common']['Coc1']['Rsingle']*(mdlvdict['Common']['Coc1']['nSer']/mdlvdict['Common']['Coc1']['nPar']),
				mdlvdict['Common']['Coc2']['Rsingle']*(mdlvdict['Common']['Coc2']['nSer']/mdlvdict['Common']['Coc2']['nPar']),
				#?'LV Filter Elko-Cap Dissipation'
				mdlvdict['Common']['Coec2']['Rsingle']*(mdlvdict['Common']['Coec2']['nSer']/mdlvdict['Common']['Coec2']['nPar']),
				#?'LV Filter Y-Cap Dissipation'
				4*mdlvdict['Common']['Cyoc']['Rsingle']*(mdlvdict['Common']['Cyoc']['nSer']/mdlvdict['Common']['Cyoc']['nPar']),
				#?'LV Filter DMC Dissipation'
				2*mdlvdict['Common']['LVdmc']['Rwind'],
				#?'LV Filter CMC Dissipation'
				2*mdlvdict['Common']['LVcmc']['Rwind'],
				#?'LV Filter Single Busbar Rb_Plus Dissipation'
				mdlvdict['Common']['Busbars_PCB']['LV_Filter']['PlusResistance']																																													,
				#?'LV Filter Single Busbar Rb_Minus Dissipation'
				mdlvdict['Common']['Busbars_PCB']['LV_Filter']['MinusResistance']
			]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D' 	:
			dp.Resistances     =   [
			]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'PFC' 		:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_S'	:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_D'	:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'OBC'		:
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _			:
			dp.tkinter.messagebox.showerror('Resistances Value Error', 'Resistances Value Error ! ')
			dp.sys.exit()

	return  dp.np.array(dp.Resistances)

def remove_ranges(input_list, *ranges):
    """
    Remove specified ranges from the input list.

    Parameters:
    	- input_list 	(list)	: The input list to be modified.
    	- *ranges 		(tuple)	: Variable-length argument representing the ranges to be removed.
                      			  Each range is a tuple (start, end), where start and end are indices.
    Returns:
    	list					: The modified input list with specified ranges removed.
    """
    ranges = sorted(ranges, reverse=True)  # Sort in reverse order to avoid index shifting issues
    for start, end in ranges:
        if 0 <= start <= len(input_list) and 0 <= end <= len(input_list):
            del input_list[start:end+1]

    return input_list

def overwrite_values_with_ints(lst,shift=0):
    """
    Overwrites the values of the input list `lst` with integers corresponding to their index.

    Args:
    - lst (list)     : A list whose values need to be overwritten.
    - shift (int)   : An integer between 0 or 1 : 0 by default | 1 if we don't have Time as first key in the dict.

    Returns:
    - dict          : An ordered dictionary with the same keys as `od`, but with integer values corresponding to their index.
    """
    new_od = dp.OrderedDict()
    for i, value in enumerate(lst):
        new_od[value] = i + shift
    return new_od

def tofile_map_gen(mapping_Raw,lengths):
	"""
		Generates two ordered dictionaries of mappings from a raw mapping list and a list of segment lengths.

		The function takes three arguments:

		Args:
		------
		map_names (dict): A dictionary containing the names of the maps and their corresponding index.
		The keys are strings representing the names of the maps, and the values are
		integers representing their index. Each map index must be unique and should
		be within the range of the mapping_Raw list indices.

		mapping_Raw (list): A list representing the raw mapping data.

		lengths (list): A list of integers representing the lengths of the segments in the mapping data.
		The sum of the lengths must be less than or equal to the length of mapping_Raw.

		Returns:
		--------
		A tuple containing two ordered dictionaries:

		- Tofile_mapping_3D (dp.OrderedDict): An ordered dictionary of 3D mappings, where the keys are
		the names of the maps and the values are lists of integers.

		- Tofile_mapping_multiple (dp.OrderedDict): An ordered dictionary of multiple mappings, where the
		keys are the names of the maps and the values are
		lists of integers.
	"""
	c,idx_shift 								=	0,1
	Maps_names =  [		"Peak_Currents"		,
                        "Peak_Voltages"		,
                        "Dissipations"		,
                        "Elec_Stats"		,
                        "Temps"				,
						"Thermal_Stats"		,
                        "Controls"
	]

	Tofile_mapping_3D ,Tofile_mapping_multiple		= 	dp.OrderedDict(),dp.OrderedDict()
	for i in range(1,len(lengths)):
		Tofile_mapping_3D[Maps_names[i-1]] 			= overwrite_values_with_ints(dp.copy.deepcopy(mapping_Raw[c+1:lengths[i]+c+1]),shift=0)
		Tofile_mapping_multiple[Maps_names[i-1]] 	= overwrite_values_with_ints(dp.copy.deepcopy(mapping_Raw[c+1:lengths[i]+c+1]),shift=idx_shift)
		c			+=lengths[i]
		idx_shift	+=lengths[i]
	return	Tofile_mapping_3D,Tofile_mapping_multiple

def gen_consts(Constans_list):
	"""
     This function generates a dictionary of constants based on the configuration specified in 'dp.JSON['TF_Config']'.
     The constants are organized as key-value pairs, where the key is the constant name, and the value is a list containing the constant name, its physical mapping, and units.
     The specific constants and their details are determined based on the configuration.

     Parameters        :   Constants_list        :          List
                                                            A list of Constants parameters from the model mapping. 
      Returns          :   Constants_dict        :          Dictionary
                                                            An ordered dictionary of constants and values from the model parameters mapping.
	"""
	constants_dict	=	dp.OrderedDict()
	for sublist in Constans_list:
		constants_dict[f'{sublist[0]}'] = [f'{sublist[0]}', dp.pmapping[f'{sublist[0]}'], f'{sublist[1]}']
	return	constants_dict

def gen_pmap_plt():
	"""
	Generates plots mapping dictionaries for the html report.
	"""
	pmap_plt_dict , pmap_plt_ctrl_dict	=	dp.OrderedDict(),dp.OrderedDict()

	match dp.JSON['TF_Config']:
		case 'DCDC_S':
			for i in range(1,len(DCDC_Ctrl_plt)):	#? controls scopes
				pmap_plt_ctrl_dict[f'{DCDC_Ctrl_plt[0][i-1]}']	=	[	[
	                                                    					DCDC_Ctrl_plt[i][j][1],
																			[f"{str(DCDC_Ctrl_plt[i][j][0])} ({', '.join(str(item) for item in [str(dp.pmapping[f'{DCDC_Ctrl_plt[i][j][1][k]}']) for k in range(len(DCDC_Ctrl_plt[i][j][1]))])})"]				,
                  															[dp.pmapping[f'{DCDC_Ctrl_plt[i][j][1][k]}'] for k in range(len(DCDC_Ctrl_plt[i][j][1]))],
																			DCDC_Ctrl_plt[i][j][2]*len(DCDC_Ctrl_plt[i][j][1])

                  														]	for j in range(len(DCDC_Ctrl_plt[i]))
                                                      				]
			for i in range(len(DCDC_pmap_plt)) :
				pmap_plt_dict[f'{DCDC_pmap_plt[i][0]}'] = [
																[	[f'{DCDC_pmap_plt[i][1]}' ],
																	[f'{DCDC_pmap_plt[i][0]}'+  " Current" +'(' + str(dp.pmapping[f'{DCDC_pmap_plt[i][1]}']+1) + ')'],
																	[dp.pmapping[f'{DCDC_pmap_plt[i][1]}']],
																	['[ A ]']
																],
																[	[f'{DCDC_pmap_plt[i][2]}' ],
																	[f'{DCDC_pmap_plt[i][0]}'+  " Voltage" +'(' + str(dp.pmapping[f'{DCDC_pmap_plt[i][2]}']+1) + ')'],
																	[dp.pmapping[f'{DCDC_pmap_plt[i][2]}']],
																	['[ V ]']
																]
																]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D':
			for i in range(1,len(DCDC_DUAL_Ctrl_plt)):	#? controls scopes
				pmap_plt_ctrl_dict[f'{DCDC_DUAL_Ctrl_plt[0][i-1]}']	=	[	[
	                                                    					DCDC_DUAL_Ctrl_plt[i][j][1],
																			[f"{str(DCDC_DUAL_Ctrl_plt[i][j][0])} ({', '.join(str(item) for item in [str(dp.pmapping[f'{DCDC_DUAL_Ctrl_plt[i][j][1][k]}']) for k in range(len(DCDC_DUAL_Ctrl_plt[i][j][1]))])})"]				,
                  															[dp.pmapping[f'{DCDC_DUAL_Ctrl_plt[i][j][1][k]}'] for k in range(len(DCDC_DUAL_Ctrl_plt[i][j][1]))],
																			DCDC_DUAL_Ctrl_plt[i][j][2]*len(DCDC_DUAL_Ctrl_plt[i][j][1])

                  														]	for j in range(len(DCDC_DUAL_Ctrl_plt[i]))
                                                      				]

			for i in range(len(DCDC_DUAL_pmap_plt)) :
				if len(DCDC_DUAL_pmap_plt[i])==5:
					pmap_plt_dict[f'{DCDC_DUAL_pmap_plt[i][0]}'] = [
															[	[f'{DCDC_DUAL_pmap_plt[i][1]}',f'{DCDC_DUAL_pmap_plt[i][2]}' ],
																[f'{DCDC_DUAL_pmap_plt[i][0]}'+  " Current" +'(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']+1) + ')' +
                 													 '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']+1) + ')'],
																[dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}'],dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']],
																['[ A ]','[ A ]']
															],
															[	[f'{DCDC_DUAL_pmap_plt[i][3]}',f'{DCDC_DUAL_pmap_plt[i][4]}' ],
																[f'{DCDC_DUAL_pmap_plt[i][0]}'+  " Voltage" +'(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][3]}']+1) + ')' +
                 													 '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][4]}']+1) + ')'],
																[dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][3]}'],dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][4]}']],
																['[ V ]','[ V ]']
															]


															]
				else:
						pmap_plt_dict[f'{DCDC_DUAL_pmap_plt[i][0]}'] = [
																[	[f'{DCDC_DUAL_pmap_plt[i][1]}'],
																	[f'{DCDC_DUAL_pmap_plt[i][0]}'+  " Current" +'(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']+1) + ')'],
																	[dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']],
																	['[ A ]']
																],
																[	[f'{DCDC_DUAL_pmap_plt[i][2]}'],
																	[f'{DCDC_DUAL_pmap_plt[i][0]}'+  " Voltage" +'(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']+1) + ')'],
																	[dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']],
																	['[ V ]']
																],


																]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'PFC' :		# PFC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_S':		# Single LLC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_D':		# Dual LLC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'OBC':			# OBC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _:				# Default Case
			dp.tkinter.messagebox.showerror('ModelVar Value Error', 'dp.Config Value Error ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
	return	pmap_plt_dict,pmap_plt_ctrl_dict

def add_str(input_list, add_string):
    """
    Add a specified string to each element in the input list.

    Parameters:
    	- input_list (list)	: The input list of strings.
    	- add_string (str)	: The string to be added to each element.
    Returns:
    list					: A new list with the specified string added to each element.
    """
    modified_list = [string + add_string for string in input_list]
    return modified_list

def insert_sublist(in_list, item_list):
	"""
	Insert sublists into the input list at specified indices.

 	Parameters:
		- in_list 	(list)	: The input list.
		- item_list (list)	: List of tuples where each tuple contains a sublist and its index.

 	Returns:
		list				: The modified input list with sublists inserted at specified indices.
	"""
	in_list = dp.np.array(in_list)
	for i, (sub_list, index) in enumerate(item_list):
		in_list = dp.np.insert(in_list, index, dp.np.array(sub_list))
	return in_list.tolist()

def remove_slices(input_list, slice_indices):
    """
    Remove slices from the input list based on specified indices.

    Parameters:
    - input_list 	(list): The input list to be modified.
    - slice_indices (list): List of tuples representing the start and end indices of slices to be removed.

    Returns:
    list				  : The modified input list with specified slices removed.
    """
    for start, end in slice_indices:
        input_list[start:end] = []
    return input_list

def backward_slice(input_list, back_idx, back_size):
	"""
	Remove elements from the input list starting from a specified index in reverse order.

 	Parameters:
		- input_list 	(list)	: The input list to be modified.
		- back_idx 		(int)	: The starting index for backward slicing.
		- back_size 	(int)	: The number of elements to remove starting from back_idx.
	Returns:
		list					: The modified input list with elements removed in reverse order.
	"""
	if len(input_list) >= back_idx:
		# Remove back_size elements starting from the back_idx element backwards
		del input_list[-(back_idx + 1):-(back_idx + back_size +1):-1]
	return input_list

def dump_headers(raw_dict, names):
	"""
	Dump header information into JSON files based on specified mapping.
	Parameters:
		- raw_dict 	(dict): The raw dictionary containing header information.
		- names 	(list): List of names used for indexing header information.
	"""
    # Dumping the Header list from plecs mapping into a json file.
	with open(dp.Header_File,'w') as f:
		Time_series_header = backward_slice(dp.copy.copy(raw_dict),dp.Y_list[-1],dp.Y_Length[10])
		dp.json.dump(remove_slices(Time_series_header, [(sum(dp.Y_list[0:3]),sum(dp.Y_list[0:3])+dp.Y_Length[9])]) , f)
	f.close()
	#?-------------------------------------------------------------
	# Dumping each sub header list from plecs mapping into a separate json file
	c   =   0
	sublists 	=	[	(add_str(raw_dict[1:dp.Y_list[1]+1],' RMS')						  	 ,	sum(dp.Y_Length[0:2])),
						(add_str(raw_dict[1:dp.Y_list[1]+1],' AVG')						  	 ,	sum(dp.Y_Length[0:3])),
						(add_str(raw_dict[sum(dp.Y_list[0:2]):sum(dp.Y_list[0:3])],' RMS')   ,  sum(dp.Y_Length[0:5])),
						(add_str(raw_dict[sum(dp.Y_list[0:2]):sum(dp.Y_list[0:3])],' AVG')	 ,	sum(dp.Y_Length[0:6])),

           				(add_str(raw_dict[1:dp.Y_list[1]+1],'')						  	 ,	sum(dp.Y_Length[0:7])),
						(add_str(raw_dict[sum(dp.Y_list[0:2]):sum(dp.Y_list[0:3])],'')	 ,	sum(dp.Y_Length[0:8]))
					]
	temp_raw_dict = insert_sublist(dp.copy.copy(raw_dict),sublists)
	for i in range(1,len(dp.Y_Length)):
		header_file =   "Script/assets/HEADER_FILES/"+Maps_index[names][i-1]+ ".json"
		with open(header_file,'w') as file:
			dp.json.dump(temp_raw_dict[c+1:dp.Y_Length[i]+c+1],file)
		file.close()
		c			+=dp.Y_Length[i]

def remove_strings_from_json(json_file_path, strings_to_remove):
	"""
	 Compares a given list of strings with the ones already in a given json file
	 if found they would be removed from the json file.

	Args:
		json_file_path (str)	: input vars json file path.
		strings_to_remove (list): list of strings to be removed.
	"""
	with open(json_file_path, 'r') as file:
		data = dp.json.load(file)
	modified_list = data.copy()
	file.close()
	for string_to_remove in strings_to_remove:
		if str(string_to_remove).lower() in [item.lower() for item in modified_list]:
			modified_list.remove(string_to_remove)
	with open(json_file_path,'w') as file:
			dp.json.dump(modified_list,file)
	file.close()

def pwm_dict(raw_map,elem1,elem2 ):
	"""
       Generates a dictionary for pwm signals to be used in multiplotting.

      Parameters        	:   raw_map         :       List
                                                        The original raw mapping.
                                elem1           :       string
                                                    	First element in pwm signals.
								elem2			:		string
														Last element in pwm signals.
      Returns             	:	pwm_dict		:		List
														Ordered dictionary of the given pwm signals.
	"""
	pwm_dict = dp.OrderedDict()
	pwm_list = raw_map[raw_map.index(elem1):raw_map.index(elem2)]
	for i in range(len(pwm_list)):
		pwm_dict[f"{pwm_list[i]}"] = raw_map.index(pwm_list[i])
	return pwm_dict

def select_mapping(DCDC_pmap_Raw):
	"""
       This function selects the appropriate mapping based on the 'TF_Config' value and performs the necessary setup.

       Select Plecs mapping based on the value of the 'TF_Config' field in the JSON configuration.

       Parameters        :   DCDC_pmap_raw                :         A dictionary
       																The raw Plecs mapping dictionary.
	"""
    # initialize mapping parameters
	if dp.JSON['model'] == 'DCDC':
		dp.mode      = dp.pmap.Maps_index['DCDC_data_mat'][0]
		dp.map_index = dp.pmap.Maps_index['DCDC_data_mat'][1]
		dp.map_names = dp.pmap.Maps_index['DCDC_map_names']
	elif dp.JSON['model'] == 'OBC':
		dp.mode      = dp.pmap.Maps_index['OBC_data_mat'][0]
		dp.map_index = dp.pmap.Maps_index['OBC_data_mat'][1]
		dp.map_names = dp.pmap.Maps_index['OBC_map_names']
	else:
		raise NameError(dp.JSON['model'])


	match dp.JSON['TF_Config']:
		case 'DCDC_S'	:	#? Assign single Rail mapping

			dp.Y_Length            		=  [1,77,77,77,69,69,69,77,69,62,15,18,8,148]                                   		            # Lengths related to all exported and calculated data.
			dp.Y_list              		=  [1,77,69,25,15,18,148]																			# Lengths related to plecs output only.
			dp.Pout_idx            		=  13																								# Output power Index in Electstat maps.
			dp.Rail_idx            		=  15
			dp.Common_idx          		=  53
			dp.phase               		=  2																								# Number of phases : single , dual ...
			dp.current_idx         		=  37																								# Index up to which all currents related to resistive loads.
			dp.com_cols            		=  6																								# Number of columns of commun data (exp : LV filter).
			dump_headers(DCDC_pmap_Raw,'DCDC_map_names')																					# Generate json header files.
			DCDC_pmap_Raw 				= remove_slices(DCDC_pmap_Raw, [(sum(dp.Y_list[0:3]),sum(dp.Y_list[0:3])+dp.Y_Length[9])])			# Drop unessecary slices of the mapping.
			DCDC_pmap_Raw 				= backward_slice(DCDC_pmap_Raw,dp.Y_list[-1],dp.Y_Length[12])										# Remove thermal stats  mapping.
			dp.pmapping					= overwrite_values_with_ints(DCDC_pmap_Raw,0)														# Generate DCDC plecs mapping dict from RAW list.
			dp.pmap_3D,dp.pmap_multi	= tofile_map_gen(DCDC_pmap_Raw,dp.Y_list)															# Generate DCDC mapping dicts both for 3D and multiple plots.
			dp.pwm_dict 				= pwm_dict(DCDC_pmap_Raw,"PWM Modulator Primary PWM Outputs S1","PWM Modulator Auxiliary PWM Outputs Sdis" )
			dp.pmap_plt,dp.pmap_plt_ctrl= gen_pmap_plt()																					# Generate DCDC html plots mapping dict & ctrls mapping.
			dp.constant_dict 			= gen_consts(DCDC_Constants)																		# Generate Constants Dictionary.
			dp.plt_title_list  			= DCDC_pmap_plt
			dp.idx_start,dp.idx_end     = 53,61
			strings_to_remove			=  ['HV Left-Leg ON Current'							,
                           					'HV Left-Leg OFF Current'							,
                           					'HV Left-Leg Max Current1'							,
											'HV Left-Leg Max Current2'							,
											'HV Right-Leg ON Current'							,
         									'HV Right-Leg OFF Current'							,
         									'HV Right-Leg Max Current1'							,
											'HV Right-Leg Max Current2'
         									]
			remove_strings_from_json("Script/assets/HEADER_FILES/FFT_Current.json", strings_to_remove)
			# Define the slices as a list
			dp.slices = [
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:4]), sum(dp.Y_list[:5]))   , #? elect_stats Slice
				slice(sum(dp.Y_list[:5]), sum(dp.Y_list[:6]))   , #? Temp        Slice
				slice(sum(dp.Y_list[:6]), sum(dp.Y_list[:7]))     #? CTRL        Slice


			]
			# Define matrix operations using the slices
			dp.matrix_ops = [(f"MAT{b}", dp.mode[b-1], dp.slices[c]) for b ,c in zip([1,2,3,4,5,6,10,11,13] ,[0,1,2,3,4,5,6,7,8,9])]
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D' 	:	#? assign dual rail mapping
			dp.Y_Length            		=  [1,136,136,136,120,120,120,136,120,1,17,1,8,292]                                             	# Lengths related to all exported and calculated data.
			dp.Y_list              		=  [1,136,120,1,17,1,292]																			# Lengths related to plecs output only.
			dp.Pout_idx            		=  0																								# Output power Index in Electstat maps.
			dp.Rail_idx            		=  0
			dp.Common_idx          		=  0
			dp.phase               		=  2																								# Number of phases : single , dual ...
			dp.current_idx         		=  0																								# Index up to which all currents related to resistive loads.
			dp.com_cols            		=  0																								# Number of columns of commun data (exp : LV filter).
			dump_headers(DCDC_DUAL_pmap_Raw,'DCDC_map_names')																				# Generate json header files.
			dp.pmapping					=  overwrite_values_with_ints(DCDC_DUAL_pmap_Raw,0)													# Generate DCDC plecs mapping dict from RAW list.
			dp.pmap_3D,dp.pmap_multi	=  tofile_map_gen(DCDC_DUAL_pmap_Raw,dp.Y_list)														# Generate DCDC mapping dicts both for 3D and multiple plots.
			dp.pwm_dict 				= pwm_dict(DCDC_DUAL_pmap_Raw,"PWM Modulator Carrier Waveforms 1 Rail 1","PWM Modulator Auxiliary PWM Outputs Sdis Rail 2" )
			dp.pmap_plt,dp.pmap_plt_ctrl=  gen_pmap_plt()																					# Generate DCDC html plots mapping dict & ctrls mapping.
			dp.constant_dict 			=  gen_consts(DCDC_DUAL_Constants)																	# Generate Constants Dictionary.
			dp.plt_title_list  			=  DCDC_DUAL_pmap_plt
			dp.idx_start,dp.idx_end     =  97,113
			strings_to_remove			=  [
									        'HV Left-Leg ON Current Rail 1'				,
         									'HV Left-Leg ON Current Rail 2'				,
         									'HV Left-Leg OFF Current Rail 1'			,
                							'HV Left-Leg OFF Current Rail 2'			,
                							'HV Left-Leg Max Current1 Rail 1'			,
                     						'HV Left-Leg Max Current1 Rail 2'			,
											'HV Left-Leg Max Current2 Rail 1'			,
         									'HV Left-Leg Max Current2 Rail 2'			,
											'HV Right-Leg ON Current Rail 1'			,
         									'HV Right-Leg ON Current Rail 2'			,
         									'HV Right-Leg OFF Current Rail 1'			,
                							'HV Right-Leg OFF Current Rail 2'			,
                							'HV Right-Leg Max Current1 Rail 1'			,
                     						'HV Right-Leg Max Current1 Rail 2'			,
											'HV Right-Leg Max Current2 Rail 1'			,
         									'HV Right-Leg Max Current2 Rail 2'
											]
			remove_strings_from_json("Script/assets/HEADER_FILES/FFT_Current.json", strings_to_remove)
			# Define the slices as a list
			dp.slices = [
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)                      , #? Currents    Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:2]), sum(dp.Y_list[:3]))   , #? voltage     Slice
				slice(sum(dp.Y_list[:4]), sum(dp.Y_list[:5]))   , #? elect_stats Slice
				slice(sum(dp.Y_list[:5]), sum(dp.Y_list[:6]))   , #? Temp        Slice
				slice(sum(dp.Y_list[:6]), sum(dp.Y_list[:7]))     #? CTRL        Slice
			]
			# Define matrix operations using the slices
			dp.matrix_ops = [(f"MAT{b}", dp.mode[b-1], dp.slices[c]) for b ,c in zip([1,2,3,4,5,6,10,11,13] ,[0,1,2,3,4,5,6,7,8,9])]
  	#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'PFC' 		:	#? PFC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_S'	:	#? Single LLC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'LLC_D'	:	#? Dual LLC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'OBC'		:	#? OBC Mapping
			dp.tkinter.messagebox.showerror('ERROR', 'MODEL NOT IMPLEMENTED YET ! ')
			dp.sys.exit()
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _			:	#? Default Case
			dp.tkinter.messagebox.showerror('ModelVar Value Error', 'TF_Config Value Error ! ')
			dp.sys.exit()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
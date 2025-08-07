
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 ____                                  ____                                _
#?						/ ___|  ___ _ __  ___  ___  _ __ ___  |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___
#?						\___ \ / _ \ '_ \/ __|/ _ \| '__/ __| | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?						 ___) |  __/ | | \__ \ (_) | |  \__ \ |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?						|____/ \___|_| |_|___/\___/|_|  |___/ |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs sensor models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------import dependencies
import Dependencies as dp

#------------------

#! Call the Post-Processing class and point to the location of csv data
postProcessing 	=	dp.PP.Processing()
sensorsPath		=	'Script/Data/Sensors_Errors/'

#! random number generator range
randMin	=	-1e6
randMax	=	1e6

#! Sensors models parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Voltage Sensors

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'Si8932D_Error'
error		=	postProcessing.extractArrays(sensor)

SI8932D				=	{																																	#*	generic SI8932D voltage sensor model
							'Config'				: 2																									,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'				: 1																									,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'					: 0																									,	#?	point in time of sampling trigger
							'Divider'				:	{																									#!	voltage divider parameters
															'R1'				: 160e3*5																,	#?	HV resistance
															'R2'				: 3.79e3																,	#?	LV resistance
															'Cf'				: 820e-12+4.7e-9															#?	filter capacitance
														},
							'FirstComponent'		:	{																									#!	first BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 23.446																,	#?	second-order first resistance
															'R2_2'				: 23.446																,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 20e-9																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'SecondComponent'		:	{																									#!	second BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'ThirdComponent'		:	{																									#!	third BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 0																			#?	filter capacitance
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 3.79/(3.79 + 160*5)													,	#?	measurement gain
															'Voffset'			: 0.0																	,	#?	measurement offset
															'Delay'				: 1.0e-6																	#?	sensor delay
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
                            'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 1e-9																	,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 5e-3																	,	#?	max current limit on capacitive link
                                                            'LoLim'				: -5e-3																	,	#?	min current limit on capacitive link
                                                            'Voffset'			: 0																			#?	voltage offset for inductive link
							}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'BuffDivider_1_Error'
error		=	postProcessing.extractArrays(sensor)

BuffDivider_1		=	{																																	#*	voltage divider model
							'Config'											: 2																		,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'											: 1																		,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'												: 0																		,	#?	point in time of sampling trigger
							'R1'												: 18e3																	,	#?	HV resistance
							'R2'												: 2e3																	,	#?	LV resistance
							'Cf'												: 0.0																	,	#?	filter capacitance
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 0																			#?	filter capacitance
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 1e-9																	,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 0																			#?	voltage offset for inductive link
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 2/(2 + 18)															,	#?	measurement gain
															'Voffset'			: 0.0																	,	#?	measurement offset
															'Delay'				: 500e-9																	#?	sensor delay
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'BuffDivider_2_Error'
error		=	postProcessing.extractArrays(sensor)

BuffDivider_2		=	{																																	#*	voltage divider model
							'Config'											: 2																		,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'											: 1																		,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'												: 0																		,	#?	point in time of sampling trigger
							'R1'												: 9e3																	,	#?	HV resistance
							'R2'												: 1e3																	,	#?	LV resistance
							'Cf'												: 100e-12																,	#?	filter capacitance
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 200																	,	#?	filter resistance
															'C'					: 330e-12																	#?	filter capacitance
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 0																		,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 0																			#?	voltage offset for inductive link
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 1/(1 + 9)																,	#?	measurement gain
															'Voffset'			: 0.0																	,	#?	measurement offset
															'Delay'				: 1e-6																		#?	sensor delay
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'BuffDivider_3_Error'
error		=	postProcessing.extractArrays(sensor)

BuffDivider_3		=	{																																	#*	voltage divider model
							'Config'											: 2																		,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'											: 1																		,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'												: 0																		,	#?	point in time of sampling trigger
							'R1'												: 56e3																	,	#?	HV resistance
							'R2'												: 4.7e3																	,	#?	LV resistance
							'Cf'												: 100e-12																,	#?	filter capacitance
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 0																			#?	filter capacitance
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 1e-9																	,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 0																			#?	voltage offset for inductive link
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 4.7/(4.7 + 56)														,	#?	measurement gain
															'Voffset'			: 0.0																	,	#?	measurement offset
															'Delay'				: 1.0e-6																	#?	sensor delay
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Current Sensors

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'INA240A2_Error'
error		=	postProcessing.extractArrays(sensor)

INA240A2			=	{																																	#*	generic INA240A2 voltage sensor model
							'Config'				: 2																									,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'				: 1																									,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'					: 0																									,	#?	point in time of sampling trigger
							'R'						: 100e-6																							,	#?	shunr or internal sensor resistance
                            'Rth'					: [4.260,6.212,6.000,5.222,13.956]																	,	#?	sensor themral resistance vector
                            'Cth'					: [1.504,0.350,15.102,127.085,40.961]																,	#?	sensor themral capacitance vector
							'FirstComponent'		:	{																									#!	first BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 34.0																	,	#?	second-order first resistance
															'R2_2'				: 34.0																	,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 11.72e-9																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'SecondComponent'		:	{																									#!	second BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 2.45e3																,	#?	second-order first resistance
															'R2_2'				: 7.3																	,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 203e-12																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 50.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'ThirdComponent'		:	{																									#!	third BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 1e-9																		#?	filter capacitance
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 100e-6*50																,	#?	measurement gain
															'Voffset'			: 1.5																	,	#?	measurement offset
															'Delay'				: 511e-9																	#?	sensor delay
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
							'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 0																		,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 1.5																		#?	voltage offset for inductive link
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'INA240A1_Error'
error		=	postProcessing.extractArrays(sensor)

INA240A1			=	{																																	#*	generic INA240A2 voltage sensor model
							'Config'				: 2																									,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'				: 1																									,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'					: 0																									,	#?	point in time of sampling trigger
							'R'						: 300e-6																							,	#?	shunt or inline sensor resistance
                            'Rth'					: [4.260,6.212,6.000,5.222,13.956]																	,	#?	sensor themral resistance vector
                            'Cth'					: [1.504,0.350,15.102,127.085,40.961]																,	#?	sensor themral capacitance vector
							'FirstComponent'		:	{																									#!	first BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 34.0																	,	#?	second-order first resistance
															'R2_2'				: 34.0																	,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 11.72e-9																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'SecondComponent'		:	{																									#!	second BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 2.45e3																,	#?	second-order first resistance
															'R2_2'				: 7.3																	,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 203e-12																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 20.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'ThirdComponent'		:	{																									#!	third BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 1e-9																		#?	filter capacitance
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 300e-6*20																,	#?	measurement gain
															'Voffset'			: 1.5																	,	#?	measurement offset
															'Delay'				: 511e-9																	#?	sensor delay
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 0																		,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 1.5																		#?	voltage offset for inductive link
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'ACS773_Error'
error		=	postProcessing.extractArrays(sensor)

ACS773				=	{																																	#*	generic ACS773 voltage sensor model
							'Config'				: 2																									,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'				: 1																									,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'					: 0																									,	#?	point in time of sampling trigger
							'R'						: 100e-6																							,	#?	shunr or internal sensor resistance
							'FirstComponent'		:	{																									#!	first BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 75.0																	,	#?	second-order first resistance
															'R2_2'				: 212.0																	,	#?	second-order second resistance
															'C1_2'				: 20e-9																	,	#?	second-order first capacitance
															'C2_2'				: 1.0e-9																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 66.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'SecondComponent'		:	{																									#!	second BWF filter parameters
															'R1_1'				: 40.0																	,	#?	first-order resistance
															'C1_1'				: 10e-9																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 1																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'ThirdComponent'		:	{																									#!	third BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 2e3																	,	#?	filter resistance
															'C'					: 1e-9																		#?	filter capacitance
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 100e-6*66																,	#?	measurement gain
															'Voffset'			: 1.5																	,	#?	measurement offset
															'Delay'				: 2.5e-6																	#?	sensor delay
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
                            'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 0																		,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.5e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.5e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 1.5																		#?	voltage offset for inductive link
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'ASC724_Error'
error		=	postProcessing.extractArrays(sensor)

ACS724				=	{																																	#*	generic ACS724 voltage sensor model
							'Config'				: 2																									,	#?	1->physical model | 2->small-signal model | 3->Ideal model
							'Channel'				: 1																									,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Phase'					: 0																									,	#?	point in time of sampling trigger
							'R'						: 264e-6																							,	#?	shunr or internal sensor resistance
							'FirstComponent'		:	{																									#!	first BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 28.35e3																,	#?	second-order first resistance
															'R2_2'				: 10.0																	,	#?	second-order second resistance
															'C1_2'				: 10e-9																	,	#?	second-order first capacitance
															'C2_2'				: 40.1e-12																,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 250.0																	,	#?	feedback gain
															'Config'			: 2																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'SecondComponent'		:	{																									#!	second BWF filter parameters
															'R1_1'				: 72.3																	,	#?	first-order resistance
															'C1_1'				: 10e-9																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 1																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'ThirdComponent'		:	{																									#!	third BWF filter parameters
															'R1_1'				: 0.0																	,	#?	first-order resistance
															'C1_1'				: 0.0																	,	#?	first-order capacitance
															'R1_2'				: 0.0																	,	#?	second-order first resistance
															'R2_2'				: 0.0																	,	#?	second-order second resistance
															'C1_2'				: 0.0																	,	#?	second-order first capacitance
															'C2_2'				: 0.0																	,	#?	second-order second capacitance
															'R3'				: 1e3																	,	#?	feedback gain resistance
															'Gain'				: 1.0																	,	#?	feedback gain
															'Config'			: 3																		,	#?	1->first-order | 2->second-order | 3->pass
														},
							'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 0																			#?	filter capacitance
														},
							'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 264e-6*250															,	#?	measurement gain
															'Voffset'			: 1.5																	,	#?	measurement offset
															'Delay'				: 4.0e-6																	#?	sensor delay
														},
							'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
							'CurrentLimit'			:	{																									#*	current limit
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'Ts'				: 0 																	,	#?	sampling time for inductive link
															'tau'				: 1e-9																	,	#?	first-order delay for inductive link
                                                            'Rs'				: 0																		,	#?	source impedance of inductive link
                                                            'UpLim'				: 1.6e-3																,	#?	max current limit on capacitive link
                                                            'LoLim'				: -1.6e-3																,	#?	min current limit on capacitive link
                                                            'Voffset'			: 1.5																		#?	voltage offset for inductive link
														}
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

randError	=	dp.random.SystemRandom().randint(randMin, randMax)
randNoise	=	dp.random.SystemRandom().randint(randMin, randMax)
sensor 		= 	sensorsPath + 'DS_P100076_Error'
error		=	postProcessing.extractArrays(sensor)

DS_P100076			=	{																																	#*	DS_P100076 current transformer parameters
							'Config'				:	1																								,	#?	1->physical model | 2->small-signal model | 3->ideal model
                            'Channel'				:   1																								,	#?	0->odd-odd or even-even | 1->even-odd or odd-even
							'Trafo'					:	dp.copy.deepcopy(dp.Mags_Dicts.DS_P100076_Trafo)												,	#?	current transformer parameters
                            'Rt'					:	11																								,	#?	burden or terminating resistance
                            'Ct'					:	0																								,	#?	terminating capacitance
							'Vf'        			:	0.375			    																			,   #?	rectifier diode forward voltage
							'Rd'       				:	22e-3		        																			,   #?	rectifier diode ON-state resistance
							'Rf'					:	100																								,	#?	RC filter resistance
							'Cf'					:	100e-12																							,	#?	RC filter capacitance
                            'Phase'					: 	0																								,	#?	point in time of sampling trigger
							'Cf_factor'				:	100																								,	#?	RC filter capacitance factor
							'DiodeLoss'				:	[0.1, 0.1, 0.1, 0.1]	 																		,	#?	estimated switching loss of the CT diodes
                            'LP_Filter'				:	{																									#!	external low-pass filter
															'R'					: 0																		,	#?	filter resistance
															'C'					: 0																			#?	filter capacitance
														},
                            'Misc'					:	{																									#!	miscellaneous parameters
															'Vadc'				: 3.0																	,	#?	full-scale ADC voltage
															'Gain'				: 11/100																,	#?	measurement gain
															'Voffset'			: 0																		,	#?	measurement offset
															'Delay'				: 0																			#?	sensor delay
														},
                            'Error'					:	{																									#*	error parameters
									'Vvec'										: error[0]																,	#?	voltage vector referred to ADC range
                                    'Polarity'									: 1																		,	#?	1->positive | 2->negative | 3->random
									'Seed'										: randError																,   #?	random polarity seed
									'SampleTime'								: 10e-6																	,	#?	random polarity sample time
									'Digital'	:	{																										#!	digital error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[1:5])).T).tolist()								,	#?	digital error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
                                    'Analog'	:	{																										#!	analog error parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
															'ErrVec'			: ((dp.np.array(error[5:9])).T).tolist()								,	#?	analog error vectors
															'ErrType'			: 1																			#?	1->uncalibrated rms error | 2->uncalibrated max error | 3->calibrated rms error | 4->calibrated max error
													},
														},
							'Noise'					:	{																									#*	white noise parameters
									'Digital'	:	{																										#!	digital noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
                                    'Analog'	:	{																										#!	analog noise parameters
															'Config'			: 2																		,	#?	1->enable | 2->disable
                                                            'Sigma'				: 0.05																	,	#?	standard deveiation of the normally distributed noise
                                                            'Mean'				: 0																		,	#?	DC offset of the normally distributed noise
															'Seed'				: randNoise																,   #?	random noise seed
															'SampleTime'		: 100e-6																	#?	random noise sample time
													},
														},
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!	assemble all sensors to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AllSensors 			= 	{
							'SI8932D' 				: 	SI8932D 			,
							'BuffDivider_1' 		: 	BuffDivider_1 		,
							'BuffDivider_2' 		: 	BuffDivider_2 		,
                            'BuffDivider_3' 		: 	BuffDivider_3 		,
							'INA240A2' 				: 	INA240A2 			,
                            'INA240A1'				:	INA240A1			,
							'ACS773' 				: 	ACS773 				,
							'ACS724' 				: 	ACS724 				,
							'DS_P100076' 			: 	DS_P100076
						}
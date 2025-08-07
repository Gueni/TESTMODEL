
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 __  __    _    ____ _   _ _____ _____ ___ ____ ____    ____   _    ____      _    __  __ _____ _____ _____ ____  ____
#?						|  \/  |  / \  / ___| \ | | ____|_   _|_ _/ ___/ ___|  |  _ \ / \  |  _ \    / \  |  \/  | ____|_   _| ____|  _ \/ ___|
#?						| |\/| | / _ \| |  _|  \| |  _|   | |  | | |   \___ \  | |_) / _ \ | |_) |  / _ \ | |\/| |  _|   | | |  _| | |_) \___ \
#?						| |  | |/ ___ \ |_| | |\  | |___  | |  | | |___ ___) | |  __/ ___ \|  _ <  / ___ \| |  | | |___  | | | |___|  _ < ___) |
#?						|_|  |_/_/   \_\____|_| \_|_____| |_| |___\____|____/  |_| /_/   \_\_| \_\/_/   \_\_|  |_|_____| |_| |_____|_| \_\____/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs transformer models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------import dependencies

import Dependencies as dp

#------------------

#! Call the Post-Processing class and point to the location of csv data
paramProcess				=	dp.PM.ParamProcess()
MagsCoreLossesPath			=	'Script/Data/Mags_Core_Losses/'
MagsFreqResistancePath		=	'Script/Data/Mags_Freq_Resistance/'
InductanceCurrentPath		=	'Script/Data/Mags_L_I/'

#! Transformer models parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Transformers

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'TDK_A20_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['TDK_A20_Pri','TDK_A20_Sec'])

TDK_A20_Trafo 		=	{																																	#!	TDK A2.0 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	10					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]		                															,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]						                											,   #?	secondary windings resistance
							'Lkp' 	    			:	4.0e-6			               																	,   #?	leakage inductance of primary side
							'Lks' 	    			:	0.0			               																		,   #?	leakage inductance of secondary side
							'Lm'        			:	630e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	0.0																								,	#?	primary-side intrawinding capacitance
							'Cs'					:	0.0																								,	#?	secondary-side intrawinding capacitance
							'Cm'					:	0																								,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0				           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1]																								,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.00																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.00																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
									'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B10_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B10_Pri','Cyntec_B10_Sec'])

Cyntec_B10_Trafo 	=	{																																	#!	Cyntec B1.0 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	10					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]	                																,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]					                												,   #?	secondary windings resistance
							'Lkp' 	    			:	2.75e-6			               																	,   #?	leakage inductance of primary side
							'Lks' 	    			:	0.0			               																		,   #?	leakage inductance of secondary side
							'Lm'        			:	570e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	0																								,	#?	primary-side intrawinding capacitance
							'Cs'					:	0																								,	#?	secondary-side intrawinding capacitance
							'Cm'					:	0																								,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0				           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1,3,5,7,9]																						,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.025																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[200,250,300,350,400,425]																		,	#?	excitation voltage vector
                                    'Temperatures'	:	[25,50,75,90]																					,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B20_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B20_Pri','Cyntec_B20_Sec'])

Cyntec_B20_Trafo 	=	{																																	#!	Cyntec B2.0 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	10					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]	                																,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]					                												,   #?	secondary windings resistance
							'Lkp' 	    			:	1.4e-6			               																	,   #?	leakage inductance of primary side
							'Lks' 	    			:	20e-9			               																	,   #?	leakage inductance of secondary side
							'Lm'        			:	800e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	16e-12																							,	#?	primary-side intrawinding capacitance
							'Cs'					:	200e-12																							,	#?	secondary-side intrawinding capacitance
							'Cm'					:	50e-12																							,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0				           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1,3,5,7,9]																						,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.025																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[200,250,300,350,400,425]																		,	#?	excitation voltage vector
									'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B21_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B21_Pri','Cyntec_B21_Sec'])

Cyntec_B21_Trafo 	=	{																																	#!	Cyntec B2.1 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	10					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]	                																,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]					                												,   #?	secondary windings resistance
							'Lkp' 	    			:	2.4e-6			               																	,   #?	leakage inductance of primary side
							'Lks' 	    			:	0			               																		,   #?	leakage inductance of secondary side
							'Lm'        			:	800e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	16e-12																							,	#?	primary-side intrawinding capacitance
							'Cs'					:	200e-12																							,	#?	secondary-side intrawinding capacitance
							'Cm'					:	50e-12																							,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0				           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1,3,5,7,9]																						,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.025																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[200,250,300,350,400,425]																		,	#?	excitation voltage vector
                                    'Temperatures'	:	[25,50,75,90]																					,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        	'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Cyntec_C10_Trafo 	=	dp.copy.deepcopy(Cyntec_B21_Trafo)																									#!	Cyntec C1.0 transformer parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_C20_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_C20_Pri','Cyntec_C20_Sec'])

Cyntec_C20_Trafo 	=	{																																	#!	Cyntec C2.0 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	10					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]	                																,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]					                												,   #?	secondary windings resistance
							'Lkp' 	    			:	2.4e-6			               																	,   #?	leakage inductance of primary side
							'Lks' 	    			:	0			               																		,   #?	leakage inductance of secondary side
							'Lm'        			:	800e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	16e-12																							,	#?	primary-side intrawinding capacitance
							'Cs'					:	200e-12																							,	#?	secondary-side intrawinding capacitance
							'Cm'					:	50e-12																							,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0				           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1,3,5,7,9]																						,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,50,75,100]																					,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.025																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[200,250,300,350,400,425]																		,	#?	excitation voltage vector
                                    'Temperatures'	:	[25,50,75,90]																					,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        	'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_EB2_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_EB2_Pri','Cyntec_EB2_Sec'])

Cyntec_EB2_Trafo 	=	{																																	#!	Cyntec B2.1 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	11					            																,   #?	number of primary windings
							'Ns'  	   				:	1					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]	                																,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]					                												,   #?	secondary windings resistance
							'Lkp' 	    			:	2.9e-6		               																		,   #?	leakage inductance of primary side
							'Lks' 	    			:	0			               																		,   #?	leakage inductance of secondary side
							'Lm'        			:	836e-6			                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	20e-12																							,	#?	primary-side intrawinding capacitance
							'Cs'					:	2.5e-9																							,	#?	secondary-side intrawinding capacitance
							'Cm'					:	48e-12																							,	#?	interwinding capacitance
                            'Ae'					:  	468e-6			                																,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	3465			           																		,   #?	relative core permeability
							'B_sat'	   				:	0.0					            																,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
								'Harmonics'			:	[1]																								,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.025																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[200,250,300,350,400,425]																		,	#?	excitation voltage vector
									'Temperatures'	:	[25,50,75,90]																					,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
                                    'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	34198/30928																							#?	core loss scaling with frequency or volume
						},
                        'SS_Model'	:	{																													#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-0.002109008,0.000374324,1.80e-05]																,	#?	first row values
                                    'A2'			:	[-0.014719316,-0.017618562,0.00293545]															,	#?	second row values
                                    'A3'			:	[0.023404674,0.025759437,-0.010189019]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[2.18e-05,-3.45e-06,3.66e-06]																	,	#?	first row values
                                    'B2'			:	[-0.000113555,0.000348812,8.16e-05]																,	#?	second row values
                                    'B3'			:	[0.000241227,-0.000589271,-0.000270645]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[14.19379266,0.360298286,0.140996579]															,	#?	first row values
                                    'C2'			:	[6.50794603,1.523482938,-0.122709737]															,	#?	second row values
                                    'C3'			:	[1.921283377,-1.128116181,-1.081509356]																#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[0.118972596,0.021220688,0.015891864]															,	#?	first row values
                                    'D2'			:	[0.036744395,0.034747295,0.011020122]															,	#?	second row values
                                    'D3'			:	[0.011994022,-0.002309562,0.03076368]																#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'DS_P100076_Trafo')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['DS_P100076_Pri','DS_P100076_Sec'])

DS_P100076_Trafo 	=	{																																	#!	DS_P100076 transformer parameters
							'Config'    			:	1					            																,   #?	1->ideal electrical model | 2->nonideal electrical model | 3->magnetic model
							'Np'  	   				:	1					            																,   #?	number of primary windings
							'Ns'  	   				:	100					            																,   #?	number of secondary windings
							'Rpri'      			:	Rvec[0][-1][0]                																	,   #?	primary windings resistance
							'Rsec' 	   				:	Rvec[1][-1][0]			                														,   #?	secondary windings resistance
							'Lkp' 	    			:	0			               																		,   #?	leakage inductance of primary side
							'Lks' 	    			:	290e-6			               																	,   #?	leakage inductance of secondary side
							'Lm'        			:	7e-3/100**2		                																,   #?	magnetizing inductance primary-reflected
							'Vs'					:	1000e-6																							,	#?	core maximum volt-seconds before saturation
							'Cp'					:	0																								,	#?	primary-side intrawinding capacitance
							'Cs'					:	4e-12																							,	#?	secondary-side intrawinding capacitance
							'Cm'					:	0																								,	#?	interwinding capacitance
                            'Ae'					:  	0			                																	,   #?	effective flux area
							'Le'					:  	0				            																	,   #?	effective flux length
							'mu_r'	   				:  	0					           																	,   #?	relative core permeability
							'B_sat'	   				:	0.0				            																	,   #?	saturation flux density
                            'FF'					:	1																								,	#?	core saturation fitting function, 1->atan | 2->coth
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[1]																								,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rpri'		:	{																											#!	primary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.00																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							},
								'Rsec'		:	{																											#!	secondary windings parameters
									'Rvec'			:	(dp.np.array(Rvec[1]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[1]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.00																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
									'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss values matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	0																								,	#?	initial condition for the running max
                                    'MinInit'		:	0																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						},
                        'SS_Model'	:	{																												#*	state-space thermal model for core and windings
								'A_matrix'	:	{																											#!	A matrix values
                                    'A1'			:	[-5.2729E-03, 1.1113E-03, -2.6198E-05]															,	#?	first row values
                                    'A2'			:	[1.9485E-03, 8.3994E-04, -2.8774E-03]															,	#?	second row values
                                    'A3'			:	[-2.2308E-02, 8.1219E-02, -7.1983E-02]																#?	third row values
								},
                                'B_matrix'	:	{																											#!	B matrix values
                                    'B1'			:	[-7.2224E-06, -4.2520E-05, -4.5810E-06]															,	#?	first row values
                                    'B2'			:	[-2.6539E-05, 1.6315E-05, -2.4964E-05]															,	#?	second row values
                                    'B3'			:	[-6.7454E-05, 1.5621E-03, -1.1633E-03]																#?	third row values
								},
                                'C_matrix'	:	{																											#!	C matrix values
                                    'C1'			:	[-440.3173, -174.4865, -6.2049]																	,	#?	first row values
                                    'C2'			:	[-1328.4458, 357.8770, -3.4755]																	,	#?	second row values
                                    'C3'			:	[-940.8181, 303.2090, -58.1557]																		#?	third row values
								},
                                'D_matrix'	:	{																											#!	D matrix values
                                    'D1'			:	[4.7351, 13.7871, -2.4276]																		,	#?	first row values
                                    'D2'			:	[0.5827, 7.6973, 1.9641]																		,	#?	second row values
                                    'D3'			:	[0.5863, 4.4643, 2.1765]																			#?	third row values
								},
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Inductors

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'TDK_A20_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['TDK_A20_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'TDK_A20_Choke')

TDK_A20_Choke	= 	{																																		#!	TDK A2.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	2.6e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,100,125]																					,	#?	temperatures vector
                                'Lscale'			:	1.00																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0]																								,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.00																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
                                	'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Sumida_B10_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Sumida_B10_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Sumida_B10_Choke')

Sumida_B10_Choke	= 	{																																	#!	Sumida B1.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.5e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,100]																						,	#?	temperatures vector
								'Lscale'			:	1.00																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B10_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B10_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Cyntec_B10_Choke')

Cyntec_B10_Choke	= 	{																																	#!	Cyntec B1.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.7e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,100]																						,	#?	temperatures vector
								'Lscale'			:	1.00																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.0625																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B20_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B20_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Cyntec_B20_Choke')

Cyntec_B20_Choke	= 	{																																	#!	Cyntec B2.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.5e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,100]																						,	#?	temperatures vector
								'Lscale'			:	1.167																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.20																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_B21_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_B21_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Cyntec_B21_Choke')

Cyntec_B21_Choke	= 	{																																	#!	Cyntec B2.1 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.95e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,50,75,100]																					,	#?	temperatures vector
								'Lscale'			:	1.282																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.20																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Cyntec_C10_Choke 	=	dp.copy.deepcopy(Cyntec_B21_Choke)																									#!	Cyntec C1.0 choke parameters

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_C20_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_C20_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Cyntec_C20_Choke')

Cyntec_C20_Choke	= 	{																																	#!	Cyntec C2.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.95e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,50,75,100]																					,	#?	temperatures vector
								'Lscale'			:	1.282																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,50,75,100]																					,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.20																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

flux,cat,loss 	=	paramProcess.Mags_CoreLoss_Data(MagsCoreLossesPath,'Cyntec_EB2_Choke')
Fvec,Rvec 		=	paramProcess.Mags_FreqRes_Data(MagsFreqResistancePath,['Cyntec_EB2_Choke'])
Ivec,Lvec 		=	paramProcess.Mags_LI_Data(InductanceCurrentPath,'Cyntec_EB2_Choke')

Cyntec_EB2_Choke	= 	{																																	#!	Cyntec B2.0 choke parameters
							'Config'   				:	1																								, 	#?	1->constant inductance | 2->variable inductance | 3->magnetic domain
							'L'  	   				:	1.3e-6   		    																			, 	#?	constant inductance value
							'R'  	   				:	Rvec[0][-1][0]  		   		 																	, 	#?	winding series resistance
                            'C'						:	3e-12*0																							,	#?	interwinding capacitance
                            'Rp'					:	"inf"																							,	#?	parasitic parallel resistance
							'Ae'	   				:   0			   																					,   #?	effective core area
							'Le'	   				:   0																								,   #?	effective flux length
							'N'		   				:   0																								,   #?	number of turns
							'g'		   				:   0			   																					,   #?	air gap length
							'Acp'	   				:   0  																								,   #? 	air gap area
							'mu_r'	   				:   0																								,   #?	relative permeability
							'Bsat'	   				:   0				            																	,   #?	saturation flux density
							'Inductance'	:	{																											#!	variable inductance parameters
								'Ivec'				:	Ivec																							,	#?	currents vector
								'Lvec'				:	Lvec 																							,	#?	inductances vector
								'Tvec'				:	[25,100]																						,	#?	temperatures vector
								'Lscale'			:	1.00																							,	#?	scaling between typ and max
								'Temp'				:	100																									#?	operating temperature
							},
                            'Winding'	:	{																												#*	winding resistance lookup table parameters
    							'Harmonics'			:	[0,2,4,6,8,10]																					,	#!	harmonics order for Fourier decomposition
								'Temperatures'		:	[25,100]																						,	#!	windings temperature vector for resistance scaling
								'Rwind'		:	{																											#!	windings parameters
									'Rvec'			:	(dp.np.array(Rvec[0]).T).tolist()																,	#?	resistance spectrum vector
                                    'Fvec'			:	Fvec[0]																							,	#?	frequency spectrum vector
									'Rscale'		:	1.2093																							,	#?	scaling between typ and max
									'Temp'			:	100																									#?	constant operating temperature
							}
						},
                            'Core'		:	{																												#!	core loss lookup table parameters
									'Voltage'		:	[0,2000]																						,	#?	excitation voltage vector
                                    'Temperatures'	:	[0,100]																							,	#?	core temperature vector for loss scaling
									'Flux'			:	flux 																							,	#?	operating flux linkage vector
                                    'CAT'			:	cat																								,	#?	octave core loss syntax
                                    'Loss'			:	loss																							,	#?	core loss matrix
									'Temp'			:	25																								,	#?	operting temperature
                                    'MaxInit'		:	-1																								,	#?	initial condition for the running max
                                    'MinInit'		:	1																								,	#?	initial condition for the running min
									'Factor'		:	1.0																									#?	core loss scaling with frequency or volume
						}
					}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!	assemble all trafos to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Trafos 			= 	{
						'TDK_A20_Trafo'			:	TDK_A20_Trafo			,
                    	'Cyntec_B10_Trafo'		:	Cyntec_B10_Trafo		,
						'Cyntec_B20_Trafo' 		: 	Cyntec_B20_Trafo		,
                    	'Cyntec_B21_Trafo'		:	Cyntec_B21_Trafo		,
                        'Cyntec_C10_Trafo'		:	Cyntec_C10_Trafo		,
                        'Cyntec_C20_Trafo'		:	Cyntec_C20_Trafo		,
                    	'Cyntec_EB2_Trafo'		:	Cyntec_EB2_Trafo		,
						'DS_P100076_Trafo'		:	DS_P100076_Trafo
					}

Chokes 			= 	{
						'TDK_A20_Choke'			:	TDK_A20_Choke			,
                    	'Cyntec_B10_Choke'		:	Cyntec_B10_Choke		,
                    	'Sumida_B10_Choke'		:	Sumida_B10_Choke		,
						'Cyntec_B20_Choke' 		: 	Cyntec_B20_Choke		,
                    	'Cyntec_B21_Choke'		:	Cyntec_B21_Choke		,
                        'Cyntec_C10_Choke'		:	Cyntec_C10_Choke		,
                        'Cyntec_C20_Choke'		:	Cyntec_C20_Choke		,
                    	'Cyntec_EB2_Choke'		:	Cyntec_EB2_Choke
					}

AllMagnetics	=	{
						'TDK_A20_Trafo'			:	TDK_A20_Trafo			,
                    	'Cyntec_B10_Trafo'		:	Cyntec_B10_Trafo		,
						'Cyntec_B20_Trafo' 		: 	Cyntec_B20_Trafo		,
                    	'Cyntec_B21_Trafo'		:	Cyntec_B21_Trafo		,
                        'Cyntec_C10_Trafo'		:	Cyntec_C10_Trafo		,
                        'Cyntec_C20_Trafo'		:	Cyntec_C20_Trafo		,
                    	'Cyntec_EB2_Trafo'		:	Cyntec_EB2_Trafo		,
						'DS_P100076_Trafo'		:	DS_P100076_Trafo		,
                        'TDK_A20_Choke'			:	TDK_A20_Choke			,
                    	'Cyntec_B10_Choke'		:	Cyntec_B10_Choke		,
                    	'Sumida_B10_Choke'		:	Sumida_B10_Choke		,
						'Cyntec_B20_Choke' 		: 	Cyntec_B20_Choke		,
                    	'Cyntec_B21_Choke'		:	Cyntec_B21_Choke		,
                        'Cyntec_C10_Choke'		:	Cyntec_C10_Choke		,
                        'Cyntec_C20_Choke'		:	Cyntec_C20_Choke		,
                    	'Cyntec_EB2_Choke'		:	Cyntec_EB2_Choke
					}

#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?						 _____                      ____                                _
#?						|  ___|   _ ___  ___  ___  |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___
#?						| |_ | | | / __|/ _ \/ __| | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?						|  _|| |_| \__ \  __/\__ \ |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?						|_|   \__,_|___/\___||___/ |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs fuses models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Dependencies as dp

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#! Call the Post-Processing class and point to the location of csv data
postProcessing 		=	dp.PP.Processing()
FusesDissipation	=	'Script/Data/Fuses_Dissipation/'

#! Fuses models parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

fuse 	=	FusesDissipation + 'MEV55C'
loss	=	postProcessing.extractArrays(fuse)

MEV55C				=	{																																	#*	MEV55C parameters
							'Config'						:	2																						,	#?	1->enable | 2->short | 3->open
							'Type'							:	5																						,	#?	1->real-inductive | 2->ideal | 3->real-resistive | 4->pass | 5->short
							'Ron'							:	2.88e-3																					,	#?	constant on-state resistance
							'Roff'							:	1e9																						,	#?	constant off-state resistance
							'L'								:	1e-9																					,	#?	fuse series inductance
							'tau'							:	40e-9																					,	#?	fuse opening time constant
							'I2t'							:	6000																					,	#?	fuse I2t threshold
							'RatedCurrent'					:	30																						,	#?	DC rated current
							'Dissipation'			:	{																									#!	power dissipation parameters
								'RatedCurrentPercent'		:	50.0																					,	#?	percentage of rated current where loss is given
								'Loss'						:	0.65																					,	#?	loss at given percentage of rated current
								'CurrentVec'				:	loss[0]																					,	#?	percentage vector of rated current
								'LossVec'					:	loss[1]																						#?	loss factor vector based on current flow
							},
                            'TimeVec'						:	[0, 1]																					,	#? 	time vector for activation of fuse
							'OutVec'						:	[1, 1]																					,	#? 	enable vector for activation of fuse
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SFH400C				=	{																																	#*	SFH400C parameters
							'Config'						:	1																						,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->short
							'Ron'							:	35e-6																					,	#?	constant on-state resistance
							'Roff'							:	5e9																						,	#?	constant off-state resistance
							'L'								:	30e-9																					,	#?	fuse series inductance
                            'Cr_parallel'   	  			:	0																						, 	#?	parasitic capacitance between plates
							'Rr_parallel'   	  			:	0																						, 	#?	parasitic ESR between plates
							'tau'							:	0																						,	#?	fuse opening time constant
							'TonFlight'						:	0																						,	#?	switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'						:	0																						,	#?	switching time constant in which inductor is magnetised
							'TonBounce'						:	0																						,	#?	switching time constant in which relay metal plate is bouncing at contact
							'Toff'							:	0																						,	#?	switching time constant in which relay switches to off state
							'Fbounce'						:	0																						,	#?	bounce frequency
							'DutyCycle'						:	0																						,	#?	bounce dutycycle
                            'TimeVec'						:	[0, 1]																					,	#? 	time vector for activation of fuse
							'OutVec'						:	[1, 1]																					,	#? 	enable vector for activation of fuse

						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

EVQGL63				=	{																																	#*	EVQGL63 parameters
							'Config'						:	1																						,	#?	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->short
							'Ron'							:	2.88e-3																					,	#?	constant on-state resistance
							'Roff'							:	1e9																						,	#?	constant off-state resistance
							'L'								:	1e-9																					,	#?	fuse series inductance
							'Cr_parallel'   	  			:	0																						, 	#?	parasitic capacitance between plates
							'Rr_parallel'   	  			:	0																						, 	#?	parasitic ESR between plates
							'tau'							:	0																						,	#?	fuse opening time constant
							'TonFlight'						:	0																						,	#?	switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'						:	0																						,	#?	switching time constant in which inductor is magnetised
							'TonBounce'						:	0																						,	#?	switching time constant in which relay metal plate is bouncing at contact
							'Toff'							:	0																						,	#?	switching time constant in which relay switches to off state
							'Fbounce'						:	0																						,	#?	bounce frequency
							'DutyCycle'						:	0																						,	#?	bounce dutycycle
                            'TimeVec'						:	[0, 1]																					,	#? 	time vector for activation of fuse
							'OutVec'						:	[1, 1]																					,	#? 	enable vector for activation of fuse
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

SCH4KAA				=	{																																	#*	SCH4KAA parameters
							'Config'						:	1																						,	#!	1->Real-Inductive | 2->Ideal | 3->Real-Resistive | 4->Pass | 5->short
							'Ron'							:	100e9																					,	#!	constant on-state resistance
							'Roff'							:	50e-3																					,	#!	constant off-state resistance
							'L'								:	1e-9																					,	#!	fuse series inductance
							'Cr_parallel'   	  			:	0																						, 	#?	parasitic capacitance between plates
							'Rr_parallel'   	  			:	0																						, 	#?	parasitic ESR between plates
							'tau'							:	0																						,	#?	fuse opening time constant
							'TonFlight'						:	0																						,	#?	switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'						:	0																						,	#?	switching time constant in which inductor is magnetised
							'TonBounce'						:	0																						,	#?	switching time constant in which relay metal plate is bouncing at contact
							'Toff'							:	0																						,	#?	switching time constant in which relay switches to off state
							'Fbounce'						:	0																						,	#?	bounce frequency
							'DutyCycle'						:	0																						,	#?	bounce dutycycle
                            'TimeVec'						:	[0, 1]																					,	#? 	time vector for activation of fuse
							'OutVec'						:	[1, 1]																					,	#? 	enable vector for activation of fuse
						}

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#!	assemble all fuses to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PassiveFuses 	=	{
						'MEV55C' 				: 	MEV55C 					,
					}

ActiveFuses 	= 	{
                    	'SFH400C' 				: 	SFH400C					,
                    	'EVQGL63'				:	EVQGL63					,
                    	'SCH4KAA'				: 	SCH4KAA					,
					}

AllFuses 		= 	{
						'MEV55C' 				: 	MEV55C 					,
                    	'SFH400C' 				: 	SFH400C					,
                    	'EVQGL63'				:	EVQGL63					,
                    	'SCH4KAA'				: 	SCH4KAA					,
					}
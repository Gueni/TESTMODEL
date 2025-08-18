#?---------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#?                                        _____      _               _____                               _                
#?                                        |  __ \    | |             |  __ \                             | |               
#?                                        | |__) |___| | __ _ _   _  | |__) |_ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___ 
#?                                        |  _  // _ \ |/ _` | | | | |  ___/ _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?                                        | | \ \  __/ | (_| | |_| | | |  | (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?                                        |_|  \_\___|_|\__,_|\__, | |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?                                                            __/ |                                                       
#?                                                            |___/    
#?----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs relay models.
#!   Do not modify the values in this file.
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------import dependencies

import Dependencies as dp

#------------------

#! Relay models parameters
#!----------------------------------------------------------------------------------------------------------------------------------------------------------------------
EVRBA50CI			=	{																										#!	Main plus relay configuration
							'Ron' 	  				: 1e-3																	, 	#?	relay closed-state resistance
							'Roff'					: 1e9																	,	#?	relay open-state resistance
							'L'   	  				: 10e-9																	, 	#?	relay inductance
							'Cr_parallel'   	  	: 1e-9																	, 	#?	relay parasitic capacitance between plates
							'Rr_parallel'   	  	: 1e-3																	, 	#?	relay parasitic ESR between plates
							'tau'					: 20e-3																	,	#?	relay switching time constant
							'TonFlight'				: 3.6e-3																,	#?	relay switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'				: 3.6e-3																,	#?	relay switching time constant in which inductor is magnetised
							'TonBounce'				: 2.6e-3																,	#?	relay switching time constant in which relay metal plate is bouncing at contact
							'Toff'					: 10e-3																	,	#?	relay switching time constant in which relay switches to off state
							'Fbounce'				: 2e-3																	,	#?	relay bounce frequency
							'DutyCycle'				: 0.5																	,	#?	relay bounce dutycycle
							'TimeVec' 				: [0, 1]	  															, 	#?	relay time control vector
							'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
						}

EVRBE400CIS5		=	{																										#!	Main plus relay configuration
							'Ron' 	  				: 150e-6																, 	#?	relay closed-state resistance
							'Roff'					: 1e9																	,	#?	relay open-state resistance
							'L'   	  				: 10e-9																	, 	#?	relay inductance
							'Cr_parallel'   	  	: 1e-9																	, 	#?	relay parasitic capacitance between plates
							'Rr_parallel'   	  	: 1e-3																	, 	#?	relay parasitic ESR between plates
							'tau'					: 17e-9																	,	#?	relay switching time constant
							'TonFlight'				: 3.6e-3																,	#?	relay switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'				: 3.6e-3																,	#?	relay switching time constant in which inductor is magnetised
							'TonBounce'				: 2.6e-3																,	#?	relay switching time constant in which relay metal plate is bouncing at contact
							'Toff'					: 5e-3																	,	#?	relay switching time constant in which relay switches to off state
							'Fbounce'				: 2e-3																	,	#?	relay bounce frequency
							'DutyCycle'				: 0.5																	,	#?	relay bounce dutycycle
							'TimeVec' 				: [0, 1]	  															, 	#?	relay time control vector
							'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
						}

EVRBE10UG			=	{																										#!	Main plus relay configuration
							'Ron' 	  				: 50e-3																	, 	#?	relay closed-state resistance
							'Roff'					: 1000e9																,	#?	relay open-state resistance
							'L'   	  				: 10e-9																	, 	#?	relay inductance
							'Cr_parallel'   	  	: 1e-9																	, 	#?	relay parasitic capacitance between plates
							'Rr_parallel'   	  	: 1e-3																	, 	#?	relay parasitic ESR between plates
							'tau'					: 20e-9																	,	#?	relay switching time constant
							'TonFlight'				: 3.6e-3																,	#?	relay switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'				: 3.6e-3																,	#?	relay switching time constant in which inductor is magnetised
							'TonBounce'				: 2.6e-3																,	#?	relay switching time constant in which relay metal plate is bouncing at contact
							'Toff'					: 10e-3																	,	#?	relay switching time constant in which relay switches to off state
							'Fbounce'				: 2e-3																	,	#?	relay bounce frequency
							'DutyCycle'				: 0.5																	,	#?	relay bounce dutycycle
							'TimeVec' 				: [0, 1]	  															, 	#?	relay time control vector
							'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
						}

PierburgHVC			=	{																										#!	Main plus relay configuration
							'Ron' 	  				: 200e-6																, 	#?	relay closed-state resistance
							'Roff'					: 100e9																	,	#?	relay open-state resistance
							'L'   	  				: 10e-9																	, 	#?	relay inductance
							'Cr_parallel'   	  	: 1e-9																	, 	#?	relay parasitic capacitance between plates
							'Rr_parallel'   	  	: 1e-3																	, 	#?	relay parasitic ESR between plates
							'tau'					: 17e-9																	,	#?	relay switching time constant
							'TonFlight'				: 3.6e-3																,	#?	relay switching time constant in which relay metal plate is not connected to another plate
							'TonDelay'				: 3.6e-3																,	#?	relay switching time constant in which inductor is magnetised
							'TonBounce'				: 2.6e-3																,	#?	relay switching time constant in which relay metal plate is bouncing at contact
							'Toff'					: 5e-3																	,	#?	relay switching time constant in which relay switches to off state
							'DutyCycle'				: 0.5																	,	#?	relay bounce dutycycle
							'Fbounce'				: 2e-3																	,	#?	relay bounce frequency
							'TimeVec' 				: [0, 1]	  															, 	#?	relay time control vector
							'OutVec'  				: [1, 1]        														    #?	relay status vector, 0->open | 1->closed
						}



#!	assemble all relays to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AllRelays = {
                'EVRBA50CI'         	:   EVRBA50CI,
                'EVRBE400CIS5'     		:   EVRBE400CIS5,
                'EVRBE10UG'         	:   EVRBE10UG,
                'PierburgHVC'      		:   PierburgHVC,
            }
















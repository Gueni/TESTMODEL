
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                        ____        _   _                    ____                                _
#?                                       | __ )  __ _| |_| |_ ___ _ __ _   _  |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___
#?                                       |  _ \ / _` | __| __/ _ \ '__| | | | | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?                                       | |_) | (_| | |_| ||  __/ |  | |_| | |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?                                       |____/ \__,_|\__|\__\___|_|   \__, | |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?                                                                     |___/
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs battery models.
#!   Do not modify the values in this file.
#!-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Dependencies as dp

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#! 	call the Params-Processing class and point to the location of csv data
paramProcess		=	dp.PM.ParamProcess()
BatteriesDataPath   =   'Script/Data/Batteries/'

#! 	Battery model parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
current, cat, Rs		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/Rs/','cold_EOL_Rs')
current, cat, R1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R1/','cold_EOL_R1')
current, cat, R2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R2/','cold_EOL_R2')
current, cat, C1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C1/','cold_EOL_C1')
current, cat, C2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C2/','cold_EOL_C2')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'cold_EOL')

CAMEL_230906_cold_EOL   =   {                                                                                                                       #*  CAMEL 230906 cold_EOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]                                 ,   #?  state of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8]                                                                ,   #?  temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  current vector
                                'Cnom'                  :   22                                                                                  ,   #?  cell nominal capacity in Ah
                                'cat'					:	cat                                                                                 ,   #?  Syntax
		                        'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  open circuit voltage's SOC vector
	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/Rs/','warm_EOL_Rs')
current, cat, R1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R1/','warm_EOL_R1')
current, cat, R2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R2/','warm_EOL_R2')
current, cat, C1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C1/','warm_EOL_C1')
current, cat, C2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C2/','warm_EOL_C2')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'warm_EOL')

CAMEL_230906_warm_EOL    =   {                                                                                                                       #*  CAMEL 230906 warm_EOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,1]                               ,   #?  state of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8,10.5,25.7,39.7,59.35]                                           ,   #?  temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  current vector
                                'Cnom'                  :   22                                                                                  ,   #?  cell nominal capacity in Ah
                                'cat'					:	cat                                                                                 ,   #?  Syntax
		                        'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  open circuit voltage's SOC vector
	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/Rs/','warm_BOL_Rs')
current, cat, R1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R1/','warm_BOL_R1')
current, cat, R2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/R2/','warm_BOL_R2')
current, cat, C1		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C1/','warm_BOL_C1')
current, cat, C2		    =	paramProcess.batteryParams(BatteriesDataPath+'CAMEL_230906/C2/','warm_BOL_C2')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'warm_BOL')

CAMEL_230906_warm_BOL    =   {                                                                                                                       #*  CAMEL 230906 warm_BOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,1]                               ,   #?  state of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8,10.5,25.1,25.7,39.7,59.35]                                      ,   #?  temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  current vector
                                'Cnom'                  :   22                                                                                  ,   #?  cell nominal capacity in Ah
                                'cat'					:	cat                                                                                 ,   #?  Syntax
                                'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  open circuit voltage's SOC vector

	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!	assemble all battery data to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AllBatteries			=	{
								'CAMEL_230906_cold_EOL' 	: 	CAMEL_230906_cold_EOL	    ,
								'CAMEL_230906_warm_EOL' 	: 	CAMEL_230906_warm_EOL		,
                                'CAMEL_230906_warm_BOL' 	: 	CAMEL_230906_warm_BOL
							}
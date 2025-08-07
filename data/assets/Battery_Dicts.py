
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                        ____        _   _                    ____                                _
#?                                       | __ )  __ _| |_| |_ ___ _ __ _   _  |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __ ___
#?                                       |  _ \ / _` | __| __/ _ \ '__| | | | | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__/ __|
#?                                       | |_) | (_| | |_| ||  __/ |  | |_| | |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |  \__ \
#?                                       |____/ \__,_|\__|\__\___|_|   \__, | |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|  |___/
#?                                                                     |___/
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!   This Script works as a Parameter dictionary for the plecs LVS battery model.
#!   Do not modify the values in this file.
#!-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Dependencies as dp

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#! 	call the Params-Processing class and point to the location of csv data
paramProcess		=	dp.PM.ParamProcess()
BatteriesDataPath   =   'Script/Data/Batteries/'

#! 	Battery model parameters
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.Battery_Rs(BatteriesDataPath+'CAMEL_230906/Rs/', 'BOL')
current, cat, R1		    =	paramProcess.Battery_R1(BatteriesDataPath+'CAMEL_230906/R1/', 'BOL')
current, cat, R2		    =	paramProcess.Battery_R2(BatteriesDataPath+'CAMEL_230906/R2/', 'BOL')
current, cat, C1		    =	paramProcess.Battery_C1(BatteriesDataPath+'CAMEL_230906/C1/', 'BOL')
current, cat, C2		    =	paramProcess.Battery_C2(BatteriesDataPath+'CAMEL_230906/C2/', 'BOL')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'BOL')

CAMEL_230906_BOL        =   {                                                                                                                       #*  BOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]                                 ,   #?  State of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8,25.1]                                                           ,   #?  Temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  Open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  Current vector
                                'cat'					:	cat                                                                                 ,   #?  Syntax
		                        'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  Open circuit voltage's SOC vector
	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.Battery_Rs(BatteriesDataPath+'CAMEL_230906/Rs/', 'cold_EOL')
current, cat, R1		    =	paramProcess.Battery_R1(BatteriesDataPath+'CAMEL_230906/R1/', 'cold_EOL')
current, cat, R2		    =	paramProcess.Battery_R2(BatteriesDataPath+'CAMEL_230906/R2/', 'cold_EOL')
current, cat, C1		    =	paramProcess.Battery_C1(BatteriesDataPath+'CAMEL_230906/C1/', 'cold_EOL')
current, cat, C2		    =	paramProcess.Battery_C2(BatteriesDataPath+'CAMEL_230906/C2/', 'cold_EOL')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'cold_EOL')

CAMEL_230906_cold_EOL   =   {                                                                                                                       #*  cold_EOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]                                 ,   #?  State of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8]                                                                ,   #?  Temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  Open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  Current vector
                                'cat'					:	cat                                                                                 ,   #?  Syntax
		                        'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  Open circuit voltage's SOC vector
	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.Battery_Rs(BatteriesDataPath+'CAMEL_230906/Rs/', 'new_EOL')
current, cat, R1		    =	paramProcess.Battery_R1(BatteriesDataPath+'CAMEL_230906/R1/', 'new_EOL')
current, cat, R2		    =	paramProcess.Battery_R2(BatteriesDataPath+'CAMEL_230906/R2/', 'new_EOL')
current, cat, C1		    =	paramProcess.Battery_C1(BatteriesDataPath+'CAMEL_230906/C1/', 'new_EOL')
current, cat, C2		    =	paramProcess.Battery_C2(BatteriesDataPath+'CAMEL_230906/C2/', 'new_EOL')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'new_EOL')

CAMEL_230906_new_EOL    =   {                                                                                                                       #*  new_EOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,1]                               ,   #?  State of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8,10.5,25.7,39.7,59.35]                                           ,   #?  Temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,25,40,60]                                                         ,   #?  Open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  Current vector
                                'cat'					:	cat                                                                                 ,   #?  Syntax
		                        'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  Open circuit voltage's SOC vector
	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

current, cat, Rs		    =	paramProcess.Battery_Rs(BatteriesDataPath+'CAMEL_230906/Rs/', 'new_BOL')
current, cat, R1		    =	paramProcess.Battery_R1(BatteriesDataPath+'CAMEL_230906/R1/', 'new_BOL')
current, cat, R2		    =	paramProcess.Battery_R2(BatteriesDataPath+'CAMEL_230906/R2/', 'new_BOL')
current, cat, C1		    =	paramProcess.Battery_C1(BatteriesDataPath+'CAMEL_230906/C1/', 'new_BOL')
current, cat, C2		    =	paramProcess.Battery_C2(BatteriesDataPath+'CAMEL_230906/C2/', 'new_BOL')
OCV, OCV_soc				=	paramProcess.Battery_OCV(BatteriesDataPath+'CAMEL_230906/OCV/', 'new_BOL')

CAMEL_230906_new_BOL    =   {                                                                                                                       #*  new_BOL parameters
		                        'soc'					:	[0.0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,1]                               ,   #?  State of charge vector
                                'temperature'			:	[-28.3,-18.7,-9,0.8,10.5,25.7,39.7,59.35]                                           ,   #?  Temperature vector
                                'OCV_temperature'		:	[-30,-20,-10,0,10,20,30,40]                                                         ,   #?  Open circuit voltage's temperature vector
                                'current'               :   current                                                                             ,   #?  Current vector
                                'cat'					:	cat                                                                                 ,   #?  Syntax
                                'Rs'				    :	Rs                                                                                  ,   #?  Rs values matrix
                                'R1'				    :	R1                                                                                  ,   #?  R1 values matrix
                                'R2'				    :	R2                                                                                  ,   #?  R2 values matrix
                                'C1'				    :	C1                                                                                  ,   #?  C1 values matrix
                                'C2'				    :	C2                                                                                  ,   #?  C2 values matrix
		                        'OCV'					:	OCV                                                                                 ,   #?  OCV values matrix
		                        'OCV_soc'				:	OCV_soc                                                                                 #?  Open circuit voltage's SOC vector

	                        }

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!	assemble all battery data to be transferred to the PLECS model
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AllBatteries			=	{
								'CAMEL_230906_BOL' 		    : 	CAMEL_230906_BOL			,
								'CAMEL_230906_cold_EOL' 	: 	CAMEL_230906_cold_EOL	    ,
								'CAMEL_230906_new_EOL' 	    : 	CAMEL_230906_new_EOL		,
                                'CAMEL_230906_new_BOL' 	    : 	CAMEL_230906_new_BOL
							}

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?												  ____  _     _____ ____ ____    __  __                   _
#?												 |  _ \| |   | ____/ ___/ ___|  |  \/  | __ _ _ __  _ __ (_)_ __   __ _
#?												 | |_) | |   |  _|| |   \___ \  | |\/| |/ _` | '_ \| '_ \| | '_ \ / _` |
#?												 |  __/| |___| |__| |___ ___) | | |  | | (_| | |_) | |_) | | | | | (_| |
#?												 |_|   |_____|_____\____|____/  |_|  |_|\__,_| .__/| .__/|_|_| |_|\__, |
#?												                                             |_|   |_|            |___/
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
# import Dependencies as dp
import collections
import copy
import functools
import json, pathlib
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dictionary of Current Simulation Parameters.
source_mdlvar		= dp.copy.deepcopy(dp.Param_Dicts.ModelVars)

# Calculate cumulative sums for data partitioning
Ycumsum     		= Ycumsum
YLcumsum    		= dp.np.cumsum(dp.Y_Length)

# Simulation Configurations Dictionary.
config_dicts		= { 														
										'Probes'  			: 	source_mdlvar['Common']['Probes']			,
										'ToFile'			:	source_mdlvar['Common']['ToFile']			,
										'PSFBconfigs'  		: 	source_mdlvar['Common']['PSFBconfigs'] 	,
										'RboxConfigs'  		: 	source_mdlvar['Common']['RboxConfigs']
       								}

# Loop over dict and only pop out config_dicts & leave values.
values_dicts 		= dp.msc.Misc().keys_exists(config_dicts,source_mdlvar)	

# Mode of operation used in miscellaneous lib to define the mode of operation (nanmax , absolute , mean ...)
# & the names of the corresponding matrices
Maps_index 			= {	
                            'DCDC_data_mat' 	: [[1,4,5,1,4,5,1,1,1,5,5,1,1],[-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600,-600]] ,
							'DCDC_map_names'	: [	"Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage","Dissipations","Elec_Stats","Temps","Thermal_Stats","Controls"]
						}

# Load JSON mapping files
load_json = lambda subdir, name: json.load(open([file for file in (pathlib.Path.cwd() / "SIGNAL_MAPPING" / subdir).rglob(name)][0]))

# Get Single DC-DC Converter Mappings
DCDC_pmap_Raw       = load_json("DCDC_SINGLE"	, "pmap_Raw.json")
DCDC_pmap_plt       = load_json("DCDC_SINGLE"	, "pmap_plt.json")
DCDC_Constants      = load_json("DCDC_SINGLE"	, "Constants.json")
DCDC_Ctrl_plt       = load_json("DCDC_SINGLE"	, "Ctrl_plt.json")

# Get Dual DC-DC Converter Mappings
DCDC_DUAL_pmap_Raw  = load_json("DCDC_DUAL"		, "pmap_Raw.json")
DCDC_DUAL_pmap_plt  = load_json("DCDC_DUAL"		, "pmap_plt.json")
DCDC_DUAL_Constants = load_json("DCDC_DUAL"		, "Constants.json")
DCDC_DUAL_Ctrl_plt  = load_json("DCDC_DUAL"		, "Ctrl_plt.json")
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
def return_mags(op_dict):
	"""
	Extracts parameters for transformers and chokes based on the given operational dictionary.
	Args:
	    op_dict (dict): Operational dictionary containing model variables.
	Returns:
	    tuple: Tuple containing lists of parameters for transformers and chokes.
	"""
	mdlvdict 		=   op_dict['ModelVars']
	Trafo  			= mdlvdict['DCDC_Rail1']['Trafo']
	Choke  			= mdlvdict['DCDC_Rail1']['Lf']
	match dp.JSON['TF_Config']:
		case 'DCDC_S'	:
			dp.trafo_inputs = [ 
								#? Parameters for the Trafo
								[   # core losses data-------------------------------------------------------
									Trafo['Core']['Temperatures']        			,  # 0  mag_core_temp
									Trafo['Core']['Flux']                			,  # 1  mag_core_flux
									Trafo['Core']['Voltage']             			,  # 2  mag_core_volt
									Trafo['Core']['Loss']                			,  # 3  mag_core_loss
									dp.pmapping['Transformer Flux']                 ,  # 4  flux index
									dp.pmapping['Measured HV Voltage']+dp.Y_list[3] ,  # 5  Volt index
									Trafo['Core']['Temp']                			,  # 6  Core temp
									Trafo['Core']['Factor']              			,  # 7  Gain
									# primary losses data----------------------------------------------------
									Trafo['Winding']['Rpri']['Fvec']     			,  # 8  Pri Fvec
									Trafo['Winding']['Temperatures']     			,  # 9  Pri Temp vec
									Trafo['Winding']['Rpri']['Rvec']     			,  # 10 Pri Rvec
									# [Trafo['Winding']['Rpri']['Temp']]   			,  # 11 Pri Temp
                					[mdlvdict['Thermal']['Twater']] 				,
									# secondary losses data--------------------------------------------------
									Trafo['Winding']['Rsec']['Fvec']     			,  # 12 Pri Fvec
									Trafo['Winding']['Temperatures']     			,  # 13 Pri Temp vec
									Trafo['Winding']['Rsec']['Rvec']     			,  # 14 Pri Rvec
									# [Trafo['Winding']['Rsec']['Temp']]   			,  # 15 Pri Temp
         							[mdlvdict['Thermal']['Twater']]					,
        							dp.pmapping['Transformer Primary Current']		,
                 					dp.pmapping['Transformer Secondary Current']
						        ]
							  ]

			dp.choke_inputs = [
								#? Parameters for the  dc choke
								[   # core losses data-------------------------------------------------------
									Choke['Core']['Temperatures']        			,  # 0  mag_core_temp
									Choke['Core']['Flux']                			,  # 1  mag_core_flux
									Choke['Core']['Voltage']             			,  # 2  mag_core_volt
									Choke['Core']['Loss']                			,  # 3  mag_core_loss
									0                                    			,  #!  flux for the choke
									0                                       		,  #!  voltage for the choke
									Choke['Core']['Temp']                			,  # 6  Core temp
									0 ,#Choke['Core']['Factor']              		,  # 7  Gain is set to 0 to not get core loss here
									# Copper losses data----------------------------------------------------
									Choke['Winding']['Rwind']['Fvec']    			,  # 8  Pri Fvec
									Choke['Winding']['Temperatures']     			,  # 9  Pri Temp vec
									Choke['Winding']['Rwind']['Rvec']    			,  # 10 Pri Rvec
									[Choke['Winding']['Rwind']['Temp']]  			,  # 11 Pri Temp
								    dp.pmapping['DC Choke Current']					,  # 12
									Choke['Winding']['Harmonics']
								]
							]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D' 	:
			dp.trafo_inputs     =   []
			dp.choke_inputs     =   []
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _			:
			dp.tkinter.messagebox.showerror(' Value Error', ' Value Error ! ')
			dp.sys.exit()

	return  dp.trafo_inputs  , dp.choke_inputs

def return_resistances(op_dict):
    """
    Return a list of resistances based on the configuration specified in op_dict.
    
    Calculates equivalent resistances for all components in the power converter
    considering series/parallel combinations and scaling factors.
    
    Args:
        op_dict (dict): Dictionary containing model variables and configuration.
        
    Returns:
        np.ndarray: Array of resistance values for all components in the system.
        
    Raises:
        SystemExit: If an invalid configuration is specified
    """
    
	# Extract model variables dictionary
    model_vars 			= op_dict['ModelVars']
    rail1 				= model_vars['DCDC_Rail1']
    common 				= model_vars['Common']
    
    # Extract component groups for easier access
    RCsnubber 			= rail1['RCsnubber']
    clamp 				= rail1['RCDclamp1']
    freewheeler 		= rail1['FRW']
    
    # Helper function to calculate capacitor equivalent resistance
    cap_resistance 		= lambda cap_config: cap_config['Rsingle'] * (cap_config['nSer'] / cap_config['nPar'])
    resistor_network 	= lambda res_config: res_config['R'] / res_config.get('nPar', 1)
    
    match dp.JSON['TF_Config']:
        case 'DCDC_S':  # Single DC-DC Converter
            dp.Resistances = [
                # Current Transformer
                rail1['CT']['Trafo']['Rpri'],           				# CT Primary winding resistance
                rail1['CT']['Trafo']['Rsec'],           				# CT Secondary winding resistance
                
                # Choke Snubber Network
                cap_resistance(RCsnubber['Choke']['Cs']),     			# Choke snubber capacitor ESR
                resistor_network(RCsnubber['Choke']['Rs']),   			# Choke snubber resistor
                RCsnubber['Choke']['Rpar'],                   			# Choke snubber parallel resistor
                
                # RCD Clamp Network
                cap_resistance(clamp['Cs']),            				# Clamp capacitor ESR
                float(clamp['Rs']['R']),                				# Clamp resistor (single)
                
                # Freewheeling Diode Network
                cap_resistance(freewheeler['BlockingCap']), 			# Freewheeler blocking cap ESR
                freewheeler['Resistor']['R'],               			# Freewheeler resistor
                cap_resistance(freewheeler['ImpedanceCap']),			# Freewheeler impedance cap ESR
                
                # Damping and Sensing
                rail1['Coe1']['Rd'],                    				# Damping resistor
                rail1['LV_currentSense']['R'],          				# LV current sense resistor
                
                # HV Side Capacitors
                cap_resistance(rail1['Cpi']),           				# HV X-cap 1 ESR
                cap_resistance(rail1['Cin']),           				# HV X-cap 2 ESR
                rail1['HV_currentSense']['R'],          				# HV current sense resistor
                cap_resistance(rail1['Cb']),            				# Blocking capacitor ESR
                
                # Transformer Snubber
                cap_resistance(RCsnubber['Trafo']['Cs']), 				# Transformer snubber cap ESR
                resistor_network(RCsnubber['Trafo']['Rs']), 			# Transformer snubber resistor
                
                # MOSFET Snubbers (4 devices)
                4 * cap_resistance(RCsnubber['SR_MOSFET']['Cs']),     	# MOSFET snubber cap ESR
                4 * resistor_network(RCsnubber['SR_MOSFET']['Rs']),   	# MOSFET snubber resistor
                
                # HV Y-Caps (4 capacitors)
                4 * cap_resistance(rail1['Cyi']),       				# HV Y-cap ESR
                
                # LV Full Bridge Snubbers (2 bridges)
                2 * cap_resistance(RCsnubber['LV_FB']['Cs']),     		# LV FB snubber cap ESR
                2 * resistor_network(RCsnubber['LV_FB']['Rs']),   		# LV FB snubber resistor
                
                # HV Snubber Caps (2 capacitors)
                2 * cap_resistance(rail1['Cc']),        				# HV snubber cap ESR
                
                # Output Capacitors
                cap_resistance(rail1['Co']),            				# Output ceramic cap ESR
                cap_resistance(rail1['Coe1']),          				# Output electrolytic cap ESR
                4 * cap_resistance(rail1['Cyo']),       				# Output Y-cap ESR (4 capacitors)
                
                # Voltage Sensing
                (rail1['HV_voltageSense']['Divider']['R1'] + 
                 rail1['HV_voltageSense']['Divider']['R2']), 			# HV voltage divider total resistance
                
                # HV Common Mode Choke (2 windings)
                2 * rail1['HVcmc']['Rwind'],            				# HV CMC winding resistance
                
                # Common Components (LV Filter)
                cap_resistance(common['Coc1']),         				# LV Filter X-cap 1 ESR
                cap_resistance(common['Coc2']),         				# LV Filter X-cap 2 ESR
                cap_resistance(common['Coec2']),        				# LV Filter electrolytic cap ESR
                4 * cap_resistance(common['Cyoc']),     				# LV Filter Y-cap ESR (4 capacitors)
                2 * common['LVdmc']['Rwind'],           				# LV DMC winding resistance (2 windings)
                2 * common['LVcmc']['Rwind'],           				# LV CMC winding resistance (2 windings)
                
                # Busbar Resistances
                common['Busbars_PCB']['LV_Filter']['PlusResistance'],   # Positive busbar resistance
                common['Busbars_PCB']['LV_Filter']['MinusResistance']   # Negative busbar resistance
            ]
            
        case 'DCDC_D':  # Dual DC-DC Converter
            dp.Resistances = []  # To be implemented
            
        case _:  # Invalid configuration
            dp.tkinter.messagebox.showerror('Resistances Value Error', 'Resistances Value Error!')
            dp.sys.exit()

    return dp.np.array(dp.Resistances)

def tofile_map_gen(mapping_Raw, lengths):
	"""
    Generates two ordered dictionaries of mappings from a raw mapping list and segment lengths.
    
    Processes raw mapping data into structured ordered dictionaries with different indexing schemes.
    The 3D mapping uses zero-based indexing while the multiple mapping uses continuous indexing.
    
    Args:
        mapping_Raw (list): Raw mapping data as a list of elements to be partitioned
        lengths (list): List of integers representing lengths for each segment partition
                        The sum of lengths must be <= length of mapping_Raw
        
    Returns:
        tuple: Contains two ordered dictionaries:
            - Tofile_mapping_3D: OrderedDict with zero-based indexing for each segment
            - Tofile_mapping_multiple: OrderedDict with continuous indexing across segments
	"""
	# c: segment counter, idx_shift: starting index for multiple mapping
	c, idx_shift 			= 0, 1

	# Names for each mapping segment
	Maps_names 				= ["Peak_Currents", "Peak_Voltages", "Dissipations", "Elec_Stats", "Temps", "Thermal_Stats", "Controls"]

	# Initialize ordered dictionaries for mappings
	Tofile_mapping_3D 		= collections.OrderedDict()
	Tofile_mapping_multiple = collections.OrderedDict()

	for i in range(1, len(lengths)):
		# Extract segment from raw mapping data
		segment 									= copy.deepcopy(mapping_Raw[c + 1:lengths[i] + c + 1])

        # Create mapping with zero-based indexing for 3D dictionary
		Tofile_mapping_3D[Maps_names[i - 1]] 		= collections.OrderedDict(zip(segment, range(0, len(segment))))

        # Create mapping with continuous indexing for multiple dictionary  
		Tofile_mapping_multiple[Maps_names[i - 1]] 	= collections.OrderedDict(zip(segment, range(idx_shift, len(segment) + idx_shift)))

		# Update counters for next segment
		c 			+= lengths[i]
		idx_shift	+= lengths[i]

	return Tofile_mapping_3D, Tofile_mapping_multiple

def gen_pmap_plt():
    """
    Generates plot mapping dictionaries for the HTML report.
    
    This function creates two dictionaries that map measurement parameters to plot configurations:
    - pmap_plt_dict: Maps power stage measurements (currents, voltages) to plot configurations
    - pmap_plt_ctrl_dict: Maps control loop measurements to plot configurations
    
    Returns:
        tuple: (pmap_plt_dict, pmap_plt_ctrl_dict) - Two ordered dictionaries containing plot mappings
    """

    # Initialize ordered dictionaries to maintain insertion order
    pmap_plt_dict, pmap_plt_ctrl_dict = dp.OrderedDict(), dp.OrderedDict()

    # Handle different converter configurations
    match dp.JSON['TF_Config']:

        case 'DCDC_S':  # Single DC-DC Converter

            # Process control loop plots for single DC-DC converter
            for i in range(1, len(DCDC_Ctrl_plt)):  # Skip header row (index 0) ["PWM", "Measurments", "ADC", "Sampling", "SW Protection", "HW Protection"],

                # Create dictionary entry for each control plot category
                pmap_plt_ctrl_dict[f'{DCDC_Ctrl_plt[0][i-1]}'] = [
                    [
                        # Parameter names
                        DCDC_Ctrl_plt[i][j][1],

                        # Plot title with parameter mappings
                        [f"{str(DCDC_Ctrl_plt[i][j][0])} ({', '.join(str(item) for item in [str(dp.pmapping[f'{DCDC_Ctrl_plt[i][j][1][k]}']) for k in range(len(DCDC_Ctrl_plt[i][j][1]))])})"],
                        
						# Parameter indices from pmapping
                        [dp.pmapping[f'{DCDC_Ctrl_plt[i][j][1][k]}'] for k in range(len(DCDC_Ctrl_plt[i][j][1]))],
                        
						# Y-axis labels (repeated for each parameter)
                        DCDC_Ctrl_plt[i][j][2] * len(DCDC_Ctrl_plt[i][j][1])
                   
				    ] for j in range(len(DCDC_Ctrl_plt[i]))
                ]

            # Process power stage plots for single DC-DC converter
            for i in range(len(DCDC_pmap_plt)):

                pmap_plt_dict[f'{DCDC_pmap_plt[i][0]}'] = [

                    # Current plot configuration
                    [
                        [f'{DCDC_pmap_plt[i][1]}'],  # Current parameter
                        [f'{DCDC_pmap_plt[i][0]}' + " Current" + '(' + str(dp.pmapping[f'{DCDC_pmap_plt[i][1]}']+1) + ')'],  # Title with mapping
                        [dp.pmapping[f'{DCDC_pmap_plt[i][1]}']],  # Parameter index
                        ['[ A ]']  # Y-axis unit
                    ],

                    # Voltage plot configuration  
                    [
                        [f'{DCDC_pmap_plt[i][2]}'],  # Voltage parameter
                        [f'{DCDC_pmap_plt[i][0]}' + " Voltage" + '(' + str(dp.pmapping[f'{DCDC_pmap_plt[i][2]}']+1) + ')'],  # Title with mapping
                        [dp.pmapping[f'{DCDC_pmap_plt[i][2]}']],  # Parameter index
                        ['[ V ]']  # Y-axis unit
                    ]
                ]

        #------------------------------------------------------------------------------------------------------------------------------------------
        case 'DCDC_D':  # Dual DC-DC Converter

            # Process control loop plots for dual DC-DC converter
            for i in range(1, len(DCDC_DUAL_Ctrl_plt)):  # Skip header row (index 0) ["PWM", "Measurments", "ADC", "Sampling", "SW Protection", "HW Protection"],

                pmap_plt_ctrl_dict[f'{DCDC_DUAL_Ctrl_plt[0][i-1]}'] = [
                    [
                        # Parameter names
                        DCDC_DUAL_Ctrl_plt[i][j][1],

                        # Plot title with parameter mappings
                        [f"{str(DCDC_DUAL_Ctrl_plt[i][j][0])} ({', '.join(str(item) for item in [str(dp.pmapping[f'{DCDC_DUAL_Ctrl_plt[i][j][1][k]}']) for k in range(len(DCDC_DUAL_Ctrl_plt[i][j][1]))])})"],
                       
					    # Parameter indices from pmapping
                        [dp.pmapping[f'{DCDC_DUAL_Ctrl_plt[i][j][1][k]}'] for k in range(len(DCDC_DUAL_Ctrl_plt[i][j][1]))],
                       
					    # Y-axis labels (repeated for each parameter)
                        DCDC_DUAL_Ctrl_plt[i][j][2] * len(DCDC_DUAL_Ctrl_plt[i][j][1])

                    ] for j in range(len(DCDC_DUAL_Ctrl_plt[i]))
                ]

            # Process power stage plots for dual DC-DC converter
            for i in range(len(DCDC_DUAL_pmap_plt)):

                if len(DCDC_DUAL_pmap_plt[i]) == 5:
                    # Configuration for dual measurements (two currents, two voltages)
                    pmap_plt_dict[f'{DCDC_DUAL_pmap_plt[i][0]}'] = [
                     
					    # Dual current plot configuration
                        [
                            [f'{DCDC_DUAL_pmap_plt[i][1]}', f'{DCDC_DUAL_pmap_plt[i][2]}'],  # Two current parameters
                            [f'{DCDC_DUAL_pmap_plt[i][0]}' + " Current" + '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']+1) + ')' +
                             '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']+1) + ')'],  # Combined title
                            [dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}'], dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']],  # Parameter indices
                            ['[ A ]', '[ A ]']  # Y-axis units
                        ],
                       
					    # Dual voltage plot configuration
                        [
                            [f'{DCDC_DUAL_pmap_plt[i][3]}', f'{DCDC_DUAL_pmap_plt[i][4]}'],  # Two voltage parameters
                            [f'{DCDC_DUAL_pmap_plt[i][0]}' + " Voltage" + '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][3]}']+1) + ')' +
                             '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][4]}']+1) + ')'],  # Combined title
                            [dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][3]}'], dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][4]}']],  # Parameter indices
                            ['[ V ]', '[ V ]']  # Y-axis units
                        ]
                    ]
                else:
                    # Configuration for single measurements (one current, one voltage)
                    pmap_plt_dict[f'{DCDC_DUAL_pmap_plt[i][0]}'] = [
                       
					    # Current plot configuration
                        [
                            [f'{DCDC_DUAL_pmap_plt[i][1]}'],  # Current parameter
                            [f'{DCDC_DUAL_pmap_plt[i][0]}' + " Current" + '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']+1) + ')'],  # Title
                            [dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][1]}']],  # Parameter index
                            ['[ A ]']  # Y-axis unit
                        ],
                       
					    # Voltage plot configuration
                        [
                            [f'{DCDC_DUAL_pmap_plt[i][2]}'],  # Voltage parameter
                            [f'{DCDC_DUAL_pmap_plt[i][0]}' + " Voltage" + '(' + str(dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']+1) + ')'],  # Title
                            [dp.pmapping[f'{DCDC_DUAL_pmap_plt[i][2]}']],  # Parameter index
                            ['[ V ]']  # Y-axis unit
                        ],
                    ]

        #------------------------------------------------------------------------------------------------------------------------------------------------------------------
        case _:  # Default Case - Invalid configuration
            dp.tkinter.messagebox.showerror('ModelVar Value Error', 'dp.Config Value Error ! ')
            dp.sys.exit()

    return pmap_plt_dict, pmap_plt_ctrl_dict
	
def dump_headers(raw_dict, names):
    """
    Process and dump header information to JSON files.
    
    This function processes raw header data, applies various transformations,
    and saves the results to multiple JSON files organized by data categories.
    
    Args:
        raw_dict: Dictionary containing raw header data
        names: Identifier used to lookup file naming conventions in Maps_index
    """
    # Initialize counter for tracking position in processed data
	# and lambda function for appending suffixes
    c 				= 0
    add_str 		= lambda lst, s: [x + s for x in lst]
    
    # Remove specific ranges from raw data to create time series header
    # Delete elements from the end (last Y_list element + 1) and Y_Length[10] elements after that
    ts_header 		= dp.np.delete(dp.np.array(raw_dict),dp.np.r_[-(dp.Y_list[-1]+1):-(dp.Y_list[-1]+1)+dp.Y_Length[12]])
    
	# Delete additional range from Ycumsum[2] to Ycumsum[2] + Y_Length[9]
    ts_header   	= dp.np.delete(ts_header,dp.np.r_[Ycumsum[2]:Ycumsum[2]+dp.Y_Length[9]]).tolist()
    
    # Save the processed time series header to file with each element on new line
    with open(dp.Header_File, 'w') as f:
        for item in ts_header:
            dp.json.dump(item, f)
            f.write('\n')
    
    # Define slices for different data categories with corresponding suffixes
    slices 			= [
    				slice(1, dp.Y_list[1]+1)		,	# 
    				slice(1, dp.Y_list[1]+1)		,	# 
    				slice(Ycumsum[1], Ycumsum[2])	,	# 
    				slice(Ycumsum[1], Ycumsum[2])	,	# 
    				slice(1, dp.Y_list[1]+1)		,	# 
    				slice(Ycumsum[1], Ycumsum[2])		# 
    			]
    suffixes 		= [' RMS', ' AVG', ' RMS', ' AVG', '', '']
	
    # Get lengths for each segment from cumulative Y_Length values
    lengths 		= YLcumsum[[1, 2, 4, 5, 6, 7]].tolist()
    
    # Process each segment: add suffix and pair with insertion length
    sublists 		= [(add_str(raw_dict[s], suf), l) for s, suf, l in zip(slices, suffixes, lengths)]
    
	# Build temporary dictionary by inserting processed segments at specified positions
    temp_raw_dict 	= functools.reduce(lambda acc, x: dp.np.insert(acc, x[1], dp.np.array(x[0])), sublists, dp.np.array(raw_dict)).tolist()
    
    # Save each data category to separate JSON files with each element on new line
    for i, length in enumerate(dp.Y_Length[1:], 1):
        # Generate filename based on mapping index
        header_file = f"Script/assets/HEADER_FILES/{Maps_index[names][i-1]}.json"
    
	    # Write segment data to file with each element on new line
        with open(header_file, 'w') as file:
            for item in temp_raw_dict[c+1:c+1+length]:
                dp.json.dump(item, file)
                file.write('\n')
        c += length

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
                  
			# Lengths related to all exported and calculated data and Lengths related to plecs output only.
			dp.Y_Length            		=  [1,77,77,77,69,69,69,77,69,62,15,18,8,148]
			dp.Y_list              		=  [1,77,69,25,15,18,148]
			
			# Output power Index in Electstat maps.
			dp.Pout_idx            		=  13
			dp.Rail_idx            		=  15
			dp.Common_idx          		=  53
                  
			# Number of phases : single , dual ...
			dp.phase               		=  2
                  
			# Index up to which all currents related to resistive loads.
			dp.current_idx         		=  37
                  
            # Number of columns of commun data (exp : LV filter).
			dp.com_cols            		=  6
            
			# Generate json header files.
			dump_headers(DCDC_pmap_Raw,'DCDC_map_names')
            
			# Adjust the raw mapping by removing specific ranges
			DCDC_pmap_Raw 				= dp.np.delete(dp.np.array(DCDC_pmap_Raw),dp.np.r_[Ycumsum[2]:Ycumsum[2] + dp.Y_Length[9]]).tolist()
			DCDC_pmap_Raw 				= dp.np.delete(dp.np.array(DCDC_pmap_Raw),dp.np.r_[-(dp.Y_list[-1]+1) : -(dp.Y_list[-1]+1) + dp.Y_Length[12]]).tolist()
			
			# Generate DCDC mapping dicts both for 3D and multiple plots.
			dp.pmapping 				= collections.OrderedDict(zip(DCDC_pmap_Raw, range(0, len(DCDC_pmap_Raw))))
			dp.pmap_3D,dp.pmap_multi	= tofile_map_gen(DCDC_pmap_Raw,dp.Y_list)

			# Generate PWM dictionary from specific slice of the mapping      
			pwm_slice 					= DCDC_pmap_Raw[DCDC_pmap_Raw.index("PWM Modulator Primary PWM Outputs S1"):DCDC_pmap_Raw.index("PWM Modulator Auxiliary PWM Outputs Sdis")]
			dp.pwm_dict 				= dp.OrderedDict(zip(pwm_slice, map(DCDC_pmap_Raw.index, pwm_slice)))
			
			# Generate DCDC html plots mapping dict & ctrls mapping.
			dp.pmap_plt,dp.pmap_plt_ctrl= gen_pmap_plt()	
			
			# Generate constant dictionary 
			dp.constant_dict 			= collections.OrderedDict((sub[0], [sub[0], dp.pmapping[sub[0]], sub[1]]) for sub in DCDC_Constants)

			# Set plot title list and index range for 			
			dp.plt_title_list  			= DCDC_pmap_plt
			dp.idx_start,dp.idx_end     = 53,61

			# Remove specific unwanted strings from FFT_Current.json
			strings_to_remove			=  ['HV Left-Leg ON Current'							,
                           					'HV Left-Leg OFF Current'							,
                           					'HV Left-Leg Max Current1'							,
											'HV Left-Leg Max Current2'							,
											'HV Right-Leg ON Current'							,
         									'HV Right-Leg OFF Current'							,
         									'HV Right-Leg Max Current1'							,
											'HV Right-Leg Max Current2'
]
			dp.json.dump(list(filter(lambda x: x.lower() not in set(map(str.lower, strings_to_remove)),dp.json.load(open("Script/assets/HEADER_FILES/FFT_Current.json")))),open("Script/assets/HEADER_FILES/FFT_Current.json", 'w'))

			# Define slices for matrix operations
			dp.slices = [
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[3], Ycumsum[4])        , #? elect_stats Slice
				slice(Ycumsum[4], Ycumsum[5])        , #? Temp        Slice
				slice(Ycumsum[5], Ycumsum[6])          #? CTRL        Slice
			]
                  
			# Define matrix operations using the slices
			dp.matrix_ops = [(f"MAT{b}", dp.mode[b-1], dp.slices[c]) for b ,c in zip([1,2,3,4,5,6,10,11,13] ,[0,1,2,3,4,5,6,7,8,9])]
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case 'DCDC_D' 	:	#? Assign dual rail mapping
                  
			# Lengths related to all exported and calculated data and Lengths related to plecs output only.
			dp.Y_Length            		=  [1,136,136,136,120,120,120,136,120,1,17,1,8,292]
			dp.Y_list              		=  [1,136,120,1,17,1,292]
			
			# Output power Index in Electstat maps.
			dp.Pout_idx            		=  0
			dp.Rail_idx            		=  0
			dp.Common_idx          		=  0
                  
			# Number of phases : single , dual ...
			dp.phase               		=  2
                  
			# Index up to which all currents related to resistive loads.
			dp.current_idx         		=  0
                  
            # Number of columns of commun data (exp : LV filter).
			dp.com_cols            		=  0
            
			# Generate json header files.
			dump_headers(DCDC_DUAL_pmap_Raw,'DCDC_map_names')
			
			# Generate DCDC mapping dicts both for 3D and multiple plots.
			dp.pmapping 				= collections.OrderedDict(zip(DCDC_DUAL_pmap_Raw, range(0, len(DCDC_pmap_Raw))))
			dp.pmap_3D,dp.pmap_multi	= tofile_map_gen(DCDC_DUAL_pmap_Raw,dp.Y_list)

			# Generate PWM dictionary from specific slice of the mapping      
			pwm_slice 					= DCDC_DUAL_pmap_Raw[DCDC_DUAL_pmap_Raw.index("PWM Modulator Carrier Waveforms 1 Rail 1"):DCDC_DUAL_pmap_Raw.index("PWM Modulator Auxiliary PWM Outputs Sdis Rail 2")]
			dp.pwm_dict 				= dp.OrderedDict(zip(pwm_slice, map(DCDC_DUAL_pmap_Raw.index, pwm_slice)))
			
			# Generate DCDC html plots mapping dict & ctrls mapping.
			dp.pmap_plt,dp.pmap_plt_ctrl= gen_pmap_plt()
			
			# Generate constant dictionary 
			dp.constant_dict 			= collections.OrderedDict((sub[0], [sub[0], dp.pmapping[sub[0]], sub[1]]) for sub in DCDC_DUAL_Constants)

			# Set plot title list and index range for 			
			dp.plt_title_list  			= DCDC_DUAL_pmap_plt
			dp.idx_start,dp.idx_end     = 97,113

			# Remove specific unwanted strings from FFT_Current.json
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
			dp.json.dump(list(filter(lambda x: x.lower() not in set(map(str.lower, strings_to_remove)),dp.json.load(open("Script/assets/HEADER_FILES/FFT_Current.json")))),open("Script/assets/HEADER_FILES/FFT_Current.json", 'w'))

			# Define slices for matrix operations
			dp.slices = [
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(1, dp.Y_list[1] + 1)           , #? Currents    Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[1], Ycumsum[2])        , #? voltage     Slice
				slice(Ycumsum[3], Ycumsum[4])        , #? elect_stats Slice
				slice(Ycumsum[4], Ycumsum[5])        , #? Temp        Slice
				slice(Ycumsum[5], Ycumsum[6])          #? CTRL        Slice
			]
                  
			# Define matrix operations using the slices
			dp.matrix_ops = [(f"MAT{b}", dp.mode[b-1], dp.slices[c]) for b ,c in zip([1,2,3,4,5,6,10,11,13] ,[0,1,2,3,4,5,6,7,8,9])]
		#------------------------------------------------------------------------------------------------------------------------------------------------------------------
		case _			:	#? Default Case
			dp.tkinter.messagebox.showerror('ModelVar Value Error', 'TF_Config Value Error ! ')
			dp.sys.exit()
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
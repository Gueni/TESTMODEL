
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                ____    _  _____  _      ____  ____   ___   ____ _____ ____ ____ ___ _   _  ____
#?                               |  _ \  / \|_   _|/ \    |  _ \|  _ \ / _ \ / ___| ____/ ___/ ___|_ _| \ | |/ ___|
#?                               | | | |/ _ \ | | / _ \   | |_) | |_) | | | | |   |  _| \___ \___ \| ||  \| | |  _
#?                               | |_| / ___ \| |/ ___ \  |  __/|  _ <| |_| | |___| |___ ___) |__) | || |\  | |_| |
#?                               |____/_/   \_\_/_/   \_\ |_|   |_| \_\\___/ \____|_____|____/____/___|_| \_|\____|
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
from decimal import Decimal
from scipy.integrate import quad, cumtrapz
from scipy.optimize import minimize, least_squares

class Processing:

    def __init__(self):
        pass

    def gen_result(self, directory_path, itr, utc):
        """
        Read all CSV files in a directory, concatenate their data and return as a single numpy array.

        Parameters:
        -----------
        directory_path : str
            The path to the directory containing CSV files.

        Returns:
        --------
        global_array : numpy.ndarray
            A 2D numpy array containing the concatenated data from all CSV files in the directory. The first column
            of each CSV file is assumed to contain headers and is not included in the resulting array.
        """
        file            = directory_path + f"/results_{utc}_{str(itr+1)}.csv"               # Construct the full file path using directory path, UTC, and iteration
        dataFrame       = dp.pd.read_csv(file, header=None, dtype=str).transpose()          # Read CSV file with no headers as strings and transpose it
        
        try:
            listcols    = (dataFrame.apply(lambda col: col.map(Decimal))).values.tolist()   # Convert each column to Decimal and get values as list
        except Exception:   
            print("Could not apply Decimal.")                                               # Print error message if Decimal conversion fails
            pass
        
        df              = (dp.pd.DataFrame(listcols, dtype=object).transpose()).dropna()    # Convert list to DataFrame, transpose, and drop NAN values
        df.to_csv(file, index=False, header=None, mode='w')                                 # Write the processed DataFrame back to the same CSV file
        return listcols                                                                     # Return the list of Decimal values

    def norm_results(self, results):
        """
        Normalizes simulation results as a single nested array of time and values.

        Args:
            results (list)      : A list of nested dictionaries containing simulation results.

        Returns:
            list                : A nested list of lists containing the normalized simulation results.

        This function takes in a list of nested dictionaries containing simulation results
        and normalizes them into a single nested array of time and values. It finds the length
        of the longest time vector in the input list, iterates through each nested dictionary
        in the input list, and creates a new output list for each simulation, with the time
        vector padded with NaN values to match the length. The function returns a nested list
        of lists containing the normalized simulation results.

        The input `results` list should contain nested dictionaries with the following structure:

        [
            {
                'Time': [time vector],
                'Values': [[value vector 1], [value vector 2], ...]
            },
            {
                'Time': [time vector],
                'Values': [[value vector 1], [value vector 2], ...]
            },
            ...
        ]

        The output of the function will be a nested list of lists with the following structure:

        [
            [normalized time vector 1, normalized value vector 1, normalized value vector 2, ...],
            [normalized time vector 2, normalized value vector 1, normalized value vector 2, ...],
            ...
        ]
        """
        resultsvect     = []                                                                # Initialize empty list to store normalized results
        longest_length  = max(len(results[c]['Time']) for c in range(len(results)))         # Find length of longest time vector
        
        for i in range(len(results)):                                                       # Iterate through each simulation result
            timevector          = results[i]['Time']                                        # Extract time vector for current simulation
            difference_lengths  = longest_length - len(timevector)                          # Calculate padding needed for current time vector
            NaNarray            = dp.np.empty((difference_lengths))                         # Create empty array for NaN padding
            NaNarray[:]         = dp.nan                                                    # Fill padding array with NaN values
            valuesvector        = results[i]['Values']                                      # Extract values vectors for current simulation
            outputresults       = []                                                        # Initialize list for normalized results
            
            timevector          = dp.np.append(NaNarray, timevector)                        # Pad time vector with leading NaNs
            outputresults.append(timevector)                                                # Add padded time vector to output
            
            for j in range(len(valuesvector)):                                              # Iterate through each value vector
                valuesvector[j] = dp.np.append(NaNarray, valuesvector[j])                   # Pad value vector with leading NaNs
                outputresults.append(valuesvector[j])                                       # Add padded value vector to output
                
            resultsvect.append(outputresults)                                               # Add normalized simulation to final results
            
        return resultsvect                                                                  # Return list of normalized simulation results

    def norm_results_csv(self, results):
        """
        Normalize a list of lists by padding shorter sublists with NaN values to match the longest sublist.

        Parameters:
        results (list of lists): A list containing multiple lists of varying lengths.

        Returns:
        list: A list of lists where each sublist has been padded with NaN values to match the longest sublist length.

        Raises:
        ValueError: If the input is not a list of lists.
        """
        resultsvect             = []                                                                        # Initialize empty list for normalized results
        longest_length          = max(map(len, results))                                                    # Determine length of longest sublist
        for sublist in results:                                                                             # Iterate through each sublist in input
            difference_lengths  = longest_length - len(sublist)                                             # Calculate required padding length
            NaNarray            = dp.np.full(difference_lengths, dp.np.nan)                                 # Create NaN padding array
            outputresults       = [dp.np.append(NaNarray, dp.np.array(item)).tolist() for item in sublist]  # Pad each item in sublist with NaNs and convert to list
            resultsvect.append(outputresults)                                                               # Add normalized sublist to results
        return resultsvect                                                                                  # Return list of normalized sublists

    def extractArrays(self, fileName):
        """
        Reads a CSV file that contains comma-separated numerical data and returns the individual columns
        of the CSV file as a nested list.

        Args:
            fileName (str)      : The name of the CSV file to be read, including the file extension. This file
                            should be located in the current working directory.

        Returns:
            list: A nested list containing the individual columns of the CSV file. The outer list is a
                list of columns, where each element of the list is a list of values in that column.

        Raises:
            FileNotFoundError   : If the specified CSV file cannot be found in the current working directory.
            ValueError: If the specified CSV file is empty or does not contain any numerical data.

        Example:
            If the CSV file contains the following data:

            1,2,3
            4,5,6
            7,8,9

            Calling extractArrays('data.csv') will return:

            [[1.0, 4.0, 7.0], [2.0, 5.0, 8.0], [3.0, 6.0, 9.0]]
        """
        path    =   dp.os.getcwd() + '/'                            # Get current working directory path
        array   =   []                                              # Initialize empty list for results
        
        with open(path + fileName + '.csv') as f:                   # Open CSV file (adds .csv extension)
            line            =   f.readline()                        # Read first line of file
            firstRow        =   line.split(",")                     # Split first line by commas
            columnsNumber   =   len(firstRow)                       # Determine number of columns
            
            for i in range(columnsNumber):                          # Initialize each column's list
                array.append([])                                    # Add empty list for current column
                array[i].append((float(firstRow[i])))               # Add first value to column
                
            for row in f:                                           # Process remaining rows
                for i in range(columnsNumber):                      # For each column in row
                    otherRows   =   row.split(",")                  # Split current row by commas
                    array[i].append((float(otherRows[i])))          # Add value to appropriate column
                    
        return array                                                # Return nested list of columns

    def get_index(self, Data: list, Point: float, Index: int) -> int:
        """
        Returns the index of the given target point if found in the data list.

        Args:
        - Data (list)       : A nested list of numerical data.
        - Point (float)     : The target point to search for in the data.
        - Index (int)       : The index of the sub-list in Data to search.

        Returns:
        - int: The index of the closest value to the target point in the specified sub-list of Data.

        Raises:
        - TypeError: If Data is not a list or if Point is not a float.
        - IndexError: If the specified index is out of range for the Data list.
        - ValueError: If the specified sub-list is empty.

        Example:
        data = [[1.1, 2.2, 3.3], [-4.4, -5.5, -6.6], [7.7, 8.8, 9.9]]
        get_index(data, 2.0, 0)
        1
        get_index(data, -5.0, 1)
        1
        get_index(data, 8.8, 2)
        1
        """
        array   =   dp.np.asarray(Data[Index])                      # Convert target sublist to numpy array
        idx     =   dp.np.nanargmin(dp.np.abs(array - Point))       # Find index of closest value to Point
        return idx                                                  # Return the found index

    def csv_append_rows(self, fileName: str, data: list, save_mode: str = 'a') -> None:
        """
        Append the provided ND data array as a row to the specified CSV file.

        Args:
            fileName (str)      : The name of the CSV file to which the data will be appended.
            data (list)         : The ND data array to be appended.
            save_mode (str)     : Optional argument specifying the file open mode. Default value is 'a'
                                which appends data to the end of the file. To overwrite the file, 
                                set save_mode to 'w'.

        Returns:
            None

        Raises:
            TypeError: If the provided data is not a list.
            ValueError: If the provided data is an empty list.
        """
        if not isinstance(data, list):                             # Validate input is a list
            raise TypeError("data should be a list.")              # Raise error if not list
        
        if len(data) == 0:                                         # Check for empty data
            raise ValueError("data list cannot be empty.")         # Raise error if empty
        
        if all(isinstance(i, list) for i in data):                 # Check for nested lists
            df = dp.pd.DataFrame(list(data))                       # Create DataFrame directly
        else:                                                      # For flat lists
            df = dp.pd.DataFrame(data).T                           # Transpose before DataFrame
        
        df.to_csv(fileName,                                       # Write to CSV file
                mode=save_mode,                                   # Use specified save mode
                index=False,                                      # Exclude index column
                header=False)                                     # Exclude header row

    def findIndex(self, points, matrix, pattern=True):
        """
        Finds the starting index for each row/column in a matrix based on a list of points.

        Args:
        - points (list)       : A list of points to search for in the matrix.
        - matrix (list[list]) : A two-dimensional matrix to search for the points in.
        - pattern (bool)      : A boolean flag indicating whether to return a pattern matrix (default True).

        Returns:
        - indices (list)      : A list of indices representing the starting index for each row/column.
        - itr (int)           : The first index in the indices list, calculated differently depending on `pattern`.

        If `pattern=True`:
        - Computes the index of each point in its corresponding row.
        - Computes a weighted sum of these indices based on the length of subsequent rows.

        If `pattern=False`:
        - Finds the index of the first point in the first row.
        - Returns an array filled with this index.
        """
        indices = []                                                                            # Initialize empty list for indices
        if pattern:                                                                             # Pattern mode calculation
            indices = [matrix[i].index(points[i]) for i in range(len(points))]                  # Find the index of each point in its respective row
            
            #? Compute the weighted sum dynamically instead of hardcoding
            itr = sum(
                indices[i] * dp.np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])    # Weighted product
                for i in range(len(indices) - 1)                                                # For all but last index
            ) + indices[-1]                                                                     # Add last index directly
            
            indices.append(itr)                                                                 # Append computed index for reference
        else:                                                                                   # Non-pattern mode
            
            itr = matrix[0].index(points[0])                                                    # Find the index of the first point in the first row
            indices = dp.np.full(len(matrix) + 1, itr).tolist()                                 # Fill with the same value for all positions
        
        return indices, itr                                                                     # Return both indices and primary index

    def findPoint(self, matrix, index, pattern=True):
        """
        Given a matrix and a boolean pattern, returns a numpy array of size (totalLengths, len(matrix))
        containing the matrix values with the proper indexing.

        Args:
        - matrix : a list of lists, containing 10 sublists, each with variable length.
        - pattern (optional) : a boolean value that determines whether to use a pattern or not. Default is True.

        Returns:
        - ParametersMap : a numpy array of size (totalLengths, len(matrix)), containing the matrix values with the proper indexing.
        """
        if not pattern:
            ParametersMap = dp.np.array(matrix[index[-1]:]).T.tolist()                          # Convert slice to array, transpose, and back to list
            return ParametersMap, len(ParametersMap[0])                                         # Return matrix and row count (length of first column)

        lengths = [len(sublist) for sublist in matrix]                                          # Get lengths of each sublist
        totalLengths = dp.np.prod(lengths)                                                      # Calculate total parameter combinations
        ParametersMap = dp.np.zeros((totalLengths, len(matrix)))                                # Initialize result matrix with zeros
        
        step_size = totalLengths                                                                # Initialize step size with total length
        for col, sublist in enumerate(matrix):                                                  # Process each column (parameter)
            step_size //= lengths[col]                                                          # Adjust step size for current parameter
            repeat_factor = totalLengths // (step_size * lengths[col])                          # Calculate repetition factor
            ParametersMap[:, col] = dp.np.tile(dp.np.repeat(sublist, step_size), repeat_factor) # Fill column with properly repeated and tiled values
        
        return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])                        # Return sliced matrix (from index) and its row count

    def findStart(self, matrix, pattern=True):
        """
        Returns a new matrix that starts at the given index.

        Args:
        - matrix (list[list[int]])  : A 2D matrix represented as a list of lists.
        - pattern (bool)            : A boolean flag indicating whether to return a pattern matrix (default True).

        Returns:
        - Matrix (list[list[int]])  : A new matrix that starts at the given index.
        """
        if pattern:
            return [row[:] for row in matrix]                                   # Create new list with copies of each row
        max_len = max(len(row) for row in matrix)                               # Find longest row length
        padded_matrix = [row + [0] * (max_len - len(row)) for row in matrix]    # Pad shorter rows with zeros for each row in matrix
        return dp.np.array(padded_matrix).T.tolist()                            # Convert to array, transpose, and return as list

    def dump_json_data(self, json_file):
        """
        Loads and returns data from a JSON file located in the Script/assets directory.

        Args:
            json_file (str): The name of the JSON file (with extension) to be loaded 
                            from the Script/assets directory.

        Returns:
            dict: A dictionary containing the parsed JSON data from the file.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON data.
        """
        path = dp.os.getcwd().replace("\\", "/") + "/Script/assets/" + json_file    # Construct full path to JSON file in assets directory
        file = open(path, encoding='utf-8')                                         # Open JSON file with UTF-8 encoding to handle special characters
        data = dp.json.load(file)                                                   # Load and convert JSON content to Python dict
        file.close()                                                                # Ensure file handle is properly closed
        return data                                                                 # Return the parsed JSON data

    def rms_avg(self, Op, nested_list, time_values):
        """
        Calculate the Root Mean Square (RMS) or Average (AVG) values for nested lists of signal data.

        Parameters  :
            Op (str)            : Operation selection - 'RMS' for Root Mean Square or 'AVG' for Average.
            nested_list (list)  : Nested list containing signal values.
            time_values (list)  : List of corresponding time values.

        Returns:
            array : List of RMS or AVG values.

        """
        result          =   dp.np.array([])                                                                        # Empty list to store the RMS values
        delta_T         =   time_values[-1] - time_values[0]

        for sublist in nested_list:                                                                                 # Go through all lists of values in the nested list.                                                        # slice time if needed.
            match Op:                                                                                               # Use Op arg to select which operation to execute.
                case 'RMS':                                                                                         #
                    try:
                        squared_values  = (dp.np.array(sublist))**2                                                 # do the square of current.
                        res_value       = dp.np.sqrt(dp.np.trapz(squared_values, x=time_values) / delta_T)          # Calculate the RMS value.
                    except ZeroDivisionError:                                                                       #
                        print("Error: Division by zero is not allowed.")                                            #
                case 'AVG':                                                                                         #
                    try:
                        res_value  = dp.np.trapz(dp.np.array(sublist), x=time_values) / delta_T                     # Calculate the Average value.
                    except ZeroDivisionError:                                                                       #
                        print("Error: Division by zero is not allowed.")                                            #
            try:                                                                                                    #
                result = dp.np.append(result, res_value)                                                            # Append the RMS value to the result list
            except ValueError:                                                                                      #
                print("Error: Invalid input. Please enter valid numbers.")                                          #
        return result                                                                                               #

    def natsorted_list(self, dir):
        """
        Return a list of CSV file paths in the specified directory, sorted naturally (human-order).
        Excludes files ending with '_Map.csv'.

        Parameters:
            dir (str): Directory path to scan for CSV files. Should be a valid directory path.

        Returns:
            list: A naturally sorted list of CSV file paths with forward slashes.

        Raises:
            FileNotFoundError: If the specified directory does not exist.
            NotADirectoryError: If the path exists but is not a directory.
        """
        file_list = []                                                      # Initialize empty list to store file paths
        for filename in dp.os.scandir(dir):                                 # Scan directory and filter CSV files (excluding _Map.csv files)
            if (filename.is_file() and                                      # Check if it's a file (not directory)
                filename.path.endswith('.csv') and                          # Check for .csv extension
                not filename.path.endswith('_Map.csv')):                    # Exclude _Map.csv files
                file_list.append(str(filename.path.replace("\\", "/")))     # Convert paths to forward slashes
        file_list = dp.natsorted(file_list)                                 # Sort files in natural/human order (e.g., file2 comes after file1, not file10)
        return file_list                                                    # Return sorted list of CSV file paths

    def magnetic_loss(self, nestedresults, FFT_current, l, trafo_inputs, choke_inputs):
        """
        Calculate magnetic losses in a transformer system including core losses, primary copper losses, secondary copper losses, and choke losses.

        Parameters  :
            nestedresults (dict)            : Nested results containing flux linkage and voltages for transformers and chokes.
            FFT_current (numpy.ndarray)     : FFT current values.
            l (int)                         : Index for time step or frequency bin.
            trafo_inputs (list)             : List of transformer parameters.
            choke_inputs (list)             : List of choke parameters.

        Returns:
            tuple: Tuple containing core losses, primary copper losses, secondary copper losses, and choke losses.

        """
        core_loss   , pri_copper_loss , sec_copper_loss ,choke_core_loss    ,choke_copper_loss , Choke_loss= [],[],[],[],[],[]
        for i in range(len(trafo_inputs)):
            #! core losses :
            LuT3D         = self.LuT_3D(trafo_inputs[i][0] ,trafo_inputs[i][1],trafo_inputs[i][2],trafo_inputs[i][3])
            flux_link     = nestedresults[trafo_inputs[i][4]]
            point_flux    = dp.np.round((dp.np.max(flux_link)-dp.np.min(flux_link))/2 , decimals=12 )
            point_in_volt = dp.np.max(nestedresults[trafo_inputs[i][5]],axis=0)
            interp        = LuT3D([trafo_inputs[i][6],point_flux ,point_in_volt])
            core_loss.append(interp[0] * trafo_inputs[i][7] )
            #! primary losses :
            LuT2D         = self.LuT_2D(trafo_inputs[i][8],trafo_inputs[i][9],trafo_inputs[i][10])
            rvec_pri      = []
            for j in range(len(dp.harmonics)):
                interpolated_rpri = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][11]*len(dp.harmonics))[j]])
                rvec_pri.append(interpolated_rpri[0])

            pri_copper_loss.append(dp.np.sum(dp.np.array(rvec_pri) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][16]-1] )))
            #! secondary losses :
            LuT2D         = self.LuT_2D(trafo_inputs[i][12],trafo_inputs[i][13],trafo_inputs[i][14])
            rvec_sec      = []
            for j in range(len(dp.harmonics)):
                interpolated_rsec = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][15]*len(dp.harmonics))[j]])
                rvec_sec.append(interpolated_rsec[0])
            sec_copper_loss.append(dp.np.sum(dp.np.array(rvec_sec) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][17]-1] )))
        for i in range(len(choke_inputs)):                                                                                 #? Go over each trafo you have in the system.
            #! choke core losses :
            LuT3D         = self.LuT_3D(choke_inputs[i][0] ,choke_inputs[i][1],choke_inputs[i][2],choke_inputs[i][3])      # Create the 3DLut.
            flux_link     = nestedresults[choke_inputs[i][4]]                                                          # flux linkage .
            point_flux    = (dp.np.max(flux_link)-dp.np.min(flux_link))/2                                                  # Peak value of flux linkage.
            point_in_volt = dp.np.max(nestedresults[choke_inputs[i][5]])                                                # get the voltage.
            interp        = LuT3D([choke_inputs[i][6],point_flux ,point_in_volt])                                          # interplated value.
            choke_core_loss.append(interp[0] * choke_inputs[i][7] )                                                        # append choke_inputs[i][7]*Gain (Factor)
            #! choke copper losses :
            LuT2D         = self.LuT_2D(choke_inputs[i][8],choke_inputs[i][9],choke_inputs[i][10])
            rvec          = []
            for j in range(len(choke_inputs[i][13])):
                interpolated_rpri = LuT2D([(dp.np.array(choke_inputs[i][13])*dp.F_Fund)[j],(choke_inputs[i][11]*len(choke_inputs[i][13]))[j]])
                rvec.append(interpolated_rpri[0])
            choke_copper_loss.append(dp.np.sum( dp.np.array(rvec)   * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),choke_inputs[i][12]-1][choke_inputs[i][13]])) )
            Choke_loss =  [dp.np.sum(choke_core_loss + choke_copper_loss)]
        return dp.np.array(core_loss) , dp.np.array(pri_copper_loss) , dp.np.array(sec_copper_loss) , dp.np.array(Choke_loss)

    def analytical_magnetic_loss(self, nestedresults, FFT_current, l):
        """
        Calculate magnetic losses analytically for transformer core losses, primary copper losses, secondary copper losses, choke core and copper losses.

        Parameters  :
            nestedresults (dict)            : Nested results containing flux linkage and voltages for transformers and chokes.
            FFT_current (numpy.ndarray)     : FFT current values.
            l (int)                         : Index for time step or frequency bin.

        Returns:
            tuple: Tuple containing core losses, primary copper losses, secondary copper losses, choke core and copper losses.

        """
        core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss = [], [], [], [], []
        R_pri, R_sec, R_ind = [],[],[]
        #! core losses :
        flux_link     = nestedresults[dp.pmapping['Transformer Flux']]
        point_flux    = dp.np.round((dp.np.max(flux_link)-dp.np.min(flux_link))/2 , decimals=12 )
        # Bp            = point_flux/(dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['Ae'] * dp.mdlVars['DCDC_Rail1']['Trafo']['Np'])
        # d             = [nestedresults[dp.pmapping['PWM Modulator Primary Modulator Duty Cycle'] + dp.Y_list[3] + 1]]
        # d             = self.rms_avg('AVG', d, nestedresults[0])
        # Vc            = dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['Vc']
        SP_tfo        = dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['SP_tfo']
        d             = 0.532
        Bp            = 0.10776
        Vc            = 468e-6 * 72.5e-3
        core_loss.append(self.IGSE('trap', SP_tfo, d, dp.F_Fund, Bp, Vc))

        #! primary and secondary copper losses :
        f_tfo         = [0] + dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Harmonics']
        pri_Rvec        = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Rvec']
        pri_Rscale      = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Rscale']
        sec_Rvec        = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Rvec']
        sec_Rscale      = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Rscale']
        for i in range(len(pri_Rvec)):
            R_pri.append(pri_Rvec[i][-1])
            R_sec.append(sec_Rvec[i][-1])
        res_optimize_pri = self.rac_lac_values('min', dp.mdlVars['DCDC_Rail1']['Trafo']['Lm'], dp.np.array(f_tfo)* 1e5, dp.np.array(R_pri))
        res_optimize_sec = self.rac_lac_values('min', dp.mdlVars['DCDC_Rail1']['Trafo']['Lm']/100, dp.np.array(f_tfo)* 1e5, dp.np.array(R_sec))   # Lm with respect to secondary, Lm' = Lm/(turns_ratio)^2

        pri_copper_loss.append(dp.np.sum(res_optimize_pri['Rac_calculated']*pri_Rscale * (1/2) * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics), dp.pmapping['Transformer Primary Current']-1][f_tfo[1:]])))
        sec_copper_loss.append(dp.np.sum(res_optimize_sec['Rac_calculated']*sec_Rscale * (1/2) * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics), dp.pmapping['Transformer Secondary Current']-1][f_tfo[1:]])))

        #! choke core losses :
        Iind = nestedresults[dp.pmapping['DC Choke Current']]
        Iindp = (dp.np.max(Iind)- dp.np.min(Iind))/2
        Bpl           = (dp.mdlVars['DCDC_Rail1']['Lf']['L'] * Iindp) / ( dp.mdlVars['DCDC_Rail1']['Lf']['N']* dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Ae'])
        Sp_choke      = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['SP_l']
        Vcl           = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Vc']
        choke_core_loss.append(self.IGSE('tri', Sp_choke, d, 2*dp.F_Fund, Bpl, Vcl))

        #! choke copper losses :
        choke_current_fft = FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),dp.pmapping['DC Choke Current']-1]
        ind_Rvec          = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Rwind']['Rvec']
        ind_Rscale        = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Rwind']['Rscale']
        f_ind             = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Harmonics']
        for i in range(len(ind_Rvec)):
            R_ind.append(ind_Rvec[i][-1])
        choke_copper_loss.append(dp.np.sum(dp.np.array(R_ind[1:]) * ind_Rscale * (1/2) * dp.np.square(choke_current_fft[f_ind[1:]])) + (dp.np.array(R_ind[0]) * ind_Rscale * dp.np.square(choke_current_fft[0])))

        return dp.np.array(core_loss), dp.np.array(pri_copper_loss), dp.np.array(sec_copper_loss), dp.np.array(choke_core_loss), dp.np.array(choke_copper_loss)

    def dissipations(self, nestedresults_l, res_list, RMS_currents, thread, FFT_current): # trafo_inputs, choke_inputs):
        """
        Calculate dissipations including magnetic losses and resistive losses.

        Parameters  :
            nestedresults_l (numpy.ndarray) : Nested results array.
            res_list (numpy.ndarray)        : Resistances list.
            RMS_currents (numpy.ndarray)    : RMS currents array.
            thread (int)                    : Thread index.
            FFT_current (numpy.ndarray)     : FFT currents array.
            trafo_inputs (list)             : List of transformer inputs.
            choke_inputs (list)             : List of choke inputs.

        Returns:
            numpy.ndarray: Dissipation matrix including magnetic losses and resistive losses.

        """
        dissip                                                       = self.rms_avg('AVG',nestedresults_l[sum(dp.Y_list[0:3]):sum(dp.Y_list[0:4]),  : ], nestedresults_l[0])
        # core_loss , pri_copper_loss , sec_copper_loss , Choke_loss   = self.magnetic_loss(nestedresults_l,FFT_current,thread, trafo_inputs , choke_inputs)
        core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss = self.analytical_magnetic_loss(nestedresults_l, FFT_current, thread)
        res_dissip                                                   = (dp.np.square(RMS_currents[thread,0:dp.current_idx]))*res_list
        # Dissipation_matrix                                           = dp.np.concatenate((dissip, pri_copper_loss , sec_copper_loss , core_loss ,Choke_loss,res_dissip))
        Dissipation_matrix                                           = dp.np.concatenate((dissip, core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss, res_dissip))
        # print(dp.np.shape(dissip), dp.np.shape(core_loss), dp.np.shape(pri_copper_loss), dp.np.shape(sec_copper_loss), dp.np.shape(choke_core_loss), dp.np.shape(choke_copper_loss), dp.np.shape(res_dissip))
        return Dissipation_matrix

    def therm_stats(self,MAT_list,thread,P_aux):
        """
        Calculate thermal statistics including efficiency, total dissipation, and input power.

        Parameters  :
            MAT_list (list) : List containing matrices of thermal data.
            thread (int)    : Thread index.

        Returns:
            numpy.ndarray: Thermal matrix including total dissipation, efficiency, and input power.

        """
        P_rail      =   dp.np.sum(MAT_list[8][thread , dp.Rail_idx:dp.Common_idx+1])                            # get total loss of each rail
        P_common    =   dp.np.sum(MAT_list[8][thread , dp.Common_idx+1:])                                       # get total losses of common parts
        Pout        =   dp.np.mean(MAT_list[9][thread, dp.Pout_idx])                                            # get output power
        # Calculate eff for each factorial value in the list using list comprehension
        Eff         =   dp.np.array([(((Pout / ( Pout + P_rail + (factorial * P_common))*100.0) if ( Pout + P_rail + (factorial * P_common)) != 0 else 0.0)) for factorial in list(range(1, dp.phase + 1))])
        Eff_Aux     =   dp.np.array([(((Pout / ( Pout + (P_rail + (factorial * P_common))+P_aux)*100.0) if ( Pout + P_rail + (factorial * P_common)) != 0 else 0.0)) for factorial in list(range(1, dp.phase + 1))])
        # Calc Total dissipation
        Ptot        =   dp.np.array([(P_rail*factorial + P_common*factorial**2) for factorial in list(range(1, dp.phase + 1))])
        # Input Power
        Pin         =   dp.np.array([((P_rail + Pout)*factorial + P_common*factorial**2) for factorial in list(range(1, dp.phase + 1))])
        Th_mat      =   dp.np.concatenate((Ptot , Eff , Eff_Aux , Pin))
        if MAT_list[11].shape == (1, 1):
            return dp.np.empty((1,))
        else:
            return Th_mat

    def insert_array(self, file_path, index, data_to_insert):
        """
        Insert a list of lists into a specific index of a CSV file.

        Parameters  :
            file_path (str)         : Path to the CSV file.
            index (int)             : Index at which the data should be inserted.
            data_to_insert (list)   : List of lists to be inserted.

        Returns:
            None

        """
        df = dp.pd.read_csv(file_path, header=None)                                                     # Read the CSV file into a Pandas DataFrame
        data_to_insert_df = dp.pd.DataFrame(data_to_insert)                                             # Create a DataFrame from the list of lists
        df = dp.pd.concat([df.iloc[:index], data_to_insert_df, df.iloc[index:]], ignore_index=True)     # Insert into the main DataFrame at the specified index
        df.to_csv(file_path, header=False, index=False)                                                 # Write the updated DataFrame back to the CSV file

    def drop_Extra_Cols(self, filename, idx_start, idx_end):
        """
        Drop specified columns range from a CSV file.

        Parameters  :
            filename (str)     : Path to the CSV file.
            dissip_start (int)  : Starting index of columns to be dropped.
            dissip_end (int)    : Ending index (exclusive) of columns to be dropped.

        Returns:
            None

        """
        df                  = dp.pd.read_csv(filename, header=None)                                    # Read the CSV file into a DataFrame.
        df.drop(df.columns[idx_start:idx_end], axis=1, inplace=True)                              # Drop the columns specified by dissip_start and dissip_end from the DataFrame
        df.to_csv(filename, index=False, header=None)

    def LuT_2D(self, x, y, z):
        """
        Create a 2D Look-Up Table (LuT) using linear interpolation.

        Parameters  :
            x (list)            : List of values for the first dimension.
            y (list)            : List of values for the second dimension.
            z (numpy.ndarray)   : 2D array of values for the LuT.

        Returns:
            RegularGridInterpolator: Interpolation function for the LuT.

        """
        interp_func     = dp.RegularGridInterpolator((x, y), z, method='linear', bounds_error=False, fill_value=None)
        return interp_func

    def LuT_3D(self, x, y, z, data):
        """
        Create a 3D Look-Up Table (LuT) using linear interpolation.

        Parameters  :
            x (list)                : List of values for the first dimension.
            y (list)                : List of values for the second dimension.
            z (list)                : List of values for the third dimension.
            data (numpy.ndarray)    : 3D array of values for the LuT.

        Returns:
            RegularGridInterpolator: Interpolation function for the LuT.

        """
        interp_func     = dp.RegularGridInterpolator((x,y,z), data, method='linear', bounds_error=False, fill_value=None)
        return interp_func

    def resample(self, time, signal):
        """
        Resample a signal to have uniform time points.

        Parameters  :
            time (numpy.ndarray)    : Time values of the original signal.
            signal (numpy.ndarray)  : Signal values.

        Returns:
            tuple: Tuple containing the resampled time values and the corresponding resampled signal values.

        """
        new_t       = dp.np.linspace(time.min(), time.max(), len(signal))
        new_signal  = dp.np.interp(new_t,time,signal)
        return new_t,new_signal

    def IIR_Filter(self, Time, Signal, Cutoff, Order=2, BType='low', FType='butter'):
        """_summary_

        Args:
            Time (_type_): _description_
            Signal (_type_): _description_
            Cutoff (_type_): _description_
            Order (int, optional): _description_. Defaults to 2.
            BType (str, optional): _description_. Defaults to 'low'.
            FType (str, optional): _description_. Defaults to 'butter'.

        Returns:
            _type_: _description_
        """
        dt                  =   Time[1] - Time[0]
        Fs                  =   1.0/dt
        Fn                  =   min(Fs/2-1, Cutoff)

        b,a                 =   dp.scipy.signal.iirfilter(Order, Wn=Fn, fs=Fs, btype=BType, ftype=FType)
        Signal_Filtered     =   dp.scipy.signal.filtfilt(b, a, Signal)

        return Signal_Filtered

    def pyFFT(self, signal, fs):
        """
        Compute the Fast Fourier Transform (FFT) of a signal and return amplitude, phase, and frequency information.

        Parameters  :
            signal (numpy.ndarray)  : Input signal.
            fs (float)              : Sampling frequency of the signal.

        Returns:
            tuple: Tuple containing amplitude, phase, and frequency arrays.

        """
        N               = len(signal)                                                   #
        f               = dp.fftfreq(N,1/fs)                                            #
        f               = f[f >= 0]                                                     #
        useful          = dp.np.arange(0, len(f)/2, dtype=int)                          # Select useful indices and corresponding frequency values
        fft             = dp.fft(x=signal,workers=dp.multiprocessing.cpu_count())       # Compute FFT
        amplitude       = dp.np.abs(fft)                                                # Calculate magnitude of FFT result
        amplitude[0]    = (1/N) * amplitude[0]                                          # Scale the magnitude values
        amplitude[1:N]  = (2/N) * amplitude[1:N]                                        # Scale the magnitude values
        amplitude       = amplitude[useful]                                             # Select useful indices and corresponding magnitude values
        pahse           = dp.np.angle(fft[useful],deg=True)                             # Calculate phase angles of the FFT result
        frequency       = f[useful]                                                     #
        return amplitude, pahse, frequency

    def safe_get(self,my_list, index):
        try:
            return my_list[index]
        except IndexError:
            return None

    def FFT_mat(self, T_vec, nestedresults):
        """
        Compute the Fast Fourier Transform (FFT) matrix of nested results.

        Parameters  :
            T_vec (numpy.ndarray)           : Time vector.
            nestedresults (numpy.ndarray)   : Nested results array.

        Returns:
            numpy.ndarray: Transposed FFT matrix.

        """
        fft_mat     =   dp.np.zeros((len(nestedresults),len(dp.harmonics)))

        for x in range(len(nestedresults)):
            if dp.mdlVars['Common']['ToFile']['Ts'] == 0:                               # var sampling
                time_vec,signal_vec  = self.resample(T_vec, nestedresults[x])
            else :                                                                      # fixed sampling
                time_vec,signal_vec  = T_vec, nestedresults[x]

            # time_vec             = T_vec
            # signal_vec           = nestedresults[x]
            dt                   = time_vec[-1]-time_vec[0]
            fs                   = 1/((dp.np.round(dt,decimals=6)))
            Magnitude , _ ,_     = self.pyFFT(signal_vec , dp.F_Fund)
            idx                  = [int(c) for c in (((dp.np.array(dp.harmonics,dtype=int)*dp.F_Fund).tolist())/fs).tolist()]
            Mag_array            = [self.safe_get(Magnitude, index) for index in idx if self.safe_get(Magnitude, index) is not None]
            fft_mat[x, :]        = dp.np.pad(Mag_array, (0, len(dp.harmonics) - len(Mag_array)), 'constant')
        return dp.np.transpose(fft_mat)

    def remove_duplicates(self, nested_array):
        """
        Remove duplicates from a nested array.

        Parameters:
            nested_array (list): Nested array containing subarrays.

        Returns:
            list: Modified nested array without duplicate values.

        """
        seen_values         = set()                                                                                             # Define set for duplicates.
        indexes_to_remove   = {i for i, value in enumerate(nested_array[0]) if value in seen_values or seen_values.add(value)}  # Find duplicate values at index 0.
        nested_array[:]     = [[value for j, value in enumerate(row) if j not in indexes_to_remove] for row in nested_array[:]] # Remove corresponding elements from the arrays.
        return nested_array

    def findMissingResults(self,path,itr,threads_vector,Threads):
        """
        In case of a crash find and reconstruct the missing results using the last iteration and thread and path.

        Parameters     :
                                path     :               string
                                                         path to results folder.
                                itr      :               int
                                                         Last iteration number.
                                Threads  :               int
                                                         Last Thread count.
        Returns        :        Missing  :               List
                                                         List of missing data.
        """
        file_list           =   []
        Iters               =   []
        if dp.JSON['hierarchical']:
            iteration_range     =   list(range(1,sum(threads_vector[0:itr+1])+1))
        else:
            iteration_range     =   list(range(1,Threads*(itr+1)+1))
        for filename in dp.os.scandir(path):
            file_list.append(str(filename.path.replace("\\","/")))

        for i in range(len(file_list)):
            x               =   file_list[i].split("s_")[-1]
            x               =   x.split(".")[0]
            x               =   x.split("_")[-1]
            Iters.append(int(x))
            Iters.sort()

        Set                 =   set(Iters)
        Missing             =   [x for x in iteration_range if x not in Set]

        return Missing

    def last_filled_X(self):

        lists = [dp.JSON[f'X{i}']for i in range(1,11)]  # Construct the list of X input lists from the json file.
        for lst in reversed(lists):                     # Iterate through the list of lists from last to first
            lst     = dp.ast.literal_eval(lst)          # Evaluate expression of the list coming from json.
            if lst != [0]:                              # Check if the list is not [0]
                return len(lst)                         # Return the length of the first non-zero list
        return 0                                        # Return 0 if all lists are [0]

    def hierarchicalSims(self, Map):
            """ 
            Calculate hierarchical simulation parameters for operation under different conditions.

            This method computes current and power limits for continuous, 10-second, and 2-second operation modes.
            It categorizes operating points into these modes and calculates thread distribution.

            Parameters:
            -----------
            Map : list of lists

            Returns:
            --------
            list
                A vector containing thread distribution values for continuous, 10-second, and 2-second operation modes.

            """
            thread_vector                                       =   []
            iter_continous ,    iter_10s        , iter_2s       =   []               , []    , []
            Vmin           ,    Vnom            , Vmax          =   6                , 13.5  , 15.5
            Twater_nom     ,    Twater_max                      =   35               , 75
            Pmax_2s_35     ,    Pmax_2s_75                      =   2600             , 1950
            Pmax_10s_35    ,    Pmax_10s_75                     =   2160             , 1822
            Pcont_35       ,    Pcont_75                        =   1800             , 1505
            Imax_2s_35     ,    Imax_2s_75                      =   Pmax_2s_35/Vnom  , Pmax_2s_75/Vnom
            Imax_10s_35    ,    Imax_10s_75                     =   Pmax_10s_35/Vnom , Pmax_10s_75/Vnom
            Icont_35       ,    Icont_75                        =   Pcont_35/Vnom    , Pcont_75/Vnom

            for i in range(len(Map)):

                Pcont_Tw                                        =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pcont_35,Pcont_75,
                                                                                        Pcont_75,Pcont_35,
                                                                                        Map[i][1])
                P10s_Tw                                         =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pmax_10s_35,Pmax_10s_75,
                                                                                        Pmax_10s_75,Pmax_10s_35,
                                                                                        Map[i][1])
                P2s_Tw                                          =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pmax_2s_35,Pmax_2s_75,
                                                                                        Pmax_2s_75,Pmax_2s_35,
                                                                                        Map[i][1])
                Icont_Tw                                        =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Icont_35,Icont_75,
                                                                                        Icont_75,Icont_35,
                                                                                        Map[i][1])
                I10s_Tw                                         =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Imax_10s_35,Imax_10s_75,
                                                                                        Imax_10s_75,Imax_10s_35,
                                                                                        Map[i][1])
                I2s_Tw                                          =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Imax_2s_35,Imax_2s_75,
                                                                                        Imax_2s_75,Imax_2s_35,
                                                                                        Map[i][1])
                I2s_Vo                                          =   self.linearDerating(Vnom,Vmax,
                                                                                        P2s_Tw/Vnom,P2s_Tw/Vmax,
                                                                                        P2s_Tw/Vmax,P2s_Tw/Vnom,
                                                                                        Map[i][3])
                I10s_Vo                                         =   self.linearDerating(Vnom,Vmax,
                                                                                        P10s_Tw/Vnom,P10s_Tw/Vmax,
                                                                                        P10s_Tw/Vmax,P10s_Tw/Vnom,
                                                                                        Map[i][3])
                Icont_Vo                                        =   self.linearDerating(Vnom,Vmax,
                                                                                        Pcont_Tw/Vnom,Pcont_Tw/Vmax,
                                                                                        Pcont_Tw/Vmax,Pcont_Tw/Vnom,
                                                                                        Map[i][3])
                Pmax_Vo                                         =   self.linearDerating(Vmin,Vnom,
                                                                                        Vmin*P2s_Tw/Vnom,Vnom*P2s_Tw/Vnom,
                                                                                        Vmin*P2s_Tw/Vnom,Vnom*P2s_Tw/Vnom,
                                                                                        Map[i][3])
                Pmax                                            =   min(P2s_Tw,Pmax_Vo)
                Pmax                                            =   min(Map[i][4],Pmax)
                I2s                                             =   round(min(I2s_Tw,I2s_Vo),4)
                I10s                                            =   round(min(I10s_Tw,I10s_Vo),4)
                Icont                                           =   round(min(Icont_Tw,Icont_Vo),4)
                I_L                                             =   round(Pmax/Map[i][3],4)

                if (I_L <= I2s and I_L > I10s):
                    iter_2s.append(iter_10s_1)

                elif (I_L <= I10s and I_L > Icont):
                    iter_10s.append(iter_continous)
                    iter_10s_1 = i

                else:
                    iter_continous = i

            iter_10s = dp.np.array(iter_10s)
            iter_10s = list(dp.np.unique(iter_10s))

            iter_2s = dp.np.array(iter_2s)
            iter_2s = list(dp.np.unique(iter_2s))

            for i in range(len(iter_10s)):
                thread_1 = iter_10s[i]+1-self.last_filled_X()*i
                thread_2 = iter_2s[i]-iter_10s[i]
                thread_3 = self.last_filled_X()-(thread_1+thread_2)

                thread_vector.append(thread_1)
                thread_vector.append(thread_2)
                thread_vector.append(thread_3)

            return thread_vector

    def hierarchicalSimsEntry(self,Map):
            """
            Calculate hierarchical simulation parameters for entry conditions.
            Computes current and power limits for continuous, 10-second, and 2-second operation modes.

            Parameters:
            -----------
            Map : list of lists

            Returns:
            --------
            list
                A vector containing thread distribution values for continuous, 10-second, and 2-second operation modes. 
            """
            thread_vector                                       =   []
            iter_continous ,    iter_10s        , iter_2s       =   []               , []    , []
            Vmin           ,    Vnom            , Vmax          =   6                , 13.5  , 15.5
            Twater_nom     ,    Twater_max                      =   35               , 75
            Pmax_2s_35     ,    Pmax_2s_75                      =   2295             , 1500
            Pmax_10s_35    ,    Pmax_10s_75                     =   1620             , 1323
            Pcont_35       ,    Pcont_75                        =   1276             , 1148
            Imax_2s_35     ,    Imax_2s_75                      =   Pmax_2s_35/Vnom  , Pmax_2s_75/Vnom
            Imax_10s_35    ,    Imax_10s_75                     =   Pmax_10s_35/Vnom , Pmax_10s_75/Vnom
            Icont_35       ,    Icont_75                        =   Pcont_35/Vnom    , Pcont_75/Vnom

            for i in range(len(Map)):

                Pcont_Tw                                        =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pcont_35,Pcont_75,
                                                                                        Pcont_75,Pcont_35,
                                                                                        Map[i][1])
                P10s_Tw                                         =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pmax_10s_35,Pmax_10s_75,
                                                                                        Pmax_10s_75,Pmax_10s_35,
                                                                                        Map[i][1])
                P2s_Tw                                          =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Pmax_2s_35,Pmax_2s_75,
                                                                                        Pmax_2s_75,Pmax_2s_35,
                                                                                        Map[i][1])
                Icont_Tw                                        =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Icont_35,Icont_75,
                                                                                        Icont_75,Icont_35,
                                                                                        Map[i][1])
                I10s_Tw                                         =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Imax_10s_35,Imax_10s_75,
                                                                                        Imax_10s_75,Imax_10s_35,
                                                                                        Map[i][1])
                I2s_Tw                                          =   self.linearDerating(Twater_nom,Twater_max,
                                                                                        Imax_2s_35,Imax_2s_75,
                                                                                        Imax_2s_75,Imax_2s_35,
                                                                                        Map[i][1])
                I2s_Vo                                          =   self.linearDerating(Vnom,Vmax,
                                                                                        P2s_Tw/Vnom,P2s_Tw/Vmax,
                                                                                        P2s_Tw/Vmax,P2s_Tw/Vnom,
                                                                                        Map[i][3])
                I10s_Vo                                         =   self.linearDerating(Vnom,Vmax,
                                                                                        P10s_Tw/Vnom,P10s_Tw/Vmax,
                                                                                        P10s_Tw/Vmax,P10s_Tw/Vnom,
                                                                                        Map[i][3])
                Icont_Vo                                        =   self.linearDerating(Vnom,Vmax,
                                                                                        Pcont_Tw/Vnom,Pcont_Tw/Vmax,
                                                                                        Pcont_Tw/Vmax,Pcont_Tw/Vnom,
                                                                                        Map[i][3])
                Pmax_Vo                                         =   self.linearDerating(Vmin,Vnom,
                                                                                        Vmin*P2s_Tw/Vnom,Vnom*P2s_Tw/Vnom,
                                                                                        Vmin*P2s_Tw/Vnom,Vnom*P2s_Tw/Vnom,
                                                                                        Map[i][3])
                Pmax                                            =   min(P2s_Tw,Pmax_Vo)
                Pmax                                            =   min(Map[i][4],Pmax)
                I2s                                             =   round(min(I2s_Tw,I2s_Vo),4)
                I10s                                            =   round(min(I10s_Tw,I10s_Vo),4)
                Icont                                           =   round(min(Icont_Tw,Icont_Vo),4)
                I_L                                             =   round(Pmax/Map[i][3],4)

                if (I_L <= I2s and I_L > I10s):
                    iter_2s.append(iter_10s_1)

                elif (I_L <= I10s and I_L > Icont):
                    iter_10s.append(iter_continous)
                    iter_10s_1 = i

                else:
                    iter_continous = i

            iter_10s = dp.np.array(iter_10s)
            iter_10s = list(dp.np.unique(iter_10s))

            iter_2s = dp.np.array(iter_2s)
            iter_2s = list(dp.np.unique(iter_2s))

            for i in range(len(iter_10s)):
                thread_1 = iter_10s[i]+1-self.last_filled_X()*i
                thread_2 = iter_2s[i]-iter_10s[i]
                thread_3 = self.last_filled_X()-(thread_1+thread_2)

                thread_vector.append(thread_1)
                thread_vector.append(thread_2)
                thread_vector.append(thread_3)

            return thread_vector

    def linearDerating(self,X1,X2,Y1,Y2,Ymin,Ymax,X):
        """
        Calculates a linear derating factor (Y) based on the given inputs.

        Args:
            X1 (float): The lower limit of the X range.
            X2 (float): The upper limit of the X range.
            Y1 (float): The derating factor when X=X1.
            Y2 (float): The derating factor when X=X2.
            Ymin (float): The minimum allowable value of the derating factor Y.
            Ymax (float): The maximum allowable value of the derating factor Y.
            X (float): The X value for which the derating factor is to be calculated.

        Returns:
            float: The linearly interpolated derating factor Y for the given X.

        Raises:
            ValueError: If X2 is equal to X1, which would result in a division by zero error.

        Example:
            # Calculate the derating factor for X=7, given X1=2, X2=10, Y1=0.5, Y2=1.0, Ymin=0.0, Ymax=1.0.
            derating_factor = linearDerating(2, 10, 0.5, 1.0, 0.0, 1.0, 7)
            print(derating_factor)
            # Output: 0.8
        """
        m   =   (Y2 - Y1)/(X2 - X1)
        b   =   Y1 - m*X1

        Y   =   m*X + b

        Y   =   min(Y,Ymax)
        Y   =   max(Y,Ymin)

        return Y

    def IGSE(self, Wf, SP, d, f_s, Bp, Vc):
        """
        Analytical magnetic core loss calculation from IGSE- Improved Generailzed Steinmetz Equation for trapezoidal and triangular magnetic flux density waveform
        Args:
            Wf (str)    : Waveform selection - 'trap' for trapezoidal magnetic flux density waveform
                                               'tri' for triangular magnetic flux density waveform
            SP          : Steinmetz parameters of the core (k,a,b)
            d (0... 1)  : Duty cycle
            f_s (Hz)    : Switching frequency
            Bp (T)      : Magnetic field peak value
            Vc (m3)     : Core volume
        Returns:
            Pave_core(W) : Average core losses
        """

        def ki(k,a,b):
            f = lambda theta, a: (abs(dp.np.cos(theta)))**SP[1]
            integral, error = quad(f, 0, 2* dp.np.pi, args=(SP[1]))
            ki = SP[0]/((2*dp.np.pi)**(SP[1]-1) * 2**(SP[2]-SP[1]) * integral)
            return ki

        match Wf:
            case 'trap':
                 Pave_density = ki(SP[0], SP[1], SP[2]) * f_s**SP[1] * Bp**SP[2] * 2**(SP[1]+SP[2]) * d**(1-SP[1])                        # Average core losses density (W/m3)
                 Pave_core = Pave_density * Vc                                                                                              # Average core losses (W)
            case 'tri':
                Pave_density = ki(SP[0], SP[1], SP[2]) * f_s**SP[1] * Bp**SP[2] * 2**SP[2] * (d**(1-SP[1]) + (1-d)**(1-SP[1]))            # Average core losses density (W/m3)
                Pave_core = Pave_density * Vc                                                                                               # Average core losses (W)

        return Pave_core

    def rac_lac_values(self, method, L_primary,frequencies, Z_real_csv):
        """
        Calculate Rac and Lac values from the measured real resistance values of the transformer
        Args:
            method (str)    : optimization method selection - 'min' for minimize method, 'ls' for least squares method
            L_primary (H)   : Magnetizing inductance
            frequencies (Hz): Harmonic frequency spectrum
            Z_real_csv (Ω)  : Measured real resistance values from csv
        Returns:
            res_optimize : Dictionary of calculated Rac, Lac, Rac_calculated, Z_real_residual, Z_real_calculated and percentage_difference
        """
        R_dc = Z_real_csv[frequencies == 0][0] #/ 1000                                                                                      # Extract R_dc
        valid_index = frequencies != 0                                                                                                      # Remove the frequency = 0 row
        frequencies = dp.np.array(frequencies[valid_index])
        Z_real_csv = dp.np.array(Z_real_csv[valid_index]) #/1000
        num_frequency = len(frequencies)
        #initial guess
        R_ac = dp.np.ones(len(frequencies))*1e-3                                                                                            # initialize Rac with small positive value (1 mΩ)
        L_ac = dp.np.full(len(frequencies), L_primary/len(frequencies))                                                                     # initialize Lac value by dividing Lm equally
        initial = dp.np.concatenate([R_ac,L_ac])
        omega = 2 * dp.np.pi * frequencies
        Z_real_residual_csv = Z_real_csv - R_dc                                                                                             # Real residual resistance
        match method:
            case 'min':                                                                                                                     # minimize method
                #cost function
                def cost_minimize(params, omega, Z_real_residual_csv):                                                                      # cost function of minimize method
                    R_ac = params[:len(frequencies)]
                    L_ac = params[len(frequencies):]
                    X_lac = omega * L_ac
                    num = R_ac * X_lac**2
                    den = R_ac**2 + X_lac**2
                    Z_real_residual = num/den
                    error = Z_real_residual_csv - Z_real_residual
                    return sum(error**2)
                #constarints
                def R_ac_constraint(params):                                                                                                 # Rac constraint for minimize method
                    R_ac = params[:len(frequencies)]
                    return [R_ac[4] - R_ac[3],                                                                                               # R5 > R4
                            R_ac[3] - R_ac[2],                                                                                               # R4 > R3
                            R_ac[2] - R_ac[1],                                                                                               # R3 > R2
                            R_ac[1] - R_ac[0]]                                                                                               # R2 > R1

                def L_ac_constraint(params):                                                                                                 # Lac constraint for minimize method
                    L_ac = params[len(frequencies):]
                    return L_primary - sum(L_ac)                                                                                             # sum(Lac) < Lm

                constraints = [{'type':'ineq', 'fun': R_ac_constraint}, {'type':'ineq', 'fun': L_ac_constraint}]
                #bounds
                bounds = [(1e-6, 100e-3)]* len(frequencies) + [((L_primary/len(frequencies)), 1e-3)]* len(frequencies)                       # bounds for minimize method

                res = minimize(cost_minimize, initial, args=(omega, Z_real_residual_csv), bounds=bounds, constraints=constraints)

            case 'ls':                                                                                                                       # cost function for least_squares method
                #cost function
                def cost_leastsquares(params, omega, Z_real_residual_csv):
                    R_ac = params[:len(frequencies)]
                    L_ac = params[len(frequencies):]
                    X_lac = omega * L_ac
                    num = R_ac * X_lac**2
                    den = R_ac**2 + X_lac**2
                    Z_real_residual = num/den
                    error = Z_real_residual_csv - Z_real_residual
                    return error
                #bounds
                lb = [1e-6]* len(frequencies) + [L_primary/len(frequencies)]* len(frequencies)                                               # lower bound for least_squares
                ub = [100e-3]* len(frequencies) + [1e-3]* len(frequencies)                                                                   # upper bound for least_squares

                res = least_squares(cost_leastsquares, initial, args= (omega, Z_real_residual_csv), bounds=(lb,ub))

        fitted_param            = res.x
        R_fit                   = fitted_param[:len(frequencies)]
        L_fit                   = fitted_param[len(frequencies):]
        Xl_fit                  = omega * L_fit
        Z_real_residual         = ((R_fit * Xl_fit**2)/(R_fit**2 + Xl_fit**2))
        Z_real_calculated       = Z_real_residual + R_dc
        percentage_difference   = ((Z_real_calculated - Z_real_csv)/Z_real_csv) * 100
        res_optimize = {
        'Rac'                   : R_fit,
        'Lac'                   : L_fit,
        'Rac_calculated'        : R_fit + R_dc,
        'Z_real_residual'       : Z_real_residual,
        'Z_real_calculated'     : Z_real_calculated,
        'Percentage_difference' : percentage_difference
        }

        return res_optimize

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
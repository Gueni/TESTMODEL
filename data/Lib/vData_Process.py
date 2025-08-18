
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                ____    _  _____  _      ____  ____   ___   ____ _____ ____ ____ ___ _   _  ____
#?                               |  _ \  / \|_   _|/ \    |  _ \|  _ \ / _ \ / ___| ____/ ___/ ___|_ _| \ | |/ ___|
#?                               | | | |/ _ \ | | / _ \   | |_) | |_) | | | | |   |  _| \___ \___ \| ||  \| | |  _
#?                               | |_| / ___ \| |/ ___ \  |  __/|  _ <| |_| | |___| |___ ___) |__) | || |\  | |_| |
#?                               |____/_/   \_\_/_/   \_\ |_|   |_| \_\\___/ \____|_____|____/____/___|_| \_|\____|
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
from collections import defaultdict

from collections import defaultdict

def recursive_defaultdict():
    return defaultdict(recursive_defaultdict)

dict1 = recursive_defaultdict()
dict1['modelvars']['x']['c']['bb'] = 5.2  # Works at any depth
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp
from decimal import Decimal
from scipy.integrate import quad
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
        file            = directory_path + f"/results_{utc}_{str(itr+1)}.csv"   # Construct the file name using the provided directory path, UTC, and iteration number.           
        dataFrame       = dp.pd.read_csv(file, header=None, dtype=str).transpose()  # Read the CSV file into a pandas DataFrame, transposing it to have columns as rows.
        try:        
            listcols   = (dataFrame.apply(lambda col: col.map(Decimal))).values.tolist()    # Convert the DataFrame to a list of lists, applying Decimal conversion to each column.
        except Exception:
            print("Could not apply Decimal.")   # If there's an error in applying Decimal conversion, print an error message.
            pass    
        df              = (dp.pd.DataFrame(listcols, dtype=object).transpose()).dropna()    # Create a new DataFrame from the list of lists, transposing it back to original orientation and dropping any NaN values.
        df.to_csv(file, index=False, header=None, mode='w') # Save the DataFrame back to the CSV file without index and header, overwriting the original file.
        return listcols # Return the list of lists containing the concatenated data from all CSV files.

    def norm_results(self,results):
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
        resultsvect             = []                    # Initialize an empty list to store the normalized results.
        longest_length          = max(len(results[c]['Time']) for c in range(len(results)))         # Find the longest time vector length in the input results.
        for i in range(len(results)):               # Iterate through each nested dictionary in the input results.
            timevector          = results[i]['Time']            # Extract the time vector from the current nested dictionary.
            difference_lengths  = longest_length - len(timevector)  # Calculate the difference in lengths between the longest time vector and the current time vector.
            NaNarray            = dp.np.empty((difference_lengths))         # Create an array of NaN values with the calculated difference in lengths.
            NaNarray[:]         = dp.nan        #   Fill the NaN array with NaN values.
            valuesvector        = results[i]['Values']  # Extract the values vector from the current nested dictionary.
            outputresults       = []               # Initialize an empty list to store the output results for the current simulation.
            timevector = dp.np.append(NaNarray,timevector)      # Append the NaN array to the time vector to normalize its length.
            outputresults.append(timevector)          # Append the normalized time vector to the output results.
            for j in range(len(valuesvector)):           # Iterate through each value vector in the values vector.
                valuesvector[j] = dp.np.append(NaNarray,valuesvector[j])    # Append the NaN array to the current value vector to normalize its length.
                outputresults.append(valuesvector[j])   # Append the normalized value vector to the output results.
            resultsvect.append(outputresults)       # Append the output results for the current simulation to the main results vector.
        return resultsvect      #   Return the normalized results vector containing the nested list of lists with time and values.

    def norm_results_csv(self,results):
        """
        Normalize a list of lists by padding shorter sublists with NaN values to match the longest sublist.

        Parameters:
        results (list of lists): A list containing multiple lists of varying lengths.

        Returns:
        list: A list of lists where each sublist has been padded with NaN values to match the longest sublist length.

        Raises:
        ValueError: If the input is not a list of lists.
        """
        resultsvect             = []               # Initialize an empty list to store the normalized results.
        longest_length          = max(map(len, results))    # Find the length of the longest sublist in the input results.
        for sublist in results:              # Iterate through each sublist in the input results.
            difference_lengths  = longest_length - len(sublist) # Calculate the difference in lengths between the longest sublist and the current sublist.
            NaNarray            = dp.np.full(difference_lengths, dp.np.nan)     # Create an array of NaN values with the calculated difference in lengths.
            outputresults       = [dp.np.append(NaNarray, dp.np.array(item)).tolist() for item in sublist]  # Append the NaN array to each item in the current sublist and convert it to a list.
            resultsvect.append(outputresults)   # Append the normalized sublist to the main results vector.
        return resultsvect  # Return the normalized results vector containing the list of lists with padded NaN values.

    def extractArrays(self,fileName):
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
        path    =   dp.os.getcwd() + '/'    # Get the current working directory.
        array   =   []  # Initialize an empty list to store the columns of the CSV file.
        with open(path + fileName + '.csv') as f:   # Open the specified CSV file in read mode.
            line            =   f.readline()    # Read the first line of the file, which contains the column headers.
            firstRow        =   line.split(",") # Split the first line by commas to get the individual column headers.
            columnsNumber   =   len(firstRow)   # Get the number of columns in the CSV file based on the length of the first row.
            for i in range(columnsNumber):  # Iterate through each column index.
                array.append([])    # Initialize an empty list for each column in the array.
                array[i].append((float(firstRow[i])))   # Append the first value of each column to the corresponding list in the array.
            for row in f:   # Iterate through the remaining rows in the CSV file.
                for i in range(columnsNumber):      # For each column index, split the current row by commas to get the individual values.
                    otherRows   =   row.split(",")      # Append the value of the current column to the corresponding list in the array.
                    array[i].append((float(otherRows[i])))  # Convert the value to a float before appending.
        return array    # # Return the nested list containing the individual columns of the CSV file as lists.

    def get_index(self,Data: list, Point: float, Index: int) -> int:
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
        array   =   dp.np.asarray(Data[Index])  # Convert the specified sub-list of Data to a numpy array for efficient processing.
        idx     =   dp.np.nanargmin(dp.np.abs(array - Point))   # Find the index of the closest value to the target point in the sub-list.
        return idx  # Return the index of the closest value found in the sub-list.

    def csv_append_rows(self, fileName: str, data: list, save_mode: str = 'a') -> None:

        """
            Append the provided ND data array as a row to the specified CSV file.

            Args:
                fileName (str)      : The name of the CSV file to which the data will be appended.
                data (list)         : The ND data array to be appended.
                save_mode (str)     : Optional argument specifying the file open mode. Default value is 'a'
                which appends data to the end of the file. To overwrite the file, set save_mode to 'w'.

            Returns:
                None

            Raises:
                TypeError: If the provided data is not a list.
                ValueError: If the provided data is an empty list.

        """
        if not isinstance(data, list):  # Check if the data is a list
            raise TypeError("data should be a list.")   # Raise an error if data is not a list.
        if len(data) == 0:  # Check if the data list is empty
            raise ValueError("data list cannot be empty.")  # Raise an error if data is empty.
        if all(isinstance(i, list) for i in data):  # Check if all elements in data are lists
            df = dp.pd.DataFrame(list(data))    # Convert the list of lists to a DataFrame
        else:   # If data is not a list of lists, convert it to a DataFrame directly
            df = dp.pd.DataFrame(data).T    # Convert the data to a DataFrame and transpose it.
        df.to_csv(fileName, mode=save_mode, index=False, header=False)  # Append the DataFrame to the specified CSV file without index and header.

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
        indices = []    # Initialize an empty list to store indices.
        if pattern: # If pattern is True, find indices based on points in the matrix.
            indices = [matrix[i].index(points[i]) for i in range(len(points))]  # Find the index of each point in its corresponding row.
            itr = sum(indices[i] * dp.np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])for i in range(len(indices) - 1) # Compute the weighted sum of indices.
            ) + indices[-1]  # Last index is added directly
            indices.append(itr)  # Append computed index for reference
        else:   # If pattern is False, find the index of the first point in the first row.
            itr = matrix[0].index(points[0])    # Find the index of the first point in the first row.
            indices = dp.np.full(len(matrix) + 1, itr).tolist()  # Fill with the same value
        return indices, itr # Return the list of indices and the first index.

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

        if not pattern: # If pattern is False, return the matrix transposed from the last index onward.
            ParametersMap = dp.np.array(matrix[index[-1]:]).T.tolist()      # Transpose the matrix and slice from the last index onward.
            return ParametersMap, len(ParametersMap[0])  # Return matrix and the number of rows (length of first column)
        lengths = [len(sublist) for sublist in matrix]  # Get the lengths of each sublist in the matrix.
        totalLengths = dp.np.prod(lengths)  # Calculate the total number of combinations by multiplying the lengths of all sublists.
        ParametersMap = dp.np.zeros((totalLengths, len(matrix)))  # Initialize empty matrix of correct shape
        step_size = totalLengths  # Start with total length
        for col, sublist in enumerate(matrix):  # Iterate through each sublist in the matrix.
            step_size //= lengths[col]  # Reduce step size for each column
            repeat_factor = totalLengths // (step_size * lengths[col])  # Compute how often values should repeat
            ParametersMap[:, col] = dp.np.tile(dp.np.repeat(sublist, step_size), repeat_factor)  # Fill column efficiently
        return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])  # Slice according to index and return

    def findStart(self, matrix, pattern=True):
        """
        Returns a new matrix that starts at the given index.

        Args:
        - matrix (list[list[int]])  : A 2D matrix represented as a list of lists.
        - pattern (bool)            : A boolean flag indicating whether to return a pattern matrix (default True).

        Returns:
        - Matrix (list[list[int]])  : A new matrix that starts at the given index.
        """

        if pattern: # If pattern is True, return a shallow copy of the matrix.
            return [row[:] for row in matrix]  # Create a shallow copy of each row and return
        max_len = max(len(row) for row in matrix)   # Find the maximum length of the rows in the matrix.
        padded_matrix = [row + [0] * (max_len - len(row)) for row in matrix]    # Pad each row with zeros to make them of equal length.
        return dp.np.array(padded_matrix).T.tolist()  # Transpose the matrix and return as a list

    def dump_json_data(self,json_file):
        """_summary_

        Args:
            json_file (_type_): _description_

        Returns:
            _type_: _description_
        """
        path = dp.os.getcwd().replace("\\","/")+"/Script/assets/"+json_file # Construct the path to the JSON file.
        file = open(path,encoding='utf-8')   # Opening JSON file
        data = dp.json.load(file)   # returns JSON object as a dictionary
        file.close()    # Closing file
        return data # Return the loaded JSON data as a dictionary.

    def rms_avg(self, Op, nested_list, time_values):
        """
        Calculate the Root Mean Square (RMS) or Average (AVG) of signal data using trapezoidal integration.
        
        For 'RMS', computes the square root of the integral of squared values over time (normalized by duration).  
        For 'AVG', computes the integral of values over time (normalized by duration).  
        Uses `numpy.trapz()` for numerical integration, which approximates the area under the curve using the trapezoidal rule.  
        [numpy.trapz() docs]: https://numpy.org/doc/1.25/reference/generated/numpy.trapz.html  

        Parameters:
            Op (str)            : Operation selection - 'RMS' for Root Mean Square or 'AVG' for Average.
            nested_list (list)  : Nested list containing signal values (e.g., [[samples1], [samples2], ...]).
            time_values (list)  : List of corresponding time values (must be same length as signal samples).

        Returns:
            array : Computed RMS or AVG values for each sublist in `nested_list`.

        Raises:
            ZeroDivisionError : If the time range (`delta_T = time_values[-1] - time_values[0]`) is zero.
            ValueError       : If input data is invalid (e.g., non-numeric).
        """
        result          =   dp.np.array([])                     # Initialize an empty numpy array to store the results.                                                  
        delta_T         =   time_values[-1] - time_values[0]    # Calculate the time interval (delta_T) based on the first and last time values. 
        for sublist in nested_list:     # Iterate through each sublist in the nested list.                    
            match Op:   #   Match the operation type to determine the calculation method.                       
                case 'RMS': # If the operation is 'RMS', calculate the Root Mean Square value.                          
                    try:    # Try to perform the RMS calculation.
                        squared_values  = (dp.np.array(sublist))**2 # Square each value in the sublist.                                                 
                        res_value       = dp.np.sqrt(dp.np.trapz(squared_values, x=time_values) / delta_T)  # Integrate the squared values and divide by delta_T, then take the square root.       
                    except ZeroDivisionError:   # If a division by zero occurs, handle the exception.                                                 
                        print("Error: Division by zero is not allowed.")    # Print an error message if division by zero occurs.             
                case 'AVG': # If the operation is 'AVG', calculate the Average value.
                    try:    #   Try to perform the Average calculation.
                        res_value  = dp.np.trapz(dp.np.array(sublist), x=time_values) / delta_T # Integrate the values in the sublist and divide by delta_T to get the average.
                    except ZeroDivisionError:   #  If a division by zero occurs, handle the exception.
                        print("Error: Division by zero is not allowed.")    # Print an error message if division by zero occurs.          
            try:    # Try to append the calculated result to the result array.
                result = dp.np.append(result, res_value)    # Append the calculated result to the result array.                                     
            except ValueError:  # If a ValueError occurs while appending, handle the exception. 
                print("Error: Invalid input. Please enter valid numbers.")  # Print an error message if the input is invalid.                    
        return result   # Return the result array containing the calculated RMS or AVG values for each sublist in the nested list.

    def natsorted_list(self,dir):

        """
        Return a list of file paths in the specified directory, sorted naturally.

        Parameters  :
            dir (str): Directory path to scan for files.

        Returns:
            list: A list of file paths sorted naturally.

        """
        file_list      =   []   # Initialize an empty list to store file paths.
        for filename in dp.os.scandir(dir): # Iterate through each file in the specified directory.
            if filename.is_file() and filename.path.endswith('.csv') and not filename.path.endswith('_Map.csv'):    # Check if the file is a regular file, ends with '.csv', and does not end with '_Map.csv'.
                file_list.append(str(filename.path.replace("\\","/")))  # Append the file path to the list, replacing backslashes with forward slashes for consistency.
        file_list      =   dp.natsorted(file_list)  # Sort the file paths naturally using natsorted from the natsort library.
        return file_list    # Return the sorted list of file paths.

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
        core_loss   , pri_copper_loss , sec_copper_loss ,choke_core_loss    ,choke_copper_loss , Choke_loss= [],[],[],[],[],[]      # Initialize empty lists to store losses.
        for i in range(len(trafo_inputs)):                                                                                 #? Go over each trafo you have in the system.
            #! core losses :                
            LuT3D         = self.LuT_3D(trafo_inputs[i][0] ,trafo_inputs[i][1],trafo_inputs[i][2],trafo_inputs[i][3])   # Create the 3DLut for core losses.
            flux_link     = nestedresults[trafo_inputs[i][4]]                                                          # Get the flux linkage for the transformer.
            point_flux    = dp.np.round((dp.np.max(flux_link)-dp.np.min(flux_link))/2 , decimals=12 )               # Calculate the peak value of flux linkage.
            point_in_volt = dp.np.max(nestedresults[trafo_inputs[i][5]],axis=0)                         # Get the maximum voltage from the nested results.
            interp        = LuT3D([trafo_inputs[i][6],point_flux ,point_in_volt])                       # Interpolate the core loss using the 3D LUT.
            core_loss.append(interp[0] * trafo_inputs[i][7] )                                           # Append the core loss multiplied by the gain factor.
            #! primary losses :
            LuT2D         = self.LuT_2D(trafo_inputs[i][8],trafo_inputs[i][9],trafo_inputs[i][10])      # Create the 2DLut for primary copper losses.
            rvec_pri      = []                                              # Initialize an empty list to store primary resistance values.
            for j in range(len(dp.harmonics)):                              # Iterate over harmonics to calculate primary resistance values.
                interpolated_rpri = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][11]*len(dp.harmonics))[j]])    # Interpolate the primary resistance using the 2D LUT.
                rvec_pri.append(interpolated_rpri[0])           # Append the interpolated primary resistance value to the list.

            pri_copper_loss.append(dp.np.sum(dp.np.array(rvec_pri) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][16]-1] ))) # Calculate and append the primary copper loss.
            #! secondary losses :
            LuT2D         = self.LuT_2D(trafo_inputs[i][12],trafo_inputs[i][13],trafo_inputs[i][14])    # Create the 2DLut for secondary copper losses.
            rvec_sec      = []                                         # Initialize an empty list to store secondary resistance values.
            for j in range(len(dp.harmonics)):                             # Iterate over harmonics to calculate secondary resistance values.
                interpolated_rsec = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][15]*len(dp.harmonics))[j]])    # Interpolate the secondary resistance using the 2D LUT.
                rvec_sec.append(interpolated_rsec[0])         # Append the interpolated secondary resistance value to the list.
            sec_copper_loss.append(dp.np.sum(dp.np.array(rvec_sec) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][17]-1] ))) # Calculate and append the secondary copper loss.
        for i in range(len(choke_inputs)):                                                                                 #? Go over each trafo you have in the system.
            #! choke core losses :
            LuT3D         = self.LuT_3D(choke_inputs[i][0] ,choke_inputs[i][1],choke_inputs[i][2],choke_inputs[i][3])      # Create the 3DLut.
            flux_link     = nestedresults[choke_inputs[i][4]]                                                          # flux linkage .
            point_flux    = (dp.np.max(flux_link)-dp.np.min(flux_link))/2                                                  # Peak value of flux linkage.
            point_in_volt = dp.np.max(nestedresults[choke_inputs[i][5]])                                                # get the voltage.
            interp        = LuT3D([choke_inputs[i][6],point_flux ,point_in_volt])                                          # interplated value.
            choke_core_loss.append(interp[0] * choke_inputs[i][7] )                                                        # append choke_inputs[i][7]*Gain (Factor)
            #! choke copper losses :
            LuT2D         = self.LuT_2D(choke_inputs[i][8],choke_inputs[i][9],choke_inputs[i][10])                     # Create the 2DLut for choke copper losses.
            rvec          = []                                     # Initialize an empty list to store choke resistance values.
            for j in range(len(choke_inputs[i][13])):                          # Iterate over the harmonics to calculate choke resistance values.
                interpolated_rpri = LuT2D([(dp.np.array(choke_inputs[i][13])*dp.F_Fund)[j],(choke_inputs[i][11]*len(choke_inputs[i][13]))[j]])  # Interpolate the choke resistance using the 2D LUT.
                rvec.append(interpolated_rpri[0])   # Append the interpolated choke resistance value to the list.
            choke_copper_loss.append(dp.np.sum( dp.np.array(rvec)   * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),choke_inputs[i][12]-1][choke_inputs[i][13]])) )        # Calculate and append the choke copper loss.
            Choke_loss =  [dp.np.sum(choke_core_loss + choke_copper_loss)]  # Calculate the total choke loss by summing choke core and copper losses.
        return dp.np.array(core_loss) , dp.np.array(pri_copper_loss) , dp.np.array(sec_copper_loss) , dp.np.array(Choke_loss)           # Return the core losses, primary copper losses, secondary copper losses, and choke losses as numpy arrays.

    def analytical_magnetic_loss(self, nestedresults, FFT_current, l):
        """                                                                                                                         # Docstring for analytical_magnetic_loss function
        Calculate magnetic losses analytically for transformer core losses, primary copper losses, secondary copper losses, choke core and copper losses.

        Parameters  :
            nestedresults (dict)            : Nested results containing flux linkage and voltages for transformers and chokes.
            FFT_current (numpy.ndarray)     : FFT current values.
            l (int)                         : Index for time step or frequency bin.

        Returns:
            tuple: Tuple containing core losses, primary copper losses, secondary copper losses, choke core and copper losses.

        """
        core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss = [], [], [], [], []                        # Initialize empty lists for different loss types
        R_pri, R_sec, R_ind = [],[],[]                                                                                             # Initialize empty lists for resistances
        #! core losses :                                                                                                           # Comment indicating core losses calculation section
        flux_link     = nestedresults[dp.pmapping['Transformer Flux']]                                                              # Get flux linkage from nested results
        point_flux    = dp.np.round((dp.np.max(flux_link)-dp.np.min(flux_link))/2 , decimals=12 )                                  # Calculate point flux by rounding the difference between max and min flux
        # Bp            = point_flux/(dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['Ae'] * dp.mdlVars['DCDC_Rail1']['Trafo']['Np'])    # Commented out calculation for Bp
        # d             = [nestedresults[dp.pmapping['PWM Modulator Primary Modulator Duty Cycle'] + dp.Y_list[3] + 1]]             # Commented out calculation for duty cycle
        # d             = self.rms_avg('AVG', d, nestedresults[0])                                                                  # Commented out RMS average calculation
        # Vc            = dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['Vc']                                                           # Commented out volume calculation
        SP_tfo        = dp.mdlVars['DCDC_Rail1']['Trafo']['Core']['SP_tfo']                                                        # Get Steinmetz parameters for transformer
        d             = 0.532                                                                                                      # Hardcoded duty cycle value
        Bp            = 0.10776                                                                                                    # Hardcoded peak flux density
        Vc            = 468e-6 * 72.5e-3                                                                                           # Hardcoded core volume calculation
        core_loss.append(self.IGSE('trap', SP_tfo, d, dp.F_Fund, Bp, Vc))                                                         # Append core loss using IGSE method

        #! primary and secondary copper losses :                                                                                    # Comment indicating copper losses calculation section
        f_tfo         = [0] + dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Harmonics']                                            # Get transformer winding harmonics
        pri_Rvec        = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Rvec']                                              # Get primary resistance vector
        pri_Rscale      = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rpri']['Rscale']                                            # Get primary resistance scale factor
        sec_Rvec        = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Rvec']                                              # Get secondary resistance vector
        sec_Rscale      = dp.mdlVars['DCDC_Rail1']['Trafo']['Winding']['Rsec']['Rscale']                                            # Get secondary resistance scale factor
        for i in range(len(pri_Rvec)):                                                                                             # Loop through primary resistance vector
            R_pri.append(pri_Rvec[i][-1])                                                                                          # Append last element of each sub-vector
            R_sec.append(sec_Rvec[i][-1])                                                                                          # Append last element of each sub-vector
        res_optimize_pri = self.rac_lac_values('min', dp.mdlVars['DCDC_Rail1']['Trafo']['Lm'], dp.np.array(f_tfo)* 1e5, dp.np.array(R_pri))    # Optimize primary Rac/Lac values
        res_optimize_sec = self.rac_lac_values('min', dp.mdlVars['DCDC_Rail1']['Trafo']['Lm']/100, dp.np.array(f_tfo)* 1e5, dp.np.array(R_sec)) # Optimize secondary Rac/Lac values

        pri_copper_loss.append(dp.np.sum(res_optimize_pri['Rac_calculated']*pri_Rscale * (1/2) * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics), dp.pmapping['Transformer Primary Current']-1][f_tfo[1:]])))    # Calculate and append primary copper loss
        sec_copper_loss.append(dp.np.sum(res_optimize_sec['Rac_calculated']*sec_Rscale * (1/2) * dp.np.square(FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics), dp.pmapping['Transformer Secondary Current']-1][f_tfo[1:]])))  # Calculate and append secondary copper loss

        #! choke core losses :                                                                                                      # Comment indicating choke core losses section
        Iind = nestedresults[dp.pmapping['DC Choke Current']]                                                                      # Get choke current from nested results
        Iindp = (dp.np.max(Iind)- dp.np.min(Iind))/2                                                                               # Calculate peak choke current
        Bpl           = (dp.mdlVars['DCDC_Rail1']['Lf']['L'] * Iindp) / ( dp.mdlVars['DCDC_Rail1']['Lf']['N']* dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Ae'])    # Calculate peak flux density for choke
        Sp_choke      = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['SP_l']                                                              # Get Steinmetz parameters for choke
        Vcl           = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Vc']                                                                # Get choke core volume
        choke_core_loss.append(self.IGSE('tri', Sp_choke, d, 2*dp.F_Fund, Bpl, Vcl))                                               # Append choke core loss using IGSE method

        #! choke copper losses :                                                                                                    # Comment indicating choke copper losses section
        choke_current_fft = FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),dp.pmapping['DC Choke Current']-1]    # Get FFT of choke current
        ind_Rvec          = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Rwind']['Rvec']                                              # Get choke winding resistance vector
        ind_Rscale        = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Rwind']['Rscale']                                            # Get choke winding resistance scale factor
        f_ind             = dp.mdlVars['DCDC_Rail1']['Lf']['Winding']['Harmonics']                                                  # Get choke winding harmonics
        for i in range(len(ind_Rvec)):                                                                                              # Loop through choke resistance vector
            R_ind.append(ind_Rvec[i][-1])                                                                                           # Append last element of each sub-vector
        choke_copper_loss.append(dp.np.sum(dp.np.array(R_ind[1:]) * ind_Rscale * (1/2) * dp.np.square(choke_current_fft[f_ind[1:]])) + (dp.np.array(R_ind[0]) * ind_Rscale * dp.np.square(choke_current_fft[0])))    # Calculate and append choke copper loss

        return dp.np.array(core_loss), dp.np.array(pri_copper_loss), dp.np.array(sec_copper_loss), dp.np.array(choke_core_loss), dp.np.array(choke_copper_loss)    # Return all loss arrays

    def dissipations(self, nestedresults_l, res_list, RMS_currents, thread, FFT_current): # trafo_inputs, choke_inputs):
        """                                                                                                                         # Docstring for dissipations function
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
        dissip                                                       = self.rms_avg('AVG',nestedresults_l[sum(dp.Y_list[0:3]):sum(dp.Y_list[0:4]),  : ], nestedresults_l[0])    # Calculate average dissipation
        # core_loss , pri_copper_loss , sec_copper_loss , Choke_loss   = self.magnetic_loss(nestedresults_l,FFT_current,thread, trafo_inputs , choke_inputs)                       # Commented out old magnetic loss calculation
        core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss = self.analytical_magnetic_loss(nestedresults_l, FFT_current, thread)                     # Calculate magnetic losses analytically
        res_dissip                                                   = (dp.np.square(RMS_currents[thread,0:dp.current_idx]))*res_list                                            # Calculate resistive dissipation
        # Dissipation_matrix                                           = dp.np.concatenate((dissip, pri_copper_loss , sec_copper_loss , core_loss ,Choke_loss,res_dissip))         # Commented out old dissipation matrix
        Dissipation_matrix                                           = dp.np.concatenate((dissip, core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss, res_dissip))    # Create new dissipation matrix
        # print(dp.np.shape(dissip), dp.np.shape(core_loss), dp.np.shape(pri_copper_loss), dp.np.shape(sec_copper_loss), dp.np.shape(choke_core_loss), dp.np.shape(choke_copper_loss), dp.np.shape(res_dissip))    # Commented out shape printing
        return Dissipation_matrix                                                                                                  # Return dissipation matrix

    def therm_stats(self,MAT_list,thread,P_aux):
        """                                                                                                                         # Docstring for therm_stats function
        Calculate thermal statistics including efficiency, total dissipation, and input power.

        Parameters  :
            MAT_list (list) : List containing matrices of thermal data.
            thread (int)    : Thread index.

        Returns:
            numpy.ndarray: Thermal matrix including total dissipation, efficiency, and input power.

        """
        P_rail      =   dp.np.sum(MAT_list[8][thread , dp.Rail_idx:dp.Common_idx+1])                            # Calculate total rail losses
        P_common    =   dp.np.sum(MAT_list[8][thread , dp.Common_idx+1:])                                       # Calculate total common losses
        Pout        =   dp.np.mean(MAT_list[9][thread, dp.Pout_idx])                                            # Calculate output power
        # Calculate eff for each factorial value in the list using list comprehension                            # Comment about efficiency calculation
        Eff         =   dp.np.array([(((Pout / ( Pout + P_rail + (factorial * P_common))*100.0) if ( Pout + P_rail + (factorial * P_common)) != 0 else 0.0)) for factorial in list(range(1, dp.phase + 1))])    # Calculate efficiency array
        Eff_Aux     =   dp.np.array([(((Pout / ( Pout + (P_rail + (factorial * P_common))+P_aux)*100.0) if ( Pout + P_rail + (factorial * P_common)) != 0 else 0.0)) for factorial in list(range(1, dp.phase + 1))])    # Calculate efficiency with auxiliary power
        # Calc Total dissipation                                                                                 # Comment about total dissipation
        Ptot        =   dp.np.array([(P_rail*factorial + P_common*factorial**2) for factorial in list(range(1, dp.phase + 1))])    # Calculate total dissipation array
        # Input Power                                                                                            # Comment about input power
        Pin         =   dp.np.array([((P_rail + Pout)*factorial + P_common*factorial**2) for factorial in list(range(1, dp.phase + 1))])    # Calculate input power array
        Th_mat      =   dp.np.concatenate((Ptot , Eff , Eff_Aux , Pin))                                        # Concatenate thermal metrics
        if MAT_list[11].shape == (1, 1):                                                                       # Check if MAT_list[11] has shape (1,1)
            return dp.np.empty((1,))                                                                            # Return empty array if true
        else:                                                                                                  # Else case
            return Th_mat                                                                                      # Return thermal matrix

    def insert_array(self, file_path, index, data_to_insert):
        """                                                                                                                         # Docstring for insert_array function
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
        """                                                                                                                         # Docstring for drop_Extra_Cols function
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
        """                                                                                                                         # Docstring for LuT_2D function
        Create a 2D Look-Up Table (LuT) using linear interpolation.

        Parameters  :
            x (list)            : List of values for the first dimension.
            y (list)            : List of values for the second dimension.
            z (numpy.ndarray)   : 2D array of values for the LuT.

        Returns:
            RegularGridInterpolator: Interpolation function for the LuT.

        """
        interp_func     = dp.RegularGridInterpolator((x, y), z, method='linear', bounds_error=False, fill_value=None)    # Create 2D interpolation function
        return interp_func                                                                                              # Return interpolation function

    def LuT_3D(self, x, y, z, data):
        """                                                                                                                         # Docstring for LuT_3D function
        Create a 3D Look-Up Table (LuT) using linear interpolation.

        Parameters  :
            x (list)                : List of values for the first dimension.
            y (list)                : List of values for the second dimension.
            z (list)                : List of values for the third dimension.
            data (numpy.ndarray)    : 3D array of values for the LuT.

        Returns:
            RegularGridInterpolator: Interpolation function for the LuT.

        """
        interp_func     = dp.RegularGridInterpolator((x,y,z), data, method='linear', bounds_error=False, fill_value=None)    # Create 3D interpolation function
        return interp_func                                                                                                  # Return interpolation function

    def resample(self, time, signal):
        """                                                                                                                         # Docstring for resample function
        Resample a signal to have uniform time points.

        Parameters  :
            time (numpy.ndarray)    : Time values of the original signal.
            signal (numpy.ndarray)  : Signal values.

        Returns:
            tuple: Tuple containing the resampled time values and the corresponding resampled signal values.

        """
        new_t       = dp.np.linspace(time.min(), time.max(), len(signal))    # Create new uniformly spaced time vector
        new_signal  = dp.np.interp(new_t,time,signal)                       # Interpolate signal at new time points
        return new_t,new_signal                                             # Return new time and signal vectors

    def IIR_Filter(self, Time, Signal, Cutoff, Order=2, BType='low', FType='butter'):
        """
        Design and apply an Infinite Impulse Response (IIR) filter to a signal with zero-phase distortion.

        This function uses SciPy's signal processing module (scipy.signal) to design and apply Butterworth, Chebyshev, 
        or other IIR filters. Zero-phase filtering is achieved using filtfilt, which processes the signal forward 
        and backward to eliminate phase delay.

        Libraries Used:
        - scipy.signal.iirfilter  (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirfilter.html)    :Designs an IIR filter of specified type (Butterworth, Chebyshev, etc.) and order.
        - scipy.signal.filtfilt (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html)     :Applies zero-phase filtering by processing the signal forward and backward.

        Parameters:
        - Time      (numpy.ndarray)       : Time vector corresponding to the signal (in seconds). Used to calculate the sampling frequency.
        - Signal    (numpy.ndarray)       : Input signal to be filtered (1D array).
        - Cutoff    (float or list)       : Cutoff frequency (Hz) for low/high-pass filters, or [low, high] frequencies for band-pass/stop filters.
        - Order     (int, optional)       : Order of the filter. Higher orders provide steeper roll-off but may introduce numerical instability. Default: 2.
        - BType     (str, optional)       : Filter type: 'low' (low-pass), 'high' (high-pass), 'band' (band-pass), or 'bandstop'. Default: 'low'.
        - FType     (str, optional)       : Filter design type: 'butter' (Butterworth), 'cheby1' (Chebyshev Type I), 'cheby2' (Chebyshev Type II), or 'ellip' (elliptic). Default: 'butter'.

        Returns:
        - numpy.ndarray               : The filtered signal with zero-phase distortion.

        """

        dt                  =   Time[1] - Time[0]                                                                                   # Calculate time step
        Fs                  =   1.0/dt                                                                                             # Calculate sampling frequency
        Fn                  =   min(Fs/2-1, Cutoff)                                                                                # Calculate Nyquist frequency

        b,a                 =   dp.scipy.signal.iirfilter(Order, Wn=Fn, fs=Fs, btype=BType, ftype=FType)                           # Design IIR filter
        Signal_Filtered     =   dp.scipy.signal.filtfilt(b, a, Signal)                                                             # Apply zero-phase filtering

        return Signal_Filtered                                                                                                     # Return filtered signal

    def pyFFT(self, signal, fs):
        """
        Compute the Fast Fourier Transform (FFT) of a signal and return amplitude, phase, and frequency information.
        
        This function uses SciPy's FFT implementation (scipy.fft) which provides efficient numerical computation
        of the discrete Fourier Transform. The function automatically utilizes all available CPU cores for parallel
        computation.

        Libraries used:
        - scipy.fft             (https://docs.scipy.org/doc/scipy/reference/fft.html)                                              : Fast Fourier Transform implementation
        - scipy.fftpack.fftfreq (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fftfreq.html#scipy.fft.fftfreq)    : Frequency bin calculation

        Parameters:
            signal (numpy.ndarray)      : Input time-domain signal (1D array)
            fs (float)                  : Sampling frequency of the signal in Hz

        Returns:
            tuple: Contains three elements:
                - amplitude (numpy.ndarray) : Scaled FFT magnitude spectrum 
                - phase (numpy.ndarray)     : Phase angles in degrees [0-360]
                - frequency (numpy.ndarray) : Frequency bins in Hz corresponding to the amplitude/phase values

        Notes:
            1. The DC component (0 Hz) is scaled by 1/N
            2. All other components are scaled by 2/N
            3. Only positive frequencies are returned
            4. Phase values are wrapped in the range [-180, 180] degrees
        """
        N               = len(signal)                                                   # Get length of signal
        f               = dp.fftfreq(N,1/fs)                                            # Calculate frequency bins
        f               = f[f >= 0]                                                     # Keep only positive frequencies
        useful          = dp.np.arange(0, len(f)/2, dtype=int)                          # Select useful indices and corresponding frequency values
        fft             = dp.fft(x=signal,workers=dp.multiprocessing.cpu_count())       # Compute FFT using all available CPUs
        amplitude       = dp.np.abs(fft)                                                # Calculate magnitude of FFT result
        amplitude[0]    = (1/N) * amplitude[0]                                          # Scale DC component
        amplitude[1:N]  = (2/N) * amplitude[1:N]                                        # Scale other components
        amplitude       = amplitude[useful]                                             # Select useful frequency components
        pahse           = dp.np.angle(fft[useful],deg=True)                             # Calculate phase angles in degrees
        frequency       = f[useful]                                                     # Select useful frequencies
        return amplitude, pahse, frequency                                              # Return amplitude, phase and frequency

    def safe_get(self,my_list, index):
        try:                                                                                    # Try block for safe list access
            return my_list[index]                                                               # Return list element if index exists
        except IndexError:                                                                      # Catch index error
            return None                                                                         # Return None if index doesn't exist

    def FFT_mat(self, T_vec, nestedresults):
        """                                                                                                                        
        Compute the Fast Fourier Transform (FFT) matrix of nested results.

        Parameters  :
            T_vec (numpy.ndarray)           : Time vector.
            nestedresults (numpy.ndarray)   : Nested results array.

        Returns:
            numpy.ndarray: Transposed FFT matrix.

        """
        fft_mat     =   dp.np.zeros((len(nestedresults),len(dp.harmonics)))                      # Initialize FFT matrix with zeros

        for x in range(len(nestedresults)):                                                      # Loop through nested results
            if dp.mdlVars['Common']['ToFile']['Ts'] == 0:                                        # Check for variable sampling
                time_vec,signal_vec  = self.resample(T_vec, nestedresults[x])                    # Resample if variable sampling
            else :                                                                               # Fixed sampling case
                time_vec,signal_vec  = T_vec, nestedresults[x]                                  # Use original vectors

            # time_vec             = T_vec                                                       # Commented out time vector assignment
            # signal_vec           = nestedresults[x]                                            # Commented out signal vector assignment
            dt                   = time_vec[-1]-time_vec[0]                                      # Calculate time duration
            fs                   = 1/((dp.np.round(dt,decimals=6)))                              # Calculate sampling frequency
            Magnitude , _ ,_     = self.pyFFT(signal_vec , dp.F_Fund)                            # Compute FFT
            idx                  = [int(c) for c in (((dp.np.array(dp.harmonics,dtype=int)*dp.F_Fund).tolist())/fs).tolist()]    # Calculate harmonic indices
            Mag_array            = [self.safe_get(Magnitude, index) for index in idx if self.safe_get(Magnitude, index) is not None]    # Get magnitudes at harmonic frequencies
            fft_mat[x, :]        = dp.np.pad(Mag_array, (0, len(dp.harmonics) - len(Mag_array)), 'constant')    # Pad magnitude array
        return dp.np.transpose(fft_mat)                                                         # Return transposed FFT matrix

    def remove_duplicates(self, nested_array):
        """                                                                                                                         # Docstring for remove_duplicates function
        Remove duplicates from a nested array.

        Parameters:
            nested_array (list): Nested array containing subarrays.

        Returns:
            list: Modified nested array without duplicate values.

        """
        seen_values         = set()                                                                                             # Initialize set to track seen values
        indexes_to_remove   = {i for i, value in enumerate(nested_array[0]) if value in seen_values or seen_values.add(value)}   # Find duplicate indexes
        nested_array[:]     = [[value for j, value in enumerate(row) if j not in indexes_to_remove] for row in nested_array[:]]  # Remove elements at duplicate indexes
        return nested_array                                                                                                     # Return modified array

    def findMissingResults(self,path,itr,threads_vector,Threads):
        """                                                                                                                         # Docstring for findMissingResults function
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
        file_list           =   []                                                                                                # Initialize empty file list
        Iters               =   []                                                                                                # Initialize empty iteration list
        if dp.JSON['hierarchical']:                                                                                               # Check hierarchical mode
            iteration_range     =   list(range(1,sum(threads_vector[0:itr+1])+1))                                                # Calculate iteration range for hierarchical
        else:                                                                                                                    # Non-hierarchical case
            iteration_range     =   list(range(1,Threads*(itr+1)+1))                                                             # Calculate iteration range for non-hierarchical
        for filename in dp.os.scandir(path):                                                                                     # Scan directory for files
            file_list.append(str(filename.path.replace("\\","/")))                                                               # Add file paths to list

        for i in range(len(file_list)):                                                                                          # Loop through file list
            x               =   file_list[i].split("s_")[-1]                                                                     # Extract iteration number from filename
            x               =   x.split(".")[0]                                                                                  # Remove file extension
            x               =   x.split("_")[-1]                                                                                 # Get iteration number
            Iters.append(int(x))                                                                                                 # Add to iterations list
            Iters.sort()                                                                                                        # Sort iterations

        Set                 =   set(Iters)                                                                                      # Convert to set
        Missing             =   [x for x in iteration_range if x not in Set]                                                     # Find missing iterations
        return Missing                                                                                                           # Return missing iterations

    def last_filled_X(self):
        """                                                                                                                         # Docstring for last_filled_X function
        Find the last non-empty X input list from the JSON configuration.

        Returns:
            int: Length of the last non-empty X input list, or 0 if all are empty.
        """
        lists = [dp.JSON[f'X{i}']for i in range(1,11)]                                                                          # Construct list of X input lists from JSON
        for lst in reversed(lists):                                                                                             # Iterate from last to first
            lst     = dp.ast.literal_eval(lst)                                                                                  # Safely evaluate string to list
            if lst != [0]:                                                                                                      # Check if list is not [0]
                return len(lst)                                                                                                 # Return length of first non-zero list
        return 0                                                                                                                # Return 0 if all lists are [0]

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
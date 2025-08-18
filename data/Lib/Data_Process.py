
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
from scipy.integrate import quad
from scipy.optimize import minimize, least_squares

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class Processing:
    def __init__(self):
        pass

    def append_zeros(self,nestedresults):
        """
        Append zeros to the nestedresults array to make sure that all sub-arrays have
        the desired length as specified in the 'ToFile' dictionary.

        Args:
            nestedresults (numpy.ndarray)   : The nested array of results to be padded with zeros.
            misc (object)                   : An object containing miscellaneous settings and variables.

        Returns:
            numpy.ndarray                   : The modified nested array of results, with zeros appended to
                                            sub-arrays that do not have the desired length as specified in
                                            the 'ToFile' dictionary.
        """
        actual_lengths 		= 	[1]						                        # list of actual lengths , will be filled from the dict
        list_of_indices 	= 	[]						                        # list of the indices of the missing arrays
        list_of_lens		=	[]						                        # list of the lengths correspondiding to the indices
        del_idx_list        =   []                                              #
        del_len_list        =   []                                              #
        pattern             =   r'Y(?!2|3|5|6|7|8|12)'                              # Define a pattern that matches the Ys in plecs
        for key in dp.ToFile.keys():                                            # get the desired lengths from the tofile dict into a list
            if 'Y' in key and dp.re.findall(pattern, key):                      #
                actual_lengths.append(dp.ToFile[key]['Length'] )                # use plecs_lens instead of desired and pop out the extra ys
        for i in range(len(actual_lengths)):                                    #
            if not actual_lengths[i] == dp.Y_list[i]:                           #
                sum_of_previous_values = sum(dp.Y_list[:i])                     #
                list_of_indices.append(sum_of_previous_values)                  #
                list_of_lens.append(dp.Y_list[i])                               #
            elif  actual_lengths[i] == dp.Y_list[i] and dp.Y_list[i] == 1:      #
                sum_of_previous_values = sum(dp.Y_list[:i])                     #
                del_idx_list.append(sum_of_previous_values)                     #
                del_len_list.append(dp.Y_list[i])                               #
        for index, x in zip(list_of_indices, list_of_lens):                     # go over the newly populated lists and patch up the array
            zeros = dp.np.zeros((x-1, len(nestedresults[0])))      #
            nestedresults = dp.np.insert(nestedresults, index, zeros,axis=0)    #
        return nestedresults

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
        file            = directory_path + f"/results_{utc}_{str(itr+1)}.csv"
        dataFrame       = dp.pd.read_csv(file, header=None, dtype=str).transpose()
        try:
            listcols   = (dataFrame.apply(lambda col: col.map(Decimal))).values.tolist()
        except Exception:
            print("Could not apply Decimal.")
            pass
        df              = (dp.pd.DataFrame(listcols, dtype=object).transpose()).dropna()
        df.to_csv(file, index=False, header=None, mode='w')
        return listcols

    def col2csv(self,nestedlist,filename,itr,mode='a'):
        """
            Saves a list of lists to a csv file as columns.

            Args:
                nestedlist (list)   : List of lists to be saved.
                filename (string)   : Path to the csv file.
                itr (int)           : Starting index for the file name.
                mode (string)       : Mode for opening the file (default is 'a', append).

            Returns:
                None. The function saves the csv file to the specified path.

            Raises:
                None.
        """
        df = dp.pd.DataFrame(nestedlist).transpose()
        df2 = df.dropna()
        df2.to_csv(filename +str(itr+1) + '.csv', index=None,header=None,mode=mode)

    def csvSlice(self,fileName,startIndex,endIndex):
        """
            Reads a CSV file and returns the columns as a nested list between two specific indices.

            Args:
                fileName (str)      : The path to the CSV file.
                startIndex (int)    : The starting index of the columns to return.
                endIndex (int)      : The ending index of the columns to return.

            Returns:
                List[List[str]]     : A nested list containing the columns between the start and end index.

            Raises:
                FileNotFoundError   : If the file does not exist in the specified path.
                ValueError          : If the start index is greater than or equal to the end index.
                TypeError           : If the file is not a CSV file.
        """
        dataFrame       =   dp.pd.read_csv(fileName,header = None)
        dataFrame       =   dataFrame.iloc[startIndex:endIndex]
        array           =   dataFrame.T.to_numpy().tolist()
        return array

    def csv_col_merge(self,dir,filename):
        """
        Combines multiple CSV files in a directory into a single CSV file with columns.

        Args:
            dir (str)           : The directory path containing the CSV files.
            filename (str)      : The path and name of the file to save the merged CSV to.

        Returns:
            None

        Raises:
            FileNotFoundError   : If the directory specified does not exist.
            TypeError           : If the directory does not contain any CSV files.
        """
        dp.os.chdir(dir)
        extension = 'csv'
        all_filenames = [i for i in dp.glob.glob('*.{}'.format(extension))]
        x=[]    #combine all files in the list
        for f in all_filenames:
            df = dp.pd.read_csv(f,delimiter=',',index_col=None,header=None)
            x.append(df)
            for i in range(len(x)-1):
                combined_csv = dp.pd.merge(x[i],right=x[i+1],left_index=True, right_index=True) # using merge function by setting how='inner'
        combined_csv.to_csv( filename ,index=None,header=None, encoding='utf-8-sig') #export to csv

    def csv_row_merge(self,dir,filename):
        """
        Combines multiple CSV files in a directory into a single CSV file.

        Args:
        - dir (str)             : Path to the directory containing CSV files.
        - filename (str)        : Path and name of the merged CSV file to be saved.

        Returns:
        - None

        Raises:
        - FileNotFoundError     : If the specified directory does not exist.
        - ValueError            : If the specified directory does not contain any CSV files.
        - Exception             : If an error occurs while trying to merge and export the CSV files.

        Description:
        - The function takes in a directory path and a file name as arguments.
        - It searches for all CSV files in the directory and combines them into a single CSV file.
        - The merged CSV file is then saved with the specified file name in the specified directory.
        - The function returns None.
        """
        dp.os.chdir(dir)
        extension = 'csv'
        all_filenames = [i for i in dp.glob.glob('*.{}'.format(extension))]
        x=[] #combine all files in the list
        for f in all_filenames:
            df = dp.pd.read_csv(f,delimiter=',',index_col=None,header=None)
            x.append(df)
            combined_csv = dp.pd.concat(x)
        combined_csv.to_csv( filename ,index=None,header=None, encoding='utf-8-sig',line_terminator=None) #export to csv

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
        resultsvect     = []
        longest_length = max(len(results[c]['Time']) for c in range(len(results)))
        for i in range(len(results)):
            timevector          = results[i]['Time']
            difference_lengths  = longest_length - len(timevector)
            NaNarray            = dp.np.empty((difference_lengths))
            NaNarray[:]         = dp.nan
            valuesvector        = results[i]['Values']
            outputresults       = []
            timevector = dp.np.append(NaNarray,timevector)
            outputresults.append(timevector)
            for j in range(len(valuesvector)):
                valuesvector[j] = dp.np.append(NaNarray,valuesvector[j])
                outputresults.append(valuesvector[j])
            resultsvect.append(outputresults)
        return resultsvect

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
        resultsvect             = []
        longest_length          = max(map(len, results))  # Find the longest sublist
        for sublist in results:
            difference_lengths  = longest_length - len(sublist)
            NaNarray            = dp.np.full(difference_lengths, dp.np.nan)  # Create an array of NaNs
            outputresults       = [dp.np.append(NaNarray, dp.np.array(item)).tolist() for item in sublist]
            resultsvect.append(outputresults)
        return resultsvect

    def simResultsSlice(self,Nresult,ibegin,iend):
        """
        Slices a nested list between two indices.

        Args:
            Nresult (list)          : A nested list of simulation results.
            ibegin (int)            : The starting index for the slice.
            iend (int)              : The ending index for the slice.

        Returns:
            sliced_results (list)   : A nested list of simulation results sliced between the specified indices.

        Examples:
            >>> Nresult = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            >>> simResultsSlice(Nresult, 0, 2)
            [[1, 2], [4, 5], [7, 8]]

            >>> Nresult = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            >>> simResultsSlice(Nresult, 1, 3)
            [[2, 3], [5, 6], [8, 9]]
        """
        sliced_results = Nresult
        for i in range(len(sliced_results)):
            sliced_results[i] = sliced_results[i][ibegin:iend]
        return sliced_results

    def sliceList(self,Nresult,ibegin,iend):
        """
        Slices a nested list between two indices.

        Args:
            Nresult (list)      : A nested list.
            ibegin (int)        : The starting index of the slice.
            iend (int)          : The ending index of the slice.

        Returns:
            list                : The sliced nested list.

        The function takes a nested list as input along with the starting and ending indices for slicing the inner lists.
        It returns the sliced nested list.

        Example:
        >>> sliceList([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 1)
        [[1, 2], [4, 5], [7, 8]]

        """
        sliced_results = Nresult
        for i in range(len(sliced_results)):
            sliced_results[i] = Nresult[i][ibegin:iend+1]
        return sliced_results

    def csvrow2list(self,csvfile):
        """
        Reads a CSV file and converts its rows into a nested list.

        Args:
            csvfile (str)       : The path to the CSV file.

        Returns:
            List[List[str]]     : A nested list containing the rows of the CSV file.
        """
        df          = dp.pd.read_csv(csvfile, delimiter=',', header=None, index_col=False)
        list_of_csv = [list(row) for row in df.values]
        return list_of_csv

    def csvcol2list(self,fileName):
        """
        Reads a CSV file and returns the columns between the specified start and end indices
        as a nested list.

        Args:
            fileName (str)          : The path to the CSV file.
            startIndex (int)        : The index of the first column to include.
            endIndex (int)          : The index of the last column to include.

        Returns:
            List[List[str]]         : A nested list containing the CSV columns between startIndex and endIndex,
            where each inner list represents a single column of the CSV file.
        """
        file    =   (fileName + '.csv').replace("\\","/")
        dataFrame       =   dp.pd.read_csv(file,header = None).transpose()
        listcols        =   dataFrame.to_numpy().tolist()
        if len(listcols)>1:
            return listcols
        else:
            return listcols[0]

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
        path    =   dp.os.getcwd() + '/'
        array   =   []
        with open(path + fileName + '.csv') as f:
            line            =   f.readline()
            firstRow        =   line.split(",")
            columnsNumber   =   len(firstRow)
            for i in range(columnsNumber):
                array.append([])
                array[i].append((float(firstRow[i])))
            for row in f:
                for i in range(columnsNumber):
                    otherRows   =   row.split(",")
                    array[i].append((float(otherRows[i])))
        return array

    def parseArraysTo(self,Data,Point,Index):
        """
        Takes in a nested list of numerical data `Data`, an integer `Point`, and an integer `Index`
        representing the index of the element array that is monotonically increasing. The function
        returns a nested list that contains the same number of arrays as `Data`, but where each array
        only contains the elements up to the index `idx` corresponding to the first element in the `Index`
        array that is greater than or equal to `Point`.

        Args:
            Data (list)     : A nested list of numerical data where each element array corresponds to a different variable or feature.
            Point (int)     : A desired endpoint up to where the nested arrays are to be returned.
            Index (int)     : The index of the element array that is monotonically increasing.

        Returns:
            list: A nested list that contains the same number of arrays as `Data`, but where each array only
            contains the elements up to the index `idx` corresponding to the first element in the `Index` array
            that is greater than or equal to `Point`.
        """
        idx = 0
        for i in range(len(Data[Index])):
            if Data[Index][i] >= Point:
                idx = i
                break
        array = []
        for i in range(len(Data)):
            array.append([])
            for j in range(idx + 1):
                array[i].append(Data[i][j])
        return array

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
        >>> data = [[1.1, 2.2, 3.3], [-4.4, -5.5, -6.6], [7.7, 8.8, 9.9]]
        >>> get_index(data, 2.0, 0)
        1
        >>> get_index(data, -5.0, 1)
        1
        >>> get_index(data, 8.8, 2)
        1
        """
        array   =   dp.np.asarray(Data[Index])
        idx     =   dp.np.nanargmin(dp.np.abs(array - Point))
        return idx

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
        # Check if data is a list
        if not isinstance(data, list):
            raise TypeError("data should be a list.")
        # Check if the data list is empty
        if len(data) == 0:
            raise ValueError("data list cannot be empty.")
        # Check if all elements in the data list are lists
        if all(isinstance(i, list) for i in data):
            # If yes, create a Pandas DataFrame from the list
            df = dp.pd.DataFrame(list(data))
        else:
            # If not, create a Pandas DataFrame from the transposed list
            df = dp.pd.DataFrame(data).T
        # Write the DataFrame to the specified CSV file
        df.to_csv(fileName, mode=save_mode, index=False, header=False)

    def findIndex(self,points,matrix,pattern=True):
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
        indices = []
        if pattern:
            # Find the index of each point in its respective row
            indices = [matrix[i].index(points[i]) for i in range(len(points))]
            # Compute the weighted sum dynamically instead of hardcoding
            itr = sum(
                indices[i] * dp.np.prod([len(matrix[j]) for j in range(i + 1, len(matrix))])
                for i in range(len(indices) - 1)
            ) + indices[-1]  # Last index is added directly
            indices.append(itr)  # Append computed index for reference
        else:
            # Find the index of the first point in the first row
            itr = matrix[0].index(points[0])
            indices = dp.np.full(len(matrix) + 1, itr).tolist()  # Fill with the same value
        return indices, itr

    def findPoint(self,matrix,index,pattern=True):
        """_summary_

        Args:
            matrix (_type_): _description_
            index (_type_): _description_
            pattern (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if not pattern:
            # Find the maximum row length in the matrix to standardize dimensions
            max_len = max(len(row) for row in matrix)
            # Pad shorter rows with zeros so that all rows are of equal length
            padded_matrix = [row + [0] * (max_len - len(row)) for row in matrix]
            padded_matrix = dp.np.array(padded_matrix).T
            return padded_matrix, len(padded_matrix)  # Return matrix and the number of rows (length of first column)

        # Compute the product of all sublist lengths to determine total number of rows
        lengths = [len(sublist) for sublist in matrix]
        totalLengths = dp.np.prod(lengths)
        ParametersMap = dp.np.zeros((totalLengths, len(matrix)))  # Initialize empty matrix of correct shape

        step_size = totalLengths  # Start with total length
        for col, sublist in enumerate(matrix):
            step_size //= lengths[col]  # Reduce step size for each column
            repeat_factor = totalLengths // (step_size * lengths[col])  # Compute how often values should repeat
            ParametersMap[:, col] = dp.np.tile(dp.np.repeat(sublist, step_size), repeat_factor)  # Fill column efficiently

        return ParametersMap[index[-1]:], len(ParametersMap[index[-1]:])  # Slice according to index and return

    def findStart(self,matrix,index,pattern=True):
        """_summary_

        Args:
            matrix (_type_): _description_
            index (_type_): _description_
            pattern (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if pattern:
            return [row[:] for row in matrix]  # Create a shallow copy of each row and return

        # Convert the selected portion of matrix to a numpy array, transpose it, and convert it back to a list
        ParametersMap = dp.np.array(matrix[index[-1]:]).T.tolist()
        return ParametersMap

    def dump_json_data(self,json_file):
        """_summary_

        Args:
            json_file (_type_): _description_

        Returns:
            _type_: _description_
        """
        path = dp.os.getcwd().replace("\\","/")+"/Script/assets/"+json_file
        file = open(path,encoding='utf-8')   # Opening JSON file
        data = dp.json.load(file)   # returns JSON object as a dictionary
        file.close()
        return data

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

        Parameters:
            dir (str): Directory path to scan for files.

        Returns:
            list: A list of file paths sorted naturally.

        """
        file_list      =   []
        for filename in dp.os.scandir(dir):
            if filename.is_file() and filename.path.endswith('.csv') and not filename.path.endswith('_Map.csv') and not filename.endswith('_Standalone.csv'):
                file_list.append(str(filename.path.replace("\\","/")))
        file_list      =   dp.natsorted(file_list)
        return file_list

    def magnetic_loss(self, nestedresults, FFT_current, l, trafo_inputs, choke_inputs):
        """
        Calculate magnetic losses in a transformer system including core losses, primary copper losses, secondary copper losses, and choke losses.

        Parameters:
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
            #! core losses:
            LuT3D         = self.LuT_3D(trafo_inputs[i][0] ,trafo_inputs[i][1],trafo_inputs[i][2],trafo_inputs[i][3])
            flux_link     = nestedresults[trafo_inputs[i][4]]
            point_flux    = dp.np.round((dp.np.max(flux_link)-dp.np.min(flux_link))/2 , decimals=12 )
            point_in_volt = dp.np.max(nestedresults[trafo_inputs[i][5]],axis=0)
            interp        = LuT3D([trafo_inputs[i][6],point_flux ,point_in_volt])
            core_loss.append(interp[0] * trafo_inputs[i][7] )
            #! primary losses:
            LuT2D         = self.LuT_2D(trafo_inputs[i][8],trafo_inputs[i][9],trafo_inputs[i][10])
            rvec_pri      = []
            for j in range(len(dp.harmonics)):
                interpolated_rpri = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][11]*len(dp.harmonics))[j]])
                rvec_pri.append(interpolated_rpri[0])

            pri_copper_loss.append(dp.np.sum(dp.np.array(rvec_pri) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][16]-1] )))
            #! secondary losses:
            LuT2D         = self.LuT_2D(trafo_inputs[i][12],trafo_inputs[i][13],trafo_inputs[i][14])
            rvec_sec      = []
            for j in range(len(dp.harmonics)):
                interpolated_rsec = LuT2D([(dp.np.array(dp.harmonics)*dp.F_Fund)[j],(trafo_inputs[i][15]*len(dp.harmonics))[j]])
                rvec_sec.append(interpolated_rsec[0])
            sec_copper_loss.append(dp.np.sum(dp.np.array(rvec_sec) * (1/2) * dp.np.square( FFT_current[l*len(dp.harmonics):l*len(dp.harmonics)+len(dp.harmonics),trafo_inputs[i][17]-1] )))
        for i in range(len(choke_inputs)):                                                                                 #? Go over each trafo you have in the system.
            #! choke core losses:
            LuT3D         = self.LuT_3D(choke_inputs[i][0] ,choke_inputs[i][1],choke_inputs[i][2],choke_inputs[i][3])      # Create the 3DLut.
            flux_link     = nestedresults[choke_inputs[i][4]]                                                          # flux linkage .
            point_flux    = (dp.np.max(flux_link)-dp.np.min(flux_link))/2                                                  # Peak value of flux linkage.
            point_in_volt = dp.np.max(nestedresults[choke_inputs[i][5]])                                                # get the voltage.
            interp        = LuT3D([choke_inputs[i][6],point_flux ,point_in_volt])                                          # interplated value.
            choke_core_loss.append(interp[0] * choke_inputs[i][7] )                                                        # append choke_inputs[i][7]*Gain (Factor)
            #! choke copper losses:
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

        Parameters:
            nestedresults (dict)            : Nested results containing flux linkage and voltages for transformers and chokes.
            FFT_current (numpy.ndarray)     : FFT current values.
            l (int)                         : Index for time step or frequency bin.

        Returns:
            tuple: Tuple containing core losses, primary copper losses, secondary copper losses, choke core and copper losses.

        """
        core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss = [], [], [], [], []
        R_pri, R_sec, R_ind = [],[],[]
        #! core losses:
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

        #! primary and secondary copper losses:
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

        #! choke core losses:
        Iind = nestedresults[dp.pmapping['DC Choke Current']]
        Iindp = (dp.np.max(Iind)- dp.np.min(Iind))/2
        Bpl           = (dp.mdlVars['DCDC_Rail1']['Lf']['L'] * Iindp) / ( dp.mdlVars['DCDC_Rail1']['Lf']['N']* dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Ae'])
        Sp_choke      = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['SP_l']
        Vcl           = dp.mdlVars['DCDC_Rail1']['Lf']['Core']['Vc']
        choke_core_loss.append(self.IGSE('tri', Sp_choke, d, 2*dp.F_Fund, Bpl, Vcl))

        #! choke copper losses:
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

        Parameters:
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
        dissip                                                       = self.rms_avg('AVG',nestedresults_l[sum(dp.Y_list[0:3]):sum(dp.Y_list[0:4]),:],nestedresults_l[0])
        res_dissip                                                   = (dp.np.square(RMS_currents[thread,0:dp.current_idx]))*res_list
        # core_loss, pri_copper_loss, sec_copper_loss,\
        # choke_core_loss, choke_copper_loss                           = self.analytical_magnetic_loss(nestedresults_l, FFT_current, thread)

        # Dissipation_matrix                                           = dp.np.concatenate((dissip, core_loss, pri_copper_loss, sec_copper_loss, choke_core_loss, choke_copper_loss, res_dissip))
        Dissipation_matrix                                           = dp.np.concatenate((dissip, res_dissip))
        return Dissipation_matrix

    def therm_stats(self,MAT_list,thread,P_aux):
        """
        Calculate thermal statistics including efficiency, total dissipation, and input power.

        Parameters:
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

        Parameters:
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

        Parameters:
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

        Parameters:
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

        Parameters:
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

        Parameters:
            time (numpy.ndarray)    : Time values of the original signal.
            signal (numpy.ndarray)  : Signal values.

        Returns:
            tuple: Tuple containing the resampled time values and the corresponding resampled signal values.

        """
        new_t       = dp.np.linspace(time.min(), time.max(), len(signal))
        new_signal  = dp.np.interp(new_t,time,signal)
        return new_t,new_signal

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
        try:
            return my_list[index]
        except IndexError:
            return None

    def FFT_mat(self, T_vec, nestedresults):
        """
        Compute the Fast Fourier Transform (FFT) matrix of nested results.

        Parameters:
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

    def hierarchicalSims(self,Map):
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
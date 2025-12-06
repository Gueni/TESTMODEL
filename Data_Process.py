
 in WCA case   
 {
  "X1": "[[10, 0.1, 5, 15], [20, 0.2, 15, 25]]",
  "X2": "[[100, 0.5, 50, 150]]",
  "X3": "[[5, 0.2, 3, 7], [15, 0.3, 10, 20], [25, 0.4, 20, 30]]",
  "X4": "[[50, 0.1, 40, 60]]",
  "X5": "[[1, 0.5, 0.5, 2], [2, 0.5, 1, 3]]",
  "X6": "[[8, 0.25, 6, 10]]",
  "X7": "[[0]]",
  "X8": "[[0]]",
  "X9": "[[0]]",
  "X10": "[[0]]",

  "startPoint": "[[10, 0.1, 5, 15], [100, 0.5, 50, 150], [5, 0.2, 3, 7], [50, 0.1, 40, 60], [1, 0.5, 0.5, 2], [8, 0.25, 6, 10], [0], [0], [0], [0]]"
}



# Shape: (total_iterations, num_variables, 3)
Map = [
    # Iteration 0
    [
        [x1calculatedwcavalue ,x12calculatedwcavalue...],  # X1
        [x2calculatedwcavalue ,x22calculatedwcavalue...],  # X2
        [x3calculatedwcavalue ,x32calculatedwcavalue...],  # X3

        ...  # up to X10
    ],
    
 
    
    # ... more iterations
    
    # Last iteration (nominal)
    [
        [x1_nominal, x1_min, x1_max],  # X1 (nominal value)
        [x2_nominal, x2_min, x2_max],  # X2
        [x3_nominal, x3_min, x3_max],  # X3
        ...
    ]
]
    def binary_index(self, iteration, index):
      
        bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
        return bin_idx
    
    def WCA(self, iteration, Xs):
      
        results = []
        for i, var_data in enumerate(Xs):
            if var_data == [[0]]:
                results.append([0])  # WCA unused variables become [0, 0, 0]
                continue
                
            wca_values = []
            for j, (nom, tol, min_val, max_val) in enumerate(var_data):
                if tol <= 1:
                    # Absolute tolerance
                    x = self.funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
                else:
                    # Relative tolerance
                    x = self.funtol(Abs_rel=False, iteration=iteration, index=i, nom=nom, tol=tol)
                
                wca_value = min(max(x,min_val),max_val)
                
                wca_values.append(wca_value)
            
            results.append(wca_values)
            
        return results
    
    def funtol(self, Abs_rel, iteration, index, nom, tol):
      
        if Abs_rel:
            if self.binary_index(iteration, index):
                return nom * tol
            else:
                return nom / tol
        else:
            if self.binary_index(iteration, index):
                return nom * (1 + tol)
            else:
                return nom * (1 - tol)
 

in normal case 
# # Shape: (total_iterations, num_variables)
# Map = [
#     [x1_value, x2_value, x3_value, ..., x10_value],  # Iteration 0
#     [x1_value, x2_value, x3_value, ..., x10_value],  # Iteration 1
#     ...  # more iterations
# ]


how it is :
{

  "X1"            :  "[0]",
  "X2"            :  "[35,75]",
  "X3"            :  "[200,300]",
  "X4"            :  "[10.5,11.5]",
  "X5"            :  "[500]",
  "X6"            :  "[0]",
  "X7"            :  "[0]",
  "X8"            :  "[0]",
  "X9"            :  "[0]",
  "X10"           :  "[0]",
  "sweepNames"    :   ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10"],
  "startPoint"    :   "[0,35,200,10.5,500,0,0,0,0,0]",
  "maxThreads"    :   4,
  "parallel"      :   true,
  "permute"       :   true,

}

how it will be :
  
  in case of WCA [permute false]
{

  "X1"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]", # [[value , tol ]]
  "X2"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X3"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X4"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X5"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X6"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X7"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X8"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X9"            :  "[[2.5 , 0.6], [2.5 , 0.6],[2.5 , 0.6],[2.5 , 0.6]]",
  "X10"           :  "[[0]]",
  "sweepNames"    :   ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10"],
  "startPoint"    :   "[0,35,200,10.5,500,0,0,0,0,0]",
  "maxThreads"    :   4,
  "parallel"      :   true,
  "permute"       :   true,

}  

in case normal [permute true]
{

  "X1"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X2"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X3"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X4"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X5"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X6"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X7"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X8"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X9"            :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "X10"           :  "[[1.0], [1.0],[1.0],[1.0]]", # [[value ]]
  "sweepNames"    :   ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10"],
  "startPoint"    :   "[0,35,200,10.5,500,0,0,0,0,0]",
  "maxThreads"    :   4,
  "parallel"      :   true,
  "permute"       :   true,

}  



{

  "X1"            :  "[0]",
  "X2"            :  "[35,75]",
  "X3"            :  "[200,300]",
  "X4"            :  "[10.5,11.5]",
  "X5"            :  "[500]",
  "X6"            :  "[0]",
  "X7"            :  "[0]",
  "X8"            :  "[0]",
  "X9"            :  "[0]",
  "X10"           :  "[0]",
  "sweepNames"    :   ["X1","X2","X3","X4","X5","X6","X7","X8","X9","X10"],
  "startPoint"    :   "[0,35,200,10.5,500,0,0,0,0,0]",
  "maxThreads"    :   4,
  "parallel"      :   true,
  "permute"       :   true,

}

in normal case 
# # Shape: (total_iterations, num_variables)
# Map = [
#     [x1_value, x2_value, x3_value, ..., x10_value],  # Iteration 0
#     [x1_value, x2_value, x3_value, ..., x10_value],  # Iteration 1
#     ...  # more iterations
# ]

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class Processing:
    def __init__(self):
        pass

   

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
    
    def init_sim(self,maxThreads=1,startPoint=[0,0,0,0,0,0,0,0,0,0],X1=[0],X2=[0],X3=[0],X4=[0],X5=[0],X6=[0],X7=[0],X8=[0],X9=[0],X10=[0],pattern=True,model='DCDC'):
        """
        Initialize a simulation.

        Parameters
        ----------
        maxThreads : int, optional
            Maximum number of threads to use for parallel simulations, default is 1.
        startPoint : list of 10 floats, optional
            Starting point of the parameter sweep, default is [0,0,0,0,0,0,0,0,0,0].
        X1, X2, X3, X4, X5, X6, X7, X8, X9, X10 : list of floats, optional
            Lists of parameter values to sweep over. Each list must have at least one value.
        pattern : bool, optional
            If True, perform a patterned sweep, otherwise perform a full sweep, default is True.
        model : str, optional
            The type of model to use, either 'DCDC' or 'OBC', default is 'DCDC'.

        Returns
        -------
        None
        """
        # define starting point of sweep
        self.sweepMatrix         =   [X1,X2,X3,X4,X5,X6,X7,X8,X9,X10]
        self.startPoint          =   startPoint

        # define order of sweep
        self.idx ,itrr           =   self.postProcessing.findIndex(self.startPoint,self.sweepMatrix,pattern)
        self.matrix              =   self.postProcessing.findStart(self.sweepMatrix,self.idx,pattern)
        self.Map,self.Iterations =   self.postProcessing.findPoint(self.matrix,self.idx,pattern)
        self.iterNumber          =   0
  

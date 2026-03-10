

def init_sim(self, maxThreads=1, X1=[[0]], X2=[[0]], X3=[[0]], X4=[[0]], X5=[[0]], X6=[[0]], X7=[[0]], X8=[[0]], X9=[[0]], X10=[[0]], model='DCDC', pattern=True):
    """
    Initialize simulation with parameter sweeps.
    Starting points are always the first element or first sublist of each X list.
    """

    # Store all parameters
    self.sweepMatrix = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]
    self.maxThreads, self.model = maxThreads, model

    # Detect mode
    self.mode = self.detect_mode(self.sweepMatrix)

    if self.mode == "WCA":
        # Reduced matrix: first sublist of each parameter
        self.startPoint = self.calculate_wca_values(0, [[var[0]] for var in self.sweepMatrix])

        # Always use first iteration (first sublist of each parameter)
        self.idx, self.itrr = self.findIndex(self.startPoint, self.sweepMatrix, pattern=True)

        # Build full WCA map
        active = self.get_active_wca_params(self.sweepMatrix)
        self.Iterations = 2 ** len(active) + 1  # total WCA iterations
        self.Map = [self.calculate_wca_values(i, self.sweepMatrix) for i in range(self.Iterations)]
        self.Map = self.Map[self.itrr:]  # start from first sublist
        self.Map2D = [sum((list(p) if isinstance(p, list) else [p] for p in row), []) for row in self.Map]

    else:
        # Normal mode: first element of each list
        self.startPoint = [ var[0] for var in self.sweepMatrix]
        self.idx, self.itrr = self.findIndex(self.startPoint, self.sweepMatrix, pattern)
        self.matrix = self.findStart(self.sweepMatrix, self.idx, pattern)
        self.Map2D, self.Iterations = self.findPoint(self.matrix, self.idx, pattern)
        self.Map = self.Map2D

    # iteration counter and matrices initialization remain the same
    self.iterNumber = 0
    [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations, dp.Y_Length[i]))) for i in list(range(1, 7)) + list(range(9, 14))]
    [setattr(self, f"MAT{i}", dp.np.zeros((self.Iterations * len(dp.harmonics), dp.Y_Length[i]))) for i in range(7, 9)]

    # Threads and hierarchical simulations
    if dp.JSON['hierarchical']:
        self.threads_vector = self.postProcessing.hierarchicalSims(self.Map)
        self.Simulations = len(self.threads_vector)
    else:
        maxThreads = self.simThreads(maxThreads)
        self.Threads = self.paralellThreads(maxThreads, self.Iterations)
        self.Simulations = self.Iterations // self.Threads

    self.MAT_list = [getattr(self, f"MAT{i}") for i in range(1, 14)]

    # Set mapping parameters based on model type
    if model == 'DCDC':
        self.mode = dp.pmap.Maps_index['DCDC_data_mat'][0]
        self.map_index = dp.pmap.Maps_index['DCDC_data_mat'][1]
        self.map_names = dp.pmap.Maps_index['DCDC_map_names']
    elif model == 'OBC':
        self.mode = dp.pmap.Maps_index['OBC_data_mat'][0]
        self.map_index = dp.pmap.Maps_index['OBC_data_mat'][1]
        self.map_names = dp.pmap.Maps_index['OBC_map_names']
    else:
        raise NameError(model)

    return self
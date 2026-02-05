#!========================================================
import os, natsort
csv_maps_dir        = dp.os.path.join(fileLog.resultfolder, "CSV_MAPS")
standalone_files    = [f for f in natsort.natsorted(os.listdir(csv_maps_dir)) if f.startswith('Standalone') and f.endswith('_MAP.csv')]
standalone_exist    = len(standalone_files) == 5  # RMS, AVG, MAX, MIN, FFT

if standalone_exist:
    # Load headers from time series standalone files
    csv_time_series_dir     = dp.os.path.join(fileLog.resultfolder, "CSV_TIME_SERIES")
    time_series_files       = natsort.natsorted(glob.glob(csv_time_series_dir + "/*Standalone*.csv"))
    
    if time_series_files:
        df              = dp.pd.read_csv(time_series_files[0])
        headers_list    = df.columns[1:].tolist()  # Skip first column (Time)
    
    mat_names           = ["Standalone_RMS","Standalone_AVG","Standalone_MAX","Standalone_MIN","Standalone_FFT"]
    FFT_headers         = headers_list  # Assuming same headers for FFT
    headers_array       = headers_list 
    
    # Load matrices from standalone MAP files
    standalone_matrices = {}
    for file_type, file_name in zip(['RMS', 'AVG', 'MAX', 'MIN', 'FFT'], mat_names):
        file_path = dp.os.path.join(csv_maps_dir, file_name + '_MAP.csv')
        if dp.os.path.exists(file_path):
            df = dp.pd.read_csv(file_path, header=None)
            # Skip header row if present
            if df.shape[0] > 0 and any(isinstance(val, str) for val in df.iloc[0]):
                df = df.iloc[1:]
            standalone_matrices[file_type] = df.values.astype(float)
    
    # Combine non-FFT matrices
    combined_matrix = None
    for file_type in ['RMS', 'AVG', 'MAX', 'MIN']:
        if file_type in standalone_matrices:
            if combined_matrix is None:
                combined_matrix = standalone_matrices[file_type]
            else:
                combined_matrix = dp.np.hstack((combined_matrix, standalone_matrices[file_type]))
    
    # FFT matrix
    combined_fft_matrix = standalone_matrices.get('FFT')
    
else:
    #!========================================================
    # Define matrix and header name same order as in Y_length and get the headers lists accordingly.
    mat_names           = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage","Dissipations","Elec_Stats","Temps","Thermal_Stats"]
    headers_lists       = [data if isinstance((data := dp.json.load(open(dp.os.path.join(header_path, f"{name}.json")))), list) else [data] for name in mat_names]

    # Define sum cumulative increment and slice to get signals and fft headers lists.
    cumsum              = dp.np.cumsum(dp.Y_Length[1:]).tolist()
    all_headers         = sum(headers_lists, [])
    fft_start, fft_end  = cumsum[5], cumsum[7]
    FFT_headers         = all_headers[fft_start:fft_end]
    headers_array       = all_headers[:fft_start] + all_headers[fft_end:]

    # Combined matrix for signals and ffts
    combined_matrix     = dp.np.hstack((simutil.MAT_list[:6] + simutil.MAT_list[8:12]))
    combined_fft_matrix = dp.np.hstack((simutil.MAT_list[6:8]))
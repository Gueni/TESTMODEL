else:
    #!========================================================
    # Define matrix and header name same order as in Y_length and get the headers lists accordingly.
    mat_names       = ["Peak_Currents","RMS_Currents","AVG_Currents","Peak_Voltages","RMS_Voltages","AVG_Voltages","FFT_Current","FFT_Voltage","Dissipations","Elec_Stats","Temps","Thermal_Stats"]
    headers_lists   = [data if isinstance((data := dp.json.load(open(dp.os.path.join(header_path, f"{name}.json")))), list) else [data] for name in mat_names]

    # Define sum cumulative increment and slice to get signals and fft headers lists.
    cumsum              = dp.np.cumsum(dp.Y_Length[1:]).tolist()
    all_headers         = sum(headers_lists, [])
    fft_start, fft_end  = cumsum[5], cumsum[7]
    FFT_headers         = all_headers[fft_start:fft_end]
    headers_array       = all_headers[:fft_start] + all_headers[fft_end:]

    # Combined matrix for signals and ffts (always built from base)
    combined_matrix     = dp.np.hstack((simutil.MAT_list[:6] + simutil.MAT_list[8:12]))
    combined_fft_matrix = dp.np.hstack((simutil.MAT_list[6:8]))

    # ── Sensitivity: load, generate headers, and append ─────────────────────
    if (not dp.JSON["perturbation"] == 0) and (dp.JSON["nvars"] == None):

        sens_mat_names      = [f"{n}_Sens" for n in mat_names]
        sens_headers_lists  = [[f"{h}_Sens" for h in hlist] for hlist in headers_lists]

        # Load sens matrices from CSV_MAPS
        sens_MAT_list = []
        for name in sens_mat_names:
            file_path = dp.os.path.join(csv_maps_dir, name + '_Map.csv')
            df        = dp.pd.read_csv(file_path, header=None)
            sens_MAT_list.append(df.values.astype(float))

        # Build sens combined matrices using same slice logic
        combined_sens_matrix     = dp.np.hstack(sens_MAT_list[:6] + sens_MAT_list[8:12])
        combined_fft_sens_matrix = dp.np.hstack(sens_MAT_list[6:8])

        # Build sens header arrays using same fft_start/fft_end slicing
        sens_all_headers = sum(sens_headers_lists, [])
        FFT_headers_sens    = sens_all_headers[fft_start:fft_end]
        headers_array_sens  = sens_all_headers[:fft_start] + sens_all_headers[fft_end:]

        # Append sens to base — columns grow rightward, headers extend accordingly
        combined_matrix     = dp.np.hstack((combined_matrix,     combined_sens_matrix))
        combined_fft_matrix = dp.np.hstack((combined_fft_matrix, combined_fft_sens_matrix))
        headers_array       = headers_array  + headers_array_sens
        FFT_headers         = FFT_headers    + FFT_headers_sens

        # Extend mat_names and headers_lists so category grouping covers sens too
        mat_names       = mat_names     + sens_mat_names
        headers_lists   = headers_lists + sens_headers_lists
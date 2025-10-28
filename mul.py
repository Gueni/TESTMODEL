def auto_plot(self, simutil, fileLog, misc, open=False, iterReport=False):
    """
    Generates an HTML report containing multiple plots using multiprocessing.
    """
    misc.tic()
    ResDir = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_TIME_SERIES"
    MAPS_dir = (dp.os.getcwd()).replace("\\","/") + "/Script/" + "D".upper() + "ata/Res/"+self.script_name+ "_"+self.utc+dp.suffix +"/CSV_MAPS"
    FFT_curr_path = MAPS_dir+"/FFT_Current_Map.csv"
    FFT_volt_path = MAPS_dir+"/FFT_Voltage_Map.csv"
    
    file_list = fileLog.natsort_files(ResDir)
    legend = True if dp.JSON['TF_Config'] == 'DCDC_D' else False
    
    if dp.JSON['TF_Config'] in ['DCDC_S', 'DCDC_D']:
        simutil.postProcessing.drop_Extra_Cols(FFT_curr_path, dp.idx_start, dp.idx_end)

    if iterReport:
        self.gen_iter_report(ResDir, dp.pmap_multi['Peak_Currents'], fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc, "[ A ]", "Currents", open)
        self.gen_iter_report(ResDir, dp.pmap_multi['Peak_Voltages'], fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc, "[ V ]", "Voltages", open)
    
    if iterReport and dp.JSON['FFT']:
        self.fft_gen_iter_report("FFT_Current.json", " Currents_FFT", FFT_curr_path, fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc, "Currents_FFT", open)
        self.fft_gen_iter_report("FFT_Voltage.json", "Voltages_FFT", FFT_volt_path, fileLog.resultfolder + "/HTML_REPORTS/" + "HTML_Report_" + self.utc, "Voltages_FFT", open)

    # Prepare data for multiprocessing
    processing_data = []
    for x in range(len(file_list)):
        processing_data.append({
            'file_path': file_list[x],
            'index': x,
            'FFT_curr_path': FFT_curr_path,
            'FFT_volt_path': FFT_volt_path,
            'legend': legend,
            'result_folder': fileLog.resultfolder,
            'utc': self.utc,
            'open_flag': open
        })

    # Process files in parallel
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(self.process_single_file, processing_data)

    fileLog.log("--------------------------------------------------------------------------------------------------------------------------")
    fileLog.log(f"Generating HTML Report    {'= '.rjust(49+17, ' ')}{str(misc.toc())} seconds.\n")

def process_single_file(self, data):
    """
    Process a single file for HTML generation (to be used with multiprocessing)
    """
    file_path = data['file_path']
    index = data['index']
    FFT_curr_path = data['FFT_curr_path']
    FFT_volt_path = data['FFT_volt_path']
    legend = data['legend']
    result_folder = data['result_folder']
    utc = data['utc']
    open_flag = data['open_flag']
    
    try:
        # Generate FFT figures
        FFT_figs = self.fft_bar_plot(FFT_curr_path, FFT_volt_path, index)
        
        # Generate main figures
        figures_list = self.plot_scopes(file_path, dp.pmap_plt, Legend=legend)
        figures_list_ = self.shuffle_lists(figures_list, FFT_figs)
        
        if dp.JSON['TF_Config'] in ['DCDC_S', 'DCDC_D']:
            # Drop extra columns if needed
            # simutil.postProcessing.drop_Extra_Cols(file_path, sum(dp.Y_list[0:3]), sum(dp.Y_list[0:4]))
            figures_list_ctrl = self.plot_scopes(file_path, dp.pmap_plt_ctrl, Legend=True)
            figures_list_.extend(figures_list_ctrl)
        
        # Generate HTML file
        output_path = f"{result_folder}/HTML_REPORTS/HTML_REPORT_{utc}_{index + 1}.html"
        self.append_to_html(file_path, figures_list_, output_path, auto_open=open_flag, i=index)
        
        # Clear temporary data
        self.constants_list.clear()
        self.constants_vals.clear()
        self.constants_units.clear()
        figures_list_.clear()
        
        return f"Successfully processed {file_path}"
        
    except Exception as e:
        return f"Error processing {file_path}: {str(e)}"
    










    from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing

def auto_plot_threaded(self, simutil, fileLog, misc, open=False, iterReport=False):
    """
    Threaded version - often better for I/O-bound tasks like file writing
    """
    # ... (same setup code as above)
    
    # Prepare data for threading
    processing_data = []
    for x in range(len(file_list)):
        processing_data.append({
            'file_path': file_list[x],
            'index': x,
            # ... other parameters
        })

    # Use ThreadPoolExecutor (often better for I/O operations)
    max_workers = min(multiprocessing.cpu_count(), len(file_list))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(self.process_single_file, data): data['file_path'] 
            for data in processing_data
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f'{file_path} generated an exception: {exc}')





Key Points:
multiprocessing.Pool - Uses separate processes (good for CPU-bound tasks)

ThreadPoolExecutor - Uses threads (good for I/O-bound tasks like file writing)

Process isolation - Each worker gets its own memory space

Error handling - Important when running in parallel

Resource limits - Don't use more workers than available CPU cores
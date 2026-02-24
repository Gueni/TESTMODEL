import numpy as np
import pandas as pd
from lmfit import Model, Parameters
from lmfit.minimizer import Minimizer
import concurrent.futures
import multiprocessing
import psutil
import time
from pathlib import Path
from functools import partial
import warnings
import glob
import os
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

class UltraFastRLCFitter:

    def __init__(self, parallel_level='both', max_workers=None):
        """
        parallel_level: 'files' (default), 'single_fit', 'global', or 'both'
        """
        self.parallel_level = parallel_level
        self.max_workers = max_workers or max(1, psutil.cpu_count(logical=True) - 1)
        print(f"🔥 Using {self.max_workers} CPU cores")
        print(f"📊 Parallelization mode: {parallel_level}")
        
    def circuit_impedance(self, f, R1, L1, R2, L2, C2, C3):
        """Calculate total impedance of the circuit"""
        w = 2 * np.pi * np.array(f)
        
        # Branch 1: R1 + L1 (series)
        Z1 = R1 + 1j * w * L1
        
        # Branch 2: Parallel RL
        Z_R2 = R2
        Z_L2 = 1j * w * L2
        Z_RL = 1 / (1/Z_R2 + 1/Z_L2)
        
        # Branch 3: Parallel RC (using same R2)
        Z_R2_2 = R2
        Z_C2 = 1 / (1j * w * C2)
        Z_RC = 1 / (1/Z_R2_2 + 1/Z_C2)
        
        # Parallel combination of RL and RC
        Z_parallel = 1 / (1/Z_RL + 1/Z_RC)
        
        # Total impedance before C3
        Z_mid = Z1 + Z_parallel
        
        # Add C3 to ground
        Z_C3 = 1 / (1j * w * C3)
        Z_total = 1 / (1/Z_mid + 1/Z_C3)
        
        return Z_total
    
    def impedance_magnitude(self, f, R1, L1, R2, L2, C2, C3):
        """Return magnitude of impedance for fitting"""
        Z = self.circuit_impedance(f, R1, L1, R2, L2, C2, C3)
        return np.abs(Z)
    
    def fit_single_file_parallel(self, file_path, fit_type='magnitude'):
        """
        Fit a single file WITH PARALLEL COMPUTATION inside the fit
        """
        start_time = time.time()
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # FIXED: Use raw string with r prefix
            data = pd.read_csv(
                file_path, 
                comment='#',           
                sep=r'\s+',              # Raw string regex for whitespace
                header=None,           
                names=['freq', 'mag', 'phase'],  
                nrows=5000,             
                engine='python'          # Use python engine for regex separator
            )
            
            # Check if we have data
            if len(data) == 0:
                raise ValueError(f"No data found in {file_path}")
            
            # Downsample if too many points
            if len(data) > 1000:
                data = data.iloc[::5, :].reset_index(drop=True)
            
            freq = data['freq'].values
            measured = data['mag'].values
            
            # Smart initial guess
            low_f_idx = int(len(freq) * 0.1)
            R1_guess = measured[low_f_idx] if low_f_idx < len(measured) else 50
            
            # Setup parameters
            params = Parameters()
            params.add('R1', value=R1_guess, min=0.1, max=1e4)
            params.add('L1', value=1e-6, min=1e-9, max=1e-3)
            params.add('R2', value=100, min=1, max=1e5)
            params.add('L2', value=1e-6, min=1e-9, max=1e-3)
            params.add('C2', value=1e-9, min=1e-12, max=1e-6)
            params.add('C3', value=1e-9, min=1e-12, max=1e-6)
            
            # Use lmfit
            model = Model(self.impedance_magnitude)
            
            # Fit with bounds
            result = model.fit(
                measured, 
                params, 
                f=freq, 
                method='leastsq', 
                max_nfev=200,
                nan_policy='omit'
            )
            
            fit_time = time.time() - start_time
            
            return {
                'file': Path(file_path).name,
                'success': True,
                'R1': result.params['R1'].value,
                'L1': result.params['L1'].value,
                'R2': result.params['R2'].value,
                'L2': result.params['L2'].value,
                'C2': result.params['C2'].value,
                'C3': result.params['C3'].value,
                'chi2': result.chisqr,
                'time': fit_time,
                'method': self.parallel_level
            }
            
        except Exception as e:
            fit_time = time.time() - start_time
            return {
                'file': Path(file_path).name,
                'success': False,
                'error': str(e),
                'time': fit_time
            }
    
    def fit_multiple_files(self, file_paths, fit_type='magnitude'):
        """
        Fit multiple files - Level 1: Parallel across files
        """
        results = []
        
        # Filter out non-existent files
        valid_files = [f for f in file_paths if os.path.exists(f)]
        if len(valid_files) < len(file_paths):
            print(f"⚠️ Warning: {len(file_paths) - len(valid_files)} files not found")
        
        if not valid_files:
            print("❌ No valid files to process")
            return results
        
        # Use process pool for file-level parallelism
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_file = {
                executor.submit(self.fit_single_file_parallel, f, fit_type): f 
                for f in valid_files
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                results.append(result)
                
                # Print progress
                status = "✅" if result['success'] else "❌"
                error_info = f" - {result['error']}" if not result['success'] and 'error' in result else ""
                print(f"{status} {result['file']}: {result['time']:.2f}s{error_info}")
        
        return results
    
    def save_results(self, results, output_file='fitted_parameters.csv'):
        """Save fitting results to CSV"""
        successful = [r for r in results if r['success']]
        
        if successful:
            df = pd.DataFrame(successful)
            # Remove non-serializable columns
            df = df.drop(columns=[col for col in ['result'] if col in df.columns], errors='ignore')
            df.to_csv(output_file, index=False)
            print(f"\n💾 Saved {len(successful)} successful fits to {output_file}")
            
            # Print statistics
            times = [r['time'] for r in successful]
            print(f"📊 Fit times - Avg: {np.mean(times):.2f}s, "
                  f"Min: {np.min(times):.2f}s, Max: {np.max(times):.2f}s")
        else:
            print("\n⚠️ No successful fits to save")

    def plot_fit_result(self, fitter, file_path, result):
        """Plot measured data vs fitted curve"""
        # Load data
        data = pd.read_csv(file_path, comment='#', sep=r'\s+', 
                        names=['freq', 'mag', 'phase'], engine='python')
        
        freq = data['freq'].values
        measured = data['mag'].values
        
        # Generate fitted curve
        fitted = fitter.impedance_magnitude(
            freq, 
            result['R1'], result['L1'], 
            result['R2'], result['L2'], 
            result['C2'], result['C3']
        )
        
        # Plot
        plt.figure(figsize=(10, 6))
        plt.loglog(freq, measured, 'b.', label='Measured', alpha=0.5)
        plt.loglog(freq, fitted, 'r-', label='Fitted', linewidth=2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Impedance Magnitude (Ω)')
        plt.title(f"Fit for {Path(file_path).name}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    your_data_folder = r"D:/WORKSPACE/TESTMODEL/"
    
    import glob
    your_files = glob.glob(your_data_folder + "*.txt")
    
    if not your_files:
        print(f"No files found in {your_data_folder}")
    else:
        print(f"Found {len(your_files)} files to process")
        
        # Create fitter
        fitter = UltraFastRLCFitter(parallel_level='both', max_workers=8)
        
        start = time.time()
        results = fitter.fit_multiple_files(your_files)
        total_time = time.time() - start
        
        print(f"\n🎯 Processed {len(your_files)} files in {total_time:.2f}s")
        print(f"📈 Average per file: {total_time/len(your_files):.2f}s")
        
        # Save your results
        fitter.save_results(results, 'my_component_values.csv')
        fitter.plot_fit_result(fitter, your_files[0], results[0])






























def iter_report_standalone(self, csv_files, html_path, auto_open):
        """
        Generates an iteration report in HTML format for a set of standalone CSV files located in a given directory.

        Parameters:     csv_files (list)    list of the CSV standalone files.
                        html_path (string)  The path where the HTML file should be saved.
                        auto_open (bool)    If True, opens the generated HTML report in a new browser window automatically.
        """
        plot_items        =   ''
        html_content      =   self.prep_html_template(Time_series = False)
        fig_list = []
        include_plotlyjs = 'cdn'

        if len(csv_files) >= 1:
            dfs = [dp.pd.read_csv(f) for f in csv_files]              # Read each csv into a Pandas dataframe

            # Get all column names from the first CSV (assuming all CSVs have same structure)
            if dfs:
                all_columns = dfs[0].columns.tolist()
                # Skip the first column (assuming it's time/x-axis)
                plot_columns = all_columns[1:] if len(all_columns) > 1 else all_columns
                plot_columns = [dp.re.sub(r'[^a-zA-Z0-9]', '_', each) for each in plot_columns] # for names

                for each in plot_columns:
                    fig = dp.make_subplots()
                    C = 1
                    for df in dfs:
                        df.columns   = [dp.re.sub(r'[^a-zA-Z0-9]', '_', col) for col in df.columns] # for signal names
                        signal_units = [dp.unit_map[dp.pattern.search(" ".join(s.split()[-2:])).group().lower()] if dp.pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in df.columns.values]
                        fig.add_trace(dp.go.Scatter(x = df.iloc[:, 0],y = df[each],name = str("Iter :" + str(C) + " | ") + each,mode = "lines",line = dict(shape='linear')))
                        # Find which column index 'each' corresponds to in the current dataframe
                        col_idx = df.columns.get_loc(each) if each in df.columns else 1
                        fig.update_layout(showlegend = True,title = each, xaxis = dict(title='Time [S]'),yaxis = dict(side = "left",title = signal_units[col_idx], titlefont = dict(color="#1f77b4"),tickfont = dict(color="#1f77b4")),plot_bgcolor = '#f8fafd')
                        C += 1
                    fig_list.append(fig)
                        # If 'iterSplit' is enabled in the JSON settings, a separate HTML report is generated for each key.
                    if dp.JSON['iterSplit']:

                        plot_items      +=  fig.to_html(full_html=False, include_plotlyjs=include_plotlyjs)
                        html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                        with open(html_path + "_Standalone_" + each + ".html", 'w', encoding='utf-8') as file: file.write(html_content)
                        file.close()

                # If 'iterSplit' is disabled in the JSON settings, a single consolidated HTML report is generated.
                if not dp.JSON['iterSplit']:
                    for fig_i in fig_list:
                        plot_items      +=  fig_i.to_html(full_html=False, include_plotlyjs=include_plotlyjs)

                    # Replace plot items
                    html_content = html_content.replace("{{PLOT_ITEMS}}", plot_items)
                    # Write the populated HTML
                    with open(html_path + "_Standalone_Iterations.html", 'w', encoding='utf-8') as file: file.write(html_content)
                    file.close()

                # If auto_open is enabled, the generated HTML report is automatically opened in the default web browser.
                if auto_open: dp.webbrowser.open(dp.pathlib.Path(html_path).absolute().as_uri())
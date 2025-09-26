
#?-------------------------------------------------------------------------------------------------------------------------------
#?  Import Libraries
#?-------------------------------------------------------------------------------------------------------------------------------
import os, json
from natsort import natsorted
import pandas as pd, numpy as np

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Header Files to JSON Array
#?-------------------------------------------------------------------------------------------------------------------------------
# Combine all JSON files in a directory into a single array, excluding specific files
# Excluded files: 'header.json', 'FFT_Current.json', 'FFT_Voltage.json'
# j_array will contain the combined data

f_path      = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
all_files   = os.listdir(f_path)
j_files     = natsorted([f for f in all_files if f not in {'header.json', 'FFT_Current.json', 'FFT_Voltage.json','Peak_Losses.json'}])
j_array     = []
[j_array.extend(data) if isinstance((data := json.load(open(os.path.join(f_path, f)))), list) else j_array.append(data) for f in j_files]

# print(f"Processed {len(j_files)} files")
# print(f"Combined array length: {len(j_array)}")
# print("Array contents:", j_array)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Combine CSV Files into a Single Matrix
#?-------------------------------------------------------------------------------------------------------------------------------

# Define the folder containing CSV files and combine them into a single CSV file
folder      = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"

# Load and combine CSV files, excluding specific ones
# Excluded files: 'FFT_Voltage_Map.csv', 'FFT_Current_Map.csv'
# The combined_matrix will contain the horizontally stacked data from the CSV files
combined_matrix = np.hstack([pd.read_csv(os.path.join(folder, f), header=None).values 
                           for f in sorted(os.listdir(folder)) 
                           if f.endswith('.csv') and f not in ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']])

# print(f"Combined matrix shape: {combined_matrix.shape}")
print("Combined matrix contents:", combined_matrix)

#?-------------------------------------------------------------------------------------------------------------------------------
#?  
#?-------------------------------------------------------------------------------------------------------------------------------


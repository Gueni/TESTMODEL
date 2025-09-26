

import os, json
from natsort import natsorted


#?-------------------------------------------------------------------------------------------------------------------------------
#?  Header Files to JSON Array
#?-------------------------------------------------------------------------------------------------------------------------------
# Combine all JSON files in a directory into a single array, excluding specific files
# Excluded files: 'header.json', 'FFT_Current.json', 'FFT_Voltage.json'
# j_array will contain the combined data

f_path     = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
all_files  = os.listdir(f_path)
j_files    = natsorted([f for f in all_files if f not in {'header.json', 'FFT_Current.json', 'FFT_Voltage.json'}])
j_array    = []
[j_array.extend(data) if isinstance((data := json.load(open(os.path.join(f_path, f)))), list) else j_array.append(data) for f in j_files]

# print(f"Processed {len(j_files)} files")
# print(f"Combined array length: {len(j_array)}")
# print("Array contents:", j_array)
#?-------------------------------------------------------------------------------------------------------------------------------
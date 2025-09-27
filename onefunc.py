#?-------------------------------------------------------------------------------------------------------------------------------
#?  Import Libraries
#?-------------------------------------------------------------------------------------------------------------------------------
import os, json
from natsort import natsorted
import pandas as pd, numpy as np
from itertools import product
import re
import plotly.graph_objects as go
import datetime
from plotly.io import to_html

#?-------------------------------------------------------------------------------------------------------------------------------
#?  Main Function
#?-------------------------------------------------------------------------------------------------------------------------------
def generate_bjt_report(header_path: str,
                        folder: str,
                        input_json: str,
                        base64_file: str,
                        html_base: str,
                        harmonics=[1,2],
                        F_fund=1e5,
                        split_3D=True):

    # Load input config
    with open(input_json) as f:
        config = json.load(f)
    var1, var2 = config["Var1"], config["Var2"]

    # Load base64 logo
    with open(base64_file, 'r') as f:
        base64_img = ''.join(line.strip() for line in f)

    # Timestamp and date
    UTC = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    date = str(datetime.datetime.now().replace(microsecond=0))
    
    # Load header files
    all_header_files = os.listdir(header_path)
    excluded_headers = {'header.json', 'Peak_Losses.json'}
    headers_files = natsorted([f for f in all_header_files if f not in excluded_headers])
    headers_lists = [data if isinstance((data := json.load(open(os.path.join(header_path, f)))), list) else [data] for f in headers_files]
    FFT_headers = sum(headers_lists[5:7], [])
    headers_array = sum(headers_lists[:5] + headers_lists[7:], [])

    # Combine CSV files
    excluded = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
    combined_matrix = np.hstack(
        [pd.read_csv(os.path.join(folder, f), header=None).values
         for f in sorted(os.listdir(folder))
         if f.endswith('.csv') and f not in excluded]
    )
    combined_fft_matrix = np.hstack(
        [pd.read_csv(os.path.join(folder, f), header=None).values
         for f in natsorted([f for f in os.listdir(folder)
                             if f.endswith('.csv') and f in excluded])]
    )

    # Sweep variables
    sweep_vars = {k: eval(v) for k, v in config.items() if re.fullmatch(r"X\d+", k) and eval(v) != [0]}
    all_combos = list(product(*sweep_vars.values()))
    fft_combos = list(map(tuple, np.repeat(all_combos, len(harmonics), axis=0).astype(object)))

    # Fixed variables
    sweep_keys = list(sweep_vars.keys())
    other_vars = {k: eval(v) for k, v in config.items()
                  if re.fullmatch(r"X\d+", k)
                  and k not in [var1, var2]
                  and eval(v) != [0]
                  and not config["sweepNames"][int(re.search(r'\d+', k).group())-1].startswith("X")}
    fixed_combos = list(product(*other_vars.values()))
    fixed_keys = list(other_vars.keys())

    rows_list = []
    fft_rows_list = []
    for fixed_values in fixed_combos:
        fixed = dict(zip(fixed_keys, fixed_values))
        try:
            rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(all_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
            ])
            fft_rows = np.array([
                (i, combo[sweep_keys.index(var1)], combo[sweep_keys.index(var2)])
                for i, combo in enumerate(fft_combos)
                if all(combo[sweep_keys.index(k)] == v for k, v in fixed.items())
            ])
            rows_list.append(rows)
            fft_rows_list.append(fft_rows)
        except:
            print("No matching rows found for fixed combination:", fixed)
            rows_list.append(np.array([]))
            fft_rows_list.append(np.array([]))

    # 3D Surface plotting
    list_of_plots = []
    for component, fixed_values, rows in product(headers_array, fixed_combos, rows_list):
        if len(rows) == 0: continue
        fixed = dict(zip(fixed_keys, fixed_values))
        z_column = headers_array.index(component)
        x_vals = rows[:, 1]
        y_vals = rows[:, 2]
        z_vals = combined_matrix[rows[:, 0].astype(int), z_column]
        fixed_title = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k, v in fixed.items())
        x_unique, y_unique = np.unique(x_vals), np.unique(y_vals)
        X, Y = np.meshgrid(x_unique, y_unique)
        Z = np.full_like(X, fill_value=np.nan, dtype=float)
        xi = np.searchsorted(x_unique, x_vals)
        yi = np.searchsorted(y_unique, y_vals)
        Z[yi, xi] = z_vals
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', colorbar=dict(title=component))])
        fig.update_layout(title=f'{component} @ {fixed_title}',
                          scene=dict(xaxis_title=config["sweepNames"][int(re.search(r'\d+', var1).group())-1],
                                     yaxis_title=config["sweepNames"][int(re.search(r'\d+', var2).group())-1],
                                     zaxis_title=component))
        list_of_plots.append(fig)

    # FFT 3D Bar plotting
    fft_plots = []
    def fft_barchart3d(x_vals, y_vals, z_vals, title, z_title, colorscale='Viridis', opacity=0.8):
        fig = go.Figure()
        ann = []
        dx = np.min(np.diff(np.sort(np.unique(x_vals)))) * 0.4 if len(x_vals)>1 else 1.0
        dy = np.min(np.diff(np.sort(np.unique(y_vals)))) * 0.4 if len(y_vals)>1 else 1.0
        for i, z_max in enumerate(z_vals):
            x_cnt, y_cnt = x_vals[i], y_vals[i]
            x_min, x_max = x_cnt-dx/2, x_cnt+dx/2
            y_min, y_max = y_cnt-dy/2, y_cnt+dy/2
            fig.add_trace(go.Mesh3d(
                x=[x_min, x_min, x_max, x_max, x_min, x_min, x_max, x_max],
                y=[y_min, y_max, y_max, y_min, y_min, y_max, y_max, y_min],
                z=[0,0,0,0,z_max,z_max,z_max,z_max],
                alphahull=0, intensity=[0,0,0,0,z_max,z_max,z_max,z_max],
                coloraxis='coloraxis', opacity=opacity
            ))
            ann.append(dict(showarrow=False, x=x_cnt, y=y_cnt, z=z_max,
                            text=f'{z_max:.2f}', font=dict(color='white', size=10),
                            bgcolor='rgba(0,0,0,0.3)', xanchor='center', yanchor='middle'))
        fig.update_layout(title=title,
                          scene=dict(xaxis_title="Frequency [Hz]",
                                     yaxis_title="Sweep Var",
                                     zaxis_title=z_title,
                                     annotations=ann),
                          coloraxis=dict(colorscale=colorscale))
        return fig

    for component, fixed_values, fft_rows in product(FFT_headers, fixed_combos, fft_rows_list):
        if len(fft_rows) == 0: continue
        fixed = dict(zip(fixed_keys, fixed_values))
        z_column = FFT_headers.index(component)
        y_vals = fft_rows[:, 2]
        harm_xval = np.array(harmonics) * F_fund
        x_vals = np.tile(harm_xval, int(np.ceil(len(y_vals) / len(harm_xval))))[:len(y_vals)]
        z_vals = combined_fft_matrix[fft_rows[:, 0].astype(int), z_column]
        fixed_title = " | ".join(f"{config['sweepNames'][int(re.search(r'\d+', k).group())-1]} = {v}" for k, v in fixed.items())
        fig = fft_barchart3d(x_vals, y_vals, z_vals, f"{component} @ {fixed_title}", component)
        fft_plots.append(fig)

    # HTML report writing
    def write_html_report(html_file, plots):
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('''
                    <style> .container {position: relative;width: 100%;height: 150px;}
                            .logo {position: absolute;top: 0;right: 0;height: 120px;}
                            .info {position: absolute;left: 10px;font-weight: bold;}
                            .script_name { top: 10px; }
                            .date { top: 50px; }
                            .utc { top: 90px; }
                    </style>''')
            f.write(f'''<div class="container">
                        <img class="logo" src="data:image/png;base64,{base64_img}" alt="BMW Logo"/>
                        <div class="info script_name">Simulation: {os.path.basename(__file__)}</div>
                        <div class="info date">Date & Time: {date}</div>
                        <div class="info utc">Simulation ID: {UTC}</div>
                    </div>''')
            f.write('<div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;">\n')
            for fig in plots:
                fig_html = to_html(fig, include_plotlyjs='cdn', full_html=False)
                f.write(f'<div style="flex: 0 0 48%;">{fig_html}</div>\n')
            f.write('</div>\n')
            f.write('<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>\n')

    if split_3D:
        for idx, component in enumerate(headers_array):
            start, end = idx * len(fixed_combos), (idx + 1) * len(fixed_combos)
            write_html_report(f"{html_base}_{UTC}_{component}.html", list_of_plots[start:end])
        for idx, component in enumerate(FFT_headers):
            start, end = idx * len(fixed_combos), (idx + 1) * len(fixed_combos)
            write_html_report(f"{html_base}_{UTC}_{component}.html", fft_plots[start:end])
    else:
        write_html_report(f"{html_base}_{UTC}.html", list_of_plots)
        write_html_report(f"{html_base}_FFT_{UTC}.html", fft_plots)






header_path   = r"D:\WORKSPACE\BJT-MODEL\assets\HEADER_FILES"
folder        = r"D:\WORKSPACE\BJT-MODEL\CSV_MAPS"
input_json    = r"D:\WORKSPACE\BJT-MODEL\assets\Input_vars.json"
base64_file   = r"D:\WORKSPACE\BJT-MODEL\assets\BMW_Base64_Logo.txt"
html_base     = r"D:\WORKSPACE\BJT-MODEL\results\result"

excluded      = ['FFT_Voltage_Map.csv', 'FFT_Current_Map.csv']
excluded_headers = {'header.json', 'Peak_Losses.json'}

with open(input_json) as f: config = json.load(f)
var1, var2 = config["Var1"], config["Var2"]
split_3D   = True  
harmonics  = [1,2] 
F_fund     = 1e5 

script_name = os.path.basename(__file__)
UTC         = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
date        = str(datetime.datetime.now().replace(microsecond=0))

with open(base64_file, 'r') as f: base64_img = ''.join(line.strip() for line in f)
generate_bjt_report(header_path, folder, input_json, base64_file, html_base)

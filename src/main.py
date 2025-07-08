
#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                 ______  ____  _______  _____
#?                / __ \ \/ /  |/  / __ \/ ___/
#?               / /_/ /\  / /|_/ / / / /\__ \
#?              / ____/ / / /  / / /_/ /___/ /
#?             /_/     /_/_/  /_/\____//____/
#?
#? Name:        main.py
#? Purpose:     Main entry point for running simulations using the pymos models
#?
#? Author:      Mohamed Gueni (mohamedgueni@outlook.com)
#? Created:     21/05/2025
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import bjt
from Plot import MOSFETModelComparer
#? -------------------------------------------------------------------------------
points = 10     
Vgs_values = np.linspace(0, 20, points)
Vds_values = np.linspace(0, 10, points)
T_values   = np.linspace(300, 400.0, points)
BSIM3v3_2_PATH                   = r"D:\WORKSPACE\BSIM-Python-Implementation\data\BSIM3v3_2.csv"
PLOT                        = True
BSIM3v3_2_model            = BSIM3v3_2.BSIM3v3_Model()
#? -------------------------------------------------------------------------------
def simulate_model(model, T_values, Vgs_values, Vds_values, path):
    records         = []
    combinations    = [(T, Vgs, Vds) for T in T_values for Vgs in Vgs_values for Vds in Vds_values]
    total_points    = len(combinations)

    for i, (T, Vgs, Vds) in enumerate(combinations):
        Id  = model.compute(Vgs, Vds,0.0,T)
        records.append({
            'time'  : i // total_points ,
            'T'     : T                 ,
            'VGS'   : Vgs               ,
            'VDS'   : Vds               ,
            'ID'    : Id                
        })

    df = pd.DataFrame(records)
    df.to_csv(path, index=False)

def main():

    simulate_model(BSIM3v3_2_model            , T_values, Vgs_values, Vds_values, BSIM3v3_2_PATH       )

    if PLOT:
        plotter = MOSFETModelComparer([BSIM3v3_2_PATH])
        plotter.plot()
#? -------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#? -------------------------------------------------------------------------------
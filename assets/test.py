import numpy as np

# Simulate the dp module variables used in the function
class dp:
    np = np
    JSON = {'TF_Config': 'DCDC_S'}
    tkinter = type('tk', (), {'messagebox': type('mb', (), {'showerror': print})})
    sys = type('sys', (), {'exit': exit})
from functools import reduce

import ast
from functools import reduce
import operator

def return_resistances(op_dict):
    mdlv = op_dict['ModelVars']
    if dp.JSON['TF_Config'] != 'DCDC_S':
        dp.tkinter.messagebox.showerror('ERROR','MODEL NOT IMPLEMENTED OR INVALID CONFIG')
        dp.sys.exit()

    # Full paths in bracket-chain style with aligned colons
    paths = {
        "['DCDC_Rail1']['CT']['Trafo']['Rpri']"                  	: 1,
        "['DCDC_Rail1']['CT']['Trafo']['Rsec']"                  	: 1,
        "['DCDC_Rail1']['RCsnubber']['Choke']['Cs']['Rsingle']" 	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['Choke']['Rs']['R']"       	: lambda m: m['value']*1/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['Choke']['Rpar']"          	: 1,
        "['DCDC_Rail1']['RCDclamp1']['Cs']['Rsingle']"          	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCDclamp1']['Rs']['R']"                	: 1,
        "['DCDC_Rail1']['FRW']['BlockingCap']['Rsingle']"       	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['FRW']['Resistor']['R']"                	: 1,
        "['DCDC_Rail1']['FRW']['ImpedanceCap']['Rsingle']"      	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['Coe1']['Rd']"                          	: 1,
        "['DCDC_Rail1']['LV_currentSense']['R']"                	: 1,
        "['DCDC_Rail1']['Cpi']['Rsingle']"                      	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['Cin']['Rsingle']"                      	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['HV_currentSense']['R']"                	: 1,
        "['DCDC_Rail1']['Cb']['Rsingle']"                       	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['Trafo']['Cs']['Rsingle']" 	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['Trafo']['Rs']['R']"       	: lambda m: m['value']*1/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Cs']['Rsingle']" : lambda m: m['value']*4*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['SR_MOSFET']['Rs']['R']"       : lambda m: m['value']*4/m['nPar'],
        "['DCDC_Rail1']['Cyi']['Rsingle']"                      	: lambda m: m['value']*4*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['LV_FB']['Cs']['Rsingle']" 	: lambda m: m['value']*2*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['RCsnubber']['LV_FB']['Rs']['R']"       	: lambda m: m['value']*2/m['nPar'],
        "['DCDC_Rail1']['Cc']['Rsingle']"                       	: lambda m: m['value']*2*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['Co']['Rsingle']"                       	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['Coe1']['Rsingle']"                     	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['Cyo']['Rsingle']"                      	: lambda m: m['value']*4*m['nSer']/m['nPar'],
        "['DCDC_Rail1']['HV_voltageSense']['Divider']['R1']"    	: lambda m: m['value']*m['R1']+m['R2'],
        "['DCDC_Rail1']['HVcmc']['Rwind']"                      	: 2,
        "['Common']['Coc1']['Rsingle']"                         	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['Common']['Coc2']['Rsingle']"                         	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['Common']['Coec2']['Rsingle']"                        	: lambda m: m['value']*m['nSer']/m['nPar'],
        "['Common']['Cyoc']['Rsingle']"                         	: lambda m: m['value']*4*m['nSer']/m['nPar'],
        "['Common']['LVdmc']['Rwind']"                          	: 2,
        "['Common']['LVcmc']['Rwind']"                          	: 2,
        "['Common']['Busbars_PCB']['LV_Filter']['PlusResistance']"  : 1,
        "['Common']['Busbars_PCB']['LV_Filter']['MinusResistance']" : 1
    }

    # Compute resistances in a one-liner
    dp.Resistances = [
        ((lambda v, s: v*s if not callable(s) else v*s(v))(
            reduce(operator.getitem,
                   ast.literal_eval("[" + path.replace("][", ",")[1:-1] + "]"),
                   mdlv),
            scale
        ))
        for path, scale in paths.items()
    ]

    return dp.np.array(dp.Resistances)
# Example ModelVars dictionary
ModelVars_example = {
    'DCDC_Rail1': {
        'CT': {
            'Trafo': {
                'Rpri': 0.1,
                'Rsec': 0.05, 'nSer': 2, 'nPar': 1
            }
        },
        'RCsnubber': {
            'Choke': {
                'Cs': {'Rsingle': 0.01,'nSer': 2, 'nPar': 1},
                'Rs': {'R': 0.02}, 'nSer': 2, 'nPar': 1,
                'Rpar': 0.03
            },
            'Trafo': {
                'Cs': {'Rsingle': 0.01}, 'nSer': 2, 'nPar': 1,
                'Rs': {'R': 0.02}
            },
            'SR_MOSFET': {
                'Cs': {'Rsingle': 0.005}, 'nSer': 2, 'nPar': 1,
                'Rs': {'R': 0.01}
            },
            'LV_FB': {
                'Cs': {'Rsingle': 0.002}, 'nSer': 2, 'nPar': 1,
                'Rs': {'R': 0.004}
            }
        },
        'RCDclamp1': {
            'Cs': {'Rsingle': 0.006}, 'nSer': 2, 'nPar': 1,
            'Rs': {'R': 0.007}
        },
        'FRW': {
            'BlockingCap': {'Rsingle': 0.008}, 'nSer': 2, 'nPar': 1,
            'Resistor': {'R': 0.009}, 'nSer': 2, 'nPar': 1,
            'ImpedanceCap': {'Rsingle': 0.01}
        },
        'Coe1': {'Rd': 0.02, 'Rsingle': 0.01}, 'nSer': 2, 'nPar': 1,
        'LV_currentSense': {'R': 0.003}, 'nSer': 2, 'nPar': 1,
        'Cpi': {'Rsingle': 0.004},
        'Cin': {'Rsingle': 0.005},
        'HV_currentSense': {'R': 0.002},
        'Cb': {'Rsingle': 0.006},
        'Cyi': {'Rsingle': 0.007},
        'Cc': {'Rsingle': 0.008},
        'Co': {'Rsingle': 0.009},
        'Cyo': {'Rsingle': 0.01},
        'HV_voltageSense': {'Divider': {'R1': 1, 'R2': 2}},
        'HVcmc': {'Rwind': 0.05}
    },
    'Common': {
        'Coc1': {'Rsingle': 0.005},
        'Coc2': {'Rsingle': 0.006},
        'Coec2': {'Rsingle': 0.007},
        'Cyoc': {'Rsingle': 0.008},
        'LVdmc': {'Rwind': 0.01},
        'LVcmc': {'Rwind': 0.02},
        'Busbars_PCB': {'LV_Filter': {'PlusResistance': 0.001, 'MinusResistance': 0.002}}
    }
}

# Wrap in op_dict
op_dict_example = {'ModelVars': ModelVars_example}

# Call the function
resistances_array = return_resistances(op_dict_example)

print("Computed resistances:")
print(resistances_array)

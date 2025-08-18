
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                                    ____                            _                 _
#?                                                   |  _ \  ___ _ __   ___ _ __   __| | ___ _ __   ___(_) ___  ___
#?                                                   | | | |/ _ \ '_ \ / _ \ '_ \ / _` |/ _ \ '_ \ / __| |/ _ \/ __|
#?                                                   | |_| |  __/ |_) |  __/ | | | (_| |  __/ | | | (__| |  __/\__ \
#?                                                   |____/ \___| .__/ \___|_| |_|\__,_|\___|_| |_|\___|_|\___||___/
#?                                                              |_|
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Use the following command to install libs #? python -m pip install --proxy=http://hostname:<yourserver>:<port> <library to install>
# Example : python -m pip install --proxy=http://hostname:pass@proxy.muc:8080 numpy
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

import ast
import json                                                                                     #
from doctest import script_from_examples                                                        #
import os,sys                                                                                   #
import time,copy,glob,datetime                                                                  #
from importlib.resources import path                                                            #
from sysconfig import get_path                                                                  #
from collections import OrderedDict                                                             #
import numpy as np                                                                              #
import pandas as pd                                                                             #
from csv import writer                                                                          #
from cmath import nan                                                                           #
import math                                                                                     #
from numpy import dtype                                                                         #
from turtle import shape                                                                        #
from os.path import exists                                                                      #
import pyfiglet                                                                                 #
from pyfiglet import figlet_format                                                              #
import xmlrpc.client                                                                            #
import jsonrpc_requests	                                                                        #
sys.path.insert(1,os.getcwd() + '/Script/Lib')                                                  #
import pyplecs_rpc as pc                                                                        #
import Data_Process as PP                                                                       #
import Param_Process as PM                                                                      #
import Pylog as flg                                                                             #
import Pyutils as sutl                                                                          #
import Pymisc as msc                                                                            #
import RunScripts as run                                                                        #
sys.path.insert(1,os.getcwd() + '/Script/assets')                                               #
import random                                                                                   #
import Mags_Dicts,Sensor_Dicts,Switches_Dicts,Fuses_Dicts,Relay_Dicts, Battery_Dicts                          #
#import SA21_param,SB10_param,SB20_param,SB21_param,SEB2_param                                   #
import warnings                                                                                 #
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)                        #
from matplotlib import style,cm                                                                 #
import csv ,shutil                                                                              #
from pathlib import Path                                                                        #
import xmlrpc.client                                                                            #
import psutil,subprocess,re,socket                                                              #
import py_plot as plt                                                                           #
import tkinter as tk                                                                            #
from tkinter import font                                                                        #
from plotly.subplots import make_subplots                                                       #
import plotly.graph_objects as go                                                               #
import tkinter.messagebox                                                                       #
from tkinter import filedialog                                                                  #
import multiprocessing                                                                          #
from natsort import natsorted                                                                   #
import itertools                                                                                #
from more_itertools import chunked                                                              #
import flatdict                                                                                 #
from unflatten import unflatten                                                                 #
import re                                                                                       #
import importlib                                                                                #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
inputname           =   "Input_vars.json"                                                       #
JSON                =   PP.Processing().dump_json_data(inputname)                               #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
if JSON["resim"]:
    sys.path.insert(0,os.getcwd() +  '/Script/Data/Res/' + JSON['scriptName'] + '_' + str(JSON['folder_utc_res']) )
else:
    sys.path.insert(1,os.getcwd() + '/Script/assets')

# Get the module name from the configuration
if (not JSON.get("params")):
    paramdict_to_use = "Param_Dicts"                                                            # Default to "Param_Dicts"
else:
    paramdict_to_use    = JSON.get("params")

# Dynamically import the specified module
try:
    Param_Dicts     = importlib.import_module(paramdict_to_use)
except ModuleNotFoundError:
    raise ImportError(f"Module {paramdict_to_use} specified in input_vars.json could not be found.")
globals()["Param_Dicts"] = Param_Dicts

sys.path.insert(1,os.getcwd() + '/Script/assets')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
url                 =   "http://127.0.0.1"                                                        # PLECS Host ip address : keep default if used locally.
port                =   "1080"                                                                    # Port at which to communicate with PLECS.
mdl_precision       =   8                                                                         # value precision for init dictionaries.
mdlVars             =   Param_Dicts.ModelVars                                                     # ModelVars simulation parameters dictionary.
slvOpts             =   Param_Dicts.SolverOpts                                                    # SolverOpts simulation parameters dictionary.
anlOpts             =   Param_Dicts.AnalysisOpts                                                  # AnalysisOpts simulation parameters dictionary.
METHOD			    =   "JSON"				                                                      # Options --> "XML", "JSON"
Export              =   "TF"                                                                      # Options --> "RPC", "TF"
command             =   r"C:/plecs/PLECS.exe"                                                     # Command to execute Plecs software automatically form the OS.
BMW_Base64_Logo     =   "Script/assets/BMW_Base64_Logo.txt"                                       # Base64 data related to BMW logo used in html reports.
Header_File         =   "Script/assets/HEADER_FILES/header.json"                                  # Json file path in which we store headers.
script_path         =   ''                                                                        # Path to the current running python script.
cp_mdl              =   ''                                                                        # Path to the current running plecs model.
suffix              =   ""                                                                        # Suffix used in results folder name.
ToFile              =   mdlVars['Common']['ToFile']                                               # ModelVars ToFile Dictionary.
tinit_sim           =   time.time()                                                               # Simulation init Time.
pmapping            =	[]                                                                        # Plecs mapping list.
pmap_3D		        =	[]                                                                        # Plecs mapping nested list for 3D plotting purposes.
pmap_multi	        =	[]                                                                        # Plecs mapping nested list for multi-plotting purposes.
pmap_plt            =   {}                                                                        # Plecs mapping dictionary for generating html reports.
constant_dict       =   {}                                                                        # Plecs mapping dictionary for constants.
pmap_plt_ctrl       =   {}                                                                        # Plecs mapping dictionary for controls
scriptname          =   JSON['scriptName']                                                        #
Runscript_path      =   "Lib/RunScripts.py"                                                       #
ScriptBody_path     =   "Lib/ScriptBody.py"                                                       #
Y_Length            =   []                                                                        #
Y_list              =   []                                                                        #
Resistances         =   []                                                                        #
Pout_idx            =   0                                                                         #
Rail_idx            =   0                                                                         #
Common_idx          =   0                                                                         #
phase               =   0                                                                         #
current_idx         =   0                                                                         #
com_cols            =   0                                                                         #
harmonics           =   np.arange(0,JSON['hrmcs']+1,1, dtype=int).tolist()                        #
F_Fund              =   mdlVars['Common']['MCU']['f_s']                                           #
trafo_inputs        =   []                                                                        #
choke_inputs        =   []                                                                        #
idx_start,idx_end   =   0,0                                                                       #
plt_title_list      =   []                                                                        #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
if JSON["resim"]:                                                                                 #
    sys.path.insert(1,os.getcwd() +  '/Script/Data/Res/' + JSON['scriptName'] + '_' + str(JSON['folder_utc_res']) )
    import plecs_mapping as pmap                                                                  #
else:                                                                                             #
    sys.path.insert(1,os.getcwd() + '/Script/assets')                                             #
    import plecs_mapping as pmap                                                                  #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
from scipy.interpolate import RegularGridInterpolator ,interp1d                                   #
from scipy.fft import fft,fftfreq                                                                 #
import scipy.signal                                                                               #
pwm_dict            = {}                                                                          #
from decimal import Decimal                                                                       #
slices              = []                                                                          # Define the slices as a list
mode                = " "                                                                         #
map_index           = " "                                                                         #
map_names           = " "

from deepdiff import DeepDiff

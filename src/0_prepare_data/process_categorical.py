#%%
import pandas as pd
from pathlib import Path
import numpy as np
import yaml
import os, sys
import pickle

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

#%%
from src.utils import *
config = load_config()

DATA_PATH = PROJECT_PATH.joinpath('data')
output_path = Path(config['path']).joinpath('data/processed/process_data')

if not output_path.exists() : 
    output_path.mkdir(parents=True)
    
creatinine = load_data('CREATININE')

#%%
idx = ~creatinine.labresult.isna()
creatinine = creatinine[idx].copy()

# %%

with open(output_path.joinpath('BP.pkl'), 'rb') as f:
    bp = pickle.load(f)
patients =  bp['patientunitstayid']
del bp
# %%
creatinine = creatinine[creatinine.patientunitstayid.isin(patients)].copy()

# %%
# make categorical
def make_categorical(x):
    if x > 1.2 :
        return 3
    elif (x <= 1.2) & (x >= 0.7) :
        return 2
    else :
        return 1

creatinine['value'] = creatinine.labresult.apply(make_categorical)

creatinine = creatinine[['patientunitstayid','labresultoffset','value']].copy()

creatinine = creatinine.sort_values(by=['patientunitstayid','labresultoffset'])
# %%
creatinine['timestep'] = creatinine.groupby('patientunitstayid').cumcount()

#%%
creatinine = creatinine[['patientunitstayid','timestep','value']].copy()

# %%
creatinine = creatinine.pivot_table(index='patientunitstayid',columns='timestep',values='value').reset_index()
# %%

creatinine = creatinine.fillna(0)


# %%
def to_pickle(path : Path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

to_pickle(output_path.joinpath('creatinine.pkl'), creatinine)
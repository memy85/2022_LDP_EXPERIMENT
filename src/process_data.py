#%%

import pandas as pd
from pathlib import Path
import yaml
import os, sys
import pickle
from utils import *

#%%
config = load_config()
output_path = Path(config['path']).joinpath('data/processed/process_data')

if not output_path.exists() : 
    output_path.mkdir(parents=True)

#%%

BP = load_data('BP')
CRP = load_data('CRP')
glucose = load_data('glucose')
RBC = load_data('RBC')

#%%
BP = BP.sort_values(by=['patientunitstayid','observationoffset'])
CRP = CRP.sort_values(by=['patientunitstayid','labresultoffset'])
glucose = glucose.sort_values(by=['patientunitstayid','labresultoffset'])
RBC = RBC.sort_values(by=['patientunitstayid','labresultoffset'])

#%%
BP = BP.dropna().reset_index(drop=True)
CRP = CRP.dropna().reset_index(drop=True)
glucose = glucose.dropna().reset_index(drop=True)
RBC = RBC.dropna().reset_index(drop=True)

#%%
BP = BP.rename(columns = {"noninvasivesystolic":"value"})
CRP = CRP.rename(columns = {"labresultext":"value"})
glucose = glucose.rename(columns = {"labresultext":"value"})
RBC = RBC.rename(columns = {"labresultext":"value"})

#%%
data = {'BP':BP, 'CRP':CRP, 'glucose':glucose, 'RBC':RBC}

def load_original_data(name):
    ori_data, patients = data[name], set(data[name].patientunitstayid.unique())
    divided_by_patients = [ori_data[ori_data.patientunitstayid == pt] for pt in list(patients) if len(ori_data[ori_data.patientunitstayid == pt]) > 1]
    return divided_by_patients

#%%
bp_list = load_original_data('BP')
crp_list = load_original_data('CRP')
rbc_list = load_original_data('RBC')
glucose_list = load_original_data('glucose')


def to_pickle(path : Path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
#%%

to_pickle(output_path.joinpath('BP.pkl'), bp_list)
to_pickle(output_path.joinpath('CRP.pkl'), crp_list)
to_pickle(output_path.joinpath('RBC.pkl'), rbc_list)
to_pickle(output_path.joinpath('glucose.pkl'), glucose_list)

print('done')
# BP.to_feather(output_path.joinpath('BP.feather'))
# CRP.to_feather(output_path.joinpath('CRP.feather'))
# glucose.to_feather(output_path.joinpath('glucose.feather'))
# RBC.to_feather(output_path.joinpath('RBC.feather'))


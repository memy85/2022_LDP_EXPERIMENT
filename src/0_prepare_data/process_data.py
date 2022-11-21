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

BP = BP.dropna().reset_index(drop=True)
CRP = CRP.dropna().reset_index(drop=True)
glucose = glucose.dropna().reset_index(drop=True)
RBC = RBC.dropna().reset_index(drop=True)

#%%
BP = BP.rename(columns = {"noninvasivesystolic":"value","observationoffset":"time"})
CRP = CRP.rename(columns = {"labresulttext":"value","labresultoffset":"time"})
glucose = glucose.rename(columns = {"labresulttext":"value","labresultoffset":"time"})
RBC = RBC.rename(columns = {"labresulttext":"value","labresultoffset":"time"})

#%%
CRP = CRP.replace('>|<', '', regex=True)
glucose = glucose.replace('>|<', '', regex=True)
RBC = RBC.replace('>|<', '', regex=True)

def drop_one_step(data):
    df = data.groupby('patientunitstayid', as_index=False).size()
    df = df.rename(columns = {'size':"row_count"})

    include_patients = df[df.row_count > 1]['patientunitstayid'].unique()
    data = data[data.patientunitstayid.isin(include_patients)]
    return data.reset_index(drop=True).copy()


#%%
BP = drop_one_step(BP)
CRP = drop_one_step(CRP)
glucose = drop_one_step(glucose)
RBC = drop_one_step(RBC)

#%%
#%% filter patients with same stay id
bp_patients = set(BP.patientunitstayid)
crp_patients = set(CRP.patientunitstayid)
glu_patients = set(glucose.patientunitstayid)
rbc_patients = set(RBC.patientunitstayid)

common_patients = bp_patients & crp_patients & glu_patients & rbc_patients
#%%

BP = BP[BP.patientunitstayid.isin(common_patients)].reset_index(drop=True).copy()
CRP = CRP[CRP.patientunitstayid.isin(common_patients)].reset_index(drop=True).copy()
glucose = glucose[glucose.patientunitstayid.isin(common_patients)].reset_index(drop=True).copy()
RBC = RBC[RBC.patientunitstayid.isin(common_patients)].reset_index(drop=True).copy()


#%%
# def filter_out_patients(data):
#     frame = data.groupby('patientunitstayid').size()
#     index = (data.groupby('patientunitstayid').size() >= 2)
#     include_these_patients = frame[index].index.tolist()
#     data = data[data.patientunitstayid.isin(include_these_patients)].copy().reset_index(drop=True)
    
#     q3 = data.groupby('patientunitstayid').size().quantile(0.75)
#     q1 = data.groupby('patientunitstayid').size().quantile(0.25)
#     iq = q3 - q1 
#     lower_bound = q1 - 1.5*iq
#     upper_bound = q3 + 1.5*iq

#     frame = data.groupby('patientunitstayid').size()
#     lower = frame < lower_bound
#     upper = frame > upper_bound

#     exclude_these = set(frame[lower].index.tolist()) | set(frame[upper].index.tolist())
#     data = data[~data.patientunitstayid.isin(exclude_these)].copy()
#     return data



#%%
BP = BP.astype({'value':'float32'})
CRP = CRP.astype({'value':'float32'})
glucose = glucose.astype({'value':'float32'})
RBC = RBC.astype({'value':'float32'})


#%%
BP['timestep']=BP.groupby('patientunitstayid').cumcount()
CRP['timestep']=CRP.groupby('patientunitstayid').cumcount()
glucose['timestep']=glucose.groupby('patientunitstayid').cumcount()
RBC['timestep']=RBC.groupby('patientunitstayid').cumcount()

#%%
BP = BP.pivot_table(index='patientunitstayid',columns='timestep',values='value').reset_index()
CRP = CRP.pivot_table(index='patientunitstayid',columns='timestep',values='value').reset_index()
glucose = glucose.pivot_table(index='patientunitstayid',columns='timestep',values='value').reset_index()
RBC = RBC.pivot_table(index='patientunitstayid',columns='timestep',values='value').reset_index()

#%%
BP = BP.fillna(0)
CRP = CRP.fillna(0)
glucose = glucose.fillna(0)
RBC = RBC.fillna(0)

# #%%
# book = {'BP':BP, 'CRP':CRP, 'glucose':glucose, 'RBC':RBC}

#%%

# def load_original_data(name):
#     global book
#     ori_data, patients = book[name], set(book[name].patientunitstayid.unique())
#     divided_by_patients = [ori_data[ori_data.patientunitstayid == pt] for pt in list(patients) if len(ori_data[ori_data.patientunitstayid == pt]) > 1]
#     return divided_by_patients


# #%%
# bp_list = load_original_data('BP')
# crp_list = load_original_data('CRP')
# rbc_list = load_original_data('RBC')
# glucose_list = load_original_data('glucose')


def to_pickle(path : Path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
#%%

to_pickle(output_path.joinpath('BP.pkl'), BP)
to_pickle(output_path.joinpath('CRP.pkl'), CRP)
to_pickle(output_path.joinpath('RBC.pkl'), RBC)
to_pickle(output_path.joinpath('glucose.pkl'), glucose)

print('done')





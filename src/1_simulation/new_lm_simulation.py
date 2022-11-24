#%%
import pandas as pd
from pathlib import Path
import yaml
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from pathos.multiprocessing import ProcessingPool, _ProcessPool
from multiprocessing import Pool
import argparse
import pickle
from itertools import repeat
from sklearn.preprocessing import MinMaxScaler

# import syndp.algorithm.timedp_algorithm as tdp
# from syndp.mechanism.bounded_laplace_mechanism import boundedlaplacemechanism as blm
# from syndp.mechanism.laplace_mechanism import laplace_mechanism as lm
# from syndp import laplace_mechanism as lm
# from syndp import bounded_laplace_mechanism as blm
import syndp.original_timedp as odp

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

#%%
from src.utils import *
config = load_config()
    
epsilon = config['epsilon']
PROJ_PATH = Path(config['path'])
INPUT_PATH = PROJ_PATH.joinpath('data/processed/process_data')
OUTPUT_PATH = PROJ_PATH.joinpath('data/processed/new_lm_simulation')

if not OUTPUT_PATH.exists():
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    

#%%
def load_original_data(name):
    '''
    return original data from processed path
    return : (original data : dataframe, unique patient : set)
    '''
    with open(INPUT_PATH.joinpath(f'{name}.pkl'), 'rb') as f:
        ori_data = pickle.load(f)
    patients = len(ori_data)
    
    return ori_data, patients

#%%
def give_noise(data, eps):
    syn = data.copy()
    vals = syn.values[:, 1:]
    
    scaler = MinMaxScaler((-1,1))
    scaler.fit(vals)
    scaled = scaler.transform(vals)
    
    vals = list(vals)
    # apply original timeseries differential privacy
    # new_vals = np.apply_along_axis(odp.timeseries_dp, 1, vals, eps)
    with Pool(16) as p:
        new_values = p.starmap(odp.timeseries_dp, zip(vals, repeat(eps)))
    
    new_values = np.array(new_values)
    new_values = np.round(scaler.inverse_transform(new_values))

    bone = data[['patientunitstayid']]
    new_values = pd.DataFrame(new_values)
    syn = pd.concat([bone, new_values], axis=1)
    
    syn = syn.melt(id_vars = 'patientunitstayid', var_name='timestep')
    syn = syn.sort_values(by=['patientunitstayid','timestep'])
    
    return syn['value']
    # return dp_creator.new_vector

def get_changed_results(data, epsilon=epsilon):
    melt_table = data.melt(id_vars='patientunitstayid').copy()
    melt_table = melt_table.sort_values(by=['patientunitstayid','timestep'])
    
    for eps in epsilon :
        melt_table[f'value_{eps}']= give_noise(data, eps)
    
    return melt_table

#%%
def transform_data(name):
    ori_data, patients = load_original_data(name)
    
    print(f'total patient counts : {patients}')
    
    all_results = get_changed_results(ori_data)
    return all_results

#%%
if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-n", "--name", dest="name", action="store")          
    # args = parser.parse_args()

    for name in ['CRP','BP','glucose','RBC','creatinine']:
        print(f'starting {name} ...')
        result = transform_data(name)
        result = result.reset_index(drop=True)
        print(f'{name} is finished')
        
        result.to_feather(OUTPUT_PATH.joinpath(f'{name}.feather'))





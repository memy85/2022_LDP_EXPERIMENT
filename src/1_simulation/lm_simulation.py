#%%
import pandas as pd
from pathlib import Path
import yaml
import os, sys
import matplotlib.pyplot as plt
import numpy as np
from pathos.multiprocessing import ProcessingPool, _ProcessPool
import argparse
import pickle
from itertools import repeat

# import syndp.algorithm.original_timedp as odp
# import syndp.algorithm.timedp_algorithm as tdp
# from syndp.mechanism.bounded_laplace_mechanism import boundedlaplacemechanism as blm
# from syndp.mechanism.laplace_mechanism import laplace_mechanism as lm
from syndp import laplace_mechanism as lm
from syndp import bounded_laplace_mechanism as blm

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

#%%
from src.utils import *
config = load_config()
    
epsilon = config['epsilon']
PROJ_PATH = Path(config['path'])
INPUT_PATH = PROJ_PATH.joinpath('data/processed/process_data')
OUTPUT_PATH = PROJ_PATH.joinpath('data/processed/lm_simulation')

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

def give_noise(data, eps, scale):
    data['value'] = data['value'].astype('float')
    copied_data = data.copy() 
    # lpm = np.vectorize(lm)
    length = len(copied_data['value'])
    scale = scale/eps
    
    rv = np.random.laplace(0, scale, length)
    noised_value = copied_data['value'] + rv
    # noised_value = lpm(copied_data['value'], 1, eps)
    return noised_value

def get_changed_results(data, scale, epsilon=epsilon):
    for eps in epsilon :
        data[f'value_{eps}']= give_noise(data, eps, scale)
        
    return data

#%%
def transform_data(name):
    ori_data, patients = load_original_data(name)
    min_val, max_val = ori_data.values[:,1:].min(), ori_data.values[:,1:].max()
    scales = abs(max_val - min_val)
    
    ori_data = ori_data.melt(id_vars='patientunitstayid')
    ori_data = ori_data.sort_values(by=['patientunitstayid','timestep'])
    
    print('divided patients')
    print(f'total patient counts : {patients}')
    
    
    all_results = get_changed_results(ori_data, scales)
    return all_results

#%%

if __name__ == "__main__":
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-n", "--name", dest="name", action="store")          
    # args = parser.parse_args()
    for name in ['BP','CRP','CRP', 'glucose']:
        print(f'starting {name} ...')
        result = transform_data(name)
        result = result.reset_index(drop=True)
        print(f'{name} is finished')
        
        result.to_feather(OUTPUT_PATH.joinpath(f'{name}.feather'))




#%%
import pandas as pd
from pathlib import Path
import yaml
import os, sys
import matplotlib.pyplot as plt
from utils import *
import numpy as np
from pathos.multiprocessing import ProcessingPool
import argparse
import pickle

# import syndp.algorithm.original_timedp as odp
# import syndp.algorithm.timedp_algorithm as tdp
# from syndp.mechanism.bounded_laplace_mechanism import boundedlaplacemechanism as blm
from syndp.mechanism.laplace_mechanism import laplace_mechanism as lm

#%%

config = load_config()
epsilon = config['epsilon']
PROJ_PATH = Path(config['path'])
INPUT_PATH = PROJ_PATH.joinpath('data/processed/process_data')
OUTPUT_PATH = PROJ_PATH.joinpath('data/processed/lm_simulation')

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

#%%
def change_column_name(data):
    return data.rename(columns={'labresulttext':'value'})

def load_original_data(name):
    '''
    return original data from processed path
    return : (original data : dataframe, unique patient : set)
    '''
    with open(INPUT_PATH.joinpath(f'{name}.pkl'), 'rb') as f:
        ori_data = pickle.load(f)
    patients = len(ori_data)
    return ori_data, patients

def give_noise(data, eps):
    data['value'] = data['value'].astype('float')
    copied_data = data.copy() 
    lpm = np.vectorize(lm)
    noised_value = lpm(copied_data['value'], 1, eps)
    return noised_value

def get_changed_results(data, epsilon=epsilon):
    for eps in epsilon :
        data[f'value_{eps}']= give_noise(data, eps)
    return data

#%%
def transform_data(name):
    ori_data, patients = load_original_data(name)
    
    print('divided patients')
    print(f'total patient counts : {patients}')
    
    pool = ProcessingPool(8)
    all_results = pool.map(get_changed_results, ori_data)
    all_results = pd.concat(all_results)
    return all_results

#%%

#%%

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")          
    args = parser.parse_args()

    result = transform_data(args.name)
    result = result.reset_index(drop=True)

    #%%
    result.to_feather(OUTPUT_PATH.joinpath(f'{args.name}.feather'))

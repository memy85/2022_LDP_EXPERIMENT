#%%
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import yaml
import os, sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
import pylab
import argparse
from tslearn.metrics import dtw
import numpy as np

from pathos.pools import ParallelPool
from pathos.multiprocessing import ProcessPool

from pathlib import Path
import os, sys
# changed

#%%
PROJECT_PATH = Path(__file__).parents[1]
DATA_PATH = PROJECT_PATH.joinpath('data')

from src.utils import *
from src.privacy import *

#%%

config = load_config()

#%%

PROJ_PATH = Path(config['path'])
input_path = PROJ_PATH.joinpath('data/processed/process_for_figures')
output_path = PROJ_PATH.joinpath('data/processed/process_for_figures')
if not output_path.exists() :
    PROJ_PATH.joinpath('data/processed/process_for_figures').mkdir(parents=True)
fig_path = PROJ_PATH.joinpath('figures')


#%%
def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
    
def load_data(name, type, eps):
    return load_pickle(input_path.joinpath(f'{type}_{name}_{eps}.pkl'))


def change_dtypes(x):
    return np.array(x)

def change_dtype_for_data(name, types):
    
    for eps in config['epsilon']:
        data = load_data(name, types, eps)
        d1, d2, s1 = data
        
        d1 = list(map(change_dtypes, d1))
        d2 = list(map(change_dtypes, d2))
        s1 = list(map(change_dtypes, s1))
        
        obj = (d1, d2, s1)
        with open(output_path.joinpath(f'{types}_{name}_{eps}.pkl'), 'wb') as f:
            pickle.dump(obj, f)
        
        print(f'type {types} name {name} epsilon {eps} finished')
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")          
    parser.add_argument("-t", "--type", dest='type', action="store")
    args = parser.parse_args()
    
    change_dtype_for_data(args.name, args.type)
    print('finished!')
    
if __name__== "__main__":
    main()
    
    
    
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

from pathos.pools import ParallelPool
from pathos.multiprocessing import ProcessPool

from utils import *
from privacy import *


#%%
config = load_config()

PROJ_PATH = Path(config['path'])
lm_sim_data = PROJ_PATH.joinpath('data/processed/lm_simulation')
new_lm_sim_data = PROJ_PATH.joinpath('data/processed/new_lm_simulation')
output_path = PROJ_PATH.joinpath('data/processed/process_for_figures')
if not output_path.exists() :
    PROJ_PATH.joinpath('data/processed/process_for_figures').mkdir(parents=True)
fig_path = PROJ_PATH.joinpath('figures')

#%%
def load_lm_data(name):
    return pd.read_feather(lm_sim_data.joinpath(f'{name}.feather'))

def load_new_lm_data(name):
    return pd.read_feather(new_lm_sim_data.joinpath(f'{name}.feather'))


#%%

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")          
    parser.add_argument("-t", "--type", dest='type', action="store")
    args = parser.parse_args()
    
    if args.type == 'lm':
        data = load_lm_data(args.name)
    else :
        data = load_new_lm_data(args.name)
    
    epsilons = config['epsilon']
    
    for eps in epsilons:
        (D1, S1), D2 = process_for_privacy_validation(data, eps)
        obj = (D1, D2, S1)
        with open(output_path.joinpath(f'{args.type}_{args.name}_{eps}.pkl'), 'wb') as f:
            pickle.dump(obj, f)
        del obj
        print(f'finished epsilon {eps}')
        
if __name__ == "__main__":
    main()

#%%
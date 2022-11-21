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
from tslearn.metrics import dtw
import pylab
import argparse
from multiprocessing import Pool
from pathos.multiprocessing import _ProcessPool
from itertools import repeat
import numpy as np

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

from src.utils import *
config = load_config()

PROJ_PATH = Path(config['path'])
lm_sim_data = PROJ_PATH.joinpath('data/processed/lm_simulation')
new_lm_sim_data = PROJ_PATH.joinpath('data/processed/new_lm_simulation')
fig_path = PROJ_PATH.joinpath('figures')

#%%
def load_lm_data(name):
    return pd.read_feather(lm_sim_data.joinpath(f'{name}.feather'))

def load_new_lm_data(name):
    return pd.read_feather(new_lm_sim_data.joinpath(f'{name}.feather'))
#%%

def calculate_dtw(patient_id, data, epsilon):
    original = data[data.patientunitstayid == patient_id]['value']
    synthetic = data[data.patientunitstayid == patient_id][f'value_{epsilon}']
    return dtw(original, synthetic)


#%%
def calculate_dtw_from_table(table):
    epsilon = config['epsilon']
    
    patients = list(table['patientunitstayid'].unique())
    
    dtw_list = []
    for eps in epsilon:
        #     mse = ((table['value'] - table[f'value_{eps}'])**2).mean()
    #     mse_list.append(mse)
        with _ProcessPool(16) as p:
            dtws = p.starmap(calculate_dtw, zip(patients, repeat(table), repeat(eps)))
            dtws = np.array(dtws)
            val = np.mean(dtws)
            dtw_list.append(val)
        
    return dtw_list


#%%
def main():
    
    list_of_args = ['BP','RBC','glucose','CRP']
    
    lm_datas = [load_lm_data(name) for name in list_of_args]
    new_lm_datas = [load_new_lm_data(name) for name in list_of_args]
    
    dtws = []
    new_dtws = []
    for data, new_data in zip(lm_datas, new_lm_datas):
        
        dtws.append(calculate_dtw_from_table(data))
        new_dtws.append(calculate_dtw_from_table(new_data))
    
    xticks = [str(i) for i in config['epsilon']]
    
    fig, ax = plt.subplots(figsize = (10,10), nrows=2, ncols=2)

    for idx, (dtw_lm, dtw_new_lm) in enumerate(zip(dtws, new_dtws)):
        name = list_of_args[idx]
        r = idx // 2
        c = idx % 2
        
        ax[r,c].plot(xticks, dtw_lm, 'o-', color='black', label='DP')
        ax[r,c].plot(xticks, dtw_new_lm, 'o--', color='black', label='TDP')
        ax[r,c].set_title(config['title'][name])
        ax[r,c].set_ylabel(config['ylabels'][name])
        ax[r,c].set_xlabel(f'epsilon [$\epsilon$]')
        ax[r,c].legend(loc='upper right')
    
    fig.tight_layout()
    # plt.show()
    
    plt.savefig(fig_path.joinpath(f'supplement1.png'), 
                dpi=200,
                bbox_inches='tight')
    pass

#%%

if __name__ == "__main__":    
    main()
# %%

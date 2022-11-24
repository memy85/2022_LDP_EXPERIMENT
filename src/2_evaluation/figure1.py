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
def calculate_mse(table):
    epsilon = config['epsilon']
    mse_list = []
    for eps in epsilon:
        mse = ((table['value'] - table[f'value_{eps}'])**2).mean()
        mse_list.append(mse)
    return mse_list


#%%
def main():
    
    # list_of_args = ['BP','RBC','glucose','CRP']
    list_of_args = ['BP','RBC', 'glucose', 'CRP','creatinine']
    
    lm_datas = [load_lm_data(name) for name in list_of_args]
    new_lm_datas = [load_new_lm_data(name) for name in list_of_args]
    
    mses = []
    new_mses = []
    for data, new_data in zip(lm_datas, new_lm_datas):
        
        mses.append(calculate_mse(data))
        new_mses.append(calculate_mse(new_data))
    
    xticks = [str(i) for i in config['epsilon']]
    
    plt.rcParams.update({'font.size':12})
    fig, ax = plt.subplots(figsize = (10,10), nrows=3, ncols=1)
    
    for idx, (mse_lm, mse_new_lm) in enumerate(zip(mses, new_mses)):
        name = list_of_args[idx]
        # r = idx // 2
        # c = idx % 2
        
        # ax[r,c].plot(xticks, mse_lm, 'o-', color='black', label='DP')
        # ax[r,c].plot(xticks, mse_new_lm, 'o--', color='black', label='TDP')
        # ax[r,c].set_title(config['title'][name])
        # ax[r,c].set_ylabel(config['ylabels'][name])
        # ax[r,c].set_xlabel(f'epsilon [$\epsilon$]')
        # ax[r,c].legend(loc='upper right')
        
        ax[idx].plot(xticks, mse_lm, 'o-', color='black', label='DP')
        ax[idx].plot(xticks, mse_new_lm, 'o--', color='black', label='TDP')
        ax[idx].set_ylim([0, 10])
        ax[idx].set_title(config['title'][name])
        ax[idx].set_ylabel(config['ylabels'][name])
        ax[idx].set_xlabel(f'epsilon [$\epsilon$]')
        ax[idx].legend(loc='upper right')
    
    fig.tight_layout()
    # plt.show()
    
    plt.savefig(fig_path.joinpath(f'fig1_supplement.png'), 
                dpi=200,
                bbox_inches='tight')
    pass
#%%

if __name__ == "__main__":    
    main()
# %%

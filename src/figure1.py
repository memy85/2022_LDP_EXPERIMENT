#%%
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import yaml
import os, sys
import matplotlib.pyplot as plt
import argparse
from utils import *

#%%
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
def calculate_mse(data):
    epsilon = config['epsilon']
    mse_list = []
    for eps in epsilon:
        print(eps)
        mse = sum((data['value'] - data[f'value_{eps}'])**2) / len(data)
        mse_list.append(mse)
    return mse_list

#%%
# mse_lm = calculate_mse(data)
# mse_new_lm = calculate_mse()

#%%
# mse
# #%%

# plt.plot(mse_lm, style='dotted')
# plt.plot(mse_new_lm, style='dashdot')
# plt.xlabel('epsilon')


#%%
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")
    args = parser.parse_args()
    
    data = load_lm_data(args.name)
    mse_lm = calculate_mse(data)
    mse_new_lm = calculate_mse()

    #%%

    plt.plot(mse_lm, style='dotted')
    plt.plot(mse_new_lm, style='dashdot')
    plt.xticks([0.1, 1, 5, 10, 20])
    plt.xlabel('epsilon')
    plt.show()
    
    plt.savefig(fig_path.joinpath(f'fig1_{args.name}.png'), 
                dpi=200,
                bbox_inches='tight')
    pass

if __name__ == "__main__":    
    main()
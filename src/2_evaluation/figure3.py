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
import seaborn as sns
import pylab
import argparse
import numpy as np

from utils import *

#%%
config = load_config()

#%%
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
def calculate_helinger(data):
    epsilon = config['epsilon']
    mse_list = []
    for eps in epsilon:
        mse = ((data['value'] - data[f'value_{eps}'])**2).mean()
        mse_list.append(mse)
    return mse_list

#%%
CRP = load_lm_data('CRP')


#%%

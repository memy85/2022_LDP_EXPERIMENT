
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

from utils import *

#%%

config = load_config()

PROJ_PATH = Path(config['path'])
input_path = PROJ_PATH.joinpath('data/processed/classify')
output_path = PROJ_PATH.joinpath('data/processed/table1')
if not output_path.exists() :
    output_path.mkdir(parents=True)

#%%
def load_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__" :
    all_datas = [load_pickle(path) for path in input_path.iterdir()]

#%%
    results = pd.DataFrame(all_datas)
    results.to_csv(output_path.joinpath('table1.csv'), index=False)



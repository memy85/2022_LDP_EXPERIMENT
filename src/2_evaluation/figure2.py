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

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

from src.utils import *
config = load_config()

PROJ_PATH = Path(config['path'])
input_path = PROJ_PATH.joinpath('data/processed/table1/')
fig_path = PROJ_PATH.joinpath('figures')

#%%
table1 = pd.read_csv(input_path.joinpath('table1.csv'))
#%%
table1 = table1.replace('lm', 'DP')
table1 = table1.replace('new_lm','TDP')

#%%
def give_data(name):
    data = table1[table1.name == name]
    return data

def plot(name):
    data = give_data(name)
    
    fig, axes = plt.subplots(1,4, figsize=(7,3))
    plt.rcParams.update({'font.size':12})
# sns.set_style('white')
    s1 = sns.boxplot(data=data, x = 'types', y='accuracy', color='gray', hue ='types',ax=axes[0])
    s1.set_title('Accuracy')
    s1.set(xlabel=None)
    s1.set(ylabel=None)
    s1.legend([])

    s2 = sns.boxplot(data=data, x = 'types', y='sensitivity', color='gray',hue ='types',ax=axes[1])
    s2.set_title('Sensitivity')
    s2.set(ylabel=None)
    s2.set(xlabel=None)
    s2.legend([])

    s3 = sns.boxplot(data=data, x = 'types', y='specificity', color='gray', hue ='types',ax=axes[2])
    s3.set_title('Specificity')
    s3.set(ylabel=None)
    s3.set(xlabel=None)
    s3.legend([])

    s4 = sns.boxplot(data=data, x = 'types', y='f1_score', color='gray', hue ='types',ax=axes[3])
    s4.set_title('F1 score')
    s4.set(ylabel=None)
    s4.set(xlabel=None)
    s4.legend([])

    plt.tight_layout()
    # plt.show()/
    plt.savefig(fig_path.joinpath(f'fig2_{name}.png'),
                dpi=200,
                bbox_inches='tight')
#%%

#%%

if __name__ == "__main__":

    for variables in ['RBC','BP','CRP','glucose'] :
        plot(variables)
        print(f'plot {variables}')

    
#%%




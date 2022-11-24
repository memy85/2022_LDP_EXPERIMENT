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

def give_data(name):
    data = table1[table1.name == name]
    return data

book = {"epsilon":
    {0.1 : 1, 0.2 : 2, 0.4 : 3,
     0.8 : 4, 1.6 : 5, 3.2 : 6,
     6.4 : 7}
    }

def plot(name):
    data = give_data(name)
    data = data.copy().replace(book)
    
    plt.style.use('ggplot')
    sns.set(font_scale=1.3)
    fig, axes = plt.subplots(4,1, figsize=(10, 14), sharex=True, sharey=True)
    plt.rcParams.update({'font.size':15})
    markers = ["o","o"]
    size = 8
    xtick_size = 15
    ytick_size = 10
    palettes = ['black','black']
    
# sns.set_style('white')

    s1 = sns.lineplot(data=data, x = 'epsilon', y='accuracy', markers=markers, style='types', 
                      palette=palettes, hue ='types',ax=axes[0], markersize=size, legend=False)
    s1.set_title('Accuracy')
    s1.set_xticks([1,2,3,4,5,6,7])
    s1.set_xticklabels(['0.1', '0.2', '0.4', '0.8', '1.6', '3.2', '6.4'], fontsize=xtick_size)
    # s1.set_ytick(fontsize=ytick_size)

    s2 = sns.lineplot(data=data, x = 'epsilon', y='sensitivity', markers=markers, style='types', 
                      palette=palettes,hue ='types',ax=axes[1], markersize=size, legend=False)
    s2.set_xticks([1,2,3,4,5,6,7])
    s2.set_xticklabels(['0.1', '0.2', '0.4', '0.8', '1.6', '3.2', '6.4'], fontsize=xtick_size)
    s2.set_title('Sensitivity')

    s3 = sns.lineplot(data=data, x = 'epsilon', y='specificity', markers=markers, style='types', 
                      palette=palettes, hue ='types',ax=axes[2], markersize=size, legend=False)
    s3.set_xticks([1,2,3,4,5,6,7])
    s3.set_xticklabels(['0.1', '0.2', '0.4', '0.8', '1.6', '3.2', '6.4'], fontsize=xtick_size)
    s3.set_title('Specificity')
    s3.set_ylim([0.2, 1.1])

    s4 = sns.lineplot(data=data, x = 'epsilon', y='f1_score', markers=markers ,  style='types', 
                      palette=palettes, hue ='types',ax=axes[3], markersize=size, legend=False)
    s4.set_xticks([1,2,3,4,5,6,7])
    s4.set_xticklabels(['0.1', '0.2', '0.4', '0.8', '1.6', '3.2', '6.4'], fontsize=xtick_size)
    s4.set_title('F1 score')
    
    plt.xlim(0.8, 7.2)
    plt.legend(['DP','TDP'],bbox_to_anchor=(0.65, -0.2),ncol=2)
    plt.tight_layout()
    
    plt.savefig(fig_path.joinpath(f'fig2_{name}.png'),
                dpi=200,
                bbox_inches='tight')



if __name__ == "__main__":

    for variables in ['BP','CRP','glucose','RBC','creatinine'] :
        plot(variables)
        print(f'plot {variables}')

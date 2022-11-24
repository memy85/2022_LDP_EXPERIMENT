
'''
This code is for printing some examples of the synthesized results
'''
#%%
import pandas as pd
import pickle
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_score, recall_score, confusion_matrix, f1_score, accuracy_score
import os, sys
from pathlib import Path
import matplotlib.pyplot as plt
import random

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

from src.utils import *
config = load_config()

PROJ_PATH = Path(config['path'])
input_path = PROJ_PATH.joinpath('data/processed/create_train_test')
figure_path = PROJ_PATH.joinpath('figures/')
if not figure_path.exists():
    figure_path.mkdir(parents=True)

#%%
def load_data(name, types, epsilon):
    '''
    override load_data from utils.py
    '''
    path = input_path.joinpath(f'{name}_{types}_{epsilon}.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)


#%%

def main():
    '''
    samples the patients from the figure preprocessed data and
    draws the how the samples are different by DP and TDP
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--name')
    parser.add_argument('--epsilon', type=float)
    args = parser.parse_args()

    lm_sample, _, _, _ = load_data(args.name, 'lm', args.epsilon)
    new_lm_sample, _, _, _ = load_data(args.name, 'new_lm', args.epsilon)

    patients = [i for i in range(0, len(lm_sample)//2)]

    pt = random.sample(patients, 1)[0]
    idx = lm_sample.shape[0]//2
    
    plt.rcParams.update({'font.size':12})
    plt.title(config["title"][args.name])
    plt.plot(lm_sample[pt], 'o--',color='#1b9e77', label='original')
    plt.plot(lm_sample[idx + pt], 'o-',color='#d95f02', label='DP')
    plt.plot(new_lm_sample[idx + pt], 'x-', color='#7570b3', label='TDP')
    plt.xlim(-0.2, 6)
    plt.xlabel('timestep')
    plt.ylabel(config['ylabels'][args.name])
    plt.legend() 
    
    plt.tight_layout()
    # plt.show()/
    plt.savefig(figure_path.joinpath(f'discussion_{args.name}.png'),
                dpi=200,
                bbox_inches='tight')

# %%
if __name__ == "__main__" : 
    main()
# %%

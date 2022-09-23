#%%
from ast import arg
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import math
import argparse
import random

from utils import *

config = load_config()

#%%
PROJ_PATH = Path(config['path'])
lm_path = PROJ_PATH.joinpath('data/processed/lm_simulation')
new_lm_path = PROJ_PATH.joinpath('data/processed/new_lm_simulation')
output_path = PROJ_PATH.joinpath('data/processed/create_train_test')

if not output_path.exists() :
    output_path.mkdir(parents=True)

#%%
def load_data(name, types):
    '''
    overloading the load_data function from utils.py
    '''
    if types == 'lm':
        path = lm_path.joinpath(f'{name}.feather')
    else :
        path = new_lm_path.joinpath(f'{name}.feather')
    return pd.read_feather(path)


#%%
def equalize_data_length(data, epsilon):
    if epsilon == 0 :
        value = 'value'
    else :
        value = f'value_{epsilon}'
    max_length = data['patientunitstayid'].value_counts().max()
    number_of_patients = len(data['patientunitstayid'].unique())
    
    central = np.zeros((number_of_patients,max_length))
    grouped = data.groupby('patientunitstayid')[value]
    
    for idx, (indices, patient_data) in enumerate(grouped):
        length = len(patient_data)
        central[idx,0:length] = patient_data
    return central

#%%




#%%

def create_train_test(numpy_data : np.array, new_numpy_data):
    number_of_patients = len(numpy_data)
    random.seed(config['seed'])
    
    indices = [idx for idx in range(number_of_patients)]
    new_indices = random.sample(indices, math.floor(number_of_patients/10))
    cut_index = math.floor(len(new_indices)*0.8)
    
    train_idx, test_idx = new_indices[:cut_index], new_indices[cut_index:]
    
    x_train = np.take(numpy_data, train_idx, axis=0)
    x_test = np.take(numpy_data, test_idx, axis=0)
    y_train = np.zeros(len(train_idx))
    y_test = np.zeros(len(test_idx))
    
    new_x_train = np.take(new_numpy_data, train_idx, axis=0)
    new_x_test = np.take(new_numpy_data, test_idx, axis=0)
    new_y_train = np.ones(len(train_idx))
    new_y_test = np.ones(len(test_idx))
    
    x_train = np.concatenate((x_train, new_x_train), axis=0)
    x_test = np.concatenate((x_test, new_x_test), axis=0)
    y_train = np.concatenate((y_train, new_y_train))
    y_test = np.concatenate((y_test, new_y_test))
    
    return x_train, x_test, y_train, y_test
    

#%%

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")          
    parser.add_argument("-t", "--type", dest="type", action="store")          
    parser.add_argument("-e", "--epsilon", dest='epsilon', action="store")
    args = parser.parse_args()
    
    data = load_data(args.name, args.type)
    
    np_data1 = equalize_data_length(data, 0)
    np_data2 = equalize_data_length(data, args.epsilon)

    x_train, x_test, y_train, y_test = create_train_test(np_data1, np_data2)
    
    dataset = (x_train, x_test, y_train, y_test)
    
    with open(output_path.joinpath(f'{args.name}_{args.type}_{args.epsilon}.pkl'), 'wb') as f:
        pickle.dump(dataset, f)
    
#%%

if __name__=="__main__":
    main()
#%%
import pandas as pd
import pickle
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_score, recall_score, confusion_matrix, f1_score, accuracy_score
import os, sys
from pathlib import Path

PROJECT_PATH = Path(__file__).parents[2]
os.sys.path.append(PROJECT_PATH.as_posix())

from src.utils import *
config = load_config()

#%%
PROJ_PATH = Path(config['path'])
input_path = PROJ_PATH.joinpath('data/processed/create_train_test')
output_path = PROJ_PATH.joinpath('data/processed/classify')
if not output_path.exists():
    output_path.mkdir(parents=True)

#%%
def load_data(name, types, epsilon):
    '''
    override load_data from utils.py
    '''
    path = input_path.joinpath(f'{name}_{types}_{epsilon}.pkl')
    with open(path, 'rb') as f:
        return pickle.load(f)

def write_dict(name, types, epsilon, precision, sensitivity, specificity, f1score, accuracy):
    
    book = {'name':name, 'types': types,'epsilon' : epsilon, 
            'precision':precision, 'sensitivity':sensitivity,
            'specificity':specificity, 'f1_score':f1score,
            'accuracy':accuracy}
    
    with open(output_path.joinpath(f'{name}_{types}_{epsilon}.pkl'), 'wb') as f:
        pickle.dump(book, f)

#%%

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", action="store")          
    parser.add_argument("-t", "--type", dest="type", action="store")          
    parser.add_argument("-e", "--epsilon", dest='epsilon', action="store")
    args = parser.parse_args()
    
    print(f'starting {args.name} {args.type} {args.epsilon} testing')
    
    dataset = load_data(args.name, args.type, args.epsilon)   

    x_train, x_test, y_train, y_test = dataset

    #%% 
    clf = RandomForestClassifier(max_depth=2, random_state=config['seed'])
    
    clf.fit(x_train, y_train)

    y_pred = clf.predict(x_test)

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    
    specificity = tn / (tn + fp)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro')
    sensitivity = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    
    write_dict(args.name, args.type, args.epsilon, precision, sensitivity, specificity, f1, accuracy)
    print('done')
    
if __name__ == "__main__":
    main()


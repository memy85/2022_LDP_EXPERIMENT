
#%%
from multiprocessing.dummy import Process
from pandas import Series, DataFrame
import pandas as pd
from scipy.spatial.distance import hamming
from tslearn.metrics import dtw
from itertools import combinations
import pickle
from pathos.multiprocessing import ProcessingPool
from multiprocessing import pool

from figure2 import calculate_dtw
#%%

def hamming_distance(d1 : Series, d2 : Series):
    '''
    hamming distance calculator
    '''
    return hamming(d1, d2) * len(d1)

def dtw_distance(d1 : Series, d2 : Series):
    return dtw(d1, d2)

    
def return_data_as_list(data : DataFrame):
    patients = data['patientunitstayid'].unique().tolist()
    
    def return_id_data(id):
        return data[data.patientunitstayid == id].copy()
    p = ProcessingPool(16)
    data_list = p.map(return_id_data, patients)
    return data_list

def get_D1_and_S1(data_list, epsilon, idx):
    d1 = data_list[:idx]
    
    def extract_D1(data):
        return data['value'].copy()
    
    p = ProcessingPool(16)
    D1 = p.map(extract_D1, d1)
    
    def extract_S1(data):
        return data[f'value_{epsilon}'].copy()
    S1 = p.map(extract_S1, d1)
    return D1, S1

def get_D2(data_list, idx):
    
    d2 = data_list[idx:]
    def extract_D2(data):
        return data['value'].copy()
    p = ProcessingPool(16)
    D2 = p.map(extract_D2, d2)
    return D2

    
def process_for_privacy_validation(data, epsilon):
    '''
    data : refers to the original data with the dp data
    this selects the D1 and D2 and S1
    '''
    all_patients = len(data['patientunitstayid'].unique())
    idx = all_patients // 2
    
    data_list = return_data_as_list(data)
    
    D1, S1 = get_D1_and_S1(data_list, epsilon, idx)
    D2 = get_D2(data_list, idx)
    return (D1, S1), D2

def calculate_distance(real : Series, synth_list : list):
    
    
    f = lambda x : dtw_distance(real, x)
    
    output = list(map(f, synth_list))
    return min(output)


def validate_privacy(D1 : list, D2 : list, S1 :list):
    '''
    returns the sensitivity and specificity score for 
    D1 and D2 and S1 
    '''
    D1 = D1.copy()
    D2 = D2.copy()
    
    D1.extend(D2)
    distance_list = []
    
    # p = ProcessingPool(8)
    
    
    f = lambda x : calculate_distance(x, S1)
    distance_list = list(map(f, D1))
    
    return distance_list


def load_pickled_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data
    

def make_dataframe(path, distance):
    data = load_pickled_data(path)
    
    D1, D2, S1 = data[0], data[1], data[2]
    distance_list = validate_privacy(D1, D2, S1)
    
    # patients = data['patientunitstayid'].unique().tolist()
    df = pd.DataFrame({'distance' : distance_list})
    
    return df.eval(f'query = distance <= {distance}')

def calculate_sens_and_spec(df):
    
    idx = len(df) // 2
    positive  = df['query'].sum()
    TP = df.iloc[:idx, 'query'].sum()
    
    negative = len(df) - positive
    TN = sum(~df.iloc[idx:, 'query'])
    
    return TP/positive, TN/negative
    




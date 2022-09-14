import pandas as pd
from pandas import Series
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import sklearn as sk


def count_values(series : Series, value):
    '''
    count values in a series
    '''
    return sum(series == value)


def hellinger_metric(A : Series, B : Series, type):
    '''
    A : original data column
    B : synthetic data column
    type : continuous, categorical
    
    H(P,Q) = 1/sqrt(2)||sqrt(P)-sqrt(Q)||_2 : Euclidian norm
    where, P, A are probability distributions
    '''
    A, B = A.dropna().copy(), B.dropna().copy()
    
    assert len(A) != 0, 'the input of original data has no data'
    assert len(B) != 0, 'the input of synthetic data has no data'
    
    if type == 'categorical':
        
        values_of_A = A.unique().tolist()
        values_of_B = B.unique().tolist()

        all_possible_values = set(values_of_A) | set(values_of_B)
        val_counts_A = dict()
        val_counts_B = dict()
        
        for val in all_possible_values:
            
            val_counts_A[val] = count_values(A, val) / len(A)
            val_counts_B[val] = count_values(B, val) / len(B)
            
        f = lambda p, q : (np.sqrt(p) - np.sqrt(q))**2
        
        def H(P : dict, Q : dict , values : list):
            return np.sqrt(sum([f(P[val], Q[val]) for val in values])) * 1/np.sqrt(2)
        
        return H(val_counts_A, val_counts_B, all_possible_values)  
            
    else :
        '''
        case where type == continuous
        '''
        
        min_val, max_val = min(min(A), min(B)), max(max(A), max(B))
        scaled_A, scaled_B = A / max_val, B / max_val
        
        def find_interval(val):
            down = round(val, 2)
            if down == 1 :
                return 0.995
            return round(down + 0.005, 3)

        def make_count_book(values):
            d = list(map(find_interval, values)) # output of calculated interval
            count_book = {round(k, 3) : 0 for k in np.arange(0.005, 1, 0.01)}
            for val in d:
                count_book[val] += 1
            count_book = {k : v/len(d) for k, v in count_book.items()}
            return count_book
        
        cb_A = make_count_book(scaled_A)
        cb_B = make_count_book(scaled_B)
        
        all_values = list(cb_A.keys())

        f = lambda p, q : (np.sqrt(p) - np.sqrt(q))**2
        
        def H(P : dict, Q : dict , values : list):
            return np.sqrt(sum([f(P[val], Q[val]) for val in values])) * 1/np.sqrt(2)
        
        return H(cb_A, cb_B, all_values)
    
    
    
from pandas import Series, DataFrame
import pandas as pd
from numpy import array
import numpy as np

#%%
def compare_two_records(real : Series, synthetic : Series, distance):
    '''
    compares two give real and synthetic record
    metric -> hamming distance
    '''
    dist = sum(real == synthetic)
    
    if dist > distance : 
        return 0
    else :
        return 1
    

#%%
def identity_disclosure(real_1: DataFrame, real_2 : DataFrame, synthetic: DataFrame, hamming_distance = 5):
    '''
    real_1 : 합성에 사용된 원본 데이터
    real_2 : 합성에 사용되지 않은 원본 데이터
    synthetic : 합성된 데이터
    '''
    real1 = real_1.copy()
    real2 = real_2.copy()
    
    real1['category'] = 1
    real2['category'] = 2
    
    pd.concat([real1, real2])
    
    pass



def attribute_disclosure():
    pass
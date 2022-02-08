#%%
import numpy as np
import pandas as pd
import pickle
from argparse import Namespace
from pathlib import Path
from multiprocessing import Pool

# Settings
settings = Namespace(
    data_dir = Path.parent.joinpath('data')
    epsilon = "0.1"
    delta = "0.5" # should be in (0,1)
)



# define Bounded Laplace Mechanim
def pdf_BLM(value, D: tuple, b=1, epsilon, delta): 
    '''
    density function of Wq(bounded laplace mechanism)
    D : the support for x(value)
    b : variance -> requires checkup. 
    sensitivity : the minimal difference 
    '''
    # assign boundaries
    l, u  = D

    if value not in range(l,u+1): return 0
    
    # calculate C with internal function
    def calc_C(value , D:tuple ,b):
        l, u = D
        return 1 - (1/2)*(np.exp(-((value-l)/b)) + np.exp(-(u-value)/b))

    
    # Theorem 4.4(Fixed Point)
    dQ = abs(u - l)
    
    # calculate Cl, Cl_dQ #Definition3.4
    Cl = calc_C(l, D, b)
    Cl_dQ = calc_C(l + dQ, D, b)
    
    dC = Cl_dQ / Cl

    if b < dQ/(epsilon - np.log(dC) - np.log(1 - delta)) :
        print('the variance does not suffice the preconditions')
        print('editing b ...')
        b = dQ/(epsilon - np.log(dC) - np.log(1 - delta))
        print(f"the value of b is {b}")
        # update b

    # calculate the optimal Cq
    Cq = calc_C(value, D, b)
    # return density 
    theRange = np.linspace(l, u, num = 10**3)

    e_term = np.exp(-(abs(theRange - value)/b))
    density  = (1/Cq)*(1/(2*b))*(e_term)
    return density

if __name__ == "__main__":

    pdf_BLM(value, settings.epsilon)

#%%
import numpy as np
import pandas as pd
import pickle
from argparse import Namespace
from pathlib import Path
from multiprocessing import Pool

# Settings
settings = Namespace(
    # data_dir = Path.parent.joinpath('data'),
    epsilon = "0.1",
    delta = "0.5" # should be in (0,1)
)

# calculate Cq
def cal_C(value, D, b):
    l, u = D
    return 1 - (1/2)*(np.exp((l-value)/b) + np.exp((value-u)/b))


# define Bounded Laplace Mechanim
def boundedLaplaceMechanism(value, D: tuple, b, epsilon, delta): 
    '''
    density function of Wq(bounded laplace mechanism)
    D : the support for x(value)
    b : variance -> requires checkup. 
    sensitivity : the minimal difference 
    '''
    # assign boundaries
    l, u  = D

    if value not in range(l,u+1): return 0
    
    # Theorem 4.4(Fixed Point)
    dQ = abs(u - l)
    
    # calculate Cl, Cl_dQ #Definition3.4
    Cl = cal_C(l, D, b)
    Cl_dQ = cal_C(l + dQ, D, b)
    
    dC = Cl_dQ / Cl
    # print(f'Cl is {Cl} and Cl_dQ is {Cl_dQ}')
    # print(f'dC is {dC}')

    if b < dQ/(epsilon - np.log(dC) - np.log(1 - delta)) :
        # print('the variance does not suffice the preconditions')
        # print('editing b ...')
        b = dQ/(epsilon - np.log(dC) - np.log(1 - delta))
        # print(f"the value of b is {b}")
        # update b

    # Here we do not calculate Cq 
    # Instead we calculate the function and then sum the output calculations
    theRange = np.linspace(l, u, num = 10**4)
    e_term = np.exp(-(abs(theRange - value)/b)) 
    output_calculation  = (1/(2*b))*(e_term)
    
    # sum the output calculation and normalize
    theSum = output_calculation.sum()
    density = output_calculation/theSum 
    
    # the function will output a randomized output!
    randomized_output = np.random.choice(theRange, 1, p=density)

    return randomized_output.item()

if __name__ == "__main__":
    
    # load data 
    data = np.loadtxt(settings.data_dir.joinpath('data'))
    range_info = "insert range info" # range 정보 적어줘야 함

    with Pool(5) as p :
        p.map(pdf_BLM, data)
        pdf_BLM(value, settings.epsilon)

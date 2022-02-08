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



# define Bounded Laplace Mechanim


if __name__ == "__main__":
    
    # load data 
    data = np.loadtxt(settings.data_dir.joinpath('data'))
    range_info = "insert range info" # range 정보 적어줘야 함

    with Pool(5) as p :
        p.map(pdf_BLM, data)
        pdf_BLM(value, settings.epsilon)

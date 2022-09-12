#%%
import pandas as pd
from pathlib import Path
import yaml
import os, sys
import matplotlib.pyplot as plt
from utils import *
#%%

config = load_config()

#%%
PROJ_PATH = Path(config['path'])

#%%

plt.plot()
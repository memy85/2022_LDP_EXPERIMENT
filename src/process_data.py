#%%

import pandas as pd
from pathlib import Path
import yaml
import os, sys
from utils import *

#%%
config = load_config()
output_path = Path(config['path']).joinpath('data/processed/process_data')

if not output_path.exists() : 
    output_path.mkdir(parents=True)

#%%

BP = load_data('BP')
CRP = load_data('CRP')
glucose = load_data('glucose')
RBC = load_data('RBC')

#%%

BP = BP.dropna().reset_index(drop=True)
CRP = CRP.dropna().reset_index(drop=True)
glucose = glucose.dropna().reset_index(drop=True)
RBC = RBC.dropna().reset_index(drop=True)

#%%
BP = BP.sort_values(by=['patientunitstayid','observationoffset'])
CRP = CRP.sort_values(by=['patientunitstayid','labresultoffset'])
glucose = glucose.sort_values(by=['patientunitstayid','labresultoffset'])
RBC = RBC.sort_values(by=['patientunitstayid','labresultoffset'])

#%%

BP.to_feather(output_path.joinpath('BP.feather'))
CRP.to_feather(output_path.joinpath('CRP.feather'))
glucose.to_feather(output_path.joinpath('glucose.feather'))
RBC.to_feather(output_path.joinpath('RBC.feather'))
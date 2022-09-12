from json import load
import os, sys
from pathlib import Path
import yaml
import pandas as pd

def load_config():
    project_path = Path.cwd().parents[0]
    with open(project_path.joinpath('config/config.yaml')) as f:
        config = yaml.load(f, yaml.SafeLoader)
    return config


def load_data(name):
    '''
    data names : BP, CRP, glucose, RBC
    '''
    config = load_config()
    PROJ_PATH = Path(config['path'])
    path = PROJ_PATH.joinpath(f'data/raw/{name}.feather')
    return pd.read_feather(path)
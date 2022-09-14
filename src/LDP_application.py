import pandas as pd
import numpy as np
from multiprocessing import Pool
import os, sys
from pathlib import Path
from configparser import ConfigParser
from LDP_application import BLM

# PATH SETTINGS
CURDIR = Path
parser = ConfigParser()
parser.read('config.txt')


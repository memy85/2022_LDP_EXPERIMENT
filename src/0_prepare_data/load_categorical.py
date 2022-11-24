#%%
import pandas as pd
import sqlalchemy as db
import urllib.parse
from pathlib import Path
import os, sys
# changed

#%%
PROJECT_PATH = Path(__file__).parents[2]
DATA_PATH = PROJECT_PATH.joinpath('data')


#%%
pwd = urllib.parse.quote_plus("@wkd1ao2al3")
engine = db.create_engine(f'mysql+pymysql://wonseok:{pwd}@103.22.220.149:13306/eicu')

query = '''
select patientunitstayid, labresultoffset, labname, labresult, labmeasurenamesystem
from LAB
where labname="creatinine"
'''

creatinine = pd.read_sql_query(query, con=engine)

creatinine.to_feather(DATA_PATH.joinpath('raw','CREATININE.feather'))

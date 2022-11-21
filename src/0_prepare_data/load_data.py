
#%%
import pandas as pd
import sqlalchemy as db
import urllib.parse
from pathlib import Path
import os, sys
# changed

#%%
PROJECT_PATH = Path(__file__).parents[1]
DATA_PATH = PROJECT_PATH.joinpath('data')

#%%
pwd = urllib.parse.quote_plus("@wkd1ao2al3")
engine = db.create_engine(f'mysql+pymysql://wonseok:{pwd}@103.22.220.149:13306/eicu')

query = '''
select *
from LAB
'''
lab = pd.read_sql_query(query, con=engine)


#%%
query = '''
select *
from VITALAPERIODIC
'''

vital = pd.read_sql_query(query, con=engine)

#%%

BP = vital[['patientunitstayid','observationoffset','noninvasivesystolic']].reset_index(drop=True)
RBC = lab[lab.labname == 'RBC'][['patientunitstayid','labresultoffset','labname','labresulttext']].reset_index(drop=True)
glucose = lab[lab.labname == 'glucose'][['patientunitstayid','labresultoffset','labname','labresulttext']].reset_index(drop=True)
CRP = lab[lab.labname == 'CRP'][['patientunitstayid','labresultoffset','labname','labresulttext']].reset_index(drop=True)

#%%

BP.to_feather(DATA_PATH.joinpath('raw','BP.feather'))
RBC.to_feather(DATA_PATH.joinpath('raw','RBC.feather'))
glucose.to_feather(DATA_PATH.joinpath('raw','glucose.feather'))
CRP.to_feather(DATA_PATH.joinpath('raw','CRP.feather'))
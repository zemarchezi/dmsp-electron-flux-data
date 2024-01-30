#%%
import numpy as np
import pandas as pd
from pysatdata.loaders.load import *
# %%
trange_plot=['2010-07-03', '2010-07-05'] # time range for ploting
trange=['2010-07-02', '2010-07-06'] 
paramLoadSat = {"satellite": 'dmsp', "probe": 'f17',
                "instrument": 'ssj', "datatype": 'precipitating-electrons-ions'}

varss_dmsp = load_sat(trange=trange, satellite=paramLoadSat["satellite"],
                     probe=[paramLoadSat["probe"]],
                     instrument=paramLoadSat["instrument"],datatype=paramLoadSat["datatype"], downloadonly=False,
                     testRemotePath=True,
                     usePandas=False, usePyTplot=True)
print(varss_dmsp)
# %%

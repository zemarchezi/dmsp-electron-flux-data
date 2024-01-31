#%%
import numpy as np
import pandas as pd
from pysatdata.loaders.load import *
import pytz
import datetime
import matplotlib.pyplot as plt
# %%
trange_plot=['2010-07-03', '2010-07-05'] # time range for ploting
trange=['2010-07-02', '2010-07-06'] 
paramLoadSat = {"satellite": 'dmsp', "probe": 'f17',
                "instrument": 'ssj', "datatype": 'precipitating-electrons-ions'}

varss_dmsp = load_sat(trange=trange, satellite=paramLoadSat["satellite"],
                     probe=[paramLoadSat["probe"]],
                     instrument=paramLoadSat["instrument"],datatype=paramLoadSat["datatype"], downloadonly=False,
                     testRemotePath=False, searchFilesFirst=True,
                     usePandas=False, usePyTplot=True)
print(varss_dmsp)
# %%
quants_electr_dmsp = pytplot.data_quants['ELE_DIFF_ENERGY_FLUX']
# %%
flux_dmsp = quants_electr_dmsp.values
#%%
time_dt_dmsp = quants_electr_dmsp.coords['time'].values
#%%
time_dt_dmsp = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in time_dt_dmsp]
# %%
spec = quants_electr_dmsp.coords['spec_bins'].values
#%%
v1 = quants_electr_dmsp.coords['v'].values
# %%
ener30 = flux_dmsp[:,-1]
# %%
## Ssis data for MLT and location.

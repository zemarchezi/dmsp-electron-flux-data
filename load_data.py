#%%
import numpy as np
import pandas as pd
from pysatdata.loaders.load import *
import pytz
import datetime
import matplotlib.pyplot as plt
from scipy import interpolate as interp
# %%
trange_plot=['2009-07-03', '2009-07-05'] # time range for ploting
trange=['2009-07-02', '2009-07-06'] 
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
spec = quants_electr_dmsp.coords['spec_bins'].values[0]
#%%
v1 = quants_electr_dmsp.coords['v'].values
# %%
ener30 = flux_dmsp[:,-1]
# %%
## Ssis data for MLT and location.
paramLoadSat = {"satellite": 'dmsp', "probe": 'f17',
                "instrument": 'ssies', "datatype": 'thermal-plasma'}

varss_dmsp = load_sat(trange=trange, satellite=paramLoadSat["satellite"],
                     probe=[paramLoadSat["probe"]],
                     instrument=paramLoadSat["instrument"],datatype=paramLoadSat["datatype"], downloadonly=False,
                     testRemotePath=True,
                     usePandas=False, usePyTplot=True)
print(varss_dmsp)
# %%
quants_mlt_dmsp = pytplot.data_quants['mlt']
quants_mlat_dmsp = pytplot.data_quants['mlat']
mlt_dmsp = quants_mlt_dmsp.values
mlat_dmsp = quants_mlat_dmsp.values
#%%
time_mlt_dmsp = quants_mlt_dmsp.coords['time'].values
#%%
time_mlt_dmsp = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in time_mlt_dmsp]

#%%

fl = interp.interp1d((np.arange(0, len(mlt_dmsp))), mlt_dmsp, bounds_error=False)
lnewy = np.linspace(0, len(mlt_dmsp), ener30.shape[0])
mlt_new = fl(lnewy)
# mltDf = pd.DataFrame(mlt_new,index=time).interpolate()
# %%
fl = interp.interp1d((np.arange(0, len(mlat_dmsp))), mlat_dmsp, bounds_error=False)
lnewy = np.linspace(0, len(mlat_dmsp), ener30.shape[0])
mlat_new = fl(lnewy)
# %%
dfEnergy = pd.DataFrame({"ener30": ener30, "mlt": mlt_new, "mlat": mlat_new}, index=time_dt_dmsp)
# %%
# mlatArray = dfEnergy["mlat"].apply(np.floor).unique()
# mlatArray = np.sort(mlatArray)
bin_size = 3
mlatArray = np.arange(60,90,bin_size)

mltArray = np.arange(0,24, 1)

# %%
binOccurrence = np.zeros((len(mltArray),len(mlatArray)))
for mlat in range(len(mlatArray)):
    for mlt in range(len(mltArray)):
        mlst = dfEnergy[(dfEnergy.mlt >= mltArray[mlt]) & (dfEnergy.mlt < mltArray[mlt]+1)]
        ls = mlst[(mlst['mlat'] >= mlatArray[mlat]) & (mlst['mlat'] < mlatArray[mlat]+bin_size)]
        binOccurrence[mlt,mlat] = ls.mlat.count() 
# %%
rad = mlatArray
azm = np.asarray(mltArray)/23.*2*np.pi
r, th = np.meshgrid(rad, azm)

cm2 = plt.cm.get_cmap('plasma')
fig = plt.figure(figsize=(12,15))
ax = fig.add_subplot(111, projection='polar')
ax.set_theta_offset(np.pi*3/2)
plt.pcolormesh(th, r, binOccurrence, cmap=cm2)
plt.plot(azm, r, ls='none')
plt.grid()
# plt.thetagrids([theta * 15 for theta in range(360//15)], labels=mltArray)
plt.colorbar(aspect=20, fraction=0.08)
# # %%

# %%

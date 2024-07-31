#%%
import numpy as np
import pandas as pd
import glob
import pytplot
from tqdm import tqdm
import pickle
import gc
from datetime import datetime
from pysatdata.loaders.load import *
import pytz
from scipy import interpolate as interp
#%%
def download_read_electron_data(trange, paramLoadSat):
    pytplot.del_data()
    varss_dmsp = load_sat(trange=trange, satellite=paramLoadSat["satellite"],
                     probe=[paramLoadSat["probe"]],
                     instrument=paramLoadSat["instrument"],datatype=paramLoadSat["datatype"], downloadonly=False,
                     testRemotePath=False, searchFilesFirst=True,
                     usePandas=False, usePyTplot=True)
    try:
        quants_dmsp = pytplot.data_quants['ELE_DIFF_ENERGY_FLUX']

        flux_dmsp = quants_dmsp.values
        time_dt_dmsp = quants_dmsp.coords['time'].values
        time_dt_dmsp = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in time_dt_dmsp]
        spec = quants_dmsp.coords['spec_bins'].values[0]
        colss = [str(i) for i in spec]

        return flux_dmsp, time_dt_dmsp, colss
    except:
        return None, None, None
    
def download_read_plasma_data(trange, paramLoadSat):
    pytplot.del_data()
    varss_dmsp = load_sat(trange=trange, satellite=paramLoadSat["satellite"],
                     probe=[paramLoadSat["probe"]],
                     instrument=paramLoadSat["instrument"],datatype=paramLoadSat["datatype"], downloadonly=False,
                     testRemotePath=False, searchFilesFirst=True,
                     usePandas=False, usePyTplot=True)
    try:
        quants_mlt_dmsp = pytplot.data_quants['mlt']
        quants_mlat_dmsp = pytplot.data_quants['mlat']
        mlt_dmsp = quants_mlt_dmsp.values
        mlat_dmsp = quants_mlat_dmsp.values

        time_mlt_dmsp = quants_mlt_dmsp.coords['time'].values
        time_mlt_dmsp = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in time_mlt_dmsp]

        return mlt_dmsp, mlat_dmsp, time_mlt_dmsp
    except:
        return None, None, None

def interpolate_cadence(data, new_time):
    fl = interp.interp1d((np.arange(0, len(data))), data, bounds_error=False)
    lnewy = np.linspace(0, len(data), new_time.shape[0])
    new_data = fl(lnewy)
    return new_data
#%%

AUXDAT_PATH = "/home/jmarchezi/research-projects/gic-statistics/auxData"
OUTPUT_PATH = "/data/output/gic_statistics/outputData"

#%%
stormList = pd.read_csv(f"{AUXDAT_PATH}/StormList2_manPhStart_NewBeginEnd.csv")
stormList.rename(columns={"Unnamed: 0": "stormNumber"}, inplace=True)
# %%
logs = open("log.txt", "a")
stormDmspData = []
probe = "f15"
for row in tqdm(stormList.iterrows()):
    
    initial_phase = pd.to_datetime(row[1].loc["new_begining_times"])
    main_phase = pd.to_datetime(row[1].loc["main_phase"])
    minimumSymH = pd.to_datetime(row[1].loc["minimumSymH"])
    end_rec_phase = pd.to_datetime(row[1].loc["new_ending_times"])
    
    year_range = [str(y) for y in range(initial_phase.year,end_rec_phase.year+1)]
    
    st = f"{initial_phase.year}_{row[1].loc['stormNumber']}"
    storm_number = row[1].loc['stormNumber']

    ifHSS = row[1].loc["ifHSS"]
    ifCME = row[1].loc["ifCME"]

    delta_t = end_rec_phase - initial_phase

    trange=[initial_phase.strftime("%Y-%m-%d"), end_rec_phase.strftime("%Y-%m-%d")] 
    paramLoadSat_ele = {"satellite": 'dmsp', "probe": probe,
                "instrument": 'ssj', "datatype": 'precipitating-electrons-ions'}

    flux_dmsp, time_dt_dmsp, colss = download_read_electron_data(trange, paramLoadSat_ele)

    paramLoadSat_plasma = {"satellite": 'dmsp', "probe": probe,
                "instrument": 'ssies', "datatype": 'thermal-plasma'}
    
    mlt_dmsp, mlat_dmsp, time_mlt_dmsp = download_read_plasma_data(trange, paramLoadSat_plasma)

    if flux_dmsp is not None and mlt_dmsp is not None:
        dfEnergy = pd.DataFrame(flux_dmsp, columns=colss, index=time_dt_dmsp)
        mlt_new = interpolate_cadence(mlt_dmsp, flux_dmsp)
        mlat_new = interpolate_cadence(mlat_dmsp, flux_dmsp)
        dfEnergy["mlt"] = mlt_new
        dfEnergy["mlat"] = mlat_new
        stormDmspData.append(dfEnergy)
    try:
        dmspData = pd.concat(stormDmspData)

        dmspData.reset_index(inplace=True)

        dmspData.to_feather(f'{OUTPUT_PATH}/{st}_Dmsp_{probe}_for_storms.feather')
            
        logs.write(f'{st} -- ok \n')
    except Exception as e:
        print(e)

        logs.write(f'{st} -- ERROR \n')
    gc.collect()
logs.close()
# %%

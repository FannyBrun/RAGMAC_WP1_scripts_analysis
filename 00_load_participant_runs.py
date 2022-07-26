# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:46:13 2020

@author: brunbarf
"""

import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
from osgeo import osr, gdal, gdalconst
gdal.UseExceptions()
from matplotlib import cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pickle
import datetime
import shutil
import os
import pandas as pd
from general_table import color_dic, dict_replacement, sensor_dic, marker_dic, RGI_dic
from table_participants_exp1 import dic_HEF, dic_ALE, dic_VES
from table_participants_exp2 import dic_BAL_period1, dic_BAL_period2,dic_NPI_period1, dic_NPI_period2

from function_plots import plot_volume_change_each_part, dh_dt_function_period, dh_dt_function_period_colored_sensor



list_keys = ['participant','run_id','glacier_id', 'run_code', 'S_km2', 'start_date_yyyy-mm-dd',
       'end_date_yyyy-mm-dd', 'method', 'dh_m', 'dh_sigma_m', 'dV_km3',
       'dV_sigma_km3', 'start_date', 'end_date', 'color', 'sensor']

list_keys = ['participant','run_id','glacier_id', 'run_code', 'S_km2', 'start_date_yyyy-mm-dd',
       'end_date_yyyy-mm-dd', 'dh_m', 'dh_sigma_m', 'dV_km3',
       'dV_sigma_km3', 'start_date', 'end_date', 'color', 'sensor','start_date_str', 'end_date_str']

path = 'C:/Users/brunbarf/Data/RAGMAC/WG1/'


### for Hinterheiferner
df_HEF = pd.DataFrame(columns=list_keys)
list_participants = list(dic_HEF.keys())
for participant in list_participants:
#    print(participant)
    for results_files in dic_HEF[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data = data.drop(data[np.isnan(data['dh_m'])].index)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')
        if participant == 'Validation':
            data['run_code'] = 'Validation'
        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'AST'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
            elif participant == 'Piermattei':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
                    
        else:
            data['sensor'] = sensor_dic[participant]
        
        df_HEF =  pd.concat([df_HEF, data[list_keys]])

df_HEF['delta_t'] = df_HEF['end_date'] - df_HEF['start_date']
df_HEF['dh_dt'] = df_HEF['dh_m']/df_HEF['delta_t'].dt.days*365.25
df_HEF['sigma_dh_dt'] = df_HEF['dh_sigma_m']/df_HEF['delta_t'].dt.days*365.25

df_HEF.index = range(len(df_HEF))

df_HEF[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_HEF.csv')

df_HEF.to_csv('table_HEF.csv')
with open('df_HEF.pkl', 'wb') as handle:
    pickle.dump(df_HEF, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
### for Aletsch group
list_participants = list(dic_ALE.keys())

df_ALE = pd.DataFrame(columns=list_keys)
for participant in list_participants:
#    print(participant)
    for results_files in dic_ALE[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')
        if participant == 'Validation':
            data['run_code'] = 'Validation'
        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'both'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
            elif participant == 'Piermattei':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
               
        else:
            data['sensor'] = sensor_dic[participant]
        df_ALE =  pd.concat([df_ALE, data[list_keys]])
df_ALE['delta_t'] = df_ALE['end_date'] - df_ALE['start_date']
df_ALE['dh_dt'] = df_ALE['dh_m']/df_ALE['delta_t'].dt.days*365.25
df_ALE.index = range(len(df_ALE))

df_ALE[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_ALE.csv')
df_ALE.to_csv('table_ALE.csv')

with open('df_ALE.pkl', 'wb') as handle:
    pickle.dump(df_ALE, handle, protocol=pickle.HIGHEST_PROTOCOL)



df_ALE_ALE =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01450']
df_ALE_ALE.index = range(len(df_ALE_ALE))
df_ALE_ISC =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01346']
df_ALE_ISC.index = range(len(df_ALE_ISC))
df_ALE_MIT =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01797']
df_ALE_MIT.index = range(len(df_ALE_MIT))
df_ALE_OBE =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01827']
df_ALE_OBE.index = range(len(df_ALE_OBE))
df_ALE_LAN =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01698']
df_ALE_LAN.index = range(len(df_ALE_LAN))


### for Vest group
list_participants = list(dic_VES.keys())

df_VES = pd.DataFrame(columns=list_keys)
for participant in list_participants:
#    print(participant)
    
    for results_files in dic_VES[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')
        if participant == 'Validation':
            data['run_code'] = 'Validation'
        if participant == 'Piermattei':
            data['dV_km3'] = data['dV_km3']/1000.
        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'both'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
            elif participant == 'Piermattei':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
               
        else:
            data['sensor'] = sensor_dic[participant]
        df_VES =  pd.concat([df_VES, data[list_keys]])
df_VES['delta_t'] = df_VES['end_date'] - df_VES['start_date']
df_VES['dh_dt'] = df_VES['dh_m']/df_VES['delta_t'].dt.days*365.25
df_VES.index = range(len(df_VES))

df_VES[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_VES.csv')
df_VES.to_csv('table_VES.csv')

with open('df_VES.pkl', 'wb') as handle:
    pickle.dump(df_VES, handle, protocol=pickle.HIGHEST_PROTOCOL)



df_VES_ENG =  df_VES[df_VES['glacier_id']=='RGI60-08.01657']
df_VES_ENG.index = range(len(df_VES_ENG))
df_VES_STN =  df_VES[df_VES['glacier_id']=='RGI60-08.00287']
df_VES_STN.index = range(len(df_VES_STN))
df_VES_STS =  df_VES[df_VES['glacier_id']=='RGI60-08.01641']
df_VES_STS.index = range(len(df_VES_STS))



### for Baltoro
df_BAL = pd.DataFrame(columns=list_keys)
list_participants = list(dic_BAL_period1.keys())

for participant in list_participants:
#    print(participant)
    for results_files in dic_BAL_period1[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data = data.drop(data[np.isnan(data['dh_m'])].index)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')

        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'AST'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
                   
        else:
            data['sensor'] = sensor_dic[participant]
        
        df_BAL =  pd.concat([df_BAL, data[list_keys]])
        
    for results_files in dic_BAL_period2[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data = data.drop(data[np.isnan(data['dh_m'])].index)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')

        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'AST'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
                   
        else:
            data['sensor'] = sensor_dic[participant]
        
        df_BAL =  pd.concat([df_BAL, data[list_keys]])
        


df_BAL['delta_t'] = df_BAL['end_date'] - df_BAL['start_date']
df_BAL['dh_dt'] = df_BAL['dh_m']/df_BAL['delta_t'].dt.days*365.25
df_BAL['sigma_dh_dt'] = df_BAL['dh_sigma_m']/df_BAL['delta_t'].dt.days*365.25

df_BAL.index = range(len(df_BAL))

df_BAL[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_BAL.csv')

df_BAL.to_csv('table_BAL.csv')

with open('df_BAL.pkl', 'wb') as handle:
    pickle.dump(df_BAL, handle, protocol=pickle.HIGHEST_PROTOCOL)




### for Baltoro
df_NPI = pd.DataFrame(columns=list_keys)
list_participants = list(dic_NPI_period1.keys())

for participant in list_participants:
#    print(participant)
    for results_files in dic_NPI_period1[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data = data.drop(data[np.isnan(data['dh_m'])].index)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')

        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'AST'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
                   
        else:
            data['sensor'] = sensor_dic[participant]
        
        df_NPI =  pd.concat([df_NPI, data[list_keys]])
        
    for results_files in dic_NPI_period2[participant]['path_results']:
        data = pd.read_csv(results_files)
#        print(results_files[61:])
        data.columns = data.columns.str.replace(' ', '')
        data = data.rename(columns=dict_replacement)
        data = data.drop(data[np.isnan(data['dh_m'])].index)
        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')

        data['run_id'] = participant + ' - ' + data['run_code']
        data['color'] = color_dic[participant]
        data['participant'] = participant
        
        if (data['run_id'] == 'Florentine - CTL').any():
            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
#        print(data['dh_m'])
        
        if sensor_dic[participant] == 'ask':
            if participant == 'Florentine':
                data['sensor'] = 'AST'
            elif participant == 'Sommer':
                if 'TDX' in results_files:
                    data['sensor'] = 'TDX'
                else:
                    data['sensor'] = 'AST'
                   
        else:
            data['sensor'] = sensor_dic[participant]
        
        df_NPI =  pd.concat([df_NPI, data[list_keys]])
        


df_NPI['delta_t'] = df_NPI['end_date'] - df_NPI['start_date']
df_NPI['dh_dt'] = df_NPI['dh_m']/df_NPI['delta_t'].dt.days*365.25
df_NPI['sigma_dh_dt'] = df_NPI['dh_sigma_m']/df_NPI['delta_t'].dt.days*365.25

df_NPI.index = range(len(df_NPI))

df_NPI[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_NPI.csv')

df_NPI.to_csv('table_NPI.csv')

with open('df_NPI.pkl', 'wb') as handle:
    pickle.dump(df_NPI, handle, protocol=pickle.HIGHEST_PROTOCOL)


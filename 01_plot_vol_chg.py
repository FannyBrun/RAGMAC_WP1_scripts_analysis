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
from function_plots import *
from function_stats import calculate_dist_to_val, append_seasonal_correction


path = 'C:/Users/brunbarf/Data/RAGMAC/WG1/'

ice_dens = 0.85 #Huss 2013

#### for Hinterheiferner
df_HEF = pickle.load(open('df_HEF.pkl', "rb" ))
plot_volume_change_each_part(df_HEF, 'HEF')
dh_dt_function_period(df_HEF,
                      'HEF',
                      datetime.datetime(2010, 10, 8),
                      datetime.datetime(2019, 9, 21))

dh_dt_function_period_colored_sensor(df_HEF,
                      'HEF',
                      datetime.datetime(2010, 10, 8),
                      datetime.datetime(2019, 9, 21))

path_csv_seas_cor = path + 'EXP1_from_participants/temporal_correction/list_HEF_corr_bias_corrections_FB.csv'
df_HEF = append_seasonal_correction(df_HEF, path_csv_seas_cor)
df_HEF = calculate_dist_to_val(df_HEF)

plot_diff_to_ref_function_uncert(df_HEF, 'HEF')
plot_diff_to_ref_function_seasonal_correction(df_HEF, 'HEF')
plot_diff_to_ref_before_and_after_seasonal_correction(df_HEF, 'HEF')

plt.close('all')


#### for Aletsch group
df_ALE = pickle.load(open('df_ALE.pkl', "rb" ))
path_csv_seas_cor = path + 'EXP1_from_participants/temporal_correction/list_ALE_bias_corrections.csv'
df_ALE = append_seasonal_correction(df_ALE, path_csv_seas_cor)

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

df_ALE_ALE = calculate_dist_to_val(df_ALE_ALE)

dict_df_ALE = {'ALE' : df_ALE_ALE,
               'ISC' : df_ALE_ISC,
               'MIT' : df_ALE_MIT,
               'OBE' : df_ALE_OBE,
               'LAN' : df_ALE_LAN}

for ref in list(dict_df_ALE.keys()):
    dict_df_ALE[ref] = calculate_dist_to_val(dict_df_ALE[ref])
    plot_volume_change_each_part(dict_df_ALE[ref], ref)
    dh_dt_function_period(dict_df_ALE[ref], ref,datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
    dh_dt_function_period_colored_sensor(dict_df_ALE[ref], ref,datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
    plot_diff_to_ref_function_uncert(dict_df_ALE[ref],ref)
    if ref == 'ALE':
        plot_diff_to_ref_function_seasonal_correction(dict_df_ALE[ref], ref)
        plot_diff_to_ref_before_and_after_seasonal_correction(dict_df_ALE[ref], ref)

plt.close('all')

#### for Vest group
df_VES = pickle.load(open('df_VES.pkl', "rb" ))

df_VES_ENG =  df_VES[df_VES['glacier_id']=='RGI60-08.01657']
df_VES_ENG.index = range(len(df_VES_ENG))
df_VES_STN =  df_VES[df_VES['glacier_id']=='RGI60-08.00287']
df_VES_STN.index = range(len(df_VES_STN))
df_VES_STS =  df_VES[df_VES['glacier_id']=='RGI60-08.01641']
df_VES_STS.index = range(len(df_VES_STS))

dict_df_VES = {'ENG' : df_VES_ENG,
               'STN' : df_VES_STN,
               'STS' : df_VES_STS
               }

for ref in list(dict_df_VES.keys()):
    dict_df_VES[ref] = calculate_dist_to_val(dict_df_VES[ref])
    plot_volume_change_each_part(dict_df_VES[ref], ref)
    dh_dt_function_period(dict_df_VES[ref], ref,datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))
    dh_dt_function_period_colored_sensor(dict_df_VES[ref], ref,datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))
    plot_diff_to_ref_function_uncert(dict_df_VES[ref],ref)

plt.close('all')


#### for Baltoro group
df_BAL = pickle.load(open('df_BAL.pkl', "rb" ))
df_BAL_BAL =  df_BAL[df_BAL['glacier_id']=='RGI60-14.06794']
df_BAL_BAL.index = range(len(df_BAL_BAL))

df_BAL_BAL_per1 = df_BAL_BAL[df_BAL_BAL['period']=='period1']
df_BAL_BAL_per1.index = range(len(df_BAL_BAL_per1))
plot_volume_change_each_part(df_BAL_BAL_per1, 'BAL_period1')

df_BAL_BAL_per2 = df_BAL_BAL[df_BAL_BAL['period']=='period2']
df_BAL_BAL_per2.index = range(len(df_BAL_BAL_per2))
plot_volume_change_each_part(df_BAL_BAL_per2, 'BAL_period2')

#plot_volume_change_each_part(df_BAL_BAL, 'BAL')
dh_dt_function_period(df_BAL_BAL, 'BAL')
dh_dt_function_period_colored_sensor(df_BAL_BAL, 'BAL')
plt.close('all')


#plot_volume_change_each_part(df_BAL_BAL[ref], ref)

#
##### plots all glaciers together
fig, ax = plt.subplots()
ax.boxplot([df_HEF['dV_km3'],
            df_ALE_ALE['dV_km3'],
            df_ALE_ISC['dV_km3'],
            df_ALE_MIT['dV_km3'], 
            df_ALE_OBE['dV_km3'], 
            df_ALE_LAN['dV_km3'],
            df_VES_ENG['dV_km3'], 
            df_VES_STN['dV_km3'], 
            df_VES_STS['dV_km3']])
ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN'])
plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
plt.ylabel('Volume change [km$^3$]')
plt.savefig('boxplots_vol_chg.png',
            dpi = 300,
            bbox_inches = 'tight')


fig, ax = plt.subplots()
ax.boxplot([df_HEF['dh_m'],
            df_ALE_ALE['dh_m'],
            df_ALE_ISC['dh_m'],
            df_ALE_MIT['dh_m'], 
            df_ALE_OBE['dh_m'], 
            df_ALE_LAN['dh_m'],
            df_VES_ENG['dh_m'], 
            df_VES_STN['dh_m'], 
            df_VES_STS['dh_m']
            ])
ax.plot(1,df_HEF['dh_m'][df_HEF['participant']=="Validation"],'ko')
ax.plot(2,df_ALE_ALE['dh_m'][df_ALE_ALE['participant']=="Validation"],'ko')
ax.plot(3,df_ALE_ISC['dh_m'][df_ALE_ISC['participant']=="Validation"],'ko')
ax.plot(4,df_ALE_MIT['dh_m'][df_ALE_MIT['participant']=="Validation"],'ko')
ax.plot(5,df_ALE_OBE['dh_m'][df_ALE_OBE['participant']=="Validation"],'ko')
ax.plot(6,df_ALE_LAN['dh_m'][df_ALE_LAN['participant']=="Validation"],'ko')
ax.plot(7,df_VES_ENG['dh_m'][df_VES_ENG['participant']=="Validation"],'ko')
ax.plot(8,df_VES_STN['dh_m'][df_VES_STN['participant']=="Validation"],'ko')
ax.plot(9,df_VES_STS['dh_m'][df_VES_STS['participant']=="Validation"],'ko')

ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
plt.ylabel('Mean dh [m]')
plt.savefig('boxplots_dh.png',
            dpi = 300,
            bbox_inches = 'tight')
#
fig, ax = plt.subplots()
ax.boxplot([df_HEF['dh_dt'], 
            df_ALE_ALE['dh_dt'], 
            df_ALE_ISC['dh_dt'], 
            df_ALE_MIT['dh_dt'], 
            df_ALE_OBE['dh_dt'], 
            df_ALE_LAN['dh_dt'],
            df_VES_ENG['dh_dt'], 
            df_VES_STN['dh_dt'], 
            df_VES_STS['dh_dt']
            ])
ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
plt.ylabel('Mean dh/dt [m/yr]')
plt.savefig('boxplots_dh_dt.png',
            dpi = 300,
            bbox_inches = 'tight')


fig, ax = plt.subplots()
ax.boxplot([df_HEF['dh_sigma_m'],
            df_ALE_ALE['dh_sigma_m'],
            df_ALE_ISC['dh_sigma_m'],
            df_ALE_MIT['dh_sigma_m'],
            df_ALE_OBE['dh_sigma_m'],
            df_ALE_LAN['dh_sigma_m'],
            df_VES_ENG['dh_sigma_m'],
            df_VES_STN['dh_sigma_m'],
            df_VES_STS['dh_sigma_m']])

ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
#plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
plt.ylabel('$\sigma$ dh [m]')
plt.savefig('boxplots_sigma_dh.png',
            dpi = 300,
            bbox_inches = 'tight')

plt.close('all')

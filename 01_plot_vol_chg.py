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
from function_plots import plot_volume_change_each_part, dh_dt_function_period, dh_dt_function_period_colored_sensor
from function_stats import calculate_dist_to_val


path = 'C:/Users/brunbarf/Data/RAGMAC/WG1/'



#### for Hinterheiferner
df_HEF = pickle.load(open('df_HEF.pkl', "rb" ))
plot_volume_change_each_part(df_HEF, 'HEF')
dh_dt_function_period(df_HEF,
                      'HEF',
                      datetime.datetime(2010, 10, 8),
                      datetime.datetime(2019, 9, 21))

df_HEF = calculate_dist_to_val(df_HEF)

#
##### for Aletsch group
#df_ALE = pickle.load(open('df_ALE.pkl', "rb" ))
#
#df_ALE_ALE =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01450']
#df_ALE_ALE.index = range(len(df_ALE_ALE))
#df_ALE_ISC =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01346']
#df_ALE_ISC.index = range(len(df_ALE_ISC))
#df_ALE_MIT =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01797']
#df_ALE_MIT.index = range(len(df_ALE_MIT))
#df_ALE_OBE =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01827']
#df_ALE_OBE.index = range(len(df_ALE_OBE))
#df_ALE_LAN =  df_ALE[df_ALE['glacier_id']=='RGI60-11.01698']
#df_ALE_LAN.index = range(len(df_ALE_LAN))
#
#dh_dt_function_period(df_ALE_ALE, 'ALE',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#dh_dt_function_period(df_ALE_ISC, 'ISC',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#dh_dt_function_period(df_ALE_MIT, 'MIT',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#dh_dt_function_period(df_ALE_OBE, 'OBE',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#dh_dt_function_period(df_ALE_LAN, 'LAN',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#

#### for Vest group
#list_participants = list(dic_VES.keys())
#
#df_VES = pd.DataFrame(columns=list_keys)
#for participant in list_participants:
#    print(participant)
#    for results_files in dic_VES[participant]['path_results']:
#        data = pd.read_csv(results_files)
#        data.columns = data.columns.str.replace(' ', '')
#        data = data.rename(columns=dict_replacement)
#        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
#        data['start_date_str'] = data['start_date'].dt.strftime('%Y-%m-%d')
#        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
#        data['end_date_str'] = data['end_date'].dt.strftime('%Y-%m-%d')
#        if participant == 'Validation':
#            data['run_code'] = 'Validation'
#        if participant == 'Piermattei':
#            data['dV_km3'] = data['dV_km3']/1000.
#        data['run_id'] = participant + ' - ' + data['run_code']
#        data['color'] = color_dic[participant]
#        data['participant'] = participant
#        
#        if (data['run_id'] == 'Florentine - CTL').any():
#            data['dV_km3'] = data['dh_m']*data['S_km2']*1e-3
#            data['dV_sigma_km3'] = data['dh_sigma_m']*data['S_km2']*1e-3
##        print(data['dh_m'])
#        
#        if sensor_dic[participant] == 'ask':
#            if participant == 'Florentine':
#                data['sensor'] = 'both'
#            elif participant == 'Sommer':
#                if 'TDX' in results_files:
#                    data['sensor'] = 'TDX'
#                else:
#                    data['sensor'] = 'AST'
#            elif participant == 'Piermattei':
#                if 'TDX' in results_files:
#                    data['sensor'] = 'TDX'
#                else:
#                    data['sensor'] = 'AST'
#               
#        else:
#            data['sensor'] = sensor_dic[participant]
#        df_VES =  pd.concat([df_VES, data[list_keys]])
#df_VES['delta_t'] = df_VES['end_date'] - df_VES['start_date']
#df_VES['dh_dt'] = df_VES['dh_m']/df_VES['delta_t'].dt.days*365.25
#df_VES.index = range(len(df_VES))
#
#df_VES[['run_id', 'glacier_id','start_date_str', 'end_date_str']].to_csv('list_VES.csv')
#
#
#df_VES_ENG =  df_VES[df_VES['glacier_id']=='RGI60-08.01657']
#df_VES_ENG.index = range(len(df_VES_ENG))
#df_VES_STN =  df_VES[df_VES['glacier_id']=='RGI60-08.00287']
#df_VES_STN.index = range(len(df_VES_STN))
#df_VES_STS =  df_VES[df_VES['glacier_id']=='RGI60-08.01641']
#df_VES_STS.index = range(len(df_VES_STS))
#
#
#
##plot_volume_change_each_part(df_HEF, 'HEF')
##plot_volume_change_each_part(df_VES_ENG, 'ENG')
##plot_volume_change_each_part(df_VES_STN, 'STN')
##plot_volume_change_each_part(df_VES_STS, 'STS')
##plot_volume_change_each_part(df_ALE_ALE, 'ALE')
##plot_volume_change_each_part(df_ALE_ISC, 'ISC')
##plot_volume_change_each_part(df_ALE_MIT, 'MIT')
##plot_volume_change_each_part(df_ALE_OBE, 'OBE')
##plot_volume_change_each_part(df_ALE_LAN, 'LAN')
##
##
##dh_dt_function_period(df_HEF, 'HEF',datetime.datetime(2010, 10, 8),datetime.datetime(2019, 9, 21))
##dh_dt_function_period(df_VES_ENG, 'ENG',datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))
##dh_dt_function_period(df_VES_STN, 'STN',datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))
##dh_dt_function_period(df_VES_STS, 'STS',datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))
##dh_dt_function_period(df_ALE_ALE, 'ALE',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
##dh_dt_function_period(df_ALE_ISC, 'ISC',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
##dh_dt_function_period(df_ALE_MIT, 'MIT',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
##dh_dt_function_period(df_ALE_OBE, 'OBE',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
##dh_dt_function_period(df_ALE_LAN, 'LAN',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
##
##
##
#dh_dt_function_period_colored_sensor(df_HEF, 'HEF',datetime.datetime(2010, 10, 8),datetime.datetime(2019, 9, 21))
#dh_dt_function_period_colored_sensor(df_ALE_ALE, 'ALE',datetime.datetime(2011, 9, 13),datetime.datetime(2017, 9, 21))
#dh_dt_function_period_colored_sensor(df_VES_ENG, 'ENG',datetime.datetime(2008, 9, 2),datetime.datetime(2020, 8, 10))

#
###### plots all glaciers together
#fig, ax = plt.subplots()
#ax.boxplot([df_HEF['dV_km3'],
#            df_ALE_ALE['dV_km3'],
#            df_ALE_ISC['dV_km3'],
#            df_ALE_MIT['dV_km3'], 
#            df_ALE_OBE['dV_km3'], 
#            df_ALE_LAN['dV_km3'],
#            df_VES_ENG['dV_km3'], 
#            df_VES_STN['dV_km3'], 
#            df_VES_STS['dV_km3']])
#ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN'])
#plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
#plt.ylabel('Volume change [km$^3$]')
#plt.savefig('boxplots_vol_chg.png',
#            dpi = 300,
#            bbox_inches = 'tight')
#
#
#fig, ax = plt.subplots()
#ax.boxplot([df_HEF['dh_m'],
#            df_ALE_ALE['dh_m'],
#            df_ALE_ISC['dh_m'],
#            df_ALE_MIT['dh_m'], 
#            df_ALE_OBE['dh_m'], 
#            df_ALE_LAN['dh_m'],
#            df_VES_ENG['dh_m'], 
#            df_VES_STN['dh_m'], 
#            df_VES_STS['dh_m']
#            ])
#ax.plot(1,df_HEF['dh_m'][df_HEF['participant']=="Validation"],'ko')
#ax.plot(2,df_ALE_ALE['dh_m'][df_ALE_ALE['participant']=="Validation"],'ko')
#ax.plot(3,df_ALE_ISC['dh_m'][df_ALE_ISC['participant']=="Validation"],'ko')
#ax.plot(4,df_ALE_MIT['dh_m'][df_ALE_MIT['participant']=="Validation"],'ko')
#ax.plot(5,df_ALE_OBE['dh_m'][df_ALE_OBE['participant']=="Validation"],'ko')
#ax.plot(6,df_ALE_LAN['dh_m'][df_ALE_LAN['participant']=="Validation"],'ko')
#ax.plot(7,df_VES_ENG['dh_m'][df_VES_ENG['participant']=="Validation"],'ko')
#ax.plot(8,df_VES_STN['dh_m'][df_VES_STN['participant']=="Validation"],'ko')
#ax.plot(9,df_VES_STS['dh_m'][df_VES_STS['participant']=="Validation"],'ko')
#
#ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
#plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
#plt.ylabel('Mean dh [m]')
#plt.savefig('boxplots_dh.png',
#            dpi = 300,
#            bbox_inches = 'tight')
##
#fig, ax = plt.subplots()
#ax.boxplot([df_HEF['dh_dt'], 
#            df_ALE_ALE['dh_dt'], 
#            df_ALE_ISC['dh_dt'], 
#            df_ALE_MIT['dh_dt'], 
#            df_ALE_OBE['dh_dt'], 
#            df_ALE_LAN['dh_dt'],
#            df_VES_ENG['dh_dt'], 
#            df_VES_STN['dh_dt'], 
#            df_VES_STS['dh_dt']
#            ])
#ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
#plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
#plt.ylabel('Mean dh/dt [m/yr]')
#plt.savefig('boxplots_dh_dt.png',
#            dpi = 300,
#            bbox_inches = 'tight')
#
#
#fig, ax = plt.subplots()
#ax.boxplot([df_HEF['dh_sigma_m'],
#            df_ALE_ALE['dh_sigma_m'],
#            df_ALE_ISC['dh_sigma_m'],
#            df_ALE_MIT['dh_sigma_m'],
#            df_ALE_OBE['dh_sigma_m'],
#            df_ALE_LAN['dh_sigma_m'],
#            df_VES_ENG['dh_sigma_m'],
#            df_VES_STN['dh_sigma_m'],
#            df_VES_STS['dh_sigma_m']])
#
#ax.set_xticklabels(['HEF', 'ALE', 'ISC', 'MIT', 'OBE', 'LAN', 'ENG', 'STN', 'STS'])
##plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
#plt.ylabel('$\sigma$ dh [m]')
#plt.savefig('boxplots_sigma_dh.png',
#            dpi = 300,
#            bbox_inches = 'tight')
#
#
#
##plt.figure(figsize = (6,5))
##for i in range(len(df_HEF)):
##    plt.plot([df_HEF['start_date'][i],df_HEF['end_date'][i]], [df_HEF['dh_dt'][i],df_HEF['dh_dt'][i]], color = df_HEF['color'][i])
##    plt.scatter([df_HEF['start_date'][i],df_HEF['end_date'][i]],
##            [df_HEF['dh_dt'][i],df_HEF['dh_dt'][i]],
###            s = 4,
##            marker = '|',
##            c = [df_HEF['color'][i], df_HEF['color'][i]]
##            )
##    plt.axvline(datetime.datetime(2010, 10, 8), lw = 1, color = 'k', ls = 'dashed')
##    plt.axvline(datetime.datetime(2019, 9, 21), lw = 1, color = 'k', ls = 'dashed')
##plt.ylim(-3,0)
##plt.title('HEF')
##plt.xlabel('Time')
##plt.ylabel('Mean dh/dt [m/yr]')
##plt.savefig('HEF_mean_dh_dt.png',
##            dpi = 300,
##            bbox_inches = 'tight')
##
##
##plt.figure(figsize = (6,5))
##for i in list(df_ALE_ALE.index):
##    plt.plot([df_ALE_ALE['start_date'][i],df_ALE_ALE['end_date'][i]], [df_ALE_ALE['dh_dt'][i],df_ALE_ALE['dh_dt'][i]], color = df_ALE_ALE['color'][i])
##    plt.scatter([df_ALE_ALE['start_date'][i],df_ALE_ALE['end_date'][i]],
##            [df_ALE_ALE['dh_dt'][i],df_ALE_ALE['dh_dt'][i]],
###            s = 4,
##            marker = '|',
##            c = [df_ALE_ALE['color'][i], df_ALE_ALE['color'][i]]
##            )
##    plt.axvline(datetime.datetime(2011, 9, 13), lw = 1, color = 'k', ls = 'dashed')
##    plt.axvline(datetime.datetime(2017, 9, 21), lw = 1, color = 'k', ls = 'dashed')
##plt.ylim(-3,0)
##plt.title('ALE')
##plt.xlabel('Time')
##plt.ylabel('Mean dh/dt [m/yr]')
##plt.savefig('ALE_mean_dh_dt.png',
##            dpi = 300,
##            bbox_inches = 'tight')
#
#
##plt.figure(figsize = (6,5))
##for i in list(df_ALE_ALE.index):
##    plt.plot([df_ALE_ALE['start_date'][i],df_ALE_ALE['end_date'][i]], [df_ALE_ALE['dh_dt'][i],df_ALE_ALE['dh_dt'][i]], color = df_ALE_ALE['color'][i])
##    plt.scatter([df_ALE_ALE['start_date'][i],df_ALE_ALE['end_date'][i]],
##            [df_ALE_ALE['dh_dt'][i],df_ALE_ALE['dh_dt'][i]],
###            s = 4,
##            marker = '|',
##            c = [df_ALE_ALE['color'][i], df_ALE_ALE['color'][i]]
##            )
##    plt.axvline(datetime.datetime(2011, 9, 13), lw = 1, color = 'k', ls = 'dashed')
##    plt.axvline(datetime.datetime(2017, 9, 21), lw = 1, color = 'k', ls = 'dashed')
##plt.ylim(-3,0)
##plt.title('ALE')
##plt.xlabel('Time')
##plt.ylabel('Mean dh/dt [m/yr]')
##plt.savefig('ALE_mean_dh_dt.png',
##            dpi = 300,
##            bbox_inches = 'tight')
##
##
##
##
##
##plt.figure(figsize = (6,5))
##for i in range(len(df_VES_ENG)):
##    plt.plot([df_VES_ENG['start_date'][i],df_VES_ENG['end_date'][i]], [df_VES_ENG['dh_dt'][i],df_VES_ENG['dh_dt'][i]], color = df_VES_ENG['color'][i])
##    plt.scatter([df_VES_ENG['start_date'][i],df_VES_ENG['end_date'][i]],
##            [df_VES_ENG['dh_dt'][i],df_VES_ENG['dh_dt'][i]],
###            s = 4,
##            marker = '|',
##            c = [df_VES_ENG['color'][i], df_VES_ENG['color'][i]]
##            )
##    plt.axvline(datetime.datetime(2008, 9, 2), lw = 1, color = 'k', ls = 'dashed')
##    plt.axvline(datetime.datetime(2020, 8, 10), lw = 1, color = 'k', ls = 'dashed')
##plt.ylim(-3,0)
##plt.title('ENG')
##plt.xlabel('Time')
##plt.ylabel('Mean dh/dt [m/yr]')
##plt.savefig('ENG_mean_dh_dt.png',
##            dpi = 300,
##            bbox_inches = 'tight')
##
##
##plt.figure(figsize = (6,5))
##for i in range(len(df_VES_STN)):
##    plt.plot([df_VES_STN['start_date'][i],df_VES_STN['end_date'][i]], [df_VES_STN['dh_dt'][i],df_VES_STN['dh_dt'][i]], color = df_VES_STN['color'][i])
##    plt.scatter([df_VES_STN['start_date'][i],df_VES_STN['end_date'][i]],
##            [df_VES_STN['dh_dt'][i],df_VES_STN['dh_dt'][i]],
###            s = 4,
##            marker = '|',
##            c = [df_VES_STN['color'][i], df_VES_STN['color'][i]]
##            )
##    plt.axvline(datetime.datetime(2008, 9, 2), lw = 1, color = 'k', ls = 'dashed')
##    plt.axvline(datetime.datetime(2020, 8, 10), lw = 1, color = 'k', ls = 'dashed')
##plt.ylim(-3,0)
##plt.title('STN')
##plt.xlabel('Time')
##plt.ylabel('Mean dh/dt [m/yr]')
##plt.savefig('STN_mean_dh_dt.png',
##            dpi = 300,
##            bbox_inches = 'tight')
#

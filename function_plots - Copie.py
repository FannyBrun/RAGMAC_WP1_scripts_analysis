# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 09:06:58 2022

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

def plot_volume_change_each_part(df_GLA, ref):
    fig, ax = plt.subplots()
    for i in range(len(df_GLA)):
        plt.scatter(i,
                df_GLA['dV_km3'][i],
    #            s = 4,
                marker = marker_dic[df_GLA['sensor'][i]],
                c = df_GLA['color'][i]
                )
        
        plt.scatter([i,i],
                [df_GLA['dV_km3'][i]-df_GLA['dV_sigma_km3'][i], df_GLA['dV_km3'][i]+df_GLA['dV_sigma_km3'][i]],
    #            s = 4,
                marker = '+',
                c = [df_GLA['color'][i],df_GLA['color'][i]]
                )
    plt.axhline(0, lw = 1, color = 'k', ls = 'dashed')
    plt.axhline(float(df_GLA[df_GLA['participant']=='Validation']['dV_km3']), lw = 1, color = 'k', ls = ':', zorder = 0)
    plt.title(ref)
    ax.set_xticklabels([])
    plt.ylabel('Volume change [km$^3$]')
    plt.savefig('volume_change_each_part_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')
    

def dh_dt_function_period(df_GLA, ref, start_date, end_date): 
    plt.figure(figsize = (6,5))
    for i in range(len(df_GLA)):
        if df_GLA['participant'][i] == 'Validation':
            plt.plot([df_GLA['start_date'][i],df_GLA['end_date'][i]], [df_GLA['dh_dt'][i],df_GLA['dh_dt'][i]], color = df_GLA['color'][i], lw = 2)
        else:
            plt.plot([df_GLA['start_date'][i],df_GLA['end_date'][i]], [df_GLA['dh_dt'][i],df_GLA['dh_dt'][i]], color = df_GLA['color'][i])

        plt.scatter([df_GLA['start_date'][i],df_GLA['end_date'][i]],
                [df_GLA['dh_dt'][i],df_GLA['dh_dt'][i]],
    #            s = 4,
                marker = '|',
                c = [df_GLA['color'][i], df_GLA['color'][i]]
                )
        plt.axvline(start_date, lw = 1, color = 'k', ls = 'dashed')
        plt.axvline(end_date, lw = 1, color = 'k', ls = 'dashed')
    plt.ylim(-3,0)
    plt.title(ref)
    plt.xlabel('Time')
    plt.ylabel('Mean dh/dt [m/yr]')
    plt.savefig('mean_dh_dt_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')
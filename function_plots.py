# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 09:06:58 2022

@author: brunbarf
"""
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
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
from general_table import color_dic, dict_replacement, sensor_dic, marker_dic, RGI_dic, marker_to_color_dic
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
    if len(df_GLA[df_GLA['participant']=='Validation']['dV_km3'])>0:
        plt.axhline(float(df_GLA[df_GLA['participant']=='Validation']['dV_km3']), lw = 1, color = 'k', ls = ':', zorder = 0)
    plt.title(ref)
    ax.set_xticklabels([])
    plt.ylabel('Volume change [km$^3$]')
    plt.savefig('figures/volume_change_each_part_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')


def plot_diff_to_ref_function_uncert(df_GLA, ref):
    fig, ax = plt.subplots()
    for i in range(len(df_GLA)):
        plt.scatter(df_GLA['dh_sigma_m'][i],
                np.abs(df_GLA['diff_val_percent'][i]),
                marker = marker_dic[df_GLA['sensor'][i]],
                c = marker_to_color_dic[df_GLA['sensor'][i]]
#                c = df_GLA['color'][i]
                )

    plt.title(ref)
    plt.xlabel('Uncertainty [m]')
    plt.ylabel('Absolute value of distance to validation [%]')
    plt.savefig('figures/diff_to_ref_function_uncert_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')
    
    
def plot_diff_to_ref_function_seasonal_correction(df_GLA, ref):
    fig, ax = plt.subplots()
    for i in range(len(df_GLA)):
        plt.scatter(df_GLA['seas_corr_mwe'][i],
                df_GLA['diff_val_m'][i],
                marker = marker_dic[df_GLA['sensor'][i]],
                c = marker_to_color_dic[df_GLA['sensor'][i]]
#                c = df_GLA['color'][i]
                )

    plt.title(ref)
#    ax.set_xticklabels([])
    plt.xlabel('Seasonal correction [m w.e.]')
    plt.ylabel('Distance to validation [m]')
    plt.savefig('figures/diff_to_ref_function_seas_corr_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')

def plot_diff_to_ref_before_and_after_seasonal_correction(df_GLA, ref):
    df_GLA = df_GLA.sort_values(by=['sensor'])
    df_GLA.drop(df_GLA.index[df_GLA['participant'] == 'Validation'], inplace = True)
    df_GLA = df_GLA.reset_index(drop=True)
    fig, ax = plt.subplots()
    for i in range(len(df_GLA)):
        ax.scatter(i,
                df_GLA['diff_val_after_seas_corr_percent'][i],
                s = 75,
                marker = "o",
                fc = 'white',
                ec = marker_to_color_dic[df_GLA['sensor'][i]],
                linewidths = 1,
                label = 'after correction'
                )
        ax.scatter([i],
                df_GLA['diff_val_percent'][i],
                marker = ".",
#                marker = marker_dic[df_GLA['sensor'][i]],
#                c = 'tab:red',
                c = marker_to_color_dic[df_GLA['sensor'][i]],
#                c = 'k',
                label = 'before correction'
                )

    ax.axhline(0, lw = 1, color = 'k', ls = 'dashed')
    plt.title(ref)
    ax.set_xticklabels([])
    legend_elements = [Line2D([0], [0], marker='.', color='k',lw = 0, label='before correction'),
                       Line2D([0], [0], marker='o', color='white', label='after correction',
                              markeredgecolor='k', markersize=10)]
    ax.legend(handles=legend_elements, loc='best')
    plt.ylabel('Absolute value of distance to validation [%]')
    plt.savefig('figures/diff_to_ref_before_and_after_seasonal_correction_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')
    
    

def dh_dt_function_period(df_GLA, ref, start_date = None, end_date = None): 
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
    if start_date is not None:
        plt.axvline(start_date, lw =  1, color = 'grey', ls = 'dashed')
    if end_date is not None:
        plt.axvline(end_date, lw =  1, color = 'grey', ls = 'dashed')
    plt.axhline(0, lw =  0.5, color = 'k', ls = 'dashed')

#    plt.ylim(-3,0)
    plt.title(ref)
    plt.xlabel('Time')
    plt.ylabel('Mean dh/dt [m/yr]')
    plt.savefig('figures/mean_dh_dt_'+ref+'.png',
                dpi = 300,
                bbox_inches = 'tight')
    

    
    
def dh_dt_function_period_colored_sensor(df_GLA, ref, start_date = None, end_date = None): 
    fig, ax = plt.subplots(figsize = (6,5))
    for i in range(len(df_GLA)):
        if df_GLA['participant'][i] == 'Validation':
            plt.plot([df_GLA['start_date'][i],df_GLA['end_date'][i]], [df_GLA['dh_dt'][i],df_GLA['dh_dt'][i]], color = df_GLA['color'][i], lw = 2)
        else:
            plt.plot([df_GLA['start_date'][i],df_GLA['end_date'][i]],
                     [df_GLA['dh_dt'][i],
                     df_GLA['dh_dt'][i]],
                     color = marker_to_color_dic[df_GLA['sensor'][i]])

        plt.scatter([df_GLA['start_date'][i],df_GLA['end_date'][i]],
                [df_GLA['dh_dt'][i],df_GLA['dh_dt'][i]],
    #            s = 4,
                marker = '|',
                c = [marker_to_color_dic[df_GLA['sensor'][i]],marker_to_color_dic[df_GLA['sensor'][i]]]
                )
    if start_date is not None:
        plt.axvline(start_date, lw =  1, color = 'grey', ls = 'dashed')
    if end_date is not None:
        plt.axvline(end_date, lw =  1, color = 'grey', ls = 'dashed')
    plt.axhline(0, lw =  0.5, color = 'k', ls = 'dashed')
    legend_elements = [Line2D([0], [0], color=marker_to_color_dic['Ref'],lw = 2, label='Validation'),
                   Line2D([0], [0], color=marker_to_color_dic['AST'], label='AST'),
                   Line2D([0], [0], color=marker_to_color_dic['TDX'], label='TDX'),
                   Line2D([0], [0], color=marker_to_color_dic['both'], label='both')]
    ax.legend(handles=legend_elements, loc='best')
#    plt.ylim(-2.5,0.5)
    plt.title(ref)
    plt.xlabel('Time')
    plt.ylabel('Mean dh/dt [m/yr]')
    plt.savefig('figures/mean_dh_dt_'+ref+'_poster_LPS.png',
                dpi = 300,
                bbox_inches = 'tight')
    
    
    
    
    
    
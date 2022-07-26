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
from general_table import color_dic, dict_replacement, sensor_dic, marker_dic, RGI_dic, marker_to_color_dic
from table_participants_exp1 import dic_HEF, dic_ALE, dic_VES

def calculate_dist_to_val(df_GLA):
    val = df_GLA['dh_m'][df_GLA['participant']=='Validation']
    df_GLA['diff_val_m'] = df_GLA['dh_m'] - float(val)
    df_GLA['diff_val_percent'] = df_GLA['diff_val_m']/float(val)*100
    
    return df_GLA
    
    
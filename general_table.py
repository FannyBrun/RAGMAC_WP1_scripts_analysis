# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 08:46:13 2020

@author: brunbarf
"""

import matplotlib as mpl
import matplotlib.colors as mcolors
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
from matplotlib import colors


path = 'C:/Users/brunbarf/Data/RAGMAC/WG1/'

list_participants = ['Belart',
          'Berthier',
          'Dehecq',
          'Dussaillant',
          'Florentine',
          'Hugonnet',
          'Krieger',
          'Piermattei',
          'Sommer',
          'Wendt',
          'Bolch',
          'LaFernierre'
          ]

colors_part =  plt.cm.tab20( np.arange(len(list_participants)))
#plt.scatter(np.arange(len(list_participants)),np.ones(len(list_participants)), c=colors_part, s=180)
#plt.show()

#color_dic = {}
#for participant,i in zip(list_participants, range(len(list_participants))):
#    color_dic[participant] = colors_part[i]

color_dic = {'Belart': 'tab:blue',
          'Berthier' : 'tab:orange',
          'Dehecq' : 'tab:green',
          'Dussaillant' : 'tab:red',
          'Florentine' : 'tab:purple',
          'Hugonnet' : 'tab:brown',
          'Krieger' : 'tab:pink',
          'Piermattei' : 'tab:grey',
          'Sommer' : 'tab:olive',
          'Wendt' : 'tab:cyan',
          'Bolch' : 'blue',
          'LeFernierre' : 'red',
          'Validation' : 'k'
          }

sensor_dic = {'Belart': 'AST',
          'Berthier' : 'AST',
          'Dehecq' : 'AST',
          'Dussaillant' : 'AST',
          'Florentine' : 'ask',
          'Hugonnet' : 'AST',
          'Krieger' : 'TDX',
          'Piermattei' : 'ask',
          'Sommer' : 'ask',
          'Wendt' : 'TDX',
          'Bolch' : 'AST',
          'LeFernierre' : 'TDX',
          'Validation' : 'Ref'
          }

RGI_dic = {'RGI60-11.00897' : 'HEF',
           'RGI60-11.01450': 'ALE',
           'RGI60-11.01346' : 'ISC', #Ischmeer
           'RGI60-11.01797' : 'MIT', #Mittlealetsch
           'RGI60-11.01827' : 'OBE', #Oberaltealetsch
           'RGI60-11.01698' : 'LAN', #Langgletscher
           'RGI60-08.01346' : 'ENG', #Engebreen
           'RGI60-08.00287' : 'STN', #Storglombreen_N
           'RGI60-08.01641' : 'STS' #Storglombreen_S
               } 

marker_to_color_dic = {'AST': 'tab:blue',
              'TDX': 'tab:orange',
              'both' : 'tab:green',
              'Ref' : 'k'}


marker_dic = {'AST': 'o',
              'TDX': 'd',
              'both' : 's',
              'Ref' : 'D'}


dict_replacement = {'RunCode':'run_code',
                    'StartDateSensor_DD/MM/YYYY': 'StartDateSensor_yyyy-mm-dd',
                    'EndDateSensor_DD/MM/YYYY': 'EndDateSensor_yyyy-mm-dd',
                    'start_date_DD/MM/YYYY': 'start_date_yyyy-mm-dd',
                    'end_date_DD/MM/YYYY': 'end_date_yyyy-mm-dd',
                    'start_date': 'start_date_yyyy-mm-dd',
                    'end_date': 'end_date_yyyy-mm-dd',
                    'dh_sigma': 'dh_sigma_m',
                    'dV_sigma': 'dV_sigma_km3',
                    'GlacierID': 'glacier_id',
                    'Area(km2)': 'S_km2',
                    'Startdateused': 'start_date_yyyy-mm-dd',
                    'Enddateused': 'end_date_yyyy-mm-dd',
                    'MeanElevationChange(m)': 'dh_m',
                    'OverallElevationChangeUncertainty(m)': 'dh_sigma_m',
                    'VolumeChange(km3)': 'dV_km3',
                    'OverallVolumeChangeUncertainty': 'dV_sigma_km3',
                    'remarks (=% with valid data)': 'remarks',
                    'remarks(=%withvaliddata)': 'remarks',
                    }



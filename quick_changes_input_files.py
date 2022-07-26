# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 09:13:15 2022

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
path_HEF = path + 'EXP1_from_participants/HEF/'
path_ALE = path + 'EXP1_from_participants/ALE/'


#dh_dt_file = path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_trend_dh_HINTEREIS_2000.8-2021.6.tif'
#dh_file = path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_dh_HINTEREIS_2000.8-2021.6.tif'
#delta_t = 20.8
#
#dh_dt_file = path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_trend_dh_HINTEREISFERNER_2019.75-2010.75.tif'
#dh_file = path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_dh_HINTEREISFERNER_2019.75-2010.75.tif'
#delta_t = 9.0
#
#shutil.copy(dh_dt_file, dh_file)
#ds = gdal.Open(dh_file, gdal.GA_Update)
#band = ds.GetRasterBand(1)
#dh_dt_array = ds.GetRasterBand(1).ReadAsArray()
#dh_dt_array[dh_dt_array==-9999] = np.nan
#dh_array = dh_dt_array*delta_t
#dh_array[np.isnan(dh_array)] = -9999
#band.WriteArray(dh_array)
#ds = None

#dh_file1 = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_FAU_ASTER/region_015_AST_Hintereisferner/dh_on_ice__Hintereisferner-strips_crp2reg_015_AST_Hintereisferner.tif'
#dh_file2 = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_FAU_ASTER/region_015_AST_Hintereisferner/dh_no_ice__Hintereisferner-strips_crp2reg_015_AST_Hintereisferner.tif'
#dh_file_merged = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_FAU_ASTER/region_015_AST_Hintereisferner/dh_Hintereisferner-strips_crp2reg_015_AST_Hintereisferner.tif'
#
#
#dh_file1 = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_TDX_FAU/region_013_TDX_Hintereisferner/dh_on_ice__Hintereisferner-strips_crp2reg_013_TDX_Hintereisferner.tif'
#dh_file2 = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_TDX_FAU/region_013_TDX_Hintereisferner/dh_no_ice__Hintereisferner-strips_crp2reg_013_TDX_Hintereisferner.tif'
#dh_file_merged = path_HEF + 'Exp1_HEF_FAU\Exp1_HEF_TDX_FAU/region_013_TDX_Hintereisferner/dh_Hintereisferner-strips_crp2reg_013_TDX_Hintereisferner.tif'
#
#dh_file1 = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/region_007_AST_Aletsch/dh_on_ice__Aletsch-strips_crp2reg_007_AST_Aletsch.tif'
#dh_file2 = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/region_007_AST_Aletsch/dh_no_ice__Aletsch-strips_crp2reg_007_AST_Aletsch.tif'
#dh_file_merged = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/region_007_AST_Aletsch/dh_Aletsch-strips_crp2reg_007_AST_Aletsch.tif'
##
#dh_file1 = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/region_001_TDX_Aletsch/dh_on_ice__Aletsch-strips_crp2reg_001_TDX_Aletsch.tif'
#dh_file2 = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/region_001_TDX_Aletsch/dh_no_ice__Aletsch-strips_crp2reg_001_TDX_Aletsch.tif'
#dh_file_merged = path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/region_001_TDX_Aletsch/dh_Aletsch-strips_crp2reg_001_TDX_Aletsch.tif'
#
##
#shutil.copy(dh_file1, dh_file_merged)
#
#ds = gdal.Open(dh_file2)
#dh2 = ds.GetRasterBand(1).ReadAsArray()
#nodata = ds.GetRasterBand(1).GetNoDataValue()
#dh2[np.abs(dh2)>=1e4] = np.nan
#ds = None
#
#
#ds = gdal.Open(dh_file_merged, gdal.GA_Update)
#band = ds.GetRasterBand(1)
#dh_array = ds.GetRasterBand(1).ReadAsArray()
#dh_array[np.abs(dh_array)>=1e4] = np.nan
#dh_array[np.isnan(dh_array)] = dh2[np.isnan(dh_array)]
#dh_array[np.isnan(dh_array)] = -9999
#band.WriteArray(dh_array)
#ds.GetRasterBand(1).SetNoDataValue(-9999)
#ds = None


#dh_file = path_HEF + 'Exp1_HEF_Berthier/BERTHIER_AT_HINTEREISFERNER_2019-09-21_2010-10-08_CTL.tif'
#dh_file = path_ALE + 'Exp1_ALE_Berthier/BERTHIER_CH_ALETSCH_2017-09-21_2011-09-13_CTL.tif'
#
#
#ds = gdal.Open(dh_file, gdal.GA_Update)
#ds.GetRasterBand(1).SetNoDataValue(-9999)
#ds = None
path_BAL = path + 'EXP2_from_participants/BAL/'

list_excel_files = [path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2019_2011_v3/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2019_2011_v3/') if (x.endswith('.xlsx'))]
for fil in list_excel_files:
    read_file = pd.read_excel(fil)
    read_file.to_csv(fil[:-5]+'.csv')
    
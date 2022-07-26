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
import sys
from os import path

sys.path.append(path.abspath('C:/Users/brunbarf/Data/07_trucs_astuce/reproj_matching_CRS_res'))
from reproj_imB_on_imA import reproj_imB_matching_imA
from table_participants import color_dic, dic_HEF, dict_replacement, sensor_dic, dic_ALE, marker_dic, RGI_dic


path = 'C:/Users/brunbarf/Data/RAGMAC/WG1/'

ref_DEM_ALE = path + 'ASTER_processing/Aletsch/REF_DEM_MASK/DEM_REF.tif'

shp_all_glaciers = path+'EXP1_from_participants\shp\glaciers_around_ALE.shp'
glacier_outlines = shpreader.Reader(shp_all_glaciers)

list_participants = list(dic_ALE.keys())
#list_participants = ['Belart',
# 'Berthier',
# 'Dehecq',
# 'Dussaillant',
# 'Florentine',
# 'Hugonnet',
# 'Krieger',
# 'Sommer',
# 'Wendt']


#list_participants = ['Belart']

ds = gdal.Open(ref_DEM_ALE)
DEM = ds.GetRasterBand(1).ReadAsArray()
gt = ds.GetGeoTransform()
proj = ds.GetProjection()
nc = ds.RasterXSize
nl = ds.RasterYSize
ds = None


inproj = osr.SpatialReference()
inproj.ImportFromWkt(proj)
projcs = inproj.GetAuthorityCode('PROJCS')
projection = ccrs.epsg(projcs)

xmin=gt[0]
xmax=gt[0] + nc * gt[1]
ymin=gt[3] + nl * gt[5]
ymax=gt[3]



### for Hinterheiferner
N = 0
for participant in list_participants:
#    print(participant)
    for dh_files in dic_ALE[participant]['path_dh']:
        N+=1


[nx,ny] = np.shape(DEM)
stacked=np.zeros((N,nx,ny))*np.nan

i = 0
for participant in list_participants:
    print(participant)
    for dh_files in dic_ALE[participant]['path_dh']:
        dest_file = dh_files[:-4]+'_reproj.tif'
        reproj_imB_matching_imA(ref_DEM_ALE, dh_files, dest_file, method = 'bilinear')
        
        ds = gdal.Open(dest_file)
        dh_map = ds.GetRasterBand(1).ReadAsArray()
        ds = None
        
        dh_map[np.abs(dh_map)>1000] = np.nan
        
        stacked[i,::] = dh_map
        i+=1
        
#        plt.figure()
#        plt.imshow(stacked[i,::], vmin = -20, vmax = 20)
        
mean_dh = np.nanmean(stacked, axis = 0)
median_dh = np.nanmean(stacked, axis = 0)
std_dh = np.nanstd(stacked, axis = 0)
count = np.count_nonzero(~np.isnan(stacked), axis = 0)


#### plot mean dh
vmin = -20
vmax = 20
cmap_RdBu = cm.get_cmap('coolwarm_r', 100)
norm =mpl.colors.Normalize(vmin=vmin, vmax=vmax)


subplot_kw = dict(projection=projection)
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)
ax.set_extent([xmin, xmax, ymin,ymax], crs=projection)
extent = (gt[0], gt[0] + nc * gt[1],
          gt[3] + nl * gt[5], gt[3])
#    
img = ax.imshow(mean_dh,
            transform = ccrs.epsg(projcs),
            extent=extent,
            cmap = cmap_RdBu,
            vmin = vmin,
            vmax = vmax,
            origin='upper')

for line in glacier_outlines.records():
    ax.add_geometries([line.geometry], ccrs.epsg(projcs) ,facecolor='none' 
            , edgecolor='black',
            linewidth=0.8, zorder=2)
    
##### insert colorbar      
cbbox = inset_axes(ax, '15%', '30%', loc = 'upper right')
cbbox.set_xticks([]) 
cbbox.set_yticks([]) 
cbbox.set_facecolor([1,1,1,0.8])
ax2 = inset_axes(cbbox, '20%', '90%', loc = 6)

cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_RdBu,
                                norm=norm,
                                extend = 'both',
                                orientation='vertical')
cb1.set_label('dh [m]')
    
plt.savefig('mean_dh_ALE.png',
            dpi = 300,
            bbox_inches = 'tight')



#### plot median dh
vmin = -20
vmax = 20
cmap_RdBu = cm.get_cmap('coolwarm_r', 100)
norm =mpl.colors.Normalize(vmin=vmin, vmax=vmax)


subplot_kw = dict(projection=projection)
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)
ax.set_extent([xmin, xmax, ymin,ymax], crs=projection)
extent = (gt[0], gt[0] + nc * gt[1],
          gt[3] + nl * gt[5], gt[3])
#    
img = ax.imshow(median_dh,
            transform = ccrs.epsg(projcs),
            extent=extent,
            cmap = cmap_RdBu,
            vmin = vmin,
            vmax = vmax,
            origin='upper')

for line in glacier_outlines.records():
    ax.add_geometries([line.geometry], ccrs.epsg(projcs) ,facecolor='none' 
            , edgecolor='black',
            linewidth=0.8, zorder=2)
    
##### insert colorbar      
cbbox = inset_axes(ax, '15%', '30%', loc = 'upper right')
cbbox.set_xticks([]) 
cbbox.set_yticks([]) 
cbbox.set_facecolor([1,1,1,0.8])
ax2 = inset_axes(cbbox, '20%', '90%', loc = 6)

cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_RdBu,
                                norm=norm,
                                extend = 'both',
                                orientation='vertical')
cb1.set_label('dh [m]')
    
plt.savefig('median_dh_ALE.png',
            dpi = 300,
            bbox_inches = 'tight')



#### plot DEM count

vmin = 0
vmax = 16
cmap_RdBu = cm.get_cmap('inferno', 100)
norm =mpl.colors.Normalize(vmin=vmin, vmax=vmax)


subplot_kw = dict(projection=projection)
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)
ax.set_extent([xmin, xmax, ymin,ymax], crs=projection)
extent = (gt[0], gt[0] + nc * gt[1],
          gt[3] + nl * gt[5], gt[3])
#    
img = ax.imshow(count,
            transform = ccrs.epsg(projcs),
            extent=extent,
            cmap = cmap_RdBu,
            vmin = vmin,
            vmax = vmax,
            origin='upper')


for line in glacier_outlines.records():
    ax.add_geometries([line.geometry], ccrs.epsg(projcs) ,facecolor='none' 
            , edgecolor='black',
            linewidth=0.8, zorder=2)

##### insert colorbar      
cbbox = inset_axes(ax, '15%', '30%', loc = 'upper right')
cbbox.set_xticks([]) 
cbbox.set_yticks([]) 
cbbox.set_facecolor([1,1,1,0.8])
ax2 = inset_axes(cbbox, '20%', '90%', loc = 6)

cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_RdBu,
                                norm=norm,
                                extend = 'both',
                                orientation='vertical')
cb1.set_label('DEM count')
    
plt.savefig('DEM_count_ALE.png',
            dpi = 300,
            bbox_inches = 'tight')



#### plot std dh
vmin = 0
vmax = 20
cmap_RdBu = cm.get_cmap('viridis', 100)
norm =mpl.colors.Normalize(vmin=vmin, vmax=vmax)


subplot_kw = dict(projection=projection)
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)
ax.set_extent([xmin, xmax, ymin,ymax], crs=projection)
extent = (gt[0], gt[0] + nc * gt[1],
          gt[3] + nl * gt[5], gt[3])
#    
img = ax.imshow(std_dh,
            transform = ccrs.epsg(projcs),
            extent=extent,
            cmap = cmap_RdBu,
            vmin = vmin,
            vmax = vmax,
            origin='upper')

for line in glacier_outlines.records():
    ax.add_geometries([line.geometry], ccrs.epsg(projcs) ,facecolor='none' 
            , edgecolor='black',
            linewidth=0.8, zorder=2)
    
##### insert colorbar      
cbbox = inset_axes(ax, '15%', '30%', loc = 'upper right')
cbbox.set_xticks([]) 
cbbox.set_yticks([]) 
cbbox.set_facecolor([1,1,1,0.8])
ax2 = inset_axes(cbbox, '20%', '90%', loc = 6)

cb1 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap_RdBu,
                                norm=norm,
                                extend = 'both',
                                orientation='vertical')
cb1.set_label('std dh [m]')
    
plt.savefig('std_dh_dic_ALE.png',
            dpi = 300,
            bbox_inches = 'tight')


#### for Aletsch group
#df_ALE = pd.DataFrame(columns=list_keys)
#for participant in list_participants:
##    print(participant)
#    for results_files in dic_ALE[participant]['path_results']:
#        data = pd.read_csv(results_files)
#        data.columns = data.columns.str.replace(' ', '')
#        data = data.rename(columns=dict_replacement)
#        data['start_date'] = pd.to_datetime(data['start_date_yyyy-mm-dd'])
#        data['end_date'] = pd.to_datetime(data['end_date_yyyy-mm-dd'])
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
#        else:
#            data['sensor'] = sensor_dic[participant]
#        df_ALE =  pd.concat([df_ALE, data[list_keys]])
#df_ALE['delta_t'] = df_ALE['end_date'] - df_ALE['start_date']
#df_ALE['dh_dt'] = df_ALE['dh_m']/df_ALE['delta_t'].dt.days*365.25
#df_ALE.index = range(len(df_ALE))
#

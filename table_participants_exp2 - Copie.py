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


path_BAL = path + 'EXP2_from_participants/BAL/'
path_BAL_Dehecq = path_BAL + 'Exp2_BAL_Dehecq/'
list_dir_BAL_Dehecq = os.listdir(path_BAL_Dehecq)
list_Dehecq_all_files = [os.listdir(path_BAL_Dehecq + y) for y in list_dir_BAL_Dehecq]
flat_list_Dehecq_all_files = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.abspath(path_BAL_Dehecq)) for file in files]

        
dic_BAL_period1 = {'Berthier' : 
             {'path_dh': [path_BAL + 'Exp2_BAL_Berthier/2000-2012/CTL/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_CTL_dh.tif',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-BIAS/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-BIAS_dh.tif',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-CO/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-CO_dh.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Berthier/2000-2012/CTL/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_CTL_results.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-BIAS/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-BIAS_results.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-CO/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-CO_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_Berthier/2000-2012/CTL/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_CTL_errors.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-BIAS/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-BIAS_errors.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2000-2012/NO-CO/BERTHIER_PK_BALTORO_2000-02-01_2012-10-01_NO-CO_errors.csv']
             },
             'Bolch' : 
             {'path_dh': [path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2012_2000_CTRL.tif',
                          path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2012_2000_NO_COREG.tif',
                          path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2012_2000_NO_GAP.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2019_2012_RUN_results_updated_modifid_FB.csv'],
             'path_errors': []
             },
          'Dehecq' : 
             {'path_dh': [x for x in flat_list_Dehecq_all_files if (x.endswith('.tif') & ('2000_2012' in x))],
             'path_results': [x for x in flat_list_Dehecq_all_files if (x.endswith('_results.csv') & ('2000_2012' in x))],
             'path_errors': [x for x in flat_list_Dehecq_all_files if (x.endswith('_errors.csv') & ('2000_2012' in x))]
             },
          'Florentine' :  
            {'path_dh': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('.tif') & ('2001-12-28_2011-05-06' in x))],
             'path_results': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('_results.csv') & ('2001-12-28_2011-05-06' in x))],
             'path_errors': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('_error.csv') & ('2001-12-28_2011-05-06' in x))]
             },
          'Hugonnet' :   
            {'path_dh': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2012-10-01_2000-02-01_CTL_map.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2012-10-01_2000-02-01_CTL_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2012-10-01_2000-02-01_CTL_errors.csv']
             },
          'LeFernierre' : 
            {'path_dh': [path_BAL + 'Exp2_BAL_LaFrenierre/Elevation_Change_TIFs/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Elevation_Change_TIFs/') if (x.endswith('.tif') & ('2000_2011' in x))],
             'path_results': [path_BAL + 'Exp2_BAL_LaFrenierre/Results_2011_2000_v3/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Results_2011_2000_v3/') if (x.endswith('_results.csv'))],
             'path_errors': [path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2011_2000_v3/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2011_2000_v3/') if (x.endswith('_errors.csv'))]
             },
          'Sommer' : 
            {'path_dh': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/region_027_AST_Baltoro/dh_merge_BLT_AST_2000-2011.tif',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/region_025_TDX_Baltoro/dh_merge_BALT_2012_V2_CP30.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/FAU_PK_BALTORO_2011-03_2000-07_CTL_results.csv',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/FAU_PK_BALTORO_2012-02-09_2000-02-16_CTL_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/FAU_PK_BALTORO_2011-03_2000-07_CTL_errors.csv',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/FAU_PK_BALTORO_2012-02-09_2000-02-16_CTL_errors.csv']
             },
          }
            
dic_BAL_period2 = {'Berthier' : 
             {'path_dh': [path_BAL + 'Exp2_BAL_Berthier/2012-2019/CTL/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_CTL_dh.tif',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-BIAS/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-BIAS_dh.tif',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-CO/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-CO_dh.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Berthier/2012-2019/CTL/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_CTL_results.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-BIAS/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-BIAS_results.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-CO/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-CO_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_Berthier/2012-2019/CTL/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_CTL_errors.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-BIAS/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-BIAS_errors.csv',
                          path_BAL + 'Exp2_BAL_Berthier/2012-2019/NO-CO/BERTHIER_PK_BALTORO_2012-10-01_2019-10-01_NO-CO_errors.csv']
             },
             'Bolch' : 
             {'path_dh': [path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2019_2012_CTRL.tif',
                          path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2019_2012_NO_COREG.tif',
                          path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2019_2012_NO_GAP.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Bolch/BOLCH_BALTORO_2019_2012_RUN_results_updated_modifid_FB.csv'],
             'path_errors': []
             },
          'Dehecq' : 
             {'path_dh': [x for x in flat_list_Dehecq_all_files if (x.endswith('.tif') & ('2012_2019' in x))],
             'path_results': [x for x in flat_list_Dehecq_all_files if (x.endswith('_results.csv') & ('2012_2019' in x))],
             'path_errors': [x for x in flat_list_Dehecq_all_files if (x.endswith('_errors.csv') & ('2012_2019' in x))]
             },
          'Florentine' :  
            {'path_dh': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('.tif') & ('2011-05-06_2019-10-12' in x))],
             'path_results': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('_results.csv') & ('2011-05-06_2019-10-12' in x))],
             'path_errors': [path_BAL + 'Exp2_BAL_USGS/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_USGS/')if (x.endswith('_error.csv') & ('2011-05-06_2019-10-12' in x))]
             },
          'Hugonnet' :   
            {'path_dh': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2019-10-01_2012-10-01_CTL_map.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2019-10-01_2012-10-01_CTL_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_Hugonnet/HUGONNET_CH_BALTORO_2019-10-01_2012-10-01_CTL_errors.csv']
             },
          'LeFernierre' : 
            {'path_dh': [path_BAL + 'Exp2_BAL_LaFrenierre/Elevation_Change_TIFs/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Elevation_Change_TIFs/') if (x.endswith('.tif') & ('2019_2011' in x))],
         'path_results': [path_BAL + 'Exp2_BAL_LaFrenierre/Results_2019_2011_v3/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Results_2019_2011_v3/') if (x.endswith('_results.csv'))],
             'path_errors': [path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2019_2011_v3/'+x for x in os.listdir(path_BAL + 'Exp2_BAL_LaFrenierre/Errors_2019_2011_v3/') if (x.endswith('_errors.csv'))]
             },
          'Sommer' : 
            {'path_dh': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/region_031_AST_Baltoro/dh_merge_BLT_AST_2011-2019.tif',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/region_029_TDX_Baltoro/dh_merge_BALT_2018_V2_CP30.tif'],
             'path_results': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/FAU_PK_BALTORO_2020-07_2011-03_CTL_results.csv',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/FAU_PK_BALTORO_2018-09-18_2012-02-09_CTL_results.csv'],
             'path_errors': [path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_ASTER_FAU/FAU_PK_BALTORO_2020-07_2011-03_CTL_errors.csv',
                         path_BAL + 'Exp2_BAL_FAU/Exp2_BAL_TDX_FAU/FAU_PK_BALTORO_2018-09-18_2012-02-09_CTL_errors.csv']
             },
          }

if __name__ == "__main__":     
#    data = pd.read_csv(path + 'EXP1_from_participants/participants.csv', delimiter = ';')
#    list_participants = list(data.keys())
#    for participant in list_participants:
#        print(participant)
#        print(colors.to_rgba_array(color_dic[participant])*255.)
    
    dic_sites = {'BAL_per1' : dic_BAL_period1,
                 'BAL_per2' : dic_BAL_period2
                 }
    
    list_sites = ['BAL_per1', 'BAL_per2']

    
    for site in list_sites:
        print(site)
        dic_site = dic_sites[site]
        list_participants = list(dic_site.keys())
        for participant in list_participants:
            print(participant)
            ## check tif
            for tif_files in dic_site[participant]['path_dh']:
                if not os.path.exists(tif_files):
                    print(tif_files)
            for results_files in dic_site[participant]['path_results']:
                if not os.path.exists(results_files):
                    print(results_files)
            for error_files in dic_site[participant]['path_errors']:
                if not os.path.exists(error_files):
                    print(error_files)
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



path_HEF = path + 'EXP1_from_participants/HEF/'
dic_HEF = {'Belart': 
            {'path_dh': [path_HEF + 'Exp1_HEF_Belart/hin_20190917_minus_20101002-diff.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Belart/_Belart_ISL_RGI60-11.00897_20170916_20130916_RUN_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Belart/_Belart_ISL_RGI60-11.00897_20170916_20130916_RUN_errors.csv']
             },
          'Berthier' : 
             {'path_dh': [path_HEF + 'Exp1_HEF_Berthier/BERTHIER_AT_HINTEREISFERNER_2019-09-21_2010-10-08_CTL.tif'], ## dh map NOT rescaled for seasonal correction
             'path_results': [path_HEF + 'Exp1_HEF_Berthier/BERTHIER_AT_HINTEREISFERNER_2019-09-29_2009-10-03_SEAS_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Berthier/BERTHIER_AT_HINTEREISFERNER_2019-09-29_2009-10-03_SEAS_errors.csv']
             },
          'Dehecq' : 
             {'path_dh': [path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_autoselect/ddem_2010_2019_mode_median.tif',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_median/ddem_2010_2019_mode_median.tif',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries_full/ddem_2010_2019_mode_TimeSeries3.tif',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries3/ddem_2010_2019_mode_TimeSeries3.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_autoselect/xdem_AT_Hintereisferner_2010_2019_DEMdiff_autoselect_results.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_median/xdem_AT_Hintereisferner_2010_2019_DEMdiff_median_results.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries_full/xdem_AT_Hintereisferner_2010_2019_TimeSeries_full_results.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries3/xdem_AT_Hintereisferner_2010_2019_TimeSeries3_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_autoselect/xdem_AT_Hintereisferner_2010_2019_DEMdiff_autoselect_errors.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_DEMdiff_median/xdem_AT_Hintereisferner_2010_2019_DEMdiff_median_errors.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries_full/xdem_AT_Hintereisferner_2010_2019_TimeSeries_full_errors.csv',
                          path_HEF + 'Exp1_HEF_Dehecq/results_CTL_TimeSeries3/xdem_AT_Hintereisferner_2010_2019_TimeSeries3_errors.csv']
             },
          'Dussaillant' :  
             {'path_dh': [path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_dh_HINTEREIS_2000.8-2021.6.tif',
                          path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_dh_HINTEREISFERNER_2019.75-2010.75.tif'],
             'path_results': [
#                     path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_CTL_results.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_SEAS_results.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_CTL_results.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_SEAS_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_CTL_errors.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_longrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_SEAS_errors.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_CTL_errors.csv',
                              path_HEF + 'Exp1_HEF_Dussaillant/Exp1_HEF_Dussaillant_shortrun/IDUSSAILLANT_AT_HINTEREISFERNER_2019.75_2010.75_SEAS_errors.csv']
             },
          'Florentine' :  
            {'path_dh': [path_HEF + 'Exp1_HEF_USGS/McNeil_AT_Hintereisferner_2010-08-27_2019-09-21_CTL.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_USGS/McNeil_AT_Hintereisferner_2010-08-27_2019-09-21_CTL_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_USGS/McNeil_AT_Hintereisferner_2010-08-27_2019-09-21_CTL_error.csv']
             },
          'Hugonnet' :   
            {'path_dh': [path_HEF + 'Exp1_HEF_Hugonnet/HUGONNET_CH_HINTEREI_2019-10-01_2010-10-01_CTL.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Hugonnet/HUGONNET_CH_HINTEREI_2019-10-01_2010-10-01_CTL_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Hugonnet/HUGONNET_CH_HINTEREI_2019-10-01_2010-10-01_CTL_errors.csv']
             },
          'Krieger' :   
             {'path_dh': [path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS_dh.tif',
                          path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME_dh.tif',
                          path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME_dh.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS_results.csv',
                              path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME_results.csv',
                              path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSCROSS_errors.csv',
                              path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_COPERNICUSSAME_errors.csv',
                              path_HEF + 'Exp1_HEF_Krieger/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME/DLR_AT_HINTEREISFERNER_2019-09-21_2010-10-08_TDMGLOBALSAME_errors.csv']
             },
          'Piermattei' :   
             {'path_dh': [path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_ASTER_20190920_20101008_RANSAC.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_ASTER_20190929_20091003_coregistLSM.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_ASTER_20190929_20091003_coregLSM_filter.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_ASTER_20190929_20091003_coregLSM_filter_voidIDW.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_ASTER_20190929_20091003_coregLSM_filter_voidIHypsometry.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20190206_20120216_coregLSM.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20190206_20120216_coregLSM_filter.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20190206_20120216_coregLSM_filter_voidHypsometry.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20200911_20110924_coregLSM.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20200911_20110924_coregLSM_filter.tif',
                          path_HEF + 'Exp1_HEF_Piermattei/Piermattei_Hintereisferner_DEMdiff/DEMdiff_TDX_20200911_20110924_coregLSM_filter_voidIDW.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20091003_20190929_ASTER_DEMdiffVoidHypsom.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20091003_20190929_ASTER_DEMdiffVoidIDW.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20101001_20190929_ASTER_DEMdiffVoidHypsomSEAS.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20101001_20190929_ASTER_TimeSeriesLinear.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20101001_20190929_ASTER_TimeSeriesRANSAC.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20101001_20190929_TDX_DEMdiffVoidHypsomSEAS.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20110924_20200911_TDX_DEMdiffVoidHypsom.csv',
                              path_HEF + 'Exp1_HEF_Piermattei/_Piermattei_AT_Hintereis_20120216_20190206_TDX_DEMdiffVoidHypsom.csv'],
             'path_errors': []
             },
          'Sommer' : 
            {'path_dh': [path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_ASTER/region_015_AST_Hintereisferner/dh_merge_HEF_AST_2010-2019.tif',
                         path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_TDX/region_013_TDX_Hintereisferner/dh_merge_Hintereisferner_2011-2019_v01.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_ASTER/FAU_AT_HINTEREISFERNER_2020-09_2009-10_CTL_results.csv',
                         path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_TDX/FAU_AT_HINTEREISFERNER_2019-01-18_2011-12-12_CTL_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_ASTER/FAU_AT_HINTEREISFERNER_2020-09_2009-10_CTL_errors.csv',
                         path_HEF + 'Exp1_HEF_FAU/Exp1_HEF_FAU_TDX/FAU_AT_HINTEREISFERNER_2019-01-18_2011-12-12_CTL_errors.csv']
             },
          'Wendt' :  
            {'path_dh': [path_HEF + 'Exp1_HEF_Wendt/Wendt_HEF_2019-02-06_2012-02-16.tif'],
             'path_results': [path_HEF + 'Exp1_HEF_Wendt/Wendt_HEF_2019-02-06_2012-02-16_CLT_results.csv'],
             'path_errors': [path_HEF + 'Exp1_HEF_Wendt/Wendt_HEF_2019-02-06_2012-02-16_CLT_errors.csv']
             },
          'Validation' :  
            {'path_results': [path_HEF + '_Hintereisferner_2019-09-21_2010-10-08_validation.csv']
             }
          }


path_ALE = path + 'EXP1_from_participants/ALE/'
dic_ALE = {'Belart': 
            {'path_dh': [path_ALE + 'Exp1_ALE_Belart/ale_20170916_minus_20110916-diff.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_Belart/' + x for x in os.listdir(path_ALE + 'Exp1_ALE_Belart') if x.endswith('_results.csv')],
             'path_errors': [path_ALE + 'Exp1_ALE_Belart/' + x for x in os.listdir(path_ALE + 'Exp1_ALE_Belart') if x.endswith('_errors.csv')]
             },
          'Berthier' : 
             {'path_dh': [path_ALE + 'Exp1_ALE_Berthier/BERTHIER_CH_ALETSCH_2017-09-21_2011-09-13_CTL.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_Berthier/BERTHIER_CH_ALETSCH_2017-09-05_2012-09-07_SEAS_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_Berthier/BERTHIER_CH_ALETSCH_2017-09-05_2012-09-07_SEAS_errors.csv']
             },
          'Dehecq' : 
             {'path_dh': [path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_autoselect/ddem_2011_2017_mode_median.tif',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_median/ddem_2011_2017_mode_median.tif',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries_full/ddem_2011_2017_mode_TimeSeries3.tif',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries3/ddem_2011_2017_mode_TimeSeries3.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_autoselect/xdem_CH_Aletschgletscher_2011_2017_DEMdiff_autoselect_results.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_median/xdem_CH_Aletschgletscher_2011_2017_DEMdiff_median_results.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries_full/xdem_CH_Aletschgletscher_2011_2017_TimeSeries_full_results.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries3/xdem_CH_Aletschgletscher_2011_2017_TimeSeries3_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_autoselect/xdem_CH_Aletschgletscher_2011_2017_DEMdiff_autoselect_errors.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_DEMdiff_median/xdem_CH_Aletschgletscher_2011_2017_DEMdiff_median_errors.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries_full/xdem_CH_Aletschgletscher_2011_2017_TimeSeries_full_errors.csv',
                          path_ALE + 'Exp1_ALE_Dehecq/results_CTL_TimeSeries3/xdem_CH_Aletschgletscher_2011_2017_TimeSeries3_errors.csv']
             },
          'Dussaillant' :  
             {'path_dh': [path_ALE + 'Exp1_ALE_Dussaillant/IDUSSAILLANT_trend_dh_ALETSCH_2000.9-2021.6.tif'],
             'path_results': [
                              path_ALE + 'Exp1_ALE_Dussaillant/IDUSSAILLANT_CH_ALETSCH_2017.75_2011.75_SEAS_results.csv'
                              ],
             'path_errors': [path_ALE + 'Exp1_ALE_Dussaillant/IDUSSAILLANT_CH_ALETSCH_2017.75_2011.75_SEAS_errors.csv']
             },
          'Florentine' :  
            {'path_dh': [path_ALE + 'Exp1_ALE_USGS/McNeil_CH_GrosserAletschgletcher_2011-09-23_2017-09-22__CTL.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_USGS/McNeil_CH_GrosserAletschgletcher_2011-09-23_2017-09-22__CTL_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_USGS/McNeil_CH_GrosserAletschgletcher_2011-09-23_2017-09-22__CTL_error.csv']
             },
          'Hugonnet' :   
            {'path_dh': [path_ALE + 'Exp1_ALE_Hugonnet/HUGONNET_CH_ALETSCH_2017-09-01_2011-09-01_CTL.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_Hugonnet/HUGONNET_CH_ALETSCH_2017-09-01_2011-09-01_CTL_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_Hugonnet/HUGONNET_CH_ALETSCH_2017-09-01_2011-09-01_CTL_errors.csv']
             },
          'Krieger' :   
             {'path_dh': [path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS_dh.tif',
                          path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL_dh.tif'
                          ],
             'path_results': [path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS_results.csv',
                              path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL_results.csv'
                              ],
             'path_errors': [path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_COPERNICUS_errors.csv',
                              path_ALE + 'Exp1_ALE_Krieger/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL/DLR_CH_ALETSCHGLETSCHER_2017-09-21_2011-09-13_TDMGLOBAL_errors.csv'
                              ]
             },
          'Sommer' : 
            {'path_dh': [path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/region_007_AST_Aletsch/dh_on_ice__Aletsch-strips_crp2reg_007_AST_Aletsch.tif',
                         path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/region_001_TDX_Aletsch/dh_merge_Aletsch_2011-2017_v03.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/FAU_CH_ALETSCH_2018-09_2011-03_CTL_results.csv',
                         path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/FAU_CH_ALETSCH_2017-12-12_2012-01-19_CTL_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_ASTER/FAU_CH_ALETSCH_2018-09_2011-03_CTL_errors.csv',
                         path_ALE + 'Exp1_ALE_FAU/Exp1_ALE_FAU_TDX/FAU_CH_ALETSCH_2017-12-12_2012-01-19_CTL_errors.csv']
             },
          'Wendt' :  
            {'path_dh': [path_ALE + 'Exp1_ALE_Wendt/Wendt_ALE_2019-01-01_2013-03-21.tif'],
             'path_results': [path_ALE + 'Exp1_ALE_Wendt/Wendt_ALE_2019-01-01_2013-03-21_CLT_results.csv'],
             'path_errors': [path_ALE + 'Exp1_ALE_Wendt/Wendt_ALE_2019-01-01_2013-03-21_CLT_errors.csv']
             },
          'Validation' :  
            {'path_results': [path_ALE + '_AletschGroup_2017-09-21_2011-09-13_validation.csv']
             }
          }
            
            
path_VES = path + 'EXP1_from_participants/VES/'
dic_VES = {'Dehecq' : 
             {'path_dh': [path_VES + 'Exp1_VES_Dehecq/results_CTL_DEMdiff_median/ddem_2008_2020_mode_median.tif',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries_full/ddem_2008_2020_mode_TimeSeries3.tif',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries3/ddem_2008_2020_mode_TimeSeries3.tif'],
             'path_results': [path_VES + 'Exp1_VES_Dehecq/results_CTL_DEMdiff_median/xdem_NO_Vestisen_2008_2020_DEMdiff_median_results.csv',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries_full/xdem_NO_Vestisen_2008_2020_TimeSeries_full_results.csv',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries3/xdem_NO_Vestisen_2008_2020_TimeSeries3_results.csv'],
             'path_errors': [path_VES + 'Exp1_VES_Dehecq/results_CTL_DEMdiff_median/xdem_NO_Vestisen_2008_2020_DEMdiff_median_errors.csv',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries_full/xdem_NO_Vestisen_2008_2020_TimeSeries_full_errors.csv',
                          path_VES + 'Exp1_VES_Dehecq/results_CTL_TimeSeries3/xdem_NO_Vestisen_2008_2020_TimeSeries3_errors.csv']
             },
          'Florentine' :  
            {'path_dh': [path_VES + 'Exp1_VES_USGS/McNeil_VO_Vestisen_2011-03-20_2021-01-01__CTL.tif'],
             'path_results': [path_VES + 'Exp1_VES_USGS/McNeil_VO_Vestisen_2011-03-20_2021-01-01__CTL_results.csv'],
             'path_errors': [path_VES + 'Exp1_VES_USGS/McNeil_VO_Vestisen_2011-03-20_2021-01-01__CTL_error.csv']
             },
          'Hugonnet' :   
            {'path_dh': [path_VES + 'Exp1_VES_Hugonnet/HUGONNET_CH_VESTISEN_2019-08-01_2007-09-01_CTL_map.tif'],
             'path_results': [path_VES + 'Exp1_VES_Hugonnet/HUGONNET_CH_VESTISEN_2019-08-01_2007-09-01_CTL_results.csv'],
             'path_errors': [path_VES + 'Exp1_VES_Hugonnet/HUGONNET_CH_VESTISEN_2019-08-01_2007-09-01_CTL_errors.csv']
             },
          'Piermattei' : 
            {'path_dh': [path_VES + 'Exp1_VES_Piermattei/Piermattei_Vestisen_DEMdiff/' + x for x in os.listdir(path_VES + 'Exp1_VES_Piermattei/Piermattei_Vestisen_DEMdiff/') if x.endswith('.tif')],
             'path_results': [path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20060811_20190728_ASTER_MmastDEMdiffVoidHypsomGlacierComplex.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20060811_20190728_ASTER_MmastOpalsDEMdiffVoidHypsomGlacierComplex.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20060811_20190728_ASTER_ProvDEMdiffVoidHypsomGlacier.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20060811_20190728_ASTER_ProvDEMdiffVoidHypsomGlacierComplex.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20060811_20190728_ASTER_ProvDEMdiffVoidIDW.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20080902_20200810_ASTER_TimeSeriesRANSACglacier.csv',
                              path_VES + 'Exp1_VES_Piermattei/_Piermattei_NO_Vestisen_20080902_20200810_ASTER_TimeSeriesRANSACglacierComplex.csv'],
             'path_errors': []
             },
          'Sommer' : 
            {'path_dh': [path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_ASTER/region_2007-2021_AST_Vestisen/dh_merge_VIS_AST_2008-2020.tif',
                         path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_TDX/region_2011-2021_TDX_Vestisen/dh_merge_Vestisen_2011-2020_v02.tif'],
             'path_results': [path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_ASTER/FAU_NO_Vestisen_2021-08-26_2007-06-01_CTL_results.csv',
                         path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_TDX/FAU_NO_Vestisen_2021-01-01_2011-03-20_CTL_results.csv'],
             'path_errors': [path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_ASTER/FAU_NO_Vestisen_2021-08-26_2007-06-01_CTL_errors.csv',
                         path_VES + 'Exp1_VES_FAU/Exp1_VES_FAU_TDX/FAU_NO_Vestisen_2021-01-01_2011-03-20_CTL_errors.csv']
             },
          'Validation' :  
            {'path_results': [path_VES + '_Vestisen_2020-08-10_2008-09-92_validation.csv']
             }
          }


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
                    'remarks(=%withvaliddata)': 'remarks'
                    }



if __name__ == "__main__":     
#    data = pd.read_csv(path + 'EXP1_from_participants/participants.csv', delimiter = ';')
#    list_participants = list(data.keys())
#    for participant in list_participants:
#        print(participant)
#        print(colors.to_rgba_array(color_dic[participant])*255.)
    
    dic_sites = {'ALE' : dic_ALE,
                 'HEF' : dic_HEF,
                 'VES' : dic_VES}
    
    list_sites = ['ALE', 'HEF', 'VES']
#    list_sites = ['VES']

    
    for site in list_sites:
        print(site)
        dic_site = dic_sites[site]
        list_participants = list(dic_site.keys())
        list_participants.remove('Validation')
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
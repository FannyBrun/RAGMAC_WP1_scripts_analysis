# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 09:06:58 2022

@author: brunbarf
"""
import pandas as pd

ice_dens = 0.85 #Huss 2013


def calculate_dist_to_val(df_GLA):
    val = df_GLA['dh_m'][df_GLA['participant']=='Validation']
    df_GLA['diff_val_m'] = df_GLA['dh_m'] - float(val)
    df_GLA['diff_val_percent'] = df_GLA['diff_val_m']/float(val)*100
    
   
    if 'seas_corrected_dh_m' in list(df_GLA.keys()):
        df_GLA['diff_val_after_seas_corr_m'] = df_GLA['seas_corrected_dh_m'] - float(val)
        df_GLA['diff_val_after_seas_corr_percent'] = df_GLA['diff_val_after_seas_corr_m']/float(val)*100
        
    val = df_GLA['dh_dt'][df_GLA['participant']=='Validation']
    df_GLA['diff_val_ma-1'] = df_GLA['dh_dt'] - float(val)
    df_GLA['diff_val_dh_dt_percent'] = df_GLA['diff_val_ma-1']/float(val)*100

    return df_GLA
    

def append_seasonal_correction(df_GLA, path_csv):
    df_seas_corr = pd.read_csv(path_csv)
    df_GLA = pd.concat([df_GLA, df_seas_corr[['start_date_bias_corr_mwe','end_date_bias_corr_mwe']]], axis=1)
    df_GLA['seas_corrected_dh_m'] = df_GLA['dh_m'] + df_GLA['start_date_bias_corr_mwe']/ice_dens + df_GLA['end_date_bias_corr_mwe']/ice_dens
    df_GLA['seas_corr_mwe'] = df_GLA['start_date_bias_corr_mwe'] + df_GLA['end_date_bias_corr_mwe']
    return df_GLA
    
    
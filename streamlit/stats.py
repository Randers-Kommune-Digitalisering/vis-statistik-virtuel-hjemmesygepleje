import pandas as pd

from utils.time import get_last_week, format_decimal_hours
from database import get_weekly_stats_dataframe_by_week

def get_weekly_stats(week=None):
    if not week:
        week = get_last_week()

    df  = get_weekly_stats_dataframe_by_week(week)

    if df is None:
        return df
    
    for col in df.columns:
        new_name = None
        if 'visit' in col and 'citizen' in col:
            df[col] = df[col].astype(int)
            new_name = 'Borgere med planlagt skærmbesøg' if 'screen' in col else 'Borgere med planlagt besøg'
        elif 'visit' in col:
            df[col] = df[col].astype(int)
            new_name = 'Planlagte skærmbesøg' if 'screen' in col else 'Planlagte besøg'
        elif 'citizen' in col:
            df[col] = df[col].astype(int)
            new_name = 'Borgere'#'Planlagte skærmbesøg' if 'screen' in col else 'Planlagte besøg'
        elif 'hour' in col:
            df[col] = df[col].apply(format_decimal_hours)
            new_name = 'Tid planlagte skærmbesøg' if 'screen' in col else 'Tid planlagte besøg'
        
        df.rename(columns={col:new_name}, inplace=True)
            
    return df

def get_weekly_stats_screen(week=None):
    if not week:
        week = get_last_week()

    df  = get_weekly_stats_dataframe_by_week(week)

    if df is None:
        return df
    
    for col in df.columns:
        new_name = None
        if 'visit' in col and 'citizen' in col:
            if 'screen' in col:
                df[col] = df[col].astype(int)
                new_name = 'Borgere med planlagt skærmbesøg'
            else:
                df = df.drop(col, axis=1)
        elif 'visit' in col:
            if 'screen' in col:
                df[col] = df[col].astype(int)
                new_name = 'Planlagte skærmbesøg'
            else:
                df = df.drop(col, axis=1)
        elif 'citizen' in col:
            df = df.drop(col, axis=1)
        elif 'hour' in col:
            if 'screen' in col:
                df[col] = df[col].apply(format_decimal_hours)
                new_name = 'Tid planlagte skærmbesøg'
            else:
               df = df.drop(col, axis=1) 
        
        df.rename(columns={col:new_name}, inplace=True)
            
    return df
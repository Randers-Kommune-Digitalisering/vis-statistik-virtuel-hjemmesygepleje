import pandas as pd
from datetime import timedelta

from models import District, Call
from database import get_calls
from utils.time import get_week_start_and_end, get_last_week, format_decimal_hours
from utils.district import get_district_vitacomm, get_nexus_district

def get_calls_dataframe(week=None, deltadays=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)
    if deltadays:
        return get_calls(days=deltadays, end=end)
    else:
        return get_calls(start=start, end=end)

def answered_unanwsered_by_district(dataframe, district=None):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    if district:
        df = df[df['callee_district'].str.contains(district)]

    df = df[(df['caller_employee']==True) & (df['callee_employee']==False)]

    df.loc[:,'duration'] =  df['duration'].astype("string").str.split(":").apply(lambda x:  pd.to_timedelta(int(x[0][-2])*60*60 + int(x[1])*60 + int(x[2]), unit='s'))

    return len(df[df['duration'] > timedelta(seconds=0)]), len(df[df['duration'] == timedelta(seconds=0)])

def answered_unanwsered_all_districts(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = df.groupby('callee_district')['duration'].apply(lambda x: pd.Series([(x == 0).sum(), (x > 0).sum()])).unstack()
    df.reset_index(inplace=True)
    df['callee_district'] = df['callee_district'].apply(get_nexus_district)
    df.columns = ['Distrikt', 'Ubesvarede', 'Besvarede']

    return df

def answered_unanwsered_all_districts(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    pd.set_option('display.max_columns', None)

    df = df[(df['caller_employee']==True) & (df['callee_employee']==False)]
    
    df.loc[:,'duration'] =  df['duration'].astype("string").str.split(":").apply(lambda x:  pd.to_timedelta(int(x[0][-2])*60*60 + int(x[1])*60 + int(x[2]), unit='s'))

    df = df.groupby('callee_district')['duration'].apply(lambda x: pd.Series([(x == timedelta(seconds=0)).sum(), (x > timedelta(seconds=0)).sum()])).unstack()
    df = df.reset_index()
    df.columns = ['Distrikt', 'Ubesvarede', 'Besvarede']

    return df

def average_duration_all_districts(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = df[(df['caller_employee']==True) & (df['callee_employee']==False)]

    df.loc[:,'duration'] =  df['duration'].astype("string").str.split(":").apply(lambda x:  int(x[0][-2])*60*60 + int(x[1])*60 + int(x[2]))

    df = df[df['duration'] > 0]
    
    overall_avg_duration = pd.to_timedelta(df['duration'].mean(), unit='s')
    df.loc[:,'duration'] = pd.to_timedelta(df['duration'], unit='s')
    
    durations_df = df.groupby('callee_district')['duration'].mean().sort_values(ascending=False)
    durations_df = durations_df.sort_index(ascending=True)
    durations_df = pd.concat([durations_df, pd.Series(overall_avg_duration, index = ['Randers Kommune'])])
    durations_df.index.names = ['Distrikt']
    durations_df.name = 'Gennemsnitlig varighed'
    durations_df =  durations_df.astype(str).str[10:].str.split('.').str[0]

    return durations_df


def unique_citizens(dataframe, callee_district=True):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = df[(df['caller_employee']==True) & (df['callee_employee']==False)]

    df.loc[:,'duration'] =  df['duration'].astype("string").str.split(":").apply(lambda x:  pd.to_timedelta(int(x[0][-2])*60*60 + int(x[1])*60 + int(x[2]), unit='s'))
    
    df = df[df['duration'] > timedelta(seconds=0)]

    if callee_district:
        citizens_s = df.groupby('callee_district')['callee'].nunique().sort_values(ascending=False)
    else:
        citizens_s = df.groupby('caller_district')['callee'].nunique().sort_values(ascending=False)
    citizens_s = pd.concat([citizens_s, pd.Series(df['callee'].nunique(), index = ['Randers Kommune'])])
    citizens_s.name = 'Borgere med opkald'

    return citizens_s

def visits_data(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = df[(df['caller_employee']==True) & (df['callee_employee']==False)]

    df.loc[:,'duration'] =  df['duration'].astype("string").str.split(":").apply(lambda x:  pd.to_timedelta(int(x[0][-2])*60*60 + int(x[1])*60 + int(x[2]), unit='s'))
     
    df = df[df['duration'] > timedelta(seconds=0)]

    citizens_s = df.groupby('callee_district')['callee'].nunique().sort_values(ascending=False)
    citizens_s = pd.concat([citizens_s, pd.Series(df['callee'].nunique(), index = ['Randers Kommune'])])
    citizens_s.name = 'Borgere med opkald'

    duration_s = df.groupby('callee_district')['duration'].sum()
    duration_s = pd.concat([duration_s, pd.Series(df['duration'].sum(), index = ['Randers Kommune'])])
    duration_s = duration_s.apply(lambda x: format_decimal_hours((x.seconds / 3600)))
    duration_s.name = 'Tid i opkald'

    calls_s = df.groupby('callee_district')['id'].count()
    calls_s = pd.concat([calls_s, pd.Series(df['id'].count(), index = ['Randers Kommune'])])
    calls_s.name = 'Besvarede opkald'

    return pd.concat([citizens_s, duration_s, calls_s], axis=1)
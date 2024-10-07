import pandas as pd
import numpy as np
from datetime import timedelta

from models import OU, Call
from database import get_calls
from utils.time import get_week_start_and_end, get_last_week, format_decimal_hours
from utils.district import get_district_vitacomm, get_nexus_district
from utils.call import only_employee_to_resident, only_answered_calls


def get_calls_dataframe(week=None, deltadays=None):
    if week is None:
        week = get_last_week()

    start, end = get_week_start_and_end(week)
    if deltadays:
        return get_calls(days=deltadays, end=end)
    else:
        return get_calls(start=start, end=end)


def answered_unanwsered_by_district(dataframe, district_id=None):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    if district_id:
        df = df[df['callee_district'].str.contains(district_id)]

    df = only_employee_to_resident(df)

    # Assuming that an answered calls have a duration greater than 0 and vice versa
    data = {'answered': [len(df[df['duration'] > timedelta(seconds=0)])], 'unanswered': [len(df[df['duration'] == timedelta(seconds=0)])]}

    return pd.DataFrame(data)


def answered_unanwsered_all_districts(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    # Assuming that an answered calls have a duration greater than 0 and vice versa
    df = df.groupby('caller_district_id')['duration'].apply(lambda x: pd.Series([(x > timedelta(seconds=0)).sum(), (x == timedelta(seconds=0)).sum()])).unstack()

    df = df.reset_index()

    df.columns = ['caller_district_id', 'answered', 'unanswered']

    return df


def average_duration_all_districts(dataframe):
    print('HEJ!!!')
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    overall_avg_duration = pd.to_timedelta(df['duration'].mean(), unit='s')
    df.loc[:, 'duration'] = pd.to_timedelta(df['duration'], unit='s')

    durations_df = df.groupby('caller_district_id')['duration'].mean().sort_values(ascending=False)
    durations_df = durations_df.sort_index(ascending=True)
    durations_df = pd.concat([durations_df, pd.Series(overall_avg_duration, index=[0])])
    # durations_df.index.names = ['Distrikt']
    # durations_df.name = 'Gennemsnitlig varighed'
    durations_df = durations_df.astype(str).str[10:].str.split('.').str[0]

    return durations_df


def unique_citizens(dataframe, callee_district=True):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    if callee_district:
        citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)
    else:
        citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)

    citizens_s = pd.concat([citizens_s, pd.Series(df['callee_cpr'].nunique(), index=[0])])
    # citizens_s.name = 'Borgere med opkald'

    return citizens_s


def visits_data(dataframe):
    if isinstance(dataframe, pd.DataFrame):
        df = dataframe
    else:
        df = get_calls_dataframe()

    df = only_employee_to_resident(df)
    df = only_answered_calls(df)

    citizens_s = df.groupby('caller_district_id')['callee_cpr'].nunique().sort_values(ascending=False)
    citizens_s = pd.concat([citizens_s, pd.Series(df['callee_cpr'].nunique(), index=[0])])
    # citizens_s.name = 'Borgere med opkald'

    duration_s = df.groupby('caller_district_id')['duration'].sum()
    duration_s = pd.concat([duration_s, pd.Series(df['duration'].sum(), index=[0])])
    # duration_s = duration_s.apply(lambda x: format_decimal_hours((x.seconds / 3600)))
    # duration_s.name = 'Tid i opkald'

    calls_s = df.groupby('caller_district')['id'].count()
    calls_s = pd.concat([calls_s, pd.Series(df['id'].count(), index=[0])])
    # calls_s.name = 'Besvarede opkald'

    return pd.concat([citizens_s, duration_s, calls_s], axis=1)
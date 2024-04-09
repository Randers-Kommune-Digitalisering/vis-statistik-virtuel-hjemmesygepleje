import pandas as pd

from utils.time import get_last_week
from database import get_services_dataframes #, get_services_dataframes_by_week


def get_services():
    screen, non_screen = get_services_dataframes()
    screen = screen[['name', 'visits', 'district', 'week']].copy()
    non_screen = non_screen[['name', 'visits', 'district', 'week']].copy()
    
    screen = screen.groupby(['name', 'district', 'week']).aggregate({'visits': 'sum'}).sort_values(['visits'], ascending=[0])
    non_screen = non_screen.groupby(['name', 'district', 'week']).aggregate({'visits': 'sum'}).sort_values(['visits'], ascending=[0])

    return screen, non_screen

"""
def get_weekly_services(week=None):
    if not week:
        week = get_last_week()

    df  = get_services_dataframes_by_week(week)

    if df is None:
        return df
            
    return df
"""
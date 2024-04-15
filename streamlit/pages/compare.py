import streamlit as st
import altair as alt

from st_pages import add_page_title

from stats import get_weekly_stats_screen
from calls import get_calls_dataframe, visits_data
from utils.time import get_last_week
from utils.pages import week_selector, add_logo

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
add_logo()

@st.cache_data
def read_data(week_str):
    stats_df = get_weekly_stats_screen(week_str)

    if stats_df is None:
        return stats_df

    stats_df = stats_df.reset_index()
    stats_df.rename(columns={ stats_df.columns[0]: "Distrikt" }, inplace = True)

    weekly_calls = get_calls_dataframe(week_str)

    calls_df = visits_data(weekly_calls)
    calls_df = calls_df.reset_index()
    calls_df.rename(columns={ calls_df.columns[0]: "Distrikt" }, inplace = True)

    all_df = stats_df.merge(calls_df,on='Distrikt')
    all_df = all_df.set_index('Distrikt')
    return all_df[['Borgere med opkald', 'Borgere med planlagt skærmbesøg', 'Besvarede opkald', 'Planlagte skærmbesøg','Tid i opkald', 'Tid planlagte skærmbesøg']]

week = week_selector(get_last_week(), '2024-07')

stats = read_data(week)

if stats is None:
    st.write('Intet data')
else:
    st.table(stats)
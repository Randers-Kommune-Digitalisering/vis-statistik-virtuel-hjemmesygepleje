import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt

from datetime import timedelta
from st_pages import add_page_title

from stats import get_weekly_stats
from calls import get_calls_dataframe, unique_citizens
from utils.time import get_last_week, get_week_start_and_end
from utils.pages import week_selector, add_logo

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
add_logo()

@st.cache_data
def read_data(week_str):
    weekly_stats =  get_weekly_stats(week_str)
    
    if weekly_stats is None:
        return None
    
    start_date, end_date = get_week_start_and_end(week_str)
    start_date_week = pd.Timestamp(start_date).tz_localize('utc')
    start_date_fortnight = pd.Timestamp(start_date - timedelta(days=7)).tz_localize('utc')
    start_date_three_weeks = pd.Timestamp(start_date - timedelta(days=14)).tz_localize('utc')
    end_date = pd.Timestamp(end_date).tz_localize('utc')

    month_df = get_calls_dataframe(week_str, deltadays=30)
    three_weeks_df = month_df[(month_df['start_time'] >= start_date_three_weeks) & (month_df['end_time'] <= end_date)]
    fortnight_df = month_df[(month_df['start_time'] >= start_date_fortnight) & (month_df['end_time'] <= end_date)]
    week_df = month_df[(month_df['start_time'] >= start_date_week) & (month_df['end_time'] <= end_date)]
       
    month_calls = unique_citizens(month_df)
    month_calls.rename(month_calls.name + '(30 dage)', inplace=True)
    three_weeks_calls= unique_citizens(three_weeks_df)
    three_weeks_calls.rename(three_weeks_calls.name + '(21 dage)', inplace=True)
    fortnight_calls= unique_citizens(fortnight_df)
    fortnight_calls.rename(fortnight_calls.name + '(14 dage)', inplace=True)
    weekly_calls = unique_citizens(week_df)
    weekly_calls.rename(weekly_calls.name + '(7 dage)', inplace=True)
    
    #calls = month_calls.astype('Int64').to_frame().join(three_weeks_calls.astype('Int64').to_frame(), lsuffix='(30 dage)', rsuffix='(21 dage)')
    calls = month_calls.astype('Int64').to_frame().join([three_weeks_calls, fortnight_calls, weekly_calls])
    
    #stats = weekly_stats['Borgere med planlagt skærmbesøg'].astype('Int64').to_frame().join(weekly_stats['Borgere'].astype('Int64'))
    stats = weekly_stats['Borgere'].astype('Int64')
    data = calls.join(stats).fillna(0)
    
    for i in data.index.values.tolist():
        if i not in weekly_stats.index.values.tolist():
            data = data.drop(i)

    return data

def generate_sizes(dataframe, district, datatype):
    return dataframe.loc[district][datatype],  dataframe.loc[district]['Borgere'] - dataframe.loc[district][datatype]

def generate_pie_chart(dataframe, district, datatype):    
    df = pd.DataFrame({'Borgere': ['Med skærm', 'Uden skærm'], 'Antal': [dataframe.loc[district][datatype], dataframe.loc[district]['Borgere'] - dataframe.loc[district][datatype]]})
    df['Procent'] = ((df['Antal'] / sum(df['Antal'])) * 100)
    df['Procent'] =  df['Procent'].map('{:.2f}%'.format)

    base = alt.Chart(df).encode(
        theta="Antal:Q",
        color=alt.Color("Borgere:N", scale=alt.Scale(range=['#356093', '#6da3e3'])),
        tooltip=['Borgere', 'Antal', 'Procent']
    )

    pie = base.mark_arc(outerRadius=140)
    text = base.mark_text(radius=160, size=20).encode(text="Procent:N")

    return pie + text

def generate_bar_charts(dataframe, type):
    df = dataframe.drop('Randers Kommune').reset_index()
    df.rename(columns={ df.columns[0]: "Distrikt" }, inplace = True)

    df['Med skærm'] = df[type]
    df['Uden skærm'] = df['Borgere'] - df[type]

    by_amount =  alt.Chart(df).transform_fold(
        ['Med skærm', 'Uden skærm'],
        as_=['Borgere', 'Antal'],
    ).mark_bar().encode(
        color=alt.Color('Borgere:N', scale=alt.Scale(range=['#356093', '#6da3e3'])),
        y=alt.Y('Distrikt:N', sort=alt.SortField("Med skærm", 'descending'), axis=alt.Axis(labelAngle=0, title=None, labelLimit=300)),
        x='Antal:Q'
    )

    df_p = df.copy(deep=True)
    df_p['Med skærm'] = ((df_p['Med skærm'] / df_p['Borgere']) * 100).round(2)
    df_p['Uden skærm'] = ((df_p['Uden skærm'] / df_p['Borgere']) * 100).round(2)

    by_percentage = alt.Chart(df_p).transform_fold(
        ['Med skærm', 'Uden skærm'],
        as_= ['Borgere', 'Procent (%)'],
    ).mark_bar().encode(
        y=alt.Y('Distrikt:N', sort=alt.SortField("Med skærm", 'descending'), axis=alt.Axis(labelAngle=0, title=None, labelLimit=300)),
        x='Procent (%):Q',
        color=alt.Color('Borgere:N', scale=alt.Scale(range=['#356093', '#6da3e3']))
    )

    return by_amount, by_percentage

#st.set_page_config(page_title="Omlægningsgrad",page_icon="assets/favicon.ico", layout='wide')
#st.markdown("# Omlægningsgrad")

district_selectort_cont, week_selector_cont = st.columns(2)

with week_selector_cont:
    week = week_selector(get_last_week(), '2024-07')

data = read_data(week)

time_interval = '14 dage'

with district_selectort_cont:
    districts = data.index.values.tolist()
    district = st.selectbox(
        'Distrikt',
        districts,
        index = districts.index('Randers Kommune'),
    )

    data_type = f'Borgere med opkald({time_interval})'

if data is None:
    st.write('Intet data')
else:
    district_cont, all_cont = st.columns(2)

    with district_cont:
        pie_chart = generate_pie_chart(data, district, data_type)
        st.write(data_type + f'({district})')
        st.altair_chart(pie_chart, use_container_width=True)
    
    with all_cont:
        amount, percentage = generate_bar_charts(data, data_type)
        st.write(data_type)
        st.altair_chart(amount, use_container_width=True)
        st.altair_chart(percentage, use_container_width=True)
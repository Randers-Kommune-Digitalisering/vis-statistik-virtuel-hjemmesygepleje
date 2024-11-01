import streamlit as st
import altair as alt
import pandas as pd

from st_pages import add_page_title

from stats import get_weekly_stats
from data import get_calls_dataframe, unique_citizens
from database import get_citizens, get_call_citizens
from utils.time import get_last_week, get_weeks
from utils.pages import week_selector, get_logo, font_sizes

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
get_logo()
font_sizes()

@st.cache_data
def read_data(week_str, callee_district=True):
    weekly_stats =  get_weekly_stats(week_str)
    
    if weekly_stats is None:
        return None
    
    #start_date, end_date = get_week_start_and_end(week_str)
    #start_date_week = pd.Timestamp(start_date).tz_localize('utc')
    #start_date_fortnight = pd.Timestamp(start_date - timedelta(days=7)).tz_localize('utc')
    #start_date_three_weeks = pd.Timestamp(start_date - timedelta(days=14)).tz_localize('utc')
    #end_date = pd.Timestamp(end_date).tz_localize('utc')

    #month_df = get_calls_dataframe(week_str, deltadays=30)
    #three_weeks_df = month_df[(month_df['start_time'] >= start_date_three_weeks) & (month_df['end_time'] <= end_date)]
    #fortnight_df = month_df[(month_df['start_time'] >= start_date_fortnight) & (month_df['end_time'] <= end_date)]
    #eek_df = month_df[(month_df['start_time'] >= start_date_week) & (month_df['end_time'] <= end_date)]

    fortnight_df = get_calls_dataframe(week_str, deltadays=14)
       
    #month_calls = unique_citizens(month_df)
    #month_calls.rename(month_calls.name + '(30 dage)', inplace=True)
    #three_weeks_calls= unique_citizens(three_weeks_df)
    #three_weeks_calls.rename(three_weeks_calls.name + '(21 dage)', inplace=True)
    fortnight_calls= unique_citizens(fortnight_df, callee_district)
    fortnight_calls.rename(fortnight_calls.name + '(14 dage)', inplace=True)
    #weekly_calls = unique_citizens(week_df)
    #weekly_calls.rename(weekly_calls.name + '(7 dage)', inplace=True)
    
    #calls = month_calls.astype('Int64').to_frame().join(three_weeks_calls.astype('Int64').to_frame(), lsuffix='(30 dage)', rsuffix='(21 dage)')
    #calls = month_calls.astype('Int64').to_frame().join([three_weeks_calls, fortnight_calls, weekly_calls])
    
    #stats = weekly_stats['Borgere med planlagt skærmbesøg'].astype('Int64').to_frame().join(weekly_stats['Borgere'].astype('Int64'))
    stats = weekly_stats['Borgere'].astype('Int64')
    #data = calls.join(stats).fillna(0)

    data = fortnight_calls.astype('Int64').to_frame().join(stats).fillna(0)
    
    for i in data.index.values.tolist():
        if i not in weekly_stats.index.values.tolist():
            data = data.drop(i)

    return data

@st.cache_data
def read_nexus_data(start, end):
    weeks = get_weeks(start, end)
    data = get_citizens(weeks)
    temp = data.groupby(data['week']).aggregate('sum').reset_index()
    temp['district'] = 'Randers kommune'
    data = pd.concat([data, temp])
    return data

@st.cache_data
def read_vitacomm_data(start, end, district, callee_distrct=True):
    district = None if district == 'Randers Kommune' else district
    weeks = get_weeks(start, end)
    data = get_call_citizens(weeks, district=district, callee_district=callee_distrct)
    return data

def generate_sizes(dataframe, district, datatype):
    return dataframe.loc[district][datatype],  dataframe.loc[district]['Borgere'] - dataframe.loc[district][datatype]

def generate_pie_chart(dataframe, district, datatype):    
    df = pd.DataFrame({'Borgere': ['Med skærm', 'Uden skærm'], 'Antal': [dataframe.loc[district][datatype], dataframe.loc[district]['Borgere'] - dataframe.loc[district][datatype]]})
    df['Procent'] = ((df['Antal'] / sum(df['Antal'])) * 100)
    df['Procent'] =  df['Procent'].map('{:.2f}%'.format)

    base = alt.Chart(df, title=alt.TitleParams(district, anchor='start', offset=-20)).encode(
        theta="Antal:Q",
        color=alt.Color("Borgere:N", scale=alt.Scale(range=['#356093', '#6da3e3'])),
        tooltip=['Borgere', 'Antal', 'Procent']
    )

    pie = base.mark_arc(outerRadius=140)
    text = base.mark_text(radius=165, size=14).encode(text="Procent:N")

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

def generate_graph(dataframe):    
    dataframe['Uden skærm'] = dataframe['citizens'] - dataframe['screen']
    dataframe['Procent med skærm'] = (dataframe['screen'] / dataframe['citizens'])

    dataframe.rename(columns={'screen':'Med skærm'}, inplace=True)
    dataframe.rename(columns={'week':'Uge'}, inplace=True)
    dataframe.rename(columns={'district':'Distrikt'}, inplace=True)
    

    selection = alt.selection_multi(fields=['Distrikt'], bind='legend')

    chart = alt.Chart(dataframe).mark_line( point={
      "filled": False,
      "fill": "white"
    }).encode(
        alt.X('Uge:N',  scale=alt.Scale(padding=0)),
        alt.Y('Procent med skærm:Q').axis(format='%'),
        alt.Color('Distrikt:N').scale(scheme="dark2"),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    ).add_params(
        selection
    )

    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Uge', 'Distrikt'], empty='none')

    selectors = alt.Chart().mark_point(size=150, filled=True).encode(
        alt.Color('Distrikt:N').scale(scheme="dark2"),
        x="Uge:N",
        y = alt.Y('Procent med skærm:Q').axis(format='.2%'),
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=['Distrikt', 'Uge', alt.Tooltip('Procent med skærm',  format=".2%"), 'Med skærm', 'Uden skærm']
    ).add_selection(
        nearest
    ).transform_filter(selection)

    chart = alt.layer(chart, selectors, data=dataframe, height=500)

    return chart

district_selectort_cont, week_selector_cont = st.columns(2)

# based_on_district_cont, 

# with based_on_district_cont:
#     display = ("Baseret på medarbejder distrikt", "Baseret på borger distrikt")

#     options = (False, True)

#     based_on_district = st.selectbox("Data grundlag", options, format_func=lambda x: display[x])


with week_selector_cont:
    week = week_selector(get_last_week(), '2024-07')

data = read_data(week)

time_interval = '14 dage'

if data is None:
    st.write(f'Intet data for uge {week}')
else:
    with district_selectort_cont:
        districts = data.index.values.tolist()
        district = st.selectbox(
            'Distrikt',
            districts,
            index = districts.index('Randers Kommune'),
        )
    data_type = f'Borgere med opkald({time_interval})'
    district_cont, all_cont = st.columns(2)

    with district_cont:
        pie_chart = generate_pie_chart(data, district, data_type)
        st.altair_chart(pie_chart, use_container_width=True)
    
    with all_cont:
        amount, percentage = generate_bar_charts(data, data_type)
        st.altair_chart(amount, use_container_width=True)
        st.altair_chart(percentage, use_container_width=True)


start_week_cont, end_week_cont = st.columns(2)

with start_week_cont:
    st.write('Fra')
    start_week = week_selector(get_last_week(), '2024-07', 'start', 5)

with end_week_cont:
    st.write('Til')
    end_week = week_selector(get_last_week(), '2024-07', 'end')

nexus = read_nexus_data(start_week, end_week)

districts = nexus['district'].unique()

vitacomm_list = []
for district in districts:
    district = None if district == 'Randers kommune' else district
    vitacomm_list.append(read_vitacomm_data(start_week, end_week, district))

vitacomm = pd.concat(vitacomm_list)

data= nexus.merge(vitacomm, on=["week","district"])

graph = generate_graph(data)
st.altair_chart(graph, use_container_width=True)
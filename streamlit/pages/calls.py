import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

from st_pages import add_page_title

from call import get_calls_dataframe, answered_unanwsered_by_district, answered_unanwsered_all_districts, average_duration_all_districts
from utils.time import get_last_week, get_weeks
from utils.district import get_district_names
from utils.pages import week_selector, add_logo

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
add_logo()

@st.cache_data
def read_data(week_str):
    return get_calls_dataframe(week_str)

@st.cache_data
def read_historic_data(start, end):
    weeks = get_weeks(start, end)

    all_weeks_dfs = []
    for week in weeks:
        data = get_calls_dataframe(week)
        df = answered_unanwsered_all_districts(data)
        df = df[df.Distrikt != 'Intet distrikt']
        next_index = len(df) + 1
        df.loc[next_index] = df.sum(numeric_only=True, axis=0)
        df.at[next_index, 'Distrikt'] = 'Randers Kommune'
        df['Uge'] = week
        all_weeks_dfs.append(df)

    data = pd.concat(all_weeks_dfs)

    return data

def generate_pie_chart(dataframe, district):
    title = district
    if district == 'Randers Kommune':
        district = None  
    df = pd.DataFrame({'Status': ['Besvarede', 'Ubesvarede'], 'Antal': list(answered_unanwsered_by_district(data, district))})
    df['Procent'] = ((df['Antal'] / sum(df['Antal'])) * 100)
    df['Procent'] =  df['Procent'].map('{:.2f}%'.format)

    base = alt.Chart(df, title=alt.TitleParams(title, anchor='start', offset=-20)).encode(
        theta="Antal:Q",
        color=alt.Color("Status:N", scale=alt.Scale(range=['#6f9460','#ba3c3c'])),
        order=alt.Order("Procent", sort='ascending'),
        tooltip=['Status', 'Antal', 'Procent']
    )

    pie = base.mark_arc(outerRadius=140)
    text = base.mark_text(radius=165, size=14).encode(text="Procent:N")

    return pie + text

def generate_bar_charts(dataframe):
    by_amount = alt.Chart(dataframe).transform_fold(
        ['Besvarede', 'Ubesvarede'],
        as_=['Status', 'Antal']
    ).mark_bar().encode(
        y=alt.Y('Distrikt:N', sort=alt.SortField("Besvarede", 'descending'), axis=alt.Axis(labelAngle=0, title=None, labelLimit=300)),
        x='Antal:Q',
        color=alt.Color('Status:N', scale=alt.Scale(range=['#6f9460','#ba3c3c']))
    )

    df_p = dataframe.copy(deep=True)
    total = df_p['Besvarede'] + df_p['Ubesvarede']
    df_p['Besvarede'] = ((df_p['Besvarede'] / total) * 100).round(2)
    df_p['Ubesvarede'] = ((df_p['Ubesvarede'] / total) * 100).round(2)

    by_percentage = alt.Chart(df_p).transform_fold(
        ['Besvarede', 'Ubesvarede'],
        as_=['Status', 'Procent (%)'],
    ).mark_bar().encode(
        y=alt.Y('Distrikt:N', sort=alt.SortField("Besvarede", 'descending'), axis=alt.Axis(labelAngle=0, title=None, labelLimit=300)),
        x='Procent (%):Q',
        color=alt.Color('Status:N', scale=alt.Scale(range=['#6f9460','#ba3c3c']))
    )

    return by_amount, by_percentage

def generate_graph(dataframe):
    dataframe['Procent besvarede'] = ((dataframe['Besvarede'] / dataframe[['Besvarede','Ubesvarede']].sum(axis=1)))

    selection = alt.selection_multi(fields=['Distrikt'], bind='legend')

    chart = alt.Chart(dataframe).mark_line( point={
      "filled": False,
      "fill": "white"
    }).encode(
        alt.X('Uge:N',  scale=alt.Scale(padding=0)),
        alt.Y('Procent besvarede:Q').axis(format='%'),
        alt.Color('Distrikt:N').scale(scheme="dark2"),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
    ).add_params(
        selection
    )

    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['Uge', 'Distrikt'], empty='none')

    selectors = alt.Chart().mark_point(size=150, filled=True).encode(
        alt.Color('Distrikt:N').scale(scheme="dark2"),
        x="Uge:N",
        y = alt.Y('Procent besvarede:Q').axis(format='.2%'),
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        tooltip=['Distrikt', 'Uge', alt.Tooltip('Procent besvarede',  format=".2%"), 'Besvarede', 'Ubesvarede']
    ).add_selection(
        nearest
    ).transform_filter(selection)

    chart = alt.layer(chart, selectors, data=dataframe, height=500)
    return chart

district_selector_cont, duration_selector_cont = st.columns(2)

with district_selector_cont:
    district = st.selectbox(
        'Distrikt',
        ('Randers Kommune',) + get_district_names(),
        index=0,
        placeholder="Randers Kommune",
    )

with duration_selector_cont:
    week = week_selector(get_last_week(), '2023-18')
    
data = read_data(week)

answered_district_cont, answered_all_cont, duration_cont = st.columns(3)

answered_df = answered_unanwsered_all_districts(data)

with answered_district_cont:
    pie_chart = generate_pie_chart(data, district)
    st.altair_chart(pie_chart, use_container_width=True)

with answered_all_cont:
    amount, percentage = generate_bar_charts(answered_df)
    st.altair_chart(amount, use_container_width=True)
    st.altair_chart(percentage, use_container_width=True)

with duration_cont:
    st.table(average_duration_all_districts(data))

start_week_cont, end_week_cont = st.columns(2)

with start_week_cont:
    st.write('Fra')
    start_week = week_selector(get_last_week(), '2023-18', 'start', 5)

with end_week_cont:
    st.write('Til')
    end_week = week_selector(get_last_week(), '2023-18', 'end')

historic_data = read_historic_data(start_week, end_week)
graph = generate_graph(historic_data)

st.altair_chart(graph, use_container_width=True)

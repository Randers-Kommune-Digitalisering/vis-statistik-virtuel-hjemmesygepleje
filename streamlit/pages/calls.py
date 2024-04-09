import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

from st_pages import add_page_title

from calls import get_calls_dataframe, answered_unanwsered_by_district, answered_unanwsered_all_districts, average_duration_all_districts
from utils.time import get_last_week
from utils.district import get_district_names
from utils.pages import week_selector, add_logo

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
add_logo()

@st.cache_data
def read_data(week_str):
    return get_calls_dataframe(week_str)

def generate_pie_chart(dataframe, district):
    df = pd.DataFrame({'Status': ['Besvarede', 'Ubesvarede'], 'Antal': list(answered_unanwsered_by_district(data, district))})
    df['Procent'] = ((df['Antal'] / sum(df['Antal'])) * 100)
    df['Procent'] =  df['Procent'].map('{:.2f}%'.format)

    base = alt.Chart(df).encode(
        theta="Antal:Q",
        color=alt.Color("Status:N", scale=alt.Scale(range=['#6f9460','#ba3c3c'])),
        order=alt.Order("Procent", sort='ascending'),
        tooltip=['Status', 'Antal', 'Procent']
    )

    pie = base.mark_arc(outerRadius=140)
    text = base.mark_text(radius=180, size=20).encode(text="Procent:N")

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

#st.set_page_config(page_title="Opkald", page_icon="assets/favicon.ico", layout='wide')
#st.markdown("# Opkald")

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
    st.write(district) 
    if district == 'Randers Kommune':
        district = None       
    pie_chart = generate_pie_chart(data, district)
    st.altair_chart(pie_chart, use_container_width=True)

with answered_all_cont:
    amount, percentage = generate_bar_charts(answered_df)
    st.altair_chart(amount, use_container_width=True)
    st.altair_chart(percentage, use_container_width=True)

with duration_cont:
    st.table(average_duration_all_districts(data))
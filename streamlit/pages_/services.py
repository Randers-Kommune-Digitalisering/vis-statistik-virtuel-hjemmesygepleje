import streamlit as st
import altair as alt

from st_pages import add_page_title

from services import get_services
from utils.time import get_last_week
from utils.ou import get_district_names
from utils.pages import week_selector, get_logo, font_sizes

st.set_page_config(page_icon="assets/favicon.ico")
add_page_title(layout="wide")
get_logo()
font_sizes()

@st.cache_data
def read_data():
    return get_services()


def generate_pie_chart(dataframe):    
    return alt.Chart(dataframe).mark_arc().encode(
        theta="Antal",
        color=alt.Color("Ydelse", sort=alt.EncodingSortField('Antal', op='mean', order='descending')),
        order=alt.Order("Antal", sort='descending'),
        tooltip=['Ydelse', 'Antal', 'Procent']
    )

services_screen, services_non_screen = read_data()

district_cont, week_cont, all_time_cont = st.columns(3)


with district_cont:
    district = st.selectbox(
    'Distrikt',
    ('Randers Kommune',) + get_district_names(),
    index=0,
    placeholder="Randers Kommune",
)

with all_time_cont:
    st.write('')
    st.write('')
    all_time = st.checkbox('Altid')

with week_cont:
    if not all_time:
        week = week_selector(get_last_week(), '2024-07')
    else:
        st.write('')
        st.write('')
        st.write('')


screen_all_cont, non_screen_all_cont = st.columns(2)

with screen_all_cont:
    title_string = f'#### Skærm ({district})' if all_time else f'#### Skærm ({district}) uge {week}' 
    st.write(title_string)
    if services_screen is None:
        st.write('Intet data')
    else:
        if district != 'Randers Kommune':
            services_screen = services_screen.iloc[services_screen.index.get_level_values('district') == district]
        if not all_time:
            services_screen = services_screen.iloc[services_screen.index.get_level_values('week') == week]

        if services_screen.empty:
             st.write('Intet data')
        else:
            services_screen = services_screen.groupby(['name']).aggregate({'visits': 'sum'}).sort_values(['visits'], ascending=[0])
            services_screen.rename(columns={ services_screen.columns[0]: "Antal" }, inplace = True)
            services_screen['Procent'] = services_screen.apply(lambda col: (col / sum(col)) * 100)
            services_screen['Procent'] =  services_screen['Procent'].map('{:.2f}%'.format)

            chart_df = services_screen.reset_index().head(10)
            chart_df.rename(columns={ chart_df.columns[0]: "Ydelse" }, inplace = True)

            pie_chart = generate_pie_chart(chart_df)
            
            st.altair_chart(pie_chart, use_container_width=True)

            st.table(services_screen.head(10))


with non_screen_all_cont:
    title_string = f'#### Ikke Skærm ({district})' if all_time else f'#### Ikke Skærm ({district}) uge {week}' 
    st.write(title_string)
    if services_non_screen is None:
        st.write('Intet data')
    else:
        if district != 'Randers Kommune':
            services_non_screen = services_non_screen.iloc[services_non_screen.index.get_level_values('district') == district]
        if not all_time:
            services_non_screen = services_non_screen.iloc[services_non_screen.index.get_level_values('week') == week]
        
        if services_non_screen.empty:
             st.write('Intet data')
        else:
            services_non_screen = services_non_screen.groupby(['name']).aggregate({'visits': 'sum'}).sort_values(['visits'], ascending=[0])
            services_non_screen.rename(columns={ services_non_screen.columns[0]: "Antal" }, inplace = True)
            services_non_screen['Procent'] = services_non_screen.apply(lambda col: (col / sum(col)) * 100)
            services_non_screen['Procent'] =  services_non_screen['Procent'].map('{:.2f}%'.format)

            chart_df = services_non_screen.reset_index().head(10)
            chart_df.rename(columns={ chart_df.columns[0]: "Ydelse" }, inplace = True)

            pie_chart = generate_pie_chart(chart_df)

            st.altair_chart(pie_chart, use_container_width=True)

            st.table(services_non_screen.head(10))

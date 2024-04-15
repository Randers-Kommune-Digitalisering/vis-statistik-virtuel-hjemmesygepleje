import streamlit as st
from datetime import date

from utils.time import get_week_start_and_end, last_week_for_year

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.randers.dk/static/logo.svg);
                background-repeat: no-repeat;
                filter: brightness(0) invert(20%) sepia(9%) saturate(7500%) hue-rotate(200deg) brightness(95%) contrast(95%);
                background-size: 85%;
                background-position: 20px 30px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def week_selector(week_str, min_week_str, key='', delta_week_index=None):
    min_year, min_week = [int(x) for x in min_week_str.split('-')]
    default_year, default_week = [int(x) for x in week_str.split('-')]
    
    year_range = sorted([default_year - i for i in range((default_year - min_year + 1))], reverse=True)

    week_cont, year_cont, date_cont = st.columns(3)

    with year_cont:
        selected_year = st.selectbox('År', year_range, index=year_range.index(default_year), key=key + 'year')
    
    if selected_year == min_year:
        start_week = min_week
    else:
        start_week = 1

    if selected_year == default_year:
        end_week = default_week + 1
    else:
        end_week = last_week_for_year(selected_year)

    if selected_year == default_year:
        index = 1
    else:
        index = 0

    week_numbers = sorted([i for i in range(start_week, end_week + 1 )], reverse=True)

    with week_cont:
        if delta_week_index:
            week = week_numbers[index]-delta_week_index if week_numbers[index]-delta_week_index > 0 else 0
            index = week_numbers.index(week)
        
        selected_week = st.selectbox('Uge', week_numbers, index=index, key=key + 'week')

    start_of_week, end_of_week = get_week_start_and_end(f"{selected_year}-{selected_week}")

    with date_cont:
        st.write('')
        st.write('')
        st.write(f'{start_of_week.strftime("%d/%m-%Y")} - {end_of_week.strftime("%d/%m-%Y")}')

    week = f'{selected_year}-{str(selected_week).zfill(2)}'
   
    return week
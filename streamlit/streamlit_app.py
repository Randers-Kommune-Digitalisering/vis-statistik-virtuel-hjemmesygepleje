# import streamlit as st
# from st_pages import add_page_title, show_pages, Page, Section
# st.set_page_config(page_icon="assets/favicon.ico", layout="wide")

# show_pages(
#         [
#             Page("streamlit_app.py", "Forside"),

#             Section(name="Skærmbesøg"),
#             Page("pages/restructure.py", "Omlægningsgrad"),
#             Page("pages/calls.py", "Opkald"),

#             Section(name="Nexus"),
#             Page("pages/services.py", "Ydelser"),
#         ]
#     )

# font_sizes()
# add_page_title()

import streamlit as st
import streamlit_antd_components as sac

from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import OU
from database import get_engine
from call.data import get_call_data, get_children
from utils.pages import get_logo
from utils.time import get_last_week, get_week_before_last
import pandas as pd

with Session(get_engine()) as session:
    def generate_menu_items():
        top = session.query(OU).filter(and_(OU.children != None, OU.parent == None)).first()
        added_items = set()

        def generate_menu_item(ou):
            if ou.nexus_name in added_items:
                return None

            children = [generate_menu_item(child) for child in ou.children if 'intet' not in child.nexus_name.lower()] if ou.children else None
            if any(x in ou.nexus_name for x in ['Ældre og Sundhed', 'Vest', 'Nord', 'Syd']) and children:
                children.insert(0, sac.MenuItem(ou.nexus_name, children=None))
            if children:
                added_items.add(ou.nexus_name)
                return sac.MenuItem(ou.nexus_name, children=[child for child in children if child is not None])
            added_items.add(ou.nexus_name)
            return sac.MenuItem(ou.nexus_name)

        menu_items = [generate_menu_item(top)]
        return menu_items

    st.set_page_config(page_icon="assets/favicon.ico", layout="wide")
    st.markdown(get_logo(), unsafe_allow_html=True)
    top_container = st.container()
    c = st.columns([1, 5])

    with c[0]:
        selected_menu_item = sac.menu(generate_menu_items(), indent=10, color='black', index=3, open_index=[0, 1, 2, 3])

    last_week = get_last_week()

    children = get_children(selected_menu_item)

    if children:
        children_convertion_rate = []
        for child in children:
            children_convertion_rate.append({child: get_call_data(last_week, child)['Omlægningsgrad']})

    ou_to_select = None if 'Ældre og Sundhed' in selected_menu_item else selected_menu_item
    data_this_week = get_call_data(last_week, ou_to_select)
    data_week_before_last = get_call_data(get_week_before_last(), ou_to_select)

    with top_container:
        tc = st.columns([1, 1, 1])
        with tc[1]:
            st.markdown(f"### {selected_menu_item} - Uge {last_week.split('-')[1]}")

    with c[1]:
        if data_this_week:
            if children:
                nc = st.columns([1, 1, 1, 1])
            else:
                nc = st.columns([1, 1, 1])

            for key, value in data_this_week.items():
                old_value = data_week_before_last[key]
                if type(value) is timedelta:
                    if value.total_seconds() < old_value.total_seconds():
                        delta_value = '-' + str(timedelta(seconds=round((old_value.total_seconds() - value.total_seconds()))))
                    else:
                        delta_value = str(timedelta(seconds=round((value.total_seconds() - old_value.total_seconds()))))
                    value = str(timedelta(seconds=round(value.total_seconds())))
                elif type(value) is float:
                    delta_value = round(value - old_value, 2)
                    value = round(value, 2)
                elif type(value) is str:
                    delta_value = '-'
                elif type(value) is list:
                    pass
                else:
                    delta_value = data_this_week[key] - data_week_before_last[key] 

                if 'Omlægningsgrad' in key:
                    value = str(round(value * 100, 2)) + '%'
                    delta_value = str(round(delta_value * 100, 2)) + '%'

                if any(x in key for x in ['Ubesvarede', 'varighed']):
                    delta_color = 'inverse'
                else:
                    delta_color = 'normal'

                if type(value) is list:
                    pass
                elif 'Opkald' in key:
                    with nc[0]:
                        st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                elif 'Borgere' in key:
                    with nc[1]:
                        st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                else:
                    with nc[2]:
                        st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)

            if children:
                with nc[3]:
                    import matplotlib.pyplot as plt

                    child_names = [list(child.keys())[0] for child in children_convertion_rate]
                    conversion_rates = [list(child.values())[0] * 100 for child in children_convertion_rate]  # Convert to percentages

                    df = pd.DataFrame({
                        'Adm. enhed': child_names,
                        'Omlægningsgrad (%)': conversion_rates  # Update column name to reflect percentage
                    })

                    fig, ax = plt.subplots()
                    bars = ax.bar(df['Adm. enhed'], df['Omlægningsgrad (%)'])
                    ax.set_title('Omlægningsgrad')
                    ax.set_ylabel('Omlægningsgrad (%)')
                    ax.set_ylim(0, 15)  # Set y-axis limit to 15%
                    ax.set_xticklabels(df['Adm. enhed'], rotation=90)  # Rotate x labels

                    # Add values on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax.annotate(f'{height:.2f}%',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3),  # 3 points vertical offset
                                    textcoords="offset points",
                                    ha='center', va='bottom')

                    st.pyplot(fig, use_container_width=True)

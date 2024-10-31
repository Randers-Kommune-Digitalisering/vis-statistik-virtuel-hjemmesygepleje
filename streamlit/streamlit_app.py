import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import matplotlib.pyplot as plt

from models import OU
from database import get_engine
from data import get_overview_data, get_children, get_employee_data, get_service_data
from charts import create_service_pie_chart, create_conversion_rate_bar_chart, create_calls_bar_chart, create_use_level_bar_chart, create_duration_bar_chart
from utils.pages import get_logo
from utils.time import get_last_week, get_week_before_last, get_previous_week, get_weeks
from utils.pages import  week_selector

with Session(get_engine()) as session:
    def generate_menu_items():
        top = session.query(OU).filter(and_(OU.children != None, OU.parent == None)).first()
        added_items = set()

        def generate_menu_item(ou):
            if ou.nexus_name in added_items:
                return None

            children = [generate_menu_item(child) for child in ou.children if 'intet' not in child.nexus_name.lower()] if ou.children else None
            # if any(x in ou.nexus_name for x in ['Vest', 'Nord', 'Syd']) and children:
            #     children.insert(0, sac.TreeItem(ou.nexus_name, description='Område', children=None, tag=[sac.Tag('Område', color='black')]))
            # elif 'Omsorg' in ou.nexus_name:
            #     children.insert(0, sac.TreeItem(ou.nexus_name, description='Alle', children=None, tag=[sac.Tag('Alle', color='black')]))
            if children:
                added_items.add(ou.nexus_name)
                return sac.TreeItem(ou.nexus_name, children=[child for child in children if child is not None])
            added_items.add(ou.nexus_name)
            return sac.TreeItem(ou.nexus_name)

        menu_items = [generate_menu_item(top)]
        return menu_items

    st.set_page_config(page_title="Statistikmodul", page_icon="assets/favicon.ico", layout="wide")
    st.markdown(get_logo(), unsafe_allow_html=True)
    top_container = st.container()

    with st.sidebar:
        selected_menu_item = sac.tree(generate_menu_items(), color='dark', align='start', icon=None, show_line=False, checkbox=False, checkbox_strict=True, index=1, open_index=[0, 1])  # indent=10, color='black', index=2, open_index=[0, 1])

    if not isinstance(selected_menu_item, str):
        if 'selected_menu_item' in st.session_state:
            selected_menu_item = st.session_state['selected_menu_item']
        else:
            selected_menu_item = 'Sundhed kultur og Omsorg'
    else:
        st.session_state['selected_menu_item'] = selected_menu_item

    ou_to_select = None if any(x in selected_menu_item for x in ['Omsorg', 'Kommune']) else selected_menu_item

    with top_container:
        st.markdown(f'<font size="6"> {selected_menu_item}', unsafe_allow_html=True)
        with st.expander('Vælg uge', expanded=False):
            selected_week = week_selector(get_last_week(), '2023-18')

    content_tabs = sac.tabs([sac.TabsItem('Overblik'), sac.TabsItem('Medarbejdere'), sac.TabsItem('Ydelser'), sac.TabsItem('Historik')], color='dark', size='md', position='top', align='start', use_container_width=True)

    with st.spinner('Henter data...'):
        if content_tabs == 'Overblik':  
            children = get_children(selected_menu_item)

            if children:
                children_of_children = [item for child in children for item in get_children(child)]
                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_overview_data(selected_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_overview_data(selected_week, child)})

            data_this_week = get_overview_data(selected_week, ou_to_select)
            data_week_before_last = get_overview_data(get_previous_week(selected_week), ou_to_select)

            st.markdown(f'<font size="5"> Uge {selected_week.split("-")[1]}', unsafe_allow_html=True)
            content_top_container = st.container()
            content_bottom_container = st.container()
            with content_top_container:
                if data_this_week:
                    nc = st.columns([1, 1, 1])
                    for key, value in data_this_week.items():
                        old_value = data_week_before_last[key]
                        if type(value) is timedelta:
                            if value.total_seconds() < old_value.total_seconds():
                                delta_value = '-' + str(timedelta(seconds=round((old_value.total_seconds() - value.total_seconds()))))
                            else:
                                delta_value = str(timedelta(seconds=round((value.total_seconds() - old_value.total_seconds()))))
                            value = str(timedelta(seconds=round(value.total_seconds())))
                        elif type(value) is str:
                            delta_value = '-'
                        elif type(value) is list:
                            pass
                        else:
                            delta_value = data_this_week[key] - data_week_before_last[key] 

                        if 'Omlægningsgrad' in key:
                            value = f"{value * 100:.2f}%"
                            delta_value = f"{delta_value * 100:.2f}%"

                        if 'Anvendelsesgrad' in key:
                            delta_value = round(value - old_value, 2)
                            value = round(value, 2)

                        if any(x in key for x in ['ubesvarede', 'varighed']):
                            delta_color = 'inverse'
                        else:
                            delta_color = 'normal'

                        if type(value) is list:
                            pass
                        elif 'Opkald' in key:
                            with nc[0]:
                                if 'gennemsnitlig' in key:
                                    st.metric(label=key, value=value)
                                else:
                                    st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                        elif 'Borgere' in key:
                            with nc[1]:
                                st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                        else:
                            with nc[2]:
                                st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)

                    if children:
                        with content_bottom_container:
                            nc_bottom = st.columns([1, 1])
                            with nc_bottom[0]:
                                child_names = [list(child.keys())[0] for child in children_data if 'intet' not in list(child.keys())[0].lower()]
                                conversion_rates = [list(child.values())[0]['Omlægningsgrad'] for child in children_data if 'intet' not in list(child.keys())[0].lower()]  # Convert to percentages

                                chart = create_conversion_rate_bar_chart({'Enhed': child_names}, {'Omlægningsgrad': conversion_rates}, x_is_ou=True)
                                st.altair_chart(chart, use_container_width=True)

                            with nc_bottom[1]:
                                child_names = [list(child.keys())[0] for child in children_data if 'intet' not in list(child.keys())[0].lower()]
                                answered_calls = [list(child.values())[0]['Opkald besvarede'] for child in children_data if 'intet' not in list(child.keys())[0].lower()]

                                chart = create_calls_bar_chart({'Enhed': child_names}, {'Opkald besvarede': answered_calls}, x_is_ou=True)
                                st.altair_chart(chart, use_container_width=True)

        elif content_tabs == 'Medarbejdere':
            st.markdown(f'<font size="5"> Uge {selected_week.split("-")[1]}', unsafe_allow_html=True)
            children = get_children(selected_menu_item)

            if children:
                children_of_children = [item for child in children for item in get_children(child)]
                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_overview_data(selected_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_overview_data(selected_week, child)})

            data_this_week = get_employee_data(selected_week, ou_to_select)
            data_week_before_last = get_employee_data(get_previous_week(selected_week), ou_to_select)

            if data_this_week:
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

                    delta_color = 'off'

                    if 'Opkald besvarede' == key:
                        with nc[0]:
                            st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                    elif 'Opkald ubesvarede' == key:
                        with nc[1]:
                            st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)
                    else:
                        with nc[2]:
                            st.metric(label=key, value=value, delta=delta_value, delta_color=delta_color)

        elif content_tabs == 'Ydelser':
            data = get_service_data(selected_week, ou_to_select)

            if data:
                st.markdown(f'<font size="5"> Uge {selected_week.split("-")[1]}', unsafe_allow_html=True)
                cols = st.columns(len(data))
                # Create a unique color map for all names
                unique_names = set()
                for key, value in data.items():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        # Sort items by visits and take the top 10 in reverse order
                        top_items = sorted(value, key=lambda x: x['visits'], reverse=True)[:10]
                        unique_names.update(item['name'] for item in top_items)
                unique_names.add('Andet')
                unique_names = sorted(unique_names)

                color_palette = plt.get_cmap('tab20b').colors
                color_map = {name: '#{:02x}{:02x}{:02x}'.format(int(color[0]*255), int(color[1]*255), int(color[2]*255)) for name, color in zip(unique_names, color_palette)}

                index = 0

                for key, value in data.items():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        names = [item['name'] for item in value]
                        visits = [item['visits'] for item in value]

                        if names and visits:
                            # Calculate percentage for all items
                            total_visits = sum(visits)
                            percentages = [(visit / total_visits) * 100 for visit in visits]

                            # Filter out items with less than 4% and limit to a maximum of 9 items
                            filtered_data = [(name, visit) for name, visit, percentage in zip(names, visits, percentages) if percentage >= 4]
                            filtered_data = sorted(filtered_data, key=lambda x: x[1], reverse=True)[:9]
                            other_data = [(name, percentage, amount) for name, amount, percentage in zip(names, visits, percentages) if percentage < 4 and amount > 0]
                            other_data = [(name, percentage, amount) for name, percentage, amount in sorted(other_data, key=lambda x: x[1], reverse=True)[:11]]

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            other_visits = total_visits - sum(filtered_visits)

                            if other_visits > 0:
                                if len(other_data) == 1:
                                    filtered_data.append((list(other_data.keys())[0], other_visits))
                                else:
                                    filtered_data.append(('Andet', other_visits))

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            with cols[index]:
                                # st.pyplot(fig, use_container_width=True)
                                pie_chart = create_service_pie_chart(filtered_names, filtered_visits, key, color_map)
                                st.altair_chart(pie_chart, use_container_width=True)
                                if 'Andet' in filtered_names and other_data:
                                    if len(other_data) > 10:
                                        st.markdown('<font size="4"> Top 10 i andet:', unsafe_allow_html=True)
                                        del other_data[-1]
                                    else:
                                        st.markdown('<font size="4"> Andet:', unsafe_allow_html=True)
                                    other_df = pd.DataFrame(other_data, columns=['Ydelse', 'Procent', 'Antal'])
                                    other_df['Procent'] = other_df['Procent'].apply(lambda x: f"{x:.1f}%")
                                    st.markdown(other_df.to_markdown(index=False))
                                index += 1
        elif content_tabs == 'Historik':
            st.markdown(f'<font size="5"> Fra uge:', unsafe_allow_html=True)
            first_week = week_selector(get_week_before_last(), '2023-18', key='start')
            st.markdown(f'<font size="5"> Til uge:', unsafe_allow_html=True)
            last_week = week_selector(get_last_week(), '2023-18', key='end')
            
            weeks = get_weeks(first_week, last_week)
            data = []
            for week in weeks:
                week_data = get_overview_data(week, ou_to_select)
                if week_data:
                    week_data['Uge'] = week
                    data.append(week_data)

            combined_data = {}
            for d in data:
                for key, value in d.items():
                    if key not in combined_data:
                        combined_data[key] = []
                    combined_data[key].append(value)

            graph_tabs = sac.tabs([sac.TabsItem(item) for item in combined_data.keys() if 'inaktiv' not in item and item != 'Uge'])
            chart = None
            if graph_tabs == 'Anvendelsesgrad':
                chart = create_use_level_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})
            elif graph_tabs == 'Omlægningsgrad':
                chart = create_conversion_rate_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})
            elif 'varighed' in graph_tabs:
                chart = create_duration_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})
            else:
                chart = create_calls_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})

            st.altair_chart(chart, use_container_width=True)

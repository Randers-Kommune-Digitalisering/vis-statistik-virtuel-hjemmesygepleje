import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import matplotlib.pyplot as plt

from models import OU
from database import get_engine
from data import get_overview_data, get_children, get_employee_data, get_service_data, get_filtered_overview_data, get_filtered_employee_data, get_filtered_service_data
from charts import create_service_pie_chart, create_conversion_rate_bar_chart, create_calls_bar_chart, create_use_level_bar_chart, create_duration_bar_chart
from utils.pages import get_logo
from utils.time import get_last_week, get_week_before_last, get_previous_week, get_weeks
from utils.pages import week_selector

if "selected_week" not in st.session_state:
    st.session_state.selected_week = get_last_week()

if "first_week" not in st.session_state:
    st.session_state.first_week = get_week_before_last()

if "last_week" not in st.session_state:
    st.session_state.last_week = get_last_week()

with Session(get_engine()) as session:
    def generate_menu_items():
        top = session.query(OU).filter(and_(OU.children != None, OU.parent == None)).first()
        added_items = set()

        def generate_menu_item(ou):
            if ou.nexus_name in added_items:
                return None

            # children = [generate_menu_item(child) for child in ou.children if 'intet' not in child.nexus_name.lower()] if ou.children else None
            children = [generate_menu_item(child) for child in ou.children if all(s not in child.nexus_name.lower() for s in ['intet', 'borgerteam', 'sygeplejegruppe', 'plejecenter'])] if ou.children else None

            if 'kultur og omsorg' in ou.nexus_name.lower():
                # Borgerteams
                borgerteams = session.query(OU.nexus_name).filter(OU.nexus_name.like('%Borgerteam%')).all()
                unique_borgerteams = list(set(borgerteam[0] for borgerteam in borgerteams))
                borgerteam_item = sac.TreeItem('Borgerteam', children=[sac.TreeItem(borgerteam) for borgerteam in unique_borgerteams])
                children.append(borgerteam_item)

                # Sygeplejegrupper
                sygeplejegrupper = session.query(OU.nexus_name).filter(OU.nexus_name.like('%Sygeplejegruppe%')).all()
                unique_sygeplejegrupper = list(set(sygeplejegruppe[0] for sygeplejegruppe in sygeplejegrupper))
                sygeplejegrupper_item = sac.TreeItem('Sygeplejegrupper', children=[sac.TreeItem(sygeplejegruppe) for sygeplejegruppe in unique_sygeplejegrupper])
                children.append(sygeplejegrupper_item)

            if children:
                added_items.add(ou.nexus_name)
                return sac.TreeItem(ou.nexus_name, children=[child for child in children if child is not None])

            added_items.add(ou.nexus_name)
            return sac.TreeItem(ou.nexus_name)

        menu_items = [generate_menu_item(top)]

        return menu_items

    st.set_page_config(page_title="Statistikmodul", page_icon="assets/favicon.ico", layout="wide")
    st.markdown(get_logo(), unsafe_allow_html=True)
    top_container = st.empty()

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

    with top_container.empty():
        top_columns = st.columns([1, 1, 1])
        with top_columns[2]:
            # with st.expander('Vælg uge', expanded=False):
            with st.container(border=True):
                st.session_state.selected_week = week_selector(get_last_week(), '2023-18', week_to_select=st.session_state.selected_week)
        with top_columns[0]:
            st.markdown(f'<font size="6"> {selected_menu_item} - Uge {st.session_state.selected_week.split("-")[1].lstrip("0")}', unsafe_allow_html=True)

    content_tabs = sac.tabs([sac.TabsItem('Overblik'), sac.TabsItem('Medarbejdere'), sac.TabsItem('Ydelser'), sac.TabsItem('Historik')], color='dark', size='md', position='top', align='start', use_container_width=True)

    with st.spinner('Henter data...'):
        if content_tabs == 'Overblik':  
            # start old way (correct way) #
            # children = get_children(selected_menu_item)

            # if children:
            #     children_of_children = [item for child in children for item in get_children(child)]

            #     children_data = []
            #     if children_of_children:
            #         for child in children_of_children:
            #             children_data.append({child: get_overview_data(st.session_state.selected_week, child)})
            #     else:
            #         for child in children:
            #             children_data.append({child: get_overview_data(st.session_state.selected_week, child)})

            # data_this_week = get_overview_data(st.session_state.selected_week, ou_to_select)
            # data_week_before_last = get_overview_data(get_previous_week(st.session_state.selected_week), ou_to_select)
            # end old way #

            # start new way (hacky) #
            if 'kultur og omsorg' in selected_menu_item.lower():
                children = get_children(selected_menu_item)
            else:
                children = get_children(selected_menu_item, ['sygeplejegrupper', 'borgerteam', 'plejecenter'])

            if children:
                if 'kultur og omsorg' in selected_menu_item.lower():
                    children_of_children = [item for child in children for item in get_children(child, ['plejecenter'])]
                else:
                    children_of_children = [item for child in children for item in get_children(child, ['sygeplejegrupper', 'borgerteam'])]

                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_filtered_overview_data(st.session_state.selected_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_filtered_overview_data(st.session_state.selected_week, child)})

            if ou_to_select:
                if "borgerteam" not in ou_to_select.lower() and "sygeplejegrupper" not in ou_to_select.lower():
                    data_this_week = get_filtered_overview_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                    data_week_before_last = get_filtered_overview_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                else:
                    data_this_week = get_filtered_overview_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
                    data_week_before_last = get_filtered_overview_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Plejecenter'])
            else:
                # data_this_week = get_overview_data(st.session_state.selected_week, ou_to_select)
                data_this_week = get_filtered_overview_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
                # data_week_before_last = get_overview_data(get_previous_week(st.session_state.selected_week), ou_to_select)
                data_week_before_last = get_filtered_overview_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Plejecenter'])
            # end new way #

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
                            if type(old_value) not in [int, float]:
                                old_value = 0
                            delta_value = data_this_week[key] - old_value

                        if 'Omlægningsgrad' in key:
                            if type(value) is str:
                                delta_value = None
                            else:
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

                                if all(isinstance(rate, str) for rate in conversion_rates):
                                    pass
                                else:
                                    conversion_rates = [0 if isinstance(rate, str) else rate for rate in conversion_rates]
                                    chart = create_conversion_rate_bar_chart({'Enhed': child_names}, {'Omlægningsgrad': conversion_rates}, x_is_ou=True)
                                    st.altair_chart(chart, use_container_width=True)

                            with nc_bottom[1]:
                                child_names = [list(child.keys())[0] for child in children_data if 'intet' not in list(child.keys())[0].lower()]
                                answered_calls = [list(child.values())[0]['Opkald besvarede'] for child in children_data if 'intet' not in list(child.keys())[0].lower()]

                                chart = create_calls_bar_chart({'Enhed': child_names}, {'Opkald besvarede': answered_calls}, x_is_ou=True)
                                st.altair_chart(chart, use_container_width=True)

        elif content_tabs == 'Medarbejdere':
            children = get_children(selected_menu_item)

            if children:
                children_of_children = [item for child in children for item in get_children(child)]

                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_overview_data(st.session_state.selected_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_overview_data(st.session_state.selected_week, child)})

            # start old way (correct way) #
            # data_this_week = get_employee_data(st.session_state.selected_week, ou_to_select)
            # data_week_before_last = get_employee_data(get_previous_week(st.session_state.selected_week), ou_to_select)
            # end old way #

            # start new way (hacky) #
            if ou_to_select:
                if "borgerteam" not in ou_to_select.lower() and "sygeplejegrupper" not in ou_to_select.lower():
                    data_this_week = get_filtered_employee_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                    data_week_before_last = get_filtered_employee_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                else:
                    data_this_week = get_filtered_employee_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
                    data_week_before_last = get_filtered_employee_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Plejecenter'])
            else:
                # data_this_week = get_employee_data(st.session_state.selected_week, ou_to_select)
                data_this_week = get_filtered_employee_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
                # data_week_before_last = get_employee_data(get_previous_week(st.session_state.selected_week), ou_to_select)
                data_week_before_last = get_filtered_employee_data(get_previous_week(st.session_state.selected_week), ou_to_select, keywords_exclude=['Plejecenter'])
            # end new way #

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
            # start old way (correct way) #
            # data = get_service_data(st.session_state.selected_week, ou_to_select)
            # end old way #

            # start new way (hacky) #
            if ou_to_select:
                if "borgerteam" not in ou_to_select.lower() and "sygeplejegrupper" not in ou_to_select.lower():
                    data = get_filtered_service_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                else:
                    data = get_filtered_service_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
            else:
                # data = get_service_data(st.session_state.selected_week, ou_to_select)
                data = get_filtered_service_data(st.session_state.selected_week, ou_to_select, keywords_exclude=['Plejecenter'])
            # end new way #

            if data:
                cols = st.columns(len(data))
                # Create a unique color map for all names
                unique_names = set()
                for key, value in data.items():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        # Sort items by visits and take the top  in reverse order
                        top_items = sorted(value, key=lambda x: x['visits'], reverse=True)[:8]
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

                            # Filter out items with less than 4% and limit to a maximum of 8 items
                            filtered_data = [(name, visit) for name, visit, percentage in zip(names, visits, percentages) if percentage >= 4]
                            filtered_data = sorted(filtered_data, key=lambda x: x[1], reverse=True)[:8]
                            other_data = [(name, percentage, amount) for name, amount, percentage in zip(names, visits, percentages) if percentage < 4 and amount > 0]
                            other_data = [(name, percentage, amount) for name, percentage, amount in sorted(other_data, key=lambda x: x[1], reverse=True)[:8]]

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            other_visits = total_visits - sum(filtered_visits)

                            if other_visits > 0:
                                if len(other_data) == 1:
                                    filtered_data.append((other_data[0][0], other_visits))
                                else:
                                    filtered_data.append(('Andet', other_visits))

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            with cols[index]:
                                chart_name = f'Planlagte ydelser ({key.lower()})'
                                pie_chart, total_amount = create_service_pie_chart(filtered_names, filtered_visits, chart_name, color_map)
                                st.altair_chart(pie_chart, use_container_width=True)
                                st.markdown(f'<b>{chart_name} i alt: {total_amount}</b>', unsafe_allow_html=True)
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
            st.markdown(f'<font size="5"> {content_tabs}', unsafe_allow_html=True)
            with top_container.empty():
                top_columns = st.columns([1, 1, 1])
                with top_columns[0]:
                    st.markdown(f'<font size="6"> {selected_menu_item}', unsafe_allow_html=True)
                with top_columns[1]:
                    with st.container(border=True):
                        st.write('Fra')
                        st.session_state.first_week = week_selector(get_week_before_last(), '2023-18', key='start', week_to_select=st.session_state.first_week)
                with top_columns[2]:
                    with st.container(border=True):
                        st.write('Til')
                        st.session_state.last_week = week_selector(get_last_week(), '2023-18', key='end', week_to_select=st.session_state.last_week)

            weeks = get_weeks(st.session_state.first_week, st.session_state.last_week)
            data = []
            for week in weeks:
                # start old way (correct way) #
                # week_data = get_overview_data(week, ou_to_select)
                # end old way #

                # start new way (hacky) #
                if ou_to_select:
                    if "borgerteam" not in ou_to_select.lower() and "sygeplejegrupper" not in ou_to_select.lower():
                        week_data = get_filtered_overview_data(week, ou_to_select, keywords_exclude=['Sygeplejegrupper', 'Borgerteam', 'Plejecenter'])
                    else:
                        week_data = get_filtered_overview_data(week, ou_to_select, keywords_exclude=['Plejecenter'])
                else:
                    # week_data = get_overview_data(week, ou_to_select)
                    week_data = get_filtered_overview_data(week, ou_to_select, keywords_exclude=['Plejecenter'])
                # end new way #
                
                if week_data:
                    week_data['Uge'] = week
                    data.append(week_data)

            combined_data = {}
            for d in data:
                for key, value in d.items():
                    if key not in combined_data:
                        combined_data[key] = []
                    combined_data[key].append(value)

            graph_tabs = sac.tabs([sac.TabsItem(item) for item in combined_data.keys() if 'inaktiv' not in item and item != 'Uge'], color='dark', size='sm', position='top', align='start', use_container_width=True)
            chart = None
            if graph_tabs == 'Anvendelsesgrad':
                chart = create_use_level_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})
            elif graph_tabs == 'Omlægningsgrad':
                data = [0 if isinstance(value, str) else value for value in combined_data[graph_tabs]]
                chart = create_conversion_rate_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: data})
            elif 'varighed' in graph_tabs:
                chart = create_duration_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})
            else:
                chart = create_calls_bar_chart({'Uge': combined_data['Uge']}, {graph_tabs: combined_data[graph_tabs]})

            st.altair_chart(chart, use_container_width=True)

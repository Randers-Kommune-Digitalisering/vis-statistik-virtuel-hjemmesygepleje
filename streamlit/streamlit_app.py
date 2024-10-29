import streamlit as st
import streamlit_antd_components as sac

from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import matplotlib.pyplot as plt

from models import OU
from database import get_engine
from data import get_overview_data, get_children, get_employee_data, get_service_data
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
    last_week = get_last_week()

    with top_container:
        st.markdown(f'<font size="6"> {selected_menu_item}', unsafe_allow_html=True)

    # TODO: Add history --  , sac.TabsItem('Historik')
    content_tabs = sac.tabs([sac.TabsItem('Overblik'), sac.TabsItem('Medarbejdere'), sac.TabsItem('Ydelser')], color='dark', size='md', position='top', align='start', use_container_width=True)

    with st.spinner('Henter data...'):
        if content_tabs == 'Overblik':  
            children = get_children(selected_menu_item)

            if children:
                children_of_children = [item for child in children for item in get_children(child)]
                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_overview_data(last_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_overview_data(last_week, child)})

            data_this_week = get_overview_data(last_week, ou_to_select)
            data_week_before_last = get_overview_data(get_week_before_last(), ou_to_select)

            st.markdown(f'<font size="5"> Uge {last_week.split("-")[1]}', unsafe_allow_html=True)
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
                                conversion_rates = [list(child.values())[0]['Omlægningsgrad'] * 100 for child in children_data if 'intet' not in list(child.keys())[0].lower()]  # Convert to percentages

                                df = pd.DataFrame({
                                    'Adm. enhed': child_names,
                                    'Omlægningsgrad (%)': conversion_rates  # Update column name to reflect percentage
                                })

                                df = df.sort_values('Adm. enhed', ascending=True)
                                df = df.groupby('Adm. enhed', as_index=False).sum()

                                fig, ax = plt.subplots()
                                bars = ax.bar(df['Adm. enhed'], df['Omlægningsgrad (%)'])
                                ax.set_title('Omlægningsgrad')
                                ax.set_ylabel('Omlægningsgrad (%)')
                                ax.set_ylim(0, max(df['Omlægningsgrad (%)']) * 1.2)  # Set y-axis limit to 10% higher than the highest percentage
                                ax.set_xticks(range(len(df['Adm. enhed'])))
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

                            with nc_bottom[1]:
                                child_names = [list(child.keys())[0] for child in children_data if 'intet' not in list(child.keys())[0].lower()]
                                answered_calls = [list(child.values())[0]['Opkald besvarede'] for child in children_data if 'intet' not in list(child.keys())[0].lower()]

                                df = pd.DataFrame({
                                    'Adm. enhed': child_names,
                                    'Opkald besvarede': answered_calls  # Update column name to reflect percentage
                                })

                                df = df.sort_values('Adm. enhed', ascending=True)
                                df = df.groupby('Adm. enhed', as_index=False).sum()

                                fig, ax = plt.subplots()
                                bars = ax.bar(df['Adm. enhed'], df['Opkald besvarede'])
                                ax.set_title('Opkald besvarede')
                                ax.set_ylabel('Opkald besvarede')
                                ax.set_ylim(0, max(df['Opkald besvarede']) * 1.1)  # Set y-axis limit to highest number plus 10
                                ax.set_xticks(range(len(df['Adm. enhed'])))
                                ax.set_xticklabels(df['Adm. enhed'], rotation=90)  # Rotate x labels

                                # Add values on bars
                                for bar in bars:
                                    height = bar.get_height()
                                    ax.annotate(f'{height:d}',
                                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                                xytext=(0, 3),  # 3 points vertical offset
                                                textcoords="offset points",
                                                ha='center', va='bottom')

                                st.pyplot(fig, use_container_width=True)

        elif content_tabs == 'Medarbejdere':
            st.markdown(f'<font size="5"> Uge {last_week.split("-")[1]}', unsafe_allow_html=True)
            children = get_children(selected_menu_item)

            if children:
                children_of_children = [item for child in children for item in get_children(child)]
                children_data = []
                if children_of_children:
                    for child in children_of_children:
                        children_data.append({child: get_overview_data(last_week, child)})
                else:
                    for child in children:
                        children_data.append({child: get_overview_data(last_week, child)})

            data_this_week = get_employee_data(last_week, ou_to_select)
            data_week_before_last = get_employee_data(get_week_before_last(), ou_to_select)

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
            data = get_service_data(last_week, ou_to_select)

            if data:
                st.markdown(f'<font size="5"> Uge {last_week.split("-")[1]}', unsafe_allow_html=True)
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
                color_map = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

                index = 0

                for key, value in data.items():
                    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
                        names = [item['name'] for item in value]
                        visits = [item['visits'] for item in value]

                        if names and visits:
                            # Calculate percentage for all items
                            total_visits = sum(visits)
                            percentages = [(visit / total_visits) * 100 for visit in visits]

                            # Filter out items with less than 3% and limit to a maximum of 9 items
                            filtered_data = [(name, visit) for name, visit, percentage in zip(names, visits, percentages) if percentage >= 4]
                            filtered_data = sorted(filtered_data, key=lambda x: x[1], reverse=True)[:9]
                            other_data = [(name, percentage) for name, visit, percentage in zip(names, visits, percentages) if percentage < 4 and visit > 0]
                            other_data = {name: percentage for name, percentage in sorted(other_data, key=lambda x: x[1], reverse=True)[:11]}

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            other_visits = total_visits - sum(filtered_visits)

                            if other_visits > 0:
                                if len(other_data) == 1:
                                    filtered_data.append((list(other_data.keys())[0], other_visits))
                                else:
                                    filtered_data.append(('Andet', other_visits))

                            filtered_names, filtered_visits = zip(*filtered_data) if filtered_data else ([], [])

                            fig, ax = plt.subplots()
                            colors = [color_map[name] for name in filtered_names]
                            ax.pie(filtered_visits, labels=filtered_names, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 8})
                            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                            ax.set_title(f'{key}', fontsize=14, pad=20)

                            with cols[index]:
                                st.pyplot(fig, use_container_width=True)
                                if 'Andet' in filtered_names and other_data:
                                    if len(other_data) > 10:
                                        st.markdown('<font size="4"> Top 10 i andet:', unsafe_allow_html=True)
                                        other_data.popitem()
                                    else:
                                        st.markdown('<font size="4"> Andet:', unsafe_allow_html=True)
                                    other_df = pd.DataFrame(list(other_data.items()), columns=['Ydelse', 'Procent'])
                                    other_df['Procent'] = other_df['Procent'].apply(lambda x: f"{x:.1f}%")
                                    st.markdown(other_df.to_markdown(index=False))
                                index += 1

import streamlit as st
from st_pages import add_page_title, show_pages, Page, Section

from utils.pages import add_logo

st.set_page_config(page_icon="assets/favicon.ico", layout="wide")

show_pages(
        [
            Page("streamlit_app.py", "Forside"),

            Section(name="Skærmbesøg"),
            Page("pages/restructure.py", "Omlægningsgrad"),
            Page("pages/calls.py", "Opkald"),

            Section(name="Nexus"),
            Page("pages/services.py", "Ydelser"),
        ]
    )

add_page_title()
add_logo()
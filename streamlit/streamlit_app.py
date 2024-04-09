import gc
import streamlit as st

from st_pages import Page, Section, show_pages, add_indentation

show_pages(
        [
            Page("pages/home.py", "Forside"),

            Section(name="Skærmbesøg"),
            Page("pages/restructure.py", "Omlægningsgrad"),
            Page("pages/calls.py", "Opkald"),

            Section(name="Nexus"),
            Page("pages/services.py", "Ydelser"),
        ]
    )

add_indentation()
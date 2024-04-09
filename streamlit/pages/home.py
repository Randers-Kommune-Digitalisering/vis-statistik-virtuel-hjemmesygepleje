import streamlit as st
from st_pages import add_page_title

from utils.pages import add_logo

st.set_page_config(page_icon="assets/favicon.ico", layout="wide")
add_page_title()
add_logo()
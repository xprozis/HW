import streamlit as st
from pages.shared.shared import *



st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="centered"
)

page_header("BOM Editor","In this page the user can load, add and edit the BOM final quantities")

# Sempre que carregar no componente, faz reset ao dataframe e carrega um novo dataframe para a página e para uma variavel global guardada no controlador
file = st.file_uploader("Drop here your BOM.xlsl file related to your project", type="xlsx")

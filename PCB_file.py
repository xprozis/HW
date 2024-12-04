import streamlit as st
from pages.shared.shared import *
from controller.PCB_file_controller import *



st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="centered"
)

page_header("PCB File Generator","Made by GOATs, for GOATs")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("ANTERIOR", use_container_width=True, on_click=nav_back)
with col2:
    st.button("SEGUINTE", use_container_width=True, on_click=nav_foward)
with col4:
    st.button("GERAR ZIP", use_container_width=True, type="primary")

st.progress(page_number/3)


if page_number == 0:
    st.subheader("1.º Ficheiros 3D")
    
    name_0 = ["TOP_VIEW","BOTTOM_VIEW"]
    name_1 = ["BOTTOM_VIEW","TOP_VIEW"]

    st.caption("No Fusion, abrir a vista 3D da PCB. Começar por tirar uma captura de ecra à vista superior (TOP VIEW) e de seguida à vista inferior (BOTTOM VIEW)")
    picture = st.file_uploader("Capturas de ecra da vista TOP e BOTTOM da PCB", type="PNG", accept_multiple_files=True, label_visibility="collapsed")

    if picture:
        for i in range(len(picture)):
                st.image(picture[i], caption = name_0[i])

        if st.button("( change name of the images )", use_container_width=True):
            name = name_0



if page_number == 1:
    st.subheader("2.º Ficheiros Assembly")
    top_bottom_view_silkscreen = st.file_uploader("2 PDF files of Silkscreen TOP and BOTTOM", type="pdf")
    BOM_file = st.file_uploader("BOM File", type="xlsl")
    pick_and_place = st.file_uploader("Pick and Place File", type="xlsl")

if page_number == 2:
    st.subheader("3.º Gerber Files")

if page_number == 3:
    st.subheader("4.º ReadME Files")
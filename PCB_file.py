import streamlit as st
from pages.shared.shared import *
from controller.PCB_file_controller import *



st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="centered"
)

page_header("PCB File Generator","Made by GOATs, for GOATs")


# Progress bar
st.progress(pagina/numero_paginas, text=f'{pagina} /' + str(numero_paginas))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("ANTERIOR", use_container_width=True, on_click=nav_back)
with col2:
    st.button("SEGUINTE", use_container_width=True, on_click=nav_foward)
with col4:
    st.button("GERAR ZIP", use_container_width=True, type="primary")

# Definir variavel de dados
define_dic()

# Nome do projecto
if pagina == 1:
    st.subheader("1.º Nome do projecto")
    st.caption("Inserir o Nome e Versão do projecto a ser apresentado na pasta de ficheiros")
    col1, col2 = st.columns([3,1])
    with col1:
        nome_projecto = st.text_input("NomeProjecto", value = project_dic["nome_projecto"], placeholder="Nome da PCB ex: pcb002A", label_visibility="collapsed")
    with col2:
        versao_projecto = st.text_input("Versao", value = project_dic["versao_projecto"], placeholder="Versão da PCB: ex: 2.0", label_visibility="collapsed")
    if nome_projecto and versao_projecto:
        st.subheader("Projecto: " + nome_projecto + "_V" + versao_projecto)
        st.caption("Directoria final: ./" + nome_projecto + "/" + versao_projecto + "/" + nome_projecto + "_" + versao_projecto + "/Production/")
        project_dic["nome_projecto"] = nome_projecto
        project_dic["versao_projecto"] = versao_projecto

if pagina == 2:
    st.subheader("2.º Ficheiros 3D")
    

    name_0 = ["TOP_VIEW","BOTTOM_VIEW"]
    name_1 = ["BOTTOM_VIEW","TOP_VIEW"]

    st.caption("1) No Fusion, abrir a vista 3D da PCB.")
    st.caption("2) Começar por tirar uma captura de ecra à vista superior - TOP VIEW")
    st.caption("3) Tirar uma captura de ecra à vista inferior - BOTTOM VIEW")
    st.caption("4) Seleciomar as duas capturas de ecra")

    picture = st.file_uploader("Capturas de ecra da vista TOP e BOTTOM da PCB", type="PNG", accept_multiple_files=True, label_visibility="collapsed")
    if picture:
        for i in range(len(picture)):
                st.image(picture[i], caption = name_0[i])

if pagina == 3:
    st.subheader("3.º Ficheiros Assembly")
    top_bottom_view_silkscreen = st.file_uploader("2 PDF files of Silkscreen TOP and BOTTOM", type="pdf")
    BOM_file = st.file_uploader("BOM File", type="xlsl")
    pick_and_place = st.file_uploader("Pick and Place File", type="xlsl")

if pagina == 4:
    st.subheader("3.º Gerber Files")

if pagina == 5:
    st.subheader("4.º ReadME Files")



import streamlit as st
from pages.shared.shared import *
from controller.PCB_file_controller import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss
import pandas as pd

# Declare variable.
if 'pdf_ref' not in ss:
    ss.pdf_ref = None

if 'image_ref' not in ss:
    ss.image_ref = None

if 'bom_csv_ref' not in ss:
    ss.bom_csv_ref = pd.DataFrame()


# Definir variavel de dados
define_variables()

st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="centered"
)

page_header("PCB File Generator","Made by GOATs, for GOATs")


# Progress bar
st.progress(pagina/numero_paginas, text=f'Etapas do processo: {pagina} /' + str(numero_paginas))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("Retroceder", use_container_width=True, on_click=nav_back)
with col2:
    st.button("Avançar", use_container_width=True, on_click=nav_foward)
with col4:
    st.button("Download ZIP", use_container_width=True, type="primary", disabled = False)


# Nome do projecto
if pagina == 1:
    st.subheader("Nome do projecto")
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

# Inserir imagens
if pagina == 2:
    st.subheader("Imagens 3D Top e Bottom view")
    with st.expander("Instruções de como captar as fotos"):
        st.caption("1) No Fusion, abrir a vista 3D da PCB.")
        st.caption("2) Começar por tirar uma captura de ecra à vista superior - TOP VIEW")
        st.caption("3) Tirar uma captura de ecra à vista inferior - BOTTOM VIEW")
        st.caption("4) Seleciomar as duas capturas de ecra e colar a baixo")

    pictures_3D_view = st.file_uploader("Adicionar capturas de ecra da vista TOP e BOTTOM da PCB", type="PNG", key="picture_3D", accept_multiple_files=True)
    if ss.picture_3D:
        ss.image_ref = ss.picture_3D  # backup
    
    if ss.image_ref:
        name_order = st.selectbox("SB_TB_View", ["Top / Bottom View", "Bottom / Top View"], key=[0,1], label_visibility="collapsed")
        for i in range(len(ss.image_ref)):   
            st.image(ss.image_ref[i], caption = ss.image_ref[i].name)

## Vista Silkscreen
if pagina == 3:
    st.subheader("PDF Silkscreen Top e Bottom view")
    with st.expander("Instruções para gerar Silkscreen Top e Bottom"):
        st.caption('1) No Fusion, abrir a vista "Layout"')
        st.caption('2) No separador "Display Layers" selecionar')
        st.caption('3) Clique em imprimir')
        st.caption('4) Nas configurações selecionar')
    
    # Access the uploaded ref via a key.
    st.file_uploader("Adicionar PDFs da vista silkscreen Top e Bottom view", type=('pdf'), key='pdf', accept_multiple_files=True)
    if ss.pdf:
        ss.pdf_ref = ss.pdf  # backup
    
    # Now you can access "pdf_ref" anywhere in your app.
    if ss.pdf_ref:
        for i in range(len(ss.pdf_ref)): 
            binary_data = ss.pdf_ref[i].getvalue()
            pdf_viewer(input=binary_data, width=700)
            st.caption(ss.pdf_ref[i].name)

# BOM file
if pagina == 4:
    st.subheader("Bill of Materials (BOM)")
    with st.expander("Instruções para gerar BOM"):
        st.caption('1) No Fusion, abrir a vista do Esquemático')
        st.caption('2) No campo "OUTPUT" clicar no primeiro simbolo que representa "Bill of Materials"')
        st.caption('3) Mudar o "List type" para "Values" e o "Output format" para CSV')
        st.caption('4) Pressione "Save" para guardar a BOM.csv')
    
    st.file_uploader("Adicionar BOM CSV file", key="bom_csv", type=('csv'))
    if ss.bom_csv:
        ss.bom_csv_ref =    bom_formatter(pd.read_csv(ss.bom_csv, sep = ";"))
     
    
    if not ss.bom_csv_ref.empty:
        st.caption("Ficheiro XLSL formatado (nota que poderá ser necessário colorir a tabela através do microsoft Excel)")
        df_edited = st.data_editor(
            ss.bom_csv_ref,
            use_container_width=True,
            column_config={
                "HANDLING": st.column_config.SelectboxColumn(
                    "HANDLING",
                    help="Select the handler",
                    width="medium",
                    options=[
                        "Assembler",
                        "Prozis"
                    ],
                    required=True,
                )}, hide_index=True)
        
        if st.button("Guardar alterações", use_container_width=True):
            ss.bom_csv_ref = df_edited
            st.success("Alterações guardadas")

# Pick and Place
if pagina == 5:
    st.subheader("Pick and Place")
    with st.expander("Instruções para gerar BOM"):
        st.caption('1) No Fusion, abrir a vista do Esquemático')
        st.caption('2) No campo "OUTPUT" clicar no primeiro simbolo que representa "Bill of Materials"')




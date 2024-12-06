
from pages.shared.shared import *
from controller.PCB_file_controller import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss
import pandas as pd
import io
import cv2
import numpy as np


numero_paginas = 6

if 'pagina_ref' not in ss:
    ss.pagina_ref = 1

if 'nome_projecto_ref' not in ss:
    ss.nome_projecto_ref = "pcb0000A_v0.0"

if 'image_ref' not in ss:
    ss.image_ref = None

if 'image_3D_order_ref' not in ss:
    ss.image_3D_order_ref = 0

if 'pdf_order_ref' not in ss:
    ss.pdf_order_ref = 0

if 'pdf_ref' not in ss:
    ss.pdf_ref = None

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


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.button("Anterior", key="pagina_anterior", use_container_width=True)
    if ss.pagina_anterior:
        if ss.pagina_ref > 1:
            ss.pagina_ref = ss.pagina_ref - 1
with col2:
    st.button("Seguinte", key="pagina_seguinte", use_container_width=True)
    if ss.pagina_seguinte:
        if ss.pagina_ref < numero_paginas:
            ss.pagina_ref = ss.pagina_ref + 1
with col5:
    if st.button("Download ZIP", use_container_width=True, type="primary", disabled = False):
        for i in range(7):
            print("Teste" + str(i))

# Progress bar
st.progress(ss.pagina_ref/numero_paginas, text=f'Etapas do processo: {ss.pagina_ref} /' + str(numero_paginas))


# Nome do projecto
if ss.pagina_ref == 1:
    st.subheader("Nome do projecto")
    st.caption('Inserir o Nome e Versão da PCB a produzir, separados por "_". Exemplo: "pcb0021B_V0.75')
    
    st.text_input("NomeProjecto", value = ss.nome_projecto_ref, key = "nome_projecto", placeholder='Nome projecto: "pcb0000_V0.0"', label_visibility="collapsed")
    if ss.nome_projecto:
        ss.nome_projecto_ref = ss.nome_projecto


# Inserir imagens
if ss.pagina_ref == 2:
    st.subheader("Imagens 3D Top e Bottom view")
    with st.expander("Instruções de como captar as fotos"):
        st.caption("1) No Fusion, abrir a vista 3D da PCB.")
        st.caption("2) Começar por tirar uma captura de ecra à vista superior - TOP VIEW")
        st.caption("3) Tirar uma captura de ecra à vista inferior - BOTTOM VIEW")
        st.caption("4) Seleciomar as duas capturas de ecra e colar a baixo")

    st.file_uploader("Adicionar capturas de ecra da vista TOP e BOTTOM da PCB", type="PNG", key="picture_3D", accept_multiple_files=True)
    if ss.picture_3D:
        ss.image_ref = ss.picture_3D  # backup
    
    if ss.image_ref:
        st.selectbox("SB_TB_3D_View", ["Top View / Bottom View", "Bottom View / Top View"], index= ss.image_3D_order_ref, key="image_3D_order", label_visibility="collapsed")
        if ss.image_3D_order:
            if ss.image_3D_order == "Top View / Bottom View":
                ss.image_3D_order_ref = 0
            else:
                ss.image_3D_order_ref = 1

        for i in range(len(ss.image_ref)):   
            st.image(ss.image_ref[i], caption = ss.image_ref[i].name)
        
        picture_file = ss.image_ref[0]
        buffer = io.BytesIO()
        file = picture_file.read()
        file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
        imageBGR = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageRGB)
        im_2 = Image.fromarray(imageBGR)
        im.save(buffer, format="PNG")
        im_2.save(buffer, format="PNG")
        
        st.download_button(
            label=f"Download",
            data=buffer, 
            file_name=f"Top_View.png",
            mime="image/png")
        
## Vista Silkscreen
if ss.pagina_ref == 3:
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
        st.selectbox("SB_TB_SLK_View", ["Top View / Bottom View", "Bottom View / Top View"], index= ss.pdf_order_ref, key="pdf_order", label_visibility="collapsed")
        if ss.pdf_order:
            if ss.pdf_order == "Top View / Bottom View":
                ss.pdf_order_ref = 0
            else:
                ss.pdf_order_ref = 1

        for i in range(len(ss.pdf_ref)): 
            binary_data = ss.pdf_ref[i].getvalue()
            pdf_viewer(input=binary_data, width=700)
            st.caption(ss.pdf_ref[i].name)

# BOM file
if ss.pagina_ref == 4:
    st.subheader("Bill of Materials (BOM)")
    with st.expander("Instruções para gerar BOM"):
        st.caption('1) No Fusion, abrir a vista do Esquemático')
        st.caption('2) No campo "OUTPUT" clicar no primeiro simbolo que representa "Bill of Materials"')
        st.caption('3) Mudar o "List type" para "Values" e o "Output format" para CSV')
        st.caption('4) Pressione "Save" para guardar a BOM.csv')
    
    st.file_uploader("Adicionar BOM CSV file", key="bom_csv", type=('csv'))
    if ss.bom_csv:
        ss.bom_csv_ref = bom_formatter(pd.read_csv(ss.bom_csv, sep = ";"))
    
    if not ss.bom_csv_ref.empty:
        col1,col2, col3 = st.columns([2,0.5,0.5])
        with col1:
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
        with col2:
            if st.button("Guardar", use_container_width=True, type="primary"):
                ss.bom_csv_ref = df_edited
        with col3:
            if st.button("Exportar", use_container_width=True, type="primary"):
                ""

# Pick and Place
if ss.pagina_ref == 5:
    st.subheader("Pick and Place")
    with st.expander("Instruções para gerar BOM"):
        st.caption('1) No Fusion, abrir a vista do Esquemático')
        st.caption('2) No campo "OUTPUT" clicar no primeiro simbolo que representa "Bill of Materials"')


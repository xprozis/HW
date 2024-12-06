
from pages.shared.shared import *
from controller.PCB_file_controller import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss


numero_paginas = 6

if 'pagina_ref' not in ss:
    ss.pagina_ref = 1

if 'nome_projecto_ref' not in ss:
    ss.nome_projecto_ref = "pcb000A_V0.0"

if 'all_files_ref' not in ss:
    ss.all_files_ref = None

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


st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="wide"
)

page_header("Ficheiros Produção PCB","Made by GOATs, for GOATs")

col1, col2 = st.columns([1,2])
with col1:
    st.text_input("NomeProjecto", value = ss.nome_projecto_ref, key = "nome_projecto", placeholder='Nome projecto: "pcb0000_V0.0"', label_visibility="collapsed")
    if ss.nome_projecto:
        ss.nome_projecto_ref = ss.nome_projecto
    st.caption('(Inserir o Nome e Versão da PCB a produzir, separados por "_". Exemplo: "pcb0021B_V0.75')

st.file_uploader("Adicionar todos os ficheiros gerados", type=['png','pdf','csv'], key="all_files", accept_multiple_files=True, label_visibility="collapsed")
if ss.all_files:
    ss.all_files_ref = ss.all_files

custom_single_space()

col1, col2 = st.columns(2, gap="medium")
with col1:
    st.subheader("Top_View, Bottom_View e Layer_stack")
    with st.expander("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):
        st.markdown("Adicionar capturas de ecra da vista TOP e BOTTOM da PCB")
        st.caption("1) No Fusion, abrir a vista 3D da PCB.")
        st.caption("2) Começar por tirar uma captura de ecra à vista superior - TOP VIEW")
        st.caption("3) Tirar uma captura de ecra à vista inferior - BOTTOM VIEW")
        st.caption("4) Seleciomar as duas capturas de ecra e colar a baixo")
    
    if ss.all_files_ref:
        pic_counter = 0
        for i in range(len(ss.all_files_ref)):
            if ss.all_files_ref[i].type == "image/png":
                pic_counter+=1
               
                col11, col22 = st.columns([2,1])
                with col11:
                   pic_name = st.selectbox("SB_Pictures_" + str(pic_counter), ["Top_View", "Bottom_View", "Layer_Stack"], label_visibility="collapsed")
                with col22:
                    download_button_image(ss.all_files_ref[i], "Guardar Imagem " + str(pic_counter), ss.nome_projecto_ref + "_" + str(pic_name) + ".png")
                st.image(ss.all_files_ref[i], caption = ss.all_files_ref[i].name)
                st.divider()
    else:
        st.caption("Sem ficheiros para mostrar")

with col2:
    st.subheader("Top_View_Silkscreen, Bottom_View_Silkcseen")
    with st.expander("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):
        st.markdown("Instruções para gerar Silkscreen Top e Bottom")
        st.caption('1) No Fusion, abrir a vista "Layout"')
        st.caption('2) No separador "Display Layers" selecionar')
        st.caption('3) Clique em imprimir')
        st.caption('4) Nas configurações selecionar')
    
    if ss.all_files_ref:
        pdf_counter = 0
        for i in range(len(ss.all_files_ref)):
            if ss.all_files_ref[i].type == "application/pdf":
                pdf_counter+=1
                col11, col22 = st.columns([2,1])
                with col11:
                    pdf_name = st.selectbox("SB_PDF_" + str(pdf_counter), ["Top_Silkscreen", "Bottom_Silkscreen"], label_visibility="collapsed")  
                with col22: 
                    download_button_pdf(ss.all_files_ref[i], "Guardar PDF " + str(pdf_counter), ss.nome_projecto_ref + "_" + str(pdf_name) + ".pdf")
                
                binary_data = ss.all_files_ref[i].getvalue()
                pdf_viewer(input=binary_data)
                st.caption(ss.all_files_ref[i].name)  
                st.divider()
    else:
        st.caption("Sem ficheiros para mostrar")
 
col1, col2 = st.columns(2, gap="medium")
with col1:
    st.subheader("BOM e Pick_and_Place")
    with st.expander("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):  
        st.markdown("Instruções para gerar BOM")
        st.caption('1) No Fusion, abrir a vista do Esquemático')
        st.caption('2) No campo "OUTPUT" clicar no primeiro simbolo que representa "Bill of Materials"')
        st.caption('3) Mudar o "List type" para "Values" e o "Output format" para CSV')
        st.caption('4) Pressione "Save" para guardar a BOM.csv')
    
    if ss.all_files_ref:
        csv_counter = 0
        for i in range(len(ss.all_files_ref)):
            if ss.all_files_ref[i].type == "text/csv":
                csv_counter+=1
                csv_to_df = pd.read_csv(ss.all_files_ref[i], sep = ";")
                
                type, data = df_checker(csv_to_df)

                col11, col22 = st.columns([2,1])
                with col22:
                    download_button_pdf(ss.all_files_ref[i], "Guardar XSLX " + str(csv_counter), ss.nome_projecto_ref + "_" + type + ".xlsx")
                
                st.data_editor(
                    data = data,
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
                st.caption("Ficheiro XLSL formatado (nota que poderá ser necessário colorir a tabela através do microsoft Excel)")
                
              
                st.divider()
            
    else:
        st.caption("Sem ficheiros para mostrar")


with col2:
    st.subheader("Ficheiro Read Me")
    if ss.all_files_ref:
        st.text_area("")
    else:
        st.divider()
        st.caption("Sem ficheiros para mostrar")
      
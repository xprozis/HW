
from pages.shared.shared import *
from controller.PCB_file_controller import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss

sem_dados_texto = "Carregar ficheiros para mostrar"
numero_paginas = 6

if 'pagina_ref' not in ss:
    ss.pagina_ref = 1

if 'nome_projecto_ref' not in ss:
    ss.nome_projecto_ref = "pcb000A_V0_0"

if 'all_files_ref' not in ss:
    ss.all_files_ref = None


st.set_page_config(
    page_title="PROZIS HW File",
    page_icon="🔴",
    layout="wide"
)

page_header("Ficheiros Produção PCB","Made by GOATs, for GOATs")


col1, col2 = st.columns([1,2])
with col1:
    st.text_input('Inserir o Nome e Versão da PCB a produzir, separados por "_". Exemplo: "XBAND_pcb0021B_V0_7', value = ss.nome_projecto_ref, key = "nome_projecto", placeholder='Nome projecto: "pcb0000_V0.0"')
    if ss.nome_projecto:
        ss.nome_projecto_ref = ss.nome_projecto
    st.file_uploader("Adicionar todos os ficheiros gerados", type=['png','pdf','csv'], key="all_files", accept_multiple_files=True, label_visibility="collapsed")
    if ss.all_files:
        ss.all_files_ref = ss.all_files
    
custom_single_space()

col1, col2 = st.columns(2, gap="medium")
with col1:
    st.subheader("Top_View, Bottom_View e Layer_stack")
    with st.popover("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):
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
                    st.download_button(label="Guardar Imagem " + str(pic_counter), data=ss.all_files_ref[i], file_name= ss.nome_projecto_ref + "_" + str(pic_name) + ".png" ,mime="image/png", type="primary", use_container_width=True)                 
                st.image(ss.all_files_ref[i], caption = ss.all_files_ref[i].name)
                custom_single_space()
    else:
        custom_single_space()

with col2:
    st.subheader("Top_View_Silkscreen, Bottom_View_Silkcseen")
    with st.popover("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):
        
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
                    file = ss.all_files_ref[i].read()
                    st.download_button(label= "Guardar PDF " + str(pdf_counter),data=file, file_name= ss.nome_projecto_ref + "_" + str(pdf_name) + ".pdf",mime="application/pdf", type="primary", use_container_width=True)
                binary_data = ss.all_files_ref[i].getvalue()
                pdf_viewer(input=binary_data)
                st.caption(ss.all_files_ref[i].name)  
                custom_single_space()
    else:
        custom_single_space()


st.divider()
st.subheader("BOM e Pick_and_Place")
with st.popover("⚙️ Expandir para obter mais informações à cerca dos ficheiros necessários"):  
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

            col11, col22 = st.columns([3,1])
            data_edited = st.data_editor(
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
            

            with col22:
                if type == "BOM":
                    st.download_button(label="Guardar XLSX " + str(csv_counter), data=df_to_excel_data(data_edited), file_name= ss.nome_projecto_ref + "_" + str(type) + ".xlsx",mime="application/vnd.ms-excel", use_container_width=True, type="primary")
                if type == "Pick_and_Place":
                    csv = data.to_csv(index=False).encode('utf-8')
                    st.download_button("Guardar CSV " + str(csv_counter),csv, ss.nome_projecto_ref + "_" + str(type) + ".csv","text/csv",key='download-csv', use_container_width=True, type="primary")
                    
            st.caption("Ficheiro XLSL formatado (nota que poderá ser necessário colorir a tabela através do microsoft Excel)")  
            custom_single_space()
        
else:
    custom_single_space()


st.divider()
st.subheader("Ficheiro Read Me")
if ss.all_files_ref:
    template_type = st.selectbox("Selecionar template a usar", ["2 Layer", "4 Layer"])
    with st.expander("Expandir para ver ficheiro Readme.txt"):
        st.text("Teste")
else:
    st.divider()
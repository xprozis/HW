
from pages.shared.shared import *
from controller.PCB_file_controller import *
from streamlit_pdf_viewer import pdf_viewer
from streamlit import session_state as ss
import mitosheet.streamlit.v1 as mt

sem_dados_texto = "Carregar ficheiros para mostrar"
numero_paginas = 6

if 'pagina_ref' not in ss:
    ss.pagina_ref = 1

if 'nome_pcb_ref' not in ss:
    ss.nome_pcb_ref = "pcb000A_V0_0"


if 'all_files_ref' not in ss:
    ss.all_files_ref = None

im = Image.open("./pages/shared/p_logo.ico")

st.set_page_config(
    page_title="Ficheiros Produção PCB",
    page_icon=im,
    layout="wide"
)


page_header("Ficheiros Produção PCB", "Made by GOATs, for GOATs")


col1, col2 = st.columns([1,2])
with col1:
    st.text_input('Inserir o Nome e Versão da PCB a produzir, separados por "_". Exemplo: "pcb0021B_V0_7', value = ss.nome_pcb_ref, key = "nome_projecto_pcb", placeholder='Nome projecto: "pcb0000_V0.0"')
    if ss.nome_projecto_pcb:
        ss.nome_pcb_ref = ss.nome_projecto_pcb

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
                    pic_name = st.selectbox("SB_Pictures_" + str(pic_counter), ["View_Top", "View_Bottom", "Layer_Stack"], label_visibility="collapsed")
                with col22:
                    st.download_button(label="Guardar Imagem " + str(pic_counter), data=ss.all_files_ref[i], file_name= ss.nome_pcb_ref + "_" + str(pic_name) + ".png" ,mime="image/png", type="primary", use_container_width=True)                 
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
                    pdf_name = st.selectbox("SB_PDF_" + str(pdf_counter), ["Silkscreen_Top", "Silkscreen_Bottom"], label_visibility="collapsed")  
                with col22: 
                    file = ss.all_files_ref[i].read()
                    st.download_button(label= "Exportar PDF " + str(pdf_counter),data=file, file_name= ss.nome_pcb_ref + "_" + str(pdf_name) + ".pdf",mime="application/pdf", type="primary", use_container_width=True)
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
            

            if type == "BOM":
                
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
                st.caption("Dados da BOM com coluna selecionadas e ordenadas. Ficheiro XLSL formatado (nota que poderá ser necessário colorir a tabela através do microsoft Excel)")  
                with col22:
                    st.download_button(label="Exportar XLSX " + str(csv_counter), data=df_to_excel_data(data_edited), file_name= ss.nome_pcb_ref + "_" + str(type) + ".xlsx",mime="application/vnd.ms-excel", use_container_width=True, type="primary")
                 
            
            if type == "Pick_and_Place":
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
            
                st.caption("Dados do Pick and Place com a informação relativa ao frame removida")
                with col22:
                    csv = data.to_csv(index=False).encode('utf-8')
                    st.download_button("Guardar CSV " + str(csv_counter),csv, ss.nome_pcb_ref + "_" + str(type) + ".csv","text/csv",key='download-csv', use_container_width=True, type="primary")
            
            st.divider()
        
else:
    custom_single_space()


st.divider()
st.subheader("Ficheiro Read Me")

col1, col2 = st.columns([3,1])
my_readme_2_layer = f"""_ Production Files
Includes:
Assembly data:
    . Bill of materials - Assembly/{ss.nome_pcb_ref}_bom.xlsx
    . Pick and Place - Assembly/{ss.nome_pcb_ref}_pick_and_place.csv
    . Silkscreen file top - Assembly/{ss.nome_pcb_ref}_silkscreen_top
    . Silkscreen file bottom - Assembly/{ss.nome_pcb_ref}_silkscreen_bottom
Manufacturing Data:
    . Gerbers and drill map - Gerbers/{ss.nome_pcb_ref}_.zip
    . Layer stack - Gerbers/layer_stack.png
    
PCB information:
    . Layers: _
    . Material: FR4
    . PCB dimension: _ x _ mm
    . Layer stack:
        - Outer layers copper: _ um
        - Prepreg thickness: _ um
        - Core thickness: _ mm
        - Total board final thickness: _ mm
    . Vias:
        - Through hole (layers 1-16)
        - Blind vias
            - layers 1-16
        - Vias in SM pads - needs filling - suggest material

    . Relative dielectric constant: 4.5
    . Soldermask: Top and bottom green
    . Silkscreen: Top and bottom white
    . SM Components: Bottom
    . Special milling:
        - _
        
Additional information:
    . Bill of materials file include a column with title "handling" with variables "Prozis" and "Assembler":
        - Components marked "Prozis" will be delivered by Prozis to assembler and components marked with "Assembler" must be provided by assembler
"""
st.text_area("Ficheiro txt gerado", height=900, value = my_readme_2_layer, label_visibility="collapsed")

with col2:
    st.download_button("Exportar Readme", file_name="Readme.txt", data=my_readme_2_layer, use_container_width=True, type="primary")
import pandas as pd
from PIL import Image
import streamlit as st
import io


def custom_single_space():
    """
        Funcao que gera um espaço entre items
    """
    st.markdown("")


def pickplace_formatter(df):
    """
        Filtro de CSV file
    """
    #df = df[~df['RefDes,Layer,LocationX,LocationY,Rotation'].str.contains('FID')]
    df = df[~df['RefDes,Layer,LocationX,LocationY,Rotation'].str.contains('FRAME')]
    return df


def bom_formatter(df):
    """
        Formatador de dataframe
    """

    # Constroi a tabela
    df_formated = pd.DataFrame()
    df_formated["Qty"] = df["Qty"]
    df_formated["REF"] = df["REF"]
    df_formated["DESCRIPTION"] =  df["DESCRIPTION"]
    df_formated["Parts"] = df["Parts"]
    df_formated["1_MPN"] = df["1_MPN"]
    df_formated["1_MANUFACTURER"] = df["1_MANUFACTURER"]
    df_formated["2_MPN"] = df["2_MPN"]
    df_formated["2_MANUFACTURER"] = df["2_MANUFACTURER"]
    df_formated["3_MPN"] = df["3_MPN"]
    df_formated["3_MANUFACTURER"] = df["3_MANUFACTURER"]
    
    # Configura o HANDLING entre Assembler ou Prozis
    df_formated["HANDLING"] = "Prozis"
    df_formated['HANDLING'][df_formated['Parts'].str.contains('R1')] = "Assembler"
    df_formated['HANDLING'][df_formated['Parts'].str.contains('C1')] = "Assembler"

    # Remove fiduciais e frames
    df_formated = df_formated[~df_formated['Parts'].str.contains('FID1')]
    df_formated = df_formated[~df_formated['Parts'].str.contains('FRAME1')]

    # Ordena a coluna HANDLING
    df_formated = df_formated.sort_values("HANDLING", ascending=True)
    return df_formated


def df_checker(df):
    """
        Verifica o numero de colunas, se for 1 é o Pick and Place se for mais é a BOM
    """
    if len(df.columns) == 1:
        
        return "Pick_and_Place", pickplace_formatter(df)

    else:
        return "BOM", bom_formatter(df)
    

def df_to_excel_data(df):
    """
        Converte dataframe para um ficheio excel
    """
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Workbook
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    format1 = workbook.add_format({'num_format': '0'}) 
    worksheet.set_column('A:A', None, format1)
    worksheet.autofit()
    
    writer.close()
    processed_data = output.getvalue()
    return processed_data


import pandas as pd
from PIL import Image
import streamlit as st



project_dic = {
  "nome_projecto": "pcb0000",
  "versao_projecto": "0.0",
}

silk_top = 0
silk_bottom = 0

def define_variables():
    global project_dic

def bom_formatter(df):
    """
        Formatador de dataframe
    """
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
    df_formated["HANDLING"] = "Assembler"

    df_formated = df_formated[~df_formated['Parts'].str.contains('FID1')]
    df_formated = df_formated[~df_formated['Parts'].str.contains('FRAME1')]
    return df_formated


def load_image(image_file):
    img = Image.open(image_file)
    return img
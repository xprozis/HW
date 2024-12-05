import pandas as pd

pagina = 1
numero_paginas = 6

project_dic = {
  "nome_projecto": "pcb0000",
  "versao_projecto": "0.0",
}

silk_top = 0
silk_bottom = 0

def define_variables():
    global project_dic

def nav_back():
    global pagina
    if pagina > 1:
        pagina+=-1

def nav_foward():
    global pagina
    if pagina < numero_paginas:
        pagina+=1


def bom_formatter(df):
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
    
    return df_formated
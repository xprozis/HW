import pandas as pd
from PIL import Image
import streamlit as st
import io
import cv2
import numpy as np


def custom_single_space():
    st.markdown("")

def pickplace_formatter(df):
    df = df[~df['RefDes,Layer,LocationX,LocationY,Rotation'].str.contains('FID')]
    df = df[~df['RefDes,Layer,LocationX,LocationY,Rotation'].str.contains('FRAME')]
    return df


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

def df_checker(df):
    """
        Verifica o numero de colunas, se for 1 é o Pick and Place se for mais é a BOM
    """
    if len(df.columns) == 1:
        
        return "PicK_and_Place", pickplace_formatter(df)

    else:
        return "BOM", bom_formatter(df)
    

def load_image(image_file):
    img = Image.open(image_file)
    return img

def download_button_image(file,label_btn,file_name):
    buffer = io.BytesIO()
    file = file.read()
    file_bytes = np.asarray(bytearray(file), dtype=np.uint8)
    imageBGR = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    imageRGB = cv2.cvtColor(imageBGR , cv2.COLOR_BGR2RGB)
    im = Image.fromarray(imageRGB)
    im.save(buffer, format="PNG")
    st.download_button(label=label_btn,data=buffer, file_name=file_name,mime="image/png", type="primary", use_container_width=True)


def download_button_pdf(file,label_btn,file_name):
    file = file.read()
    st.download_button(label=label_btn,data=file, file_name=file_name,mime="application/pdf", type="primary", use_container_width=True)


def download_button_xsls(file,label_btn,file_name):
    file = file.read()
    st.download_button(label=label_btn,data=file, file_name=file_name,mime="text/xlsx", type="primary", use_container_width=True)
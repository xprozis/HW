pagina = 1
numero_paginas = 6

project_dic = {
  "nome_projecto": "pcb0000",
  "versao_projecto": "0.0",
}

pictures_3D_saved = []
picture3D_name = 0

silk_top = 0
silk_bottom = 0

def define_variables():
    global project_dic
    global pictures_3D


def nav_back():
    global pagina
    if pagina > 1:
        pagina+=-1

def nav_foward():
    global pagina
    if pagina < numero_paginas:
        pagina+=1


def picture3D_save(files,name):
    global pictures_3D_saved
    global picture3D_name

    pictures_3D_saved = files
    picture3D_name = name
   


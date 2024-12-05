pagina = 1
numero_paginas = 5

project_dic = {
  "nome_projecto": "pcb000",
  "versao_projecto": "0.0",
}


def define_dic():
    global project_dic


def nav_back():
    global pagina
    if pagina > 1:
        pagina+=-1

def nav_foward():
    global pagina
    if pagina < numero_paginas:
        pagina+=1



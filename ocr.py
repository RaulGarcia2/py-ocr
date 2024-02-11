#!/bin/env python3
import PySimpleGUI as sg
from PIL import Image
import tempfile
import os
import os.path
import io
import sys

def eventoFileList(values, ventana):
    try:
        filename = os.path.join( values["-FOLDER-"], values["-FILE LIST-"][0])
        image = Image.open(filename)
        image.thumbnail(tamano)
        bio = io.BytesIO()
        image.save(bio, format="PNG")

        ventana["-TOUT-"].update(filename)
        ventana["-IMAGE-"].update(data=bio.getvalue())
    except:
        pass

def eventoFolder(values, ventana):
    folder = values["-FOLDER-"]
    try:
        file_list = os.listdir(folder)
    except:
        file_list =[]

    fnames = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder, f))
        and f.lower().endswith((".png",".gif"))
    ]

    ventana["-FILE LIST-"].update(fnames)

def salvarFicharo(texto, nombrefichero):
    f=open(nombrefichero, 'w')
    f.write(texto)
    f.close()

def convertir(imagen, panel_resultado):
    # Implementar la lógica de conversión
    t=tempfile.NamedTemporaryFile()
    salidatmp=t.name

    #El comando que nos convierte el fichero a un texto en español
    comando='/usr/bin/tesseract  -l spa "{}" {}'.format(imagen, salidatmp)
    os.system(comando)

    #El programa tesseract nos crea un fichero con extensión txt
    salidatmp += '.txt'

    with  open(salidatmp, 'r') as f:
        contenido=f.read()

    panel_resultado.update(contenido)
    f.close()
    t.close()

    #Eliminamos el fichero temporal con el texto
    os.unlink(salidatmp)

if len(sys.argv) > 1:
    carpeta=os.path.dirname(sys.argv[1])
    nombrefichero=os.path.basename(sys.argv[1])
else:
    carpeta=''
    nombrefichero=''

tamano=(600,400)

tCarpeta=sg.In(carpeta, size=(25,1), enable_events=True, key="-FOLDER-")
lFicheros = sg.Listbox(
                values=[], enable_events=True, size=(40,20),
                key="-FILE LIST-")
#bSalvar = sg.FileSaveAs("Salvar a fichero...", initial_folder=carpeta, file_types=(('Text', '.txt'),), key="-ABRESAVE-", enable_events=True),
#bSalvar = sg.FileSaveAs("Salvar a fichero...", file_types=(('Text', '.txt'),), key="-ABRESAVE-", enable_events=True),
if carpeta == "":
    initial_folder=os.getcwd()
else:
    initial_folder=carpeta

lista_ficheros_columna = [
        [
            sg.Text("Directorio de imágenes"),
            tCarpeta,
            sg.FolderBrowse(button_text="Selecciona carpeta...")
            ],
        [ lFicheros ]
        ]

visor_imagen_columna = [
        [sg.Text("Elije imagen para ver:")],
        [sg.Text(size=(100,1), key="-TOUT-")],
        [sg.Frame("", [[sg.Image(key="-IMAGE-", size=tamano)]], size=tamano)],
        [
            sg.Button("Convertir", key="-CONVERT-"), 
            sg.In("", size=(25,1), visible=False, key="-SAVETXT-", enable_events=True),
            sg.FileSaveAs("Salvar a fichero...", initial_folder=initial_folder, file_types=(('Text', '.txt'),), key="-ABRESAVE-", enable_events=True),
            sg.Button("Salir", key="-SALIR-", enable_events=True)
            ],
        [sg.Multiline(size=(100,20), background_color="#eeeeee", key="-SALIDA-")],
        ]

layout = [
        [
            sg.Column(lista_ficheros_columna),
            sg.VSeparator(),
            sg.Column(visor_imagen_columna)
            ]
        ]

ventana = sg.Window("Visualizador", layout)

if carpeta != '':
    event, values = ventana.read()
    eventoFolder(values, ventana)
    lFicheros.update(set_to_index=lFicheros.get_list_values().index(nombrefichero))
    event, values = ventana.read()
    eventoFileList(values, ventana)

while True:
    event, values = ventana.read()

    if event == "Exit"  or event == sg.WIN_CLOSED or event == "-SALIR-":
        break
    if event == "-FOLDER-":
        eventoFolder(values, ventana)
    elif event == "-SAVETXT-" and values["-SAVETXT-"] != "":
        contenido = values["-SALIDA-"]
        ficheroS = values["-SAVETXT-"]
        if ficheroS:
            #ventana["-SAVETXT-"].update(value=ficheroS)
            salvarFicharo(contenido, ficheroS)

    elif event == "-ABRESAVE-":
        ventana["-SAVETXT-"].update("")

    elif event == "-CONVERT-":
        fichero = os.path.join( values["-FOLDER-"], values["-FILE LIST-"][0])
        convertir(fichero, ventana["-SALIDA-"])
    elif event == "-FILE LIST-":
        eventoFileList(values, ventana)

ventana.close()



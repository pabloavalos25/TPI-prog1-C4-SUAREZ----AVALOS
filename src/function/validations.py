import csv
import os

from base_dato import *

def inicializar_archivo():
    if not os.path.exists("paises.csv"):
        with open("paises.csv","w", encoding='UTF-8', newline="") as archivo:
            encabezado=['nombre','poblacion','superficie','continente']
            escritor = csv.DictWriter(archivo,filedname=encabezado)
            escritor.writeheader()
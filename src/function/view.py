
import csv
import os


def listar_archivo(directorio):
    for elemento in os.listdir(directorio):
        ruta = os.path.join(directorio, elemento)
        if os.path.isdir(ruta):
            print(f"Directorio: {elemento}")
            listar_archivo(ruta)
        else:
            print(f"Archivo: {elemento}")

listar_archivo('./src')

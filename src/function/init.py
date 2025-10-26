
import os
import shutil  
import csv
from function.tools import *


def gestionar_db(directorio_base, ruta_objetivo):
    ruta_objetivo_norm = os.path.normpath(ruta_objetivo)

    if os.path.isfile(ruta_objetivo_norm):
        limpiar_consola()
        print("******************************")
        print(f"🆙 Iniciando aplicacion...")
        print(f"✅ Sistema cargado")
        return ruta_objetivo_norm
    limpiar_consola()
    print("************************************************************************************") 
    print(f"Archivo no encontrado en '{ruta_objetivo_norm}'.")
    print(f"Buscando en todo el proyecto ('{directorio_base}')...")
    ruta_encontrada = None

    for dirpath, dirnames, filenames in os.walk(directorio_base):
        if "paises.csv" in filenames:

            ruta_encontrada = os.path.normpath(os.path.join(dirpath, "paises.csv"))

            if ruta_encontrada != ruta_objetivo_norm:
                limpiar_consola()
                print("****************************************************")                
                print("⚠️ ¡Archivo encontrado en una ubicación incorrecta! ")
                try:
                    os.makedirs(os.path.dirname(ruta_objetivo_norm), exist_ok=True)
                    shutil.move(ruta_encontrada, ruta_objetivo_norm)
                    
                    print(f"📦 Archivo movido exitosamente a: {ruta_objetivo_norm}")
                    
                    print("****************************************************")
                    print(f"🆙 Iniciando aplicacion...")
                    print(f"✅ Sistema cargado")
                    return ruta_objetivo_norm 
                    
                except Exception as e:
                    print(f"❌ ERROR: No se pudo mover el archivo. Error: {e}")
                    return None
            else:
                print(f"✅ Archivo 'paises.csv' localizado en la ruta correcta: {ruta_encontrada}")
                return ruta_encontrada
    print(f"❌ ERROR: El archivo 'paises.csv' no se encontró en ningún directorio del proyecto.")
    print(f"Creando archivo en la ruta objetivo: {ruta_objetivo_norm}")
    try:
        os.makedirs(os.path.dirname(ruta_objetivo_norm), exist_ok=True)
        with open(ruta_objetivo_norm, 'w', newline='', encoding='utf-8-sig') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(["nombre","poblacion","superficie","continente"])
        print(f"📄 Archivo 'paises.csv' creado correctamente en: {ruta_objetivo_norm} ")
        print("Se creo solo con su encabezado nombre, poblacion, superficie, continente")
        print("Por favor, ingresar los datos manualmente en el archivo csv.")
        print("************************************************************************************") 


        print(f"✅ Iniciando aplicacion")
        return ruta_objetivo_norm
    except Exception as e:
        print("****************************************************")         
        print(f"❌ ERROR: No se pudo crear el archivo. Error: {e}")
        return None

RUTA_CORRECTA_DB = 'src/db/paises.csv'

def init_db(project_root):
    db_path = gestionar_db(project_root, RUTA_CORRECTA_DB)
    if db_path is None:
        print("****************************************************")         
        print("No se pudo preparar la base de datos. Saliendo.")
        return None
    return db_path


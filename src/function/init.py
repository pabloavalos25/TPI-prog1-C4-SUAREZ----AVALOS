
import os
import shutil  


def gestionar_db(directorio_base, ruta_objetivo):
    ruta_objetivo_norm = os.path.normpath(ruta_objetivo)

    if os.path.isfile(ruta_objetivo_norm):
        print(f"✅ Archivo 'paises.csv' encontrado en la ubicación correcta.")
        return ruta_objetivo_norm

    print(f"Archivo no encontrado en '{ruta_objetivo_norm}'.")
    print(f"Buscando en todo el proyecto ('{directorio_base}')...")
    ruta_encontrada = None

    for dirpath, dirnames, filenames in os.walk(directorio_base):
        if "paises.csv" in filenames:

            ruta_encontrada = os.path.normpath(os.path.join(dirpath, "paises.csv"))

            if ruta_encontrada != ruta_objetivo_norm:
                print(f"⚠️ ¡Archivo encontrado en una ubicación incorrecta!: {ruta_encontrada}")
                
                try:
                    os.makedirs(os.path.dirname(ruta_objetivo_norm), exist_ok=True)
                    shutil.move(ruta_encontrada, ruta_objetivo_norm)
                    
                    print(f"📦 Archivo movido exitosamente a: {ruta_objetivo_norm}")
                    return ruta_objetivo_norm 
                    
                except Exception as e:
                    print(f"❌ ERROR: No se pudo mover el archivo. Error: {e}")
                    return None
            else:
                print(f"✅ Archivo 'paises.csv' localizado en la ruta correcta: {ruta_encontrada}")
                return ruta_encontrada

    print(f"❌ ERROR: El archivo 'paises.csv' no se encontró en ningún directorio del proyecto.")
    return None

RUTA_CORRECTA_DB = 'src/db/paises.csv'

path_del_archivo = gestionar_db('./', RUTA_CORRECTA_DB)


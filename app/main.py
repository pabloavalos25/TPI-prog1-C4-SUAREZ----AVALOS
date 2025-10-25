import sys
import os
import csv
import unicodedata

script_path = os.path.abspath(__file__)
app_dir = os.path.dirname(script_path)
project_root = os.path.dirname(app_dir)
src_dir = os.path.join(project_root, 'src')

if project_root not in sys.path:
    sys.path.append(project_root)
if src_dir not in sys.path:
    sys.path.append(src_dir)

try:
    from function.init import init_db
    from function.view import *
    from function.statistics import *
    from function.tools import *
    from function.data_load import *
    from function.shearch import *
except ImportError:
    print(f"Error: No se pudo importar 'gestionar_db' desde 'function.init'.")
    print(f"Raíz del proyecto calculada: {project_root}")
    sys.exit(1) 

db_path = init_db(project_root)
if db_path is None:
    sys.exit(1)
paises = leer_csv(db_path)

def main():
 
    while True:
        try:
            print("*****INFO GEOGRAFICO*****")
            print("1. Buscar pais por nombre")
            print("2. Filtrar por continente")
            print("3. Filtrar por rango de poblacion")
            print("4. Filtrar por rango de superficie")
            print("5. Ordenar paises")
            print("6. Mostrar estadisticas")
            print("7. Agregar un pais")
            print("8. Editar poblacion y superficie de un pais")
            print("9. Salir")
                        
            opcion=int(input("Ingrese una opcion 1-9: "))
            print("************************")

            match opcion:
                case 1:
                        nombre=input("Ingrese el nombre del pais o parte del nombre del pais: ").lower()
                        buscar_pais(paises, nombre)
                case 2:
                        continente= input("Ingrese el nombre del continente: ").capitalize().strip()
                        filtrar_continente(paises, continente)
                case 3:
                        filtrar_poblacion(paises)
                case 4:
                        filtrar_superficie(paises)
                case 5:
                        campo = input("Campo para ordenar (nombre/poblacion/superficie): ").lower()
                        desc_input = input("¿Querés orden descendente? (s/n): ").strip().lower()
                        descendente = (desc_input == 's')
                        ordenar_paises(paises, campo, descendente)
                case 6:
                        mostrar_estadisticas(paises)
                case 7:
                        agregar_pais(paises)
                        escribir_csv(db_path, paises)
                case 8:
                        editar_pais(paises)
                        escribir_csv(db_path, paises)
                case 9:
                        print("Saliendo del programa")
                        break  
                case _:
                    print("Opcion incorrecta")
        except ValueError:
                print("Error")
                
if __name__ == '__main__':
    main()
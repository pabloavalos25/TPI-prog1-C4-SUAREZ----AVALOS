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
    PAISES = "./src/db/paises.csv"
    paises=leer_csv(PAISES)
    

except ImportError:
    print(f"Error: No se pudo importar 'gestionar_db' desde 'function.init'.")
    sys.exit(1) 

db_path = init_db(project_root)
if db_path is None:
    sys.exit(1)

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
                        descendente = input("¿Querés orden descendente? (s/n): ").lower()
                        ordenar_paises(paises, campo, descendente)
                case 6:
                        mostrar_estadisticas(paises)
                case 7:
                        agregar_pais(paises)
                case 8:
                        editar_pais(paises)
                case 9:
                        print("Saliendo del programa")
                        break  
                case _:
                    print("Opcion incorrecta")
        except ValueError:
                print("Error")
                
if __name__ == '__main__':
    main()
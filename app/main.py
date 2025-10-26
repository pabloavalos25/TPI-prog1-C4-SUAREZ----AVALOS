import sys
import os

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
        from function.view import *
        from function import api_client
        from function.api_mode import *


except ImportError:
        print(f"Error: No se pudo importar 'gestionar_db' desde 'function.init'.")
        print(f"Raíz del proyecto calculada: {project_root}")
        sys.exit(1) 

db_path = init_db(project_root)
if db_path is None:
        sys.exit(1)
        
paises = leer_csv(db_path)


MODO_API = False

def elegir_modo():
        global MODO_API
        print("****Menu****")
        print("1) CSV local")
        print("2) API en servidor")
        op = input("Elegí 1 o 2 [1]: ").strip()
        MODO_API = (op == "2")
        if MODO_API:
                try:
                        api_client.health()
                        print("**********************************")
                        print("🟢  Ingreso por API ")
                        print("☁️   Servidor nube ")
                        print("🌍  Url: http://149.50.150.15:8000")
                        print("***********************************")
                except Exception as e:
                        print("Advertencia: /health no respondió:", e)
        else:
                try:
                        print("**********************************")
                        print("🟢  Ingreso Modo Local ")
                        print("💻  Servidor Fisico ")
                        print("***********************************")
                except Exception as a:
                        print("Advertencia: /health no respondió:", a)
elegir_modo()

def main():
        while True:
                try:      
                        print("**********INFO GEOGRAFICO**********")
                        print("1. Buscar pais por nombre")
                        print("2. Filtrar por continente")
                        print("3. Filtrar por rango de poblacion")
                        print("4. Filtrar por rango de superficie")
                        print("5. Ordenar paises")
                        print("6. Mostrar estadisticas")
                        print("7. Agregar un pais")
                        print("8. Editar poblacion y superficie de un pais")
                        print("9. Borrar país")
                        print("10. Salir")
                        
                        opcion=int(input("Ingrese una opcion 1-10: "))
                        print("***********************************")

                        match opcion:
                                case 1:
                                        nombre=input("Ingrese el nombre del pais o parte del nombre del pais: ").lower()
                        
                                        if MODO_API:
                                                buscar_pais_api(nombre)
                                        else:
                                                buscar_pais(paises, nombre)
                                case 2:
                                        continente= input("Ingrese el nombre del continente: ").capitalize().strip()
                                        if MODO_API:
                                                filtrar_continente_api(continente)
                                        else:
                                                filtrar_continente(paises, continente)
                                case 3:
                                        if MODO_API:
                                                filtrar_poblacion_api()
                                        else:
                                                filtrar_poblacion(paises)
                                case 4:
                                        if MODO_API:
                                                filtrar_superficie_api()
                                        else:
                                                filtrar_superficie(paises)
                                case 5:
                                        campo = input("Campo para ordenar (nombre/poblacion/superficie): ").lower()
                                        desc_input = input("¿Querés orden descendente? (s/n): ").strip().lower()
                                        descendente = (desc_input == 's')
                                        if MODO_API:
                                                ordenar_paises_api(campo, descendente)
                                        else:
                                                ordenar_paises(paises, campo, descendente)
                                case 6:
                                        if MODO_API:
                                                estadisticas_api()
                                        else:
                                                mostrar_estadisticas(paises)
                                case 7:
                                        if MODO_API:
                                                agregar_pais_api()
                                        else:
                                                agregar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 8:
                                        if MODO_API:
                                                editar_pais_api()
                                        else:
                                                editar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 9:
                                        if MODO_API:
                                                
                                                borrar_pais_api()
                                        else:
                                                
                                                if borrar_pais(paises):
                                                        escribir_csv(db_path, paises)
                                case 10:
                                        print("Saliendo del programa")
                                        break  
                                case _:
                                        print("Opcion incorrecta")
                except ValueError:
                        print("Error")
                
if __name__ == '__main__':
        main()
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
        from function.validations import *


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
        while True:
                global MODO_API
                try:                        
                        op=seleccion()                      
                        match op:
                                case 1:
                                        try:
                                                limpiar_consola()
                                                local()
                                                break
                                        except Exception as c:
                                                limpiar_consola()
                                                except_local(c)
                                case 2:
                                        MODO_API = True
                                        try:
                                                limpiar_consola()
                                                api_client.health()
                                                nube()
                                                break
                                        except Exception as b:
                                                limpiar_consola()
                                                error_server()
                                case 3:
                                        limpiar_consola()
                                        salida()
                                        sys.exit(0)
                                case _:
                                        limpiar_consola()
                                        error_tipeo(op)
                except ValueError as a:
                        limpiar_consola()
                        except_men_server()
                        
elegir_modo()

def main():
        while True:
                try: 
                        opcion=menu_principal()
                        match opcion:
                                case 1:
                                        limpiar_consola()
                                        nombre=input("Ingrese el nombre del pais o parte del nombre del pais: ").lower()
                        
                                        if MODO_API:
                                                buscar_pais_api(nombre)
                                        else:
                                                buscar_pais(paises, nombre)
                                case 2:
                                        limpiar_consola()
                                        continente= input("Ingrese el nombre del continente: ").capitalize().strip()
                                        if MODO_API:
                                                filtrar_continente_api(continente)
                                        else:
                                                filtrar_continente(paises, continente)
                                case 3:
                                        limpiar_consola()
                                        if MODO_API:
                                                filtrar_poblacion_api()
                                        else:
                                                filtrar_poblacion(paises)
                                case 4:
                                        limpiar_consola()
                                        if MODO_API:
                                                filtrar_superficie_api()
                                        else:
                                                filtrar_superficie(paises)
                                case 5:
                                        limpiar_consola()
                                        campo = input("Campo para ordenar (nombre/poblacion/superficie): ").lower()
                                        desc_input = input("¿Querés orden descendente? (s/n): ").strip().lower()
                                        descendente = (desc_input == 's')
                                        if MODO_API:
                                                ordenar_paises_api(campo, descendente)
                                        else:
                                                ordenar_paises(paises, campo, descendente)
                                case 6:
                                        limpiar_consola()
                                        if MODO_API:
                                                estadisticas_api()
                                        else:
                                                mostrar_estadisticas(paises)
                                case 7:
                                        limpiar_consola()
                                        if MODO_API:
                                                agregar_pais_api()
                                        else:
                                                agregar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 8:
                                        limpiar_consola()
                                        if MODO_API:
                                                editar_pais_api()
                                        else:
                                                editar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 9:
                                        limpiar_consola()
                                        if MODO_API:
                                                
                                                borrar_pais_api()
                                        else:
                                                
                                                if borrar_pais(paises):
                                                        escribir_csv(db_path, paises)
                                case 10:
                                        limpiar_consola()
                                        elegir_modo()
                                case 11:
                                        limpiar_consola()
                                        salida()  
                                        break
                                case _:
                                        limpiar_consola()
                                        error_tipeo_menu(opcion)                                       
                except ValueError:
                        limpiar_consola()
                        except_men_principal()
                        
                
if __name__ == '__main__':
        main()

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

except ImportError:
    print(f"Error: No se pudo importar 'gestionar_db' desde 'function.init'.")
    print(f"Asegúrate que la estructura de carpetas sea correcta.")
    print(f"Raíz del proyecto calculada: {project_root}")
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
                        pass
                case 2:
                        pass
                case 3:
                        pass
                case 4:
                        pass
                case 5:
                        pass
                case 6:
                        pass
                case 7:
                        pass
                case 8:
                        pass
                case 9:
                        print("Saliendo del programa")
                        break  
                case _:
                    print("Opcion incorrecta")
        except ValueError:
                print("Error")
                
if __name__ == '__main__':
    main()
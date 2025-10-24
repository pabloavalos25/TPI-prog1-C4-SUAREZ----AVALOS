
from tools.validaciones import *


def main():
    #Inicializa el csv
    inicializar_archivo()
    
    #Menu de opciones
    while True:
        try:
            print("****Menu Principal****")
            print("1- Mostrar productos")
            print("2- Agregar un producto")
            print("3- Eliminar un producto")
            print("4- Actualizar precios")
            print("5- Salir")
                        
            opcion=int(input("Ingrese una opcion 1-5"))
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
                case _:
                    print("Opcion incorrecta")
        except ValueError:
                print("Error")
                
if __name__ == '__main__':
    main()
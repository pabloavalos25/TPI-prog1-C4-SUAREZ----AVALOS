
def main():
    #Inicializa el csv
    #inicializar_archivo()
    
    #Menu de opciones
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
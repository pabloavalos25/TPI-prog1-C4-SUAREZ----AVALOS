
def main(): #Creación del menú de usuario
    while True:
        print("---MENÚ BUSQUEDA DE PAISES---")
        print("1. Buscar un país")
        print("2. Filtrar país(continente, población, superficie)")
        print("3. Ordenar países (nombre, población, superficie)")
        print("4. Mostrar estadisticas de un país")
        print("5. Agregar/editar país")
        print("6. Salir")

        opcion=int(input("Seleccione la opción que desee consultar: "))

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
                print("Saliendo del sistema, saludos!")
                break
            case _:
                print("ERROR")
                

    
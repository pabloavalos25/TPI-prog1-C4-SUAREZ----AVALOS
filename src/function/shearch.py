import csv


def leer_csv(ruta_csv):
    paises = []
    try:
        with open('src/db/paises.csv',"r", encoding="utf-8")as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pais = {
                    "nombre": fila["nombre"],
                    "poblacion": int(fila["poblacion"]),
                    "superficie": int(fila ["superficie"]),
                    "continente": fila["continente"]
                }
                paises.append(pais)
    except FileNotFoundError:
        print("No se encontró el archivo csv")
    return paises

paises= leer_csv("paises.csv")
for p in paises:
    print(p)


def buscar_pais(paises, nombre): #Funcion de buscar paises por su nombre
    busqueda=input("Ingrese el nombre del pais o parte del nombre del pais: ").lower()
    encontrado=[p for p in paises if busqueda in p["nombre"].lower()]

    continentes= set(p["continente"] for p in paises)  #Se evita errores de escritura de paises/continente
    print("Continendes disponibles:",",".join(continentes))

    if encontrado:
        for p in encontrado:
            print(p)
    else:
        print("No se encontró país con ese nombre.")

def filtrar_continente(paises): #Funcion de filtrado por continente
    continente = input("Ingrese el nombre del continente: ").capitalize()
    continentes = set(p["continente"] for p in paises)
    print("Continentes disponibles:", ", ".join(continentes))

    Resultado = [p for p in paises if p["continente"].lower() ==continente.lower()]

    if Resultado:
        print(f"\nPaises del continente{continente}: ")
        for p in Resultado:
            print(f"-{p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']} Km2)")
    else:
        print("No se encontraron paises en el continente.") 

def filtrar_poblacion(paises):
    try:
        minimo = int(input("Ingrese la población minima: "))
        maximo = int(input("Ingrese la población máxima: "))

    except ValueError:
        print("Ingrese números válidos!")
        return
    
    resultado= [p for p in paises if minimo <= p['poblacion'] <= maximo]

    if resultado:
        print(f"\nPaises con poblacion entre  {minimo} y {maximo}: ")
        for p in resultado:
            print(f"-p{p['nombre']}, {p['poblacion']} habitantes")
    else:
        print("No se encontraron paises en el rango de población")

def filtrar_superficie(paises):
    try:
        min=int(input("Ingrese la superficie mínima en km2: "))
        max=int(input("Ingrese la superficie máxima en Km2: "))
    except ValueError:
        print("Ingrese numeros enteros")
        return
    
    resultado= [p for p in paises if min <=p["superficie"] <= max]

    if resultado:
        print(f"\nPaises con superficie entre {min} y {max} Km2:")
        for p in resultado:
            print(f" {p['nombre']}, {p['superficie']} Km2")
    else:
        print("No se encontro un país en el rango de superficie.")
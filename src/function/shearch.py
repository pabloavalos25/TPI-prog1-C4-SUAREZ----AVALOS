import csv
from function.tools import *
from function.view import *
from function.tools import *

def buscar_pais(paises, nombre): 
    encontrado=[p for p in paises if nombre in p["nombre"].lower()]

    continentes= set(p["continente"] for p in paises)  
    print("Continendes disponibles:",",".join(continentes))

    if encontrado:
        for p in encontrado:
            print(p)
    else:
        print("No se encontró país con ese nombre.")


def filtrar_continente(paises, continente):
    continente_normalizado = normalizar(continente)
    resultados = [p for p in paises if continente_normalizado in normalizar(p["continente"])]
    if resultados:
        print(f"\n Países en el continente '{continente}':")
        mostrar_paises(resultados)
    else:
        print(f"\n No se encontraron países en el continente '{continente}'.")
        
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
            print(f"{p['nombre']}, {p['poblacion']} habitantes")
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
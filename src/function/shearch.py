import csv
from function.tools import *
from function.view import *

def leer_csv(ruta_csv):
    paises = []
    with open(ruta_csv, "r", encoding="UTF-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
                nombre = fila.get("nombre") or fila.get("Nombre")
                poblacion = fila.get("poblacion") or fila.get("Población")
                superficie = fila.get("superficie") or fila.get("Superficie_km2")
                continente = fila.get("continente") or fila.get("Continente")
                if not (nombre and poblacion and superficie and continente):
                        raise ValueError("Faltan datos en la fila")       
                paises.append({
                    "nombre": fila["nombre"],                
                    "poblacion": int(fila["poblacion"]),
                    "superficie": float(fila["superficie"]),
                    "continente": fila["continente"],
            })
    return paises


def buscar_pais(paises, nombre): #Funcion de buscar paises por su nombre
   
    encontrado=[p for p in paises if nombre in p["nombre"].lower()]

    continentes= set(p["continente"] for p in paises)  #Se evita errores de escritura de paises/continente
    print("Continendes disponibles:",",".join(continentes))

    if encontrado:
        for p in encontrado:
            print(p)
    else:
        print("No se encontró país con ese nombre.")

#def filtrar_continente(paises, continente): #Funcion de filtrado por continente
 #   continente=normalizar(continente)

    #continentes = set(p["continente"] for p in paises)
    #print("Continentes disponibles:", ", ".join(continente))

    #Resultado = [p for p in paises if p["continente"].lower() ==continente.lower()]

    #if Resultado:
     #   print(f"\nPaises del continente{continente}: ")
      #  for p in Resultado:
      #      print(f"-{p['nombre']} (Población: {p['poblacion']}, Superficie: {p['superficie']} Km2)")
    #else:
     #   print("No se encontraron paises en el continente.") 

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
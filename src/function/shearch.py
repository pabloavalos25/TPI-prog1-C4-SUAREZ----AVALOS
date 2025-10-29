import csv
from function.tools import *
from function.view import *
from function.tools import *



def _leer_entero_no_negativo(respuesta: str):
    """
    Lee desde input y valida:
    - solo dígitos (isdigit) -> sin letras, sin espacios, sin signos
    - entero no negativo
    Devuelve int o None si es inválido.
    """
    s = input(respuesta).strip()
    if not s.isdigit():
        print("Ingrese solo números enteros no negativos (sin espacios ni letras).")
        return None
    return int(s)



def buscar_pais(paises, nombre): 
    encontrado=[p for p in paises if nombre in p["nombre"].lower()]

    continentes= set(p["continente"] for p in paises)  
    print("Contientes disponibles:",",".join(continentes))

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
    minimo = _leer_entero_no_negativo("Ingrese la población mínima: ")
    if minimo is None:
        return
    maximo = _leer_entero_no_negativo("Ingrese la población máxima: ")
    if maximo is None:
        return

    if minimo > maximo:
        print("El mínimo no puede ser mayor que el máximo.")
        return

    resultado = [p for p in paises if minimo <= p.get('poblacion', -1) <= maximo]

    if resultado:
        print(f"\nPaíses con población entre {minimo} y {maximo}:")
        for p in resultado:
            print(f"{p['nombre']}, {p['poblacion']} habitantes")
    else:
        print("No se encontraron países en ese rango de población.")


def filtrar_superficie(paises):
    
    minimo = _leer_entero_no_negativo("Ingrese la superficie mínima en km²: ")
    if minimo is None:
        return
    maximo = _leer_entero_no_negativo("Ingrese la superficie máxima en km²: ")
    if maximo is None:
        return

    if minimo > maximo:
        print("El mínimo no puede ser mayor que el máximo.")
        return

    resultado = [p for p in paises if minimo <= p.get('superficie', -1) <= maximo]

    if resultado:
        print(f"\nPaíses con superficie entre {minimo} y {maximo} km²:")
        for p in resultado:
            print(f"{p['nombre']}, {p['superficie']} km²")
    else:
        print("No se encontraron países en ese rango de superficie.")
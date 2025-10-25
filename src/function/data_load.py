
from function.tools import *

def agregar_pais(paises):
    
    print("\n--- Agregar nuevo país ---")

    nombre = input("Nombre del país: ").strip()
    while nombre == "":
        nombre = input("El nombre no puede estar vacío. Ingresá nuevamente: ").strip()

    continente = input("Continente: ").strip()
    while continente == "":
        continente = input("El continente no puede estar vacío. Ingresá nuevamente: ").strip()

    try:
        poblacion = int(input("Población: "))
        superficie = float(input("Superficie (km²): "))
    except ValueError:
        print("Error: Población y superficie deben ser numéricos.")
        return


    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }

    paises.append(nuevo_pais)
    print(f"País '{nombre}' agregado correctamente.")
    

def editar_pais(paises):
    print("\n Editar país ")
    nombre = input("Ingresá el nombre del país que querés editar: ")
    nombre_normalizado = normalizar(nombre)

    resultados = [p for p in paises if nombre_normalizado in normalizar(p["nombre"])]

    if not resultados:
        print(f" No se encontró ningún país que contenga '{nombre}'.")
        return

    print(f"\nSe encontraron {len(resultados)} país(es):")
    for i, p in enumerate(resultados):
        print(f"{i + 1}. {p['nombre']} | Población: {p['poblacion']:,} | Superficie: {p['superficie']:,} km²")

    try:
        indice = int(input("Elegí el número del país que querés editar: ")) - 1
        if indice < 0 or indice >= len(resultados):
            print(" Número inválido.")
            return

        pais = resultados[indice]
        nueva_poblacion = int(input(f"Nueva población para {pais['nombre']}: "))
        nueva_superficie = float(input(f"Nueva superficie para {pais['nombre']} (km²): "))

        pais["poblacion"] = nueva_poblacion
        pais["superficie"] = nueva_superficie

        print(f"Datos actualizados para {pais['nombre']}.")

    except ValueError:
        print("Entrada inválida.")
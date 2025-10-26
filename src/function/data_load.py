
from function.tools import *

def agregar_pais(paises):
    
    print("\n--- Agregar nuevo país ---")

    nombre = input("Nombre del país: ").strip().capitalize()
    while nombre == "":
        nombre = input("El nombre no puede estar vacío. Ingresá nuevamente: ").strip().capitalize()

    continente = input("Continente: ").strip().capitalize()
    while continente == "":
        continente = input("El continente no puede estar vacío. Ingresá nuevamente: ").strip().capitalize()

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
        
def borrar_pais(paises) -> bool:
    print("\n--- Borrar país (LOCAL) ---")
    nombre = input("Ingresá el nombre del país (o parte): ").strip().capitalize()
    if not nombre:
        print("Nombre vacío, cancelado.")
        return False

    nombre_norm = normalizar(nombre)
    resultados = [p for p in paises if nombre_norm in normalizar(p["nombre"])]

    if not resultados:
        print(f"No se encontró ningún país que contenga '{nombre}'.")
        return False

    print(f"\nSe encontraron {len(resultados)} país(es):")
    for i, p in enumerate(resultados, 1):
        print(f"{i}. {p['nombre']} | Población: {p['poblacion']:,} | Superficie: {p['superficie']:,} km²")

    try:
        idx = int(input("Elegí el número del país a borrar: ").strip()) - 1
        if idx < 0 or idx >= len(resultados):
            print("Número inválido.")
            return False
    except ValueError:
        print("Entrada inválida.")
        return False

    objetivo = resultados[idx]
    confirma = input(f"Confirmás borrar '{objetivo['nombre']}'? (s/n): ").strip().lower() == "s"
    if not confirma:
        print("Operación cancelada.")
        return False


    pos = next((i for i, p in enumerate(paises) if p["nombre"] == objetivo["nombre"]), None)
    if pos is None:
        print("No se pudo ubicar el registro en la lista original.")
        return False

    paises.pop(pos)
    print(f"'{objetivo['nombre']}' borrado correctamente (LOCAL).")
    return True
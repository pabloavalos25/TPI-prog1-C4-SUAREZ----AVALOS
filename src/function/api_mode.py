# src/function/api_mode.py
from function.tools import normalizar
from function.view import mostrar_paises, ordenar_paises
from function.statistics import mostrar_estadisticas
from function.shearch import buscar_pais, filtrar_continente, filtrar_poblacion, filtrar_superficie
from function import api_client
from function.api_client import (
    list_countries, find_by_name, delete_country
)

def _coerce(items: list[dict]) -> list[dict]:
    for p in items:
        p["poblacion"] = int(p.get("poblacion", 0))
        p["superficie"] = float(p.get("superficie", 0))
        p["continente"] = str(p.get("continente",""))
        p["nombre"] = str(p.get("nombre",""))
    return items

def obtener_paises_api(q=None, continente=None, sort_by=None, desc=False):
    items = api_client.list_countries(q=q, continente=continente, sort_by=sort_by, desc=desc)
    return _coerce(items)


def buscar_pais_api(nombre: str):
    paises = obtener_paises_api(q=nombre)

    buscar_pais(paises, (nombre or "").lower())

def filtrar_continente_api(continente: str):
    paises = obtener_paises_api()
    filtrar_continente(paises, continente) 

def filtrar_poblacion_api():
    paises = obtener_paises_api()
    filtrar_poblacion(paises)               

def filtrar_superficie_api():
    paises = obtener_paises_api()
    filtrar_superficie(paises)              



def ordenar_paises_api(campo: str, descendente: bool = False):
    paises = obtener_paises_api()
    ordenar_paises(paises, campo, descendente)  
    
def estadisticas_api():
    paises = obtener_paises_api()
    mostrar_estadisticas(paises)


def agregar_pais_api():
    print("\n--- Agregar nuevo país (API) ---")
    nombre = input("Nombre del país: ").strip()
    while nombre == "": nombre = input("El nombre no puede estar vacío. Ingresá nuevamente: ").strip().capitalize()

    continente = input("Continente: ").strip()
    while continente == "": continente = input("El continente no puede estar vacío. Ingresá nuevamente: ").strip().capitalize()

    try:
        poblacion = int(input("Población: "))
        superficie = float(input("Superficie (km²): "))
    except ValueError:
        print("Error: Población y superficie deben ser numéricos.")
        return

    creado = api_client.create_from_dict({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    })
    print(f"País '{creado['nombre']}' creado correctamente en el servidor.")

def editar_pais_api():
    print("\n Editar país (API) ")  
    nombre = input("Ingresá el nombre del país que querés editar: ")
    nombre_normalizado = normalizar(nombre)

    paises = obtener_paises_api()
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

        patch = {"poblacion": int(nueva_poblacion), "superficie": int(nueva_superficie)}
    
        if "id" not in pais:
            
            exacto = api_client.find_by_name(pais["nombre"])
            if not exacto or "id" not in exacto:
                print("No se pudo determinar el ID en el servidor.")
                return
            pais["id"] = exacto["id"]

        actualizado = api_client.patch_country(pais["id"], patch)
        print(f"Datos actualizados para {actualizado['nombre']}.")

    except ValueError:
        print("Entrada inválida.")
        
def borrar_pais_api():
    print("\n--- Borrar país (API) ---")
    modo = input("Buscar por (1) nombre o (2) id? [1]: ").strip() or "1"

    if modo == "2":
        
        try:
            cid = int(input("ID: ").strip())
        except ValueError:
            print("ID inválido.")
            return
        confirma = input(f"Confirmás borrar id={cid}? (s/n): ").strip().lower() == "s"
        if not confirma:
            print("Cancelado.")
            return
        delete_country(cid)
        print(f"Borrado id={cid} en el servidor.")
        return

    
    nombre = input("Ingresá el nombre (o parte): ").strip()
    if not nombre:
        print("Nombre vacío, cancelado.")
        return

    cand = list_countries(q=nombre, sort_by="nombre")
    if not cand:
        print(f"No se encontró ningún país que contenga '{nombre}'.")
        return

    mostrar_paises(cand)
    try:
        idx = int(input("Elegí el número del país a borrar (1..n): ").strip()) - 1
        if idx < 0 or idx >= len(cand):
            print("Número inválido.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    elegido = cand[idx]
    
    if "id" not in elegido:
        exacto = find_by_name(elegido.get("nombre",""))
        if not exacto or "id" not in exacto:
            print("No se pudo determinar el ID en el servidor.")
            return
        elegido = exacto

    confirma = input(f"Confirmás borrar '{elegido['nombre']}' (id={elegido['id']})? (s/n): ").strip().lower() == "s"
    if not confirma:
        print("Cancelado.")
        return

    delete_country(elegido["id"])
    print(f"'{elegido['nombre']}' borrado correctamente (API).")

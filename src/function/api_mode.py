# src/function/api_mode.py
from function.tools import normalizar
from function.view import mostrar_paises, ordenar_paises
from function.statistics import mostrar_estadisticas
from function.shearch import buscar_pais, filtrar_continente, filtrar_poblacion, filtrar_superficie
from function import api_client

def _coerce(items: list[dict]) -> list[dict]:
    # Asegura el mismo tipo que usa tu CSV: poblacion=int, superficie=float
    for p in items:
        p["poblacion"] = int(p.get("poblacion", 0))
        p["superficie"] = float(p.get("superficie", 0))
        p["continente"] = str(p.get("continente",""))
        p["nombre"] = str(p.get("nombre",""))
    return items

def obtener_paises_api(q=None, continente=None, sort_by=None, desc=False):
    items = api_client.list_countries(q=q, continente=continente, sort_by=sort_by, desc=desc)
    return _coerce(items)

# ---- Buscar / filtrar: reuso tus funciones tal cual ----

def buscar_pais_api(nombre: str):
    paises = obtener_paises_api(q=nombre)
    # tu buscar_pais espera (paises, nombre_en_minusculas) y printea adentro :contentReference[oaicite:4]{index=4}
    buscar_pais(paises, (nombre or "").lower())

def filtrar_continente_api(continente: str):
    paises = obtener_paises_api()
    filtrar_continente(paises, continente)  # printea adentro :contentReference[oaicite:5]{index=5}

def filtrar_poblacion_api():
    paises = obtener_paises_api()
    filtrar_poblacion(paises)               # pide rangos y printea adentro :contentReference[oaicite:6]{index=6}

def filtrar_superficie_api():
    paises = obtener_paises_api()
    filtrar_superficie(paises)              # pide rangos y printea adentro :contentReference[oaicite:7]{index=7}

# ---- Ordenar / estadísticas: reuso tus funciones ----

def ordenar_paises_api(campo: str, descendente: bool = False):
    paises = obtener_paises_api()
    ordenar_paises(paises, campo, descendente)  # hace print adentro :contentReference[oaicite:8]{index=8}

def estadisticas_api():
    paises = obtener_paises_api()
    mostrar_estadisticas(paises)                 # hace print adentro :contentReference[oaicite:9]{index=9}

# ---- Altas / Ediciones: espejo de data_load, pero contra API ----

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
    print("\n Editar país (API) ")  # espejo de data_load.editar_pais :contentReference[oaicite:10]{index=10}
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
        # la API espera enteros; tu vista los formatea igual :contentReference[oaicite:11]{index=11}
        if "id" not in pais:
            # Si hiciera falta, buscá el id exacto
            exacto = api_client.find_by_name(pais["nombre"])
            if not exacto or "id" not in exacto:
                print("No se pudo determinar el ID en el servidor.")
                return
            pais["id"] = exacto["id"]

        actualizado = api_client.patch_country(pais["id"], patch)
        print(f"Datos actualizados para {actualizado['nombre']}.")

    except ValueError:
        print("Entrada inválida.")

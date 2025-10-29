"""Cálculo e impresión de estadísticas sobre una lista de países.

Este módulo resume información general (máximos, mínimos, promedios y
cantidad por continente) a partir de una lista de diccionarios que
representan países.
"""

from function.tools import normalizar


def mostrar_estadisticas(paises):
    """Imprime estadísticas generales de una lista de países.

    Calcula y muestra:
      - País con mayor población.
      - País con menor población.
      - Promedio de población y de superficie.
      - Cantidad de países por continente (agrupando por nombre normalizado).

    La función imprime por consola y no modifica la lista recibida.

    Args:
        paises (list[dict]): Lista de países. Cada país debe contener las
            claves:
            - 'nombre' (str)
            - 'poblacion' (int)
            - 'superficie' (float | int)
            - 'continente' (str)

    Returns:
        None
    """
    if not paises:
        print(" No hay datos disponibles para mostrar estadísticas.")
        return
    pais_mayor = max(paises, key=lambda x: x["poblacion"])
    pais_menor = min(paises, key=lambda x: x["poblacion"])

    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)
    paises_por_continente = {}
    nombre_muestra_por_normalizado = {}

    for p in paises:
        cont_norm = normalizar(p["continente"])
        paises_por_continente[cont_norm] = paises_por_continente.get(cont_norm, 0) + 1
        if cont_norm not in nombre_muestra_por_normalizado:
            nombre_muestra_por_normalizado[cont_norm] = p["continente"]

    print("*********Estadísticas generales*********")
    print(f"▫ 🏳️  País con mayor población: {pais_mayor['nombre']} ({pais_mayor['poblacion']:,} hab.)")
    print(f"▫ 🏳️  País con menor población: {pais_menor['nombre']} ({pais_menor['poblacion']:,} hab.)")
    print(f"▫ 🌍 Promedio de población: {int(promedio_poblacion):,} hab.")
    print(f"▫ 🌍 Promedio de superficie: {float(promedio_superficie):,} km²")
    print("")
    print("*********Cantidad de países por continente*********")
    for cont_norm, cantidad in paises_por_continente.items():
        cont_muestra = nombre_muestra_por_normalizado.get(cont_norm, cont_norm)
        print(f"      - {cont_muestra}: {cantidad}")
    print("***************************************************")

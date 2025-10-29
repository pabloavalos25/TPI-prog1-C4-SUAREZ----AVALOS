"""Vistas y utilidades de presentación para listas de países.

Incluye funciones para:
- Mostrar países en consola con campos básicos.
- Pedir un rango numérico (mínimo y máximo) por consola.
- Ordenar listas de países por nombre, población o superficie.
"""

import csv  # (opcional: se podría eliminar si no se usa)
from function.tools import normalizar
import unicodedata  # (opcional: no se usa aquí directamente)


def mostrar_paises(lista_paises):
    """Imprime una lista de países con sus datos principales.

    Cada elemento de `lista_paises` debe ser un diccionario con las claves:
    'nombre', 'poblacion', 'superficie', 'continente'.

    Args:
        lista_paises (list[dict]): Lista de países a mostrar.

    Returns:
        None
    """
    for p in lista_paises:
        print(
            f"{p['nombre']} | "
            f"Población: {p['poblacion']:,} | "
            f"Superficie: {p['superficie']:,} km² | "
            f"Continente: {p['continente']}"
        )


def pedir_rango(nombre_campo):
    """Solicita por consola un rango (mínimo y máximo) para un campo numérico.

    Muestra dos `input()`: uno para el mínimo y otro para el máximo. Si el
    usuario ingresa un valor no numérico, informa el error y devuelve
    `(None, None)`.

    Args:
        nombre_campo (str): Nombre del campo a pedir (p. ej., 'población').

    Returns:
        tuple[int | None, int | None]: `(minimo, maximo)` si ambos son válidos;
        en caso de error, `(None, None)`.
    """
    try:
        minimo = int(input(f"Ingresá {nombre_campo} mínimo: "))
        maximo = int(input(f"Ingresá {nombre_campo} máximo: "))
        return minimo, maximo
    except ValueError:
        print("Entrada inválida. Debés ingresar números.")
        # Ajuste menor: devolvemos una tupla de dos elementos para evitar errores
        return None, None


def ordenar_paises(paises, campo, descendente=False):
    """Ordena e imprime países por 'nombre', 'poblacion' o 'superficie'.

    La detección del campo es tolerante:
      - Si `campo` contiene "nom" → ordena por nombre.
      - Si `campo` contiene "pob" → ordena por población.
      - Si `campo` contiene "sup" → ordena por superficie.

    Para `nombre` se usa orden lexicográfico por versión normalizada (sin
    acentos y en minúsculas). Para 'poblacion' y 'superficie' se ordena
    numéricamente.

    Args:
        paises (list[dict]): Lista de países a ordenar y mostrar.
        campo (str): Criterio de orden: nombre/poblacion/superficie (o subcadenas).
        descendente (bool): Si es True, orden descendente.

    Returns:
        None
    """
    try:
        campo_norm = normalizar(campo)

        if "nom" in campo_norm:
            campo = "nombre"
        elif "pob" in campo_norm:
            campo = "poblacion"
        elif "sup" in campo_norm:
            campo = "superficie"

        if campo == "nombre":
            paises_ordenados = sorted(
                paises,
                key=lambda x: normalizar(x["nombre"]),
                reverse=descendente,
            )
        elif campo in ["poblacion", "superficie"]:
            paises_ordenados = sorted(
                paises,
                key=lambda x: x[campo],
                reverse=descendente,
            )
        else:
            print("Campo inválido para ordenar. Usá: nombre / poblacion / superficie.")
            return

        print(
            f"\nPaíses ordenados por {campo} "
            f"({'descendente' if descendente else 'ascendente'}):"
        )
        mostrar_paises(paises_ordenados)

    except Exception as e:
        print(f"Error al ordenar: {e}")

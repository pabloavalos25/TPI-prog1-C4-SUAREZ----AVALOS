import csv
from function.tools import normalizar

def mostrar_paises(lista_paises):
    for p in lista_paises:
        print(f"{p['nombre']} | Población: {p['poblacion']:,} | Superficie: {p['superficie']:,} km² | Continente: {p['continente']}")


def pedir_rango(nombre_campo):
    try:
        minimo = int(input(f"Ingresá {nombre_campo} mínimo: "))
        maximo = int(input(f"Ingresá {nombre_campo} máximo: "))
        return minimo, maximo
    except ValueError:
        print("Entrada inválida. Debés ingresar números.")
        return None, 
import unicodedata


def ordenar_paises(paises, campo, descendente=False):

    try:
        campo_norm = normalizar(campo)

      
        if "nom" in campo_norm:
            campo = "nombre"
        elif "pob" in campo_norm:
            campo = "poblacion"
        elif "sup" in campo_norm:
            campo = "superficie"


        if campo == "nombre":
            paises_ordenados = sorted(paises, key=lambda x: normalizar(x["nombre"]), reverse=descendente)


        elif campo in ["poblacion", "superficie"]:
            paises_ordenados = sorted(paises, key=lambda x: x[campo], reverse=descendente)
        else:
            print("Campo inválido para ordenar. Usá: nombre / poblacion / superficie.")
            return

        print(f"\nPaíses ordenados por {campo} ({'descendente' if descendente else 'ascendente'}):")
        mostrar_paises(paises_ordenados)

    except Exception as e:
        print(f"Error al ordenar: {e}")

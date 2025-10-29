"""Utilidades comunes para el modo local y modo API.

Incluye:
- Normalización de texto (elimina acentos, espacios extremos y pasa a minúsculas).
- Lectura y escritura de países en CSV.
- Ayudas de consola (limpiar pantalla, menús, mensajes y errores).
"""

import unicodedata
import csv
import os


def normalizar(texto):
    """Devuelve el texto en minúsculas, sin espacios extremos ni acentos.

    Usa normalización Unicode (NFD) para remover marcas diacríticas.

    Args:
        texto (str): Cadena de entrada.

    Returns:
        str: Texto normalizado en minúsculas y sin acentos.
    """
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


def leer_csv(ruta_csv: str):
    """Lee un CSV de países y devuelve una lista de dicts.

    La función es tolerante a encabezados alternativos (por ejemplo, admite
    'Nombre' y 'Población', 'Superficie_km2', 'Continente'). Si encuentra
    filas con datos faltantes o no numéricos donde corresponde, las omite y
    muestra un aviso. Si no se obtiene ninguna fila válida, informa que el
    CSV puede estar dañado.

    Campos esperados por fila:
        - nombre (str)
        - poblacion (int)   [se castea desde texto/float]
        - superficie (float)
        - continente (str)
        - flag_emoji (str, opcional)

    Args:
        ruta_csv (str): Ruta al archivo CSV con codificación UTF-8 (BOM ok).

    Returns:
        list[dict]: Lista de países válidos leídos del archivo.
    """
    paises = []
    filas_invalidas = 0

    with open(ruta_csv, "r", encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            nombre = fila.get("nombre") or fila.get("Nombre")
            poblacion = fila.get("poblacion") or fila.get("Población")
            superficie = fila.get("superficie") or fila.get("Superficie_km2")
            continente = fila.get("continente") or fila.get("Continente")

            # Validación básica de presencia
            if not (nombre and poblacion and superficie and continente):
                filas_invalidas += 1
                continue

            # Parseos numéricos tolerantes
            try:
                pob = int(float(poblacion))
                sup = float(superficie)
            except (TypeError, ValueError):
                filas_invalidas += 1
                continue

            paises.append({
                "nombre": nombre.strip(),
                "poblacion": pob,
                "superficie": sup,
                "continente": continente.strip(),
                "flag_emoji": (fila.get("flag_emoji") or "").strip()
            })

    if filas_invalidas:
        print("***************************************************************************************")
        print(f"🛑 Se ignoraron {filas_invalidas} fila(s) inválida(s) en {ruta_csv}. archivo dañado")
    if not paises:
        print("🧐 CSV leído, pero no se obtuvieron filas válidas, csv corrupto o dañado")
        print("No tendra datos iterables, cuando cargue un pais se creara una base datos nueva")
        print("****************************************************************************************")
    return paises


def escribir_csv(ruta_csv: str, paises: list[dict]) -> None:
    """Escribe la lista de países en un CSV con encabezado estándar.

    El archivo se crea/sobrescribe usando UTF-8 con BOM y las columnas:
    'nombre', 'poblacion', 'superficie', 'continente'.

    Args:
        ruta_csv (str): Ruta destino del archivo CSV.
        paises (list[dict]): Lista de países a persistir.

    Returns:
        None
    """
    fieldnames = ["nombre", "poblacion", "superficie", "continente"]
    with open(ruta_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in paises:
            writer.writerow({
                "nombre": str(p["nombre"]),
                "poblacion": int(p["poblacion"]),
                "superficie": float(p["superficie"]),
                "continente": str(p["continente"]),
            })


def limpiar_consola():
    """Limpia la consola según el sistema operativo (cls/clear)."""
    os.system("cls" if os.name == "nt" else "clear")


def salida():
    """Muestra un mensaje de despedida del programa."""
    print("*******************👍************************")
    print("*     Gracias por usar el programa.         *")
    print("*********************************************")


def error_tipeo(op):
    """Informa un error de opción inválida en la selección de modo.

    Args:
        op (Any): Valor ingresado por el usuario.
    """
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {op}")
    print("*😁 Recuerda ingresar un numero del 1 al 2")
    print("*******************🛑*************************")


def nube():
    """Imprime información del modo API (servidor nube)."""
    print("**********************************")
    print("🟢  Ingreso por API ")
    print("☁️   Servidor nube ")
    print("🌍  Url: http://149.50.150.15:8000")
    print("***********************************")


def local():
    """Imprime información del modo local (archivos CSV)."""
    print("**********************************")
    print("🟢  Ingreso Modo Local ")
    print("💻  Servidor Fisico ")
    print("***********************************")


def seleccion():
    """Muestra el menú de selección de servidor y devuelve la opción elegida.

    Returns:
        int: 1 para CSV local, 2 para API, 3 para salir.

    Nota:
        Esta función no maneja ValueError de `int(input(...))`. Se espera que
        el llamador capture la excepción si el usuario ingresa texto inválido.
    """
    print("****Seleccione el servidor****")
    print("1. CSV local 💻")
    print("2. CSV  API  ☁️")
    print("3. Salir 🛑")
    op = int(input("Elegí 1 o 2 : "))
    return op


def menu_principal():
    """Muestra el menú principal de operaciones y devuelve la opción elegida.

    Returns:
        int: Número de opción (1 a 11).

    Nota:
        Esta función no maneja ValueError de `int(input(...))`. Se espera que
        el llamador capture la excepción si el usuario ingresa texto inválido.
    """
    print("")
    print("**********INFO GEOGRAFICO**********")
    print("1.  Buscar pais por nombre")
    print("2.  Filtrar por continente")
    print("3.  Filtrar por rango de poblacion")
    print("4.  Filtrar por rango de superficie")
    print("5.  Ordenar paises")
    print("6.  Mostrar estadisticas")
    print("7.  Agregar un pais")
    print("8.  Editar poblacion y superficie de un pais")
    print("9.  Borrar país")
    print("10. Cambiar modo de servidor")
    print("11. Salir")

    opcion = int(input("Ingrese una opcion 1-11: "))
    print("***********************************")
    return opcion


def error_tipeo_menu(opcion):
    """Informa un error de opción inválida en el menú principal.

    Args:
        opcion (Any): Valor ingresado por el usuario.
    """
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {opcion}  ")
    print("*😁 Recuerda ingresar un numero del 1 al 11   ")
    print("*******************🛑*************************")


def except_men_server():
    """Mensaje de error cuando la opción del selector de servidor no es numérica."""
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 2       *")
    print("***********************🛑*******************************")


def except_men_principal():
    """Mensaje de error cuando la opción del menú principal no es numérica."""
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 11       *")
    print("***********************🛑*******************************")


def except_local(e):
    """Mensaje estándar para errores en modo local.

    Args:
        e (Exception): Excepción capturada por el llamador.
    """
    print("*****************************************")
    print("😡 Advertencia: error local:", e)
    print("Intente más tarde o seleccione modo nube")
    print("Disculpe las molestias                   ")
    print("*****************************************")


def error_server():
    """Mensaje estándar para errores al contactar el servidor API."""
    print("*****************************************")
    print("😡 Advertencia: api-server no respondió ")
    print("Intente más tarde o seleccione modo local")
    print("Disculpe las molestias                   ")
    print("*****************************************")

"""Punto de entrada de la aplicación de gestión de países.

Este módulo:
- Ajusta `sys.path` para permitir importaciones relativas desde `src/` y la raíz.
- Inicializa la base de datos y carga el CSV de países.
- Permite elegir entre modo local (archivos) y modo API (servidor).
- Ejecuta el bucle del menú principal para consultar y gestionar datos.

Dependencias clave (paquete `function.*`):
- init.init_db: Inicialización de la base de datos/archivos.
- data_load.leer_csv / escribir_csv: Carga y persistencia de países.
- view, statistics, tools, shearch, api_client, api_mode: Menús, filtros, vistas,
  utilidades y llamadas a API.

Nota:
    Este módulo realiza I/O por consola y puede terminar el proceso con `sys.exit`.
"""

import sys
import os

script_path = os.path.abspath(__file__)
app_dir = os.path.dirname(script_path)
project_root = os.path.dirname(app_dir)
src_dir = os.path.join(project_root, 'src')

if project_root not in sys.path:
        sys.path.append(project_root)
if src_dir not in sys.path:
        sys.path.append(src_dir)

try:
        from function.init import init_db
        from function.view import *
        from function.statistics import *
        from function.tools import *
        from function.data_load import *
        from function.shearch import *
        from function.view import *
        from function import api_client
        from function.api_mode import *

except ImportError:
        print(f"Error: No se pudo importar 'gestionar_db' desde 'function.init'.")
        print(f"Raíz del proyecto calculada: {project_root}")
        sys.exit(1)

db_path = init_db(project_root)
if db_path is None:
        sys.exit(1)

paises = leer_csv(db_path)

# Indicador global de modo de operación. False = local, True = API.
MODO_API = False


def elegir_modo():
        """Permite seleccionar el modo de ejecución (Local, API o Salir).

        El flujo de trabajo es:
        1) Mostrar un selector (ver `seleccion()`).
        2) Cuando la opción es válida:
           - Opción 1: modo local (MODO_API=False), se limpia consola y ejecuta
             `local()`; luego continúa al menú principal.
           - Opción 2: modo API (MODO_API=True), se limpia consola, verifica
             `api_client.estado_servidor()`, ejecuta `nube()` y continúa al menú principal.
           - Opción 3: salir del programa (`salida()` y `sys.exit(0)`).
        3) En caso de error de tipeo o excepción controlada se limpia la consola y
           se informa el problema, repitiendo el bucle hasta una selección válida.

        Side effects:
            - Cambia el estado global `MODO_API`.
            - Imprime y limpia la consola.
            - Puede finalizar el proceso con `sys.exit(0)` si se elige salir.

        Returns:
            None
        """
        while True:
                global MODO_API
                try:
                        op = seleccion()
                        match op:
                                case 1:
                                        MODO_API = False
                                        try:
                                                limpiar_consola()
                                                local()
                                                break
                                        except Exception as c:
                                                limpiar_consola()
                                                except_local(c)
                                case 2:
                                        MODO_API = True
                                        try:
                                                limpiar_consola()
                                                # Antes: api_client.health()
                                                api_client.estado_servidor()
                                                nube()
                                                break
                                        except Exception as b:
                                                limpiar_consola()
                                                error_server()
                                case 3:
                                        limpiar_consola()
                                        salida()
                                        sys.exit(0)
                                case _:
                                        limpiar_consola()
                                        error_tipeo(op)
                except ValueError as a:
                        limpiar_consola()
                        except_men_server()


elegir_modo()


def main():
        """Bucle principal del programa que despacha el menú de opciones.

        Según el modo actual (`MODO_API`), las operaciones se ejecutan contra el
        backend local (listas/CSV) o invocan endpoints del servidor (API).

        Opciones principales:
            1. Buscar país por nombre o subcadena.
            2. Filtrar por continente.
            3. Filtrar por población (rango).
            4. Filtrar por superficie (rango).
            5. Ordenar países por campo y sentido.
            6. Mostrar estadísticas.
            7. Agregar país (persiste en CSV en modo local).
            8. Editar país (persiste en CSV en modo local).
            9. Borrar país (persiste en CSV en modo local si procede).
            10. Cambiar modo (Local/API).
            11. Salir.

        Side effects:
            - Lectura/escritura por consola.
            - Modificación de la lista `paises` en memoria (modo local).
            - Persistencia a disco vía `escribir_csv` (altas/bajas/modificaciones).
            - Impresiones/limpieza de pantalla con utilidades de `view/tools`.

        Returns:
            None
        """
        while True:
                try:
                        opcion = menu_principal()
                        match opcion:
                                case 1:
                                        limpiar_consola()
                                        while True:
                                                try:
                                                        nombre = input(
                                                                "Ingrese el nombre del pais o "
                                                                "parte del nombre del pais: "
                                                        ).strip().lower()
                                                        if (not nombre) or (not nombre.isalpha()):
                                                                print("Entrada inválida: use solo letras, sin espacios ni números.")
                                                                continue
                                                        break
                                                except Exception:
                                                        print("Entrada inválida. Intente nuevamente.")
                                                        continue

                                        if MODO_API:
                                                buscar_pais_api(nombre)
                                        else:
                                                buscar_pais(paises, nombre)
                                case 2:
                                        limpiar_consola()
                                        while True:
                                                try:
                                                        continente = input(
                                                                "Ingrese el nombre del continente: "
                                                        ).strip()
                                                        if (not continente) or (not continente.isalpha()):
                                                                print("Entrada inválida: use solo letras, sin espacios ni números.")
                                                                continue
                                                        continente = continente.capitalize()
                                                        break
                                                except Exception:
                                                        print("Entrada inválida. Intente nuevamente.")
                                                        continue
                                        if MODO_API:
                                                filtrar_continente_api(continente)
                                        else:
                                                filtrar_continente(paises, continente)
                                case 3:
                                        limpiar_consola()
                                        if MODO_API:
                                                filtrar_poblacion_api()
                                        else:
                                                filtrar_poblacion(paises)
                                case 4:
                                        limpiar_consola()
                                        if MODO_API:
                                                filtrar_superficie_api()
                                        else:
                                                filtrar_superficie(paises)
                                case 5:
                                        limpiar_consola()
                                        campo = input(
                                                "Campo para ordenar (nombre/poblacion/"
                                                "superficie): "
                                        ).lower()
                                        desc_input = input(
                                                "¿Querés orden descendente? (s/n): "
                                        ).strip().lower()
                                        descendente = (desc_input == 's')
                                        if MODO_API:
                                                ordenar_paises_api(campo, descendente)
                                        else:
                                                ordenar_paises(paises, campo, descendente)
                                case 6:
                                        limpiar_consola()
                                        if MODO_API:
                                                estadisticas_api()
                                        else:
                                                mostrar_estadisticas(paises)
                                case 7:
                                        limpiar_consola()
                                        if MODO_API:
                                                agregar_pais_api()
                                        else:
                                                agregar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 8:
                                        limpiar_consola()
                                        if MODO_API:
                                                editar_pais_api()
                                        else:
                                                editar_pais(paises)
                                                escribir_csv(db_path, paises)
                                case 9:
                                        limpiar_consola()
                                        if MODO_API:

                                                borrar_pais_api()
                                        else:

                                                if borrar_pais(paises):
                                                        escribir_csv(db_path, paises)
                                case 10:
                                        limpiar_consola()
                                        elegir_modo()
                                case 11:
                                        limpiar_consola()
                                        salida()
                                        break
                                case _:
                                        limpiar_consola()
                                        error_tipeo_menu(opcion)
                except ValueError:
                        limpiar_consola()
                        except_men_principal()


if __name__ == '__main__':
        main()

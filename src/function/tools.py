import unicodedata 
import csv
import os


def normalizar(texto):
    """Convierte texto a minúsculas, elimina espacios y acentos."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

def leer_csv(ruta_csv: str):
    paises = []
    filas_invalidas = 0

    with open(ruta_csv, "r", encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            
            nombre     = fila.get("nombre")     or fila.get("Nombre")
            poblacion  = fila.get("poblacion")  or fila.get("Población")
            superficie = fila.get("superficie") or fila.get("Superficie_km2")
            continente = fila.get("continente") or fila.get("Continente")

            
            if not (nombre and poblacion and superficie and continente):
                filas_invalidas += 1
                continue

            
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
    os.system("cls" if os.name == "nt" else "clear")
    
def salida():
    print("*******************👍************************")                                        
    print("*     Gracias por usar el programa.         *")
    print("*********************************************")
    
def error_tipeo(op):
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {op}")
    print("*😁 Recuerda ingresar un numero del 1 al 2")
    print("*******************🛑*************************")
    
def nube():
    print("**********************************")
    print("🟢  Ingreso por API ")
    print("☁️   Servidor nube ")
    print("🌍  Url: http://149.50.150.15:8000")
    print("***********************************")
    
def local():
    print("**********************************")
    print("🟢  Ingreso Modo Local ")
    print("💻  Servidor Fisico ")
    print("***********************************")

def seleccion():
    print("****Seleccione el servidor****")                        
    print("1. CSV local 💻")
    print("2. CSV  API  ☁️")
    print("3. Salir 🛑")
    op = int(input("Elegí 1 o 2 : "))
    return op

def menu_principal():
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
                        
    opcion=int(input("Ingrese una opcion 1-11: "))
    print("***********************************")
    return opcion

def error_tipeo_menu(opcion):
    print("*******************🛑*************************")
    print(f"*🫣  Opcion incorrecta: ingresaste {opcion}  ")
    print("*😁 Recuerda ingresar un numero del 1 al 11   ")
    print("*******************🛑*************************")
    
def except_men_server():
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 2       *")
    print("***********************🛑*******************************")

def except_men_principal():
    print("***********************🛑*******************************")
    print("*🤔 Opcion incorrecta: No ingresaste un numero valido  *")
    print("*😁      Recuerda ingresar un numero del 1 al 11       *")
    print("***********************🛑*******************************")
    
def except_local(e):
    print("*****************************************")
    print("😡 Advertencia: error local:", e)
    print("Intente más tarde o seleccione modo nube")
    print("Disculpe las molestias                   ")
    print("*****************************************")

def error_server():
    print("*****************************************")
    print("😡 Advertencia: api-server no respondió ")
    print("Intente más tarde o seleccione modo local")
    print("Disculpe las molestias                   ")
    print("*****************************************")
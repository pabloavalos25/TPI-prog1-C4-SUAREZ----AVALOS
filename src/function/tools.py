import unicodedata 
import csv
import os


def normalizar(texto):
    """Convierte texto a minúsculas, elimina espacios y acentos."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

def leer_csv(ruta_csv):
    paises = []
    with open(ruta_csv, "r", encoding="UTF-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for fila in lector:
                nombre = fila.get("nombre") or fila.get("Nombre")
                poblacion = fila.get("poblacion") or fila.get("Población")
                superficie = fila.get("superficie") or fila.get("Superficie_km2")
                continente = fila.get("continente") or fila.get("Continente")
                if not (nombre and poblacion and superficie and continente):
                        raise ValueError("Faltan datos en la fila")       
                paises.append({
                    "nombre": fila["nombre"],                
                    "poblacion": int(fila["poblacion"]),
                    "superficie": float(fila["superficie"]),
                    "continente": fila["continente"],
            })
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
            
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
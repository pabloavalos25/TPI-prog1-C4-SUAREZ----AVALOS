import unicodedata 
from function.view import *

def normalizar(texto):
    """Convierte texto a minúsculas, elimina espacios y acentos."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto


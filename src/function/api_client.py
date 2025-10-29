"""Cliente HTTP sencillo para hablar con el servidor de la API de países.

Este módulo ofrece funciones básicas para:
- Verificar si el servidor está en línea.
- Listar, buscar, crear, actualizar y eliminar países.

Las funciones usan solicitudes HTTP (GET/POST/PATCH/DELETE) con `requests`.
Se busca un código claro y simple, ideal para primer año.
"""

from typing import Optional, List, Dict

try:
    import requests
except ImportError:
    raise SystemExit(
        "*********************😎****************************\n"
        "*          Falta el paquete 'requests'.           *\n"
        "* Tener presente la version de python que tienes  *\n"
        "* Por ejemplo tengo pythob 3.13:                  *\n"
        "*   Windows: py -3.13 -m pip install requests     *\n"
        "*   Linux/Mac: python3 -m pip install requests    *\n"
        "* Es fundamental para que el proyecto funcione    *\n"
        "* Se utiliza para comunicarse con el servidor API *\n"
        "*********************👌***************************"
    )

# URL base del servidor de la API (sin barra final).
BASE_URL = "http://149.50.150.15:8000".rstrip("/")


def _url(ruta: str) -> str:
    """Arma una URL completa a partir de la ruta.

    Args:
        ruta (str): Ruta que comienza con '/' (por ejemplo, '/countries').

    Returns:
        str: URL lista para usar en la petición HTTP.
    """
    return f"{BASE_URL}{ruta}"


def establecer_base_url(url: str) -> None:
    """Cambia la URL base del servidor API.

    Args:
        url (str): Nueva URL base. Se ignora la barra final si existe.
    """
    global BASE_URL
    BASE_URL = (url or "").rstrip("/")


def estado_servidor() -> Dict:
    """Consulta el estado del servidor (endpoint de salud).

    Returns:
        dict: Respuesta JSON con información de estado.

    Raises:
        requests.HTTPError: Si la respuesta no es correcta (4xx/5xx).
    """
    resp = requests.get(_url("/health"), timeout=5)
    resp.raise_for_status()
    return resp.json()


def listar_paises(
    q: Optional[str] = None,
    continente: Optional[str] = None,
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Lista países con filtros y orden opcional.

    Args:
        q (str | None): Texto para buscar por nombre.
        continente (str | None): Filtro por continente.
        ordenar_por (str | None): Campo de orden (ej.: 'nombre').
        descendente (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista de países (cada país es un dict).

    Raises:
        requests.HTTPError: Si la respuesta no es correcta.
    """
    params: Dict[str, str] = {}
    if q:
        params["q"] = q
    if continente:
        params["continente"] = continente
    if ordenar_por:
        params["sort_by"] = ordenar_por
    if descendente:
        params["desc"] = "true"

    resp = requests.get(_url("/countries"), params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def obtener_pais(id_pais: int) -> Dict:
    """Obtiene un país por su identificador numérico.

    Args:
        id_pais (int): Identificador del país.

    Returns:
        dict: Datos del país.

    Raises:
        requests.HTTPError: Si no existe o hay error del servidor.
    """
    resp = requests.get(_url(f"/countries/{id_pais}"), timeout=10)
    resp.raise_for_status()
    return resp.json()


def crear_pais(
    nombre: str,
    poblacion: int,
    superficie: int,
    continente: str,
) -> Dict:
    """Crea un país nuevo en el servidor.

    Args:
        nombre (str): Nombre del país.
        poblacion (int): Población (entero no negativo).
        superficie (int): Superficie en km² (entero no negativo).
        continente (str): Continente del país.

    Returns:
        dict: País creado (respuesta del servidor).

    Raises:
        requests.HTTPError: Si la creación falla.
    """
    payload = {
        "nombre": nombre,
        "poblacion": int(poblacion),
        "superficie": int(superficie),
        "continente": continente,
    }
    resp = requests.post(_url("/countries"), json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def actualizar_pais_parcial(id_pais: int, cambios: Dict) -> Dict:
    """Actualiza parcialmente un país (solo los campos enviados).

    Args:
        id_pais (int): Identificador del país a modificar.
        cambios (dict): Campos a actualizar (por ejemplo, {'poblacion': 1000}).

    Returns:
        dict: País actualizado.

    Raises:
        requests.HTTPError: Si la actualización falla.
    """
    resp = requests.patch(_url(f"/countries/{id_pais}"), json=cambios, timeout=10)
    resp.raise_for_status()
    return resp.json()


def eliminar_pais(id_pais: int) -> bool:
    """Elimina un país por su identificador.

    Args:
        id_pais (int): Identificador del país.

    Returns:
        bool: True si el servidor aceptó la eliminación.

    Raises:
        requests.HTTPError: Si el servidor devuelve un error.
    """
    resp = requests.delete(_url(f"/countries/{id_pais}"), timeout=10)
    if resp.status_code not in (200, 204):
        resp.raise_for_status()
    return True


def listar_todos(
    ordenar_por: Optional[str] = None,
    descendente: bool = False,
) -> List[Dict]:
    """Devuelve todos los países con orden opcional.

    Args:
        ordenar_por (str | None): Campo de orden.
        descendente (bool): Si True, orden descendente.

    Returns:
        list[dict]: Lista completa de países.
    """
    return listar_paises(ordenar_por=ordenar_por, descendente=descendente)


def buscar_por_nombre(nombre: str) -> Optional[Dict]:
    """Busca un país por nombre (intenta coincidencia exacta primero).

    Si no encuentra coincidencia exacta, devuelve el primer resultado de la lista.

    Args:
        nombre (str): Nombre a buscar.

    Returns:
        dict | None: País encontrado o None si no hay resultados.
    """
    if not nombre:
        return None

    candidatos = listar_paises(q=nombre, ordenar_por="nombre")
    n = (nombre or "").strip().lower()
    for c in candidatos:
        if c.get("nombre", "").strip().lower() == n:
            return c
    return candidatos[0] if candidatos else None


def crear_desde_dict(item: Dict) -> Dict:
    """Crea un país a partir de un diccionario con las claves conocidas.

    Args:
        item (dict): Debe incluir 'nombre', 'poblacion', 'superficie', 'continente'.

    Returns:
        dict: País creado (respuesta del servidor).

    Raises:
        KeyError: Si faltan claves en el diccionario.
        requests.HTTPError: Si la creación falla.
    """
    return crear_pais(
        nombre=item["nombre"],
        poblacion=int(item["poblacion"]),
        superficie=int(item["superficie"]),
        continente=item["continente"],
    )

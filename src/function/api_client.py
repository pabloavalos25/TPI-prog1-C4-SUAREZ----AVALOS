try:
    import requests
except ImportError:
    raise SystemExit(
        "*********************😎***************************\n"
        "* Falta el paquete 'requests'. Instalalo con:     *\n"
        "* Tener presente la version de python que tienes  *\n"
        "* instaldo por ejemplo tengo pythob 3.13:         *\n"
        "*   Windows: py -3.13 -m pip install requests     *\n"
        "*   Linux/Mac: python3 -m pip install requests    *\n"
        "* Es fundamental para que el proyecto funcione    *\n"
        "* Se utiliza para comunicarse con el servidor API *\n"
        "*********************👌***************************"
    )

BASE_URL = "http://149.50.150.15:8000".rstrip("/")

def _url(path: str) -> str:
    return f"{BASE_URL}{path}"

def set_base_url(url: str):
    global BASE_URL
    BASE_URL = (url or "").rstrip("/")

def health():
    r = requests.get(_url("/health"), timeout=5)
    r.raise_for_status()
    return r.json()

def list_countries(q=None, continente=None, sort_by=None, desc=False):
    params = {}
    if q: params["q"] = q
    if continente: params["continente"] = continente
    if sort_by: params["sort_by"] = sort_by
    if desc: params["desc"] = "true"
    r = requests.get(_url("/countries"), params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def get_country(cid: int):
    r = requests.get(_url(f"/countries/{cid}"), timeout=10)
    r.raise_for_status()
    return r.json()

def create_country(nombre: str, poblacion: int, superficie: int, continente: str):
    payload = {
        "nombre": nombre,
        "poblacion": int(poblacion),
        "superficie": int(superficie),
        "continente": continente,
    }
    r = requests.post(_url("/countries"), json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def patch_country(cid: int, patch: dict):
    r = requests.patch(_url(f"/countries/{cid}"), json=patch, timeout=10)
    r.raise_for_status()
    return r.json()

def delete_country(cid: int):
    r = requests.delete(_url(f"/countries/{cid}"), timeout=10)
    if r.status_code not in (200, 204):
        r.raise_for_status()
    return True


def list_all(sort_by=None, desc=False):
    return list_countries(sort_by=sort_by, desc=desc)

def find_by_name(nombre: str):
    if not nombre:
        return None
    cand = list_countries(q=nombre, sort_by="nombre")
    n = (nombre or "").strip().lower()
    for c in cand:
        if c.get("nombre","").strip().lower() == n:
            return c
    return cand[0] if cand else None

def create_from_dict(item: dict):
    return create_country(
        nombre=item["nombre"],
        poblacion=int(item["poblacion"]),
        superficie=int(item["superficie"]),
        continente=item["continente"],
    )

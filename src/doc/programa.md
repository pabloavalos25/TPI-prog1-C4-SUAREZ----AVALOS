## Informe del programa (auditoría técnica y guía de integración)

### Propósito
Aplicación de consola para gestionar información de países a partir de un archivo CSV y, opcionalmente, una API remota. Permite búsquedas, filtros, ordenamientos, estadísticas y edición básica.

### Alcance del informe
- Flujo completo desde `app/main.py` hasta cada módulo involucrado.
- Dónde están las funciones y cómo se acceden.
- Requisitos de `app/main.py` para funcionar.
- Persistencia actual en CSV y propuesta de “Modo API”.
- Opciones de diseño para integrar la API remota y pasos detallados de implementación.

---

### Estructura del proyecto relevante
```text
app/
  └─ main.py                  # Punto de entrada y menú
src/
  ├─ db/
  │   └─ paises.csv           # Datos locales (CSV)
  └─ function/
      ├─ init.py              # Gestión de existencia/ubicación de CSV
      ├─ tools.py             # Utilidades: normalizar, leer_csv, escribir_csv
      ├─ shearch.py           # Búsquedas y filtros (nombre, continente, rangos)
      ├─ data_load.py         # Alta/edición en memoria
      ├─ statistics.py        # Estadísticas descriptivas
      ├─ view.py              # Presentación (listar, ordenar)
      └─ validations.py       # (vacío; oportunidad para centralizar validaciones)
```

---

### Flujo de ejecución (de punta a punta)
1. Inicio en `app/main.py`.
   - Calcula rutas (`project_root`, `src_dir`) y las agrega a `sys.path`.
   - Importa módulos desde `src/function/`.
2. Inicialización del CSV.
   - Llama a `init_db(project_root)` que asegura la existencia y ubicación correcta de `src/db/paises.csv`:
     - Si está en otro lado del proyecto, lo mueve a `src/db/`.
     - Si no existe, lo crea con encabezados.
   - Devuelve `db_path` (ruta del CSV).
3. Carga de datos.
   - `paises = leer_csv(db_path)` lee el CSV como una lista de diccionarios:
     `{"nombre": str, "poblacion": int, "superficie": float, "continente": str}`.
4. Interfaz de usuario (loop por consola).
   - Muestra menú con opciones 1–9.
   - Según la opción, delega en funciones de `shearch.py`, `view.py`, `statistics.py`, `data_load.py`.
   - En altas y ediciones (7 y 8), persiste los cambios en CSV con `escribir_csv(db_path, paises)`.
5. Salida.
   - Opción 9 cierra el programa.

---

### Módulos y funciones (qué hacen y cómo se acceden)

- `app/main.py` (punto de entrada)
  - Orquesta todo el flujo. Importa símbolos con `from function.<modulo> import *` y llama a las funciones directamente dentro del `match` del menú.
  - Casos principales:
    - 1: `buscar_pais(paises, nombre)`
    - 2: `filtrar_continente(paises, continente)`
    - 3: `filtrar_poblacion(paises)`
    - 4: `filtrar_superficie(paises)`
    - 5: `ordenar_paises(paises, campo, descendente)`
    - 6: `mostrar_estadisticas(paises)`
    - 7: `agregar_pais(paises)` y `escribir_csv(db_path, paises)`
    - 8: `editar_pais(paises)` y `escribir_csv(db_path, paises)`

- `src/function/init.py`
  - `gestionar_db(directorio_base, ruta_objetivo)`: busca `paises.csv` en todo el proyecto; si está mal ubicado, lo mueve; si no existe, lo crea.
  - `init_db(project_root)`: helper que fija `RUTA_CORRECTA_DB` y llama a `gestionar_db`.

- `src/function/tools.py`
  - `normalizar(texto)`: minúsculas + trim + remoción de acentos (NFD) para comparaciones robustas.
  - `leer_csv(ruta_csv)`: parsea el CSV a lista de dicts (conversión de tipos a int/float). Se recomienda versión robusta con fallbacks de encabezados.
  - `escribir_csv(ruta_csv, paises)`: sobrescribe el CSV con el contenido actual de `paises`.

- `src/function/view.py`
  - `mostrar_paises(lista_paises)`: imprime en consola cada país (formateo de miles/km²).
  - `ordenar_paises(paises, campo, descendente=False)`: normaliza el campo y ordena por `nombre`, `poblacion` o `superficie`.
  - `pedir_rango(nombre_campo)`: helper para leer rangos desde input.

- `src/function/shearch.py` (typo en nombre; hace “search”)
  - `buscar_pais(paises, nombre)`: coincidencias parciales por nombre; lista continentes disponibles.
  - `filtrar_continente(paises, continente)`: usa `normalizar` y muestra con `mostrar_paises`.
  - `filtrar_poblacion(paises)`: por rango `min..max` (input por consola).
  - `filtrar_superficie(paises)`: por rango `min..max` (input por consola).

- `src/function/data_load.py`
  - `agregar_pais(paises)`: pide datos, valida tipos simples y `append` in-memory (la persistencia efectiva se hace desde `main.py` con `escribir_csv`).
  - `editar_pais(paises)`: búsqueda por nombre, selección y actualización de `poblacion`/`superficie` (persistencia desde `main.py`).

- `src/function/statistics.py`
  - `mostrar_estadisticas(paises)`: máximo/mínimo por población, promedios y conteo por continente.

- `src/db/paises.csv`
  - Encabezados: `nombre,poblacion,superficie,continente`.

---

### Persistencia actual (CSV)
- Los cambios se guardan automáticamente tras las opciones 7 (agregar) y 8 (editar), llamando a `escribir_csv(db_path, paises)`.
- Formato y encoding: `utf-8-sig` y `newline=""` para compatibilidad Windows/Excel.
- Recomendación: usar la versión robusta de `leer_csv` (con fallbacks de encabezado y parseo tolerante a comas de miles).

---

### Modo API (propuesto)
Objetivo: agregar una opción de menú “Usar API” para alternar entre datos locales (CSV) y datos remotos (persistencia en nube) consumiendo una API ya disponible.

- API actual (lectura): [API de países](http://149.50.150.15:8000/countries)
  - Respuesta JSON de ejemplo: lista de objetos con campos como `nombre`, `poblacion`, `superficie`, `continente`, `flag_emoji`, `id`.
  - Nota: El modelo local no usa `id` ni `flag_emoji`; pueden almacenarse opcionalmente o ignorarse.

#### Diseño general
- Introducir un “proveedor de datos” con dos implementaciones:
  1) `CSVProvider` (actual): leer y escribir CSV.
  2) `ApiProvider`: leer desde la API y guardar cambios mediante endpoints REST.
- Selección de modo por menú (alternable en runtime) o por parámetro/env al inicio (modo fijo).

#### Opción A — Alternar por menú (recomendada para pruebas)
- Agregar opción “10. Alternar modo API (Local/Remoto)” en `main.py`.
- Variable global `MODO_API = False` al iniciar (local por defecto).
- Comportamiento por caso del menú:
  - Lecturas (1–6): si `MODO_API` es `True`, obtener lista con `api_client.get_countries()`; si es `False`, usar `paises` de memoria.
  - Altas/ediciones (7–8): si `MODO_API` es `True`, llamar a `api_client.create_country(...)` o `api_client.update_country(id, ...)`; si es `False`, operar en lista y `escribir_csv(...)`.

Snippets de referencia (nuevos archivos y uso):

- Crear `src/function/api_client.py` (usar `requests`):
```python
import requests
BASE_URL = "http://149.50.150.15:8000"
TIMEOUT = 10

def get_countries():
    r = requests.get(f"{BASE_URL}/countries", timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    # mapear a la estructura local si se desea ignorar campos extra
    return [
        {
            "id": c.get("id"),
            "nombre": c.get("nombre"),
            "poblacion": int(c.get("poblacion", 0)),
            "superficie": float(c.get("superficie", 0)),
            "continente": c.get("continente"),
        }
        for c in data
    ]

# Ejemplo de creación (requiere que la API exponga POST /countries)
# Ajustar payload/endpoint según contrato real del servidor

def create_country(pais: dict):
    payload = {
        "nombre": pais["nombre"],
        "poblacion": pais["poblacion"],
        "superficie": pais["superficie"],
        "continente": pais["continente"],
    }
    r = requests.post(f"{BASE_URL}/countries", json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

# Ejemplo de actualización (PUT/PATCH): requiere id

def update_country(pais_id: int, cambios: dict):
    r = requests.put(f"{BASE_URL}/countries/{pais_id}", json=cambios, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()
```

- Cambios mínimos en `app/main.py` (idea):
  - `from function import api_client`
  - `MODO_API = False`
  - Nueva opción 10 que hace `MODO_API = not MODO_API` e imprime estado.
  - En 1–6: si `MODO_API`, `lista = api_client.get_countries()` y operar sobre `lista` (ordenar, filtrar, mostrar). En local, usar `paises`.
  - En 7: armar `nuevo_pais` (reutilizar `agregar_pais` para pedir datos) y si `MODO_API` llamar `api_client.create_country(nuevo_pais)`; si no, `paises.append(...)` y `escribir_csv(...)`.
  - En 8: con `MODO_API`, obtener lista de la API, seleccionar registro y pasar `id` a `update_country(id, cambios)`; en local, editar `paises` y persistir CSV.

Pros:
- Muy visible para el usuario; ideal para demo y auditoría.
Contras:
- Requiere mantener ramas de lógica en `main.py` para ambos modos.

#### Opción B — Modo fijo por arranque (CLI/env)
- Variable de entorno `MODO_API=true` o argumento `--api` al ejecutar.
- Se fija el proveedor al inicio y todo el flujo usa ese proveedor (no alternable durante la ejecución).

Pros:
- Código de `main.py` más simple.
Contras:
- Menos flexible para comparar modos en vivo.

#### Opción C — Abstracción “Provider/Repository”
- Crear `src/function/repository.py` con una clase base y dos implementaciones (CSV y API). `main.py` solo llama a un `repository` inyectado.
- Facilita testeo y escalabilidad; mayor refactor inicial.

---

### Requisitos para “Modo API”
- Dependencia: `requests` (agregar a `requirements.txt` o al README como requisito opcional).
- Manejo de errores de red: `try/except`, timeouts, mensajes claros al usuario.
- Contrato de API: confirmar endpoints disponibles (GET/POST/PUT/PATCH) y esquema de payloads.
- Mapeo de campos: el modelo remoto incluye `id` y opcionalmente `flag_emoji`; decidir si se exponen en el modo API.

---

### Pasos sugeridos de implementación (secuencia recomendada)
1. Crear `src/function/api_client.py` con `get_countries`, `create_country`, `update_country`.
2. Añadir dependencia `requests` y actualizar README (sección “Modo API”).
3. Agregar opción "10. Alternar modo API (Local/Remoto)" en `app/main.py` y variable `MODO_API`.
4. Adaptar casos 1–6 para leer desde API cuando `MODO_API` sea `True` (ordenar/filtrar localmente sobre la lista recibida).
5. Adaptar casos 7–8 para persistir vía API cuando `MODO_API` sea `True`.
6. Pruebas manuales: lectura remota, alta/edición remota, reconexión tras error de red.

---

### Pruebas recomendadas
- Local (CSV): alta/edición → reiniciar → verificar cambios en `src/db/paises.csv`.
- Remoto (API): listar → alta → listar de nuevo y confirmar presencia; edición → confirmar cambio. Validar con la API: [countries](http://149.50.150.15:8000/countries).
- Ordenamientos/filtrados: comparar resultados entre local y remoto.
- Errores: simular desconexión (cortar internet) y validar mensajes.

---

### Consideraciones de diseño y riesgos
- Concurrencia: si varios usuarios editan sobre la API, puede haber condiciones de carrera; preferir identificadores (`id`) en ediciones.
- Validaciones: centralizar en `validations.py` y reutilizarlas en ambos modos.
- Nombres y consistencia: renombrar `shearch.py` a `search.py` (si el tiempo lo permite) y actualizar importaciones.
- Rutas absolutas: `init.py` debería armar la ruta con `os.path.join(project_root, RUTA_CORRECTA_DB)` para robustez.

---

### Anexo: versión robusta de `leer_csv`
Recomendación para tolerar encabezados alternativos y números con comas:
```python
import csv

def leer_csv(ruta_csv):
    paises = []
    with open(ruta_csv, "r", encoding="UTF-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        for idx, fila in enumerate(lector, start=2):
            nombre = fila.get("nombre") or fila.get("Nombre")
            poblacion_str = fila.get("poblacion") or fila.get("Población")
            superficie_str = fila.get("superficie") or fila.get("Superficie_km2")
            continente = fila.get("continente") or fila.get("Continente")
            if not (nombre and poblacion_str and superficie_str and continente):
                raise ValueError(f"Faltan datos en la fila {idx}: {fila}")
            try:
                poblacion = int(str(poblacion_str).replace(",", "").strip())
                superficie = float(str(superficie_str).replace(",", "").strip())
            except ValueError:
                raise ValueError(f"Valores numéricos inválidos en la fila {idx}: {fila}")
            paises.append({
                "nombre": nombre.strip(),
                "poblacion": poblacion,
                "superficie": superficie,
                "continente": continente.strip(),
            })
    return paises
```

---

### Referencias
- API de países (lectura actual): [http://149.50.150.15:8000/countries](http://149.50.150.15:8000/countries)

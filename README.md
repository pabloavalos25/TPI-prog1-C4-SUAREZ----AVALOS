# TPI Programación 1 — Gestión de Países (Python)

Aplicación de **consola** para consultar y administrar datos de países desde un **CSV local** o una **API REST** remota. Permite **búsquedas**, **filtros**, **ordenamientos**, **estadísticas** y **CRUD** básico.

> Proyecto orientado a cursado inicial (UTN FRM). Código y mensajes en **español**, con funciones sencillas y docstrings estilo Google.

---

## Tabla de contenidos
- [Características](#características)
- [Modos de operación](#modos-de-operación)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración rápida](#configuración-rápida)
- [Ejecución](#ejecución)
- [Menú principal](#menú-principal)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Flujo de datos](#flujo-de-datos)
- [Guía para desarrolladores](#guía-para-desarrolladores)
- [Solución de problemas](#solución-de-problemas)
- [Créditos](#créditos)

---

## Características
- **Fuente de datos dual**:
  - **Local**: `src/db/paises.csv` (lectura/escritura)
  - **API**: servidor FastAPI (HTTP GET/POST/PATCH/DELETE)
- **Operaciones**: buscar por nombre, filtrar por continente, filtrar por **población** o **superficie**, ordenar, estadísticas.
- **CRUD**: agregar, editar y borrar países (en local o API).
- **Compatibilidad**: mensajes en español y funciones con **nombres en español** (por ejemplo, `estado_servidor`, `listar_paises`, `eliminar_pais`).
- **Docstrings**: estilo Google en todos los módulos (mantenibles y legibles).

---

## Modos de operación
- **Local (CSV)**: trabaja con `src/db/paises.csv`. Si no existe, el sistema lo **crea** con el encabezado correspondiente.
- **API**: consume un servidor FastAPI (URL configurable) y replica el mismo menú de opciones sobre la fuente remota.

---

## Requisitos
- **Python** \>= 3.10 (probado en 3.13)
- **Sistema operativo**: Windows / Linux / macOS
- **Dependencias** (modo API): `requests`

**Instalación rápida de dependencias**
```bash
# Windows (PowerShell/CMD)
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install requests

# Linux / macOS
python3 -m pip install --upgrade pip
python3 -m pip install requests
```

Opcional: `requirements.txt`
```text
requests>=2.32.0
```

> Recomendado: crear un **entorno virtual** (venv) antes de instalar dependencias.

---

## Instalación
**Clonar el repositorio**
```bash
git clone https://github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS
cd TPI-prog1-C4-SUAREZ----AVALOS
```

**O descargar ZIP**
1. Abrí el repo en GitHub
2. `Code` → `Download ZIP`
3. Descomprimí la carpeta y abrila en tu editor

---

## Configuración rápida
- **URL de la API**: se define en `src/function/api_client.py` como `BASE_URL` (sin barra final). Ejemplo:
  ```python
  BASE_URL = "http://149.50.150.15:8000"
  ```
- **CSV inicial**: si `src/db/paises.csv` no existe, se crea automáticamente con encabezado:
  ```csv
  nombre,poblacion,superficie,continente
  ```
  Codificación: **UTF-8 con BOM** (para compatibilidad en Windows).

---

## Ejecución
**Windows**
```bash
py app/main.py
# Alternativa
python app/main.py
```
**Linux / macOS**
```bash
python3 app/main.py
```
Al inicio, el sistema:
1. Verifica/crea `src/db/paises.csv` (mueve el archivo si estaba en otra carpeta del proyecto).
2. Solicita el **modo**:
   ```text
   ****Seleccione el servidor****
   1. CSV local
   2. CSV API
   3. Salir
   ```
3. Si elegís API, verifica `/health` con `estado_servidor()`.

---

## Menú principal
```text
**********INFO GEOGRAFICO**********
1.  Buscar pais por nombre
2.  Filtrar por continente
3.  Filtrar por rango de poblacion
4.  Filtrar por rango de superficie
5.  Ordenar paises
6.  Mostrar estadisticas
7.  Agregar un pais
8.  Editar poblacion y superficie de un pais
9.  Borrar país
10. Cambiar modo de servidor
11. Salir
```

**Notas de uso**
- En **Local**, las modificaciones persisten en `src/db/paises.csv`.
- En **API**, se invocan los endpoints remotos (`/countries`, `/countries/{id}`, etc.).

---

## Estructura de carpetas
```text
app/
  └─ main.py               # Menú y selección de fuente (Local/API)
src/
  ├─ db/
  │   └─ paises.csv
  ├─ doc/
  │   ├─ rubrica_correccion_programacion_1.pdf
  │   ├─ tp_integrador _programacion_1.pdf
  │   └─ tp_pautas.md
  └─ function/
      ├─ api_client.py     # Cliente HTTP (estado_servidor, listar_paises, etc.)
      ├─ api_mode.py       # Lógica de modo API: muestra/filtra/ordena con datos remotos
      ├─ data_load.py      # Altas, ediciones y borrados en modo local (CSV)
      ├─ init.py           # Ubica/mueve/crea paises.csv al iniciar
      ├─ shearch.py        # Búsquedas y filtros (local)
      ├─ statistics.py     # Estadísticas generales
      ├─ tools.py          # Utilidades: normalizar, leer/escribir CSV, menús y mensajes
      └─ view.py           # Presentación: listado, ordenar, pedir rangos
README.md
```

---

## Flujo de datos
- **Local**
  - Lee: `tools.leer_csv()` → lista de dicts
  - CRUD en memoria: `data_load.*`
  - Persistencia: `tools.escribir_csv()`

- **API**
  - Cliente: `api_client.py` (`estado_servidor`, `listar_paises`, `crear_desde_dict`, `actualizar_pais_parcial`, `eliminar_pais`, `buscar_por_nombre`)
  - Integración con vistas/filtros: `api_mode.py` (pide datos por consola, reutiliza funciones de `view.py`/`shearch.py`)

---

## Guía para desarrolladores
### Estilo y documentación
- Código y nombres en **español**.
- **Docstrings** estilo Google (módulos, funciones, clases, métodos). Ejemplo:
  ```python
  def listar_paises(q: str | None = None) -> list[dict]:
      """Lista países con filtros y orden opcional.

      Args:
          q (str | None): Texto a buscar por nombre.

      Returns:
          list[dict]: Lista de países.
      """
  ```

### Calidad opcional (linters)
- `ruff` (pydocstyle integrado) + `interrogate` para cobertura de docstrings
  ```toml
  # pyproject.toml
  [tool.ruff]
  line-length = 88
  extend-select = ["D"]  # reglas de docstrings
  ignore = ["D203","D213"]

  [tool.interrogate]
  fail-under = 85
  exclude = ["tests/*","*/migrations/*","venv/*",".venv/*"]
  verbose = 1
  ```
  ```bash
  pip install ruff interrogate
  ruff check .
  interrogate -c pyproject.toml
  ```

---

## Solución de problemas
- **No inicia y aparece un ImportError genérico**
  - Verificá que `src/` o la raíz que contiene `function/` estén en `sys.path`.
  - `main.py` ya incluye lógica para ubicar `function`. Si moviste carpetas, revisá las rutas.

- **Falla al importar por renombres (list_countries → listar_paises)**
  - Asegurate de que **todo** el proyecto use los nombres en **español**:
    - `health` → `estado_servidor`
    - `list_countries` → `listar_paises`
    - `find_by_name` → `buscar_por_nombre`
    - `delete_country` → `eliminar_pais`
    - `create_from_dict` → `crear_desde_dict`
    - `patch_country` → `actualizar_pais_parcial`

- **Python < 3.10**
  - Evitá anotaciones con `|` (Union). Usá `from typing import Union, Optional`.

- **`requests` no instalado (modo API)**
  - Instalalo con `py -3.13 -m pip install requests` (Windows) o `python3 -m pip install requests` (Linux/macOS).

- **CSV vacío o con filas inválidas**
  - El sistema omite filas inválidas e informa cuántas ignoró. Podés abrir el CSV y completar manualmente.

- **Acentos o caracteres raros en consola**
  - Usá PowerShell o Windows Terminal con UTF-8 (o una terminal moderna en Linux/macOS).

---

## Créditos
- **Universidad**: UTN — Facultad Regional Mendoza
- **Carrera**: Tecnicatura Universitaria en Programación
- **Año**: 2025
- **Integrantes**: *Avalos, Pablo* — *Suárez, Ismael*


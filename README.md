## TPI Programación 1 — Gestión de Datos de Países (Python)

### ¿Qué es?
Aplicación de consola en Python para consultar y administrar información de países a partir de un archivo CSV o, opcionalmente, consumiendo una API REST remota. Permite búsquedas, filtros, ordenamientos, estadísticas y CRUD básico (agregar, editar, borrar).

- **Entrada de datos (modo Local)**: `src/db/paises.csv`
- **Servidor (modo API)**: FastAPI remoto (ej.: `http://149.50.150.15:8000`)
- **Interfaz**: Menú por consola (texto)
- **Persistencia**:
  - Local: lee/escribe en `src/db/paises.csv`
  - API: persiste en el servidor vía HTTP

---

### Requisitos
- **Python**: 3.10 o superior (probado con 3.13)
- **Git** (opcional, recomendado para clonar el repositorio)
- Sistema operativo: Windows, Linux o macOS
- **Dependencia (modo API)**: `requests`
  - Windows (PowerShell/CMD):
    ```bash
    py -3.13 -m pip install --upgrade pip
    py -3.13 -m pip install requests
    ```
  - Linux / macOS:
    ```bash
    python3 -m pip install --upgrade pip
    python3 -m pip install requests
    ```
- Opcional: archivo `requirements.txt` con:
  ```text
  requests>=2.32.0
  ```
- Sugerencia (opcional): usar entorno virtual
  - Windows: `python -m venv .venv && .\.venv\Scripts\activate`
  - Linux/macOS: `python3 -m venv .venv && source .venv/bin/activate`

---

### Instalación
- **Opción A (recomendada) — Clonar el repositorio**:
```bash
git clone https://github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS
cd TPI-prog1-C4-SUAREZ----AVALOS
```

- **Opción B — Descargar ZIP**:
  1. Abrí el repositorio: [Repositorio en GitHub](https://github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS)
  2. Hacé clic en "Code" → "Download ZIP"
  3. Descomprimí y abrí la carpeta en tu equipo

---

### Ejecución
- **Windows (PowerShell/CMD/Git Bash)**:
```bash
py app/main.py
```
  - Alternativa:
```bash
python app/main.py
```

- **Linux/macOS**:
```bash
python3 app/main.py
```

Al iniciar, el sistema verificará la existencia de `src/db/paises.csv`. Si el archivo se encuentra en otra carpeta del proyecto, lo moverá a `src/db/`. Si no existe, lo creará con los encabezados correspondientes.

Luego, se te pedirá elegir la fuente de datos:
```text
****Seleccione servidor****
1) CSV local
2) CSV  API
```
- Elegí `1` para usar el CSV local.
- Elegí `2` para usar el servidor API (se comprobará `/health` en la URL configurada).

> URL por defecto del servidor: ver `BASE_URL` en `src/function/api_client.py` (podés editarla si necesitás apuntar a otra).

---

### Menú principal (Local y API)
Al ejecutar el programa, verás el siguiente menú:
```text
**********INFO GEOGRAFICO**********
1. Buscar pais por nombre
2. Filtrar por continente
3. Filtrar por rango de poblacion
4. Filtrar por rango de superficie
5. Ordenar paises
6. Mostrar estadisticas
7. Agregar un pais
8. Editar poblacion y superficie de un pais
9. Borrar país
10. Cambiar modo de servidor
11. Salir
```

- **1) Buscar país por nombre**
  - Ingresá el nombre completo o parcial (ej.: `arg` para Argentina)
  - El sistema muestra coincidencias y continentes disponibles

- **2) Filtrar por continente**
  - Ingresá el continente (ej.: `América`, `Europa`, `Asia`)
  - Se listan los países del continente elegido

- **3) Filtrar por rango de población**
  - Ingresá valores mínimos y máximos (números enteros)
  - Se muestran los países cuya población está dentro del rango

- **4) Filtrar por rango de superficie**
  - Ingresá valores mínimos y máximos (en km²; números)
  - Se listan los países dentro del rango de superficie

- **5) Ordenar países**
  - Campo: `nombre` / `poblacion` / `superficie`
  - Descendente: respondé `s` para sí o `n` para no
  - Se imprime el listado ordenado

- **6) Mostrar estadísticas**
  - Muestra país con mayor/menor población, promedios y cantidad por continente

- **7) Agregar un país**
  - Completá: nombre, continente, población (entero) y superficie (número)
  - En modo Local, se guarda en `src/db/paises.csv` al confirmar
  - En modo API, se envía al servidor (HTTP `POST /countries`)

- **8) Editar un país**
  - Ingresá (parte de) un nombre para buscar y elegí el índice
  - En modo Local, se actualiza en memoria y luego en CSV
  - En modo API, se realiza `PATCH /countries/{id}`

- **9) Borrar país**
  - En modo Local, se elimina del CSV
  - En modo API, podés borrar por nombre (selección) o por id (`DELETE /countries/{id}`)

- **10) Cambiar modo de servidor**
  - Permite cambiar entre `CSV local` y `API` sin reiniciar el programa
  - Al elegir `API`, se verifica la conexión con `/health`
  - La URL utilizada proviene de `BASE_URL` en `src/function/api_client.py`
  - Si necesitás otra URL, editá `BASE_URL` manualmente en ese archivo

- **11) Salir**
  - Finaliza el programa

---

### Modo API (detalles rápidos)
- Cliente HTTP: `src/function/api_client.py`
- Endpoints utilizados:
  - `GET /health`
  - `GET /countries` (listado + filtros/orden)
  - `GET /countries/{id}` (detalle)
  - `POST /countries` (crear)
  - `PATCH /countries/{id}` (editar)
  - `DELETE /countries/{id}` (borrar)

Tip rápido para probar la API (reemplazá `<IP>` y `<PUERTO>` si aplica):
```bash
curl http://<IP>:<PUERTO>/health
curl "http://<IP>:<PUERTO>/countries?sort_by=nombre"
```

> Nota: la URL por defecto está en `BASE_URL` dentro de `src/function/api_client.py`. Podés cambiarla editando ese archivo.

---

### Funcionalidades
- **Búsqueda**: por nombre (parcial o exacto)
- **Filtros**: por continente, por rango de población y por superficie
- **Ordenamiento**: por nombre, población o superficie (asc/desc)
- **Estadísticas**: máximos/mínimos, promedios y cantidad por continente
- **CRUD básico**: agregar, editar y borrar (Local: CSV; API: servidor)

---

### Estructura del proyecto
```text
app/
  └─ main.py               # menú y selección de fuente de datos (Local/API)
src/
  ├─ db/
  │   └─ paises.csv
  ├─ doc/
  │   ├─ rubrica_correccion_programacion_1.pdf
  │   ├─ tp_integrador _programacion_1.pdf
  │   └─ tp_pautas.md
  └─ function/
      ├─ api_client.py     # cliente HTTP (GET/POST/PATCH/DELETE)
      ├─ api_mode.py       # integra API con el menú
      ├─ data_load.py      # altas/ediciones/borrado en modo local
      ├─ init.py           # prepara/ubica/crea paises.csv
      ├─ shearch.py        # búsquedas y filtros
      ├─ statistics.py     # estadísticas
      ├─ tools.py          # utilidades (normalizar, leer/escribir)
      ├─ validations.py
      └─ view.py           # impresión y ordenamiento
ANALISIS_APLICACION.md
README.md
```

---

### Solución de problemas
- **Python no es reconocido**: verificá la instalación y que `python`/`py`/`python3` estén en el PATH
- **Falta `requests` (modo API)**:
  - Windows: `py -3.13 -m pip install requests`
  - Linux/macOS: `python3 -m pip install requests`
- **Imports fallan en otra PC**:
  - Confirmá que existan `src/__init__.py` y `src/function/__init__.py` (pueden estar vacíos)
  - Asegurate de instalar `requests` en el mismo Python con el que ejecutás el programa
- **Problemas con el CSV**: el sistema intentará ubicar o crear `src/db/paises.csv` al iniciar
- **Acentos o caracteres raros**: usá una consola con soporte UTF-8 (p. ej., Windows Terminal o PowerShell moderno)

---

### Enlaces
- **Repositorio**: [github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS](https://github.com/pabloavalos25/TPI-prog1-C4-SUAREZ----AVALOS)
- **Análisis técnico**: `ANALISIS_APLICACION.md`

---

### Créditos
Universidad: UTN Regional Mendoza
TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN
Año: 2025
Integrantes: - Avalos Pablo  - Suarez Ismael

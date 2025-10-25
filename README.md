## TPI Programación 1 — Gestión de Datos de Países (Python)

### ¿Qué es?
Aplicación de consola en Python para consultar y administrar información de países a partir de un archivo CSV. Permite búsquedas, filtros, ordenamientos y estadísticas básicas.

- **Entrada de datos**: `src/db/paises.csv`
- **Interfaz**: Menú por consola (texto)
- **Persistencia**: Lectura desde CSV; por ahora, las altas/ediciones se mantienen solo en memoria durante la ejecución

---

### Requisitos
- **Python**: 3.10 o superior
- **Git** (opcional, recomendado para clonar el repositorio)
- Sistema operativo: Windows, Linux o macOS

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

---

### Manual de usuario (paso a paso)
Al ejecutar el programa, verás el siguiente menú:
```text
*****INFO GEOGRAFICO*****
1. Buscar pais por nombre
2. Filtrar por continente
3. Filtrar por rango de poblacion
4. Filtrar por rango de superficie
5. Ordenar paises
6. Mostrar estadisticas
7. Agregar un pais
8. Editar poblacion y superficie de un pais
9. Salir
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
  - El país se agrega a la lista actual (en memoria durante esta ejecución)

- **8) Editar un país**
  - Ingresá (parte de) un nombre para buscar
  - Elegí el índice del país a editar
  - Ingresá nueva población y superficie

- **9) Salir**
  - Finaliza el programa

> Nota: Los cambios de alta/edición ahora se guardan automáticamente en `src/db/paises.csv` al confirmar cada operación.

---

### Funcionalidades
- **Búsqueda**: por nombre (parcial o exacto)
- **Filtros**: por continente, por rango de población y por superficie
- **Ordenamiento**: por nombre, población o superficie (asc/desc)
- **Estadísticas**: máximos/mínimos, promedios y cantidad por continente

---

### Estructura del proyecto
```text
app/
  └─ main.py
src/
  ├─ db/
  │   └─ paises.csv
  ├─ doc/
  │   ├─ rubrica_correccion_programacion_1.pdf
  │   ├─ tp_integrador _programacion_1.pdf
  │   └─ tp_pautas.md
  └─ function/
      ├─ data_load.py
      ├─ init.py
      ├─ shearch.py
      ├─ statistics.py
      ├─ tools.py
      ├─ validations.py
      └─ view.py
ANALISIS_APLICACION.md
README.md
```

- **Módulos principales**
  - `app/main.py`: entrada del programa y menú
  - `src/function/shearch.py`: búsquedas y filtros
  - `src/function/view.py`: impresión de listados y ordenamientos
  - `src/function/statistics.py`: estadísticas
  - `src/function/data_load.py`: alta/edición en memoria
  - `src/function/tools.py`: utilidades (normalizar texto, leer CSV)
  - `src/function/init.py`: asegura la existencia/ubicación de `paises.csv`

---

### Solución de problemas
- **Python no es reconocido**: verificá la instalación y que `python`/`py`/`python3` estén en el PATH
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

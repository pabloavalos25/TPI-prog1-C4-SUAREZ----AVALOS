TPI Programación 1 — Gestión de Datos de Países (Python)

Aplicación de consola en Python para gestionar información de países: búsqueda, filtros, ordenamientos y estadísticas a partir de un CSV. Está pensada para ejercitar listas, diccionarios, funciones, condicionales, manejo de archivos y cálculos básicos, según el enunciado del TPI.

Objetivos del proyecto
Leer un dataset de países desde un archivo CSV.

Permitir:
Búsqueda por nombre (parcial o exacta).
Filtros por continente, rango de población y rango de superficie.
Ordenamientos por nombre, población o superficie (asc/desc).

Estadísticas: país con mayor/menor población, promedios y cantidad por continente.

Estructura del repositorio
app/
  └─ main.py
src/
  └─ db/
  │   └─ paises.csv
  doc/
  │   ├─ rubrica_correccion_programacion_1.pdf
  │   ├─ tp_integrador _programacion_1.pdf
  │   └─ tp_pautas.md   
  function/
      ├─ data_load.py
      ├─ init.py
      ├─ shearch.py
      ├─ statistics.py
      ├─ validatons.py
      └─ view.py
 README.md

Módulos principales

app/main.py: punto de entrada, muestra el menú y orquesta las opciones.
tools/shearch.py: funciones de búsqueda, filtros y ordenamientos.
tools/validaciones.py: validación de entradas, rangos y tipos.
tools/view.py: helpers de salida por consola (tablas/listados).
src/db/paises.csv: dataset base requerido por la consigna.

Requisitos
Python 3.x (según consigna). No se requieren librerías externas.

Cómo ejecutar:
Cloná el repositorio y ubicáte en la carpeta del proyecto.

Ejecutá la aplicación:
python app/main.py


Asegurate de que src/db/paises.csv esté presente (obligatorio para la entrega).

Uso (menú)
            print("*****INFO GEOGRAFICO*****")
            print("1. Buscar pais por nombre")
            print("2. Filtrar por continente")
            print("3. Filtrar por rango de poblacion")
            print("4. Filtrar por rango de superficie")
            print("5. Ordenar paises")
            print("6. Mostrar estadisticas")
            print("7. Agregar un pais")
            print("8. Editar poblacion y superficie de un pais")
            print("9. Salir")


Ejemplo:

Argentina,45376763,2780400,América
Japón,125800000,377975,Asia


Calidad del código y validaciones (según rúbrica)

Manejo de archivos CSV: lectura robusta, conversión de tipos y manejo de excepciones.

Lógica de filtros y ordenamientos: precisa y eficiente.
Modularidad: una función = una responsabilidad; código claro y cohesivo.
Legibilidad y comentarios: nombres significativos y comentarios útiles.
Manejo de errores (try/except) con mensajes claros al usuario.

Entregables y criterios de aprobación
Repositorio GitHub público con README detallado, proyecto completo y CSV.
Video explicativo de 10–15 minutos

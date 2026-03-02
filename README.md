# Proyecto: Data Management

**Materia:** Ciencia de datos en la toma de las decisiones de las organizaciones

**Alumnos:**
1. Rodrigo Jafet Osorio Angeles
2. Adolfo Román Jiménez
3. Sebastian Emiliano Gayosso Rosillo
4. Jaime Manuel Miranda Serrano
5. Francisco Joshua Quintero Montero
6. Alexa Fernanda López Tavera 

## Descripción del Proyecto
Este repositorio contiene la resolución a un test de tratamiento y manipulación de datos. El objetivo principal es la ingesta, transformación y extracción de información a partir de registros escolares (estudiantes, asignaturas e inscripciones) para la posterior toma de decisiones, utilizando Python y metodologías ETL.

## Procesamiento de Datos (`data_management.py`)
El script de Python procesa la información de los archivos de origen (`Estudiantes.csv`, `Asignaturas.csv` e `Inscripcion.csv`) mediante los siguientes pasos:

1. **Carga e Integración:** Lee los datos de los CSV de origen y los estructura para su manipulación relacional.
2. **Análisis de Rendimiento (Ejercicio 1):** 
   * Calcula el promedio general de calificaciones por cada materia.
   * Filtra y obtiene las 3 calificaciones más altas de cada asignatura.
   * Genera una bandera comparativa (`1` si la calificación del alumno es mayor al promedio de la materia, `0` si es menor o igual).
   * Exporta un archivo CSV únicamente con los alumnos que superaron el promedio.
3. **Avance de Créditos (Ejercicio 2):**
   * Calcula el porcentaje de avance de materias cursadas por cada alumno respecto al total del plan de estudios.
   * Asigna una bandera de clasificación (del `1` al `5`) dependiendo del rango porcentual de avance del estudiante.
   * Extrae dos subconjuntos: el Top 10 de alumnos con mayor avance y el Bottom 10 con menor avance, exportando solo sus nombres a un nuevo archivo CSV.

---

## Resolución de Preguntas Teóricas

### Pregunta 3: Carga de archivos CSV en una base de datos mediante ETL
**Herramienta propuesta:** Pentaho Data Integration (Kettle) / Talend Open Studio

El procedimiento estándar usando un flujo ETL gráfico consistiría en tres fases:

1. **Extracción (Extract):** Se agrega un nodo de entrada. Se configura la ruta de los archivos CSV generados en los ejercicios anteriores, definiendo el delimitador y el tipo de dato para cada columna.
2. **Transformación (Transform):** Se utiliza un nodo intermedio para mapear los nombres de las columnas del CSV a los nombres exactos que tienen los campos en la tabla de la base de datos destino. 
3. **Carga (Load):** Se agrega un nodo de salida. Se configuran las credenciales de conexión hacia el manejador de base de datos objetivo. Se selecciona la tabla destino, se activa la opción de mapeo de campos y se ejecuta el flujo para insertar los registros.

### Pregunta 4: Limpieza de caracteres y nulos con flujos analíticos
**Herramienta propuesta:** Tableau Prep Builder

Para retirar campos vacíos y caracteres especiales de un archivo CSV y depositarlo en un repositorio, los pasos dentro del flujo serían:

1. **Conexión:** Se arrastra el archivo CSV al lienzo para crear el nodo inicial de ingesta de datos.
2. **Paso de Limpieza (Clean Step):** Se añade un nodo de limpieza inmediatamente después de la conexión.
   * **Retirar campos vacíos:** Se seleccionan las columnas clave y se aplica un filtro para excluir o remover los valores nulos.
   * **Retirar caracteres especiales:** Para eliminar comas, saltos de línea, diagonales y pipelines de los campos, se crea un campo calculado. Se utiliza una función de reemplazo o expresiones regulares (ej. `REGEXP_REPLACE`) para sustituir esos caracteres por una cadena vacía.
3. **Salida (Output):** Se añade un nodo de salida al final del flujo para depositarlo en el repositorio. Se configura para guardar el resultado como una tabla en una base de datos o como un archivo CSV limpio, y se ejecuta el flujo.

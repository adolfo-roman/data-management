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

Para que este proceso sea exitoso en la herramienta eligida de nombre Pentaho (PDI) se debe considerar lo siguiente:

El proceso de integración de archivos CSV en un motor de base de datos relacional se estructura a través de un flujo de trabajo que prioriza la integridad y la eficiencia del procesamiento.

***1. Fase de Extracción: Configuración y Normalización de Origen***

En esta etapa, se establece la conexión con el archivo plano y se definen los parámetros de lectura:

* Codificación de Caracteres: Se debe especificar el
formato (comúnmente UTF-8) para garantizar la correcta interpretación de caracteres especiales y tildes
* Definición de Esquema: Se realiza la asignación manual de tipos de datos para cada columna (Entero, Cadena, Fecha, Flotante), evitando la detección automática si existen valores nulos que puedan inducir a error.
* Tratamiento de Delimitadores: Se configura el separador de campos (coma, punto y coma o tabulación) y el símbolo de encerrado de texto para prevenir rupturas en la estructura del registro.


***2. Fase de Transformación: Limpieza y Mapeo (Data Cleansing)***

Antes de la inserción, los datos deben someterse a una validación estructural:

* Normalización de Formatos: Se transforman los formatos de fecha del CSV al estándar requerido por el motor de base de datos (por ejemplo, de DD/MM/YYYY a YYYY-MM-DD).
* Limpieza de Espacios: Se aplica una operación de Trim para eliminar espacios en blanco accidentales al inicio o final de las cadenas de texto.
* Resolución de Conflictos: Se utiliza un componente de mapeo (como Select Values o tMap) para alinear técnicamente los nombres de las columnas del origen con los nombres de los campos en el esquema de destino.

***3. Fase de Carga: Inserción y Control de Errores***

La fase final se encarga de la persistencia de los datos en el servidor de destino:

* Configuración de Conexión: Se establecen los parámetros del host, puerto, base de datos y credenciales mediante el uso de drivers JDBC o nativos.
* Optimización de Carga: Se define un tamaño de lote (Commit Size) para procesar registros en bloques, lo que reduce el consumo de recursos y el tiempo de ejecución.
* Gestión de Excepciones: Se implementa un flujo de salida de errores hacia un archivo de registro (Log). Esto permite que, en caso de que un registro viole una restricción de integridad (como una llave primaria duplicada), el proceso continúe con el resto de la carga sin detenerse.

  
### Pregunta 4: Limpieza de caracteres y nulos con flujos analíticos
**Herramienta propuesta: Tableau Prep Builder**

Para retirar campos vacíos y caracteres especiales de un archivo CSV y depositarlo en un repositorio mediante un flujo analítico, los pasos a seguir son los descritos a continuación:

1. Se arrastra el archivo CSV al lienzo para crear el nodo inicial de ingesta de datos.

2. Se utiliza el perfil de datos para identificar campos vacíos, valores nulos, registros incompletos o problemas en delimitadores.

3. Se añade un nodo de limpieza inmediatamente después de la conexión. Se aplican filtros sobre columnas clave para excluir registros con valores nulos o reemplazarlos por valores por defecto según la lógica del negocio. Para eliminar comas internas, saltos de línea, diagonales, pipelines (`|`) u otros caracteres problemáticos, se crea un campo calculado usando funciones de reemplazo o expresiones regulares como `REGEXP_REPLACE`. También se estandarizan los datos aplicando funciones como `TRIM`, conversión a mayúsculas/minúsculas y validación de tipos de dato.

4. Se verifica que el número de columnas sea consistente, que no existan delimitadores mal interpretados y que los tipos de datos sean correctos.

5. Finalmente, se añade un nodo de salida para guardar el CSV limpio como un nuevo archivo o insertarlo directamente en una base de datos (data warehouse o almacenamiento en la nube) mediante conexión ODBC/JDBC, ejecutando el flujo para depositarlo en el repositorio final.
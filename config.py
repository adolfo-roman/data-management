# Rodrigo Osorio
# Rutas de archivos de entrada

PATH_ASIGNATURAS = 'Asignaturas.csv'
PATH_ESTUDIANTES = 'Estudiantes.csv'
PATH_INSCRIPCION = 'Inscripcion.csv'

# Rutas de archivos de salida

OUT_ALUMNOS_DESTACADOS = 'alumnos_mayor_promedio.csv'
OUT_TOP_BOTTOM_AVANCE = 'top_y_bottom_10_alumnos.csv'

# Validación de esquemas

REQUIRED_COLS = {
    'inscripcion': {'num_cuenta', 'asignatura_id', 'calificacion'},
    'estudiantes': {'numero_cuenta', 'nombre'},
    'asignaturas': {'asignatura_id', 'nombre'}
}

# Parámetros para el ejercicio 2
# Definición de rangos para pd.cut Binning
# Bins: [0-40), [40-65), [65-80), [80-100), 100+
# Registros a mostrar en el ejercicio 2

AVANCE_BINS = [-0.01, 40, 65, 80, 100, 101]
AVANCE_LABELS = ['1', '2', '3', '4', '5']
MAX_ROWS_DISPLAY = 10  
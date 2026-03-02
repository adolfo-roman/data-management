# Data Management
# Ciencia de datos en la toma de decisiones en la organizaciones 

import pandas as pd
import numpy as np
import os
import sys

# Definición de columnas requeridas para validación de esquemas
REQUIRED_COLUMNS_INS = {"num_cuenta", "asignatura_id", "calificacion"}
REQUIRED_COLUMNS_EST = {"numero_cuenta", "nombre"}
REQUIRED_COLUMNS_ASG = {"asignatura_id", "nombre"}

# Validación de archivos y estructuras de datos

def validar_archivo(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo crítico '{ruta}' no existe en el directorio.")

# Carga CSV y valida que no esté vacío y contenga las columnas requeridas
def cargar_csv_validado(path, min_cols=None):
    validar_archivo(path)
    df = pd.read_csv(path)
    
    if df.empty:
        raise ValueError(f"El archivo {path} está completamente vacío.")
    
    if min_cols:
        faltantes = set(min_cols) - set(df.columns)
        if faltantes:
            raise ValueError(f"Estructura corrupta en {path}. Faltan las columnas: {faltantes}")
    return df

# Carga y preparación de los datos
def preparar_datos():
    df_asignaturas = cargar_csv_validado("Asignaturas.csv", min_cols=REQUIRED_COLUMNS_ASG)
    df_estudiantes = cargar_csv_validado("Estudiantes.csv", min_cols=REQUIRED_COLUMNS_EST)
    df_inscripcion = cargar_csv_validado("Inscripcion.csv", min_cols=REQUIRED_COLUMNS_INS)

    # Estandarización de llaves foráneas
    df_inscripcion = df_inscripcion.rename(columns={"num_cuenta": "numero_cuenta"})

    # Merge encadenado manejando los sufijos automáticos _x e _y de Pandas
    df = (
        df_inscripcion
        .merge(df_estudiantes, on="numero_cuenta", how="inner")
        .merge(df_asignaturas, on="asignatura_id", how="inner")
        .rename(columns={"nombre_x": "nombre alumno", "nombre_y": "nombre materia"})
    )

    return df, df_asignaturas

# Ejercicio 1: Análisis de calificaciones

def ejercicio_1(df):
    """Análisis de calificaciones con optimización transform y ordenamiento visual."""
    print("\n" + "=" * 40 + "\nEJERCICIO 1: CALIFICACIONES POR ASIGNATURA\n" + "=" * 40)

    # Transformación vectorizada
    df["calificacion promedia"] = df.groupby("nombre materia")["calificacion"].transform("mean")
    df["bandera"] = np.where(df["calificacion"] > df["calificacion promedia"], 1, 0)

    # Ordenamiento dual para claridad visual
    top3 = (
        df.sort_values(["nombre materia", "calificacion"], ascending=[True, False])
        .groupby("nombre materia", group_keys=False)
        .head(3)
    )

    columnas_salida = ["nombre alumno", "nombre materia", "calificacion", "calificacion promedia", "bandera"]
    print(top3[columnas_salida].to_string(index=False))

    alumnos_destacados = df[df["bandera"] == 1][["nombre alumno"]].drop_duplicates()
    alumnos_destacados.to_csv("alumnos_mayor_promedio.csv", index=False)
    print("\nArchivo 'alumnos_mayor_promedio.csv' generado correctamente.")


# Ejercicio 2: Avance académico

def ejercicio_2(df, df_asignaturas):
    # Análisis de avance utilizando pd.cut para binning eficiente
    print("\n" + "=" * 40 + "\nEJERCICIO 2: AVANCE ACADÉMICO\n" + "=" * 40)

    total_materias = len(df_asignaturas)

    avance_df = (
        df.groupby(["numero_cuenta", "nombre alumno"])["asignatura_id"]
        .nunique()
        .reset_index(name="total materias tomadas")
    )

    avance_df["total materias"] = total_materias
    avance_df["porcentaje avance"] = ((avance_df["total materias tomadas"] / total_materias) * 100).round(2)

    # Binning perfecto con pd.cut
    bins = [-0.01, 40, 65, 80, 100, 101] 
    labels = ['1', '2', '3', '4', '5']
    avance_df["bandera clasificacion"] = pd.cut(
        avance_df["porcentaje avance"], 
        bins=bins, 
        labels=labels, 
        right=False
    )

    # Orden y limpieza
    avance_df = (
        avance_df.sort_values(by=["porcentaje avance", "nombre alumno"], ascending=[False, True])
        .drop_duplicates(subset=["nombre alumno"])
    )

    columnas_salida = ["nombre alumno", "total materias tomadas", "total materias", "porcentaje avance", "bandera clasificacion"]

    print("\n--- CONSULTA GENERAL (TOP 10) ---")
    print(avance_df[columnas_salida].head(10).to_string(index=False))

    top_10 = avance_df.head(10)
    bottom_10 = avance_df.tail(10)

    print("\n--- ANÁLISIS DE EXTREMOS ---")
    print("\nTOP 10:")
    print(top_10[["nombre alumno", "porcentaje avance", "bandera clasificacion"]].to_string(index=False))

    print("\nBOTTOM 10:")
    print(bottom_10[["nombre alumno", "porcentaje avance", "bandera clasificacion"]].to_string(index=False))

    pd.concat([top_10[["nombre alumno"]], bottom_10[["nombre alumno"]]]).to_csv("top_y_bottom_10_alumnos.csv", index=False)
    print("\n Archivo 'top_y_bottom_10_alumnos.csv' generado correctamente.")

# MAIN EXECUTION

def main():
    try:
        df_completo, df_asignaturas = preparar_datos()
        ejercicio_1(df_completo.copy())
        ejercicio_2(df_completo.copy(), df_asignaturas)
        print("\n Script finalizado con éxito.")
    except Exception as e:
        print(f"\n Se detuvo la ejecución por un error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

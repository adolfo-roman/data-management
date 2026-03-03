
import pandas as pd
import numpy as np

def analizar_calificaciones(df_maestro: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza el análisis de calificaciones por materia.
    
    Args:
        df_maestro (pd.DataFrame): El DataFrame principal con las tablas ya unidas.
        
    Returns:
        pd.DataFrame: Un DataFrame filtrado (solo bandera == 1) listo para ser guardado como CSV.
    """
    print("\n" + "=" * 50)
    print("EJERCICIO 1: ANÁLISIS DE CALIFICACIONES")
    print("=" * 50)

    # 1. Trabajamos con una copia para no alterar los datos en memoria para otros ejercicios
    df = df_maestro.copy()

    # 2. Calcular el promedio por materia de forma vectorizada
    # Usamos .round(2) para que se vea limpio como en el ejemplo (ej. 7.15, 7.68)
    df["calificacion promedia"] = (
        df.groupby("nombre materia")["calificacion"]
        .transform("mean")
        .round(2)
    )

    # 3. Crear bandera: '1' si calificación > promedio, '0' si es menor o igual
    df["bandera"] = np.where(df["calificacion"] > df["calificacion promedia"], 1, 0)

    # 4. Obtener las 3 calificaciones más altas por cada asignatura
    # Ordenamos por Materia (ascendente), Calificación (descendente) y Bandera (descendente)
    top3_por_materia = (
        df.sort_values(
            by=["nombre materia", "calificacion", "bandera"], 
            ascending=[True, False, False]
        )
        .groupby("nombre materia", group_keys=False)
        .head(3)
    )

    # Definimos explícitamente las columnas solicitadas para la salida
    columnas_salida = [
        "nombre alumno", 
        "nombre materia", 
        "calificacion", 
        "calificacion promedia", 
        "bandera"
    ]


    # 5. Mostrar en consola el resultado (Los 150 registros para la terminal)
    print(f"\n--- CONSULTA: TOP 3 POR MATERIA (Total registros: {len(top3_por_materia)}) ---")
    with pd.option_context('display.max_rows', None):
        # Esta es la salida de 116-121 registros que te gustó y NO cambia
        print(top3_por_materia[columnas_salida].to_string(index=False))

    # 6. Preparar variable para el Excel (Ajuste para obtener los 28 alumnos únicos)
    # Filtramos por bandera 1 y luego eliminamos duplicados por nombre de alumno
    alumnos_unicos_excel = (
        top3_por_materia[top3_por_materia["bandera"] == 1][columnas_salida]
        .drop_duplicates(subset=['nombre alumno'])
        .copy()
    )
    
    print(f"\n💡 Análisis de exportación completado.")
    print(f"-> Se empaquetaron {len(alumnos_unicos_excel)} registros únicos con detalle completo para el CSV.")

    return alumnos_unicos_excel
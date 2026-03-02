"""
data_loader.py
Módulo responsable de la extracción, validación y transformación inicial (Merge) de los datos.
"""

import os
import pandas as pd
import config

def cargar_csv_validado(ruta: str, columnas_esperadas: set) -> pd.DataFrame:
    """
    Carga un archivo CSV validando su existencia, que no esté vacío y su estructura.
    """
    # 1. Validar existencia física del archivo
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"❌ Error Crítico: No se encontró el archivo '{ruta}'.")
    
    # 2. Carga en memoria
    df = pd.read_csv(ruta)
    
    # 3. Validar que tenga datos
    if df.empty:
        raise ValueError(f"❌ Error Crítico: El archivo '{ruta}' está completamente vacío.")
    
    # 4. Validar esquema (que contenga las columnas que necesitamos)
    faltantes = columnas_esperadas - set(df.columns)
    if faltantes:
        raise ValueError(f"❌ Error de Esquema en '{ruta}'. Faltan las columnas: {faltantes}")
    
    print(f"✅ Archivo cargado y validado exitosamente: {ruta}")
    return df

def preparar_datos() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Orquesta la carga de los 3 archivos, estandariza las llaves y realiza los merges.
    Retorna el DataFrame maestro combinado y el catálogo de asignaturas.
    """
    print("\n--- INICIANDO CARGA Y VALIDACIÓN DE DATOS ---")
    
    # Carga validada usando las constantes de config.py
    df_asig = cargar_csv_validado(config.PATH_ASIGNATURAS, config.REQUIRED_COLS['asignaturas'])
    df_est = cargar_csv_validado(config.PATH_ESTUDIANTES, config.REQUIRED_COLS['estudiantes'])
    df_ins = cargar_csv_validado(config.PATH_INSCRIPCION, config.REQUIRED_COLS['inscripcion'])

    # [cite_start]Estandarización de llaves (Arreglamos la discrepancia num_cuenta vs numero_cuenta) [cite: 8, 9]
    if 'num_cuenta' in df_ins.columns:
        df_ins = df_ins.rename(columns={'num_cuenta': 'numero_cuenta'})

    print("🔄 Realizando uniones (Merges)...")
    
    # Merge encadenado (Method Chaining)
    # Unimos inscripciones con estudiantes, y luego el resultado con asignaturas
    df_maestro = (
        df_ins
        .merge(df_est, on="numero_cuenta", how="inner")
        .merge(df_asig, on="asignatura_id", how="inner")
    )

    # Manejo del comportamiento nativo de Pandas (sufijos _x e _y en columnas duplicadas)
    # [cite_start]Al tener 'nombre' en estudiantes y 'nombre' en asignaturas, Pandas las renombra [cite: 5, 10]
    df_maestro = df_maestro.rename(columns={
        'nombre_x': 'nombre alumno', 
        'nombre_y': 'nombre materia'
    })
    
    print(f"✅ Datos preparados. Total de registros a analizar: {len(df_maestro)}")
    
    return df_maestro, df_asig

# Bloque de prueba local (Solo se ejecuta si corres este archivo directamente, útil para debug)
if __name__ == "__main__":
    try:
        df, catalogo = preparar_datos()
        print("\nMuestra del DataFrame Maestro:")
        print(df.head())
    except Exception as e:
        print(e)
""" 
 Módulo principal. Ejecuta todo el pipeline de trabajo. 

    1.- Procesa los archivos CSV de entrada y los guarda en un directorio limpio. 

    2.- Sube los archivos CSV a un bucket de S3.
    
    3.- Ejecuta consultas SQL en Athena y guarda los resultados en un directorio local.
    
    4.- Genera gráficos de los resultados.
    
    5.- Genera un modelo de recomendación de cervezas.
"""
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
import os
import boto3
import sys


from src.py.load import load_data
from src.py.transform import process_csv_files
from src.py.athena_db import (
    create_database,
    create_table,
    calcular_cervezas_per_brewery,
    calcular_cervezas_per_style,
    sensaciones_top_estilos,
)

def main():
    """
    Función principal que ejecuta el pipeline de trabajo.
    """
    # Definimos los directorios de entrada y salida
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "data/raw"
    output_dir = base_dir / "data/clean"

    # Leemos los archivos de entrada y los procesamos
    process_csv_files(input_dir, output_dir)
    print("Archivos CSV procesados y guardados en data/clean.")
    # Leemos el archivo CSV procesado
    if "sphinx" not in sys.modules:
        df = pd.read_csv(output_dir / "beer_profile_and_ratings.csv")
    # Mostramos las primeras filas del DataFrame
    print(df.head())

    # Subimos el archivo CSV a S3
    #session = boto3.Session(profile_name="arquitectura")
    session = boto3.Session()
    s3 = session.client("s3")
    if load_data(s3):
        print("Datos subidos a S3")
    else:
        print("Error  al subir datos a S3")

    # ======EDA=========
    # Creamos una serie de consultas SQL desde Athena
    # Guardamos las consultas en archivos locales para graficación
    load_dotenv()
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    # Create AWS session
    output_bucket = f"s3://{BUCKET_NAME.strip('/')}/beer/queries"
    # Creamos directorio local para guardar los resultados del query
    project_root = Path(__file__).resolve().parent  # Esto es donde está main.py
    data_dir = project_root / "data/queries"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create Database
    create_database(session)
    create_table(session, BUCKET_NAME)

    # Ejecutamos consultas:
    print("Cervezas por Cervecería:\n")
    df_query = calcular_cervezas_per_brewery(session, output_bucket)
    print(df_query.head(5))

    # Guardamos el resultado en un archivo local
    df_query.to_csv(data_dir / "cervezas_per_brewery.csv", index=False)
    print(f"Archivo guardado en {data_dir}/cervezas_per_brewery.csv")

    # print("Cervezas por Estilo:\n")
    df_query = calcular_cervezas_per_style(session, output_bucket)
    print(df_query.head(5))

    # Guardamos el resultado en un archivo local
    df_query.to_csv(data_dir / "cervezas_per_style.csv", index=False)
    print(f"Archivo guardado en {data_dir}/cervezas_per_style.csv")

    print("Sensaciones predominantes en top 10 estilos\n ")
    df_query = sensaciones_top_estilos(session, output_bucket)
    print(df_query.head(5))
    # Guardamos el resultado en un archivo local
    df_query.to_csv(data_dir / "sensaciones_top_estilos.csv", index=False)
    print(f"Archivo guardado en {data_dir}/sensaciones_top_estilos.csv")

    ###=======RECOMENDADOR DE CERVEZAS===========


if __name__ == "__main__":
    main()

"""
Modulo que realiza una exploración de los datos de la base

Funciones: 

    1.- **create_database**: Crea una base de datos en Athena

    2.- **create_table**: Crea una tabla en Athena
    
    3.- **calcular_cervezas_per_brewery**: Calcula el número de cervezas por cervecería
"""

import awswrangler as wr



# Creamos un database en Athena
def create_database(session):
    """
    Función que crea una base de datos en Athena

    Args:
        sesion: Sesión de boto3
    """
    create_db_query = "CREATE DATABASE IF NOT EXISTS beer_db"
    wr.athena.start_query_execution(sql=create_db_query, boto3_session=session)


def create_table(session, BUCKET_NAME):
    """
    Función que crea una tabla en Athena

    Args:
        sesion: Sesión de boto3
        BUCKET_NAME: Nombre del bucket de S3 donde se encuentran los datos
    """
    location = f"s3://{BUCKET_NAME}/beer/clean/beer_profile_and_ratings.csv"
    create_table_query = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS beer_db.beer(
    name STRING,
    style STRING,
    brewery STRING,
    beer_name_full STRING,
    description STRING,
    abv FLOAT,
    min_ibu INT,
    max_ibu INT,
    astringency FLOAT,
    body FLOAT,
    alcohol FLOAT,
    bitter FLOAT,
    sweet FLOAT,
    sour FLOAT,
    salty FLOAT,
    fruits FLOAT,
    hoppy FLOAT,
    spices FLOAT,
    malty FLOAT,
    review_aroma FLOAT,
    review_appearance FLOAT,
    review_palate FLOAT,
    review_taste FLOAT,
    review_overall FLOAT,
    number_of_reviews INT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE
    LOCATION '{location}'
    """
    wr.athena.start_query_execution(sql=create_table_query, boto3_session=session)


# ========EDA=========
# A base de consultas de SQL desde Athena, se generan archivos locales para graficación


def calcular_cervezas_per_brewery(session, output_bucket):
    """
    Función que calcula el número de cervezas por cervecería

    Args:
        sesion: Sesión de boto3
        output_bucket: Bucket de salida
    Returns:
        Dataframe: Respuesta de la consulta con el número de cervezas por cervecería
    """
    # Definir la consulta SQL
    query = """
    SELECT brewery, COUNT(*) as beer_count
    FROM beer_db.beer
    GROUP BY brewery
    ORDER BY beer_count DESC;
    """
    response = wr.athena.read_sql_query(
        sql=query,
        database="beer_db",  # Especifica la base de datos
        boto3_session=session,
        ctas_approach=False,  # ⚠️ Esto fuerza a no usar CTAS (no cachea)
    )
    # Mostrar las primeras filas del DataFrame
    print("Primeras filas de la consulta cervezas por brewery:")
    print(response.head())
    # Guardar el resultado en un archivo CSV
    local_filename = "cervezas_per_brewery.csv"

    # Guardar el resultado en un archivo CSV dentro del bucket de salida
    wr.s3.to_csv(df=response, path=f"{output_bucket}/{local_filename}", index=False)
    print(f"Consulta guardada en {output_bucket}/{local_filename}")

    return response


def calcular_cervezas_per_style(session, output_bucket):
    """
    Función que calcula el número de cervezas por estilo

    Args:
        sesion: Sesión de boto3
        output_bucket: Bucket de salida
    Returns:
        Dataframe: Respuesta de la consulta con las cervezas por estilo 
    
    """
    # Definir la consulta SQL
    query = """
    SELECT style, COUNT(*) as beer_count
    FROM beer_db.beer
    GROUP BY style
    ORDER BY beer_count DESC;
    """
    response = wr.athena.read_sql_query(
        sql=query,
        database="beer_db",  # Especifica la base de datos
        boto3_session=session,
    )
    print("Primeras filas de la consulta cervezas por style:")
    print(response.head())
    # Guardar el resultado en un archivo CSV
    local_filename = "cervezas_per_style.csv"

    # Guardar el resultado en un archivo CSV dentro del bucket de salida
    wr.s3.to_csv(df=response, path=f"{output_bucket}/{local_filename}", index=False)
    print(f"Consulta guardada en {output_bucket}/{local_filename}")

    return response


def sensaciones_top_estilos(session, output_bucket):
    """
    Función que calcula las sensaciones de los 15 estilos de cerveza mejor valorados

    Args:
        sesion: Sesión de boto3
        output_bucket: Bucket de salida
    Returns:
        Dataframe:  Respuesta de la consulta con las sensaciones de los estilos
    """
    query = """
    WITH top_styles AS (
    SELECT style
    FROM beer_db.beer
    GROUP BY style
    ORDER BY COUNT(*) DESC
    LIMIT 15
    )
    SELECT 
        b.style,
        COUNT(*) AS total_cervezas,
        AVG(astringency) AS avg_astringency,
        AVG(body) AS avg_body,
        AVG(alcohol) AS avg_alcohol,
        AVG(bitter) AS avg_bitter,
        AVG(sweet) AS avg_sweet,
        AVG(sour) AS avg_sour,
        AVG(salty) AS avg_salty,
        AVG(fruits) AS avg_fruits,
        AVG(hoppy) AS avg_hoppy,
        AVG(spices) AS avg_spices,
        AVG(malty) AS avg_malty
    FROM beer_db.beer b
    JOIN top_styles t ON b.style = t.style
    GROUP BY b.style
    ORDER BY total_cervezas DESC;    
    """
    df = wr.athena.read_sql_query(sql=query, database="beer_db", boto3_session=session)

    local_filename = "sensaciones_top_styles.csv"
    wr.s3.to_csv(df=df, path=f"{output_bucket}/{local_filename}", index=False)
    return df

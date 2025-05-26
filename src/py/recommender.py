"""
Módulo con funciones para el modelo de recomendación de cervezas. 
    Funciones:
        - **df_scale_data**: Escala los datos de las columnas sensoriales y de calificación.
        - **recomendar_hibrido**: Implementa un modelo Kmeans y KNN para recomendar cervezas similares.
        - **get_valid_image_url**: Obtiene una URL de imagen válida de un DataFrame.
"""

import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import requests


def df_scale_data(df):
    """
    Función para escalar los datos de las columnas sensoriales y de calificación.
    Se utiliza StandardScaler para normalizar los datos.

    Args:
        DataFrame: DataFrame con las columnas sensoriales y de calificación.
    Returns:
            DataFrame: DataFrame con los datos escalados.
            list: Lista de nombres de columnas sensoriales y de calificación.
    """
    # Selección de columnas sensoriales y de calificación

    feature_cols = [
        "abv",
        "astringency",
        "body",
        "alcohol",
        "bitter",
        "sweet",
        "sour",
        "salty",
        "fruits",
        "hoppy",
        "spices",
        "malty",
        "review_aroma",
        "review_appearance",
        "review_palate",
        "review_taste",
        "review_overall",
    ]

    # Subconjunto con esas columnas
    df_features = df[feature_cols]

    df_features_clean = df_features.apply(pd.to_numeric, errors="coerce")

    # Instanciar el escalador
    scaler = StandardScaler()

    # Ajustar y transformar los datos
    X_scaled = scaler.fit_transform(df_features_clean)

    # Convertir a DataFrame para conservar los nombres
    df_scaled = pd.DataFrame(X_scaled, columns=df_features_clean.columns)
    return df_scaled, feature_cols


def recomendar_hibrido(nombre_cerveza, df, df_scaled, feature_cols, df_img, top_n=5):

    """
    Función que implementa un modelo Kmeans y KNN para recomendar cervezas similares.

    Args:
        str: Nombre de la cerveza base para la recomendación.
        DataFrame: DataFrame con los datos de las cervezas.
        DataFrame: DataFrame con los datos escalados.
        list: Lista de nombres de columnas sensoriales y de calificación.
        DataFrame: DataFrame con las URLs de las imágenes de las cervezas.
        int: Número de recomendaciones a devolver.
    Returns:
        DataFrame: DataFrame con las cervezas recomendadas.
    """
    # Entrenar modelo final
    kmeans = KMeans(n_clusters=top_n, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(df_scaled)

    # Calcular promedios sensoriales por cluster
    df_clusters = pd.DataFrame(df_scaled, columns=feature_cols)
    df_clusters["cluster"] = df["cluster"]
    #
    df_scaled_df = pd.DataFrame(df_scaled, columns=feature_cols, index=df.index)
    # Buscar cerveza base
    base = df[df["name"].str.contains(nombre_cerveza, case=False)]
    # if base.empty:
    #    print("❌ No se encontró la cerveza.")
    #    return

    index_ref = base.index[0]
    cluster_id = base.loc[index_ref, "cluster"]

    # print(f"🍺 Cerveza base: {nombre}")
    # print(f"🧠 Cluster sensorial asignado: {cluster_id}\n")

    # Subconjunto del cluster
    cluster_df = df[df["cluster"] == cluster_id]
    cluster_scaled = df_scaled_df.loc[cluster_df.index]

    # Reentrenar KNN sobre ese cluster
    knn = NearestNeighbors(n_neighbors=top_n + 1, metric="cosine")
    knn.fit(cluster_scaled)

    # Encontrar posición relativa en cluster
    pos_in_cluster = list(cluster_df.index).index(index_ref)
    distances, indices = knn.kneighbors(cluster_scaled.iloc[[pos_in_cluster]])

    # Mostrar recomendaciones (excluyendo la base)
    df_beer_recom = pd.DataFrame(
        columns=["name", "style", "recommendation", "image_url"]
    )
    for i, idx in enumerate(indices[0][1:], 1):
        cerveza_idx = cluster_df.index[idx]
        rec_img_url = df_img.loc[
            df["name"] == df.loc[cerveza_idx, "name"], "image_url"
        ].values[0]
        df_beer_recom.loc[len(df_beer_recom)] = [
            df.loc[cerveza_idx, "name"],
            df.loc[cerveza_idx, "style"],
            1 - distances[0][i],
            rec_img_url,
        ]
        # print(f"{i}. {df.loc[cerveza_idx, 'name']}
        # ({df.loc[cerveza_idx, 'style']}) - Distancia: {distances[0][i]:.4f}")

    return df_beer_recom


def get_valid_image_url(df, url_column="image_url"):
    """
    Función que obtiene una URL de imagen válida de un DataFrame.
    
    Args:
        DataFrame: DataFrame que contiene las URLs de las imágenes.
        str: Nombre de la columna que contiene las URLs de las imágenes.

    Returns:
        str: URL de imagen válida o None si no se encuentra ninguna.
    """

    # Filter out empty entries
    valid_urls = df[df[url_column].notna()][url_column].tolist()

    if not valid_urls:
        return None  # No valid URLs found

    while valid_urls:
        # Randomly select a URL
        image_url = random.choice(valid_urls)

        try:
            # Check if the URL returns a valid image content type
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200 and "image" in response.headers.get(
                "Content-Type", ""
            ):
                return image_url  # Found a valid image

            # If the URL doesn't point to an image, remove it and retry
            valid_urls.remove(image_url)

        except requests.RequestException:
            valid_urls.remove(image_url)

    return None  # No valid image URLs found

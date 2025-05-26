"""
    Módulo  con funciones para cargar y procesar datos de cervezas y cervecerías.

    Funciones: 
        - **load_data**: Carga los datos de cervezas y cervecerías desde un archivo CSV en una URL pública.
        - **resize_image_to_height**: Descarga una imagen desde una URL y la redimensiona a la altura especificada, manteniendo la relación de aspecto.
"""
import pandas as pd
import requests
from PIL import Image
import requests
from io import BytesIO


def load_data():
    """
    Carga los datos de cervezas y cervecerías desde un archivo CSV en una URL pública.
    
    Args:
        None
     Returns:
        DataFrame: Datos de cervezas y cervecerías.  
        DataFrame: Nombres de cervezas, cervecerías y URLs de imágenes.
    """
    url = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_profile_and_ratings.csv"
    df = pd.read_csv(url)
    try:
        url_img = "https://itam-analytics-thmrudolf.s3.us-east-1.amazonaws.com/final_project/clean/beer_names_breweries_with_images.csv"
        df_img = pd.read_csv(url_img)
    except Exception as e:
        print("Access to S3 not available:", e)
        url_img = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_names_breweries_with_images.csv"
        df_img = pd.read_csv(url_img)
    return df, df_img

def resize_image_to_height(url, target_height):
    """
    Descarga una imagen desde una URL y la redimensiona a la altura especificada, manteniendo la relación de aspecto.

    Args:
        str: URL de la imagen a descargar.
        int: Altura deseada (en píxeles) para la imagen redimensionada.
    Returns:
        PIL.Image.Image: La imagen redimensionada como un objeto PIL Image.
  
    """
    # Load image from URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # Calculate new width to preserve aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    
    # Resize
    resized_img = img.resize((new_width, target_height))
    return resized_img


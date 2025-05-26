"""
Módulo de limpieza/transformación de datos
Funciones: 
    - **clean_text**: Limpia un texto aplicando transformaciones.
    - **clean_dataframe**: Limpia un DataFrame aplicando transformaciones celda por celda.
    - **process_csv_files**: Procesa todos los archivos CSV en un directorio, aplicando limpieza y guardando resultados.
"""

import re
import pandas as pd


# Diccionario de reemplazo de caracteres con tilde u otros
REPLACEMENTS = {
    r"[áàäâãå]": "a",
    r"[éèëê]": "e",
    r"[íìïî]": "i",
    r"[óòöôõö]": "o",
    r"[úùüû]": "u",
    r"[ç]": "c",
    r"[ñ]": "n",
    r"[žźż]": "z",
}


def clean_text(text):
    """
    Aplica limpieza a una celda de texto.

    - Convierte a minúsculas.
    
    - Reemplaza comas por punto y coma.
    
    - Reemplaza caracteres acentuados por su versión sin acento.
    
        Args:
            srt: Texto a limpiar.
        Returns:
            str: Texto limpio.
    """
    if not isinstance(text, str):
        return text  # No procesar valores no textuales

    # Convierte a minúsuculas
    text = text.lower()

    # Reemplaza comas por punto y coma
    text = text.replace(",", ";")

    # Reemplaza acentos en varios idiomas.
    for pattern, replacement in REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
    return text


def clean_dataframe(df):
    """
    Limpia todo un DataFrame aplicando transformaciones celda por celda.

        Args:
            Dataframe: Datos originales.
        Returns:
            Dataframe: Textos Limpios.
    """
    df_clean = df.map(clean_text)
    return df_clean


def renombrar_columnas(df):
    """
    Renombra las columnas de un DataFrame.

        Args:
            Dataframe: Datos originales.
        Returns:
            DataFrame: Columnas renombradas.
    """
    # Renombrar las columnas del DataFrame a minúsculas y con guiones bajos
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df


def process_csv_files(input_dir, output_dir):
    """
    Procesa todos los archivos CSV del directorio de entrada.

        Args:
            (Path): Directorio de entrada con archivos CSV.
            
            (Path): Directorio de salida para archivos CSV procesados.
        Returns:
            None: Los archivos CSV procesados se guardan en el directorio de salida.
    """
    # Crear el directorio de salida si no existe
    output_dir.mkdir(parents=True, exist_ok=True)

    # Procesar cada archivo CSV en el directorio de entrada
    for input_file in input_dir.glob("*.csv"):
        output_file = output_dir / input_file.name
        try:
            df = pd.read_csv(input_file)
            df = renombrar_columnas(df)
            cleaned_df = clean_dataframe(df)
            cleaned_df.to_csv(output_file, index=False)
            print(f"✅ Procesado: {input_file} → {output_file}")
        except Exception as e:
            print(f"❌ Error procesando {input_file}: {e}")

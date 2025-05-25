"""Modulo para cargar los datos a un buckect de S3
Funciones:
    1.- **load_data**: Carga los datos desde un bucket de S3
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from botocore.exceptions import ClientError


def load_data(s3):
    """
    Función que carga los datos desde un bucket de S3

     Args:
        boto3.client: Cliente de S3 para interactuar con el servicio
    Returns:
        bool: Indicador booleano de éxito o fracaso de la carga de datos.
    """

    try:
        # load environment variables
        load_dotenv()
        # Define bucket name
        BUCKET_NAME = os.getenv("BUCKET_NAME")

        # Try to create bucket if it doesn't exist
        try:
            s3.create_bucket(Bucket=BUCKET_NAME)
            print(f"Created bucket: {BUCKET_NAME}")
        except ClientError as e:
            if e.response["Error"]["Code"] == "BucketAlreadyExists":
                print(f"Bucket {BUCKET_NAME} already exists")
            else:
                raise e
        # Get the root directory path
        root_dir = Path(__file__).parent.parent.parent
        raw_dir = root_dir / "data/raw"

        # 🧹 Eliminar archivos anteriores en 'beer/clean/'
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="beer/clean/")
        if "Contents" in response:
            for obj in response["Contents"]:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
        print("🧹 Archivos anteriores eliminados de 'beer/clean/'")

        # Define files to upload
        files_to_upload = {
            "beer_profile_and_ratings.csv": "beer/clean/beer_profile_and_ratings.csv"
        }
        # Upload each file
        for local_file, s3_key in files_to_upload.items():
            file_path = raw_dir / local_file
            if file_path.exists():
                try:
                    s3.upload_file(
                        Filename=str(file_path), Bucket=BUCKET_NAME, Key=s3_key
                    )
                    print(f"Archivo {local_file} subido a {s3_key}")
                except ClientError as e:
                    print(f"Error uploading {local_file}: {str(e)}")
            else:
                print(f"Warning: File {file_path} not found")

        return True

    except Exception as e:
        print(f"Error in load_data: {str(e)}")
        return False

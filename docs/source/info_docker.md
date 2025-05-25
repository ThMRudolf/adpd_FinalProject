# 🐳 Dockerfile para BrewSmart

Este contenedor ejecuta automáticamente:

1. `main.py` para cargar datos a S3.
2. `eda_ui.py` para hacer consultas y generar CSV.
3. `streamlit_ui.py` para mostrar la app web.

## 🔧 Pasos para usarlo

### 1. Construir la imagen

Ejecuta el siguiente comando en la terminal desde la raíz del proyecto:

```bash
docker build -t brewsmart .
```
Este comando construirá la imagen de Docker con el nombre `brewsmart`.


### 2. Ejecutar el contenedor
Antes de ejecutar el contenedor, asegúrate de tener tu configuración de AWS en orden. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables de entorno:
```
BUCKET_NAME=bucket_s3
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=your_aws_region
```
Luego hay que ejecutar el contenedor en varios pasos: :

    1. Procesamiento de datos, carga a S3 y generación de archivos para EDA: 
        ```bash
        docker run --rm --env-file .env brewsmart python main.py
        ````
    2. Visualización de EDA:  
        ```bash
        docker run -p 8501:8501 --env-file .env brewsmart streamlit run src/py/eda_ui.py
        ```
        Abre tu navegador en [http://localhost:8501](http://localhost:8501) para visualizar los resultados del análisis exploratorio de datos (EDA).
    3. Recomendador de cervezas:
         ```bash
        docker run -p 8502:8501 --env-file .env brewsmart streamlit run src/py/streamlit_ui.py
        ```
        Ignora lo que aparezca en la terminal si te pide abrir el localhost:8501.
        Abre tu navegador en [http://localhost:8502](http://localhost:8502) para acceder a la aplicación de recomendación de cervezas.




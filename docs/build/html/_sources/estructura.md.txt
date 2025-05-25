# 📦 Estructura del Proyecto
```bash
.
├── data
│   ├── clean
│   │   ├── beer_names_breweries_with_images.csv
│   │   └── beer_profile_and_ratings.csv
│   ├── queries
│   │   ├── cervezas_per_brewery.csv
│   │   ├── cervezas_per_style.csv
│   │   └── sensaciones_top_estilos.csv
│   └── raw
│       └── beer_profile_and_ratings.csv
├── src
│   ├── bash
│   │   ├── clean_data_1.sh
│   │   └── clean_data.sh
│   ├── notebooks
│   │   ├── Beers_Final_Project.ipynb
│   │   ├── eda_models-1.ipynb
│   │   ├── eda.ipynb
│   │   ├── get_data.ipynb
│   │   ├── get_picture_links.ipynb
│   │   └── Limpieza.ipynb
│   └── py
│       ├── __pycache__
│       ├── athena_db.py
│       ├── eda_ui.py
│       ├── load.py
│       ├── recommender.py
│       ├── streamlit_ui.py
│       ├── transform.py
│       └── utils.py
├── environment.yml
├── main.py
└── tree

10 directories, 24 files
```

## NOTA: 
Los archivos `.csv` en las carpetas `data/clean` y `data/queries` se crean a partir de los archivos `.csv` en la carpeta `data/raw`. En el repositorio, los archivos `.csv` en la carpeta `data/raw` son los archivos originales extraídos de Kaggle. 

Para uso personal, se recomienda cargar los archivos propios en `data/raw` y ejecutar el script `main.py` para limpiar y transformar los datos.

## 🗒️ NOTEBOOKS :
Los notebooks de la carpeta `src/notebooks` son para uso personal y no se utilizan en el flujo de trabajo del proyecto. El archivo `Beers_Final_Project.ipynb` es un notebook diseñado para ejecutarlo bajo entorno de Spark. Hace la misma limpieza y análisis de datos que el script `main.py`, pero utilizando Spark.

Los notebooks  `Limpieza.ipynb`, `eda_models-1.ipynb` y  `eda.ipynb` son para limpieza, análisis exploratorio de datos y visualización, se hicieron a modo de prueba y no se utilizan en el flujo de trabajo del proyecto. 

Los notebooks `get_data.ipynb` y `get_picture_links.ipynb` son para obtener los datos de Kaggle y las imágenes de las cervezas, respectivamente. Estos notebooks no se utilizan en el flujo de trabajo del proyecto, pero pueden ser útiles para obtener datos adicionales o imágenes de cervezas.
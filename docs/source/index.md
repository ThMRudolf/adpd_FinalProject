# Documentación del Recomendador de Cervezas BrewSmart 🍺

Este documento contiene la documentación necesaria para entender y utilizar el sistema de recomendación de cervezas BrewSmart. El sistema está diseñado para ayudar a los usuarios a encontrar cervezas que se adapten a sus preferencias y gustos personales.

## 📕 Descripción del Proyecto 
El sistema de recomendación de cervezas BrewSmart utiliza técnicas de aprendizaje automático y análisis de datos para proporcionar recomendaciones personalizadas a los usuarios. 

El sistema se basa en un conjunto de datos que contiene información sobre diferentes cervezas, incluyendo sus características, sabores y preferencias de los usuarios. 

En esta primera versión, se utiliza el conjunto de datos de Kaggle [Beer_Profile_and_Ratings](https://www.kaggle.com/datasets/aklil/beer-profile-and-ratings) para entrenar el modelo de recomendación.

En versiones futuras, productivas, el conjunto de datos se sustituirá por datos propios de BrewSmart, que incluirán información sobre las cervezas en inventario y las preferencias de los usuarios.

Se presentan dos apps de Streamlit al usuario: 

1. 📊📈 **Análisis del Inventario**: Permite al usuario analizar su inventario por cervecería y estilos. Además, esta herramienta permite comparar las características fundamentales de sabor de diferentes cervezas en inventario. 
   
2.🍺🍺 **Recomendador de Cervezas**: Permite al usuario encontrar cervezas que se adapten a sus preferencias y gustos personales. El sistema utiliza un modelo de recomendación basado en el contenido y un modelo de filtrado colaborativo para proporcionar recomendaciones personalizadas.

## 📚 Uso del proyecto
Para utilizar el sistema de recomendación de cervezas BrewSmart, sigue estos pasos:

1.  **Instalación**: Ejecuta el ambiente que acompaña el proyecto: 
   ```
   conda env create -f environment.yml
   conda activate cerveza
   ```
2. **Sesión AWS**: Asegúrate de tener tu configuración de AWS en orden. 
   Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables de entorno:
   ```
   BUCKET_NAME=bucket_s3
   ```
3. **Preparación de datos**: Ejecuta el script de preparación de datos para limpiar y transformar los datos, para luego ser utilizados tanto por la app de análisis como el recomendador. 
   ```
   python main.py
   ```
4. **Ejecuta la app de análisis**: Ejecuta el script de la app de análisis para analizar tu inventario de cervezas.
   ```
   streamlit run src/py/eda_ui.py
   ```
5. **Ejecuta la app de recomendación**: Ejecuta el script de la app de recomendación para encontrar cervezas que se adapten a tus preferencias. 
   ```
   streamlit run src/py/streamlit_ui.py
   ```


```{toctree}
:maxdepth: 2
:caption: Contenido:
index
estructura
info_docker
modulos

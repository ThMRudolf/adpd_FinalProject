# Dockerfile
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    seaborn \
    streamlit \
    boto3 \
    python-dotenv \
    awswrangler \
    plotly \
    requests

# Copiar todo el proyecto
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# Valor por defecto si no se pasa comando: corre streamlit_ui
CMD ["streamlit", "run", "src/py/streamlit_ui.py"]

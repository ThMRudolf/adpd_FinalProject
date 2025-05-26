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

# Comando que corre todo en orden
ENTRYPOINT [ "bash", "-c", "\
    python main.py && \
    python src/py/eda_ui.py && \
    streamlit run src/py/streamlit_ui.py" ]

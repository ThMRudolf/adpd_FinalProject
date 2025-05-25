# 🐳 Dockerfile para BrewSmart

Este contenedor ejecuta automáticamente:

1. `main.py` para cargar datos a S3.
2. `eda_ui.py` para hacer consultas y generar CSV.
3. `streamlit_ui.py` para mostrar la app web.

## 🔧 Pasos para usarlo

### 1. Construir la imagen

```bash
docker build -t brewsmart .
```

### 2. Ejecutar el contenedor

```bash
docker run -p 8501:8501 brewsmart
```
Abre tu navegador en [http://localhost:8501](http://localhost:8501) para comenzar.


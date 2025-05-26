"""
Módulo principal de la aplicación de StreamLit 
para mostrar un análisis exploratorio de datos (EDA) 
hecho a partir de consultas SQL a una base de datos 
alojada en S3 y consultada a través de AWS Athena.

Este módulo carga los datos procesados y permite 
al usuario seleccionar diferentes vistas para 
explorar los datos de cervezas, cervecerías y estilos.

Visualizaciones: 

    - Gráfico de barras de las cervecerías con más cervezas.

    - Gráfico de barras de los estilos de cerveza más comunes.

    - Gráfico de barras comparativo de sensaciones entre 
    diferentes estilos de cerveza.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    """
    Carga los datos de cervezas, cervecerías y estilos desde archivos CSV.

    Returns:
        tuple: DataFrames con datos de cervezas por cervecería, por estilo y sensaciones.
    """
    df_brewery = pd.read_csv("../../data/queries/cervezas_per_brewery.csv")
    df_style = pd.read_csv("../../data/queries/cervezas_per_style.csv")
    df_sensaciones = pd.read_csv("../../data/queries/sensaciones_top_estilos.csv")
    return df_brewery, df_style, df_sensaciones


def vista_brewery(df):
    """
    Visualiza un gráfico de barras con la cantidad de cervezas por cervecería.

        Args:
            DataFrame: Datos de cervezas por cervecería.
    """
    st.header("🍺 Cervezas por Cervecería")
    top_n = st.slider("¿Cuántas cervecerías mostrar?", 5, 30, 10)
    top_breweries = df.sort_values("cervezas", ascending=False).head(top_n)
    fig = px.bar(top_breweries, x="brewery", y="cervezas", title="Top Cervecerías")
    st.plotly_chart(fig)


def vista_estilo(df):
    """
    Visualiza un gráfico de barras con la cantidad de cervezas por estilo.

        Args:
            DataFrame : Datos de cervezas por estilo.
    """
    st.header("🍻 Cervezas por Estilo")
    top_n = st.slider("¿Cuántos estilos mostrar?", 5, 30, 10)
    top_styles = df.sort_values("cervezas", ascending=False).head(top_n)
    fig = px.bar(top_styles, x="style", y="cervezas", title="Top Estilos")
    st.plotly_chart(fig)


def vista_sensaciones(df):
    """
    Visualiza sensaciones principales por estilo de cerveza.

        Args:
            DataFrame: Datos de sensaciones por estilo.
    """
    st.header("🎯 Sensaciones por Estilo")
    fig = px.bar(df, x="estilo", y="valor", color="atributo", barmode="group", title="Sensaciones por Estilo")
    st.plotly_chart(fig)


def main():
    """
        Función principal que ejecuta la aplicación Streamlit.
    """ 
    df_brewery, df_style, df_sensaciones = load_data()

    st.sidebar.title("📊 Navegación")
    section = st.sidebar.radio(
        "Selecciona vista:",
        ["Cervezas por Cervecería", "Cervezas por Estilo", "Sensaciones por Estilo"],
    )

    if section == "Cervezas por Cervecería":
        vista_brewery(df_brewery)
    elif section == "Cervezas por Estilo":
        vista_estilo(df_style)
    else:
        vista_sensaciones(df_sensaciones)


if __name__ == "__main__":
    main()

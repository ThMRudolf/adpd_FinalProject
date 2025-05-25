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
import os
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
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/queries"))
    df_brewery = pd.read_csv(os.path.join(BASE_PATH, "cervezas_per_brewery.csv"))
    df_style = pd.read_csv(os.path.join(BASE_PATH, "cervezas_per_style.csv"))
    df_sensaciones = pd.read_csv(os.path.join(BASE_PATH, "sensaciones_top_estilos.csv"))
    return df_brewery, df_style, df_sensaciones


def vista_brewery(df):
    """
    Visualiza un gráfico de barras con la cantidad de cervezas por cervecería.

        Args:
            DataFrame: Datos de cervezas por cervecería.
    """
    st.header("🍺 Cervezas por Cervecería")
    top_n = st.slider("¿Cuántas cervecerías mostrar?", 5, 50, 10)
    df_plot = df.sort_values("beer_count", ascending=False).head(top_n)
    fig = px.bar(
        df_plot,
        x="beer_count",
        y="brewery",
        orientation="h",
        title=f"Top {top_n} Cervecerías con más cervezas",
        labels={"beer_count": "Cantidad de Cervezas", "brewery": "Cervecería"},
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


def vista_estilo(df):
    """
    Visualiza un gráfico de barras con la cantidad de cervezas por estilo.

        Args:
            DataFrame : Datos de cervezas por estilo.
    """
    st.header("🍻 Cervezas por Estilo")
    top_n = st.slider("¿Cuántos estilos mostrar?", 5, 50, 10)
    df_plot = df.sort_values("beer_count", ascending=False).head(top_n)
    fig = px.bar(
        df_plot,
        x="beer_count",
        y="style",
        orientation="h",
        title=f"Top {top_n} Estilos de Cerveza más comunes",
        labels={"beer_count": "Cantidad de Cervezas", "style": "Estilo"},
        height=600,
    )
    st.plotly_chart(fig, use_container_width=True)


def vista_sensaciones(df):
    """
    Visualiza sensaciones principales por estilo de cerveza.

        Args:
            DataFrame: Datos de sensaciones por estilo.
    """
    st.header("🧬 Comparar Sensaciones entre Estilos")

    # Lista de sensaciones disponibles
    sensaciones_disponibles = [
        "avg_astringency",
        "avg_body",
        "avg_alcohol",
        "avg_bitter",
        "avg_sweet",
        "avg_sour",
        "avg_salty",
        "avg_fruits",
        "avg_hoppy",
        "avg_spices",
        "avg_malty",
    ]

    nombres_amigables = {
        "avg_astringency": "Astringencia",
        "avg_body": "Cuerpo",
        "avg_alcohol": "Alcohol",
        "avg_bitter": "Amargor",
        "avg_sweet": "Dulzor",
        "avg_sour": "Acidez",
        "avg_salty": "Salinidad",
        "avg_fruits": "Frutal",
        "avg_hoppy": "Lupulado",
        "avg_spices": "Especiado",
        "avg_malty": "Maltosidad",
    }

    estilos = df["style"].unique().tolist()

    # Selección de estilos (hasta 5)
    estilos_sel = st.multiselect(
        "Selecciona hasta 5 estilos para comparar",
        options=estilos,
        default=estilos[:3],
        max_selections=5,
    )

    # Selección de sensaciones (mínimo 3)
    sens_sel = st.multiselect(
        "Selecciona las sensaciones a comparar (mínimo 3)",
        options=sensaciones_disponibles,
        default=["avg_alcohol", "avg_bitter", "avg_malty"],
        format_func=lambda x: nombres_amigables[x],
    )

    if len(estilos_sel) >= 1 and len(sens_sel) >= 3:
        df_filtered = df[df["style"].isin(estilos_sel)]

        # Reorganizar para plotly
        df_plot = df_filtered.melt(
            id_vars="style",
            value_vars=sens_sel,
            var_name="sensacion",
            value_name="valor",
        )
        df_plot["sensacion"] = df_plot["sensacion"].map(nombres_amigables)

        fig = px.bar(
            df_plot,
            x="sensacion",
            y="valor",
            color="style",
            barmode="group",
            labels={"valor": "Valor Promedio", "sensacion": "Sensación"},
            title="Comparación de Sensaciones entre Estilos Seleccionados",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecciona al menos 1 estilo y 3 sensaciones.")



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

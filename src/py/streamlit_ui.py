"""
    Módulo para interfaz de usuario de Streamlit para la recomendación de cervezas.

    Este módulo utiliza la biblioteca Streamlit para crear una interfaz web interactiva
    que permite a los usuarios seleccionar su cerveza favorita y recibir recomendaciones
    basadas en sus preferencias.
"""

import streamlit as st
import pandas as pd
from recommender import df_scale_data, recomendar_hibrido, get_valid_image_url
from utils import load_data, resize_image_to_height


def main():
    """
        Función principal que ejecuta la aplicación Streamlit.

        La aplicación muestra una interfaz para que los usuarios seleccionen su estilo de cerveza
        favorito y proporcionen información adicional sobre sus preferencias. Luego, se generan
        recomendaciones de cervezas basadas en la entrada del usuario.
    """
    df, df_img = load_data()
    colH1, colH2 = st.columns(2)

    with colH1:
        st.image(
            "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/thomas/data/images/beer.png"
        )
    with colH2:
        st.header("BREWSMART")
    st.header("BEER RECOMMENDATIONS")
    st.subheader("We are here to help you find your favorite beer!")

    df_scaled, feature_cols = df_scale_data(df)
    unique_beer_type = df["name"].unique()

    st.subheader("Select your favourite beer style:")
    selected_product = st.selectbox("Beer Style:", unique_beer_type, index=0, label_visibility="hidden")

    st.subheader("Tell us a little bit more!")

    stages = ["Low", "Medium", "High"]

    col_def11, col_def12 = st.columns(2)
    with col_def11:
        selected_mouthfeel = st.select_slider("Mouthfeel:", options=stages)
    with col_def12:
        selected_taste = st.select_slider("Taste:", options=stages)

    col_def21, col_def22 = st.columns(2)
    with col_def21:
        selected_aroma = st.select_slider("Aroma:", options=stages)
    with col_def22:
        selected_flavor = st.select_slider("Flavor:", options=stages)

    df_recommendations = recomendar_hibrido(selected_product, df, df_scaled, feature_cols, df_img, top_n=3)

    default_IMAGE_URL = [get_valid_image_url(df_img) for _ in range(3)]
    IMAGE_COLUMN = "image_url"
    IMAGE_URL3 = [
        "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
    ] * 3

    RECOM_PERCENT = [0, 0, 0]
    if st.button("Find your beer..."):
        try:
            for i in range(3):
                RECOM_PERCENT[i] = df_recommendations["recommendation"].iloc[i] * 100
                img_url = df_recommendations[IMAGE_COLUMN].iloc[i]
                if pd.isna(img_url) or str(img_url).strip().lower() == "none":
                    IMAGE_URL3[i] = default_IMAGE_URL[i]
                elif get_valid_image_url(pd.DataFrame({IMAGE_COLUMN: [img_url]})) is not None:
                    IMAGE_URL3[i] = img_url
                else:
                    IMAGE_URL3[i] = default_IMAGE_URL[i]
        except ValueError:
            st.error("Ask for Water!")

    st.header("Our Recommendation")
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    for i, col in enumerate(columns):
        with col:
            st.markdown(
                f"<h1 style='text-align: center;'>{RECOM_PERCENT[i]:.2f}%</h1>",
                unsafe_allow_html=True,
            )
            name = df_recommendations["name"].iloc[i]
            style = df_recommendations["style"].iloc[i]
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<p style='font-size:24px; font-weight:bold;'>{name}</p>"
                f"<p style='font-size:20px; color:gray;'>{style}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
            IMAGE_URL3[i] = resize_image_to_height(IMAGE_URL3[i], target_height=300)
            st.image(IMAGE_URL3[i])

if __name__ == "__main__":
    main()

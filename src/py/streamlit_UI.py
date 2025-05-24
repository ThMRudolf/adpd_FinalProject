import streamlit as st
import pandas as pd
import random
from PIL import Image
import requests
from io import BytesIO
from recommender import df_scale_data,  recomendar_hibrido, get_valid_image_url
from utils import load_data, resize_image_to_height


df, df_img = load_data()
colH1, colH2 = st.columns(2)

## calling the model
df_scaled, feature_cols = df_scale_data(df)


# Extract unique values from the column
unique_beer_type = df['name'].unique()



## streamlit implementation
with colH1:
    st.image("https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/thomas/data/images/beer.png")
with colH2:
    st.header("BREWSMART")
st.subheader("BEER RECOMENDATIONS")
st.write("Tell us what you like: What is you favorite beer? ")




# Create a dropdown (popup-like) menu
selected_product = st.selectbox("Choose your favorite beer type", unique_beer_type)
# find the preferences
df_recommendations = recomendar_hibrido(selected_product, df, df_scaled, feature_cols, df_img, top_n=3)


# Define the stages
stages = ["Low", "Medium", "High"]

# oganize in columns for sliders
col_def11, col_def12, col_def13 = st.columns(3)

with col_def11:
    # Create the select slider
    selected_mouthfeel = st.select_slider(
        "Mouthfeel:",
        options=stages
    )

with col_def12:
    # Create the select slider
    selected_taste = st.select_slider(
        "Taste:",
        options=stages
    )

with col_def13:
    # Create the select slider
    selected_flavor = st.select_slider(
        "Flavor:",
        options=stages
    )


# Create the select slider
col_def21, col_def22, col_def23 = st.columns(3)
with col_def21:
    selected_aroma = st.select_slider(
        "Aroma:",
        options=stages
    )

#DEFAULT_IMAGE_URL = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
# select random picture form existing url for "none" fields
default_image_url = [None]*3
default_image_url[0] = get_valid_image_url(df_img)
default_image_url[1] = get_valid_image_url(df_img)
default_image_url[2] = get_valid_image_url(df_img)

IMAGE_COLUMN = "image_url"  # Replace with the name of your URL column
# Some input to evaluate
#user_input = st.text_input("Find you beer...")
# inicial values
recom_percentage_1 = 0
recom_percentage_2 = 0
recom_percentage_3 = 0

# Eval button
# start picture
image_url3 = [None]*3
image_url3[0] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url3[1] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url3[2] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url = None
recomenations = [0,1,2]
if st.button("Find your beer..."):
    try:
    # Generate a random percentage between 0 and 100
        recom_percentage_1 = df_recommendations["recommendation"].iloc[0]*100#round(random.uniform(0, 100), 2)
        recom_percentage_2 = df_recommendations["recommendation"].iloc[1]*100#round(random.uniform(0, 100), 2)
        recom_percentage_3 = df_recommendations["recommendation"].iloc[2]*100#round(random.uniform(0, 100), 2)
        counter = 0
        for idx in recomenations:#chosen_indices:
            image_url= df_recommendations["image_url"].iloc[idx]#df_img.loc[idx, IMAGE_COLUMN]
            #print(idx)
            #print(image_url)
            # Clean and check the image URL
            if pd.isna(image_url) or str(image_url).strip().lower() == "none":
                image_url3[counter] = default_image_url[counter]
            else:
                print(idx)
                # Check if the image URL is valid, else use default
                if get_valid_image_url(pd.DataFrame({IMAGE_COLUMN: [image_url]})) is not None:
                    image_url3[counter] = image_url
                else:
                    image_url3[counter] = default_image_url[counter]
            counter = counter+1
    except ValueError:
        st.error("Ask for Water!")



# results: plot the firt three options.
st.header("Your Recommandation")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <h1 style="text-align: center;">
            {recom_percentage_1:.2f}%
        </h1>
        """,
        unsafe_allow_html=True
    )
    name = df_recommendations["name"].iloc[0]
    style = df_recommendations["style"].iloc[0]

    st.markdown(f"""
        <div style="text-align: center;">
        <p style="font-size:24px; font-weight:bold;">{name}</p>
        <p style="font-size:20px; color:gray;">{style}</p>
        </div>
        """, unsafe_allow_html=True)

    #st.image("https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0")
    image_url3[0] = resize_image_to_height(image_url3[0], target_height=300)
    st.image(image_url3[0])#width=200,
with col2:
    st.markdown(
        f"""
        <h1 style="text-align: center;">
            {recom_percentage_2:.2f}%
        </h1>
        """,
        unsafe_allow_html=True
    )
    name = df_recommendations["name"].iloc[1]
    style = df_recommendations["style"].iloc[1]

    st.markdown(f"""
        <div style="text-align: center;">
        <p style="font-size:24px; font-weight:bold;">{name}</p>
        <p style="font-size:20px; color:gray;">{style}</p>
        </div>
        """, unsafe_allow_html=True)

    #st.image("https://i5.walmartimages.com.mx/gr/images/product-images/img_large/00750302099210L.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF")
    image_url3[1] = resize_image_to_height(image_url3[1], target_height=300)
    st.image(image_url3[1]) #width=200,
with col3:
    st.markdown(
        f"""
        <h1 style="text-align: center;">
            {recom_percentage_3:.2f}%
        </h1>
        """,
        unsafe_allow_html=True
    )
    name = df_recommendations["name"].iloc[2]
    style = df_recommendations["style"].iloc[2]

    st.markdown(f"""
        <div style="text-align: center;">
        <p style="font-size:24px; font-weight:bold;">{name}</p>
        <p style="font-size:20px; color:gray;">{style}</p>
        </div>
        """, unsafe_allow_html=True)

    #st.image("https://usercontent1.hubstatic.com/8154014_f520.jpg")
    image_url3[2] = resize_image_to_height(image_url3[2], target_height=300)
    st.image(image_url3[2]) #width=200,
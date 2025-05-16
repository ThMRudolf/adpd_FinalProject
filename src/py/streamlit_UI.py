import streamlit as st
import pandas as pd
import random


def load_data():
    url = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_profile_and_ratings.csv"
    df = pd.read_csv(url)
    return df 

df = load_data()
colH1, colH2 = st.columns(2)

with colH1:
    st.image("https://github.com/ThMRudolf/adpd_FinalProject/blob/thomas/data/images/beer.png")
with colH2:
    st.header("BREWSMART")
st.subheader("BEER RECOMENDATIONS")
st.write("Tell us what you like: What is you favorite beer? ")


# Extract unique values from the column
unique_beer_type = df['style'].unique()

# Create a dropdown (popup-like) menu
selected_product = st.selectbox("Choose your favorite beer type", unique_beer_type)


# Define the stages
stages = ["Low", "Medium", "High"]


col_def1, col_def2, col_def3 = st.columns(3)

with col_def1:
    # Create the select slider
    selected_mouthfeel = st.select_slider(
        "Mouthfeel:",
        options=stages
    )

with col_def2:
    # Create the select slider
    selected_taste = st.select_slider(
        "Taste:",
        options=stages
    )

with col_def3:
    # Create the select slider
    selected_flavor = st.select_slider(
        "Flavor:",
        options=stages
    )


# Create the select slider
selected_aroma = st.select_slider(
    "Aroma:",
    options=stages
)


# Some input to evaluate
#user_input = st.text_input("Find you beer...")
random_percentage_1 = 0
random_percentage_2 = 0
random_percentage_3 = 0
# Eval button
if st.button("Find your beer..."):
    try:
    # Generate a random percentage between 0 and 100
        random_percentage_1 = round(random.uniform(0, 100), 2)
        random_percentage_2 = round(random.uniform(0, 100), 2)
        random_percentage_3 = round(random.uniform(0, 100), 2)
    except ValueError:
        st.error("Ask Water!")




st.header("Your Recommandation")

col1, col2, col3 = st.columns(3)

with col1:
    st.header(f" {random_percentage_1}%")
    st.image("https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0")

with col2:
    st.header(f"{random_percentage_2}%")
    st.image("https://i5.walmartimages.com.mx/gr/images/product-images/img_large/00750302099210L.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF")

with col3:
    st.header(f"{random_percentage_3}%")
    st.image("https://usercontent1.hubstatic.com/8154014_f520.jpg")
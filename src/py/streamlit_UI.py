import streamlit as st
import pandas as pd
import random
from PIL import Image
import requests
from io import BytesIO


def load_data():
    url = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_profile_and_ratings.csv"
    df = pd.read_csv(url)
    url_img = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_names_breweries_with_images.csv"
    df_img = pd.read_csv(url_img)
    return df, df_img

def resize_image_to_height(url, target_height):
    # Load image from URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # Calculate new width to preserve aspect ratio
    width, height = img.size
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    
    # Resize
    resized_img = img.resize((new_width, target_height))
    return resized_img

df, df_img = load_data()
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

DEFAULT_IMAGE_URL = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
IMAGE_COLUMN = "image_url"  # Replace with the name of your URL column
# Some input to evaluate
#user_input = st.text_input("Find you beer...")
random_percentage_1 = 0
random_percentage_2 = 0
random_percentage_3 = 0

# Eval button
# jsut for ilustration purpose
valid_indices = df.index.intersection(range(0, 10))  # ensure safe range
chosen_indices = random.sample(list(valid_indices), 3)
image_url3 = [None]*3
image_url3[0] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url3[1] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url3[2] = "https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0"
image_url = None
if st.button("Find your beer..."):
    try:
    # Generate a random percentage between 0 and 100
        random_percentage_1 = round(random.uniform(0, 100), 2)
        random_percentage_2 = round(random.uniform(0, 100), 2)
        random_percentage_3 = round(random.uniform(0, 100), 2)
        counter = 0
        for idx in chosen_indices:
            image_url= df_img.loc[idx, IMAGE_COLUMN]
            print(idx)
            print(image_url)
            # Clean and check the image URL
            if pd.isna(image_url) or str(image_url).strip().lower() == "none":
                image_url3[counter] = DEFAULT_IMAGE_URL
            else:
                print(idx)
                image_url3[counter] = image_url
            counter = counter+1
    except ValueError:
        st.error("Ask Water!")




st.header("Your Recommandation")

col1, col2, col3 = st.columns(3)

with col1:
    st.header(f" {random_percentage_1}%")
    #st.image("https://cdn.dooca.store/674/products/4-altbier-1.png?v=1594668581&webp=0")
    image_url3[0] = resize_image_to_height(image_url3[0], target_height=300)
    st.image(image_url3[0])#width=200,
with col2:
    st.header(f"{random_percentage_2}%")
    #st.image("https://i5.walmartimages.com.mx/gr/images/product-images/img_large/00750302099210L.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF")
    image_url3[1] = resize_image_to_height(image_url3[1], target_height=300)
    st.image(image_url3[1]) #width=200,
with col3:
    st.header(f"{random_percentage_3}%")
    #st.image("https://usercontent1.hubstatic.com/8154014_f520.jpg")
    image_url3[2] = resize_image_to_height(image_url3[2], target_height=300)
    st.image(image_url3[2]) #width=200,
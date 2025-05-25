import pandas as pd
import requests
from PIL import Image
import requests
from io import BytesIO


def load_data():
    url = "https://raw.githubusercontent.com/ThMRudolf/adpd_FinalProject/refs/heads/thomas/data/clean/beer_profile_and_ratings.csv"
    df = pd.read_csv(url)
    try:
        url_img = "https://itam-analytics-thmrudolf.s3.us-east-1.amazonaws.com/final_project/clean/beer_names_breweries_with_images.csv"
        df_img = pd.read_csv(url_img)
    except except Exception as e:
        print("Access to S3:", e)
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

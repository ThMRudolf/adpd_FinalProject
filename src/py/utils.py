import pandas as pd
import requests
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
    """
    Downloads an image from a given URL and resizes it to the specified height while preserving the aspect ratio.
    Parameters
    ----------
    url : str
        The URL of the image to be downloaded and resized.
    target_height : int
        The desired height (in pixels) for the resized image.
    Returns
    -------
    PIL.Image.Image
        The resized image as a PIL Image object.
    Raises
    ------
    requests.exceptions.RequestException
        If there is an issue downloading the image from the URL.
    PIL.UnidentifiedImageError
        If the downloaded content is not a valid image.
    """
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

import requests
import pandas as pd
import boto3
from io import StringIO
import time
import json
#import s3fs


# === IMPORTS ===
def find_beer_image_url(beer_name, company_name, api_key, cx):
    search_query = f"{beer_name} {company_name} beer"
    params = {
        "q": search_query,
        "cx": cx,
        "key": api_key,
        "searchType": "image",
        "num": 5  # get up to 5 results to check file types
    }

    response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    response.raise_for_status()
    results = response.json()

    if "items" in results:
        for item in results["items"]:
            link = item.get("link", "")
            if link.lower().endswith((".jpg", ".jpeg", ".png")):
                return link
        return None  # No suitable image found
    else:
        return None


def add_image_url_column_if_not_exists(db_beers_names_breweries,
                                       api_key, cx,
                                       s3, S3_BUCKET, S3_KEY):
    save_interval = 100  # Save every 100 new image URLs
    found_count = 0      # Counter for how many new image URLs have been found
    for i in range(len(db_beers_names_breweries)):
        beer_name = db_beers_names_breweries.iloc[i]["name"]
        company_name = db_beers_names_breweries.iloc[i]["brewery"]
        print(f"Beer: {beer_name}, Brewery: {company_name}")
        try:
            # Check if "image_url" column exists and the ith value is empty or "None"
            if "image_url" in db_beers_names_breweries.columns and (
                pd.isna(db_beers_names_breweries.at[i, "image_url"]) or
                str(db_beers_names_breweries.at[i, "image_url"]).lower() in ["none", "nan", ""]
            ):
                image_url = find_beer_image_url(beer_name, company_name, api_key, cx)
                print("Image URL:", image_url)
                db_beers_names_breweries.at[i, "image_url"] = image_url
                found_count += 1
                # Save to CSV every 100 new findings
                if found_count % save_interval == 0:
                    filename = f"data/beer_images_partial_{found_count}.csv"
                    db_beers_names_breweries.to_csv(filename, index=False)
                    print(f"Saved intermediate results to {filename}")
                time.sleep(1.5)  # delay between requests
            else:
                print(f"Skipping row {i}, image_url already exists:")
                print(f"{db_beers_names_breweries.at[i, 'image_url']}")
        except Exception as e:
            print(f"Error at row {i}: {e}")
            db_beers_names_breweries.at[i, "image_url"] = None
            # Save the current state of the dataframe
            db_beers_names_breweries.to_csv("data/beer_names_breweries_with_images.csv", index=False)
            # Fill the rest with "none" and break the loop
            db_beers_names_breweries.loc[i+1:, "image_url"] = "none"
            break

    all_records = db_beers_names_breweries.to_dict(orient="records")

    # === SAVE TO S3 ===
    print(f"Saving {len(all_records)} image URLs to S3...")

    df = pd.DataFrame(all_records)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(Bucket=S3_BUCKET, Key=S3_KEY, Body=csv_buffer.getvalue())
    print(f"Done! Saved to s3://{S3_BUCKET}/{S3_KEY}")

    return db_beers_names_breweries



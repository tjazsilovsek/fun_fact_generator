import requests
import os
import json


def get_image(query: str) -> str:
    # Set up the API endpoint URL
    url = "https://api.unsplash.com/search/photos"

    # Set up the query parameters
    params = {
        "query": query,
        "per_page": 1,
    }
    key = os.getenv("UNSPLASH_API_KEY")

    # Set up the API headers
    headers = {
        "Authorization": f"Client-ID {key}"
    }

    # Send the API request
    response = requests.get(url, headers=headers, params=params)

    # Parse the response JSON
    data = json.loads(response.text)

    # Get the first image URL from the response
    image_url = data["results"][0]["urls"]["raw"]

    # Download the image and save it to a file
    response = requests.get(image_url)

    if response.status_code != 200:
        print(f"Failed to download image {image_url}.")
        return None

    image_path = f"content/download/{query}.jpg"

    with open(image_path, "wb") as f:
        f.write(response.content)

    return image_path

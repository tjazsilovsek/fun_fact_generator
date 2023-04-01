import requests
import os


def get_random_image(query: str) -> str:
    key = os.getenv("UNSPLASH_API_KEY")
    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {key}"}
    params = {"query": query}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        json_response = response.json()
        return json_response["urls"]["regular"]
    else:
        print(f"Error getting random image: {response.status_code}")
        return None


def download_image(url: str, filename: str) -> None:
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Error downloading image: {response.status_code}")

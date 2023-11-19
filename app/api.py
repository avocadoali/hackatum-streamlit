from dotenv import load_dotenv
import os
import requests

# get apikey
load_dotenv()
api_key = os.getenv("API_KEY")
api_url = 'https://api.synclabs.so/video'

def post_video(audio_url, video_url):
    payload = {
        "audioUrl": audio_url,
        "videoUrl": video_url,
        "synergize": True,
        "maxCredits": None,
        "webhookUrl": None
    }
    # Headers
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json',
    }

    # Make the POST request
    response = requests.post(api_url, json=payload, headers=headers)
    # Display the response
    print(f"Response code: {response.status_code}")
    print("Response:", response.json())

    return response.json()

def get_video(video_id):
    url = f"https://api.synclabs.so/video/" + video_id
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    response = requests.get(url, headers=headers)

    # Display the response
    print(f"Response code: {response.status_code}")

    if response.status_code == 200:
        return response.json()
    else:
        return None


def download_video(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
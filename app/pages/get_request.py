from dotenv import load_dotenv
import os
import streamlit as st
import requests
import urllib
from tqdm import tqdm  # Added import for tqdm
import urllib.request


def read_env_file():
    load_dotenv()
    return os.getenv("API_KEY")

def make_api_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.RequestException as err:
        return f"Request Error: {err}"

def download_video(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")






# Streamlit app
st.title("SyncLabs API Request Example")
pwd = os.getcwd()
st.write(pwd)

# Input fields
url = st.text_input("Enter API URL:", 'https://api.synclabs.so/video/f38c6133-0c9a-4857-ab0a-dc1c4663cb45')
api_key = read_env_file()

# Make the API request when the user clicks the button
if st.button("Make API Request"):
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key
    }
    
    result = make_api_request(url, headers)
    
    # Display the result
    st.header("API Response:")
    st.json(result)

    # Download video button
    if 'url' in result:
        video_url = result['url']
        st.write(video_url)
        download_video(video_url, "./app/static/download.mp4")
    
    st.write("Your video")
    # File path to your MP4 video
    video_path = "./app/static/download.mp4"

    # Display the video
    st.video(video_path)




from dotenv import load_dotenv
import os
import streamlit as st
import requests
import time


def post(audio_url, vide_url):
    payload = {
        "audioUrl": audio_url,
        "videoUrl": video_url,
        "synergize": False,
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
    print(f"Status Code: {response.status_code}")
    print("Response:")

    return response.json()

def fetch_video_data(video_id):
    url = f"https://api.synclabs.so/video/"+ video_id
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    response = requests.get(url, headers=headers)

    # Display the response
    print(f"Status Code: {response.status_code}")
    print("Response:")

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

def show_video(video_path):
    # File path to your MP4 video
    st.video(video_path)

def run_process(audio_url, video_url, destination_path):
    # Upload audio and video file
    
    print("start uploading")
    response = post(audio_url, video_url)
    print(response)
    video_id = response["id"]
    print("video id: " + video_id)

    print("Curren status")
    # Fetch status of process
    fetch_response = fetch_video_data(video_id)
    print(fetch_response)
    while fetch_response["status"] != "COMPLETED":
        fetch_response = fetch_video_data(video_id)
        print(fetch_response) 
        time.sleep(2)
    
    print("Downloading file")
    # Download video
    deepfake_video_url = fetch_response["url"]
    deepfake_video_url
    download_video(deepfake_video_url, destination_path)
    video_path= destination_path
    print("Fiel is in: " + video_path)

    show_video(video_path)



# get apikey
load_dotenv()
api_key = os.getenv("API_KEY")
api_url = 'https://api.synclabs.so/video'

# Title
st.title("Video and Audio File Uploader")

# Default file URLs
default_audio_url = "https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3"
default_video_url = "https://playful-froyo-95db49.netlify.app/susanne.mp4"

# Upload audio file
audio_file = st.file_uploader("Upload Audio File (MP3)", type=["mp3"], key="audio")
audio_url = st.text_input("Or use Default Audio URL", default_audio_url)

# Upload video file
video_file = st.file_uploader("Upload Video File (MP4)", type=["mp4"], key="video")
video_url = st.text_input("Or use Default Video URL", default_video_url)

# Destination path
destination_path = st.text_input("Destination Path", "./app/static/finaloutput/susanne_autogen.mp4")

# Display uploaded file details
if audio_file is not None:
    st.audio(audio_file, format="audio/mp3", start_time=0)
    st.markdown(f"Audio File: {audio_file.name}")
else:
    st.audio(audio_url, format="audio/mp3", start_time=0)

if video_file is not None:
    st.video(video_file, format="video/mp4", start_time=0)
    st.markdown(f"Video File: {video_file.name}")
else:
    st.video(video_url, format="video/mp4", start_time=0)

# Button to process files
if st.button("Process Files"):
    if (audio_file is not None or audio_url) and (video_file is not None or video_url):
        # Perform processing here using the uploaded files or default URLs and destination path
        st.success(f"Files processed and saved to {destination_path}")
        run_process(audio_url, video_url, destination_path)

    else:
        st.warning("Please upload audio and/or video files or provide default URLs before processing.")


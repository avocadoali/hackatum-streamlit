from dotenv import load_dotenv
import streamlit as st
import os
import requests
import time


def download_video(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Download video
st.title("Downlaod video")
path_to_generated_video = "./app/static/finaloutput/susanne_trump.mp4"
deepfake_video_url = "https://synchlabs-public.s3.amazonaws.com//tmp/5b9ba706-58a8-4512-a750-7c3ffeccbdb6_result.mp4"

if st.button("Download the video"):
    download_video(deepfake_video_url, path_to_generated_video)

    # Display the video
    st.write("Your video")
    video_path= "./app/static/finaloutput/susanne_trump.mp4"
    st.video(video_path)

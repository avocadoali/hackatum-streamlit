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

def run_processs(audio_url, video_url, destination_path):
    # Upload audio and video file
    
    print("start uploading")
    response = post(audio_url, video_url)
    print(response)
    video_id = response["id"]
    print("video id: " + video_id)

    start_time = time.time()

    print("Current status")
    # Fetch status of process
    fetch_response = fetch_video_data(video_id)
    print(fetch_response)
    while fetch_response["status"] != "COMPLETED":
        fetch_response = fetch_video_data(video_id)
        print(fetch_response) 
        time.sleep(2)
    
    # Record end time
    end_time = time.time()
    
    # Calculate and print elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    

    print("Downloading file")
    # Download video
    deepfake_video_url = fetch_response["url"]
    deepfake_video_url
    download_video(deepfake_video_url, destination_path)
    video_path= destination_path
    print("Fiel is in: " + video_path)

    show_video(video_path)

def run_process(audio_url, video_url, destination_path):
    st.write(video_url)
    st.write(audio_url)
    # Upload audio and video file
    with st.spinner("Uploading..."):
        response = post(audio_url, video_url)
        st.success("Upload completed")
        video_id = response["id"]
        st.info("Video ID: " + video_id)

    with st.spinner("Checking current status..."):
        # Fetch status of the process
        fetch_response = fetch_video_data(video_id)
        while fetch_response["status"] != "COMPLETED":
            fetch_response = fetch_video_data(video_id)
        st.success("Status check completed")
        st.info(fetch_response)
        
    with st.spinner("Downloading file..."):
        # Download video
        deepfake_video_url = fetch_response["url"]
        download_video(deepfake_video_url, destination_path)
        st.success("Download completed")
        video_path = destination_path
        st.info("File is in: " + video_path)

        st.success("Process completed successfully")

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

def upload_file(upload_directory, typee, keyy):
    uploaded_file = st.file_uploader("Upload here:", type=[typee], key=keyy)
    if uploaded_file is not None:
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"File successfully uploaded to {file_path}")

# Upload audio file
st.subheader("Upload Audio File")
audio_file = upload_file("app/static/input/audio", "mp3", "audio")

audio_url = st.text_input("Or use Default Audio URL:", default_audio_url)

st.write("")
# Upload video file

st.subheader("Upload Video File")
video_file = upload_file("app/static/input/video", "mp4", "video")
video_url = st.text_input("Or use Default Video URL:", default_video_url)

st.write("")

st.subheader("Specify output filename")
# Destination path
p= st.text_input("Filename:", "output.mp4")
destination_path = "./app/static/finaloutput/" + p

st.write("")

st.subheader("Selected Files")

# Create two columns with st.columns
col2, col1 = st.columns(2)
with col1:
    # Display uploaded file details
    st.write("Audiofile:")
    if audio_file is not None:
        st.audio(audio_file, format="audio/mp3", start_time=0)
        st.markdown(f"Audio File: {audio_file.name}")
    else:
        st.audio(audio_url, format="audio/mp3", start_time=0)


with col2:
    st.write("Videofile:")

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


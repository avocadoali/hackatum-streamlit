import streamlit as st
import os
import time
from api import post_video, get_video, download_video

# Default file URLs
default_audio_url = "https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3"
default_video_url = "https://playful-froyo-95db49.netlify.app/susanne.mp4"

def show_video(video_path):
    # File path to your MP4 video
    st.video(video_path)

def run_process(audio_url, video_url, destination_path):
    st.info("Video: " + video_url)
    st.info("Audio: " + audio_url)

    # Upload audio and video file
    with st.spinner("Uploading..."):
        response = post_video(audio_url, video_url)
        st.success("Upload completed")
        video_id = response["id"]
        st.info("Video ID: " + video_id)

    with st.spinner("Checking current status..."):
        # Fetch status of the process
        fetch_response = get_video(video_id)
        while fetch_response["status"] != "COMPLETED":
            fetch_response = get_video(video_id)
            print("Status:", fetch_response['status'])
            time.sleep(2)
        st.success("Status check completed")
        st.info("Video URL: " + fetch_response['url'])
        
    with st.spinner("Downloading file..."):
        # Download video
        deepfake_video_url = fetch_response["url"]
        download_video(deepfake_video_url, destination_path)
        st.success("Download completed")
        video_path = destination_path
        st.info("File saved to: " + video_path)

        st.success("Process completed successfully")

    show_video(video_path)

def upload_file(upload_directory, typee, keyy):
    uploaded_file = st.file_uploader("Upload here:", type=[typee], key=keyy)
    if uploaded_file is not None:
        file_path = os.path.join(upload_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"File successfully uploaded to {file_path}")

def display_videos():
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

# Title
st.title("Video and Audio File Uploader")

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

st.subheader("Selected Files")
display_videos()

st.write("")

st.subheader("Generate a Video")
p = st.text_input("Output filename:", "output.mp4")
destination_path = "./app/static/finaloutput/" + p

# Button to process files
if st.button("Process Files"):
    if (audio_file is not None or audio_url) and (video_file is not None or video_url):
        # Perform processing here using the uploaded files or default URLs and destination path
        st.success(f"Files processed and saved to {destination_path}")
        run_process(audio_url, video_url, destination_path)

    else:
        st.warning("Please upload audio and/or video files or provide default URLs before processing.")


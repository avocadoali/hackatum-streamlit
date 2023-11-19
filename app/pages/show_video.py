import os
import streamlit as st

def video_gallery(directory_path):
    video_files = [f for f in os.listdir(directory_path) if f.endswith(('.mp4', '.avi', '.mkv', '.mov'))]
    
    for video_file in video_files:
        video_path = os.path.join(directory_path, video_file)
        st.video(video_path)

# Example usage
video_directory = "app/static/finaloutput"
st.title("Video Gallery")
video_gallery(video_directory)
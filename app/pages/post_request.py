import streamlit as st
import requests
from dotenv import load_dotenv
import os


def read_env_file():
    load_dotenv()
    return os.getenv("API_KEY")




# Streamlit app
st.title("SyncLabs API POST Request Example")

# Input fields
audio_url = st.text_input("Enter audio URL:", 'https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3')
video_url = st.text_input("Enter video URL:", "https://playful-froyo-95db49.netlify.app/susanne.mp4")
synergize = st.checkbox("Synergize", False)
max_credits = st.text_input("Enter max credits (or leave blank):")
webhook_url = st.text_input("Enter webhook URL (or leave blank):")

api_url = 'https://api.synclabs.so/video'
api_key = read_env_file()

# Make the API request when the user clicks the button
if st.button("Make API Request"):
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
        'Content-Type': 'application/json'

    }

    payload = {
        'audioUrl': audio_url,
        'videoUrl': video_url,
        'synergize': synergize,
        'maxCredits': max_credits if max_credits else None,
        'webhookUrl': webhook_url if webhook_url else None
    }

    response = requests.post(api_url, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content
        st.header("API Response:")
        st.json(response.json())
    else:
        # Print an error message
        st.error(f"Error: {response.status_code} - {response.text}")

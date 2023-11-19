from dotenv import load_dotenv
import os
import streamlit as st
import requests

load_dotenv()
api_key = os.getenv("API_KEY")

def post():
    st.title("SyncLabs Video API Request")

    # Input fields
    audio_url = st.text_input("Audio URL", "https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3")
    video_url = st.text_input("Video URL", "https://playful-froyo-95db49.netlify.app/susanne.mp4")
    synergize = st.checkbox("Synergize", True)

    # Make the request when the user clicks the button
    if st.button("Generate Video"):
        # API endpoint
        api_url = 'https://api.synclabs.so/video'

        # Request payload
        payload = {
            "audioUrl": audio_url,
            "videoUrl": video_url,
            "synergize": synergize,
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

        video_id = ""
        if 'id' in response:
            vide_id = responsegg["id"]

        # Display the response
        st.text(f"Status Code: {response.status_code}")
        st.text("Response:")
        st.json(response.json())

if __name__ == "__main__":
    main()





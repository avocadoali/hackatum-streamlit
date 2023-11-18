from dotenv import load_dotenv
import streamlit as st
import os
import requests
import time

load_dotenv()
api_key = os.getenv("API_KEY")

def download_video(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

    
def get_url_deepfake(url):
    # Request to generate the deepfake
    try:
        response = requests.get(
            url, 
            json = {
                'accept': 'application/json',
                'x-api-key': api_key,
            }
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.RequestException as err:
        return f"Request Error: {err}"

def generate_deepfake(url, video_url, audio_url):
    # Input fields
    synergize = st.checkbox("Synergize", True)

    # Make the request when the user clicks the button
    if st.button("Generate Video"):
        payload = {
            "audioUrl": audio_url,
            "videoUrl": video_url,
            "synergize": synergize,
            "maxCredits": None,
            "webhookUrl": None
        }

        headers = {
            'accept': 'application/json',
            'x-api-key': api_key,
            'Content-Type': 'application/json',
        }

        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)

        # Display the response
        st.text(f"Status Code: {response.status_code}")
        st.text("Response:")
        st.json(response.json())


# Streamlit app
st.title("Generate Deepfake")

# Post request
# Premade list on what to upload


# Generate deepfake
#url='https://api.synclabs.so/video'
#video_url= "https://playful-froyo-95db49.netlify.app/susanne.mp4",
#audio_url= "https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3",


st.title("SyncLabs Video API Request")
url = 'https://api.synclabs.so/video'

audio_url = st.text_input("Audio URL", "https://playful-froyo-95db49.netlify.app/trump_voice_2.mp3")
video_url = st.text_input("Video URL", "https://playful-froyo-95db49.netlify.app/susanne.mp4")

result = generate_deepfake(url, video_url, audio_url)

 

#if st.button("Make API Request"):
#    result = generate_deepfake(url, video_url, audio_url)
#    st.write(url)
#    st.write(api_key)
#    st.json(result)
#
## Get the id of the process
#id = " "
#print(result)
#if 'id' in result:
#    pass
#    #id = result.id
#
#deepfake_status_url= url  + id
#result = get_url_deepfake(deepfake_status_url)
#
#while result.status != "COMPLETED":
#    result = get_url_deepfake(url, path_to_generated_video)
#    time.sleep(2)

## Get id
#deepfake_video_url = ""
#if 'url' in result:
#    deepfake_video_url =  result['url']
#
## Download vide
#path_to_generated_video = "./app/static/finaloutput/susanne_trump.mp4"
#download_video(deepfake_video_url, path_to_generated_video)
#
#
## Display the video
#st.write("Your video")
#video_path= "./app/static/finaloutput/susanne_trump.mp4"
#st.video(video_path)



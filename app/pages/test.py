import streamlit as st
import requests

def fetch_video_data(api_key, video_id):
    url = f"https://api.synclabs.so/video/{video_id}"
    headers = {
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    st.title("SyncLabs Video Data Fetcher")

    st.sidebar.header("User Input")
    api_key = st.sidebar.text_input("Enter x-api-key", value="e2c31e17-a063-4e48-9b58-351946b9e88c")
    video_id = st.sidebar.text_input("Enter Video ID", value="5b9ba706-58a8-4512-a750-7c3ffeccbdb6")

    if st.sidebar.button("Fetch Video Data"):
        if api_key and video_id:
            st.info("Fetching video data...")
            video_data = fetch_video_data(api_key, video_id)

            if video_data:
                st.success("Video data fetched successfully!")
                st.json(video_data)
            else:
                st.error("Failed to fetch video data. Please check your x-api-key and Video ID.")
        else:
            st.warning("Please enter both x-api-key and Video ID.")


if __name__ == "__main__":
    main()
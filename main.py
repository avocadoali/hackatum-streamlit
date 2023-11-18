import requests

def download_mp4(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print("Download complete.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# Example usage:
#url = "https://synchlabs-public.s3.amazonaws.com//tmp/5f605bfe-8759-40fd-b132-9630f5f237f3_result.mp4"
url = "http://localhost:8501/app/static/download.mp4"
save_path = 'downloaded_video.mp4'
download_mp4(url, save_path)

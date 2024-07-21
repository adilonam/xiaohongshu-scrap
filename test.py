import requests

def download_video(url, file_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Video downloaded successfully: {file_name}")
    else:
        print("Failed to download video")

# Replace 'actual_video_url' with the real URL of the video
video_url = 'https://www.xiaohongshu.com/07afd315-94b6-4e3a-be43-c6874456f0ef'
download_video(video_url, 'downloaded_video.mp4')

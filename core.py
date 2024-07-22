import time
import requests
import re
import os

from stem import Signal
from stem.control import Controller
from selenium.webdriver.common.by import By

class XhsClient:
    def __init__(self, driver) -> None:
        self.driver = driver

    def download_note_id(self, note_id):
        url = f'https://www.xiaohongshu.com/explore/{note_id}'
        
        try:
            # Open the webpage
            self.driver.get(url)

            # Wait for the page to load completely
            # time.sleep(3)  # Adjust the sleep time as needed

            # Find the <script> element that contains video info
            script_element = self.driver.find_element(By.XPATH, '/html/body/script[3]')
            
            page_title = self.driver.title
            like_count = "None"

            # Define patterns to search for
            url_pattern = re.compile(r'http:\\u002F\\u002Fsns-video-bd\.xhscdn\.com[^"]*\.mp4')
            like_pattern = re.compile(r'"likedCount":"(.*?)"')
            
            script_content = script_element.get_attribute('innerHTML')
            if script_content:
                # Search for patterns in the script content
                url_match = url_pattern.search(script_content)
                like_match = like_pattern.search(script_content)
                
                if like_match:
                    like_count = like_match.group(1)
                    
                if url_match:
                    video_url = url_match.group().replace('\\u002F', '/')
                    
                    print(f"Found matching URL: {video_url} | Title: {page_title} | Likes: {like_count}")

                    # Configure requests to use Tor proxy
                    proxies = {
                        'http': 'socks5://localhost:9050',
                        'https': 'socks5://localhost:9050'
                    }

                    # Download video
                    response = requests.get(video_url, stream=True, proxies=proxies)

                    if response.status_code == 200:
                        # Get total file size from headers
                        total_size = int(response.headers.get('Content-Length', 0))
                        downloaded_size = 0

                        # Chunk size
                        chunk_size = 64 * 1024 * 2

                        # Save video to file
                        os.makedirs('./video', exist_ok=True)
                        video_path = f'./video/{note_id}.mp4'
                        with open(video_path, 'wb') as file:
                            for chunk in response.iter_content(chunk_size=chunk_size):
                                file.write(chunk)
                                downloaded_size += len(chunk)
                                # Print download progress
                                progress = (downloaded_size / total_size) * 100
                                print(f"Download progress: {progress:.2f}%")
                        
                        print('Download completed successfully.')
                        return {"title": page_title, "like": like_count, "path": video_path}
                    else:
                        print('Failed to download video. Status code:', response.status_code)
                        return None
                else:
                    print("No video URL found")
                    return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def renew_tor_ip(self):
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate(password='your_tor_password')  # Replace with your Tor password if set
                controller.signal(Signal.NEWNYM)
        except Exception as e:
            print(f"Failed to renew Tor IP: {e}")

    def get_note_ids(self, url):
        note_id_pattern = re.compile(r'"trackId":"(.*?)"')
        
        try:
            # Open the webpage
            self.driver.get(url)

            # Wait for the page to load completely
            # time.sleep(3)  # Adjust the sleep time as needed

            # Find the <script> element that contains note IDs
            script_element = self.driver.find_element(By.XPATH, '/html/body/script[3]')
            script_content = script_element.get_attribute('innerHTML')
            
            if script_content:
                # Search for note IDs in the script content
                note_ids = note_id_pattern.findall(script_content)
                print("Note IDs found:", note_ids)
                return note_ids
        except Exception as e:
            print(f"An error occurred: {e}")
        

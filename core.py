import json
import openpyxl
import requests
import re
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class XhsClient:
    def __init__(self) -> None:
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--incognito")

        # Launch the browser with the specified options
        driver = uc.Chrome(options=options)
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

                    

                    # Download video
                    response = requests.get(video_url, stream=True)

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
                        return {"note_id" : note_id , "title": page_title, "like": like_count, "path": video_path}
                    else:
                        print('Failed to download video. Status code:', response.status_code)
                        return None
                else:
                    print("No video URL found")
                    return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None


    def get_note_ids(self, url):
        note_id_pattern = re.compile(r'"type":"video".*?"trackId":"(.*?)"')
        
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
    
    def start(self, excel_path = "./excel/video_links.xlsx"):
        os.makedirs('./video', exist_ok=True)
        data_path = './video/data.json'
        # Check if the file exists
        if os.path.exists(data_path):
            # If it exists, read and parse the JSON data
            with open(data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            # If it doesn't exist, initialize data as an empty list
            data = []
        
        workbook = openpyxl.load_workbook(excel_path)

        # Get the active sheet
        sheet = workbook.active

        # Get the first column as an array
        first_column = []
        for cell in sheet['A']:
            first_column.append(cell.value)

        # Print the first column
        print(first_column)
        
        
        for url in first_column:
            note_id_pattern = re.compile(r'https://www\.xiaohongshu\.com/explore/([a-zA-Z0-9]+)')
            note_id_match = note_id_pattern.search(url)
            if note_id_match:
                note_id = note_id_match.group(1)
                video_data = self.download_note_id(note_id)
                if video_data:
                    data.append(video_data)
                    json_data = json.dumps(data, indent=2 , ensure_ascii=False)  # indent for pretty printing, optional
                    # Write to a file (will replace contents if file exists)
                    
                    with open(data_path, 'w', encoding='utf-8') as file:
                        file.write(json_data)
                print(f"video {note_id} added succesfly")
            

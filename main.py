from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import re

# Path to the ChromeDriver executable
chrome_driver_path = './driver/chromedriver'

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
chrome_options.add_argument('--incognito') 
# Initialize the WebDriver with the specified path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the webpage
    driver.get('https://www.xiaohongshu.com/explore/669539f6000000002500328f')

    # Wait for the page to load completely
    time.sleep(3)  # Adjust the sleep time as needed

    # Find all <script> elements
    script_elements = driver.find_elements(By.TAG_NAME, 'script')

    # Define the pattern to search for
    pattern = re.compile(r'http:\\u002F\\u002Fsns-video-bd\.xhscdn\.com[^"]*\.mp4')

    for script in script_elements:
        script_content = script.get_attribute('innerHTML')
        
        if script_content:
            # Search for the pattern in the script content
            matches = pattern.findall(script_content)
            if matches:
                match = matches[0].replace('\\u002F', '/')
                print(f"Found matching URL: {match}")
                
                # Send a GET request to the URL
                response = requests.get(match, stream=True)

                # Check if the request was successful
                if response.status_code == 200:
                    # Get total file size from headers
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded_size = 0

                    # Open a file to write the video content
                    with open('./video/video.mp4', 'wb') as file:
                        # Write the video content in chunks
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                            downloaded_size += len(chunk)
                            # Calculate and print the download progress
                            progress = (downloaded_size / total_size) * 100
                            print(f"Download progress: {progress:.2f}%")
                    
                    print('Download completed successfully.')
                else:
                    print('Failed to download video. Status code:', response.status_code)

finally:
    # Close the browser
    driver.quit()

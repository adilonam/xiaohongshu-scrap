from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import re
import os
from stem import Signal
from stem.control import Controller

# Path to the ChromeDriver executable
chrome_driver_path = './driver/chromedriver'

# Set up Chrome options to use Tor proxy
chrome_options = Options()
chrome_options.add_argument('--proxy-server=socks5://localhost:9050')  # Use Tor proxy

# Initialize the WebDriver with the specified path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to get a new Tor circuit
def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='your_tor_password')  # Replace with your Tor password if set
        controller.signal(Signal.NEWNYM)

try:
    # Open the webpage
    driver.get('https://www.xiaohongshu.com/explore/669539f6000000002500328f')

    # Wait for the page to load completely
    time.sleep(3)  # Adjust the sleep time as needed

    # Find all <script> elements
    script_element = driver.find_element(By.XPATH, '/html/body/script[3]')
    
    page_title = driver.title
    
    like_count = driver.title

    # Define the pattern to search for
    url_pattern = re.compile(r'http:\\u002F\\u002Fsns-video-bd\.xhscdn\.com[^"]*\.mp4')
    like_pattern = re.compile(r'"likedCount":"(.*?)"')

    
    script_content = script_element.get_attribute('innerHTML')
    if script_content:
        # Search for the pattern in the script content
        url_match = url_pattern.search(script_content)
        like_match = like_pattern.search(script_content)
        like_count = "None"
        print(like_match)
        if like_match:
            like_count = like_match.group(1)
        if url_match:
            match = url_match.group().replace('\\u002F', '/')
            
            print(f"Found matching URL: {match} title: {page_title} like: {like_count}")

            # Configure requests to use Tor proxy
            proxies = {
                'http': 'socks5://localhost:9050',
                'https': 'socks5://localhost:9050'
            }

            # Send a GET request to the URL
            response = requests.get(match, stream=True, proxies=proxies)

            # Check if the request was successful
            if response.status_code == 200:
                # Get total file size from headers
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded_size = 0

                # Increase chunk size to 64KB
                chunk_size = 64 * 1024 * 2 # 64KB

                # Open a file to write the video content
                os.makedirs('./video', exist_ok=True)
                with open('./video/video.mp4', 'wb') as file:
                    # Write the video content in chunks
                    for chunk in response.iter_content(chunk_size=chunk_size):
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

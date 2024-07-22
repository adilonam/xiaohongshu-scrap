import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from core import XhsClient
from selenium.webdriver.common.by import By





if __name__ == "__main__":
    # Path to the ChromeDriver executable
    chrome_driver_path = './driver/chromedriver'

    # Set up Chrome options to use Tor proxy
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=socks5://localhost:9050')  # Use Tor proxy

    # Initialize the WebDriver with the specified path
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    xhs_client = XhsClient(driver)
    
    
    # Compile the regex pattern
    
    # Find all matches
    
    note_ids = xhs_client.get_note_ids("https://www.xiaohongshu.com/explore")
    
    # # Generate the next 10 hexadecimal numbers
    for note_id in note_ids:
        video_data = xhs_client.download_note_id(note_id)
        print(video_data)

   

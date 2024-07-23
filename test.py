import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd

# Set up options for Chrome to avoid detection
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
driver.get("https://www.xiaohongshu.com/user/profile/652a4291000000002a02a4ea")

# Wait for manual interaction
input("Press 'OK' after clicking on the videos to open in new tabs")

# Get all open tabs
tabs = driver.window_handles

# Collect URLs of all open tabs
urls = []
for tab in tabs:
    driver.switch_to.window(tab)
    urls.append(driver.current_url)

# Save URLs to an Excel file
df = pd.DataFrame(urls, columns=["URLs"])
df.to_excel("video_links.xlsx", index=False)

# Close the browser
driver.quit()

print("Links saved in 'video_links.xlsx' and browser closed.")

from core import XhsClient


# python -m pip install openpyxl requests undetected-chromedriver selenium
def main():
    # Prompt the user for the URL
    
    xhs_client = XhsClient()
    xhs_client.start()
    # xhs_client.start(url)
    

if __name__ == "__main__":
    main()

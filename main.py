from core import XhsClient

def main():
    # Prompt the user for the URL
    url = input("Enter the Xiaohongshu URL: ")
    
    xhs_client = XhsClient()
    xhs_client.start(url)
    

if __name__ == "__main__":
    main()

import os
import requests
from urllib.parse import urlparse
sds
def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")

def main():
    # Create images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Read URLs from file
    with open('static/images/image_urls.txt', 'r') as f:
        lines = f.readlines()
    
    # Process each line
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # Split URL and filename
            url, filename = line.split('#')
            url = url.strip()
            filename = filename.strip()
            
            # Download the image
            output_path = os.path.join('static/images', filename)
            download_image(url, output_path)

if __name__ == '__main__':
    main() 
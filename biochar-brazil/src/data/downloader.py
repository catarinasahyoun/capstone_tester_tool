import requests
import os

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create the folder if it doesn't exist

    filename = os.path.join(dest_folder, url.split('/')[-1])

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filename
    else:
        raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")

def download_datasets():
    # Example URLs for datasets (these should be replaced with actual dataset URLs)
    dataset_urls = [
        "https://example.com/dataset1.csv",
        "https://example.com/dataset2.csv"
    ]
    dest_folder = os.path.join(os.path.dirname(__file__), 'external')

    for url in dataset_urls:
        try:
            download_file(url, dest_folder)
            print(f"Downloaded: {url}")
        except Exception as e:
            print(e)
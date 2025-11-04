"""
Data downloader for the Biochar-Brazil project.
Downloads all required datasets (soil, biomass, etc.) into data/external/.
"""

import os
import requests
from pathlib import Path
import yaml


def load_download_urls(config_path: str = "configs/config.yaml") -> list[str]:
    """
    Load dataset URLs from config.yaml if available.
    Falls back to example URLs if not found.
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        urls = config.get("data", {}).get("external_urls", [])
        if not urls:
            raise KeyError
        return urls
    except Exception:
        print("Warning: No URLs found in config.yaml; using default example URLs.")
        return [
            "https://example.com/soil_data.csv",
            "https://example.com/biomass_data.csv"
        ]


def download_file(url: str, dest_folder: str) -> str:
    """
    Download a single file from a URL into the destination folder.
    """
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.join(dest_folder, url.split("/")[-1])

    # Skip if file already exists
    if os.path.exists(filename):
        print(f"File already exists, skipping: {filename}")
        return filename

    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded successfully: {filename}")
        return filename
    else:
        raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")


def download_datasets():
    """
    Download all required datasets defined in config.yaml or fallback list.
    """
    urls = load_download_urls()
    dest_folder = Path("data/external")

    for url in urls:
        try:
            download_file(url, dest_folder)
        except Exception as e:
            print(f"Error downloading {url}: {e}")

    print("All downloads complete.")


if __name__ == "__main__":
    download_datasets()

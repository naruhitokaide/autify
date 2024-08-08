import os
import argparse
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def download_asset(url, base_url, output_dir):
    try:
        asset_url = urljoin(base_url, url)
        response = requests.get(asset_url)
        response.raise_for_status()
        parsed_url = urlparse(asset_url)
        asset_path = os.path.join(output_dir, parsed_url.path.lstrip('/'))
        os.makedirs(os.path.dirname(asset_path), exist_ok=True)
        with open(asset_path, 'wb') as file:
            file.write(response.content)
        return parsed_url.path.lstrip('/')
    except requests.RequestException as e:
        print(f"Error downloading asset {url}: {e}")
        return None

def update_html_with_local_assets(html_content, base_url, output_dir):
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag, attr in [('link', 'href'), ('script', 'src'), ('img', 'src')]:
        for element in soup.find_all(tag):
            if element.has_attr(attr):
                asset_url = element[attr]
                local_path = download_asset(asset_url, base_url, output_dir)
                if local_path:
                    element[attr] = local_path
    return str(soup)

def extract_metadata(content):
    soup = BeautifulSoup(content, 'html.parser')
    num_links = len(soup.find_all('a'))
    num_images = len(soup.find_all('img'))
    fetch_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    return num_links, num_images, fetch_time

def main(urls, metadata, mirror):
    for url in urls:
        print(f"Fetching {url}...")
        content = fetch_url(url)
        if content:
            base_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
            output_dir = base_filename
            os.makedirs(output_dir, exist_ok=True)
            if mirror:
                content = update_html_with_local_assets(content, url, output_dir)
            html_filename = os.path.join(output_dir, base_filename + ".html")
            save_to_file(html_filename, content)
            print(f"Saved {url} to {html_filename}")
            if metadata:
                num_links, num_images, fetch_time = extract_metadata(content)
                print(f"site: {url}")
                print(f"num_links: {num_links}")
                print(f"images: {num_images}")
                print(f"last_fetch: {fetch_time}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch web pages and save them to disk.')
    parser.add_argument('urls', nargs='+', help='URLs to fetch')
    parser.add_argument('--metadata', action='store_true', help='Print metadata about fetched pages')
    parser.add_argument('--mirror', action='store_true', help='Create a local mirror with all assets')
    args = parser.parse_args()
    
    main(args.urls, args.metadata, args.mirror)

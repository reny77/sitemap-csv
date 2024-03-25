import sys
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3

# To disable SSL certificate notifications
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_sitemap(url):
    response = requests.get(url, verify=False)  # Disable SSL certificate verification.
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download sitemap from {url}")
        return None

def parse_sitemap(content):
    urls = []
    soup = BeautifulSoup(content, "lxml")  # Use lxml as the XML parser.
    for loc in soup.find_all("loc"):
        urls.append(loc.text.strip())
    return urls

def is_sitemap_index(content):
    soup = BeautifulSoup(content, "lxml")  # Use lxml as the XML parser.
    return soup.find("sitemapindex") is not None

def parse_sitemap_index(content):
    sitemap_urls = []
    soup = BeautifulSoup(content, "lxml")  # Use lxml as the XML parser.
    for loc in soup.find_all("loc"):
        sitemap_urls.append(loc.text.strip())
    return sitemap_urls

def process_sitemap(sitemap_url, parent_sitemap_url=None):
    content = download_sitemap(sitemap_url)
    if content:
        if is_sitemap_index(content):
            sitemap_urls = parse_sitemap_index(content)
            for sitemap_url in sitemap_urls:
                process_sitemap(sitemap_url, parent_sitemap_url=sitemap_url)
        else:
            urls = parse_sitemap(content)
            write_to_csv(urls, parent_sitemap_url)

def write_to_csv(urls, parent_sitemap_url=None):
    with open('sitemap_urls.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url in urls:
            if parent_sitemap_url:
                writer.writerow([parent_sitemap_url, url])
            else:
                writer.writerow(["", url])

def main(sitemap_url):
    process_sitemap(sitemap_url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <sitemap_url>")
        sys.exit(1)
    
    sitemap_url = sys.argv[1]
    main(sitemap_url)

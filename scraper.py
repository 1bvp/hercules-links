import os
import requests
from bs4 import BeautifulSoup

# Configuration
TARGET_URL = "https://hercules.app"
OUTPUT_FILE = "links.txt"

def get_links():
    try:
        response = requests.get(TARGET_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        new_links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Clean up relative links if any exist
            if href.startswith("/"):
                href = f"{TARGET_URL}{href}"
            if href.startswith("http"):
                new_links.add(href)

        return new_links
    except Exception as e:
        print(f"Error fetching page: {e}")
        return set()

def update_file(new_links):
    existing_links = set()

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            existing_links = set(line.strip() for line in f)

    all_links = existing_links.union(new_links)

    with open(OUTPUT_FILE, "w") as f:
        for link in sorted(all_links):
            f.write(f"{link}\n")

    print(f"Saved {len(all_links)} total links.")

if __name__ == "__main__":
    links = get_links()
    if links:
        update_file(links)

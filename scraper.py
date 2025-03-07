import logging
import requests
from bs4 import BeautifulSoup
import json

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("scraper.log"),
            logging.StreamHandler()
        ]
    )

def fetch_html(url):
    try:
        logging.info(f"Fetching HTML content from {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching HTML content: {e}")
        return None

def parse_html(html):
    try:
        logging.info("Parsing HTML content")
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        logging.error(f"Error parsing HTML: {e}")
        return None

def extract_data(soup):
    try:
        logging.info("Extracting data from parsed HTML")
        data = []
        for item in soup.find_all("div", class_="data-item"):
            title = item.find("h2").text if item.find("h2") else "No Title"
            link = item.find("a")["href"] if item.find("a") else "No Link"
            data.append({"title": title, "link": link})
        logging.info(f"Extracted {len(data)} items")
        return data
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return []

def save_to_json(data, filename="scraped_data.json"):
    try:
        logging.info(f"Saving data to {filename}")
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        logging.info("Data successfully saved")
    except Exception as e:
        logging.error(f"Error saving data: {e}")

def main():
    setup_logging()
    url = "https://example.com"
    html = fetch_html(url)
    if html:
        soup = parse_html(html)
        if soup:
            data = extract_data(soup)
            save_to_json(data)

if __name__ == "__main__":
    main()

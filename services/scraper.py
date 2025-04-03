import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.config.logger import logger

class Scraper:
    """Scrapes a website and its subpages, saving the data."""

    def __init__(self, website_url):
        self.website_url = website_url
        self.visited_urls = set()
        self.scraped_data = []

    def scrape(self):
        """Main function to scrape the website."""
        try:
            logger.info(f"Starting scrape for: {self.website_url}")
            self._scrape_page(self.website_url)

            if not self.scraped_data:
                logger.error("No data scraped from website.")
                return None

            # Save scraped data
            os.makedirs("app/data", exist_ok=True)
            with open("app/data/scraped_data.json", "w", encoding="utf-8") as f:
                json.dump(self.scraped_data, f, indent=4)

            logger.info("Scraping completed successfully.")
            return self.scraped_data

        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return None

    def _scrape_page(self, url):
        """Scrapes a single page and follows links to subpages."""
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Failed to fetch {url} - Status Code: {response.status_code}")
                return

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract relevant text from paragraphs
            page_text = " ".join([p.get_text() for p in soup.find_all("p")])
            self.scraped_data.append({"url": url, "content": page_text})

            # Find and scrape internal links
            for link in soup.find_all("a", href=True):
                full_link = urljoin(url, link["href"])
                if full_link.startswith(self.website_url):  # Only follow internal links
                    self._scrape_page(full_link)

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")

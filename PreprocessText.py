import time

import requests
from bs4 import BeautifulSoup
from typing import List


class URLParser():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def parse(self, urls: List[str,]) -> List[List[str,]]:
        return [self.parse_one(url) for url in urls]

    def parse_one(self, url: str) -> List[str,]:
        print("Request to site;", end=" ")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            print("Get html;", end=" ")
            soup = BeautifulSoup(response.text, 'lxml')

        except Exception as e:
            print("URL is not available, error")
            return []

        print("Parse html;")
        tags = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        links_1 = soup.find_all("a", class_=lambda x: x and ("product" in x))
        links_2 = soup.find_all("a", href=lambda h: h and "product" in h)

        link_text = [link.get_text(strip=True, separator=" ") for link in links_1] + [link.get_text(strip=True) for link in links_2]
        text = [tag.get_text(strip=True, separator=" ") for tag in tags]

        preprocessed_data = []
        for line in link_text + text:
            lower = line.lower()
            if line and line not in preprocessed_data:
                preprocessed_data.append(lower)
        return preprocessed_data

    def __del__(self):
        self.driver.quit()

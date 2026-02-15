import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from typing import List


class URLParser():
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # без окна браузера
        self.driver = webdriver.Edge(options=options)

    def parse(self, urls: List[str,]) -> List[List[str,]]:
        return [self.parse_one(url) for url in urls]

    def parse_one(self, url: str) -> List[str,]:
        print("Request to site;", end=" ")
        try:
            self.driver.get(url)
        except WebDriverException as e:
            print("URL is not available, error")
            return []
        print("Waiting;", end=" ")
        time.sleep(3)
        print("Get html;", end=" ")
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")

        print("Parse html;")
        tags = soup.find_all(['h1', 'h2', 'h3', 'h4'])
        links_1 = soup.find_all("a", class_=lambda x: x and ("product" in x))
        links_2 = soup.find_all("a", href=lambda h: h and "product" in h)

        link_text = [link.get_text(strip=True) for link in links_1] + [link.get_text(strip=True) for link in links_2]
        text = [tag.get_text(strip=True) for tag in tags]

        preprocessed_data = []
        for line in link_text + text:
            lower = line.lower()
            if line and line not in preprocessed_data:
                preprocessed_data.append(lower)
        return preprocessed_data

    def __del__(self):
        self.driver.quit()

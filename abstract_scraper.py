from bs4 import BeautifulSoup
import requests
from abc import ABC, abstractmethod

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
}


class AbstractScraper(ABC):

    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(url, headers=HEADERS).content,
                                  'html.parser')  # grab the url and use soup to parse it

    def url(self):
        return self.url

    @abstractmethod
    def title(self):
        pass

    @abstractmethod
    def ingredients(self):
        pass

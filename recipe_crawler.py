from bs4 import BeautifulSoup
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
}

class Recipe_crawl():

    def __init__(self, url):
        self.soup = BeautifulSoup(requests.get(url, headers=HEADERS).content,
                                  'html.parser')  # grab the url and use soup to parse it
        self.visited = set()

    def get_links(self):
        count = 0
        links = []
        for link in self.soup.find_all("a", class_="fixed-recipe-card__title-link"):
            links.append(link.get('href'))
            count += 1
            if count == 10:
                break
        return links

    def crawl(self,url):
        for link in self.get_links():
            if link in self.visited:
                continue




crawler = Recipe_crawl("https://www.allrecipes.com/recipes/227/world-cuisine/asian/?internalSource=hub%20nav&referringId=86&referringContentType=Recipe%20Hub&linkName=hub%20nav%20daughter&clickId=hub%20nav%202&page=4")
crawler.get_links()
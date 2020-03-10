from bs4 import BeautifulSoup
import requests
import csv
import scraping_utils as scrape_u
from abstract_scraper import AbstractScraper
from time import sleep
from random import randint
import pandas as pd

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
}


class ReciScrape(AbstractScraper):
    """
    Contains functions to scrape recipes off of allrecipes.com

    Attributes:
          ing (str): Ingredients separated by a comma.
          rtitle(str): The title of the recipe.
          list_of_ingredients (list str): list of the ingredients
    """
    ing = ""
    rtitle = ""
    list_of_ingredients = []

    def write_to_csv(self):
        """
        Writes the scraped recipe to the recipelist csv.

        """
        # updates the csv with new recipes
        listb = [self.rtitle, self.ing, self.url]
        with open('recipelist.csv', 'a', newline='') as csv_file:
            # fieldnames = ['Name', 'Ingredients', 'Link']
            csvdw = csv.writer(csv_file, delimiter='|')
            csvdw.writerow(listb)

    def title(self):
        """
            Gets the title/name of the recipe.
        """
        # returns recipe title
        # recipe title under h1 tag
        rname = self.soup.find("h1").get_text()
        self.rtitle = rname.lower()

    # adds ingredient to the list that's added to recipelist.csv
    def add_ingredient(self, ingredient):
        """
        Deprecated. Adds ingredient to list of ingredients.

        :param str ingredient: The ingredient.
        """
        self.list_of_ingredients.append(ingredient)

    # checks if an item is in the ingredients dictionary. if not prompts the user to identify the ingredient
    def is_ingredient(self, string_in):
        """
        Checks if the string is an ingredient in the list.

        Checks if the string is an ingredient is in the list. If not it prompts the user to identify the ingredient.

        :param str string_in: The string possibly containing the ingredient.
        :return: A list of confirmed ingredients.
        :rtype: list str
        """
        food_list = []
        # returns true if item is in the dictionary, false otherwise
        in_dict = scrape_u.in_dictionary(string_in)

        # if the item is not in the dictionary/ csv
        if not in_dict:

            update = int(
                input('what part of " %s " is an ingredient? \n1. all of it\n2.enter it yourself\n3. none of it'
                      '\n4. there are two items\n5. There is one item but the other should not be blacklisted\n'
                      % string_in))
            # the input is an ingredient and needs to be added to the dictionary
            if update == 1:
                new_ingred = string_in
            # only part of the input is an ingredient
            if update == 2:
                new_ingred = input("Please type in the ingredient name:\n")
                scrape_u.add_to_black_list(new_ingred, string_in)  # adds extra words to black list
            # not an ingredient exits the program
            if update == 3:
                return
                # there are two ingredients
            if update == 4:
                new_ingred = input("please enter the first item: \n")
                second_ingred = input("please enter the second item:\n")
                self.is_ingredient(second_ingred)  # with recursion it only adds the first ingredient to the recipe
            if update == 5:
                new_ingred = input("Please type in the ingredient name:\n")
                unwanted = input("Please type in the blacklist items:\n")
                scrape_u.add_to_black_list(new_ingred, unwanted)

            # check if it is in the dictionary now
            check_dict_again = scrape_u.in_dictionary(new_ingred)
            print("checked if %s is in the dictionary" % new_ingred)

            # if it's still not in the dictionary
            if not check_dict_again:
                # prompt the user for a category
                print("%s is not in the dictionary" % new_ingred)
                scrape_u.add_ingredient_to_dict(new_ingred)
                food_list.append(new_ingred)  # update the recipe

                print("%s has been added to the dictionary and the recipe will be updated!" % new_ingred)
                # return

                # if it is in the dictionary/csv
            if check_dict_again:
                print("%s is already in the dictionary and the recipe will be updated" % new_ingred)
                food_list.append(new_ingred)  # update the recipe
                # return

        if in_dict:
            print("%s is already in the dictionary!" % string_in)
            food_list.append(string_in)  # updates the recipe
            # return
        return food_list

    def ingredients(self):
        """
        Scrapes and cleans each ingredient string from the website. Then adds the ingredient to the list.

        Scrapes each ingredient string from the website. Cleans up the text and then checks if it is a food item.
        If it is a food item it will be added to the list of ingredients for the current recipe.

        """
        # returns ingredients
        # ingredients under li class="checkList__line" or span class = ingredients -item-name
        ingredient_list = []
        ingredients = self.soup.find_all("li", class_="checkList__line")
        if not ingredients:
            ingredients = self.soup.find_all("span", class_="ingredients-item-name")

        for ingredient in ingredients:
            ingredient_string = ingredient.get_text(strip=True)
            if ingredient_string not in ('Add all ingredients to list', ''):
                # normalizing the string
                normal_string = scrape_u.normalize_string(ingredient_string)
                new_ingredient = self.is_ingredient(normal_string)
                # type checking
                if new_ingredient is None:
                    continue
                else:
                    ingredient_list.extend(new_ingredient)
        # adds to list of ingredients
        self.ing = ', '.join(x for x in ingredient_list)

    def instructions(self):
        """
        Scrapes the instructions from the recipe's website.
        """
        # returns instructions
        # span class = "recipe-directions__list--item:>
        for instruct in self.soup.find_all("span", class_="recipe-directions__list--item"):
            b = instruct.get_text()
            print(b.strip())

    def scrape(self):
        """
        Scrapes the title and ingredients for the recipe and adds it to the recipe list.
        """
        self.title()
        self.ingredients()
        self.write_to_csv()


class RecipeCrawl():
    """ Class for scraping multiple recipes from allrecipes """

    def __init__(self, url):
        """
        A class for crawling through allrecipes.

        It is VERY important that the url provided to the constructor leads to a specific CATEGORY of recipe as well as
        it's PAGE #.
        e.g.
        - https://www.allrecipes.com/recipes/78/breakfast-and-brunch (indicates page 1)
        -https://www.allrecipes.com/recipes/78/breakfast-and-brunch/?page=2 or
        - https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/
        - https://www.allrecipes.com/recipes/728/world-cuisine/latin-american/mexican/?page=2

        The program will work if you only provide the homepage but it would be more efficient to crawl through each
        category and page #.
        In the future the crawler will be adjusted so it can go through all of the pages within a category on it's own
        and to crawl through each category automatically as well.

        :param string url: The link to the website's 'home' page with links to other recipes.
        """
        self.soup = BeautifulSoup(requests.get(url, headers=HEADERS).content,
                                  'html.parser')  # grab the url and use soup to parse it

    # returns a list of the urls in recipelist.csv
    def get_visited(self):
        """
        Returns a list of all the urls of previously scraped recipes.

        Gets the url of each recipe in the recipe list. Make's sure we don't scrape the same recipe twice.

        :return: List of visited urls.
        :rtype: list str
        """
        visited = []
        with open("recipelist.csv", 'r') as url_list:
            url_dict_reader = csv.DictReader(url_list, delimiter='|')

            for row in url_dict_reader:
                visited.append(row['Link'])
            # print(visited)
        return visited

    # returns a list of new urls
    def get_links(self):
        """
        Grabs all the links off of the specified allrecipes page.

        :return: A list of urls to recipes.
        :rtype: list str
        """
        count = 0
        links = []
        visited = self.get_visited()

        for linky in self.soup.find_all("a", class_="fixed-recipe-card__title-link"):
            url = linky.get('href')
            if url not in visited:
                links.append(url)
        return links


crawler = RecipeCrawl(
    "https://www.allrecipes.com/recipes/227/world-cuisine/asian/?page=4")
# loop through each link gathered from the web crawler
for link in crawler.get_links():
    scraper = ReciScrape(link)
    # pause the loop for a few seconds
    sleep(randint(1, 2))

    # scrape info off of the web page
    scraper.scrape()

# reformat the csv after adding ingredients
scrape_u.clean_ingredient_dict()

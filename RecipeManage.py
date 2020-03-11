from Recipe import Recipe
import csv


class User:
    """
    The User class is used for getting the user's ingredients to test the RecipeManager class.
    """
    ingredients = []  # ingredients list

    # def __init__(self, ingredients):
    # self.ingredients = ingredients

    def set_ingredients(self):  # fills the set of ingredients the user has
        input_string = input("Enter ingredients separated by a comma ")
        self.ingredients = [h.strip() for h in input_string.split(
            ",")]  # store list of ingredients in a set.doesn't account for white space

    def get_ingredients(self):
        return self.ingredients  # prints out the list


class RecipeManager:
    """
    The RecipeManager class is used to perform operations on and create Recipe objects.

    Attributes:
        recipes (list str): the list of Recipe objects.

    Methods:
        in_common(list1, list2)
            Returns the number of common ingredients between the user and recipe.
        add_recipes(user_list)
            Takes recipes from the csv and writes them to a list of Recipe objects while counting common ingredients.
        sort_recipes()
            Sorts the recipe list from hight to low based on the number of common ingredients.
        get_recipe_names(r_list)
            Makes a list of names from the recipe list.

    This class has 5 purposes:
    1. It creates Recipe objects and adds them to a list of recipes through the add_recipes function.
    2. It determines the number of ingredients the user's ingredient list has in common with each recipe in the recipe
        list.
    3. It sorts the list of recipes based on the number of ingredients each recipe has in common with the user.
    4. It provides the names of each recipe.
    5. It provides the number of ingredients in common.

    Purpose 4 and 5 are for future development of the GUI interface.
    """
    recipes = []  # list of recipe objects

    def in_common(self, list1, list2):
        """
        Counts the number of common ingredients between the user and recipe.

        :param list str list1: The user's ingredient list.
        :param list str list2: The recipe's ingredient list.
        :return: The number of ingredients shared between the user and the recipe.
        :rtype: int
        """
        count = 0
        for item in list1:
            if item in list2:
                count += 1

        return count

    def add_recipes(self, user_list):
        """
        Takes recipes from the csv and writes them to a list of Recipe objects while counting common ingredients.

        :param str user_list: List of the user's ingredients.
        :return: nothing.
        """
        # append recipe to the list, have recipe as a paramater
        with open('recipelist.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter='|')
            self.recipes.clear()
            for row in csv_reader:
                i = [h.strip() for h in row['Ingredients'].split(',')]
                x = self.in_common(user_list, i)
                if x > 0:
                    self.recipes.append(Recipe(row['Name'], row['Ingredients'], row['Link'], x))

    def sort_recipes(self):
        # loop through recipe list
        """
        Sorts the recipe list from high to low based on the number of common ingredients.

        :return: list of sorted recipes
        :rtype: list Recipe
        """
        g = self.recipes
        g.sort(key=lambda x: x.common, reverse=True)
        for item in g:
            if item.common == 0:
                g.remove(item)
        # for item in g:
        # print('Recipe %d is %s and has %d ingredients in common ' % (g.index(item), item.get_name(), item.common))
        return g

    def get_recipe_names(self, r_list):
        """
        Makes a list of names from the recipe list.

        :param Recipe r_list: List of Recipe objects.
        :return: List of recipe names.
        :rtype: list str
        """
        name_list = []
        for item in r_list:
            name_list.append(item.get_name())
        return name_list

    def get_link(self, r_list, r_name):
        for item in r_list:
            if item.get_name() == r_name:
                return item.get_url()



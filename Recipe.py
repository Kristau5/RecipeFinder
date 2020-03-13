class Recipe:
    """
    The Recipe Class is used for the creation of Recipe objects.

    Attributes:
        name (str): The name of the recipe.
        ingredients (str): The recipe's ingredients split by a comma (,).
        url (str): The url for the recipe.
        common (int): The number of ingredients the recipe has in common with the user's ingredient list.

    Methods:
        get_name()
            Returns the name of the recipe.
        get_url()
            Returns the url of the recipe.
    """

    def __init__(self, name, ingredient, url, common):
        """
        The constructor for Recipe class.
        :param str name: The name of the recipe.
        :param str ingredient: The ingredients of the recipe separated by a comma (,).
        :param str url:  The url for the recipe.
        :param int common: The number of ingredients the recipe has in common with the user's ingredient list.
        """
        self.name = name
        self.ingredients = ingredient.split(",")
        self.url = url
        self.common = common

    def get_name(self):
        """
        Get the name of the recipe.

        :return: The recipe's name.
        :rtype: str
        """
        return self.name  # get's the Recipe's name

    def get_url(self):
        """
        Get the url of the recipe.

        :return: The recipes url.
        :rtype: str
        """
        return self.url  # returns a string with the Recipe objects instructions.

    def get_num_common(self):
        """
        Get's the number of ingredients in common.

        :return: Number of ingredients in common.
        :rtype: int
        """
        return self.common

# test class

# recipea = Recipe( "peanut butter & jelly sandwhich ", "peanut butter, jelly, bread", "put the three together ", 2)
# print(recipea.get_name.__doc__)
# print(recipea.get_name())
# print(recipea.get_instructions())
# print(recipea.ingredients)

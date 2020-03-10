import Recipe


class UserR:
    ingredients = {}  # ingredients set

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def set_ingredients(self):  # fills the set of ingredients the user has
        input_string = input("Enter ingredients separated by a comma ")
        self.ingredients = input_string.split(",")  # store list of ingredients in a set.doesn't account for white space

    def get_ingredients(self):
        print(self.ingredients)  # prints out the set

# test the class

# newuser = UserRecipe()
# newuser.set_ingredients()
# newuser.get_ingredients()

# recipe1 = Recipe()

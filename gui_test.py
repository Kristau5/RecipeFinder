import PySimpleGUI as sg
import csv
import Recipe
from RecipeManage import RecipeManager
import webbrowser as wb

# user ingredients list
user_ingredients_list = []
possible_recipes = []


# returns a list of ingredients
def get_ingredients(category):
    """
    Get's all the ingredients from the specified category.

    :param str category: The ingredient category.
    :return: list of ingredients.
    :rtype: list str
    """
    i = []
    with open('ingredients.csv', 'r') as ingreds:
        csv_reader = csv.DictReader(ingreds)

        for row in csv_reader:
            i.append(row[category])

    test_list = list(filter(None, i))

    return test_list


def recipe_layout(pos_recipes):
    frames = []
    for recipe in pos_recipes:
        name = recipe.get_name()
        frames.append(sg.Frame(title="testing recipe frames", layout=[[sg.Text(text=name, enable_events=True)]]))

    list_frames = [frames[x:x+3] for x in range(0, len(frames), 3)]
    list_frames.append([sg.Button('Back')])

    return list_frames

def recipe_link(pos_recipes, r_name):

    for recipe in pos_recipes:
        if r_name == recipe.get_name():
            wb.open_new_tab(recipe.get_url())

def create_layout(category):
    """
    Creates the layout for window 2, containing all of the ingredients.

    :param str category: the ingredient category.
    :return: the window's layout.
    """
    checkboxes = []
    for ingredient in get_ingredients(category):
        if ingredient in user_ingredients_list:
            # if the user already selected the ingredient it will remain checked
            checkboxes.append([sg.Checkbox(ingredient, size=(30, 15), enable_events=True, default=True)])
        else:
            # otherwise it will remain unchecked
            checkboxes.append([sg.Checkbox(ingredient, size=(30, 15), enable_events=True)])
    # layout = [[sg.Column(checkboxes, scrollable=True, vertical_scroll_only=True)]]
    # will display a list of ingredients the user indicated thus far
    user_listbox = [
        [sg.Text('Your Ingredients')],
        [sg.Listbox(values=user_ingredients_list, size=(30, 15), enable_events=True,
                    select_mode=sg.SELECT_MODE_MULTIPLE, key='-listbox-')],
        [sg.Button('Remove Selected')]]

    layout_c = [
        [sg.Column(checkboxes, size=(360, 432), scrollable=True, vertical_scroll_only=True), sg.Column(user_listbox)],
        [sg.Button('Back'), sg.Button('Submit Changes')]]

    return layout_c


def update_ingredient_list(category, ingredient_dict, user_list):
    """
    Updated the ingredient list for the user.

    :param str category: The ingredient's category.
    :param ingredient_dict: The dictionary containing the ingredients to add.
    :param user_list: List of the user's ingredients.
    """
    ingredient_list = get_ingredients(category)
    # user_ingredients = user_ingredients_list
    # Searches through dict for ingredients to add.
    for key, value in ingredient_dict.items():
        if value and (key != '-listbox-') and (ingredient_list[key] not in user_ingredients_list):
            # only selects if value is true which means the ingredient was selected
            # also ignores everything in listbox
            # plus it checks if the ingredient is already in the user ingredients list
            user_ingredients_list.append(ingredient_list[key])


def remove_from_user_list(remove_list):
    """
    Removes ingredients from the user's ingredient list.

    :param list str remove_list: List of ingredients to remove.
    """
    # remove items from the user list
    for item in remove_list:
        user_ingredients_list.remove(item)
    # update the listbox


# -------- main window layout -----

col_a = [[sg.Button(i)] for i in ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat']]
col_b = [[sg.Button(i)] for i in ['Grain', 'Herbs & Spices', 'Oils', 'Condiments', 'Sauces']]
col_c = [[sg.Button(i)] for i in ['Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']]

# col_a += col_b this will make it a very long column
recipe_comp_layout = [
    [sg.T('You have these recipes in common:')],
    [sg.Listbox(values=[], size=(30, 15), enable_events=True, key='-recipe-list-box-')]
]
columns_layout = [[sg.Column(col_a), sg.Column(col_b), sg.Column(col_c)]]
# creates three columns but as such it acts as three separate containers
ingredients_layout = [
    [sg.TabGroup([[sg.Tab('Ingredients', columns_layout, key='-ingredients-tab-'), sg.Tab('Recipes', recipe_comp_layout, key='-recipe-tab-')]], enable_events=True, key='-tab-')],
    ]
# --------

# set the windows theme
sg.theme('DarkAmber')

# create the new window

window = sg.Window('Ingredient Selection', ingredients_layout, font='Courier 12')
win2_active = False
win3_active = False

field_names = ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat', 'Grain', 'Herbs & Spices', 'Oils',
               'Condiments', 'Sauces', 'Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']

while True:
    event, values = window.read()
    # event is the press of a button, the value is the weight tied to it?
    # print(event, values)
    # print(event,values)
    if event is None:
        break
    # updates the list of recipes
    if values.get('-tab-') == '-recipe-tab-' and (not win3_active):
        manager = RecipeManager()
        manager.add_recipes(user_ingredients_list)
        raw_recipes_sorted = manager.sort_recipes()
        possible_recipes = manager.get_recipe_names(raw_recipes_sorted)
        window['-recipe-list-box-'].update(values=possible_recipes)
        # print(raw_recipes_sorted[0].get_name())
        win3_active = True
        window.hide()
        layout3 = recipe_layout(raw_recipes_sorted)
        window3 = sg.Window('Recipe', layout3, font= 'Courier 12')
        while True:
            rev, rvals = window3.read()
            # print(rev)
            if rev == 'Back':
                window3.close()
                win3_active = False
                window.un_hide()
                break
            if rev:
                recipe_link(raw_recipes_sorted, rev)
    # opens the ingredient selection window
    if event in field_names and not win2_active:
        win2_active = True
        window.hide()
        layout2 = create_layout(event)
        window_b = sg.Window('Choose Ingredients', layout2, font='Courier 12')
        while True:
            ev2, vals2 = window_b.read()
            # print(ev2, vals2)
            if ev2 is None:
                break

            # returns to the 'main menu'
            if ev2 == 'Back':
                window_b.close()
                win2_active = False
                window.un_hide()
                break
            # adds the selected ingredients to the ingredient list
            if ev2 == 'Submit Changes':
                update_ingredient_list(event, vals2, user_ingredients_list)
                window_b['-listbox-'].update(values=user_ingredients_list)

            # removes the selected ingredients from the ingredient list
            if ev2 == 'Remove Selected':
                remove_from_user_list(vals2.get('-listbox-'))
                window_b['-listbox-'].update(values=user_ingredients_list)

window.close()

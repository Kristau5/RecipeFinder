import PySimpleGUI as sg
import csv
import Recipe
from RecipeManage import RecipeManager

# user ingredients list
user_ingredients_list = []
possible_recipes = []


# returns a list of ingredients
def get_ingredients(category):
    i = []
    with open('ingredients.csv', 'r') as ingreds:
        csv_reader = csv.DictReader(ingreds)

        for row in csv_reader:
            # print(row['Vegetable'])
            i.append(row[category])

    test_list = list(filter(None, i))

    return test_list


def create_layout(category):
    checkboxes = []
    for ingredient in get_ingredients(category):
        checkboxes.append([sg.Checkbox(ingredient, size=(30, 15), enable_events=True)])
    # layout = [[sg.Column(checkboxes, scrollable=True, vertical_scroll_only=True)]]
    # will display a list of ingredients the user indicated thus far
    user_listbox = [
        [sg.Text('Your Ingredients')],
        [sg.Listbox(values=user_ingredients_list, size=(30, 15), enable_events=True, key='-listbox-')],
        [sg.Button('Remove Selected')]]
    # user_checkboxes = [[sg.Checkbox(i)] for i in user_ingredients_list]
    # user_col = [[sg.Column(user_checkboxes, scrollable=True, vertical_scroll_only=True)]]
    # create the layout
    # layout_b = [[sg.TabGroup([[sg.Tab('Ingredients', layout), sg.Tab('Your Ingredients', user_listbox)]])],
    # [sg.Button('Back'), sg.Button('Submit Changes')]]
    layout_c = [
        [sg.Column(checkboxes, scrollable=True, vertical_scroll_only=True), sg.Column(user_listbox)],
        [sg.Button('Back'), sg.Button('Submit Changes')]]

    return layout_c


def update_ingredient_list(category, ingredient_dict, user_list):
    ingredient_list = get_ingredients(category)
    # user_ingredients = user_ingredients_list

    for key, value in ingredient_dict.items():
        if value:
            user_ingredients_list.append(ingredient_list[key])


# return user_ingredients


def remove_from_user_list(remove_list):
    # remove items from the user list
    for item in remove_list:
        user_ingredients_list.remove(item)
    # update the listbox


# --------

col_a = [[sg.Button(i)] for i in ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat']]
col_b = [[sg.Button(i)] for i in ['Grain', 'Herbs & Spices', 'Oils', 'Condiments', 'Sauces']]
col_c = [[sg.Button(i)] for i in ['Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']]

# col_a += col_b this will make it a very long column
recipe_comp_layout = [
    [sg.T('You have these recipes in common:')],
    [sg.Listbox(values=possible_recipes, size=(30, 15), enable_events=True, key='-recipe-list-box-')]
]
columns_layout = [[sg.Column(col_a), sg.Column(col_b), sg.Column(col_c)]]
# creates three columns but as such it acts as three separate containers
ingredients_layout = [
    [sg.TabGroup([[sg.Tab('Ingredients', columns_layout, key='-ingredients-tab-'), sg.Tab('Recipes', recipe_comp_layout, key='-recipe-tab-')]], enable_events=True, key='-tab-')],
    ]
# --------

# --- layout 2 ---
"""
col = create_layout()
layout = [[sg.Column(col, scrollable=True, vertical_scroll_only=True)],
          [sg.Text('bottom row')]]

tab_layout = [[sg.T('tab 2')]]
layout_b = [[sg.TabGroup([[sg.Tab('Tab 1', layout), sg.Tab('Tab 2', tab_layout)]])],
            [sg.Button('Back')]]
"""
# -----------------
sg.theme('DarkAmber')

# actual_layout = [sg.TabGroup([[sg.Tab('Tab 1', layout), sg.Tab('Tab 2', tab_layout)]])]

window = sg.Window('Ingredient Selection', ingredients_layout, font='Courier 12')
win2_active = False

field_names = ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat', 'Grain', 'Herbs & Spices', 'Oils',
               'Condiments', 'Sauces', 'Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']

while True:
    event, values = window.read()
    # event is the press of a button, the value is the weight tied to it?
    # print(event, values)
    if event is None:  # always,  always give a way out!
        break
    if values.get('-tab-') == '-recipe-tab-':
        # print("recipe selected")
        manager = RecipeManager()
        manager.add_recipes(user_ingredients_list)
        raw_recipes_sorted = manager.sort_recipes()
        possible_recipes = manager.get_recipe_names(raw_recipes_sorted)
        # print(possible_recipes)
        window['-recipe-list-box-'].update(values=possible_recipes)
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
            if ev2 == 'Back':
                window_b.close()
                win2_active = False
                window.un_hide()
                break
            if ev2 == 'Submit Changes':
                update_ingredient_list(event, vals2, user_ingredients_list)
                window_b['-listbox-'].update(values=user_ingredients_list)
            if ev2 == 'Remove Selected':
                remove_from_user_list(vals2.get('-listbox-'))
                window_b['-listbox-'].update(values=user_ingredients_list)

window.close()

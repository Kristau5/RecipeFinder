from textblob import TextBlob
import string
import csv
import pandas as pd

"""
A group of methods used for the cleaning of scraped ingredient text from recipe websites.

"""


def remove_other(text):
    """
    Removes all non-printable ascii characters.

    :param str text: String containing non-printable ascii characters.
    :return: String of printable ascii characters.
    :rtype: str
    """
    # removes non printable ascii characters from a string
    printable = set(string.printable)  # string of ascii characters that are considered printable
    new_text = ''.join(filter(lambda x: x in printable, text))
    return new_text


def lemma(in_string):
    """
    Returns the strings lemmatized (or dictionary) form.

    :param str in_string: String containing words in need of lemmatization.
    :return: String of lemmatized words.
    :rtype: str
    """
    # lemmatize a string
    cool_text = TextBlob(in_string)
    lemmad = ' '.join([w.lemmatize() for w in cool_text.words])
    return lemmad
    # list(lemmad.split(" "))


def remove_symbols(in_string):
    """
    Removes common symbols from the string.

    :param str in_string: String with unwanted symbols.
    :return: String without symbols.
    :rtype: str
    """
    # removes black listed characters and numbers from the given string
    bad_chars = [';', ',', '!', '(', ')', '/']
    last_string = ''.join(x for x in in_string if (not x.isdigit()) and (x not in bad_chars))
    return last_string


def get_phrases(document):  # returns a list of phrases
    """
    Creates a list of noun-phrases found in the string.

    For future use involving machine learning.

    :param str document: A string containing possible noun phrases.
    :return: List of noun phrases.
    """
    text_blob_object = TextBlob(document)
    np = text_blob_object.noun_phrases
    return np  # a list of noun phrases


def get_non_phrase(document, np):  # takes a document and noun phrases and returns non phrases as a list
    """
    Returns a list without noun phrases.

    For future use involving machine learning.

    :param str document: A string possibly containing noun phrases.
    :param np: A list of noun phrases.
    :return: A string without noun phrases.
    """
    text_blob_object = TextBlob(document)
    sentence = text_blob_object.raw_sentences
    for sent in reversed(sentence):
        for np_str in np:
            if np_str in sent:
                sentence.remove(sent)  # create a list without the noun phrase objects
            continue  # move to next iteration of the loop
    return sentence


# searches each word in the string to see if it's in the black_list
def remove_black_listed(in_string):
    """
    Removes blacklisted words from the string.

    In the future may contain custom blacklist parameter and dictionary search

    :param str in_string:  A string with possible blacklisted words.
    :return: A string without blacklisted words.
    :rtype: str
    """
    s = in_string.split()  # assign the string to a list for easy searching

    with open("black_list.txt") as bl:
        # rstrip is a string function which removes trailing white spaces (to the right)
        lines = [linex.rstrip() for linex in bl]
        for line in lines:
            if line in s:
                s.remove(line)
        new_str = " ".join(s)
        return new_str


# adds a new item to the black list
def add_to_black_list(ingredient, in_string):
    """
    Adds a new word to the blacklist.

    :param str ingredient: A string with only the approved word.
    :param str in_string: The raw string containing both the ingredient and non-ingredient words.
    """
    # splits both into a list for easier searching
    b_list_words = in_string.split(" ")
    ingredient_list = ingredient.split(" ")

    # future: have it search against ingredient dictionary as well to ensure accuracy.
    # self note: could I just use list.remove(elem) instead of looping through?
    # may result in faster runtime.
    with open("black_list.txt", 'a') as bl:
        for word in b_list_words:
            if word not in ingredient_list:
                bl.write(word + '\n')


# adds ingredient to ingredients.csv to be used in dictionary look ups
def add_ingredient_to_dict(in_string):
    """
    Adds an ingredient to the ingredient dictionary.

    Requires the user to identify the ingredients category.

    :param str in_string: The ingredient word.
    """
    categories = {
        1: 'Dairy', 2: 'Vegetable', 3: 'Fruit', 4: 'Seafood', 5: 'Meat', 6: 'Grain', 7: 'Herbs & Spices', 8: 'Oils',
        9: 'Condiments', 10: 'Sauces', 11: 'Soups', 12: 'Baking', 13: 'Nuts & Legumes', 14: 'Beverages', 15: 'Other'
    }
    field_names = ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat', 'Grain', 'Herbs & Spices', 'Oils',
                   'Condiments', 'Sauces', 'Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']
    category = int(input("Which category does the ingredient belong in?\n"
                         "1. Dairy\n2. Vegetable\n3. Fruit\n4. Seafood\n5. Meat\n6. Grain\n7.Herbs & Spices"
                         "\n8. Oils\n9. Condiments\n10. Sauces\n11. Soups\n12. Baking\n13. Nuts & Legumes\n"
                         "14. Beverages\n15. Other\n"))
    # create dictionary with the category and ingredient
    row_dict = {categories.get(category): in_string}

    with open('ingredients.csv', 'a', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=field_names)
        csv_writer.writerow(row_dict)
        file.close()


def in_dictionary(in_string):
    """
    Checks if the ingredient is in the dictionary.

    :param str in_string: The ingredient.
    :return: True if in_string is in the dictionary.
    :rtype: bool
    """
    in_dict = False
    with open('ingredients.csv', 'r') as csv_file:
        csv_dreader = csv.DictReader(csv_file)

        for row in csv_dreader:
            for key, value in row.items():
                # print(value)
                if value == in_string:
                    # print(key)
                    in_dict = True
    csv_file.close()
    return in_dict


def normalize_string(in_string):
    """
    Cleans the string of unwanted symbols, words and normalizes it for easier processing.

    :param str in_string: A string of unfiltered text.
    :return: A normalized string.
    :rtype: str
    """
    lowered = in_string.lower()
    no_symbols = remove_symbols(lowered)
    printable_string = remove_other(no_symbols)
    lemmad_string = lemma(printable_string)
    clean_string = remove_black_listed(lemmad_string)

    return clean_string


# removes all empty cells from the dictionary and shifts up
def clean_ingredient_dict():
    """
    Makes the ingredient dictionary easier to read.

    Shifts items to fill empty cells within their category.
    """
    # create a Data Frame from the csv
    df = pd.read_csv('ingredients.csv')
    data_dict = {}
    field_names = ['Dairy', 'Vegetable', 'Fruit', 'Seafood', 'Meat', 'Grain', 'Herbs & Spices', 'Oils',
                   'Condiments', 'Sauces', 'Soups', 'Baking', 'Nuts & Legumes', 'Beverages', 'Other']
    # remove all of the empty cells from the Data Frame, column by column
    for field in field_names:
        data_dict.update({field: df[field].dropna().values.tolist()})

    # have it orient by index to account for the arrays not being of the same length
    new_df = pd.DataFrame.from_dict(data_dict, orient='index')
    # transpose to reorient the data frame correctly
    fixed_df = new_df.transpose()
    # update the csv with null values removed and data shifted upwards. index = false keeps the row names away
    fixed_df.to_csv(r'ingredients.csv', index=False, header=True)

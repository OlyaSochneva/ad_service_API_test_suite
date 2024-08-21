import string
import random


def check_structure(item, structure):
    return item.keys() == structure.keys()


def return_category(response, category_name):
    categories = response['results']
    for category in categories:
        if category['name'] == category_name:
            return category


def return_card_category(card):
    category = card['category']
    return category['name']


def return_id(response_dict):
    return response_dict['id']


def compare_names(data, sample):
    names = []
    for item in data:
        names.append(item['name'])
    extra_categories = [string for string in names if string not in sample]
    missing_categories = [string for string in sample if string not in names]
    if len(missing_categories) == 0 and len(extra_categories) == 0:
        return "Correct"
    else:
        return ("Missing categories: " + ", ".join(missing_categories),
                "Extra categories: " + ", ".join(extra_categories))


def new_user_data():
    payload = {
        "email": generate_random_email(),
        "password": generate_random_string(5),
        "name": generate_random_string(5)
    }
    return payload


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_random_email():
    email = generate_random_string(5)
    email += '@test.com'
    return email

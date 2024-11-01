import string
import random


def return_user_ntf_id(response, notification_id):
    for item in response.get("results", []):
        if item.get("notification", {}).get("id") == notification_id:
            return item["id"]
    return None


def return_card_status(card):
    return card['status']


def return_is_favorite(card):
    return card['is_favorite']


def return_is_read(notification):
    return notification['is_read']


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_random_email():
    email = generate_random_string(5)
    email += '@test.com'
    return email


def generate_phone_number():
    phone_number = '89'  # чтобы номер был похож на настоящий
    for i in range(9):
        phone_number += random.choice(string.digits)
    return phone_number

# def return_category(response, category_name):
# categories = response['results']
# for category in categories:
# if category['name'] == category_name:
# return category


# def return_card_category(card):
# category = card['category']
# return category['name']


# def compare_names(data, sample):
# names = []
# for item in data:
# names.append(item['name'])
# extra_categories = [string for string in names if string not in sample]
# missing_categories = [string for string in sample if string not in names]
# if len(missing_categories) == 0 and len(extra_categories) == 0:
# return "Correct"
# else:
# return ("Missing categories: " + ", ".join(missing_categories),
# "Extra categories: " + ", ".join(extra_categories))

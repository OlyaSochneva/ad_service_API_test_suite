import string
import random
import requests

from data import URL, TestData as Test
from payloads import new_user_payload, new_card_payload



def create_card_by_test_user_and_return_id():
    payload = new_card_payload()
    response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {Test.USER_TOKEN}'}, json=payload)
    return response.json()["id"]


def return_user_ntf_id(response, notification_id):
    for item in response.get("results", []):
        if item.get("notification", {}).get("id") == notification_id:
            return item["id"]
    return None


def return_card_status(card):
    return card['status']


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

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

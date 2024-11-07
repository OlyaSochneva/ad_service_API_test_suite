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




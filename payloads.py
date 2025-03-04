from assistant_methods import generate_random_email, generate_random_string, generate_phone_number


def new_user_payload():
    payload = {
        "email": generate_random_email(),
        "first_name": generate_random_string(5),
        "phone_number": generate_phone_number(),
    }
    return payload


def new_card_payload():
    payload = {
        # "images": "",
        # "description": "",
        "title": "Test Card",
        "connect_method": "only_calls",
        "price": 1000,
        "new_or_used": "new",
        "category": 5,   # "Личные вещи"
        "city": 2        # Санкт-Петербург
    }
    return payload


def new_service_card_payload():
    payload = {
        # "images": "",
        # "description": "",
        "title": "Test Service Card",
        "connect_method": "only_calls",
        "price": 1000,
        "price_type": "per_unit",
        "category": 81,  # «Обучение и курсы - иностранные языки»
        "city": 2        # Санкт-Петербург
    }
    return payload


def notification_payload(user_id):
    payload = {
        "title": "test notification",
        "description": "test notification",
        "users": [user_id]
    }
    return payload


def read_notification_payload():
    return {
        "is_read": True
    }


def unread_notification_payload():
    return {
        "is_read": False
    }


def start_dialog_payload(card_id):
    return {
        "card": card_id
    }


def send_message(dialog_id, text):
    payload = {
        "dialog": dialog_id,
        "text": text
    }
    return payload




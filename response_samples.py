class Sample:
    USER_STRUCTURE = {
        "id": "",
        "email": "",
        "first_name": "",
        "last_name": "",
        "phone_number": "",
        "avatar": "",
        "date_joined": "",
        "count_cards": "",
        "count_notifications": ""
    }
    CATEGORY_STRUCTURE = {
        "id": "",
        "name": "",
        "slug": "",
        "big_parent": "",
        "children": [],
        "image": ""
    }
    CARD_STRUCTURE = {
        "id": "",
        "image": [],
        "author": {},
        "is_favorite": "",
        "favorite_count": "",
        "promo": "",
        "title": "",
        "description": "",
        "created_at": "",
        "active_at": "",
        "views": "",
        "connect_method": "",
        "status": "",
        "price": "",
        "price_type": "",
        "new_or_used": "",
        "need_correct": "",
        "comment": "",
        "category": {},
        "city": {}
    }

    SERVICE_CARD_STRUCTURE = {
        "id": "",
        "image": [],
        "author": {},
        "is_favorite": "",
        "favorite_count": "",
        "promo": "",
        "title": "",
        "description": "",
        "created_at": "",
        "active_at": "",
        "views": "",
        "connect_method": "",
        "status": "",
        "price": "",
        "price_type": "",
        "need_correct": "",
        "comment": "",
        "category": {},
        "city": {}
    }
    AUTHOR_STRUCTURE = {
        "id": "",
        "first_name": "",
        "last_name": "",
        "date_joined": "",
        "count_cards": ""
    }
    CITY_STRUCTURE = {
        "id": "",
        "name": "",
        "country": "",
        "region": ""
    }
    DIALOG_STRUCTURE = {
        "id": "",
        "user1": "",
        "user2": "",
        "card": "",
        "created_at": "",
        "last_message": ""
    }
    NOTIFICATION_CREATED_STRUCTURE = {
        "id": "",
        "title": "",
        "description": "",
        "created_at": "",
        "users": []
    }
    NOTIFICATION_STRUCTURE = {
        "id": "",
        "notification": {},
        "user_notification": {},
        "is_read": ""
    }


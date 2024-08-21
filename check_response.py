from response_samples import Sample
from data import Data
from assistant_methods import check_structure
from assistant_methods import return_id
from assistant_methods import return_category
from assistant_methods import compare_names
from assistant_methods import return_card_category


def check_response_structure(response, check_method, sample):
    if response.keys() != Sample.LIST_STRUCTURE.keys():
        return "Wrong response structure"
    data = response['results']
    errors = []
    for item in data:
        if not check_method(item, sample):
            errors.append(f"Wrong structure in id '{item['id']}'")
    if errors:
        for error in errors:
            print(error)
        return "Wrong response structure"
    return "Correct"


def check_category(category, category_sample):
    if not check_structure(category, category_sample):
        return False
    if len(category['children']) > 0:
        for child in category['children']:
            if not check_category(child, category_sample):
                return False
    return True


def check_card(card, type_of_card_sample):
    return (
            check_structure(card, type_of_card_sample) and
            check_structure(card['author'], Sample.AUTHOR_STRUCTURE) and
            check_structure(card['city'], Sample.CITY_STRUCTURE))


def check_user(user, user_sample):
    return check_structure(user, user_sample)


def check_city(city, city_sample):
    return check_structure(city, city_sample)


def check_cards_category(response, category_name):
    errors = []
    for card in response['results']:
        card_category = return_card_category(card)
        if card_category != category_name:
            errors.append(f"У карточки id {card['id']} другая категория: {card_category}")
    if errors:
        for error in errors:
            print(error)
        return "Wrong data in response"
    return "Correct"


def check_values(response_dict, sample):
    errors = []
    for key in response_dict:
        if response_dict[key] != sample[key]:
            errors.append(f"Значение '{key}' отличается от образца: {response_dict[key]} != {sample[key]}")
    if errors:
        for error in errors:
            print(error)
        return "Wrong data in response"
    return "Correct"


def check_id(response_dict, id_sample):
    item_id = return_id(response_dict)
    if item_id != id_sample:
        print(f"В ответе другой id: {item_id} != {id_sample}")
        return "Wrong id in response"
    return "Correct"


def check_categories_names(response):
    categories = response['results']
    return compare_names(categories, Data.CATEGORIES_LIST)


def check_subcategories_names(response, category_name, names_list_sample):
    parent_category = return_category(response, category_name)
    subcategories = parent_category['children']
    return compare_names(subcategories, names_list_sample)

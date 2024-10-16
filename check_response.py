from response_samples import Sample


def check_structure(item, sample):
    item_id = return_id(item)
    result = "Correct"
    for key in sample.keys():
        if key not in item.keys():
            print(f'Missing key "{key}" in id {item_id}')
            result = "Wrong response structure"
    for key in item.keys():
        if key not in sample.keys():
            print(f'Extra key "{key}" in id {item_id}')
            result = "Wrong response structure"
    return result


def check_list_structure(response, check_method, sample):
    errors_found = False
    if set(response.keys()) != set(Sample.LIST_STRUCTURE.keys()):
        return "Wrong list structure"
    data = response['results']
    if len(data) == 0:
        return "Empty list"
    for item in data:
        if check_method(item, sample) == "Wrong response structure":
            errors_found = True
    return "Wrong response structure" if errors_found else "Correct"


def return_id(response_dict):
    return response_dict['id']


def check_card(card, type_of_card_sample):
    errors_found = False
    if check_structure(card, type_of_card_sample) == "Wrong response structure":
        errors_found = True
    if check_structure(card['author'], Sample.AUTHOR_STRUCTURE) == "Wrong response structure":
        errors_found = True
    if check_structure(card['city'], Sample.CITY_STRUCTURE) == "Wrong response structure":
        errors_found = True
    return "Wrong response structure" if errors_found else "Correct"

# def check_category(category, category_sample):
# if not check_item_structure(category, category_sample):
# return False
# if len(category['children']) > 0:
# for child in category['children']:
# if not check_category(child, category_sample):
# return False
# return True


# def check_values(item, sample):
# if not check_item_structure(item, sample):
# return "Wrong response structure"
# errors = []
# for key in item:
# if item[key] != sample[key]:
# errors.append(f"Значение '{key}' отличается от образца: {item[key]} != {sample[key]}")
# if errors:
# for error in errors:
# print(error)
# return "Wrong data in response"
# return "Correct"


# def check_cards_category(response, category_name):
# errors = []
# for card in response['results']:
# card_category = return_card_category(card)
# if card_category != category_name:
# errors.append(f"У карточки id {card['id']} другая категория: {card_category}")
# if errors:
# for error in errors:
# print(error)
# return "Wrong data in response"
# return "Correct"


# def check_categories_names(response):
# categories = response['results']
# return compare_names(categories, Data.CATEGORIES_LIST)


# def check_subcategories_names(response, category_name, sample):
# parent_category = return_category(response, category_name)
# subcategories = parent_category['children']
# return compare_names(subcategories, sample)

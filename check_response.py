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
    if "results" in response:
        data = response['results']
    else:
        data = response
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



import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import new_card_payload
from response_samples import Sample
from check_response import check_item_structure


class TestCreateCard:
    @allure.title('С корректными данными можно создать новое объявление')
    def test_create_card_success(self, new_user_id_and_token):
        token = new_user_id_and_token["token"]
        payload = new_card_payload()
        response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {token}'}, json=payload)
        print(response.json())
        response_structure = check_item_structure(response.json(), Sample.CARD_STRUCTURE)
        assert (response.status_code == 201 and response_structure == "Correct")

    @allure.title('Нельзя создать объявление, если не передать токен или передать невалидный')
    @pytest.mark.parametrize('headers, error_message', [
        ({'Authorization': f'Bearer {generate_random_string(15)}'}, Message.INVALID_TOKEN),
        (None, Message.CREDENTIALS_NOT_FOUND)])
    def test_create_card_unauthorized_causes_error(self, headers, error_message):
        payload = new_card_payload()
        response = requests.post(URL.CARDS, headers=headers, json=payload)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Нельзя создать объявление, если одно из обязательных полей в теле запроса отсутствует')
    @pytest.mark.parametrize('deleted_field', ["title", "connect_method", "category", "city"])
    def test_create_new_card_without_required_field_causes_error(self, new_user_id_and_token, deleted_field):
        token = new_user_id_and_token["token"]
        payload = new_card_payload()
        payload.pop(deleted_field)
        response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {token}'}, json=payload)
        print(response.json())
        assert (response.status_code == 400 and Message.REQUIRED_FIELD in str(response.json()))

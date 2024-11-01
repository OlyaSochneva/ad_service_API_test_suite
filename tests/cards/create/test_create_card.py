import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import new_card_payload
from response_samples import Sample
from check_response import check_structure


class TestCreateCard:
    @allure.title('С корректными данными можно создать новое объявление')
    def test_create_card_success(self, user_token):
        payload = new_card_payload()
        response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {user_token}'}, json=payload)
        #print(response.json())
        response_structure = check_structure(response.json(), Sample.CARD_STRUCTURE)
        assert (response.status_code == 201 and response_structure == "Correct")

    @allure.title('(401)Нельзя создать объявление с отсут./невалидным токеном')
    @pytest.mark.parametrize('headers, error_message', [
        ({'Authorization': f'Bearer {generate_random_string(15)}'}, Message.INVALID_TOKEN),
        (None, Message.CREDENTIALS_NOT_FOUND)])
    def test_create_card_unauthorized_causes_error(self, headers, error_message):
        payload = new_card_payload()
        response = requests.post(URL.CARDS, headers=headers, json=payload)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(400)Нельзя создать объявление, если одно из обязательных полей отсутствует')
    @pytest.mark.parametrize('deleted_field', ["title", "connect_method", "price", "new_or_used",
                                               "category", "city"])
    def test_create_new_card_without_required_field_causes_error(self, user_token, deleted_field):
        payload = new_card_payload()
        payload.pop(deleted_field)
        response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {user_token}'}, json=payload)
        assert (response.status_code == 400 and Message.REQUIRED_FIELD in str(response.json()))

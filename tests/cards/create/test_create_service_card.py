import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import new_service_card_payload
from response_samples import Sample
from check_response import check_structure


#                                        POST /api/cards/services/
class TestCreateServiceCard:
    @allure.title('С корректными данными можно создать новое объявление услуги')
    def test_create_service_card_success(self, user_token):
        payload = new_service_card_payload()
        response = requests.post(URL.SERVICE_CARDS, headers={'Authorization': f'Bearer {user_token}'}, json=payload)
        response_structure = check_structure(response.json(), Sample.SERVICE_CARD_STRUCTURE)
        assert (response.status_code == 201 and response_structure == "Correct")

    @allure.title('(401)Нельзя создать объявление услуг с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN),
        (None, Message.CREDENTIALS_NOT_FOUND)])
    def test_create_service_card_unauthorized_causes_error(self, wrong_headers, error_message):
        payload = new_service_card_payload()
        response = requests.post(URL.SERVICE_CARDS, headers=wrong_headers, json=payload)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('Нельзя создать объявление услуги, если одно из обязательных полей в теле запроса отсутствует')
    @pytest.mark.parametrize('deleted_field', ["title", "connect_method", "price",
                                               "price_type", "category", "city"])
    def test_create_new_service_card_without_required_field_causes_error(self, user_token, deleted_field):
        payload = new_service_card_payload()
        payload.pop(deleted_field)
        response = requests.post(URL.SERVICE_CARDS, headers={'Authorization': f'Bearer {user_token}'}, json=payload)
        # print(response.json())
        assert response.status_code == 400









import allure
import pytest
import requests

from assistant_methods import new_card_payload
from data import URL, Message, TestData as Test


class TestCreateCard:
    @allure.title('POST/api/cards/: с корректными данными можно создать новое объявление')
    def test_create_card_success(self, new_user_id_and_token):
        token = new_user_id_and_token["token"]
        payload = new_card_payload()
        response = requests.post(URL.CARDS, headers={'Authorization': f'Bearer {token}'}, json=payload)
        print(response.json())
        assert response.status_code == 201

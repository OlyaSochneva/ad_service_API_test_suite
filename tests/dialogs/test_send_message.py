import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import Message
from admin_data import URL


class TestSendMessage:

    @allure.title('Покупатель может отправить первое сообщение в диалог')
    def test_send_first_message_by_buyer_success(self, new_dialog):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {new_dialog["buyer"]}"},
                                 json={"text": "pu-pu-pu"})
        assert response.status_code == 201

    @allure.title('Продавец может отправить сообщение в диалог')
    def test_send_message_by_seller_success(self, dialog):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {dialog["seller"]}"},
                                 json={"text": "pam-pam-pam"})
        assert response.status_code == 200

    @allure.title('(400)Нельзя отправить пустое сообщение в диалог')
    def test_send_empty_message_to_dialog_causes_error(self, dialog):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {dialog["buyer"]}"},
                                 json={"text": ""})
        assert response.status_code == 400

    @allure.title('(401)Нельзя отправить сообщение в диалог с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_send_message_unauthorized_causes_error(self, wrong_headers, error_message, dialog):
        response = requests.post(URL.MESSAGE, headers=wrong_headers, json={"text": "Alarm"})
        assert (response.status_code == 401 and error_message in str(response.json()))


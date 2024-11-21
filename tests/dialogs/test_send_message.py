import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import send_message
from tests.dialogs.test_create_dialog import BUYER, SELLER, DIALOG_ID


#                                  !!!CREATE DIALOG FIRST!!!
class TestSendMessage:
    @pytest.mark.order(1)
    @allure.title('Покупатель может отправить сообщение в созданный диалог')
    def test_send_message_by_buyer_success(self):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {BUYER}"},
                                 json=send_message(DIALOG_ID, "pu-pu-pu"))
        # print(response.json())
        assert response.status_code == 201

    @pytest.mark.order(2)
    @allure.title('Продавец может отправить сообщение в созданный диалог')
    def test_send_message_by_seller_success(self):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {SELLER}"},
                                 json=send_message(DIALOG_ID, "pam-pam-pam"))
        # print(response.json())
        assert response.status_code == 201

    @allure.title('(403)Нельзя отправить сообщение в чужой существующий диалог')
    def test_send_message_to_someone_else_dialog_causes_error(self):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {BUYER}"},
                                 json=send_message(DIALOG_ID - 1, "Alarm"))
        #print(response.json())
        assert response.status_code == 403

    @allure.title('(400)Нельзя отправить пустое сообщение в диалог')
    def test_send_empty_message_to_dialog_causes_error(self):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {BUYER}"},
                                 json=send_message(DIALOG_ID, None))
        #print(response.json())
        assert response.status_code == 400

    @allure.title('(401)Нельзя отправить сообщение в диалог с отсут./невалидным токеном')
    @pytest.mark.order(3)
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_send_message_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.post(URL.MESSAGE, headers=wrong_headers,
                                 json=send_message(DIALOG_ID, "Alarm"))
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(400)Нельзя отправить сообщение в диалог с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id', ["6666666666", "pu-pu-pu", None])
    def test_send_message_by_incorrect_dialog_id_causes_error(self, wrong_id):
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {BUYER}"},
                                 json=send_message(wrong_id, "Alarm"))
        assert response.status_code == 400

    @allure.title('(400)Нельзя отправить сообщение в диалог, если одно из обязательных полей отсутствует')
    @pytest.mark.parametrize("deleted_field", ["dialog", "text"])
    def test_send_message_by_incorrect_dialog_id_causes_error(self, deleted_field):
        payload = send_message(DIALOG_ID, "Alarm")
        payload.pop(deleted_field)
        response = requests.post(URL.MESSAGE, headers={"Authorization": f"Bearer {BUYER}"}, json=payload)
        assert response.status_code == 400

import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message
from payloads import start_dialog_payload


def test_get_card_and_seller_token(basic_card):
    print(f'Card id: {basic_card["id"]}')
    print(f'Seller token: {basic_card["token"]}')


def test_get_buyer_token(user_refresh_token):
    print(f'Buyer token: {user_refresh_token}')


SELLER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjIxODUyOCwiaWF0IjoxNzMyMTMyMTI4LCJqdGkiOiI2MzU4ODU5NDMyYjA0MDljYmJhM2Q0NWZlYjU3N2Q2MCIsImlkIjo1NH0.fueCfW3VAouMguWNZfKGLX9csxpiASebYfzgO5GibXY"

CARD_ID = "426"

BUYER = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjIxODU2MiwiaWF0IjoxNzMyMTMyMTYyLCJqdGkiOiI4YjU5YmZhZTUzZjc0N2Y4ODA2ZDA3N2RiNDRlNTA4ZiIsImlkIjo1NX0.PQMW1sllmt6eOj4vS-OhPTfvYBNHdD5IMd3f54cTz7o"

DIALOG_ID = 9


#                              !!!CHECK CARD STATUS BEFORE RUN!!!
#                                  !!!CARD SHOULD BE ACTIVE!!!

class TestCreateDialog:
    @pytest.mark.order(1)
    @allure.title('С корректными данными можно создать диалог')
    def test_create_dialog_success(self):
        response = requests.post(URL.DIALOGS + "/create/", headers={"Authorization": f"Bearer {BUYER}"},
                                 json=start_dialog_payload(CARD_ID))
        print(response.json())
        assert response.status_code == 201

    @allure.title('(400)Нельзя создать диалог по своему объявлению (с самим собой)')
    def test_create_dialog_with_yourself_causes_error(self):
        response = requests.post(URL.DIALOGS + "/create/", headers={"Authorization": f"Bearer {SELLER}"},
                                 json=start_dialog_payload(CARD_ID))
        assert response.status_code == 400

    @allure.title('(401)Нельзя создать диалог с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_create_dialog_unauthorized_causes_error(self, wrong_headers, error_message):
        response = requests.post(URL.DIALOGS + "/create/", headers=wrong_headers, json=start_dialog_payload(CARD_ID))
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(401)Нельзя создать диалог к карточке с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id', ["6666666666", "pu-pu-pu", None])
    def test_create_dialog_by_incorrect_card_id_causes_error(self, wrong_id):
        response = requests.post(URL.DIALOGS + "/create/", headers={"Authorization": f"Bearer {BUYER}"},
                                 json=start_dialog_payload(wrong_id))
        assert response.status_code == 400

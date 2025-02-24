import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import Message
from admin_data import URL


class TestCreateDialog:
    @allure.title('С корректными данными можно создать диалог')
    def test_create_dialog_success(self, create_dialog):
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["buyer"]}"},
                                 json={"card": create_dialog["id"]})
        assert response.status_code == 201

    @allure.title('Нельзя создать диалог к архивному объявлению')
    def test_create_dialog_for_archive_card_causes_error(self, create_dialog):
        requests.post(URL.CARDS + str(create_dialog["id"]) + "/archive/",
                      headers={'Authorization': f'Bearer {create_dialog["seller"]}'})
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["buyer"]}"},
                                 json={"card": create_dialog["id"]})
        assert (response.status_code == 400 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('Нельзя создать диалог к объявлению на модерации')
    def test_create_dialog_for_moderate_card_causes_error(self, create_dialog, admin_token):
        requests.post(URL.CARDS + str(create_dialog["id"]) + "/change_status/",
                      headers={'Authorization': f'Bearer {admin_token}'})
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["buyer"]}"},
                                 json={"card": create_dialog["id"]})
        assert (response.status_code == 400 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('(400)Нельзя создать диалог по своему объявлению (с самим собой)')
    def test_create_dialog_with_yourself_causes_error(self, create_dialog):
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["seller"]}"},
                                 json={"card": create_dialog["id"]})
        assert response.status_code == 400

    @allure.title('(401)Нельзя создать диалог с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_create_dialog_unauthorized_causes_error(self, wrong_headers, error_message, create_dialog):
        response = requests.post(URL.DIALOGS + "/create/", headers=wrong_headers,
                                 json={"card": create_dialog["id"]})
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(401)Нельзя создать диалог к карточке с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id', ["6666666666", "pu-pu-pu", None])
    def test_create_dialog_by_incorrect_card_id_causes_error(self, wrong_id, create_dialog):
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["buyer"]}"},
                                 json={"card": wrong_id})
        assert response.status_code == 400

    @allure.title('(401)Нельзя создать диалог, если не передать тело запроса')
    def test_create_dialog_without_payload_causes_error(self, create_dialog):
        response = requests.post(URL.DIALOGS + "/create/",
                                 headers={"Authorization": f"Bearer {create_dialog["buyer"]}"})
        assert response.status_code == 400

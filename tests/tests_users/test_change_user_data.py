import allure
import pytest
import requests

from data import URL, Message, TestData as Test
from check_response import check_id


class TestChangeUserData:
    def test_change_user_data(self, new_user_id_and_token):
        token = new_user_id_and_token["token"]
        print(token)
        payload = {
            "avatar": "changed"
        }
        response = requests.patch(URL.USER_ME, headers={'Authorization': f'Bearer {token}'}, json=payload)
        print(response.json())
        assert response.status_code == 400


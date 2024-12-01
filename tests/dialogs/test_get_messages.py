import allure
import pytest
import requests

from assistant_methods import generate_random_string
from data import URL, Message


class TestGetMessages:
    @allure.title('Можно получить сообщения')
    def test_get_dialogs_success(self, dialog):
        response = requests.get(URL.DIALOGS,
                                headers={"Authorization": f"Bearer {dialog["buyer"]}"})
        assert response.status_code == 200

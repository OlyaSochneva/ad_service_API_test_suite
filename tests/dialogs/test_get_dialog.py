import allure
import pytest
import requests

from data import URL
from tests.dialogs.test_create_dialog import BUYER, SELLER, DIALOG_ID


#                                  !!!CREATE DIALOG FIRST!!!

class TestGetDialog:
    @allure.title('Оба участника могут получить диалог')
    @pytest.mark.parametrize("participant", [BUYER, SELLER])
    def test_get_dialog_by_author_success(self, participant):
        response = requests.get(URL.DIALOGS + str(DIALOG_ID) + "/messages/",
                                headers={"Authorization": f"Bearer {participant}"})
        print(response.json())
        assert response.status_code == 200

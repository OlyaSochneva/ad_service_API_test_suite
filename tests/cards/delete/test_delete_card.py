import allure
import pytest
import requests

from data import URL, Message
from response_samples import Sample
from check_response import check_structure, return_id


def test_create_card(basic_card):
    print(basic_card)


CARD_ID = ""

TOKEN = ""


class TestDeleteCard:
    def test_delete_card_success(self, basic_card):
        response = requests.delete(URL.CARDS + str(basic_card["id"]) + "/",
                                   headers={'Authorization': f'Bearer {basic_card["token"]}'})
        #print(basic_card["id"])
        #print(response.json())
        assert response.status_code == 204






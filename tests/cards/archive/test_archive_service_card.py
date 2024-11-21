import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


class TestArchiveServiceCard:
    @allure.title('Пользователь может перевести свою карточку услуг в архив')
    def test_archive_card_by_user_success(self, service_card):
        response = requests.post(URL.CARDS + service_card["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {service_card["token"]}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('(404)Пользователь не может архивировать свою карточку услуг, если она уже в архиве')
    def test_archive_card_twice_by_user_causes_error(self, archive_service):
        response = requests.post(URL.CARDS + archive_service["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {archive_service["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

import allure
import pytest
import requests

from assistant_methods import return_card_status, generate_random_string
from data import URL, Message


class TestArchiveServiceCard:
    @allure.title('Пользователь может перевести свою карточку услуг в архив')
    def test_archive_service_card_success(self, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {active_service["token"]}'})
        status = return_card_status(response.json())
        assert response.status_code == 200 and status == "archive"

    @allure.title('(404)Пользователь не может архивировать свою карточку услуг, если она уже в архиве')
    def test_archive_service_card_twice_causes_error(self, archive_service):
        response = requests.post(URL.SERVICE_CARDS + archive_service["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {archive_service["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('Пользователь не может перевести в архив карточку услуг на модерации')
    def test_archive_service_card_on_moderation_causes_error(self, service_card):
        response = requests.post(URL.SERVICE_CARDS + service_card["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {service_card["token"]}'})
        assert (response.status_code == 404 and Message.CARD_NOT_ACTIVE in str(response.json()))

    @allure.title('Пользователь не может перевести чужую активную карточку услуг в архив')
    def test_archive_another_user_service_card_causes_error(self, user_token, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/archive/",
                                 headers={'Authorization': f'Bearer {user_token}'})
        assert (response.status_code == 403 and Message.NOT_SUFFICIENT_RIGHTS in str(response.json()))

    @allure.title('(401)Нельзя архивировать карточку услуг с отсут./невалидным токеном')
    @pytest.mark.parametrize('wrong_headers, error_message', [
        (None, Message.CREDENTIALS_NOT_FOUND),
        ({'Authorization': f'Bearer {generate_random_string(10)}'}, Message.INVALID_TOKEN)])
    def test_archive_service_card_unauthorized_causes_error(self, wrong_headers, error_message, active_service):
        response = requests.post(URL.SERVICE_CARDS + active_service["id"] + "/archive/", headers=wrong_headers)
        assert (response.status_code == 401 and error_message in str(response.json()))

    @allure.title('(404/400)Пользователь не может архивировать карточку услуг с несуществующим/невалидным id')
    @pytest.mark.parametrize('wrong_id, status_code, error_message', [
        ("6666666666", 404, Message.NON_EXISTENT_CARD),
        ("pu-pu-pu", 400, Message.INVALID_ID)])
    def test_archive_service_card_with_incorrect_id_causes_error(self, wrong_id, status_code,
                                                                 error_message, active_service):
        response = requests.post(URL.SERVICE_CARDS + wrong_id + "/archive/",
                                 headers={'Authorization': f'Bearer {active_service["token"]}'})
        assert (response.status_code == status_code and error_message in str(response.json()))


